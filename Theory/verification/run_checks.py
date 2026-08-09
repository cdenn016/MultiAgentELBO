#!/usr/bin/env python3
"""Deterministic numerical corroborations for gauge_vfe_rg.

The checks in this file are deliberately narrower than theorems.  A PASS means
that the named, current protocol met its declared numerical endpoint.  It does
not prove a mathematical statement and it does not recreate an incompletely
specified historical run.
"""

from __future__ import annotations

import argparse
import base64
import copy
import csv
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import importlib.abc
import importlib.machinery
import importlib.util
import json
import math
import os
import platform
import re
import stat
import subprocess
import sys
import tempfile
import time
import traceback
import uuid
from collections import namedtuple
from contextvars import ContextVar
from dataclasses import asdict, is_dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable


_FIXED_SITE_PACKAGES = Path(
    r"C:\Users\chris and christine\AppData\Roaming\Python\Python314\site-packages"
)
_FIXED_USER_BASE = Path(
    r"C:\Users\chris and christine\AppData\Roaming\Python"
)


def _bootstrap_fixed_site_packages() -> None:
    """Admit one non-reparse package root under isolated Python startup."""

    absolute = Path(os.path.abspath(os.fspath(_FIXED_SITE_PACKAGES)))
    parts = absolute.parts
    current = Path(parts[0])
    for part in parts[1:]:
        current /= part
        metadata = current.lstat()
        attributes = getattr(metadata, "st_file_attributes", 0)
        reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        if stat.S_ISLNK(metadata.st_mode) or bool(attributes & reparse_flag):
            raise RuntimeError(
                f"fixed isolated Python package path is reparse-mediated at {current}"
            )
    if not absolute.is_dir():
        raise RuntimeError(
            f"fixed isolated Python package path is not a directory: {absolute}"
        )
    if str(_FIXED_SITE_PACKAGES) not in sys.path:
        sys.path.append(str(_FIXED_SITE_PACKAGES))


if sys.flags.isolated == 1:
    _bootstrap_fixed_site_packages()


HERE = Path(__file__).resolve().parent
TEX_ROOT = HERE.parent
REPO_ROOT = TEX_ROOT.parents[1]
CLAIMS_PATH = HERE / "claims.json"
RUNNER_PATH = Path(__file__).resolve()
VERIFICATION_PATH = HERE / "VERIFICATION.md"
REQUIREMENTS_PATH = HERE / "requirements.txt"
RESULT_SCHEMA_PATH = HERE / "result.schema.json"
MANIFEST_POLICY_PATH = HERE / "manifest-policy.json"
LIFECYCLE_GATE_PATH = HERE / "lifecycle_gate.py"
BUILD_AUDIT_PATH = HERE / "build_audit.py"
NUMERICAL_TOKEN = r"\status{NUMERICAL}"
FLOAT_TOL = 1.0e-10
FACTORIZATION_PROTOCOL_SEED = 20260803
FACTORIZATION_PROTOCOL_CONDITIONS = (
    1.0,
    1.0e2,
    1.0e4,
    1.0e6,
    1.0e8,
    1.0e10,
    1.0e12,
    1.0e14,
)
FACTORIZATION_PROTOCOL_STRATUM_COUNTS = {
    "general": 2400,
    "exact_block_diagonal": 200,
    "near_decoupled": 200,
    "scale": 120,
    "permutation": 120,
    "nested_refinement": 80,
    "mpmath_100_digit": 18,
}
FACTORIZATION_CONDITIONING_TRIGGER = 1.0e-4
FACTORIZATION_BOUNDARY_WITNESS = (
    (0.012995137302571503, -0.08809796529646897, -0.01062753379868217, 0.07034656148572713),
    (-0.08809796529646897, 0.5974163750322803, 0.07207680102574178, -0.47702552029541695),
    (-0.01062753379868217, 0.07207680102574178, 0.008696311837782767, -0.05755126421432782),
    (0.07034656148572713, -0.47702552029541695, -0.05755126421432782, 0.3808968174377439),
)
FACTORIZATION_BOUNDARY_WITNESS_DIGEST = (
    "45310a74550d3759fed0f83f71a6cf3b0f45942499361d723a2248bbe243e2e3"
)
FACTORIZATION_BOUNDARY_WITNESS_GAP = 22.777105858844084
FACTORIZATION_BOUNDARY_WITNESS_EXCURSION = 4.440892098500626e-16
FACTORIZATION_BOUNDARY_WITNESS_ALLOWANCE = 9.432369402326953e-16


ISSUE_CODES = frozenset(
    {
        "RESULT_IO",
        "RESULT_CHANGED_DURING_VERIFY",
        "INVALID_UTF8",
        "DUPLICATE_JSON_KEY",
        "MALFORMED_JSON",
        "NONFINITE_JSON",
        "NONCANONICAL_RESULT_BYTES",
        "SCHEMA_VIOLATION",
        "SEMANTIC_DIGEST_MISMATCH",
        "SEMANTIC_RECOMPUTATION_MISMATCH",
        "RESULT_STATUS_NOT_PASS",
        "MANIFEST_POLICY_INVALID",
        "UNEXPECTED_GOVERNED_PATH",
        "MISSING_GOVERNED_PATH",
        "MANIFEST_PATH_SET_MISMATCH",
        "MANIFEST_ENTRY_MISMATCH",
        "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
        "SOURCE_REVISION_FORMAT",
        "SOURCE_REVISION_NOT_FOUND",
        "SOURCE_REVISION_NOT_ANCESTOR",
        "SOURCE_BLOB_MISSING",
        "SOURCE_BLOB_TYPE",
        "SOURCE_BLOB_MISMATCH",
        "GIT_METADATA_OVERRIDE",
        "EXECUTABLE_IDENTITY",
        "PROTOCOL_PROFILE_MISMATCH",
        "CHECK_ID_UNKNOWN",
        "CHECK_ID_MISSING",
        "CHECK_ID_DUPLICATE",
        "CHECK_ID_ORDER",
        "CHECK_STATUS_NOT_PASS",
        "OVERALL_STATUS_INCONSISTENT",
        "RECOMPUTATION_EXCEPTION",
        "REPORT_TARGET_CONFLICT",
        "ATOMIC_SERIALIZATION",
        "ATOMIC_WRITE",
        "ATOMIC_REPLACE",
    }
)


VerificationIssue = namedtuple(
    "VerificationIssue",
    ["code", "location", "message", "expected", "observed"],
    defaults=[None, None],
)
VerificationIssue.__doc__ = "One stable, machine-readable verification diagnostic."

VerificationReport = namedtuple(
    "VerificationReport",
    [
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
    ],
)
VerificationReport.__doc__ = "Immutable outcome of a nonmutating result verification."


class VerificationFailure(ValueError):
    """Construction-time failure with a stable issue classification."""

    def __init__(
        self,
        code: str,
        location: str,
        message: str,
        *,
        expected: Any = None,
        observed: Any = None,
    ) -> None:
        if code not in ISSUE_CODES:
            raise ValueError(f"unknown verification issue code: {code}")
        super().__init__(message)
        self.code = code
        self.location = location
        self.expected = expected
        self.observed = observed


class ManifestPolicyError(VerificationFailure):
    """The governed-input policy or discovered tree is invalid."""


class NonFiniteJsonError(ValueError):
    """A JSON value contains NaN or infinity."""


class DuplicateJsonKeyError(ValueError):
    """A JSON object repeats a key."""


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        converted: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError(f"JSON object key must be a string, got {type(key).__name__}")
            converted[key] = _jsonable(item)
        return converted
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    numpy_module = globals().get("np")
    if numpy_module is not None and isinstance(value, numpy_module.ndarray):
        return _jsonable(value.tolist())
    if numpy_module is not None and isinstance(value, (numpy_module.bool_,)):
        return bool(value)
    if numpy_module is not None and isinstance(value, (numpy_module.integer,)):
        return int(value)
    if numpy_module is not None and isinstance(value, (numpy_module.floating,)):
        value = float(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise NonFiniteJsonError(f"nonfinite JSON number: {value!r}")
        return value
    if isinstance(value, Path):
        return str(value)
    if is_dataclass(value) and not isinstance(value, type):
        return _jsonable(asdict(value))
    if value is None or isinstance(value, (bool, int, str)):
        return value
    raise TypeError(f"unsupported JSON value type: {type(value).__name__}")


def manifest_entry(
    path: Path,
    data: bytes | None = None,
    *,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    if data is None:
        payload, _identity = _read_registered_or_stable_file(path)
    else:
        payload = data
    root = REPO_ROOT if repo_root is None else repo_root
    return {
        "repository_relative_path": path.resolve().relative_to(root.resolve()).as_posix(),
        "byte_count": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


_MANUSCRIPT_RELATIVE = "manuscripts/gauge_vfe_rg"
_VERIFICATION_RELATIVE = f"{_MANUSCRIPT_RELATIVE}/verification"
_TESTS_RELATIVE = f"{_VERIFICATION_RELATIVE}/tests"
_EXACT_REQUIRED_PATHS = (
    f"{_MANUSCRIPT_RELATIVE}/SPEC.md",
    f"{_MANUSCRIPT_RELATIVE}/build.ps1",
    "manuscripts/references.bib",
    f"{_VERIFICATION_RELATIVE}/claims.json",
    f"{_VERIFICATION_RELATIVE}/run_checks.py",
    f"{_VERIFICATION_RELATIVE}/requirements.txt",
    f"{_VERIFICATION_RELATIVE}/VERIFICATION.md",
    f"{_VERIFICATION_RELATIVE}/result.schema.json",
    f"{_VERIFICATION_RELATIVE}/manifest-policy.json",
    f"{_VERIFICATION_RELATIVE}/lifecycle_gate.py",
    f"{_VERIFICATION_RELATIVE}/build_audit.py",
    f"{_VERIFICATION_RELATIVE}/build_bootstrap_reference.ps1.txt",
    f"{_VERIFICATION_RELATIVE}/build_bootstrap_transport.txt",
)
_STYLE_CANDIDATES = (
    f"{_MANUSCRIPT_RELATIVE}/scientific_report.sty",
    "manuscripts/scientific_report.sty",
)
_ALLOWED_EXCLUSIONS = frozenset(
    {
        f"{_MANUSCRIPT_RELATIVE}/main.pdf",
        f"{_VERIFICATION_RELATIVE}/current-results.json",
        "**/__pycache__/**",
        "**/*.pyc",
    }
)
_RECURSIVE_POLICY_CLASSES = (
    {"root": _MANUSCRIPT_RELATIVE, "glob": "**/*.tex"},
    {"root": _TESTS_RELATIVE, "glob": "**/test_*.py"},
)
PRODUCTION_PROTOCOL_PROFILE = "gauge-vfe-rg-production-v1"
SYNTHETIC_PROTOCOL_PROFILE = "synthetic-test-fixture-v1"
_PROTOCOL_PROFILES = frozenset(
    {PRODUCTION_PROTOCOL_PROFILE, SYNTHETIC_PROTOCOL_PROFILE}
)
_FIXED_PYTHON_EXECUTABLE = Path(r"C:\Python314\python.exe")
_FIXED_GIT_EXECUTABLE = Path(r"C:\Program Files\Git\cmd\git.exe")
_REQUIRED_DEPENDENCY_NAMES = (
    "numpy",
    "scipy",
    "sympy",
    "mpmath",
    "pypdf",
    "pytest",
)
_REQUIREMENT_LINE = re.compile(
    r"(?P<name>[a-z0-9]+(?:-[a-z0-9]+)*)=="
    r"(?P<version>(?:0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*))*)"
)
_RunEvidence = namedtuple(
    "_RunEvidence",
    [
        "repo_root",
        "head_revision",
        "executable_snapshot",
        "executable_identities",
        "dependency_provenance",
        "governed_manifest",
        "governed_registry",
        "test_fixture",
    ],
)
_ACTIVE_EXECUTABLE_IDENTITIES: ContextVar[dict[str, Any] | None] = ContextVar(
    "gauge_vfe_rg_executable_identities",
    default=None,
)
_ACTIVE_RUN_EVIDENCE: ContextVar[Any | None] = ContextVar(
    "gauge_vfe_rg_run_evidence",
    default=None,
)
_ACTIVE_EXECUTABLE_GUARDS: ContextVar[dict[str, Any] | None] = ContextVar(
    "gauge_vfe_rg_executable_guards",
    default=None,
)
_ACTIVE_GOVERNED_REGISTRY: ContextVar[dict[str, Any] | None] = ContextVar(
    "gauge_vfe_rg_governed_registry",
    default=None,
)
_ACTIVE_OUTPUT_STAGE_PATHS: ContextVar[set[str] | None] = ContextVar(
    "gauge_vfe_rg_output_stage_paths",
    default=None,
)
_ACTIVE_TRANSACTION_RECEIPT_ID: ContextVar[str | None] = ContextVar(
    "gauge_vfe_rg_transaction_receipt_id",
    default=None,
)
_PRODUCTION_MANUSCRIPT_FILENAMES = (
    "main.tex",
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


def _expected_protocol_profile(test_fixture: bool) -> str:
    """Return the one protocol profile authorized by the call boundary."""

    if type(test_fixture) is not bool:
        raise TypeError("test_fixture must be an explicit bool")
    return (
        SYNTHETIC_PROTOCOL_PROFILE
        if test_fixture
        else PRODUCTION_PROTOCOL_PROFILE
    )


def _require_nonproduction_fixture_tree(repo_root: Path, test_fixture: bool) -> None:
    """Keep the synthetic API from accepting a production-shaped manuscript."""

    if not test_fixture:
        return
    manuscript_root = repo_root / _MANUSCRIPT_RELATIVE
    if all(
        (manuscript_root / filename).is_file()
        for filename in _PRODUCTION_MANUSCRIPT_FILENAMES
    ):
        raise VerificationFailure(
            "PROTOCOL_PROFILE_MISMATCH",
            str(manuscript_root),
            "synthetic test_fixture mode rejects the full production manuscript envelope",
            expected="a deliberately reduced synthetic fixture tree",
            observed=list(_PRODUCTION_MANUSCRIPT_FILENAMES),
        )


def semantic_payload(document: dict[str, Any]) -> dict[str, Any]:
    """Return a deep-copied semantic payload with exactly two top-level exclusions."""

    if not isinstance(document, dict):
        raise TypeError("semantic payload input must be a dictionary")
    return copy.deepcopy(
        {
            key: value
            for key, value in document.items()
            if key not in {"generated_at_utc", "semantic_payload_digest"}
        }
    )


def _validate_json_value(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, (bool, str)):
        return
    if isinstance(value, int) and not isinstance(value, bool):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise NonFiniteJsonError(f"{path}: nonfinite JSON number {value!r}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_json_value(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError(
                    f"{path}: JSON object key must be a string, got {type(key).__name__}"
                )
            _validate_json_value(item, f"{path}.{key}")
        return
    raise TypeError(f"{path}: unsupported JSON value type {type(value).__name__}")


def canonical_json_bytes(value: object) -> bytes:
    """Serialize strict finite JSON as compact sorted UTF-8 without a final LF."""

    _validate_json_value(value)
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


class _InvalidUtf8JsonError(ValueError):
    pass


class _MalformedJsonError(ValueError):
    pass


def _strict_json_loads(raw: bytes, *, location: str) -> Any:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise _InvalidUtf8JsonError(f"{location}: UTF-8 BOM is not permitted")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise _InvalidUtf8JsonError(f"{location}: invalid UTF-8: {exc}") from exc

    def object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result_object: dict[str, Any] = {}
        for key, value in pairs:
            if key in result_object:
                raise DuplicateJsonKeyError(f"{location}: duplicate JSON key {key!r}")
            result_object[key] = value
        return result_object

    def parse_float(token: str) -> float:
        value = float(token)
        if not math.isfinite(value):
            raise NonFiniteJsonError(
                f"{location}: numeric token is outside the finite range: {token}"
            )
        return value

    def reject_constant(token: str) -> Any:
        raise NonFiniteJsonError(f"{location}: nonstandard JSON constant {token}")

    try:
        value = json.loads(
            text,
            object_pairs_hook=object_pairs,
            parse_float=parse_float,
            parse_constant=reject_constant,
        )
    except (DuplicateJsonKeyError, NonFiniteJsonError):
        raise
    except (json.JSONDecodeError, ValueError) as exc:
        raise _MalformedJsonError(f"{location}: malformed JSON: {exc}") from exc
    _validate_json_value(value)
    return value


def _strict_json_file(path: Path) -> Any:
    try:
        raw, _identity = _read_registered_or_stable_file(path)
    except OSError as exc:
        raise _MalformedJsonError(f"{path}: cannot read JSON: {exc}") from exc
    return _strict_json_loads(raw, location=str(path))


def _is_link_or_reparse(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        is_junction = getattr(os.path, "isjunction", None)
        if is_junction is not None and is_junction(path):
            return True
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
        reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        return bool(attributes & reparse_flag)
    except OSError:
        return True


class _StableFileReadError(OSError):
    """A file read was not bound to one stable path/handle identity."""


def _stat_identity(metadata: os.stat_result) -> tuple[int, int, int, int, int]:
    """Return filesystem fields that bind an opened regular-file identity."""

    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _stat_handle_binding_identity(
    metadata: os.stat_result,
) -> tuple[int, int, int, int]:
    """Return fields comparable between Windows path stat and handle fstat."""

    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
    )


def _open_stable_regular_file(
    path: Path,
) -> tuple[bytes, tuple[int, int, int, int, int]]:
    """Read through one handle bound to pre/post lexical path identity."""

    absolute = Path(os.path.abspath(os.fspath(path)))
    try:
        path_before = absolute.lstat()
    except FileNotFoundError:
        raise
    except OSError as exc:
        raise _StableFileReadError(
            f"cannot inspect stable file before opening: {absolute}: {exc}"
        ) from exc
    try:
        if not stat.S_ISREG(path_before.st_mode) or _is_link_or_reparse(absolute):
            raise _StableFileReadError(
                f"target is not a regular, non-reparse file: {absolute}"
            )
        path_identity_before = _stat_identity(path_before)
        with absolute.open("rb") as handle:
            handle_before = os.fstat(handle.fileno())
            handle_identity_before = _stat_identity(handle_before)
            if _stat_handle_binding_identity(handle_before) != (
                _stat_handle_binding_identity(path_before)
            ):
                raise _StableFileReadError(
                    f"opened handle does not match pre-open path identity: {absolute}"
                )
            payload = handle.read()
            handle_identity_after = _stat_identity(os.fstat(handle.fileno()))
            if handle_identity_after != handle_identity_before:
                raise _StableFileReadError(
                    f"opened file identity changed while it was read: {absolute}"
                )
        path_identity_after = _stat_identity(absolute.lstat())
        if (
            path_identity_after != path_identity_before
            or len(payload) != path_before.st_size
        ):
            raise _StableFileReadError(
                f"path identity changed while its opened handle was read: {absolute}"
            )
    except _StableFileReadError:
        raise
    except OSError as exc:
        raise _StableFileReadError(
            f"stable file disappeared or changed after initial observation: {absolute}: {exc}"
        ) from exc
    return payload, path_identity_before


class _ByHandleFileInformation(ctypes.Structure):
    """Windows ``BY_HANDLE_FILE_INFORMATION`` layout."""

    _fields_ = [
        ("file_attributes", wintypes.DWORD),
        ("creation_time", wintypes.FILETIME),
        ("last_access_time", wintypes.FILETIME),
        ("last_write_time", wintypes.FILETIME),
        ("volume_serial_number", wintypes.DWORD),
        ("file_size_high", wintypes.DWORD),
        ("file_size_low", wintypes.DWORD),
        ("number_of_links", wintypes.DWORD),
        ("file_index_high", wintypes.DWORD),
        ("file_index_low", wintypes.DWORD),
    ]


class _WindowsExecutableGuard:
    """Hold a deny-write/delete Windows handle across trusted execution."""

    def __init__(
        self,
        path: Path,
        role: str,
        *,
        issue_code: str = "EXECUTABLE_IDENTITY",
        subject: str = "executable",
    ) -> None:
        if issue_code not in ISSUE_CODES:
            raise ValueError(f"unknown guard issue code: {issue_code}")
        self.issue_code = issue_code
        self.subject = subject
        if os.name != "nt":
            raise VerificationFailure(
                self.issue_code,
                str(path),
                f"fixed {subject} binding requires Windows CreateFileW",
            )
        self.path = Path(path)
        self.role = role
        self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        create_file = self._kernel32.CreateFileW
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
        self._handle = create_file(
            str(self.path),
            0x80000000,
            0x00000001,
            None,
            3,
            0x00000080,
            None,
        )
        invalid_handle = ctypes.c_void_p(-1).value
        if self._handle in (None, invalid_handle):
            error = ctypes.get_last_error()
            raise VerificationFailure(
                self.issue_code,
                str(self.path),
                f"cannot acquire deny-write/delete {role} {subject} guard: WinError {error}",
            )
        self._closed = False

    @staticmethod
    def _filetime_value(value: wintypes.FILETIME) -> int:
        return (int(value.dwHighDateTime) << 32) | int(value.dwLowDateTime)

    def read(self) -> tuple[bytes, dict[str, Any]]:
        """Read and identify bytes through the still-held guard handle."""

        information = _ByHandleFileInformation()
        get_information = self._kernel32.GetFileInformationByHandle
        get_information.argtypes = (
            wintypes.HANDLE,
            ctypes.POINTER(_ByHandleFileInformation),
        )
        get_information.restype = wintypes.BOOL
        if not get_information(self._handle, ctypes.byref(information)):
            raise VerificationFailure(
                self.issue_code,
                str(self.path),
                f"cannot query guarded {self.role} {self.subject} identity: WinError {ctypes.get_last_error()}",
            )

        set_pointer = self._kernel32.SetFilePointerEx
        set_pointer.argtypes = (
            wintypes.HANDLE,
            ctypes.c_longlong,
            ctypes.POINTER(ctypes.c_longlong),
            wintypes.DWORD,
        )
        set_pointer.restype = wintypes.BOOL
        if not set_pointer(self._handle, 0, None, 0):
            raise VerificationFailure(
                self.issue_code,
                str(self.path),
                f"cannot rewind guarded {self.role} {self.subject}: WinError {ctypes.get_last_error()}",
            )

        read_file = self._kernel32.ReadFile
        read_file.argtypes = (
            wintypes.HANDLE,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        )
        read_file.restype = wintypes.BOOL
        digest = hashlib.sha256()
        byte_count = 0
        chunks: list[bytes] = []
        buffer = ctypes.create_string_buffer(1024 * 1024)
        while True:
            read_count = wintypes.DWORD()
            if not read_file(
                self._handle,
                buffer,
                len(buffer),
                ctypes.byref(read_count),
                None,
            ):
                raise VerificationFailure(
                    self.issue_code,
                    str(self.path),
                    f"cannot read guarded {self.role} {self.subject}: WinError {ctypes.get_last_error()}",
                )
            count = int(read_count.value)
            if count == 0:
                break
            chunk = buffer.raw[:count]
            chunks.append(chunk)
            digest.update(chunk)
            byte_count += count
        declared_size = (
            int(information.file_size_high) << 32
        ) | int(information.file_size_low)
        if byte_count != declared_size:
            raise VerificationFailure(
                self.issue_code,
                str(self.path),
                f"guarded {self.role} {self.subject} byte count changed while read",
                expected=declared_size,
                observed=byte_count,
            )
        if int(information.file_attributes) & 0x00000010:
            raise VerificationFailure(
                self.issue_code,
                str(self.path),
                f"guarded {self.role} target is a directory",
            )
        snapshot = {
            "path": str(self.path),
            "sha256": digest.hexdigest(),
            "byte_count": byte_count,
            "guard_filesystem_identity": [
                int(information.volume_serial_number),
                (int(information.file_index_high) << 32)
                | int(information.file_index_low),
                declared_size,
                self._filetime_value(information.creation_time),
                self._filetime_value(information.last_write_time),
                int(information.file_attributes),
            ],
        }
        return b"".join(chunks), snapshot

    def snapshot(self) -> dict[str, Any]:
        """Hash and identify bytes through the still-held guard handle."""

        _payload, snapshot = self.read()
        return snapshot

    def close(self) -> None:
        """Release the Windows handle exactly once."""

        if self._closed:
            return
        close_handle = self._kernel32.CloseHandle
        close_handle.argtypes = (wintypes.HANDLE,)
        close_handle.restype = wintypes.BOOL
        if not close_handle(self._handle):
            raise VerificationFailure(
                self.issue_code,
                str(self.path),
                f"cannot close guarded {self.role} {self.subject}: WinError {ctypes.get_last_error()}",
            )
        self._closed = True


_GovernedInputRecord = namedtuple(
    "_GovernedInputRecord",
    ["relative_path", "path", "guard", "payload", "snapshot"],
)


def _registry_path_key(path: Path) -> str:
    """Return one lexical, case-insensitive key without following reparse points."""

    return os.path.normcase(str(Path(os.path.abspath(os.fspath(path)))))


def _read_registered_or_stable_file(path: Path) -> tuple[bytes, Any]:
    """Read governed input from its retained M0 handle when one is active."""

    registry = _ACTIVE_GOVERNED_REGISTRY.get()
    record = None if registry is None else registry.get(_registry_path_key(path))
    if record is None:
        if registry is not None:
            raise VerificationFailure(
                "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
                str(path),
                "governed semantic read was absent from the retained M0 registry",
            )
        return _open_stable_regular_file(path)
    payload, snapshot = record.guard.read()
    if payload != record.payload or snapshot != record.snapshot:
        raise VerificationFailure(
            "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
            record.relative_path,
            "governed input bytes or same-handle identity changed after M0",
            expected={
                "sha256": hashlib.sha256(record.payload).hexdigest(),
                "snapshot": record.snapshot,
            },
            observed={
                "sha256": hashlib.sha256(payload).hexdigest(),
                "snapshot": snapshot,
            },
        )
    return payload, snapshot


def _open_governed_input_record(
    relative_path: str,
    path: Path,
) -> Any:
    """Acquire and snapshot one deny-write/delete governed-input handle."""

    guard = _WindowsExecutableGuard(
        path,
        relative_path,
        issue_code="GOVERNED_INPUT_CHANGED_DURING_VERIFY",
        subject="governed input",
    )
    try:
        payload, snapshot = guard.read()
    except BaseException as primary:
        try:
            guard.close()
        except BaseException as cleanup_error:
            primary.add_note(f"governed guard cleanup also failed: {cleanup_error!r}")
        raise
    return _GovernedInputRecord(
        relative_path=relative_path,
        path=Path(os.path.abspath(os.fspath(path))),
        guard=guard,
        payload=payload,
        snapshot=copy.deepcopy(snapshot),
    )


def _close_governed_registry(registry: dict[str, Any]) -> None:
    """Close a governed registry in reverse deterministic acquisition order."""

    first_error: BaseException | None = None
    records = sorted(
        registry.values(),
        key=lambda record: record.relative_path,
        reverse=True,
    )
    for record in records:
        try:
            record.guard.close()
        except BaseException as exc:
            if first_error is None:
                first_error = exc
    if first_error is not None:
        raise first_error


def _run_cleanup_actions(
    actions: tuple[tuple[str, Callable[[], None]], ...],
) -> None:
    """Run every cleanup action and preserve any already-active exception."""

    cleanup_errors: list[tuple[str, BaseException]] = []
    for label, action in actions:
        try:
            action()
        except BaseException as exc:
            cleanup_errors.append((label, exc))
    if not cleanup_errors:
        return
    active = sys.exception()
    if active is not None:
        for label, cleanup_error in cleanup_errors:
            active.add_note(f"{label} cleanup also failed: {cleanup_error!r}")
        return
    label, primary = cleanup_errors[0]
    primary.add_note(f"cleanup action failed: {label}")
    for extra_label, cleanup_error in cleanup_errors[1:]:
        primary.add_note(
            f"additional {extra_label} cleanup failure: {cleanup_error!r}"
        )
    raise primary


def _relative_posix(repo_root: Path, path: Path) -> str:
    root = repo_root.resolve(strict=True)
    resolved = path.resolve(strict=True)
    try:
        relative = resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            str(path),
            "governed path escapes the repository root",
        ) from exc
    if relative.startswith(".git/") or relative == ".git":
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            relative,
            "the Git administrative directory cannot be governed input",
        )
    return relative


def _checked_regular_file(repo_root: Path, relative: str) -> Path:
    if (
        not relative
        or "\\" in relative
        or PurePosixPath(relative).is_absolute()
        or any(part in {"", ".", ".."} for part in PurePosixPath(relative).parts)
    ):
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            relative or "$policy",
            "governed paths must be normalized repository-relative POSIX paths",
        )
    path = repo_root / Path(*PurePosixPath(relative).parts)
    if not path.exists():
        raise ManifestPolicyError(
            "MISSING_GOVERNED_PATH",
            relative,
            "required governed input does not exist",
        )
    if _is_link_or_reparse(path):
        raise ManifestPolicyError(
            "UNEXPECTED_GOVERNED_PATH",
            relative,
            "symlink, junction, or reparse governed inputs are forbidden",
        )
    try:
        mode = path.stat(follow_symlinks=False).st_mode
    except OSError as exc:
        raise ManifestPolicyError(
            "MISSING_GOVERNED_PATH",
            relative,
            f"cannot stat governed input: {exc}",
        ) from exc
    if not stat.S_ISREG(mode):
        raise ManifestPolicyError(
            "UNEXPECTED_GOVERNED_PATH",
            relative,
            "governed input is not a regular file",
        )
    if _relative_posix(repo_root, path) != relative:
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            relative,
            "governed path does not resolve to its declared repository-relative identity",
        )
    return path


def _walk_governed_files(repo_root: Path, root_relative: str) -> list[tuple[str, Path]]:
    root = repo_root / Path(*PurePosixPath(root_relative).parts)
    if not root.is_dir() or _is_link_or_reparse(root):
        raise ManifestPolicyError(
            "MISSING_GOVERNED_PATH",
            root_relative,
            "governed namespace is missing or is a reparse point",
        )
    def traversal_error(exc: OSError) -> None:
        location = getattr(exc, "filename", None) or root_relative
        raise ManifestPolicyError(
            "UNEXPECTED_GOVERNED_PATH",
            str(location),
            f"governed namespace traversal failed: {exc}",
        ) from exc

    discovered: list[tuple[str, Path]] = []
    for current_text, directories, filenames in os.walk(
        root,
        followlinks=False,
        onerror=traversal_error,
    ):
        current = Path(current_text)
        safe_directories: list[str] = []
        for directory in directories:
            child = current / directory
            if _is_link_or_reparse(child):
                relative = child.relative_to(repo_root).as_posix()
                raise ManifestPolicyError(
                    "UNEXPECTED_GOVERNED_PATH",
                    relative,
                    "reparse traversal is forbidden in a governed namespace",
                )
            safe_directories.append(directory)
        directories[:] = safe_directories
        for filename in filenames:
            path = current / filename
            relative = path.relative_to(repo_root).as_posix()
            discovered.append((relative, _checked_regular_file(repo_root, relative)))
    return discovered


def _matches_exclusion(relative: str, patterns: tuple[str, ...]) -> bool:
    if relative in patterns:
        return True
    if "**/__pycache__/**" in patterns and "/__pycache__/" in f"/{relative}/":
        return True
    if "**/*.pyc" in patterns and relative.endswith(".pyc"):
        return True
    return any(PurePosixPath(relative).match(pattern) for pattern in patterns)


def _is_owned_output_stage(repo_root: Path, relative: str) -> bool:
    """Recognize only exact temporary paths owned by the active output transaction."""

    stage_paths = _ACTIVE_OUTPUT_STAGE_PATHS.get()
    if not stage_paths:
        return False
    candidate = repo_root / Path(*PurePosixPath(relative).parts)
    return _registry_path_key(candidate) in stage_paths


def _load_manifest_policy(
    repo_root: Path,
    *,
    test_fixture: bool = False,
) -> dict[str, Any]:
    expected_profile = _expected_protocol_profile(test_fixture)
    _require_nonproduction_fixture_tree(repo_root, test_fixture)
    policy_path = repo_root / _EXACT_REQUIRED_PATHS[8]
    try:
        policy = _strict_json_file(policy_path)
    except (ValueError, OSError) as exc:
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            _EXACT_REQUIRED_PATHS[8],
            str(exc),
        ) from exc
    if not isinstance(policy, dict):
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            _EXACT_REQUIRED_PATHS[8],
            "manifest policy must be a JSON object",
        )
    allowed_keys = {
        "schema_version",
        "hash_algorithm",
        "hash_domain",
        "path_semantics",
        "recursive_inclusions",
        "required_paths",
        "style_candidates",
        "governed_namespaces",
        "explicit_exclusions",
        "bound_paths",
        "reject_unexpected_governed_paths",
        "protocol_profile",
    }
    unexpected_keys = sorted(set(policy) - allowed_keys)
    if unexpected_keys:
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            _EXACT_REQUIRED_PATHS[8],
            "manifest policy contains undeclared fields",
            expected=sorted(allowed_keys),
            observed=unexpected_keys,
        )
    if policy.get("schema_version") != "1.0":
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            f"{_EXACT_REQUIRED_PATHS[8]}:schema_version",
            "manifest policy schema_version must be 1.0",
        )
    protocol_profile = policy.get("protocol_profile")
    if protocol_profile != expected_profile:
        raise ManifestPolicyError(
            "PROTOCOL_PROFILE_MISMATCH",
            f"{_EXACT_REQUIRED_PATHS[8]}:protocol_profile",
            "manifest policy profile does not match the authorized call boundary",
            expected=expected_profile,
            observed=protocol_profile,
        )
    if policy.get("reject_unexpected_governed_paths") is not True:
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            f"{_EXACT_REQUIRED_PATHS[8]}:reject_unexpected_governed_paths",
            "unexpected governed paths must be rejected",
        )
    exclusions = policy.get("explicit_exclusions")
    if not isinstance(exclusions, list) or any(
        not isinstance(item, str) for item in exclusions
    ) or len(exclusions) != len(set(exclusions)):
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            f"{_EXACT_REQUIRED_PATHS[8]}:explicit_exclusions",
            "explicit_exclusions must be a duplicate-free list of strings",
        )
    forbidden_exclusions = sorted(set(exclusions) - _ALLOWED_EXCLUSIONS)
    if forbidden_exclusions:
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            f"{_EXACT_REQUIRED_PATHS[8]}:explicit_exclusions",
            "policy attempted to add a shrinkable exclusion",
            expected=sorted(_ALLOWED_EXCLUSIONS),
            observed=forbidden_exclusions,
        )

    bound_paths = policy.get("bound_paths")
    if bound_paths is not None and (
        not isinstance(bound_paths, list)
        or any(not isinstance(item, str) for item in bound_paths)
        or len(bound_paths) != len(set(bound_paths))
    ):
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            f"{_EXACT_REQUIRED_PATHS[8]}:bound_paths",
            "bound_paths must be a duplicate-free list of strings",
        )

    recursive = policy.get("recursive_inclusions")
    required = policy.get("required_paths")
    styles = policy.get("style_candidates")
    namespaces = policy.get("governed_namespaces")
    if not isinstance(recursive, list) or recursive != list(_RECURSIVE_POLICY_CLASSES):
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            f"{_EXACT_REQUIRED_PATHS[8]}:recursive_inclusions",
            "policy must declare exactly the ordered nonshrinkable recursive input classes",
            expected=list(_RECURSIVE_POLICY_CLASSES),
            observed=recursive,
        )
    if not isinstance(required, list) or required != list(_EXACT_REQUIRED_PATHS):
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            f"{_EXACT_REQUIRED_PATHS[8]}:required_paths",
            "policy must declare exactly the ordered nonshrinkable exact inputs",
            expected=list(_EXACT_REQUIRED_PATHS),
            observed=required,
        )
    if not isinstance(styles, list) or styles != list(_STYLE_CANDIDATES):
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            f"{_EXACT_REQUIRED_PATHS[8]}:style_candidates",
            "policy must declare both style candidates in search order",
            expected=list(_STYLE_CANDIDATES),
            observed=styles,
        )
    expected_namespaces = [_MANUSCRIPT_RELATIVE, _TESTS_RELATIVE]
    if not isinstance(namespaces, list) or namespaces != expected_namespaces:
        raise ManifestPolicyError(
            "MANIFEST_POLICY_INVALID",
            f"{_EXACT_REQUIRED_PATHS[8]}:governed_namespaces",
            "policy must declare exactly the ordered governed namespaces",
            expected=expected_namespaces,
            observed=namespaces,
        )
    for key, expected in {
        "hash_algorithm": "SHA-256",
        "hash_domain": "raw file bytes",
        "path_semantics": "repository-relative POSIX paths",
    }.items():
        if policy.get(key) != expected:
            raise ManifestPolicyError(
                "MANIFEST_POLICY_INVALID",
                f"{_EXACT_REQUIRED_PATHS[8]}:{key}",
                f"policy {key} does not match the manifest contract",
                expected=expected,
                observed=policy.get(key),
            )
    return policy


def discover_bound_inputs(
    repo_root: Path,
    *,
    test_fixture: bool = False,
) -> dict[str, Path]:
    """Discover every nonshrinkable governed input under the audited policy."""

    root = Path(repo_root).resolve(strict=True)
    policy = _load_manifest_policy(root, test_fixture=test_fixture)
    exclusions = tuple(policy.get("explicit_exclusions", []))
    governed_files = _walk_governed_files(root, _MANUSCRIPT_RELATIVE)

    selected: dict[str, Path] = {}
    for relative, path in governed_files:
        if relative.endswith(".tex"):
            selected[relative] = path
    for relative in _EXACT_REQUIRED_PATHS:
        selected[relative] = _checked_regular_file(root, relative)
    existing_styles = 0
    for relative in _STYLE_CANDIDATES:
        path = root / Path(*PurePosixPath(relative).parts)
        if path.exists():
            selected[relative] = _checked_regular_file(root, relative)
            existing_styles += 1
    if existing_styles == 0:
        raise ManifestPolicyError(
            "MISSING_GOVERNED_PATH",
            "|".join(_STYLE_CANDIDATES),
            "neither declared style candidate exists",
        )
    tests_root = root / Path(*PurePosixPath(_TESTS_RELATIVE).parts)
    for relative, path in _walk_governed_files(root, _TESTS_RELATIVE):
        if path.name.startswith("test_") and path.suffix == ".py":
            selected[relative] = path
    if not tests_root.exists():
        raise ManifestPolicyError(
            "MISSING_GOVERNED_PATH",
            _TESTS_RELATIVE,
            "verification test namespace is missing",
        )

    declared_bound = policy.get("bound_paths")
    if declared_bound is not None:
        declared_set = set(declared_bound)
        missing_minimum = sorted(set(selected) - declared_set)
        if missing_minimum:
            raise ManifestPolicyError(
                "MANIFEST_POLICY_INVALID",
                f"{_EXACT_REQUIRED_PATHS[8]}:bound_paths",
                "policy attempted to shrink the nonnegotiable discovery envelope",
                expected=sorted(selected),
                observed=sorted(declared_set),
            )
        for relative in declared_bound:
            selected[relative] = _checked_regular_file(root, relative)

    selected_casefold: dict[str, str] = {}
    for relative in sorted(selected):
        folded = relative.casefold()
        other = selected_casefold.get(folded)
        if other is not None and other != relative:
            raise ManifestPolicyError(
                "UNEXPECTED_GOVERNED_PATH",
                relative,
                f"Windows case-fold collision with {other}",
            )
        selected_casefold[folded] = relative

    all_casefold: dict[str, str] = {}
    for relative, _path in governed_files:
        if _is_owned_output_stage(root, relative):
            continue
        folded = relative.casefold()
        other = all_casefold.get(folded)
        if other is not None and other != relative:
            raise ManifestPolicyError(
                "UNEXPECTED_GOVERNED_PATH",
                relative,
                f"Windows case-fold collision with {other}",
            )
        all_casefold[folded] = relative
        if relative not in selected and not _matches_exclusion(relative, exclusions):
            raise ManifestPolicyError(
                "UNEXPECTED_GOVERNED_PATH",
                relative,
                "regular file in a governed namespace is neither bound nor explicitly excluded",
            )

    return {relative: selected[relative] for relative in sorted(selected)}


def _read_stable_file(path: Path) -> bytes:
    try:
        payload, _identity = _read_registered_or_stable_file(path)
    except (OSError, _StableFileReadError) as exc:
        raise ManifestPolicyError(
            "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
            str(path),
            f"governed input could not be read through one stable handle: {exc}",
        ) from exc
    return payload


def build_manifest(
    repo_root: Path,
    *,
    test_fixture: bool = False,
) -> dict[str, Any]:
    """Build the complete raw-byte manifest for one repository snapshot."""

    bound_inputs: dict[str, dict[str, Any]] = {}
    for relative, path in discover_bound_inputs(
        repo_root,
        test_fixture=test_fixture,
    ).items():
        payload = _read_stable_file(path)
        bound_inputs[relative] = {
            "byte_count": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }
    return {
        "hash_algorithm": "SHA-256",
        "hash_domain": "raw file bytes",
        "path_semantics": "repository-relative POSIX paths",
        "bound_inputs": bound_inputs,
    }


def _json_type_matches(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "boolean": isinstance(value, bool),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and (not isinstance(value, float) or math.isfinite(value))
        ),
        "null": value is None,
    }.get(expected, True)


def _json_value_equal(left: Any, right: Any) -> bool:
    """Compare JSON values without Python's bool/int type confusion."""

    if isinstance(left, bool) or isinstance(right, bool):
        return isinstance(left, bool) and isinstance(right, bool) and left == right
    left_number = isinstance(left, (int, float)) and not isinstance(left, bool)
    right_number = isinstance(right, (int, float)) and not isinstance(right, bool)
    if left_number or right_number:
        return left_number and right_number and left == right
    if left is None or right is None:
        return left is None and right is None
    if isinstance(left, str) or isinstance(right, str):
        return isinstance(left, str) and isinstance(right, str) and left == right
    if isinstance(left, list) or isinstance(right, list):
        return (
            isinstance(left, list)
            and isinstance(right, list)
            and len(left) == len(right)
            and all(_json_value_equal(a, b) for a, b in zip(left, right))
        )
    if isinstance(left, dict) or isinstance(right, dict):
        return (
            isinstance(left, dict)
            and isinstance(right, dict)
            and set(left) == set(right)
            and all(_json_value_equal(left[key], right[key]) for key in left)
        )
    return type(left) is type(right) and left == right


def _schema_errors(
    value: Any,
    schema: dict[str, Any],
    path: str = "$",
    root_schema: dict[str, Any] | None = None,
) -> list[str]:
    if root_schema is None:
        root_schema = schema
    reference = schema.get("$ref")
    if isinstance(reference, str):
        if not reference.startswith("#/"):
            return [f"{path}: unsupported nonlocal schema reference {reference!r}"]
        target: Any = root_schema
        try:
            for component in reference[2:].split("/"):
                key = component.replace("~1", "/").replace("~0", "~")
                target = target[key]
        except (KeyError, TypeError):
            return [f"{path}: unresolved schema reference {reference!r}"]
        if not isinstance(target, dict):
            return [f"{path}: schema reference does not select an object"]
        schema = target
    errors: list[str] = []
    if "const" in schema and not _json_value_equal(value, schema["const"]):
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and not any(
        _json_value_equal(value, candidate) for candidate in schema["enum"]
    ):
        errors.append(f"{path}: value is not in the declared enum")
    expected_type = schema.get("type")
    if isinstance(expected_type, list):
        matches = any(_json_type_matches(value, item) for item in expected_type)
    elif isinstance(expected_type, str):
        matches = _json_type_matches(value, expected_type)
    else:
        matches = True
    if not matches:
        return errors + [f"{path}: expected {expected_type}"]
    if isinstance(value, str):
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.fullmatch(pattern, value) is None:
            errors.append(f"{path}: pattern mismatch")
        minimum_length = schema.get("minLength")
        if isinstance(minimum_length, int) and len(value) < minimum_length:
            errors.append(f"{path}: string is too short")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        if isinstance(minimum, (int, float)) and value < minimum:
            errors.append(f"{path}: value is below minimum {minimum}")
    if isinstance(value, list):
        minimum_items = schema.get("minItems")
        if isinstance(minimum_items, int) and len(value) < minimum_items:
            errors.append(f"{path}: too few items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(
                    _schema_errors(
                        item,
                        item_schema,
                        f"{path}[{index}]",
                        root_schema,
                    )
                )
    if isinstance(value, dict):
        minimum_properties = schema.get("minProperties")
        if isinstance(minimum_properties, int) and len(value) < minimum_properties:
            errors.append(f"{path}: too few properties")
        required = schema.get("required", [])
        if isinstance(required, list):
            errors.extend(
                f"{path}: missing {name}"
                for name in sorted(set(required) - set(value))
            )
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        if additional is False:
            errors.extend(
                f"{path}: unexpected {name}"
                for name in sorted(set(value) - set(properties))
            )
        for name, item in value.items():
            if name in properties and isinstance(properties[name], dict):
                child_schema = properties[name]
            elif isinstance(additional, dict):
                child_schema = additional
            else:
                child_schema = {}
            errors.extend(
                _schema_errors(
                    item,
                    child_schema,
                    f"{path}.{name}",
                    root_schema,
                )
            )
    return errors


def _validate_result_shape_with_schema(
    document: Any,
    schema_path: Path,
) -> list[str]:
    try:
        schema = _strict_json_file(schema_path)
    except ValueError as exc:
        return [f"$.schema: {exc}"]
    if not isinstance(schema, dict):
        return ["$.schema: result schema must be a JSON object"]
    errors = _schema_errors(document, schema)
    try:
        canonical_json_bytes(document)
    except (TypeError, ValueError) as exc:
        errors.append(f"$: {exc}")
    if not isinstance(document, dict):
        return errors
    timestamp = document.get("generated_at_utc")
    if isinstance(timestamp, str):
        if re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", timestamp
        ) is None:
            errors.append("$.generated_at_utc: expected whole-second UTC form")
        else:
            try:
                parsed_timestamp = datetime.strptime(
                    timestamp,
                    "%Y-%m-%dT%H:%M:%SZ",
                ).replace(tzinfo=timezone.utc)
            except ValueError:
                errors.append(
                    "$.generated_at_utc: invalid Gregorian UTC calendar timestamp"
                )
            else:
                canonical_timestamp = parsed_timestamp.strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                )
                if canonical_timestamp != timestamp:
                    errors.append(
                        "$.generated_at_utc: timestamp is not canonical UTC whole-second form"
                    )
    manifest = document.get("manifest")
    if isinstance(manifest, dict):
        bound_inputs = manifest.get("bound_inputs")
        if isinstance(bound_inputs, dict):
            folded: dict[str, str] = {}
            for relative in bound_inputs:
                if (
                    not relative
                    or "\\" in relative
                    or PurePosixPath(relative).is_absolute()
                    or any(
                        part in {"", ".", ".."}
                        for part in PurePosixPath(relative).parts
                    )
                ):
                    errors.append(
                        f"$.manifest.bound_inputs.{relative}: invalid repository-relative POSIX path"
                    )
                other = folded.get(relative.casefold())
                if other is not None and other != relative:
                    errors.append(
                        f"$.manifest.bound_inputs.{relative}: case-fold collision with {other}"
                    )
                folded[relative.casefold()] = relative
    checks = document.get("checks")
    if isinstance(checks, list):
        identifiers = [
            item.get("check_id")
            for item in checks
            if isinstance(item, dict) and isinstance(item.get("check_id"), str)
        ]
        if len(identifiers) != len(set(identifiers)):
            errors.append("$.checks: duplicate check_id")
    return errors


def validate_result_shape(
    document: dict[str, Any],
    *,
    test_fixture: bool = False,
) -> list[str]:
    """Validate the strict schema-3 result shape and finite JSON domain."""

    expected_profile = _expected_protocol_profile(test_fixture)
    errors = _validate_result_shape_with_schema(document, RESULT_SCHEMA_PATH)
    production_profile_error = (
        f"$.protocol_profile: expected constant {PRODUCTION_PROTOCOL_PROFILE!r}"
    )
    if test_fixture and production_profile_error in errors:
        errors.remove(production_profile_error)
    if document.get("protocol_profile") != expected_profile:
        errors.append(
            f"$.protocol_profile: expected authorized profile {expected_profile!r}"
        )
    return errors


def _replace_file_atomically(temporary: Path, target: Path) -> None:
    """Replace *target* with the platform's same-filesystem rename primitive."""

    if os.name != "nt":
        os.replace(temporary, target)
        return

    # Keep the GIL for the short namespace transaction. This prevents another
    # Python thread from opening the pathname during Windows' replacement call;
    # an already-open reader retains its complete old-file handle.
    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.PyDLL("kernel32", use_last_error=True)
    move_file = kernel32.MoveFileExW
    move_file.argtypes = (
        wintypes.LPCWSTR,
        wintypes.LPCWSTR,
        wintypes.DWORD,
    )
    move_file.restype = wintypes.BOOL
    replace_file = kernel32.ReplaceFileW
    replace_file.argtypes = (
        wintypes.LPCWSTR,
        wintypes.LPCWSTR,
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.LPVOID,
    )
    replace_file.restype = wintypes.BOOL
    if target.exists():
        replaced = replace_file(str(target), str(temporary), None, 0x1, None, None)
    else:
        replaced = move_file(str(temporary), str(target), 0x1 | 0x8)
    if not replaced:
        raise ctypes.WinError(ctypes.get_last_error())


def _atomic_write_bytes(
    path: Path,
    payload: bytes,
) -> None:
    target = Path(path).resolve(strict=False)
    parent = target.parent.resolve()
    parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_name = handle.name
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        temporary = Path(temporary_name)
        if target.exists():
            os.chmod(temporary, stat.S_IMODE(target.stat().st_mode))
        for attempt in range(10):
            try:
                _replace_file_atomically(temporary, target)
                temporary_name = None
                break
            except PermissionError:
                if attempt == 9:
                    raise
                time.sleep(0.005 * (attempt + 1))
        # Windows does not expose a portable directory fsync, and opening a
        # directory through the CRT can transiently deny concurrent child opens.
        if os.name != "nt":
            try:
                directory_fd = os.open(parent, os.O_RDONLY)
            except OSError:
                directory_fd = None
            if directory_fd is not None:
                try:
                    os.fsync(directory_fd)
                except OSError:
                    pass
                finally:
                    os.close(directory_fd)
    finally:
        if temporary_name is not None:
            try:
                Path(temporary_name).unlink()
            except FileNotFoundError:
                pass


def atomic_write_json(
    path: Path,
    value: object,
) -> None:
    """Atomically replace *path* with strict compact canonical JSON bytes."""

    payload = canonical_json_bytes(value)
    _atomic_write_bytes(Path(path), payload)


class _StagedJson:
    """Canonical JSON retained by one deny-write/delete rename-capable handle."""

    def __init__(self, target_path: Path, payload: bytes) -> None:
        if os.name != "nt":
            raise OSError("retained JSON staging requires Windows handle semantics")
        self.target_path = Path(os.path.abspath(os.fspath(target_path)))
        self._target_existed_at_stage = self.target_path.exists()
        self.payload_sha256 = hashlib.sha256(payload).hexdigest()
        self.byte_count = len(payload)
        self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self._closed = False
        self._published = False
        self._handle: Any | None = None

        create_file = self._kernel32.CreateFileW
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
        invalid_handle = ctypes.c_void_p(-1).value
        for _attempt in range(16):
            temporary = self.target_path.parent / (
                f".{self.target_path.name}.{uuid.uuid4().hex}.stage.tmp"
            )
            handle = create_file(
                str(temporary),
                0x80000000 | 0x40000000 | 0x00010000,
                0x00000001,
                None,
                1,
                0x00000080,
                None,
            )
            if handle not in (None, invalid_handle):
                self.temporary_path = temporary
                self._handle = handle
                break
            if ctypes.get_last_error() not in (80, 183):
                raise ctypes.WinError(ctypes.get_last_error())
        else:
            raise OSError("could not allocate a collision-free retained JSON stage")

        try:
            self._write(payload)
            self.validate()
        except BaseException as primary:
            try:
                self.close()
            except BaseException as cleanup_error:
                primary.add_note(f"staged-handle cleanup also failed: {cleanup_error!r}")
            try:
                self.temporary_path.unlink()
            except OSError as cleanup_error:
                primary.add_note(f"staged-path cleanup also failed: {cleanup_error!r}")
            raise

    def _write(self, payload: bytes) -> None:
        write_file = self._kernel32.WriteFile
        write_file.argtypes = (
            wintypes.HANDLE,
            wintypes.LPCVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        )
        write_file.restype = wintypes.BOOL
        offset = 0
        while offset < len(payload):
            chunk = payload[offset : offset + 1024 * 1024]
            written = wintypes.DWORD()
            buffer = ctypes.create_string_buffer(chunk)
            if not write_file(
                self._handle,
                buffer,
                len(chunk),
                ctypes.byref(written),
                None,
            ):
                raise ctypes.WinError(ctypes.get_last_error())
            if int(written.value) != len(chunk):
                raise OSError("short write to retained JSON stage")
            offset += len(chunk)
        flush = self._kernel32.FlushFileBuffers
        flush.argtypes = (wintypes.HANDLE,)
        flush.restype = wintypes.BOOL
        if not flush(self._handle):
            raise ctypes.WinError(ctypes.get_last_error())

    def _read(self) -> bytes:
        set_pointer = self._kernel32.SetFilePointerEx
        set_pointer.argtypes = (
            wintypes.HANDLE,
            ctypes.c_longlong,
            ctypes.POINTER(ctypes.c_longlong),
            wintypes.DWORD,
        )
        set_pointer.restype = wintypes.BOOL
        if not set_pointer(self._handle, 0, None, 0):
            raise ctypes.WinError(ctypes.get_last_error())
        read_file = self._kernel32.ReadFile
        read_file.argtypes = (
            wintypes.HANDLE,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        )
        read_file.restype = wintypes.BOOL
        chunks: list[bytes] = []
        buffer = ctypes.create_string_buffer(1024 * 1024)
        while True:
            count = wintypes.DWORD()
            if not read_file(
                self._handle,
                buffer,
                len(buffer),
                ctypes.byref(count),
                None,
            ):
                raise ctypes.WinError(ctypes.get_last_error())
            if count.value == 0:
                return b"".join(chunks)
            chunks.append(buffer.raw[: int(count.value)])

    def validate(self) -> bytes:
        """Authenticate the still-held stage bytes."""

        payload = self._read()
        observed_sha256 = hashlib.sha256(payload).hexdigest()
        if len(payload) != self.byte_count or observed_sha256 != self.payload_sha256:
            raise OSError(
                "retained JSON stage changed: "
                f"expected {self.payload_sha256}, observed {observed_sha256}"
            )
        return payload

    def publish(self) -> None:
        """Rename the exact retained handle onto the target with replacement."""

        self.validate()
        target_utf16 = str(self.target_path).encode("utf-16-le")

        class _FileRenameInfoEx(ctypes.Structure):
            _fields_ = [
                ("flags", wintypes.DWORD),
                ("root_directory", wintypes.HANDLE),
                ("file_name_length", wintypes.DWORD),
                ("file_name", wintypes.WCHAR * 1),
            ]

        offset = _FileRenameInfoEx.file_name.offset
        # Although FileNameLength excludes the terminator, the Win32 variable-size
        # structure still needs one readable trailing WCHAR.  Without it the
        # kernel can inspect the adjacent heap word while normalizing a long path,
        # producing either a spurious final character or ERROR_INVALID_NAME.
        buffer = ctypes.create_string_buffer(
            offset + len(target_utf16) + ctypes.sizeof(wintypes.WCHAR)
        )
        information = ctypes.cast(
            buffer,
            ctypes.POINTER(_FileRenameInfoEx),
        ).contents
        information.flags = 0x00000001 if self._target_existed_at_stage else 0
        information.root_directory = None
        information.file_name_length = len(target_utf16)
        ctypes.memmove(
            ctypes.addressof(buffer) + offset,
            target_utf16,
            len(target_utf16),
        )
        set_information = self._kernel32.SetFileInformationByHandle
        set_information.argtypes = (
            wintypes.HANDLE,
            ctypes.c_int,
            wintypes.LPVOID,
            wintypes.DWORD,
        )
        set_information.restype = wintypes.BOOL
        if not set_information(
            self._handle,
            22,
            buffer,
            len(buffer),
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        self._published = True
        stage_paths = _ACTIVE_OUTPUT_STAGE_PATHS.get()
        if stage_paths is not None:
            stage_paths.discard(_registry_path_key(self.temporary_path))
        self.validate()

    def retain_published_read_guard(self) -> None:
        """Finalize rename while continuously retaining the exact file identity."""

        reopen_file = self._kernel32.ReOpenFile
        reopen_file.argtypes = (
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.DWORD,
        )
        reopen_file.restype = wintypes.HANDLE
        invalid_handle = ctypes.c_void_p(-1).value
        intermediate = reopen_file(
            self._handle,
            0x80000000,
            0x00000001 | 0x00000002 | 0x00000004,
            0,
        )
        if intermediate in (None, invalid_handle):
            raise ctypes.WinError(ctypes.get_last_error())
        close_handle = self._kernel32.CloseHandle
        close_handle.argtypes = (wintypes.HANDLE,)
        close_handle.restype = wintypes.BOOL
        original = self._handle
        if not close_handle(original):
            close_handle(intermediate)
            raise ctypes.WinError(ctypes.get_last_error())
        self._handle = intermediate

        strict = reopen_file(
            intermediate,
            0x80000000,
            0x00000001,
            0,
        )
        if strict in (None, invalid_handle):
            raise ctypes.WinError(ctypes.get_last_error())
        if not close_handle(intermediate):
            close_handle(strict)
            raise ctypes.WinError(ctypes.get_last_error())
        self._handle = strict
        self.validate()

    def close(self) -> None:
        """Close the retained stage handle exactly once."""

        if self._closed:
            return
        close_handle = self._kernel32.CloseHandle
        close_handle.argtypes = (wintypes.HANDLE,)
        close_handle.restype = wintypes.BOOL
        if not close_handle(self._handle):
            raise ctypes.WinError(ctypes.get_last_error())
        self._closed = True

    def cleanup(self) -> None:
        """Close and remove only an unpublished stage artifact."""

        close_error: BaseException | None = None
        try:
            self.close()
        except BaseException as exc:
            close_error = exc
        stage_paths = _ACTIVE_OUTPUT_STAGE_PATHS.get()
        if stage_paths is not None:
            stage_paths.discard(_registry_path_key(self.temporary_path))
        if not self._published:
            try:
                self.temporary_path.unlink()
            except FileNotFoundError:
                pass
            except BaseException as unlink_error:
                if close_error is not None:
                    close_error.add_note(
                        f"stage unlink also failed: {unlink_error!r}"
                    )
                else:
                    raise
        if close_error is not None:
            raise close_error


def _stage_json_document(path: Path, value: object) -> Any:
    """Durably stage canonical JSON without changing the target namespace."""

    payload = canonical_json_bytes(value)
    target = Path(os.path.abspath(os.fspath(path)))
    unsafe = _unsafe_target_component(target)
    if unsafe is not None:
        component, message = unsafe
        raise OSError(f"unsafe staged target component {component}: {message}")
    target.parent.mkdir(parents=True, exist_ok=True)
    unsafe_after_create = _unsafe_target_component(target)
    if unsafe_after_create is not None:
        component, message = unsafe_after_create
        raise OSError(f"unsafe staged target component {component}: {message}")
    staged = _StagedJson(target, payload)
    stage_paths = _ACTIVE_OUTPUT_STAGE_PATHS.get()
    if stage_paths is not None:
        stage_paths.add(_registry_path_key(staged.temporary_path))
    return staged


def _cleanup_staged_json(staged: Any | None) -> None:
    """Remove an unpublished transaction artifact without touching its target."""

    if staged is None:
        return
    staged.cleanup()


def _publish_staged_json(staged: Any, *, retain_handle: bool = False) -> None:
    """Atomically publish one authenticated stage to its exact target."""

    unsafe = _unsafe_target_component(staged.target_path)
    if unsafe is not None:
        component, message = unsafe
        raise OSError(f"unsafe publication target component {component}: {message}")
    staged.publish()
    if retain_handle:
        staged.retain_published_read_guard()
    else:
        staged.close()


def fro_relative(a: np.ndarray, b: np.ndarray) -> float:
    denom = max(float(np.linalg.norm(a, ord="fro")), float(np.linalg.norm(b, ord="fro")), 1.0)
    return float(np.linalg.norm(a - b, ord="fro") / denom)


def random_spd(rng: np.random.Generator, n: int, jitter: float = 0.5) -> np.ndarray:
    m = rng.standard_normal((n, n))
    return m @ m.T + jitter * np.eye(n)


def random_gl_plus(rng: np.random.Generator, n: int, scale: float = 0.25) -> np.ndarray:
    return sla.expm(scale * rng.standard_normal((n, n)))


def random_frame_with_condition(
    rng: np.random.Generator, n: int, condition_number: float
) -> np.ndarray:
    q1, _ = np.linalg.qr(rng.standard_normal((n, n)))
    q2, _ = np.linalg.qr(rng.standard_normal((n, n)))
    singular = np.geomspace(1.0, condition_number, n)
    frame = q1 @ np.diag(singular) @ q2.T
    if np.linalg.det(frame) < 0:
        frame[:, 0] *= -1
    return frame


def incidence_map(assignments: list[int], k: int) -> np.ndarray:
    n = len(assignments)
    nc = max(assignments) + 1
    scalar = np.zeros((n, nc))
    scalar[np.arange(n), assignments] = 1.0
    return np.kron(scalar, np.eye(k))


def assemble_interaction(
    self_terms: list[np.ndarray], weights: dict[tuple[int, int], np.ndarray]
) -> tuple[np.ndarray, np.ndarray]:
    n = len(self_terms)
    k = self_terms[0].shape[0]
    lap = np.zeros((n * k, n * k))
    for (i, j), w in weights.items():
        si = slice(i * k, (i + 1) * k)
        sj = slice(j * k, (j + 1) * k)
        lap[si, si] += w
        lap[sj, sj] += w
        lap[si, sj] -= w
        lap[sj, si] -= w
    precision = lap.copy()
    for i, a in enumerate(self_terms):
        si = slice(i * k, (i + 1) * k)
        precision[si, si] += a
    return precision, lap


def result(
    check_id: str,
    title: str,
    claim_ids: list[str],
    *,
    status: str,
    seed: int | list[int] | None,
    sample_count: int | str,
    expected: dict[str, Any],
    tolerances: dict[str, Any],
    observed: dict[str, Any],
    evidence_kind: str = "reproduced_output",
    interpretation: str,
) -> dict[str, Any]:
    return _jsonable(
        {
            "check_id": check_id,
            "title": title,
            "claim_ids": claim_ids,
            "status": status,
            "seed": seed,
            "sample_count": sample_count,
            "expected": expected,
            "tolerances": tolerances,
            "observed": observed,
            "evidence_kind": evidence_kind,
            "interpretation": interpretation,
        }
    )


def check_gauss_projection() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    k = 3
    lam = random_spd(rng, k, 0.75)
    vals, vecs = np.linalg.eigh(lam)
    lam_half = (vecs * np.sqrt(vals)) @ vecs.T
    tol = 1.0e-10

    def admissible(t: np.ndarray) -> bool:
        w = lam @ t
        conditions = [
            np.linalg.norm(w - w.T, ord="fro") <= tol,
            np.linalg.eigvalsh((w + w.T) / 2).min() >= -tol,
            np.linalg.eigvalsh((lam - w + (lam - w).T) / 2).min() >= -tol,
            np.linalg.eigvalsh((t.T @ lam @ t - w + (t.T @ lam @ t - w).T) / 2).min()
            >= -tol,
        ]
        return all(conditions)

    generic_passes = sum(admissible(rng.standard_normal((k, k))) for _ in range(4000))
    projection_passes = 0
    max_idempotency = 0.0
    max_condition_residual = 0.0
    for rank in range(k + 1):
        q, _ = np.linalg.qr(rng.standard_normal((k, k)))
        x = q @ np.diag([1.0] * rank + [0.0] * (k - rank)) @ q.T
        w = lam_half @ x @ lam_half
        t = np.linalg.solve(lam, w)
        max_idempotency = max(max_idempotency, float(np.linalg.norm(x @ x - x, ord="fro")))
        max_condition_residual = max(
            max_condition_residual,
            float(np.linalg.norm(lam @ t - w, ord="fro")),
        )
        projection_passes += int(admissible(t))
    passed = generic_passes == 0 and projection_passes == 4 and max_idempotency <= tol
    return result(
        "CHK-GAUSS-PROJECTION",
        "Generic gains against exact projection controls",
        ["NUM-GAUSS-PROJECTION"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count="4000 generic gains plus ranks 0,1,2,3",
        expected={"generic_admissible_count": 0, "projection_admissible_count": 4},
        tolerances={"matrix_feasibility": tol, "idempotency": tol},
        observed={
            "generic_admissible_count": generic_passes,
            "projection_admissible_count": projection_passes,
            "max_projection_idempotency_residual": max_idempotency,
            "max_lambda_t_minus_w_residual": max_condition_residual,
        },
        interpretation="A deterministic rerun corroborates the projection characterization; it does not prove generic measure zero.",
    )


def check_gauss_trivialization() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    k = 3
    ui = random_gl_plus(rng, k)
    uj = random_gl_plus(rng, k)
    omega = ui @ np.linalg.inv(uj)
    r = random_spd(rng, k)
    raw = np.linalg.solve(r, omega)
    weight = ui.T @ np.linalg.solve(r, ui)
    raw_asym = float(np.linalg.norm(raw - raw.T, ord="fro"))
    weight_asym = float(np.linalg.norm(weight - weight.T, ord="fro"))
    min_weight = float(np.linalg.eigvalsh(weight).min())
    passed = raw_asym > 1.0e-6 and weight_asym <= FLOAT_TOL and min_weight > 0
    return result(
        "CHK-GAUSS-TRIVIALIZATION",
        "Asymmetric raw transported block versus symmetric trivialized weight",
        ["NUM-GAUSS-TRIVIALIZATION"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count=1,
        expected={"raw_asymmetry": "> 1e-6", "trivialized_symmetry": "<= tolerance", "minimum_eigenvalue": "> 0"},
        tolerances={"symmetry": FLOAT_TOL},
        observed={
            "raw_asymmetry_frobenius": raw_asym,
            "trivialized_asymmetry_frobenius": weight_asym,
            "trivialized_minimum_eigenvalue": min_weight,
        },
        interpretation="The current matrices are fully emitted by the deterministic code; the manuscript's historical magnitudes used different omitted matrices.",
    )


def check_gauss_conditioning() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    n, k, draws = 6, 3, 200
    min_eigenvalues: list[float] = []
    condition_numbers: list[float] = []
    for _ in range(draws):
        weights: dict[tuple[int, int], np.ndarray] = {}
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < 0.6:
                    m = rng.standard_normal((k, k))
                    weights[(i, j)] = m @ m.T + 0.1 * np.eye(k)
        self_terms = []
        for _i in range(n):
            m = rng.standard_normal((k, k))
            self_terms.append(m @ m.T / k)
        precision, _ = assemble_interaction(self_terms, weights)
        eig = np.linalg.eigvalsh(precision)
        min_eigenvalues.append(float(eig[0]))
        condition_numbers.append(float(eig[-1] / eig[0]))

    complete_weights = {
        (i, j): random_spd(rng, k, 0.1)
        for i in range(n)
        for j in range(i + 1, n)
    }
    _, lap = assemble_interaction([np.zeros((k, k)) for _ in range(n)], complete_weights)
    eig_lap = np.linalg.eigvalsh(lap)
    rank_tol = max(float(eig_lap[-1]), 1.0) * 1.0e-10
    nullity = int(np.count_nonzero(np.abs(eig_lap) <= rank_tol))
    consensus_residual = float(
        np.linalg.norm(lap @ np.kron(np.ones((n, 1)), np.eye(k)), ord="fro")
    )

    symmetric_offdiag_controls = 0
    for _ in range(draws):
        unstructured = random_spd(rng, n * k)
        all_blocks_symmetric = True
        for i in range(n):
            for j in range(i + 1, n):
                block = unstructured[i * k : (i + 1) * k, j * k : (j + 1) * k]
                all_blocks_symmetric &= np.linalg.norm(block - block.T, ord="fro") <= 1.0e-10
        symmetric_offdiag_controls += int(all_blocks_symmetric)
    passed = min(min_eigenvalues) > 0 and nullity == k and symmetric_offdiag_controls == 0
    return result(
        "CHK-GAUSS-CONDITIONING",
        "Interaction-family conditioning under a fully specified current sampler",
        ["NUM-GAUSS-CONDITIONING"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count={"interaction_draws": draws, "unstructured_controls": draws},
        expected={
            "all_interaction_precisions_positive_definite": True,
            "complete_graph_zero_self_nullity": k,
            "unstructured_controls_in_family": 0,
        },
        tolerances={"rank_relative": 1.0e-10, "offdiagonal_symmetry": 1.0e-10},
        observed={
            "positive_definite_count": sum(x > 0 for x in min_eigenvalues),
            "smallest_eigenvalue": min(min_eigenvalues),
            "median_condition_number": float(np.median(condition_numbers)),
            "maximum_condition_number": max(condition_numbers),
            "zero_self_control_nullity": nullity,
            "consensus_residual_frobenius": consensus_residual,
            "unstructured_controls_with_all_symmetric_offdiagonal_blocks": symmetric_offdiag_controls,
        },
        interpretation="This replaces, rather than recreates, the manuscript's incompletely specified conditioning run.",
    )


def check_kron_exact_witness() -> dict[str, Any]:
    w1 = sp.Matrix([[2, 1], [1, 1]])
    w2 = sp.Matrix([[1, 0], [0, 2]])
    d = sp.diag(3, 4)
    product = w1 * d.inv() * w2
    asymmetry = sp.simplify(product - product.T)
    d1 = sp.diag(2, 3)
    d2 = sp.diag(5, 7)
    d3 = sp.diag(11, 13)
    diagonal_product = sp.simplify(d1 * d2.inv() * d3)
    passed = asymmetry != sp.zeros(2) and diagonal_product == diagonal_product.T
    return result(
        "CHK-KRON-EXACT-WITNESS",
        "Exact rational matrix-Kron nonclosure witness and commuting control",
        ["REVIEW-R07-KRON-NONCLOSURE"],
        status="PASS" if passed else "FAIL",
        seed=None,
        sample_count="one exact counterexample and one exact commuting control",
        expected={"counterexample_product_symmetric": False, "commuting_control_symmetric": True},
        tolerances={"arithmetic": "exact rational"},
        observed={
            "counterexample_product": [[str(x) for x in product.row(i)] for i in range(product.rows)],
            "counterexample_asymmetry": [[str(x) for x in asymmetry.row(i)] for i in range(asymmetry.rows)],
            "commuting_control_product": [
                [str(x) for x in diagonal_product.row(i)] for i in range(diagonal_product.rows)
            ],
        },
        evidence_kind="exact_symbolic_witness",
        interpretation="This exact finite witness closes nonclosure of the unrestricted matrix family, not a genericity theorem.",
    )


def check_kron_monte_carlo() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    draws = 200
    k3_symmetric = 0
    k3_relative_asymmetry: list[float] = []
    scalar_symmetric = 0
    for _ in range(draws):
        w1 = random_spd(rng, 3)
        w2 = random_spd(rng, 3)
        d = random_spd(rng, 3)
        p = w1 @ np.linalg.solve(d, w2)
        rel = float(np.linalg.norm(p - p.T, ord="fro") / max(np.linalg.norm(p, ord="fro"), 1.0))
        k3_relative_asymmetry.append(rel)
        k3_symmetric += int(rel <= 1.0e-10)
        s1 = float(rng.uniform(0.1, 3.0))
        s2 = float(rng.uniform(0.1, 3.0))
        sd = float(rng.uniform(0.1, 3.0))
        scalar_symmetric += int(abs(s1 * s2 / sd - s2 * s1 / sd) <= 1.0e-15)
    passed = k3_symmetric == 0 and scalar_symmetric == draws
    return result(
        "CHK-KRON-MONTE-CARLO",
        "Current matrix-Kron genericity sweep with scalar control",
        ["REVIEW-R07-KRON-NONCLOSURE"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count={"K=3": draws, "K=1": draws},
        expected={"K3_symmetric_count": 0, "K1_symmetric_count": draws},
        tolerances={"relative_asymmetry": 1.0e-10, "scalar_equality": 1.0e-15},
        observed={
            "K3_symmetric_count": k3_symmetric,
            "K1_symmetric_count": scalar_symmetric,
            "K3_minimum_relative_asymmetry": min(k3_relative_asymmetry),
            "K3_maximum_relative_asymmetry": max(k3_relative_asymmetry),
        },
        interpretation="The sweep is controlled numerical evidence only; the exact witness is the load-bearing nonclosure evidence.",
    )


def check_restriction_schur() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    n, r = 9, 4
    j = random_spd(rng, n)
    q, _ = np.linalg.qr(rng.standard_normal((n, n)))
    b, bp = q[:, :r], q[:, r:]
    marginal = np.linalg.inv(bp.T @ np.linalg.inv(j) @ bp)
    restricted = bp.T @ j @ bp
    rhs = bp.T @ j @ b @ np.linalg.inv(b.T @ j @ b) @ b.T @ j @ bp
    identity_residual = fro_relative(restricted - marginal, rhs)
    gap_eig = np.linalg.eigvalsh((restricted - marginal + (restricted - marginal).T) / 2)
    rank_tol = max(float(gap_eig[-1]), 1.0) * 1.0e-10
    gap_rank = int(np.count_nonzero(gap_eig > rank_tol))

    mu = rng.standard_normal(n)
    mu_perp = bp.T @ mu
    closed_cost = 0.5 * float(mu_perp @ marginal @ mu_perp)
    mu_star = mu - np.linalg.solve(j, bp) @ marginal @ mu_perp
    direct_cost = 0.5 * float((mu_star - mu) @ j @ (mu_star - mu))
    constraint_residual = float(np.linalg.norm(bp.T @ mu_star))

    eigvals, eigvecs = np.linalg.eigh(j)
    be, bpe = eigvecs[:, :r], eigvecs[:, r:]
    orth_gap = bpe.T @ j @ bpe - np.linalg.inv(bpe.T @ np.linalg.inv(j) @ bpe)
    orth_residual = float(np.linalg.norm(orth_gap, ord="fro"))
    passed = (
        identity_residual <= 1.0e-11
        and gap_eig.min() >= -1.0e-10
        and gap_rank <= r
        and abs(closed_cost - direct_cost) <= 1.0e-10
        and constraint_residual <= 1.0e-10
        and orth_residual <= 1.0e-10
    )
    return result(
        "CHK-RESTRICTION-SCHUR",
        "Marginal precision, restricted precision, and constrained mean cost",
        ["NUM-RESTRICTION-SCHUR", "NUM-CG-MEAN-TIE"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count=1,
        expected={
            "schur_identity": True,
            "gap_positive_semidefinite": True,
            "gap_rank_at_most": r,
            "closed_cost_equals_direct_cost": True,
            "orthogonal_control_gap": 0,
        },
        tolerances={"relative_identity": 1.0e-11, "spectral": 1.0e-10, "cost": 1.0e-10},
        observed={
            "schur_identity_relative_residual": identity_residual,
            "gap_minimum_eigenvalue": float(gap_eig.min()),
            "gap_rank": gap_rank,
            "closed_cost": closed_cost,
            "direct_cost": direct_cost,
            "constraint_residual": constraint_residual,
            "orthogonal_control_residual": orth_residual,
        },
        interpretation="The check independently reconstructs the block-inversion and KKT endpoints.",
    )


def gaussian_kl(
    mu_q: np.ndarray, cov_q: np.ndarray, mu_p: np.ndarray, cov_p: np.ndarray
) -> float:
    n = mu_q.size
    precision_p = np.linalg.inv(cov_p)
    delta = mu_p - mu_q
    sign_q, logdet_q = np.linalg.slogdet(cov_q)
    sign_p, logdet_p = np.linalg.slogdet(cov_p)
    if sign_q <= 0 or sign_p <= 0:
        raise ValueError("KL received a non-positive covariance")
    return 0.5 * float(
        np.trace(precision_p @ cov_q)
        + delta @ precision_p @ delta
        - n
        + logdet_p
        - logdet_q
    )


def check_ig_expectation_metric() -> dict[str, Any]:
    seed = 7
    rng = np.random.default_rng(seed)
    n = 4
    precision = random_spd(rng, n, 2.0)
    covariance = np.linalg.inv(precision)
    mu = 0.15 * rng.standard_normal(n)
    moment2 = covariance + np.outer(mu, mu)
    g_expectation = (
        (1.0 + float(mu @ precision @ mu)) * precision
        + np.outer(precision @ mu, precision @ mu)
    )
    eps_values = [1.0e-3, 5.0e-4, 2.5e-4]
    expectation_errors: list[float] = []
    moment_errors: list[float] = []
    for _ in range(6):
        u = rng.standard_normal(n)
        u /= np.linalg.norm(u)
        predicted_exp = float(u @ g_expectation @ u)
        predicted_moment = float(u @ precision @ u)
        raw_exp: list[float] = []
        raw_moment: list[float] = []
        for eps in eps_values:
            mu_eps = mu + eps * u
            cov_eps = moment2 - np.outer(mu_eps, mu_eps)
            raw_exp.append(2.0 * gaussian_kl(mu_eps, cov_eps, mu, covariance) / eps**2)
            raw_moment.append(
                2.0 * gaussian_kl(mu_eps, covariance, mu, covariance) / eps**2
            )
        extrap_exp = 2.0 * raw_exp[-1] - raw_exp[-2]
        extrap_moment = 2.0 * raw_moment[-1] - raw_moment[-2]
        expectation_errors.append(abs(extrap_exp - predicted_exp) / max(abs(predicted_exp), 1.0))
        moment_errors.append(abs(extrap_moment - predicted_moment) / max(abs(predicted_moment), 1.0))
    generalized = sla.eigvalsh(g_expectation, precision)
    mahalanobis = float(mu @ precision @ mu)
    predicted_spectrum = np.sort(
        np.array([1.0 + mahalanobis] * (n - 1) + [1.0 + 2.0 * mahalanobis])
    )
    spectrum_error = float(np.max(np.abs(np.sort(generalized) - predicted_spectrum)))
    passed = max(expectation_errors) <= 2.0e-5 and max(moment_errors) <= 2.0e-5 and spectrum_error <= 1.0e-10
    return result(
        "CHK-IG-EXPECTATION-METRIC",
        "Expectation-chart Fisher metric from finite-difference KL",
        ["NUM-IG-EXPECTATION-METRIC", "NUM-IG-REGISTER-CHART"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count={"directions": 6, "epsilon_values": eps_values},
        expected={
            "expectation_chart_matches_closed_form": True,
            "moment_chart_matches_precision": True,
            "generalized_spectrum_matches_formula": True,
        },
        tolerances={"relative_quadratic_form": 2.0e-5, "spectrum_absolute": 1.0e-10},
        observed={
            "worst_expectation_chart_relative_error": max(expectation_errors),
            "worst_moment_chart_relative_error": max(moment_errors),
            "mahalanobis_squared": mahalanobis,
            "observed_generalized_spectrum": generalized,
            "predicted_generalized_spectrum": predicted_spectrum,
            "spectrum_max_absolute_error": spectrum_error,
        },
        interpretation="This reproduces the finite-difference route under a fully specified current base point; it does not recreate the omitted 2,000,000-sample score run.",
    )


def check_ig_pullback_pushforward() -> dict[str, Any]:
    seed = 99
    rng = np.random.default_rng(seed)
    n, k, draws = 12, 5, 200
    minimum_eigenvalue = math.inf
    max_identity_error = 0.0
    for _ in range(draws):
        lam = random_spd(rng, n)
        q, _ = np.linalg.qr(rng.standard_normal((n, n)))
        b, bp = q[:, :k], q[:, k:]
        lhs = b.T @ lam @ b - np.linalg.inv(b.T @ np.linalg.inv(lam) @ b)
        rhs = b.T @ lam @ bp @ np.linalg.inv(bp.T @ lam @ bp) @ bp.T @ lam @ b
        minimum_eigenvalue = min(
            minimum_eigenvalue, float(np.linalg.eigvalsh((lhs + lhs.T) / 2).min())
        )
        max_identity_error = max(max_identity_error, fro_relative(lhs, rhs))
    lam = random_spd(rng, n)
    _, eigenvectors = np.linalg.eigh(lam)
    b, bp = eigenvectors[:, :k], eigenvectors[:, k:]
    orth_gap = b.T @ lam @ b - np.linalg.inv(b.T @ np.linalg.inv(lam) @ b)
    orth_residual = float(np.linalg.norm(orth_gap, ord="fro"))
    passed = minimum_eigenvalue >= -1.0e-10 and max_identity_error <= 1.0e-11 and orth_residual <= 1.0e-10
    return result(
        "CHK-IG-PULLBACK-PUSHFORWARD",
        "Pullback versus pushforward Fisher metric",
        ["NUM-IG-PULLBACK-PUSHFORWARD"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count=draws,
        expected={"all_gaps_positive_semidefinite": True, "schur_identity": True, "orthogonal_control_gap": 0},
        tolerances={"spectral": 1.0e-10, "relative_identity": 1.0e-11},
        observed={
            "minimum_gap_eigenvalue": minimum_eigenvalue,
            "maximum_identity_relative_error": max_identity_error,
            "orthogonal_control_residual": orth_residual,
        },
        interpretation="The numerical check corroborates the proved Schur identity and Loewner order.",
    )


def check_generalized_spectrum() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    n, k = 6, 3
    weights: dict[tuple[int, int], np.ndarray] = {}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.6:
                weights[(i, j)] = random_spd(rng, k, 0.1)
    self_terms = [random_spd(rng, k, 0.2) for _ in range(n)]
    precision, lap = assemble_interaction(self_terms, weights)
    baseline = sla.eigvalsh(lap, precision)
    baseline_ordinary = np.linalg.eigvalsh(precision)
    max_generalized_error = 0.0
    ordinary_maxima: list[float] = []
    ordinary_minima: list[float] = []
    actual_conditions: list[float] = []
    for _ in range(12):
        blocks = [random_frame_with_condition(rng, k, 22.0) for _i in range(n)]
        transform = sla.block_diag(*blocks)
        actual_conditions.append(float(np.linalg.cond(transform)))
        lap_t = transform.T @ lap @ transform
        precision_t = transform.T @ precision @ transform
        current = sla.eigvalsh(lap_t, precision_t)
        max_generalized_error = max(
            max_generalized_error, float(np.max(np.abs(np.sort(current) - np.sort(baseline))))
        )
        ordinary = np.linalg.eigvalsh(precision_t)
        ordinary_maxima.append(float(ordinary[-1]))
        ordinary_minima.append(float(ordinary[0]))
    maximum_spread = max(ordinary_maxima) / min(ordinary_maxima)
    minimum_spread = max(ordinary_minima) / min(ordinary_minima)
    passed = max_generalized_error <= 1.0e-9 and max(maximum_spread, minimum_spread) > 1.1
    return result(
        "CHK-GENERALIZED-SPECTRUM",
        "Generalized spectrum under block congruence",
        [
            "NUM-IG-GAUGE-INVARIANTS",
            "NUM-IG-REGISTER-GAUGE",
            "NUM-RG-GENERALIZED-SPECTRUM",
        ],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count=12,
        expected={"generalized_spectrum_invariant": True, "ordinary_spectrum_not_invariant": True},
        tolerances={"generalized_eigenvalue_absolute": 1.0e-9},
        observed={
            "maximum_generalized_eigenvalue_error": max_generalized_error,
            "ordinary_largest_eigenvalue_spread": maximum_spread,
            "ordinary_smallest_eigenvalue_spread": minimum_spread,
            "transform_condition_numbers": actual_conditions,
            "baseline_ordinary_condition_number": float(baseline_ordinary[-1] / baseline_ordinary[0]),
        },
        interpretation="Congruence invariance is a property of the pencil; ordinary eigenvalues provide the negative control.",
    )


def check_cg_aggregation() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    n, k = 7, 3
    assignments = [0, 0, 1, 1, 1, 2, 2]
    weights = {
        (i, j): random_spd(rng, k, 0.1)
        for i in range(n)
        for j in range(i + 1, n)
    }
    self_terms = [random_spd(rng, k, 0.1) for _ in range(n)]
    precision, lap = assemble_interaction(self_terms, weights)
    s = incidence_map(assignments, k)
    coarse = s.T @ precision @ s

    nc = 3
    coarse_self = [
        sum((self_terms[i] for i in range(n) if assignments[i] == c), np.zeros((k, k)))
        for c in range(nc)
    ]
    coarse_weights: dict[tuple[int, int], np.ndarray] = {}
    for ci in range(nc):
        for cj in range(ci + 1, nc):
            coarse_weights[(ci, cj)] = sum(
                (
                    w
                    for (i, j), w in weights.items()
                    if {assignments[i], assignments[j]} == {ci, cj}
                ),
                np.zeros((k, k)),
            )
    predicted, _ = assemble_interaction(coarse_self, coarse_weights)
    formula_error = fro_relative(coarse, predicted)
    consensus_residual = float(
        np.linalg.norm(lap @ np.kron(np.ones((n, 1)), np.eye(k)), ord="fro")
    )
    perturbed_weights = {key: value.copy() for key, value in weights.items()}
    v = rng.standard_normal(k)
    delta = 100.0 * np.outer(v, v)
    perturbed_weights[(0, 1)] += delta
    perturbed_precision, _ = assemble_interaction(self_terms, perturbed_weights)
    internal_effect = float(np.linalg.norm(s.T @ perturbed_precision @ s - coarse, ord="fro"))
    passed = formula_error <= 1.0e-11 and consensus_residual <= 1.0e-10 and internal_effect <= 1.0e-9
    return result(
        "CHK-CG-AGGREGATION",
        "Coarse block identity and internal-edge annihilation",
        ["NUM-CG-AGGREGATION"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count=1,
        expected={"coarse_formula": True, "fine_consensus_null": True, "internal_edge_effect_on_coarse_operator": 0},
        tolerances={"relative_formula": 1.0e-11, "absolute_residual": 1.0e-9},
        observed={
            "coarse_formula_relative_error": formula_error,
            "fine_consensus_residual": consensus_residual,
            "internal_edge_perturbation_norm": float(np.linalg.norm(delta, ord="fro")),
            "coarse_operator_change": internal_effect,
        },
        interpretation="The check evaluates the exact congruence and independently assembled coarse parameters.",
    )


def check_graph_holonomy() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    k = 3
    rank_rtol = 1.0e-9

    def scale_relative_nullity(matrix: np.ndarray) -> tuple[int, float, np.ndarray]:
        singular = np.linalg.svd(matrix, compute_uv=False)
        tolerance = rank_rtol * max(float(singular[0]), 1.0)
        return int(np.count_nonzero(singular <= tolerance)), tolerance, singular

    def twisted_laplacian(
        edges: list[tuple[int, int, np.ndarray]], weights: list[np.ndarray]
    ) -> np.ndarray:
        out = np.zeros((3 * k, 3 * k))
        for (i, j, theta_ij), weight in zip(edges, weights):
            residual = np.zeros((k, 3 * k))
            residual[:, i * k : (i + 1) * k] = np.eye(k)
            residual[:, j * k : (j + 1) * k] = -theta_ij
            out += residual.T @ weight @ residual
        return out

    frames = [random_gl_plus(rng, k) for _ in range(3)]
    flat_edges = [
        (0, 1, frames[0] @ np.linalg.inv(frames[1])),
        (1, 2, frames[1] @ np.linalg.inv(frames[2])),
        (2, 0, frames[2] @ np.linalg.inv(frames[0])),
    ]
    weights = [random_spd(rng, k, 1.0) for _ in flat_edges]
    flat_loop = flat_edges[0][2] @ flat_edges[1][2] @ flat_edges[2][2]
    flat_defect = float(np.linalg.norm(flat_loop - np.eye(k), ord="fro"))
    flat_laplacian = twisted_laplacian(flat_edges, weights)
    flat_nullity, flat_rank_tolerance, flat_singular = scale_relative_nullity(flat_laplacian)

    trivialized = [
        np.linalg.inv(frames[i]) @ theta_ij @ frames[j]
        for i, j, theta_ij in flat_edges
    ]
    trivialization_residual = max(
        float(np.linalg.norm(item - np.eye(k), ord="fro")) for item in trivialized
    )

    angle = 0.7
    rotation = np.array(
        [
            [math.cos(angle), -math.sin(angle), 0.0],
            [math.sin(angle), math.cos(angle), 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    retwisted_edges = [
        (0, 1, np.eye(k)),
        (1, 2, np.eye(k)),
        (2, 0, rotation),
    ]
    retwisted_loop = rotation
    retwisted_laplacian = twisted_laplacian(retwisted_edges, weights)
    retwisted_nullity, retwisted_rank_tolerance, retwisted_singular = (
        scale_relative_nullity(retwisted_laplacian)
    )
    fixed_nullity, fixed_tolerance, fixed_singular = scale_relative_nullity(
        retwisted_loop - np.eye(k)
    )

    conditioner = random_frame_with_condition(rng, k, 1.0e4)
    stressed_loop = conditioner @ rotation @ np.linalg.inv(conditioner)
    stressed_edges = [
        (0, 1, np.eye(k)),
        (1, 2, np.eye(k)),
        (2, 0, stressed_loop),
    ]
    stressed_laplacian = twisted_laplacian(stressed_edges, weights)
    stressed_nullity, stressed_rank_tolerance, stressed_singular = (
        scale_relative_nullity(stressed_laplacian)
    )
    stressed_fixed_nullity, stressed_fixed_tolerance, stressed_fixed_singular = (
        scale_relative_nullity(stressed_loop - np.eye(k))
    )

    gauges = [random_gl_plus(rng, k) for _ in range(3)]
    transformed = {
        (i, j): gauges[i] @ theta_ij @ np.linalg.inv(gauges[j])
        for i, j, theta_ij in flat_edges
    }
    transformed_loop = (
        transformed[(0, 1)] @ transformed[(1, 2)] @ transformed[(2, 0)]
    )
    conjugacy_residual = float(
        np.linalg.norm(
            transformed_loop - gauges[0] @ flat_loop @ np.linalg.inv(gauges[0]),
            ord="fro",
        )
    )
    cut_a = random_gl_plus(rng, k)
    cut_equal = float(
        np.linalg.norm(cut_a @ np.linalg.inv(cut_a) - np.eye(k), ord="fro")
    )
    cut_b = random_gl_plus(rng, k)
    cut_distinct = float(
        np.linalg.norm(cut_a @ np.linalg.inv(cut_b) - np.eye(k), ord="fro")
    )
    passed = (
        flat_defect <= 1.0e-10
        and trivialization_residual <= 1.0e-10
        and flat_nullity == k
        and retwisted_nullity == fixed_nullity == 1
        and stressed_nullity == stressed_fixed_nullity == 1
        and conjugacy_residual <= 1.0e-10
        and cut_equal <= 1.0e-10
        and cut_distinct > 1.0e-3
    )
    return result(
        "CHK-GRAPH-HOLONOMY",
        "Graph holonomy, twisted-Laplacian kernels, and conditioned-similarity control",
        ["NUM-CG-HOLONOMY", "NUM-RG-HOLONOMY"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count="one coboundary triangle, one retwisted triangle, one condition-1e4 similarity stress case, and cut-pair controls",
        expected={
            "flat_loop": "identity",
            "flat_laplacian_nullity": k,
            "retwisted_laplacian_nullity": "dim ker(H-I)",
            "conditioned_similarity_nullity": "dim ker(S H S^-1-I)",
            "two_cut_edge_walk_identity_iff_equal": True,
        },
        tolerances={
            "identity_and_conjugacy_absolute": 1.0e-10,
            "rank_relative_singular_value": rank_rtol,
            "nontrivial_cut_defect": 1.0e-3,
        },
        observed={
            "flat_loop_defect": flat_defect,
            "trivialization_residual": trivialization_residual,
            "flat_laplacian": {
                "nullity": flat_nullity,
                "rank_tolerance": flat_rank_tolerance,
                "singular_values": flat_singular,
            },
            "retwisted": {
                "laplacian_nullity": retwisted_nullity,
                "fixed_space_dimension": fixed_nullity,
                "laplacian_rank_tolerance": retwisted_rank_tolerance,
                "fixed_space_rank_tolerance": fixed_tolerance,
                "laplacian_singular_values": retwisted_singular,
                "H_minus_I_singular_values": fixed_singular,
            },
            "conditioned_similarity_stress": {
                "condition_number": float(np.linalg.cond(conditioner)),
                "laplacian_nullity": stressed_nullity,
                "fixed_space_dimension": stressed_fixed_nullity,
                "laplacian_rank_tolerance": stressed_rank_tolerance,
                "fixed_space_rank_tolerance": stressed_fixed_tolerance,
                "laplacian_singular_values": stressed_singular,
                "H_minus_I_singular_values": stressed_fixed_singular,
            },
            "conjugacy_residual": conjugacy_residual,
            "equal_cut_walk_defect": cut_equal,
            "distinct_cut_walk_defect": cut_distinct,
        },
        interpretation="The weighted graph-Laplacian nullity is compared directly with the loop fixed space. The conditioned-similarity case is a numerical stress test, not a substitute for the exact kernel proof.",
    )


def check_cg_maximal_clusters() -> dict[str, Any]:
    vertices = (0, 1, 2)
    k = 2
    angle = 0.73
    rotation = np.array(
        [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]
    )
    directed = {
        (0, 1): np.eye(k),
        (1, 0): np.eye(k),
        (1, 2): np.eye(k),
        (2, 1): np.eye(k),
        (2, 0): rotation,
        (0, 2): rotation.T,
    }

    def trivializable(subset: frozenset[int]) -> tuple[bool, float]:
        root = min(subset)
        potentials: dict[int, np.ndarray] = {root: np.eye(k)}
        queue = [root]
        while queue:
            i = queue.pop(0)
            for j in sorted(subset):
                if (i, j) not in directed or j in potentials:
                    continue
                # Theta_ij = T_i T_j^{-1}, hence T_j = Theta_ij^{-1} T_i.
                potentials[j] = np.linalg.inv(directed[(i, j)]) @ potentials[i]
                queue.append(j)
        if len(potentials) != len(subset):
            return False, math.inf
        residual = 0.0
        for (i, j), theta_ij in directed.items():
            if i in subset and j in subset:
                residual = max(
                    residual,
                    float(
                        np.linalg.norm(
                            theta_ij - potentials[i] @ np.linalg.inv(potentials[j]),
                            ord="fro",
                        )
                    ),
                )
        return residual <= 1.0e-10, residual

    subsets = [
        frozenset(i for i in vertices if mask & (1 << i))
        for mask in range(1, 1 << len(vertices))
    ]
    subset_results = {}
    admissible: list[frozenset[int]] = []
    for subset in subsets:
        is_admissible, residual = trivializable(subset)
        subset_results["".join(map(str, sorted(subset)))] = {
            "vertices": sorted(subset),
            "trivializable": is_admissible,
            "maximum_transport_residual": residual,
        }
        if is_admissible:
            admissible.append(subset)
    maximal = [s for s in admissible if not any(s < t for t in admissible)]

    def all_set_partitions(items: tuple[int, ...]) -> list[list[frozenset[int]]]:
        if not items:
            return [[]]
        first, rest = items[0], items[1:]
        output: list[list[frozenset[int]]] = []
        for partition in all_set_partitions(rest):
            output.append([frozenset({first})] + partition)
            for index in range(len(partition)):
                expanded = list(partition)
                expanded[index] = frozenset(set(expanded[index]) | {first})
                output.append(expanded)
        canonical: dict[tuple[tuple[int, ...], ...], list[frozenset[int]]] = {}
        for partition in output:
            key = tuple(sorted(tuple(sorted(block)) for block in partition))
            canonical[key] = [frozenset(block) for block in key]
        return list(canonical.values())

    partitions = all_set_partitions(vertices)
    admissible_partitions = [
        partition
        for partition in partitions
        if all(block in admissible for block in partition)
    ]
    loop = directed[(0, 1)] @ directed[(1, 2)] @ directed[(2, 0)]
    loop_defect = float(np.linalg.norm(loop - np.eye(k), ord="fro"))
    passed = (
        loop_defect > 1.0e-3
        and len(subsets) == 7
        and len(admissible) == 6
        and len(maximal) == 3
        and len(partitions) == 5
        and len(admissible_partitions) == 4
        and not subset_results["012"]["trivializable"]
    )
    return result(
        "CHK-CG-MAXIMAL-CLUSTERS",
        "Algorithmic non-flat triangle holonomy and partition enumeration",
        ["REVIEW-CG-MAXIMAL-CLUSTERS"],
        status="PASS" if passed else "FAIL",
        seed=None,
        sample_count="all seven induced nonempty subgraphs and all five algorithmically generated set partitions",
        expected={
            "full_triangle_cycle_nonidentity": True,
            "admissible_nonempty_subsets": 6,
            "maximal_admissible_subsets": 3,
            "generated_set_partitions": 5,
            "admissible_partitions": 4,
        },
        tolerances={
            "transport_identity_absolute": 1.0e-10,
            "nonidentity_cycle_defect": 1.0e-3,
            "enumeration": "exact integer counts",
        },
        observed={
            "triangle_loop_defect": loop_defect,
            "subset_results": subset_results,
            "admissible_nonempty_subsets": len(admissible),
            "maximal_admissible_subsets": len(maximal),
            "generated_set_partitions": len(partitions),
            "admissible_partitions": len(admissible_partitions),
            "maximal_sets": [sorted(x) for x in maximal],
            "admissible_partition_blocks": [
                [sorted(block) for block in partition]
                for partition in admissible_partitions
            ],
        },
        evidence_kind="algorithmic_exact_enumeration_with_floating_transport_witness",
        interpretation="Admissibility is computed from restricted transport consistency. No subset is classified by cardinality, and no partition list is supplied by hand.",
    )


def lambda_interaction(
    n: int, k: int, weights: dict[tuple[int, int], np.ndarray], lam: float
) -> np.ndarray:
    out = np.zeros((n * k, n * k))
    for (i, j), w in weights.items():
        si = slice(i * k, (i + 1) * k)
        sj = slice(j * k, (j + 1) * k)
        out[si, si] += w
        out[sj, sj] += w
        out[si, sj] -= lam * w
        out[sj, si] -= lam * w
    return out


def check_cg_lambda_continuum() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    n, k = 7, 3
    assignments = [0, 0, 1, 1, 1, 2, 2]
    nc = max(assignments) + 1
    aggregation = incidence_map(assignments, k)
    weights = {
        (i, j): random_spd(rng, k, 0.1)
        for i in range(n)
        for j in range(i + 1, n)
        if rng.random() < 0.55
    }
    self_terms = [random_spd(rng, k, 0.2) for _ in range(n)]
    inside = [-1.0, -0.5, 0.0, 0.5, 0.9, 1.0]
    min_inside = {
        str(lam): float(
            np.linalg.eigvalsh(lambda_interaction(n, k, weights, lam)).min()
        )
        for lam in inside
    }
    coarse_formula_errors = {}
    coarse_minimum_eigenvalues = {}
    for lam in inside:
        fine = lambda_interaction(n, k, weights, lam)
        for i, self_term in enumerate(self_terms):
            si = slice(i * k, (i + 1) * k)
            fine[si, si] += self_term
        aggregated = aggregation.T @ fine @ aggregation

        coarse_weights: dict[tuple[int, int], np.ndarray] = {}
        for ci in range(nc):
            for cj in range(ci + 1, nc):
                coarse_weights[(ci, cj)] = sum(
                    (
                        weight
                        for (i, j), weight in weights.items()
                        if {assignments[i], assignments[j]} == {ci, cj}
                    ),
                    np.zeros((k, k)),
                )
        coarse_self_terms = []
        for ci in range(nc):
            additive_self = sum(
                (
                    self_terms[i]
                    for i in range(n)
                    if assignments[i] == ci
                ),
                np.zeros((k, k)),
            )
            internal = sum(
                (
                    weight
                    for (i, j), weight in weights.items()
                    if assignments[i] == ci and assignments[j] == ci
                ),
                np.zeros((k, k)),
            )
            coarse_self_terms.append(additive_self + 2.0 * (1.0 - lam) * internal)
        predicted = lambda_interaction(nc, k, coarse_weights, lam)
        for ci, self_term in enumerate(coarse_self_terms):
            si = slice(ci * k, (ci + 1) * k)
            predicted[si, si] += self_term
        coarse_formula_errors[str(lam)] = fro_relative(aggregated, predicted)
        coarse_minimum_eigenvalues[str(lam)] = float(
            np.linalg.eigvalsh(aggregated).min()
        )

    two_node = {(0, 1): np.eye(k)}
    outside_min = {
        str(lam): float(np.linalg.eigvalsh(lambda_interaction(2, k, two_node, lam)).min())
        for lam in [-1.2, 1.2]
    }
    symbolic_lambda = sp.symbols("lambda", real=True)
    symbolic_two_node = sp.Matrix(
        [[1, -symbolic_lambda], [-symbolic_lambda, 1]]
    )
    symbolic_characteristic = sp.factor(
        symbolic_two_node.charpoly().as_expr()
    )
    symbolic_eigenvalues = {
        str(eigenvalue): int(multiplicity)
        for eigenvalue, multiplicity in symbolic_two_node.eigenvals().items()
    }
    consensus = np.kron(np.ones((n, 1)), np.eye(k))
    residuals = {
        str(lam): float(np.linalg.norm(lambda_interaction(n, k, weights, lam) @ consensus, ord="fro"))
        for lam in inside
    }
    scaled = [residuals[str(lam)] / (1.0 - lam) for lam in inside if lam < 1.0]
    scaled_spread = max(scaled) - min(scaled)
    lap = lambda_interaction(n, k, weights, 1.0)
    signless = lambda_interaction(n, k, weights, -1.0)
    convex_error = 0.0
    for lam in inside:
        predicted = 0.5 * (1 + lam) * lap + 0.5 * (1 - lam) * signless
        convex_error = max(convex_error, fro_relative(lambda_interaction(n, k, weights, lam), predicted))
    passed = (
        min(min_inside.values()) >= -1.0e-9
        and max(outside_min.values()) < -0.1
        and max(coarse_formula_errors.values()) <= 1.0e-11
        and min(coarse_minimum_eigenvalues.values()) > 0
        and residuals["1.0"] <= 1.0e-9
        and scaled_spread <= 1.0e-9
        and convex_error <= 1.0e-12
    )
    return result(
        "CHK-CG-LAMBDA-CONTINUUM",
        "Positive-semidefinite lambda interval and translation-invariance control",
        ["NUM-CG-LAMBDA-CONTINUUM", "NUM-CG-TRANSLATION"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count="six in-interval values and two exact two-node controls",
        expected={
            "inside_interval_positive_semidefinite": True,
            "outside_controls_indefinite": True,
            "aggregated_operator": "independently assembled coarse self/coupling form",
            "consensus_residual_proportional_to_1_minus_lambda": True,
            "two_node_exact_eigenvalues": ["1-lambda", "1+lambda"],
        },
        tolerances={
            "spectral": 1.0e-9,
            "coarse_formula_relative": 1.0e-11,
            "relative_identity": 1.0e-12,
            "symbolic": "exact",
        },
        observed={
            "inside_minimum_eigenvalues": min_inside,
            "coarse_formula_relative_errors": coarse_formula_errors,
            "coarse_minimum_eigenvalues": coarse_minimum_eigenvalues,
            "outside_two_node_minimum_eigenvalues": outside_min,
            "two_node_symbolic_characteristic_polynomial": str(
                symbolic_characteristic
            ),
            "two_node_symbolic_eigenvalues": symbolic_eigenvalues,
            "consensus_residuals": residuals,
            "scaled_residual_spread": scaled_spread,
            "convex_decomposition_max_relative_error": convex_error,
        },
        interpretation="For every tested lambda, the coarse parameters are assembled independently from block sums and compared with the congruence. The exact two-node symbolic witness establishes sharp failure outside the interval.",
    )


def check_cg_pair_merge() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    n, k = 7, 2
    m = rng.standard_normal((n * k, n * k))
    lam = (m + m.T) / 2
    maps = [
        [0, 0, 1, 2, 3, 4, 5],
        [0, 1, 1, 2, 3, 4],
        [0, 1, 1, 2, 3],
        [0, 1, 2, 2],
    ]
    scalar_product = np.eye(n)
    current = lam.copy()
    for assignment in maps:
        p = np.zeros((len(assignment), max(assignment) + 1))
        p[np.arange(len(assignment)), assignment] = 1.0
        scalar_product = scalar_product @ p
        s = np.kron(p, np.eye(k))
        current = s.T @ current @ s
    one_shot_s = np.kron(scalar_product, np.eye(k))
    one_shot = one_shot_s.T @ lam @ one_shot_s
    error = float(np.linalg.norm(current - one_shot, ord="fro"))
    expected_assignment = np.array([0, 0, 1, 1, 1, 2, 2])
    assignment_error = float(
        np.linalg.norm(scalar_product - incidence_map(expected_assignment.tolist(), 1))
    )
    passed = error <= 1.0e-12 and assignment_error == 0
    return result(
        "CHK-CG-PAIR-MERGE",
        "Pair-merge factorization of a partition congruence",
        ["NUM-CG-PAIR-MERGE"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count="one matrix and four pair merges",
        expected={
            "sequential_minus_one_shot_residual": "<= declared tolerance",
            "incidence_product_residual": "<= declared tolerance",
            "pair_merge_count": 4,
        },
        tolerances={"absolute_matrix_residual": 1.0e-12},
        observed={"matrix_residual": error, "incidence_product_residual": assignment_error},
        interpretation="The check is a floating-point evaluation of matrix associativity already proved in the text.",
    )


def check_cg_biadditive() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    n, k = 8, 3
    x = rng.uniform(0.2, 2.0, size=n)
    m = random_spd(rng, k)
    a = random_spd(rng, k)
    weights = {(i, j): x[i] * x[j] * m for i in range(n) for j in range(i + 1, n)}
    self_terms = [x[i] * a for i in range(n)]
    assignments = [0, 0, 0, 1, 1, 2, 2, 2]
    s = incidence_map(assignments, k)
    precision, _ = assemble_interaction(self_terms, weights)
    coarse = s.T @ precision @ s
    xc = np.array([sum(x[i] for i in range(n) if assignments[i] == c) for c in range(3)])
    predicted_weights = {(i, j): xc[i] * xc[j] * m for i in range(3) for j in range(i + 1, 3)}
    predicted_self = [xc[i] * a for i in range(3)]
    predicted, _ = assemble_interaction(predicted_self, predicted_weights)
    error = fro_relative(coarse, predicted)
    passed = error <= 1.0e-12
    return result(
        "CHK-CG-BIADDITIVE",
        "Bi-additive coupling and additive self closure",
        ["NUM-CG-BIADDITIVE"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count=1,
        expected={"coarse_parameters_equal_block-summed_form": True},
        tolerances={"relative_matrix": 1.0e-12},
        observed={"relative_matrix_error": error, "coarse_node_weights": xc},
        interpretation="The equality is checked directly from the fine and coarse assembled operators.",
    )


def check_cg_epsilon_divergence() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    n, r = 12, 6
    m = n - r
    lam = random_spd(rng, n)
    q, _ = np.linalg.qr(rng.standard_normal((n, n)))
    b, bp = q[:, :r], q[:, r:]
    c_parallel = np.linalg.inv(b.T @ lam @ b)
    cov_p = np.linalg.inv(lam)
    volume = 0.5 * np.linalg.slogdet(bp.T @ cov_p @ bp)[1]
    eps_values = [1.0e-3, 1.0e-4, 1.0e-6, 1.0e-8]
    measured: dict[str, float] = {}
    predicted_leading: dict[str, float] = {}
    remainders: dict[str, float] = {}
    trace_perp = float(np.trace(bp.T @ lam @ bp))
    for eps in eps_values:
        cov_q = b @ c_parallel @ b.T + eps * bp @ bp.T
        value = gaussian_kl(np.zeros(n), cov_q, np.zeros(n), cov_p)
        leading = 0.5 * m * math.log(1.0 / eps) - 0.5 * m + volume
        measured[str(eps)] = value
        predicted_leading[str(eps)] = leading
        remainders[str(eps)] = value - leading
    expected_remainders = {str(eps): 0.5 * eps * trace_perp for eps in eps_values}
    remainder_error = max(
        abs(remainders[str(eps)] - expected_remainders[str(eps)]) for eps in eps_values
    )
    slope = measured[str(1.0e-8)] - measured[str(1.0e-6)]
    predicted_slope = 0.5 * m * math.log(100.0)
    passed = abs(slope - predicted_slope - (expected_remainders[str(1.0e-8)] - expected_remainders[str(1.0e-6)])) <= 1.0e-8 and remainder_error <= 1.0e-8
    return result(
        "CHK-CG-EPSILON-DIVERGENCE",
        "Regularized identification divergence",
        ["NUM-CG-EPS-DIVERGENCE"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count={"epsilon_values": eps_values},
        expected={"leading_slope": "(m/2) log(1/epsilon)", "remainder": "(epsilon/2) trace(B_perp^T Lambda B_perp)"},
        tolerances={"absolute_identity": 1.0e-8},
        observed={
            "m": m,
            "measured_costs": measured,
            "leading_predictions": predicted_leading,
            "measured_remainders": remainders,
            "expected_remainders": expected_remainders,
            "maximum_remainder_error": remainder_error,
            "two_decade_increment": slope,
            "predicted_leading_two_decade_increment": predicted_slope,
        },
        interpretation="The current check evaluates the full Gaussian KL and the analytic asymptotic expression independently.",
    )


GapStep = namedtuple(
    "GapStep",
    (
        "value",
        "left_block",
        "right_block",
        "singular_values",
        "scipy_singular_values",
        "numpy_singular_values",
        "min_one_minus_rho_squared",
        "cholesky_residual",
        "solve_residual",
        "residual_tolerance",
        "backward_error",
        "clipping_applied",
        "clipping_amount",
        "residual_derived_clip_bound",
        "boundary_fallback_applied",
        "high_precision_fallback_applied",
        "conditioning_triggered",
        "precision_condition_number",
        "boundary_acceptance_limit",
        "evaluation_method",
    ),
)
GapStep.__doc__ = "One two-block increment in a declared telescoping merge order."

GapResult = namedtuple(
    "GapResult",
    (
        "value",
        "steps",
        "merge_order",
        "backward_error_bound",
        "singular_values",
        "min_one_minus_rho_squared",
        "maximum_cholesky_residual",
        "clipping_applied",
        "clipping_amount",
        "residual_derived_clip_bound",
        "boundary_fallback_applied",
        "high_precision_fallback_applied",
        "conditioning_triggered",
    ),
)
GapResult.__doc__ = "Stable factorization-gap value and diagnostics."

FactorizationProtocolCase = namedtuple(
    "FactorizationProtocolCase",
    (
        "case_id",
        "stratum",
        "dimension",
        "condition_number",
        "replica",
        "matrix_seed",
        "partition",
    ),
)
FactorizationCaseRecord = namedtuple(
    "FactorizationCaseRecord",
    (
        "case_id",
        "stratum",
        "dimension",
        "condition_number",
        "achieved_condition_number",
        "matrix_digest",
        "partition_digest",
        "value",
        "backward_error_bound",
        "maximum_cholesky_residual",
        "evaluation_methods",
        "clipping_applied",
        "boundary_fallback_applied",
        "high_precision_fallback_applied",
    ),
)
FactorizationHighPrecisionControl = namedtuple(
    "FactorizationHighPrecisionControl",
    ("case_id", "decimal_digits", "reference_value"),
)
FactorizationProtocolReport = namedtuple(
    "FactorizationProtocolReport",
    (
        "protocol_name",
        "seed",
        "schedule_digest",
        "historical_generator_recovered",
        "cases",
        "high_precision_controls",
        "case_failures",
    ),
)


def _even_power_of_two_exponent(matrix: np.ndarray) -> int:
    """Return an even binary exponent that range-normalizes ``matrix``."""

    maximum = float(np.max(np.abs(matrix), initial=0.0))
    if maximum == 0.0:
        return 0
    exponent = math.frexp(maximum)[1]
    return exponent if exponent % 2 == 0 else exponent + 1


def _power_of_two_scaled(matrix: np.ndarray, exponent: int) -> np.ndarray:
    """Scale by an exact power of two while suppressing harmless underflow."""

    with np.errstate(under="ignore"):
        return np.ldexp(matrix, -exponent)


def _power_of_two_scaling_loses_nonzero(
    matrix: np.ndarray, scaled: np.ndarray
) -> bool:
    return bool(np.any((matrix != 0.0) & (scaled == 0.0)))


def _safe_symmetric_midpoint(matrix: np.ndarray) -> np.ndarray:
    """Midpoint transpose pairs without changing already equal entries."""

    transposed = matrix.T
    with np.errstate(under="ignore"):
        midpoint = 0.5 * matrix + 0.5 * transposed
    return np.where(matrix == transposed, matrix, midpoint)


def _adaptive_mp_digits(matrix: np.ndarray, *, minimum: int) -> int:
    """Resolve the full binary64 dynamic range with guard digits."""

    nonzero = np.abs(matrix[matrix != 0.0])
    if nonzero.size == 0:
        return minimum
    largest_exponent = math.frexp(float(np.max(nonzero)))[1]
    smallest_exponent = math.frexp(float(np.min(nonzero)))[1]
    dynamic_decimal_digits = math.ceil(
        (largest_exponent - smallest_exponent) * math.log10(2.0)
    )
    return max(minimum, dynamic_decimal_digits + 80)


def _stable_relative_matrix_residual(
    reference: np.ndarray, approximation: np.ndarray
) -> float:
    """Compute a range-safe Frobenius relative residual."""

    exponent = _even_power_of_two_exponent(reference)
    reference_scaled = _power_of_two_scaled(reference, exponent)
    approximation_scaled = _power_of_two_scaled(approximation, exponent)
    denominator = max(
        float(np.linalg.norm(reference_scaled, ord="fro")),
        np.finfo(float).tiny,
    )
    return float(
        np.linalg.norm(reference_scaled - approximation_scaled, ord="fro")
        / denominator
    )


def _validated_precision(lam: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    raw = np.asarray(lam)
    if np.iscomplexobj(raw):
        raise TypeError("factorization gap requires a real precision matrix")
    try:
        matrix = np.asarray(raw, dtype=np.float64)
    except (TypeError, ValueError) as exc:
        raise TypeError("factorization gap requires a numeric precision matrix") from exc
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or matrix.shape[0] == 0:
        raise ValueError("factorization gap requires a nonempty square precision matrix")
    if not np.isfinite(matrix).all():
        raise ValueError("factorization gap requires finite precision entries")
    exponent = _even_power_of_two_exponent(matrix)
    matrix_scaled = _power_of_two_scaled(matrix, exponent)
    scaling_lost_nonzero = _power_of_two_scaling_loses_nonzero(
        matrix, matrix_scaled
    )
    scaled_norm = max(
        float(np.linalg.norm(matrix_scaled, ord="fro")),
        np.finfo(float).tiny,
    )
    symmetry_residual = float(
        np.linalg.norm(matrix_scaled - matrix_scaled.T, ord="fro") / scaled_norm
    )
    symmetry_tolerance = 64.0 * matrix.shape[0] * np.finfo(float).eps
    if symmetry_residual > symmetry_tolerance:
        raise ValueError(
            "factorization gap precision is nonsymmetric beyond its scale-aware tolerance"
        )
    # Work on a globally range-normalized matrix whenever that exact power-of-
    # two scaling preserves every nonzero.  If the dynamic range is too large,
    # keep the exact binary64 entries and require an exact-dyadic MP Cholesky
    # certificate before any binary64 diagnostic can accept the input.
    matrix = _safe_symmetric_midpoint(
        matrix if scaling_lost_nonzero else matrix_scaled
    )
    high_precision_cholesky = None
    if scaling_lost_nonzero:
        try:
            with mpmath.workdps(_adaptive_mp_digits(matrix, minimum=200)):
                high_precision_cholesky = mpmath.cholesky(
                    _mp_exact_matrix(matrix), tol=mpmath.mpf("0")
                )
        except (ValueError, ZeroDivisionError) as high_precision_exc:
            raise ValueError(
                "factorization gap requires a positive definite precision"
            ) from high_precision_exc
    try:
        cholesky = np.linalg.cholesky(matrix)
    except np.linalg.LinAlgError as exc:
        # A finite binary64 SPD matrix can outstrip a binary64 diagnostic even
        # though its exact stored entries remain positive definite.  Confirm
        # that exact input by high-precision Cholesky before rejecting it.
        try:
            if high_precision_cholesky is None:
                with mpmath.workdps(_adaptive_mp_digits(matrix, minimum=200)):
                    high_precision_cholesky = mpmath.cholesky(
                        _mp_exact_matrix(matrix), tol=mpmath.mpf("0")
                    )
            cholesky = np.asarray(
                [
                    [
                        float(high_precision_cholesky[row, column])
                        for column in range(matrix.shape[0])
                    ]
                    for row in range(matrix.shape[0])
                ],
                dtype=float,
            )
        except (ValueError, ZeroDivisionError) as high_precision_exc:
            raise ValueError(
                "factorization gap requires a positive definite precision"
            ) from high_precision_exc
    cholesky_exponent = _even_power_of_two_exponent(matrix)
    matrix_for_residual = _power_of_two_scaled(matrix, cholesky_exponent)
    cholesky_for_residual = _power_of_two_scaled(
        cholesky, cholesky_exponent // 2
    )
    cholesky_residual = _stable_relative_matrix_residual(
        matrix_for_residual,
        cholesky_for_residual @ cholesky_for_residual.T,
    )
    if not math.isfinite(cholesky_residual):
        raise ValueError("factorization gap Cholesky residual is nonfinite")
    return matrix, cholesky, cholesky_residual


def validate_partition(
    lam: np.ndarray, blocks: Any
) -> tuple[tuple[int, ...], ...]:
    """Validate an SPD precision and an exact, nonempty coordinate partition."""

    matrix, _, _ = _validated_precision(lam)
    if isinstance(blocks, (str, bytes)):
        raise TypeError("partition must be an iterable of index blocks")
    try:
        raw_blocks = list(blocks)
    except TypeError as exc:
        raise TypeError("partition must be an iterable of index blocks") from exc
    if not raw_blocks:
        raise ValueError("partition must contain at least one block")
    normalized: list[tuple[int, ...]] = []
    seen: set[int] = set()
    for raw_block in raw_blocks:
        if isinstance(raw_block, (str, bytes)):
            raise TypeError("partition blocks must contain integer indices")
        try:
            entries = list(raw_block)
        except TypeError as exc:
            raise TypeError("partition blocks must be iterable") from exc
        if not entries:
            raise ValueError("partition blocks must be nonempty")
        block: list[int] = []
        for entry in entries:
            if isinstance(entry, (bool, np.bool_)) or not isinstance(
                entry, (int, np.integer)
            ):
                raise TypeError("partition indices must be integers")
            index = int(entry)
            if index < 0 or index >= matrix.shape[0]:
                raise ValueError("partition index is outside the precision matrix")
            if index in seen:
                raise ValueError("partition blocks overlap or repeat an index")
            seen.add(index)
            block.append(index)
        normalized.append(tuple(block))
    if seen != set(range(matrix.shape[0])):
        raise ValueError("partition must cover every precision coordinate exactly once")
    return tuple(normalized)


def _mp_exact_float(value: float) -> mpmath.mpf:
    numerator, denominator = float(value).as_integer_ratio()
    return mpmath.mpf(numerator) / denominator


def _mp_exact_matrix(matrix: np.ndarray) -> mpmath.matrix:
    return mpmath.matrix(
        [[_mp_exact_float(float(value)) for value in row] for row in matrix]
    )


def _mp_left_solve(lower: mpmath.matrix, right: mpmath.matrix) -> mpmath.matrix:
    solved = mpmath.matrix(lower.rows, right.cols)
    for column in range(right.cols):
        vector = mpmath.lu_solve(lower, right[:, column])
        for row in range(lower.rows):
            solved[row, column] = vector[row]
    return solved


def _mp_cholesky_logdet(
    matrix: mpmath.matrix,
) -> tuple[mpmath.matrix, mpmath.mpf]:
    """Certify MP positive definiteness and return its Cholesky logdet."""

    cholesky = mpmath.cholesky(matrix, tol=mpmath.mpf("0"))
    logdet = 2 * mpmath.fsum(
        mpmath.log(cholesky[index, index])
        for index in range(cholesky.rows)
    )
    if not mpmath.isfinite(logdet):
        raise ValueError("high-precision SPD log determinant is nonfinite")
    return cholesky, +logdet


def _high_precision_two_block(
    matrix: np.ndarray,
    left: tuple[int, ...],
    right: tuple[int, ...],
    *,
    digits: int = 200,
) -> tuple[mpmath.mpf, tuple[mpmath.mpf, ...]]:
    """Evaluate the exact binary64 input at high precision on the fallback path."""

    with mpmath.workdps(_adaptive_mp_digits(matrix, minimum=digits)):
        first = _mp_exact_matrix(matrix[np.ix_(left, left)])
        second = _mp_exact_matrix(matrix[np.ix_(right, right)])
        cross = _mp_exact_matrix(matrix[np.ix_(left, right)])
        whole = _mp_exact_matrix(matrix[np.ix_(left + right, left + right)])
        _, logdet_whole = _mp_cholesky_logdet(whole)
        left_cholesky, logdet_first = _mp_cholesky_logdet(first)
        right_cholesky, logdet_second = _mp_cholesky_logdet(second)
        left_solved = _mp_left_solve(left_cholesky, cross)
        canonical = _mp_left_solve(right_cholesky, left_solved.T).T
        singular = mpmath.svd(canonical, compute_uv=False)
        rho_squared = tuple(
            sorted(
                (singular[index] * singular[index] for index in range(singular.rows)),
                reverse=True,
            )
        )
        if rho_squared and rho_squared[0] >= 1:
            raise ValueError(
                "high-precision exact-input canonical correlation is not below one"
            )
        gap = (logdet_first + logdet_second - logdet_whole) / 2
        if not mpmath.isfinite(gap) or gap < 0:
            raise ValueError("high-precision exact-input gap is not finite and nonnegative")
        return +gap, tuple(+value for value in rho_squared)


def _high_precision_partition_gap(
    matrix: np.ndarray, partition: tuple[tuple[int, ...], ...], *, digits: int
) -> mpmath.mpf:
    with mpmath.workdps(_adaptive_mp_digits(matrix, minimum=digits)):
        whole_matrix = _mp_exact_matrix(matrix)
        _, whole_logdet = _mp_cholesky_logdet(whole_matrix)
        block_log_sum = mpmath.mpf("0")
        for block in partition:
            block_matrix = _mp_exact_matrix(matrix[np.ix_(block, block)])
            _, block_logdet = _mp_cholesky_logdet(block_matrix)
            block_log_sum += block_logdet
        return +(block_log_sum - whole_logdet) / 2


def _outward_float_upper(value: mpmath.mpf, *, digits: int = 220) -> float:
    with mpmath.workdps(digits):
        if value < 0 or not mpmath.isfinite(value):
            raise ValueError(
                "outward upper conversion requires a finite nonnegative value"
            )
        rounded = float(value)
        if _mp_exact_float(rounded) < value:
            rounded = math.nextafter(rounded, math.inf)
        return rounded


def _roundoff_scale(*values: float, dimension: int, multiplier: float = 64.0) -> float:
    magnitude = max((abs(float(value)) for value in values), default=0.0)
    magnitude = max(magnitude, np.finfo(float).tiny)
    return multiplier * max(1, dimension) * np.finfo(float).eps * magnitude


def _step_result(step: GapStep) -> GapResult:
    return GapResult(
        value=step.value,
        steps=(step,),
        merge_order=((step.left_block, step.right_block, step.left_block + step.right_block),),
        backward_error_bound=step.backward_error,
        singular_values=(step.singular_values,),
        min_one_minus_rho_squared=step.min_one_minus_rho_squared,
        maximum_cholesky_residual=step.cholesky_residual,
        clipping_applied=step.clipping_applied,
        clipping_amount=step.clipping_amount,
        residual_derived_clip_bound=step.residual_derived_clip_bound,
        boundary_fallback_applied=step.boundary_fallback_applied,
        high_precision_fallback_applied=step.high_precision_fallback_applied,
        conditioning_triggered=step.conditioning_triggered,
    )


def _positive_mp_to_float(value: mpmath.mpf) -> float:
    """Preserve the sign of a positive MP diagnostic after binary64 cast."""

    if value <= 0 or not mpmath.isfinite(value):
        raise ValueError("high-precision positive diagnostic left its domain")
    rounded = float(value)
    return rounded if rounded > 0.0 else math.nextafter(0.0, 1.0)


def _finite_diagnostic_or_none(value: Any) -> float | None:
    """Normalize one attempted diagnostic to a finite binary64 value or null."""

    if value is None:
        return None
    numeric = float(value)
    return numeric if math.isfinite(numeric) else None


def _high_precision_only_two_block_result(
    matrix: np.ndarray,
    left: tuple[int, ...],
    right: tuple[int, ...],
    *,
    precision_condition_number: float,
    reason: str,
    conditioning_triggered: bool = False,
    cholesky_residual: float | None = None,
    solve_residual: float | None = None,
    residual_tolerance: float | None = None,
    backward_error: float | None = None,
) -> GapResult:
    """Fail over to an exact-dyadic MP value when binary64 diagnostics fail."""

    high_precision_gap, exact_squared = _high_precision_two_block(
        matrix, left, right, digits=200
    )
    with mpmath.workdps(_adaptive_mp_digits(matrix, minimum=220)):
        singular_values = tuple(
            float(mpmath.sqrt(value)) for value in exact_squared
        )
        exact_max_squared = exact_squared[0] if exact_squared else mpmath.mpf("0")
        min_one_minus = _positive_mp_to_float(
            mpmath.mpf(1) - exact_max_squared
        )
    step = GapStep(
        value=float(high_precision_gap),
        left_block=left,
        right_block=right,
        singular_values=singular_values,
        scipy_singular_values=(),
        numpy_singular_values=(),
        min_one_minus_rho_squared=min_one_minus,
        cholesky_residual=_finite_diagnostic_or_none(cholesky_residual),
        solve_residual=_finite_diagnostic_or_none(solve_residual),
        residual_tolerance=_finite_diagnostic_or_none(residual_tolerance),
        backward_error=_finite_diagnostic_or_none(backward_error),
        clipping_applied=False,
        clipping_amount=0.0,
        residual_derived_clip_bound=0.0,
        boundary_fallback_applied=False,
        high_precision_fallback_applied=True,
        conditioning_triggered=conditioning_triggered,
        precision_condition_number=precision_condition_number,
        boundary_acceptance_limit=float(
            64.0 * matrix.shape[0] * np.finfo(float).eps
        ),
        evaluation_method=f"exact-binary64-mpmath-200d-{reason}-fallback",
    )
    return _step_result(step)


def two_block_factorization_gap(
    lam: np.ndarray, left_block: Any, right_block: Any
) -> GapResult:
    """Compute a stable two-block determinant gap from canonical correlations."""

    matrix, _, _ = _validated_precision(lam)
    left, right = validate_partition(matrix, [left_block, right_block])
    first = matrix[np.ix_(left, left)]
    second = matrix[np.ix_(right, right)]
    cross = matrix[np.ix_(left, right)]
    exact_block_diagonal = not np.count_nonzero(cross)
    global_exponent = _even_power_of_two_exponent(matrix)
    global_probe = _power_of_two_scaled(matrix, global_exponent)
    global_scaling_lost = _power_of_two_scaling_loses_nonzero(
        matrix, global_probe
    )
    try:
        with np.errstate(over="ignore", under="ignore", invalid="ignore"):
            precision_condition_number = (
                math.inf
                if global_scaling_lost
                else float(np.linalg.cond(global_probe, p=2))
            )
    except np.linalg.LinAlgError:
        precision_condition_number = math.inf
    conditioning_triggered = bool(
        not math.isfinite(precision_condition_number)
        or precision_condition_number * np.finfo(float).eps
        >= FACTORIZATION_CONDITIONING_TRIGGER
    )
    if global_scaling_lost or not math.isfinite(precision_condition_number):
        return _high_precision_only_two_block_result(
            matrix,
            left,
            right,
            precision_condition_number=precision_condition_number,
            reason="range-or-condition",
            conditioning_triggered=conditioning_triggered,
        )

    try:
        left_exponent = _even_power_of_two_exponent(first)
        right_exponent = _even_power_of_two_exponent(second)
        first_scaled = _power_of_two_scaled(first, left_exponent)
        second_scaled = _power_of_two_scaled(second, right_exponent)
        cross_scaled = _power_of_two_scaled(
            cross, left_exponent // 2 + right_exponent // 2
        )
        left_cholesky = np.linalg.cholesky(first_scaled)
        right_cholesky = np.linalg.cholesky(second_scaled)

        left_solved = sla.solve_triangular(
            left_cholesky, cross_scaled, lower=True, check_finite=False
        )
        canonical = sla.solve_triangular(
            right_cholesky, left_solved.T, lower=True, check_finite=False
        ).T
        scipy_singular = np.asarray(
            sla.svdvals(canonical, check_finite=False), dtype=float
        )

        # A second binary64 solve is a boundary diagnostic only.  The ordinary
        # value path remains the SciPy triangular-solve construction above.
        numpy_left_solved = np.linalg.solve(left_cholesky, cross_scaled)
        numpy_canonical = np.linalg.solve(
            right_cholesky, numpy_left_solved.T
        ).T
        numpy_singular = np.asarray(
            np.linalg.svd(numpy_canonical, compute_uv=False), dtype=float
        )
    except (np.linalg.LinAlgError, ValueError, FloatingPointError):
        return _high_precision_only_two_block_result(
            matrix,
            left,
            right,
            precision_condition_number=precision_condition_number,
            reason="binary64-linear-algebra",
            conditioning_triggered=conditioning_triggered,
        )
    if not np.isfinite(scipy_singular).all() or not np.isfinite(numpy_singular).all():
        return _high_precision_only_two_block_result(
            matrix,
            left,
            right,
            precision_condition_number=precision_condition_number,
            reason="binary64-svd",
            conditioning_triggered=conditioning_triggered,
        )
    scipy_squared = scipy_singular * scipy_singular
    numpy_squared = numpy_singular * numpy_singular
    raw_max_squared = max(
        float(np.max(scipy_squared, initial=0.0)),
        float(np.max(numpy_squared, initial=0.0)),
    )
    boundary_acceptance_limit = float(
        64.0 * matrix.shape[0] * np.finfo(float).eps
    )
    first_scale = max(
        float(np.linalg.norm(first_scaled, ord=np.inf)), np.finfo(float).tiny
    )
    second_scale = max(
        float(np.linalg.norm(second_scaled, ord=np.inf)), np.finfo(float).tiny
    )
    left_cholesky_residual = _finite_diagnostic_or_none(
        np.linalg.norm(
            first_scaled - left_cholesky @ left_cholesky.T, ord=np.inf
        )
        / first_scale
    )
    right_cholesky_residual = _finite_diagnostic_or_none(
        np.linalg.norm(
            second_scaled - right_cholesky @ right_cholesky.T,
            ord=np.inf,
        )
        / second_scale
    )
    cholesky_residual = (
        max(left_cholesky_residual, right_cholesky_residual)
        if left_cholesky_residual is not None
        and right_cholesky_residual is not None
        else None
    )
    raw_solve_scale = (
        float(np.linalg.norm(left_cholesky, ord=np.inf))
        * float(np.linalg.norm(canonical, ord=np.inf))
        * float(np.linalg.norm(right_cholesky.T, ord=np.inf))
        + float(np.linalg.norm(cross_scaled, ord=np.inf))
    )
    solve_scale = (
        max(raw_solve_scale, np.finfo(float).tiny)
        if math.isfinite(raw_solve_scale)
        else None
    )
    raw_solve_residual = (
        np.linalg.norm(
            left_cholesky @ canonical @ right_cholesky.T - cross_scaled,
            ord=np.inf,
        )
        / solve_scale
        if solve_scale is not None
        else None
    )
    solve_residual = _finite_diagnostic_or_none(raw_solve_residual)
    unit_roundoff = np.finfo(float).eps / 2.0
    gamma_n = matrix.shape[0] * unit_roundoff / (
        1.0 - matrix.shape[0] * unit_roundoff
    )
    residual_tolerance = _finite_diagnostic_or_none(64.0 * gamma_n)
    backward_error = (
        _finite_diagnostic_or_none(
            math.nextafter(max(cholesky_residual, solve_residual), math.inf)
        )
        if cholesky_residual is not None and solve_residual is not None
        else None
    )
    nonfinite_residual_causes = tuple(
        name
        for name, diagnostic in (
            ("cholesky", cholesky_residual),
            ("solve", solve_residual),
            ("tolerance", residual_tolerance),
        )
        if diagnostic is None
    )
    if nonfinite_residual_causes:
        # Fixed field order retains every unusable cause deterministically.
        residual_health_reason = (
            "binary64-residual-health-nonfinite-"
            + "-and-".join(nonfinite_residual_causes)
        )
    else:
        residual_health_reason = "binary64-residual-health"
    if nonfinite_residual_causes or (
        cholesky_residual > residual_tolerance
        or solve_residual > residual_tolerance
    ):
        return _high_precision_only_two_block_result(
            matrix,
            left,
            right,
            precision_condition_number=precision_condition_number,
            reason=residual_health_reason,
            conditioning_triggered=conditioning_triggered,
            cholesky_residual=cholesky_residual,
            solve_residual=solve_residual,
            residual_tolerance=residual_tolerance,
            backward_error=backward_error,
        )

    raw_margin = 1.0 - raw_max_squared
    boundary_fallback = bool(raw_margin <= boundary_acceptance_limit)
    high_precision_fallback = boundary_fallback or (
        conditioning_triggered and not exact_block_diagonal
    )
    clipping_amount = max(0.0, raw_max_squared - 1.0)
    clipping_applied = clipping_amount > 0.0
    residual_derived_clip_bound = 0.0
    if boundary_fallback:
        high_precision_gap, exact_squared = _high_precision_two_block(
            matrix, left, right, digits=200
        )
        fallback_digits = _adaptive_mp_digits(matrix, minimum=220)
        with mpmath.workdps(fallback_digits):
            exact_max_squared = (
                exact_squared[0] if exact_squared else mpmath.mpf("0")
            )
            raw_max_exact = _mp_exact_float(raw_max_squared)
            evaluation_discrepancy = abs(raw_max_exact - exact_max_squared)
            residual_derived_clip_bound = _outward_float_upper(
                evaluation_discrepancy, digits=fallback_digits
            )
            if clipping_applied and evaluation_discrepancy > _mp_exact_float(
                boundary_acceptance_limit
            ):
                raise ValueError(
                    "binary64 canonical-correlation discrepancy exceeds the operational boundary guard"
                )
            min_one_minus = _positive_mp_to_float(
                mpmath.mpf(1) - exact_max_squared
            )
        if clipping_applied and clipping_amount > residual_derived_clip_bound:
            raise ValueError(
                "binary64 canonical-correlation excursion exceeds its exact-input allowance"
            )
        value = float(high_precision_gap)
        evaluation_method = "exact-binary64-mpmath-200d-boundary-fallback"
    elif exact_block_diagonal:
        value = 0.0
        min_one_minus = 1.0
        evaluation_method = "exact-zero-cross-block-control"
    elif conditioning_triggered:
        high_precision_gap, exact_squared = _high_precision_two_block(
            matrix, left, right, digits=200
        )
        value = float(high_precision_gap)
        with mpmath.workdps(_adaptive_mp_digits(matrix, minimum=220)):
            exact_max_squared = (
                exact_squared[0] if exact_squared else mpmath.mpf("0")
            )
            min_one_minus = _positive_mp_to_float(
                mpmath.mpf(1) - exact_max_squared
            )
        evaluation_method = "exact-binary64-mpmath-200d-conditioning-fallback"
    else:
        if raw_max_squared >= 1.0:
            raise ValueError("canonical correlation lies outside the log1p domain")
        value = -0.5 * math.fsum(math.log1p(-float(square)) for square in scipy_squared)
        min_one_minus = float(np.min(1.0 - scipy_squared, initial=1.0))
        evaluation_method = "scipy-cholesky-triangular-solve-svd-log1p"
    if not math.isfinite(value) or value < 0.0 or min_one_minus <= 0.0:
        raise ValueError("factorization gap evaluation left its finite positive domain")

    step = GapStep(
        value=value,
        left_block=left,
        right_block=right,
        singular_values=tuple(float(value) for value in scipy_singular),
        scipy_singular_values=tuple(float(value) for value in scipy_singular),
        numpy_singular_values=tuple(float(value) for value in numpy_singular),
        min_one_minus_rho_squared=min_one_minus,
        cholesky_residual=cholesky_residual,
        solve_residual=solve_residual,
        residual_tolerance=residual_tolerance,
        backward_error=backward_error,
        clipping_applied=clipping_applied,
        clipping_amount=clipping_amount,
        residual_derived_clip_bound=residual_derived_clip_bound,
        boundary_fallback_applied=boundary_fallback,
        high_precision_fallback_applied=high_precision_fallback,
        conditioning_triggered=conditioning_triggered,
        precision_condition_number=precision_condition_number,
        boundary_acceptance_limit=boundary_acceptance_limit,
        evaluation_method=evaluation_method,
    )
    return _step_result(step)


def factorization_gap(lam: np.ndarray, blocks: Any) -> GapResult:
    """Telescope stable two-block increments along the declared block order."""

    matrix, _, _ = _validated_precision(lam)
    partition = validate_partition(matrix, blocks)
    if len(partition) == 1:
        return GapResult(
            value=0.0,
            steps=(),
            merge_order=(),
            backward_error_bound=0.0,
            singular_values=(),
            min_one_minus_rho_squared=1.0,
            maximum_cholesky_residual=0.0,
            clipping_applied=False,
            clipping_amount=0.0,
            residual_derived_clip_bound=0.0,
            boundary_fallback_applied=False,
            high_precision_fallback_applied=False,
            conditioning_triggered=False,
        )

    merged = partition[0]
    steps: list[GapStep] = []
    merge_order: list[
        tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]
    ] = []
    for current in partition[1:]:
        combined = merged + current
        submatrix = matrix[np.ix_(combined, combined)]
        local_left = tuple(range(len(merged)))
        local_right = tuple(range(len(merged), len(combined)))
        local = two_block_factorization_gap(submatrix, local_left, local_right)
        step = local.steps[0]._replace(left_block=merged, right_block=current)
        steps.append(step)
        merge_order.append((merged, current, combined))
        merged = combined

    total = math.fsum(step.value for step in steps)
    backward_error_bound = (
        None
        if any(step.backward_error is None for step in steps)
        else math.fsum(step.backward_error for step in steps)
    )
    maximum_cholesky_residual = (
        None
        if any(step.cholesky_residual is None for step in steps)
        else max(step.cholesky_residual for step in steps)
    )
    return GapResult(
        value=total,
        steps=tuple(steps),
        merge_order=tuple(merge_order),
        backward_error_bound=backward_error_bound,
        singular_values=tuple(step.singular_values for step in steps),
        min_one_minus_rho_squared=min(
            step.min_one_minus_rho_squared for step in steps
        ),
        maximum_cholesky_residual=maximum_cholesky_residual,
        clipping_applied=any(step.clipping_applied for step in steps),
        clipping_amount=max(step.clipping_amount for step in steps),
        residual_derived_clip_bound=max(
            step.residual_derived_clip_bound for step in steps
        ),
        boundary_fallback_applied=any(
            step.boundary_fallback_applied for step in steps
        ),
        high_precision_fallback_applied=any(
            step.high_precision_fallback_applied for step in steps
        ),
        conditioning_triggered=any(step.conditioning_triggered for step in steps),
    )


def _factorization_case_seed(
    case_id: str, dimension: int, condition_number: float, stratum: str, *, seed: int
) -> int:
    material = (
        f"{seed}|{case_id}|{dimension}|{condition_number:.17g}|{stratum}".encode()
    )
    return int.from_bytes(hashlib.sha256(material).digest()[:8], "big", signed=False)


def _factorization_partition(
    dimension: int, stratum: str
) -> tuple[tuple[int, ...], ...]:
    if stratum == "nested_refinement" and dimension >= 3:
        cut = max(1, dimension // 3)
        return (
            tuple(range(cut)),
            tuple(range(cut, 2 * cut)),
            tuple(range(2 * cut, dimension)),
        )
    cut = dimension // 2
    return (tuple(range(cut)), tuple(range(cut, dimension)))


def _default_factorization_schedule(
    seed: int,
) -> tuple[FactorizationProtocolCase, ...]:
    cases: list[FactorizationProtocolCase] = []
    for dimension in range(2, 17):
        for condition_number in FACTORIZATION_PROTOCOL_CONDITIONS:
            for replica in range(20):
                case_id = (
                    f"general-d{dimension}-c{condition_number:.0e}-r{replica:02d}"
                )
                stratum = "general"
                cases.append(
                    FactorizationProtocolCase(
                        case_id=case_id,
                        stratum=stratum,
                        dimension=dimension,
                        condition_number=condition_number,
                        replica=replica,
                        matrix_seed=_factorization_case_seed(
                            case_id,
                            dimension,
                            condition_number,
                            stratum,
                            seed=seed,
                        ),
                        partition=_factorization_partition(dimension, stratum),
                    )
                )
    for stratum, count in FACTORIZATION_PROTOCOL_STRATUM_COUNTS.items():
        if stratum == "general":
            continue
        for replica in range(count):
            dimension = 2 + replica % 15
            condition_number = FACTORIZATION_PROTOCOL_CONDITIONS[
                replica % len(FACTORIZATION_PROTOCOL_CONDITIONS)
            ]
            case_id = f"{stratum}-{replica:03d}"
            cases.append(
                FactorizationProtocolCase(
                    case_id=case_id,
                    stratum=stratum,
                    dimension=dimension,
                    condition_number=condition_number,
                    replica=replica,
                    matrix_seed=_factorization_case_seed(
                        case_id,
                        dimension,
                        condition_number,
                        stratum,
                        seed=seed,
                    ),
                    partition=_factorization_partition(dimension, stratum),
                )
            )
    if len(cases) != 3138:
        raise RuntimeError("factorization protocol schedule is not exactly 3,138 cases")
    return tuple(cases)


def _regenerate_factorization_case(
    case: Any, *, seed: int
) -> tuple[np.ndarray, tuple[tuple[int, ...], ...]]:
    expected_seed = _factorization_case_seed(
        case.case_id,
        int(case.dimension),
        float(case.condition_number),
        case.stratum,
        seed=seed,
    )
    if int(case.matrix_seed) != expected_seed:
        raise ValueError(f"factorization protocol seed mismatch for {case.case_id}")
    rng = np.random.default_rng(expected_seed)
    dimension = int(case.dimension)
    condition_number = float(case.condition_number)
    spectrum = np.geomspace(1.0, 1.0 / condition_number, dimension)
    partition = _factorization_partition(dimension, case.stratum)
    if tuple(tuple(int(index) for index in block) for block in case.partition) != partition:
        raise ValueError(f"factorization protocol partition mismatch for {case.case_id}")
    if case.stratum == "exact_block_diagonal":
        generated_blocks = []
        for indices in partition:
            orthogonal, _ = np.linalg.qr(
                rng.standard_normal((len(indices), len(indices)))
            )
            generated_blocks.append(
                orthogonal
                @ np.diag(
                    np.geomspace(1.0, 1.0 / condition_number, len(indices))
                )
                @ orthogonal.T
            )
        matrix = np.zeros((dimension, dimension))
        offset = 0
        for block in generated_blocks:
            size = block.shape[0]
            matrix[offset : offset + size, offset : offset + size] = block
            offset += size
    else:
        orthogonal, _ = np.linalg.qr(rng.standard_normal((dimension, dimension)))
        matrix = orthogonal @ np.diag(spectrum) @ orthogonal.T
        if case.stratum == "near_decoupled":
            block_diagonal = np.zeros_like(matrix)
            for indices in partition:
                block_diagonal[np.ix_(indices, indices)] = matrix[
                    np.ix_(indices, indices)
                ]
            matrix = (
                0.999 * block_diagonal
                + 0.001 * matrix
                + np.eye(dimension) * 1.0e-12
            )
        elif case.stratum == "scale":
            matrix *= 10.0 ** ((int(case.replica) % 7) - 3)
        elif case.stratum == "permutation":
            permutation = rng.permutation(dimension)
            matrix = matrix[np.ix_(permutation, permutation)]
            inverse_permutation = np.argsort(permutation)
            partition = tuple(
                tuple(
                    sorted(
                        int(index) for index in inverse_permutation[list(indices)]
                    )
                )
                for indices in partition
            )
    matrix = (matrix + matrix.T) / 2.0
    np.linalg.cholesky(matrix)
    return matrix, partition


def _factorization_matrix_digest(matrix: np.ndarray) -> str:
    return hashlib.sha256(
        np.ascontiguousarray(matrix, dtype=np.float64).tobytes()
    ).hexdigest()


def _factorization_partition_digest(
    partition: tuple[tuple[int, ...], ...]
) -> str:
    normalized = tuple(
        tuple(int(index) for index in block) for block in partition
    )
    return hashlib.sha256(
        json.dumps(normalized, separators=(",", ":")).encode()
    ).hexdigest()


def _factorization_schedule_payload(cases: Any) -> list[dict[str, Any]]:
    fields = (
        "case_id",
        "stratum",
        "dimension",
        "condition_number",
        "replica",
        "matrix_seed",
        "partition",
    )
    return [
        asdict(case)
        if is_dataclass(case)
        else {name: getattr(case, name) for name in fields}
        for case in cases
    ]


def run_factorization_gap_protocol(
    *, seed: int = FACTORIZATION_PROTOCOL_SEED, schedule: Any = None
) -> FactorizationProtocolReport:
    """Run the frozen, case-bound 3,138-case factorization-gap protocol."""

    if seed != FACTORIZATION_PROTOCOL_SEED:
        raise ValueError(
            f"factorization protocol seed must be {FACTORIZATION_PROTOCOL_SEED}"
        )
    cases = (
        tuple(schedule)
        if schedule is not None
        else _default_factorization_schedule(seed)
    )
    if len(cases) != 3138:
        raise ValueError("factorization protocol requires exactly 3,138 cases")
    case_ids = [case.case_id for case in cases]
    if len(set(case_ids)) != len(case_ids):
        raise ValueError("factorization protocol case identities must be unique")
    stratum_counts = {
        name: sum(case.stratum == name for case in cases)
        for name in FACTORIZATION_PROTOCOL_STRATUM_COUNTS
    }
    if stratum_counts != FACTORIZATION_PROTOCOL_STRATUM_COUNTS:
        raise ValueError(
            "factorization protocol stratum counts do not match the frozen schedule"
        )
    for stratum in FACTORIZATION_PROTOCOL_STRATUM_COUNTS:
        stratum_cases = [case for case in cases if case.stratum == stratum]
        if {int(case.dimension) for case in stratum_cases} != set(range(2, 17)):
            raise ValueError(
                f"factorization protocol stratum {stratum} omits a dimension"
            )
        if {
            float(case.condition_number) for case in stratum_cases
        } != set(FACTORIZATION_PROTOCOL_CONDITIONS):
            raise ValueError(
                f"factorization protocol stratum {stratum} omits a condition tier"
            )
    schedule_payload = _factorization_schedule_payload(cases)
    frozen_schedule_payload = _factorization_schedule_payload(
        _default_factorization_schedule(seed)
    )
    if schedule_payload != frozen_schedule_payload:
        raise ValueError(
            "factorization protocol schedule differs from the frozen case-bound schedule"
        )
    schedule_digest = hashlib.sha256(
        json.dumps(schedule_payload, sort_keys=True).encode()
    ).hexdigest()

    records: list[FactorizationCaseRecord] = []
    controls: list[FactorizationHighPrecisionControl] = []
    case_failures: list[dict[str, Any]] = []
    for case in cases:
        matrix = None
        partition = None
        try:
            matrix, partition = _regenerate_factorization_case(case, seed=seed)
            achieved_condition_number = float(np.linalg.cond(matrix))
            if not math.isfinite(achieved_condition_number):
                raise ValueError(
                    "digest-bound achieved condition number is nonfinite"
                )
            gap = factorization_gap(matrix, partition)
            records.append(
                FactorizationCaseRecord(
                    case_id=case.case_id,
                    stratum=case.stratum,
                    dimension=int(case.dimension),
                    condition_number=float(case.condition_number),
                    achieved_condition_number=achieved_condition_number,
                    matrix_digest=_factorization_matrix_digest(matrix),
                    partition_digest=_factorization_partition_digest(partition),
                    value=gap.value,
                    backward_error_bound=gap.backward_error_bound,
                    maximum_cholesky_residual=gap.maximum_cholesky_residual,
                    evaluation_methods=tuple(
                        step.evaluation_method for step in gap.steps
                    ),
                    clipping_applied=gap.clipping_applied,
                    boundary_fallback_applied=gap.boundary_fallback_applied,
                    high_precision_fallback_applied=gap.high_precision_fallback_applied,
                )
            )
            if case.stratum == "mpmath_100_digit":
                with mpmath.workdps(100):
                    reference = _high_precision_partition_gap(
                        matrix, partition, digits=100
                    )
                    reference_text = mpmath.nstr(reference, n=100)
                controls.append(
                    FactorizationHighPrecisionControl(
                        case_id=case.case_id,
                        decimal_digits=100,
                        reference_value=reference_text,
                    )
                )
        except Exception as exc:
            case_failures.append(
                {
                    "case_id": case.case_id,
                    "stratum": case.stratum,
                    "dimension": int(case.dimension),
                    "nominal_condition_number": float(case.condition_number),
                    "matrix_digest": (
                        _factorization_matrix_digest(matrix)
                        if matrix is not None
                        else None
                    ),
                    "partition_digest": (
                        _factorization_partition_digest(partition)
                        if partition is not None
                        else None
                    ),
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                }
            )
    return FactorizationProtocolReport(
        protocol_name="new-deterministic-factorization-gap-3138",
        seed=seed,
        schedule_digest=schedule_digest,
        historical_generator_recovered=False,
        cases=tuple(records),
        high_precision_controls=tuple(controls),
        case_failures=tuple(case_failures),
    )


def check_cg_factor_gap() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    n = 8
    lam = random_spd(rng, n, 1.0)
    target_mean = rng.standard_normal(n)
    target_covariance = np.linalg.inv(lam)
    fine_blocks = [[0, 1], [2, 3], [4, 5], [6, 7]]

    optimum_blocks = [
        np.linalg.inv(lam[np.ix_(block, block)]) for block in fine_blocks
    ]
    optimum_covariance = sla.block_diag(*optimum_blocks)
    analytic_gap_result = factorization_gap(lam, fine_blocks)
    analytic_gap = analytic_gap_result.value
    analytic_gap_reference = float(
        _high_precision_partition_gap(
            lam,
            tuple(tuple(block) for block in fine_blocks),
            digits=200,
        )
    )
    direct_optimum_kl = gaussian_kl(
        target_mean,
        optimum_covariance,
        target_mean,
        target_covariance,
    )
    optimum_residual = abs(analytic_gap - direct_optimum_kl)
    analytic_gap_reference_error = abs(analytic_gap - analytic_gap_reference)
    direct_kl_reference_error = abs(direct_optimum_kl - analytic_gap_reference)
    analytic_gap_endpoint_tolerance = _roundoff_scale(
        analytic_gap, analytic_gap_reference, dimension=n, multiplier=512.0
    )
    direct_kl_endpoint_tolerance = _roundoff_scale(
        direct_optimum_kl,
        analytic_gap_reference,
        dimension=n,
        multiplier=1024.0,
    )
    optimum_tolerance = (
        analytic_gap_endpoint_tolerance + direct_kl_endpoint_tolerance
    )

    perturbation_draws = 5000
    perturbation_deltas: list[float] = []
    perturbation_tolerances: list[float] = []
    for _ in range(perturbation_draws):
        perturbed_blocks = []
        for optimum_block in optimum_blocks:
            symmetric = rng.standard_normal(optimum_block.shape)
            symmetric = (symmetric + symmetric.T) / 2.0
            symmetric /= max(float(np.linalg.norm(symmetric, ord="fro")), 1.0)
            amplitude = float(rng.uniform(0.05, 0.25))
            chol = np.linalg.cholesky(optimum_block)
            perturbed_blocks.append(
                chol @ sla.expm(amplitude * symmetric) @ chol.T
            )
        perturbed_covariance = sla.block_diag(*perturbed_blocks)
        perturbed_kl = gaussian_kl(
            target_mean,
            perturbed_covariance,
            target_mean,
            target_covariance,
        )
        perturbation_deltas.append(perturbed_kl - analytic_gap_reference)
        perturbation_tolerances.append(
            _roundoff_scale(
                perturbed_kl,
                analytic_gap_reference,
                dimension=n,
                multiplier=1024.0,
            )
        )
    improving_perturbations = sum(
        delta < -tolerance
        for delta, tolerance in zip(perturbation_deltas, perturbation_tolerances)
    )

    partitions = [
        [[0], [1], [2], [3], [4], [5], [6], [7]],
        [[0, 1], [2], [3], [4], [5], [6], [7]],
        [[0, 1], [2, 3], [4], [5], [6], [7]],
        [[0, 1, 2, 3], [4], [5], [6], [7]],
        [[0, 1, 2, 3], [4, 5], [6, 7]],
        [list(range(n))],
    ]
    gap_results = [factorization_gap(lam, partition) for partition in partitions]
    gaps = [gap.value for gap in gap_results]
    gap_references = [
        float(
            _high_precision_partition_gap(
                lam,
                tuple(tuple(block) for block in partition),
                digits=200,
            )
        )
        for partition in partitions
    ]
    gap_reference_errors = [
        abs(gap.value - reference)
        for gap, reference in zip(gap_results, gap_references)
    ]
    gap_reference_tolerances = [
        _roundoff_scale(
            gap.value, reference, dimension=n, multiplier=512.0
        )
        for gap, reference in zip(gap_results, gap_references)
    ]
    monotonicity_tolerances = [
        left_tolerance + right_tolerance
        for left_tolerance, right_tolerance in zip(
            gap_reference_tolerances, gap_reference_tolerances[1:]
        )
    ]
    high_precision_monotone = all(
        left >= right
        for left, right in zip(gap_references, gap_references[1:])
    )
    binary64_monotone = all(
        left.value + tolerance >= right.value
        for left, right, tolerance in zip(
            gap_results, gap_results[1:], monotonicity_tolerances
        )
    )
    monotone = (
        high_precision_monotone
        and binary64_monotone
        and all(
            error <= tolerance
            for error, tolerance in zip(
                gap_reference_errors, gap_reference_tolerances
            )
        )
    )
    single_block_tolerance = gap_reference_tolerances[-1]

    scales = [1.0, 10.0, 100.0]
    scaled_gap_results = [factorization_gap(c * lam, fine_blocks) for c in scales]
    scaled_gaps = [gap.value for gap in scaled_gap_results]
    scaled_gap_references = [
        float(
            _high_precision_partition_gap(
                c * lam,
                tuple(tuple(block) for block in fine_blocks),
                digits=200,
            )
        )
        for c in scales
    ]
    scaled_gap_reference_errors = [
        abs(gap.value - reference)
        for gap, reference in zip(scaled_gap_results, scaled_gap_references)
    ]
    scaled_gap_endpoint_tolerances = [
        _roundoff_scale(
            gap.value, reference, dimension=n, multiplier=512.0
        )
        for gap, reference in zip(scaled_gap_results, scaled_gap_references)
    ]
    scale_spread = max(scaled_gaps) - min(scaled_gaps)
    scale_reference_spread = max(scaled_gap_references) - min(
        scaled_gap_references
    )
    scale_reference_roundoff_tolerance = _roundoff_scale(
        *scaled_gap_references, dimension=n, multiplier=1024.0
    )
    scale_tolerance = (
        scale_reference_roundoff_tolerance
        + 2.0 * max(scaled_gap_endpoint_tolerances)
    )

    q, _ = np.linalg.qr(rng.standard_normal((n, n)))
    retained_dimension = 4
    b = q[:, :retained_dimension]
    b_perp = q[:, retained_dimension:]
    mu_perp = b_perp.T @ target_mean
    mean_tie_costs = {}
    volume_terms = {}
    for c in scales:
        scaled_lam = c * lam
        marginal_precision = np.linalg.inv(
            b_perp.T @ np.linalg.inv(scaled_lam) @ b_perp
        )
        mean_tie_costs[str(c)] = 0.5 * float(
            mu_perp @ marginal_precision @ mu_perp
        )
        volume_terms[str(c)] = 0.5 * float(
            np.linalg.slogdet(
                b_perp.T @ np.linalg.inv(scaled_lam) @ b_perp
            )[1]
        )
    base_mean_tie = mean_tie_costs["1.0"]
    base_volume = volume_terms["1.0"]
    mean_tie_errors = {
        str(c): abs(mean_tie_costs[str(c)] - c * base_mean_tie)
        for c in scales
    }
    mean_tie_tolerances = {
        str(c): _roundoff_scale(
            mean_tie_costs[str(c)], c * base_mean_tie, dimension=n, multiplier=256.0
        )
        for c in scales
    }
    m = n - retained_dimension
    volume_shift_errors = {
        str(c): abs(
            (volume_terms[str(c)] - base_volume) + 0.5 * m * math.log(c)
        )
        for c in scales
    }
    volume_shift_tolerances = {
        str(c): _roundoff_scale(
            volume_terms[str(c)] - base_volume,
            -0.5 * m * math.log(c),
            dimension=n,
            multiplier=256.0,
        )
        for c in scales
    }
    numerical_outputs_finite = all(
        math.isfinite(value)
        for value in (
            analytic_gap,
            direct_optimum_kl,
            analytic_gap_reference,
            analytic_gap_reference_error,
            direct_kl_reference_error,
            optimum_residual,
            *perturbation_deltas,
            *perturbation_tolerances,
            *gaps,
            *gap_references,
            *gap_reference_errors,
            *gap_reference_tolerances,
            *monotonicity_tolerances,
            *scaled_gaps,
            *scaled_gap_references,
            *scaled_gap_reference_errors,
            *scaled_gap_endpoint_tolerances,
            scale_spread,
            scale_reference_spread,
            scale_reference_roundoff_tolerance,
            scale_tolerance,
            *mean_tie_costs.values(),
            *mean_tie_errors.values(),
            *mean_tie_tolerances.values(),
            *volume_terms.values(),
            *volume_shift_errors.values(),
            *volume_shift_tolerances.values(),
        )
    )
    passed = (
        numerical_outputs_finite
        and analytic_gap_reference_error <= analytic_gap_endpoint_tolerance
        and direct_kl_reference_error <= direct_kl_endpoint_tolerance
        and optimum_residual <= optimum_tolerance
        and improving_perturbations == 0
        and monotone
        and abs(gaps[-1]) <= single_block_tolerance
        and all(
            error <= tolerance
            for error, tolerance in zip(
                scaled_gap_reference_errors, scaled_gap_endpoint_tolerances
            )
        )
        and scale_reference_spread <= scale_reference_roundoff_tolerance
        and scale_spread <= scale_tolerance
        and all(
            mean_tie_errors[key] <= mean_tie_tolerances[key]
            for key in mean_tie_errors
        )
        and all(
            volume_shift_errors[key] <= volume_shift_tolerances[key]
            for key in volume_shift_errors
        )
    )
    return result(
        "CHK-CG-FACTOR-GAP",
        "Gaussian factorization optimum, perturbation control, monotonicity, and scale laws",
        ["NUM-CG-FACTOR-GAP", "NUM-CG-GAP-MONOTONE", "NUM-CG-SCALE"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count={
            "analytic_optimum_instances": 1,
            "seeded_symmetric_block_perturbations": perturbation_draws,
            "nested_partitions": len(partitions),
            "scale_values": scales,
        },
        expected={
            "direct_KL_at_analytic_optimum": "closed-form factorization gap",
            "perturbations_improving_beyond_tolerance": 0,
            "nested_gap_nonincreasing": True,
            "single_block_gap": 0,
            "factor_gap_scale_invariance": True,
            "mean_tie_cost": "linear in c",
            "volume_shift": "-(m/2) log c",
        },
        tolerances={
            "policy": "independent 200-digit exact-binary64 references with separately declared endpoint-roundoff allowances; backward residuals are health diagnostics only",
            "analytic_gap_endpoint_roundoff": analytic_gap_endpoint_tolerance,
            "direct_KL_endpoint_roundoff": direct_kl_endpoint_tolerance,
            "analytic_optimum_cross_endpoint": optimum_tolerance,
            "perturbation_improvement_range": [
                min(perturbation_tolerances),
                max(perturbation_tolerances),
            ],
            "monotonicity_pairwise": monotonicity_tolerances,
            "single_block": single_block_tolerance,
            "scale_exact_input_reference_roundoff": scale_reference_roundoff_tolerance,
            "scale_production_endpoint_roundoff": scaled_gap_endpoint_tolerances,
            "scale_identity": scale_tolerance,
            "mean_tie_identity": mean_tie_tolerances,
            "volume_shift_identity": volume_shift_tolerances,
        },
        observed={
            "all_numerical_outputs_finite": numerical_outputs_finite,
            "analytic_optimum": {
                "closed_form_gap": analytic_gap,
                "direct_KL": direct_optimum_kl,
                "exact_binary64_reference_200d": analytic_gap_reference,
                "gap_reference_absolute_error": analytic_gap_reference_error,
                "direct_KL_reference_absolute_error": direct_kl_reference_error,
                "absolute_residual": optimum_residual,
                "gap_backward_error_bound": analytic_gap_result.backward_error_bound,
            },
            "perturbation_control": {
                "draws": perturbation_draws,
                "improving_beyond_tolerance": improving_perturbations,
                "minimum_KL_minus_optimum": min(perturbation_deltas),
                "median_KL_minus_optimum": float(np.median(perturbation_deltas)),
            },
            "monotonicity": {
                "nested_partition_gaps": gaps,
                "exact_binary64_references_200d": gap_references,
                "reference_absolute_errors": gap_reference_errors,
                "nonincreasing": monotone,
                "high_precision_reference_nonincreasing": high_precision_monotone,
                "binary64_nonincreasing_with_endpoint_allowance": binary64_monotone,
                "single_block_gap": gaps[-1],
                "gap_backward_error_bounds": [
                    gap.backward_error_bound for gap in gap_results
                ],
            },
            "scale": {
                "factorization_gaps": dict(zip(map(str, scales), scaled_gaps)),
                "exact_binary64_references_200d": dict(
                    zip(map(str, scales), scaled_gap_references)
                ),
                "production_reference_absolute_errors": dict(
                    zip(map(str, scales), scaled_gap_reference_errors)
                ),
                "factorization_gap_spread": scale_spread,
                "exact_input_reference_spread": scale_reference_spread,
                "factorization_gap_backward_error_bounds": dict(
                    zip(
                        map(str, scales),
                        (gap.backward_error_bound for gap in scaled_gap_results),
                    )
                ),
                "mean_tie_costs": mean_tie_costs,
                "mean_tie_linear_scaling_errors": mean_tie_errors,
                "volume_terms": volume_terms,
                "volume_shift_errors": volume_shift_errors,
                "transverse_dimension_m": m,
            },
        },
        interpretation="The KL optimum is evaluated independently from the determinant formula. Seeded SPD-preserving block perturbations are a control, while universal monotonicity and scaling remain algebraic statements proved in the manuscript.",
    )


def check_cg_factor_gap_stress() -> dict[str, Any]:
    schedule = _default_factorization_schedule(FACTORIZATION_PROTOCOL_SEED)
    protocol = run_factorization_gap_protocol(schedule=schedule)
    records = protocol.cases
    by_id = {record.case_id: record for record in records}
    controls = {control.case_id: control for control in protocol.high_precision_controls}
    protocol_case_failures = list(protocol.case_failures)

    all_case_oracle_failures: list[dict[str, Any]] = []
    all_case_oracle_attempts = 0
    all_case_reference_evaluations = 0
    all_case_oracle_cases = 0
    all_case_oracle_errors: list[float] = []
    all_case_oracle_tolerances: list[float] = []
    for case in schedule:
        all_case_oracle_attempts += 1
        matrix = None
        partition = None
        try:
            matrix, partition = _regenerate_factorization_case(
                case, seed=protocol.seed
            )
            reference_mp = _high_precision_partition_gap(
                matrix, partition, digits=100
            )
            if not mpmath.isfinite(reference_mp):
                raise ValueError("100-digit exact-input reference is nonfinite")
            all_case_reference_evaluations += 1
            record = by_id.get(case.case_id)
            if record is None:
                raise ValueError("production record is missing")
            reference = float(reference_mp)
            error = abs(record.value - reference)
            tolerance = max(
                _roundoff_scale(
                    record.value,
                    reference,
                    dimension=record.dimension,
                    multiplier=512.0,
                ),
                1.0e-4 * abs(reference),
                2.0e-8,
            )
            all_case_oracle_errors.append(error)
            all_case_oracle_tolerances.append(tolerance)
            all_case_oracle_cases += 1
            if (
                not math.isfinite(record.value)
                or not math.isfinite(reference)
                or error > tolerance
            ):
                all_case_oracle_failures.append(
                    {
                        "case_id": case.case_id,
                        "stratum": case.stratum,
                        "dimension": int(case.dimension),
                        "nominal_condition_number": float(
                            case.condition_number
                        ),
                        "achieved_condition_number": record.achieved_condition_number,
                        "matrix_digest": record.matrix_digest,
                        "partition_digest": record.partition_digest,
                        "production_value": record.value,
                        "reference_value_100d": mpmath.nstr(reference_mp, n=100),
                        "absolute_error": error,
                        "declared_acceptance": tolerance,
                        "disposition": "FAIL",
                    }
                )
        except Exception as exc:
            all_case_oracle_failures.append(
                {
                    "case_id": case.case_id,
                    "stratum": case.stratum,
                    "dimension": int(case.dimension),
                    "nominal_condition_number": float(case.condition_number),
                    "matrix_digest": (
                        _factorization_matrix_digest(matrix)
                        if matrix is not None
                        else None
                    ),
                    "partition_digest": (
                        _factorization_partition_digest(partition)
                        if partition is not None
                        else None
                    ),
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                    "disposition": "ERROR",
                }
            )

    control_errors: dict[str, float] = {}
    control_tolerances: dict[str, float] = {}
    for case_id, control in controls.items():
        record = by_id[case_id]
        reference = float(control.reference_value)
        control_errors[case_id] = abs(record.value - reference)
        control_tolerances[case_id] = max(
            _roundoff_scale(
                record.value, reference, dimension=record.dimension, multiplier=256.0
            ),
            1.0e-4 * abs(reference),
            2.0e-8,
        )
    stratum_counts = {
        name: sum(record.stratum == name for record in records)
        for name in FACTORIZATION_PROTOCOL_STRATUM_COUNTS
    }
    achieved_condition_ranges = {
        name: {
            "minimum": min(
                record.achieved_condition_number
                for record in records
                if record.stratum == name
            ),
            "maximum": max(
                record.achieved_condition_number
                for record in records
                if record.stratum == name
            ),
        }
        for name in FACTORIZATION_PROTOCOL_STRATUM_COUNTS
        if any(record.stratum == name for record in records)
    }
    achieved_global_range = {
        "minimum": min(
            (record.achieved_condition_number for record in records),
            default=math.nan,
        ),
        "maximum": max(
            (record.achieved_condition_number for record in records),
            default=math.nan,
        ),
    }
    nominal_versus_achieved_controls = {
        case_id: {
            "nominal_condition_number": by_id[case_id].condition_number,
            "achieved_condition_number": by_id[case_id].achieved_condition_number,
        }
        for case_id in (
            "exact_block_diagonal-015",
            "near_decoupled-015",
        )
        if case_id in by_id
    }

    witness_matrix = np.asarray(FACTORIZATION_BOUNDARY_WITNESS, dtype=float)
    witness_partition = ((0, 1), (2, 3))
    try:
        witness_gap = factorization_gap(witness_matrix, witness_partition)
        witness_step = witness_gap.steps[0]
        witness_exact_value = float(
            _high_precision_partition_gap(
                witness_matrix, witness_partition, digits=200
            )
        )
        witness_digest = _factorization_matrix_digest(witness_matrix)
        witness_excursion = witness_step.clipping_amount
        witness_allowance = witness_step.residual_derived_clip_bound
        witness_passed = (
            witness_digest == FACTORIZATION_BOUNDARY_WITNESS_DIGEST
            and math.isclose(
                witness_exact_value,
                FACTORIZATION_BOUNDARY_WITNESS_GAP,
                rel_tol=0.0,
                abs_tol=math.ulp(FACTORIZATION_BOUNDARY_WITNESS_GAP),
            )
            and witness_excursion == FACTORIZATION_BOUNDARY_WITNESS_EXCURSION
            and witness_allowance == FACTORIZATION_BOUNDARY_WITNESS_ALLOWANCE
            and witness_step.clipping_applied
            and math.isclose(
                witness_gap.value,
                witness_exact_value,
                rel_tol=0.0,
                abs_tol=math.ulp(witness_exact_value),
            )
        )
        boundary_witness = {
            "matrix_digest": witness_digest,
            "exact_input_value": witness_exact_value,
            "rho_squared_excursion": witness_excursion,
            "outward_allowance": witness_allowance,
            "production_value": witness_gap.value,
            "clipping_diagnostic_applied": witness_step.clipping_applied,
            "evaluation_method": witness_step.evaluation_method,
            "status": "PASS" if witness_passed else "FAIL",
        }
    except Exception as exc:
        witness_passed = False
        boundary_witness = {
            "matrix_digest": _factorization_matrix_digest(witness_matrix),
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "status": "FAIL",
        }

    global_near_1e14 = math.isfinite(achieved_global_range["maximum"]) and math.isclose(
        achieved_global_range["maximum"], 1.0e14, rel_tol=2.0e-2
    )
    passed = (
        len(records) == 3138
        and stratum_counts == FACTORIZATION_PROTOCOL_STRATUM_COUNTS
        and len(controls) == 18
        and not protocol_case_failures
        and all_case_oracle_attempts == 3138
        and all_case_reference_evaluations == 3138
        and all_case_oracle_cases == 3138
        and not all_case_oracle_failures
        and witness_passed
        and global_near_1e14
        and all(math.isfinite(record.value) for record in records)
        and all(
            math.isfinite(record.achieved_condition_number)
            for record in records
        )
        and all(
            control_errors[case_id] <= control_tolerances[case_id]
            for case_id in controls
        )
    )
    case_payload_digest = hashlib.sha256(
        json.dumps(
            [record._asdict() for record in records],
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    return result(
        "CHK-CG-FACTOR-GAP-STRESS-3138",
        "Frozen stable Gaussian factorization-gap stress protocol",
        ["NUM-CG-FACTOR-GAP-BOUNDARY-PROTOCOL"],
        status="PASS" if passed else "FAIL",
        seed=protocol.seed,
        sample_count={
            "total_cases": len(records),
            "attempted_schedule_cases": len(schedule),
            "strata": stratum_counts,
            "mpmath_100_digit_controls": len(controls),
            "all_case_100_digit_references": all_case_reference_evaluations,
            "focused_positive_excursion_witnesses": 1,
        },
        expected={
            "protocol_name": "new-deterministic-factorization-gap-3138",
            "historical_generator_recovered": False,
            "all_values_finite": True,
            "all_3138_values_within_declared_100_digit_reference_acceptance": True,
            "all_high_precision_controls_within_declared_tolerance": True,
            "boundary_witness": {
                "matrix_digest": FACTORIZATION_BOUNDARY_WITNESS_DIGEST,
                "exact_input_value": FACTORIZATION_BOUNDARY_WITNESS_GAP,
                "rho_squared_excursion": FACTORIZATION_BOUNDARY_WITNESS_EXCURSION,
                "outward_allowance": FACTORIZATION_BOUNDARY_WITNESS_ALLOWANCE,
                "status": "PASS",
            },
            "achieved_condition_coverage_near_1e14": "global only",
        },
        tolerances={
            "matrix_value_comparison": "independent 100-digit exact-binary64 reference; max(endpoint-scaled binary64 roundoff, 1e-4 relative, 2e-8 absolute)",
            "backward_error_role": "health diagnostic only; excluded from every forward-value acceptance",
            "near_boundary_policy": "64*n*binary64 epsilon operational guard plus 200-digit exact-input evaluation; not a general perturbation theorem",
        },
        observed={
            "protocol_name": protocol.protocol_name,
            "historical_generator_recovered": protocol.historical_generator_recovered,
            "schedule_digest": protocol.schedule_digest,
            "case_payload_digest": case_payload_digest,
            "stratum_counts": stratum_counts,
            "nominal_condition_number_range": {
                "minimum": min(FACTORIZATION_PROTOCOL_CONDITIONS),
                "maximum": max(FACTORIZATION_PROTOCOL_CONDITIONS),
            },
            "achieved_condition_number_range_global": achieved_global_range,
            "achieved_condition_number_ranges_by_stratum": achieved_condition_ranges,
            "achieved_condition_coverage_near_1e14_global_only": global_near_1e14,
            "nominal_versus_achieved_controls": nominal_versus_achieved_controls,
            "finite_values": sum(math.isfinite(record.value) for record in records),
            "clipping_cases": sum(record.clipping_applied for record in records),
            "boundary_fallback_cases": sum(
                record.boundary_fallback_applied for record in records
            ),
            "high_precision_fallback_cases": sum(
                record.high_precision_fallback_applied for record in records
            ),
            "maximum_control_error": max(control_errors.values(), default=0.0),
            "maximum_control_tolerance": max(
                control_tolerances.values(), default=0.0
            ),
            "all_case_oracle_attempts": all_case_oracle_attempts,
            "all_case_reference_evaluations": all_case_reference_evaluations,
            "all_case_oracle_cases": all_case_oracle_cases,
            "all_case_oracle_failures": len(all_case_oracle_failures),
            "all_case_oracle_failure_details": all_case_oracle_failures,
            "maximum_all_case_oracle_error": max(
                all_case_oracle_errors, default=0.0
            ),
            "maximum_all_case_oracle_acceptance": max(
                all_case_oracle_tolerances, default=0.0
            ),
            "protocol_case_failures": protocol_case_failures,
            "boundary_witness": boundary_witness,
        },
        interpretation="This is a new frozen stress protocol, not a recovered historical experiment. Every one of the 3,138 schedule cases is compared with its own 100-digit exact-input reference; the 18 designated controls remain a named stratum. The separate 4-by-4 positive-excursion fixture binds the declared boundary policy but was not produced by the ordinary 3,138-case schedule.",
    )


def check_cg_frame_cancellation() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    k = 3
    u = random_gl_plus(rng, k)
    mu = rng.standard_normal(k)
    sigma = random_spd(rng, k)
    g = random_gl_plus(rng, k)
    bar_mu = np.linalg.solve(u, mu)
    bar_sigma = np.linalg.solve(u, sigma) @ np.linalg.inv(u).T
    u2, mu2, sigma2 = g @ u, g @ mu, g @ sigma @ g.T
    bar_mu2 = np.linalg.solve(u2, mu2)
    bar_sigma2 = np.linalg.solve(u2, sigma2) @ np.linalg.inv(u2).T
    mean_error = float(np.linalg.norm(bar_mu2 - bar_mu))
    covariance_error = float(np.linalg.norm(bar_sigma2 - bar_sigma, ord="fro"))
    passed = mean_error <= 1.0e-10 and covariance_error <= 1.0e-10
    return result(
        "CHK-CG-FRAME-CANCELLATION",
        "Canonical-frame Gaussian parameters under common reframing",
        ["NUM-CG-FRAME-CANCELLATION"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count=1,
        expected={"canonical_mean_unchanged": True, "canonical_covariance_unchanged": True},
        tolerances={"absolute": 1.0e-10},
        observed={"mean_error": mean_error, "covariance_error": covariance_error},
        interpretation="The check is a direct substitution into the orbit-invariant parameter pair.",
    )


def check_cg_equivariance() -> dict[str, Any]:
    cases = [(2, 3), (3, 4), (4, 5), (5, 6), (5, 3)]
    rows = []
    passed = True
    for k, n in cases:
        angle = 2.0 * math.pi / n
        v = np.eye(k)
        v[:2, :2] = np.array(
            [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]
        )
        order_residual = float(np.linalg.norm(np.linalg.matrix_power(v, n) - np.eye(k), ord="fro"))
        rank = int(np.linalg.matrix_rank(np.eye(k) - v, tol=1.0e-10))
        det = float(np.linalg.det(v))
        rows.append({"K": k, "n": n, "determinant": det, "order_residual": order_residual, "rank_I_minus_v": rank})
        passed &= det > 0 and order_residual <= 1.0e-10 and rank == 2
    return result(
        "CHK-CG-EQUIVARIANCE",
        "Finite-order GL+ witnesses for the equivariance obstruction",
        ["NUM-CG-EQUIVARIANCE"],
        status="PASS" if passed else "FAIL",
        seed=None,
        sample_count=len(cases),
        expected={"determinant_positive": True, "v_power_n": "identity", "rank_I_minus_v": 2},
        tolerances={"order_residual": 1.0e-10, "rank": 1.0e-10},
        observed={"cases": rows},
        interpretation="Plane rotations give deterministic witnesses; no random draw is required.",
    )


def check_rg_ray_kernel() -> dict[str, Any]:
    seed = 20260729
    rng = np.random.default_rng(seed)
    observed = []
    passed = True
    for n, k in [(5, 2), (6, 3), (7, 4), (5, 3), (6, 2)]:
        x = rng.uniform(0.2, 2.0, size=n)
        s = float(x.sum())
        m = random_spd(rng, k)
        spatial = s * np.diag(x) - np.outer(x, x)
        lap = np.kron(spatial, m)
        eig = np.linalg.eigvalsh(lap)
        tol = max(float(eig[-1]), 1.0) * 1.0e-10
        nullity = int(np.count_nonzero(np.abs(eig) <= tol))
        residual = float(np.linalg.norm(lap @ np.kron(np.ones((n, 1)), np.eye(k)), ord="fro"))
        observed.append({"N": n, "K": k, "nullity": nullity, "consensus_residual": residual})
        passed &= nullity == k and residual <= 1.0e-9
    n, k = 5, 3
    x = rng.uniform(0.2, 2.0, size=n)
    q, _ = np.linalg.qr(rng.standard_normal((k, k)))
    m = q @ np.diag([2.0, 1.0, 0.0]) @ q.T
    lap = np.kron(float(x.sum()) * np.diag(x) - np.outer(x, x), m)
    eig = np.linalg.eigvalsh(lap)
    tol = max(float(eig[-1]), 1.0) * 1.0e-10
    control_nullity = int(np.count_nonzero(np.abs(eig) <= tol))
    expected_control = k + (n - 1) * (k - 2)
    passed &= control_nullity == expected_control
    return result(
        "CHK-RG-RAY-KERNEL",
        "Kernel of the bi-additive matrix ray",
        ["NUM-RG-RAY-KERNEL"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count="five full-rank draws and one rank-two control",
        expected={"full_rank_nullity": "K", "rank_two_control_nullity": expected_control},
        tolerances={"rank_relative": 1.0e-10, "consensus_absolute": 1.0e-9},
        observed={"full_rank_cases": observed, "rank_two_control_nullity": control_nullity},
        interpretation="The rank-deficient control checks the full kernel formula, not only the consensus subspace.",
    )


def check_rg_sector_split() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    n, k = 8, 3
    assignments = [0, 0, 1, 1, 2, 2, 3, 3]
    s = incidence_map(assignments, k)
    weights = {(i, j): random_spd(rng, k, 0.1) for i in range(n) for j in range(i + 1, n)}
    self_terms = [random_spd(rng, k, 0.1) for _ in range(n)]
    base, _ = assemble_interaction(self_terms, weights)
    coarse_base = s.T @ base @ s

    changed_self = [a + random_spd(rng, k, 0.1) for a in self_terms]
    self_changed, _ = assemble_interaction(changed_self, weights)
    coarse_self_changed = s.T @ self_changed @ s
    offdiag_change = 0.0
    nc = 4
    for i in range(nc):
        for j in range(i + 1, nc):
            block = (
                coarse_self_changed[i * k : (i + 1) * k, j * k : (j + 1) * k]
                - coarse_base[i * k : (i + 1) * k, j * k : (j + 1) * k]
            )
            offdiag_change = max(offdiag_change, float(np.linalg.norm(block, ord="fro")))

    weights_changed = {key: value.copy() for key, value in weights.items()}
    delta = 1000.0 * np.eye(k)
    weights_changed[(0, 1)] += delta
    internal_changed, _ = assemble_interaction(self_terms, weights_changed)
    coarse_internal_changed = s.T @ internal_changed @ s
    diagonal_change = 0.0
    for i in range(nc):
        block = (
            coarse_internal_changed[i * k : (i + 1) * k, i * k : (i + 1) * k]
            - coarse_base[i * k : (i + 1) * k, i * k : (i + 1) * k]
        )
        diagonal_change = max(diagonal_change, float(np.linalg.norm(block, ord="fro")))
    passed = offdiag_change <= 1.0e-10 and diagonal_change <= 1.0e-9
    return result(
        "CHK-RG-SECTOR-SPLIT",
        "Independent self and coupling sectors under declared aggregation",
        ["NUM-RG-SECTOR-SPLIT"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count="one system and two perturbation controls",
        expected={
            "self_to_coarse_coupling_residual": "<= declared tolerance",
            "internal_edge_to_coarse_self_residual": "<= declared tolerance",
        },
        tolerances={"absolute": 1.0e-9},
        observed={"maximum_coarse_offdiagonal_change_from_self": offdiag_change, "maximum_coarse_diagonal_change_from_internal_edge": diagonal_change},
        interpretation="The test isolates blocks of the exact parameter map; it does not assert attraction.",
    )


def aggregate_weights_pairwise(
    weights: dict[tuple[int, int], np.ndarray], n: int
) -> tuple[dict[tuple[int, int], np.ndarray], int]:
    assignments = [i // 2 for i in range(n)]
    nc = (n + 1) // 2
    out: dict[tuple[int, int], np.ndarray] = {}
    k = next(iter(weights.values())).shape[0]
    for ci in range(nc):
        for cj in range(ci + 1, nc):
            out[(ci, cj)] = sum(
                (
                    w
                    for (i, j), w in weights.items()
                    if {assignments[i], assignments[j]} == {ci, cj}
                ),
                np.zeros((k, k)),
            )
    return out, nc


def check_rg_invariant_faces() -> dict[str, Any]:
    seed = 20260729
    rng = np.random.default_rng(seed)
    n, k = 16, 3
    v = rng.standard_normal(k)
    rank_one = np.outer(v, v)
    common = {
        (i, j): rng.uniform(0.2, 2.0) * rank_one
        for i in range(n)
        for j in range(i + 1, n)
    }
    full = {
        (i, j): random_spd(rng, k, 0.2)
        for i in range(n)
        for j in range(i + 1, n)
    }
    rank_history = []
    full_rank_history = []
    current_n = n
    for _level in range(3):
        common, current_n = aggregate_weights_pairwise(common, current_n)
        full, _ = aggregate_weights_pairwise(full, current_n * 2)
        common_ranks = [int(np.linalg.matrix_rank(w, tol=1.0e-10)) for w in common.values()]
        full_ranks = [int(np.linalg.matrix_rank(w, tol=1.0e-10)) for w in full.values()]
        rank_history.append(sorted(set(common_ranks)))
        full_rank_history.append(sorted(set(full_ranks)))
    t_values = np.logspace(-2, 2, 21)
    distance_errors = []
    for t in t_values:
        mt = np.diag([t, 1.0, 1.0])
        eig = np.linalg.eigvalsh(mt)
        hilbert = math.log(float(eig.max() / eig.min()))
        distance_errors.append(abs(hilbert - abs(math.log(float(t)))))
    max_distance_error = max(distance_errors)
    passed = all(ranks == [1] for ranks in rank_history) and all(ranks == [3] for ranks in full_rank_history) and max_distance_error <= 1.0e-12
    return result(
        "CHK-RG-INVARIANT-FACES",
        "Common-range invariant face and unbounded projective diameter",
        ["NUM-RG-INVARIANT-FACES"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count="three pair-aggregation levels and 21 t values over four decades",
        expected={"common_range_rank": 1, "full_range_rank": k, "hilbert_distance": "abs(log t)"},
        tolerances={"rank": 1.0e-10, "distance_absolute": 1.0e-12},
        observed={
            "common_range_rank_sets_by_level": rank_history,
            "full_range_rank_sets_by_level": full_rank_history,
            "maximum_projective_distance_error": max_distance_error,
        },
        interpretation="Persistent rank-one ranges exhibit an invariant proper face, while the distance family has no finite diameter bound.",
    )


def check_rg_homogeneous_gate() -> dict[str, Any]:
    k, b = 2, 2
    symmetric_basis = [
        sp.Matrix([[1, 0], [0, 0]]),
        sp.Matrix([[0, 0], [0, 1]]),
        sp.Matrix([[0, 1], [1, 0]]),
    ]

    def sym_coordinates(matrix: sp.Matrix) -> sp.Matrix:
        return sp.Matrix([matrix[0, 0], matrix[1, 1], matrix[0, 1]])

    columns = []
    for sector in ("coupling", "self"):
        for basis_matrix in symmetric_basis:
            if sector == "coupling":
                output_coupling = b**2 * basis_matrix
                output_self = sp.zeros(k)
            else:
                output_coupling = sp.zeros(k)
                output_self = b * basis_matrix
            columns.append(
                sym_coordinates(output_coupling).col_join(
                    sym_coordinates(output_self)
                )
            )
    endomorphism = sp.Matrix.hstack(*columns)
    characteristic_variable = sp.symbols("x")
    characteristic = sp.factor(
        endomorphism.charpoly(characteristic_variable).as_expr()
    )
    exact_eigenvalues = {
        str(eigenvalue): int(multiplicity)
        for eigenvalue, multiplicity in endomorphism.eigenvals().items()
    }
    numeric_eigenvalues = sorted(
        [float(value) for value in endomorphism.eigenvals().keys()],
        reverse=True,
    )
    expanded_eigenvalues = sorted(
        [
            float(value)
            for value, multiplicity in endomorphism.eigenvals().items()
            for _ in range(int(multiplicity))
        ],
        reverse=True,
    )
    distinct = sorted(set(expanded_eigenvalues), reverse=True)
    naive_ratio = expanded_eigenvalues[1] / expanded_eigenvalues[0]
    outside_dominant_ratio = distinct[1] / distinct[0]
    normalized_self_ratios = [(1.0 / b) ** level for level in range(9)]
    passed = (
        endomorphism.shape == (6, 6)
        and characteristic == (characteristic_variable - 4) ** 3
        * (characteristic_variable - 2) ** 3
        and exact_eigenvalues == {"4": 3, "2": 3}
        and naive_ratio == 1.0
        and outside_dominant_ratio == 0.5
        and all(a > bval for a, bval in zip(normalized_self_ratios, normalized_self_ratios[1:]))
    )
    return result(
        "CHK-RG-HOMOGENEOUS-GATE",
        "Exact homogeneous gate spectrum and sector ratio",
        ["RG-HOMOGENEOUS-EXACT"],
        status="PASS" if passed else "FAIL",
        seed=None,
        sample_count="one exact 6x6 Sym(2) coupling-plus-self endomorphism at b=2",
        expected={"spectrum": [4, 4, 4, 2, 2, 2], "naive_top_two_ratio": 1, "outside_dominant_ratio": 0.5},
        tolerances={"arithmetic": "exact integers"},
        observed={
            "symmetric_basis": [
                [[str(entry) for entry in row] for row in matrix.tolist()]
                for matrix in symmetric_basis
            ],
            "endomorphism_matrix": [
                [str(entry) for entry in row] for row in endomorphism.tolist()
            ],
            "characteristic_polynomial": str(characteristic),
            "eigenvalue_multiplicities": exact_eigenvalues,
            "distinct_numeric_eigenvalues": numeric_eigenvalues,
            "spectrum_with_multiplicity": expanded_eigenvalues,
            "naive_top_two_ratio": naive_ratio,
            "outside_dominant_ratio": outside_dominant_ratio,
            "normalized_self_sector_ratios_by_level": normalized_self_ratios,
        },
        evidence_kind="exact_algebraic_evaluation",
        interpretation="The actual endomorphism is built on an explicit Sym(2) basis and diagonalized exactly. It does not reproduce the heterogeneous matched-null table or establish a physical fixed law.",
    )


def graph_laplacian_matrix(rng: np.random.Generator, n: int, k: int) -> np.ndarray:
    weights = {
        (i, j): random_spd(rng, k, 0.2)
        for i in range(n)
        for j in range(i + 1, n)
        if rng.random() < 0.65
    }
    # Add a chain to guarantee connectivity.
    for i in range(n - 1):
        weights.setdefault((i, i + 1), random_spd(rng, k, 0.2))
    _, lap = assemble_interaction([np.zeros((k, k)) for _ in range(n)], weights)
    return lap


def positive_quotient_basis(lap: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    eig, vec = np.linalg.eigh(lap)
    tol = max(float(eig[-1]), 1.0) * 1.0e-10
    mask = eig > tol
    return vec[:, mask], eig[mask]


def check_rg_noncommuting_limits_symbolic() -> dict[str, Any]:
    d, eps = sp.symbols("d eps")
    scalar_lap = sp.Matrix([[1, -1], [-1, 1]])
    symbolic_det = sp.factor((scalar_lap - d * (scalar_lap + eps * sp.eye(2))).det())
    expected_det = sp.factor(d * eps * (d * eps + 2 * d - 2))
    symbolic_match = sp.simplify(symbolic_det - expected_det) == 0
    x1, x2, x3, fiber = sp.symbols("x1 x2 x3 m")
    spatial = sp.Matrix(
        [
            [x1 * (x2 + x3), -x1 * x2, -x1 * x3],
            [-x1 * x2, x2 * (x1 + x3), -x2 * x3],
            [-x1 * x3, -x2 * x3, x3 * (x1 + x2)],
        ]
    )
    ray_laplacian = fiber * spatial
    ray_det = sp.factor(ray_laplacian.det())
    ray_pencil_det = sp.factor(((1 - d) * ray_laplacian).det())
    a, spectral_lambda = sp.symbols("a lambda", positive=True)
    transfer = spectral_lambda / (spectral_lambda + a)
    mass_then_infrared = sp.limit(sp.limit(transfer, a, 0, dir="+"), spectral_lambda, 0, dir="+")
    infrared_then_mass = sp.limit(sp.limit(transfer, spectral_lambda, 0, dir="+"), a, 0, dir="+")
    passed = (
        symbolic_match
        and ray_det == 0
        and ray_pencil_det == 0
        and mass_then_infrared == 1
        and infrared_then_mass == 0
    )
    return result(
        "CHK-RG-NONCOMMUTING-LIMITS",
        "Exact symbolic singular pencils and noncommuting mass/spectral limits",
        ["NUM-RG-NONCOMMUTING"],
        status="PASS" if passed else "FAIL",
        seed=None,
        sample_count="one exact symbolic two-node pencil, one symbolic three-agent bi-additive ray, and two iterated limits",
        expected={
            "symbolic_determinant": "d*eps*(d*eps + 2*d - 2)",
            "three_agent_ray_determinant": 0,
            "three_agent_ray_pencil_determinant": 0,
            "a_to_zero_at_fixed_lambda": 1,
            "lambda_to_zero_at_fixed_a": 0,
        },
        tolerances={"symbolic": "exact"},
        observed={
            "two_node_symbolic_determinant": str(symbolic_det),
            "three_agent_ray_determinant": str(ray_det),
            "three_agent_ray_pencil_determinant": str(ray_pencil_det),
            "mass_then_infrared_limit": str(mass_then_infrared),
            "infrared_then_mass_limit": str(infrared_then_mass),
        },
        evidence_kind="exact_symbolic_witness",
        interpretation="Only this exact symbolic check supports the manuscript's keep-exact disposition for the noncommuting-limit numerical tag.",
    )


def check_rg_noncommuting_limits_floating() -> dict[str, Any]:
    seed = 20260729
    rng = np.random.default_rng(seed)
    lap = graph_laplacian_matrix(rng, 6, 2)
    q, positive = positive_quotient_basis(lap)
    bar = q.T @ lap @ q
    quotient_eigen = sla.eigvalsh(bar, bar)
    quotient_error = float(np.max(np.abs(quotient_eigen - 1.0)))
    tolerance = 1.0e-10
    passed = quotient_error <= tolerance
    return result(
        "CHK-RG-NONCOMMUTING-FLOATING",
        "Seeded six-agent floating quotient-pencil control",
        ["SUPPLEMENT-RG-NONCOMMUTING-FLOATING"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count="one six-agent K=2 graph-Laplacian quotient pencil",
        expected={"quotient_generalized_eigenvalues": "within tolerance of one"},
        tolerances={"absolute_generalized_eigenvalue": tolerance},
        observed={
            "quotient_eigenvalues": quotient_eigen,
            "quotient_eigenvalue_max_error": quotient_error,
            "positive_quotient_dimension": len(positive),
        },
        evidence_kind="reproduced_output",
        interpretation="This separately seeded floating check is current corroboration only and is not classified as keep-exact evidence.",
    )


def check_rg_mass_pencil() -> dict[str, Any]:
    seed = 20260729
    rng = np.random.default_rng(seed)
    lap = graph_laplacian_matrix(rng, 6, 2)
    r = random_spd(rng, lap.shape[0], 1.0)
    generalized_lambda = sla.eigvalsh(lap, r)
    max_errors = {}
    for a in [0.5, 1.0, 3.0]:
        d_values = sla.eigvalsh(lap, lap + a * r)
        predicted = generalized_lambda / (generalized_lambda + a)
        max_errors[str(a)] = float(np.max(np.abs(np.sort(d_values) - np.sort(predicted))))
    r_identity = np.eye(lap.shape[0])
    smallest_nonzero = {}
    q, positive_lap = positive_quotient_basis(lap)
    for a in [1.0, 1.0e-2, 1.0e-4]:
        d_values = sla.eigvalsh(lap, lap + a * r_identity)
        positive_d = d_values[d_values > 1.0e-10]
        smallest_nonzero[str(a)] = float(positive_d.min())
    passed = max(max_errors.values()) <= 1.0e-10 and smallest_nonzero["0.0001"] > smallest_nonzero["1.0"]
    return result(
        "CHK-RG-MASS-PENCIL",
        "Mass-pencil eigenvalue transfer",
        ["NUM-RG-MASS-TRANSFER"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count="one 12x12 pencil at three masses plus a three-mass identity control",
        expected={"d_k": "lambda_k/(lambda_k+a)", "smaller_mass_moves_nonzero_d_toward_one": True},
        tolerances={"eigenvalue_absolute": 1.0e-10},
        observed={
            "maximum_transfer_errors": max_errors,
            "smallest_nonzero_d_by_mass": smallest_nonzero,
            "positive_laplacian_eigenvalue_count": len(positive_lap),
        },
        interpretation="The check uses a regular positive-definite reference form and treats zero modes separately.",
    )


def star_precision(
    p0: np.ndarray, omegas: list[np.ndarray], covariances: list[np.ndarray]
) -> np.ndarray:
    k = p0.shape[0]
    n = len(omegas)
    out = np.zeros(((n + 1) * k, (n + 1) * k))
    out[:k, :k] = p0
    for idx, (omega, covariance) in enumerate(zip(omegas, covariances), start=1):
        rinv = np.linalg.inv(covariance)
        si = slice(idx * k, (idx + 1) * k)
        out[:k, :k] += omega.T @ rinv @ omega
        out[:k, si] -= omega.T @ rinv
        out[si, :k] -= rinv @ omega
        out[si, si] += rinv
    return out


def reciprocal_precision(
    omega_uv: np.ndarray,
    omega_vu: np.ndarray,
    r_uv: np.ndarray,
    r_vu: np.ndarray,
) -> np.ndarray:
    k = omega_uv.shape[0]
    e_uv = np.hstack([np.eye(k), -omega_uv])
    e_vu = np.hstack([-omega_vu, np.eye(k)])
    return e_uv.T @ np.linalg.solve(r_uv, e_uv) + e_vu.T @ np.linalg.solve(r_vu, e_vu)


def check_obs_star_fold_new_protocol() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    draws, k, n = 300, 3, 4
    star_minima = []
    fold_nullities = []
    precision_block_errors = []
    for _ in range(draws):
        p0 = random_spd(rng, k, 0.5)
        omegas = [random_gl_plus(rng, k) for _i in range(n)]
        covariances = [random_spd(rng, k, 0.5) for _i in range(n)]
        star = star_precision(p0, omegas, covariances)
        star_minima.append(float(np.linalg.eigvalsh(star).min()))
        predicted_bb = p0 + sum(
            (omega.T @ np.linalg.solve(covariance, omega) for omega, covariance in zip(omegas, covariances)),
            np.zeros((k, k)),
        )
        precision_block_errors.append(float(np.linalg.norm(star[:k, :k] - predicted_bb, ord="fro")))

        omega_uv = random_gl_plus(rng, k)
        omega_vu = np.linalg.inv(omega_uv)
        fold = reciprocal_precision(
            omega_uv, omega_vu, random_spd(rng, k, 0.5), random_spd(rng, k, 0.5)
        )
        eig = np.linalg.eigvalsh(fold)
        tol = max(float(eig[-1]), 1.0) * 1.0e-9
        fold_nullities.append(int(np.count_nonzero(np.abs(eig) <= tol)))
    passed = min(star_minima) > 0 and set(fold_nullities) == {k} and max(precision_block_errors) <= 1.0e-10
    return result(
        "CHK-OBS-STAR-FOLD-NEW-PROTOCOL",
        "New declared-seed star-versus-reciprocal-fold protocol",
        ["NUM-OBS-STAR-FOLD"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count=draws,
        expected={"all_stars_positive_definite": True, "cocycle_fold_nullity": k, "apex_precision_addition": True},
        tolerances={"fold_rank_relative": 1.0e-9, "precision_block_absolute": 1.0e-10},
        observed={
            "minimum_star_eigenvalue": min(star_minima),
            "fold_nullities_observed": sorted(set(fold_nullities)),
            "maximum_apex_precision_block_error": max(precision_block_errors),
        },
        interpretation="This is a replacement run. The manuscript's historical 300-draw extrema remain unrecoverable because their seed and matrices were lost.",
    )


def check_obs_holonomy_det_kernel() -> dict[str, Any]:
    seed = 20260728
    rng = np.random.default_rng(seed)
    logdet_errors = []
    usable_draws = 0
    for draw in range(1000):
        k = draw % 5 + 1
        omega_uv = random_gl_plus(rng, k, 0.20)
        q, _ = np.linalg.qr(rng.standard_normal((k, k)))
        h_eigenvalues = rng.choice([-1.0, 1.0], size=k) * rng.uniform(0.25, 0.65, size=k) + 1.0
        h = q @ np.diag(h_eigenvalues) @ q.T
        omega_vu = h @ np.linalg.inv(omega_uv)
        r_uv = random_spd(rng, k, 1.0)
        r_vu = random_spd(rng, k, 1.0)
        h = omega_vu @ omega_uv
        j = reciprocal_precision(omega_uv, omega_vu, r_uv, r_vu)
        sign_j, logdet_j = np.linalg.slogdet(j)
        sign_h, logdet_h = np.linalg.slogdet(np.eye(k) - h)
        sign_ruv, logdet_ruv = np.linalg.slogdet(r_uv)
        sign_rvu, logdet_rvu = np.linalg.slogdet(r_vu)
        if sign_j > 0 and sign_h != 0 and sign_ruv > 0 and sign_rvu > 0:
            predicted = 2.0 * logdet_h - logdet_ruv - logdet_rvu
            logdet_errors.append(abs(float(logdet_j - predicted)))
            usable_draws += 1

    cases = []
    kernel_match = True
    for k in range(2, 6):
        for multiplicity in range(k + 1):
            q, _ = np.linalg.qr(rng.standard_normal((k, k)))
            nonunit = [1.5 + 0.3 * idx for idx in range(k - multiplicity)]
            h = q @ np.diag([1.0] * multiplicity + nonunit) @ q.T
            omega_uv = np.eye(k)
            omega_vu = h
            j = reciprocal_precision(omega_uv, omega_vu, random_spd(rng, k, 1.0), random_spd(rng, k, 1.0))
            eig_j = np.linalg.eigvalsh(j)
            j_tol = max(float(eig_j[-1]), 1.0) * 1.0e-9
            observed_nullity = int(np.count_nonzero(np.abs(eig_j) <= j_tol))
            observed_fixed = k - np.linalg.matrix_rank(h - np.eye(k), tol=1.0e-9)
            kernel_match &= observed_nullity == multiplicity == observed_fixed
            cases.append(
                {
                    "K": k,
                    "prescribed_multiplicity": multiplicity,
                    "J_nullity": observed_nullity,
                    "fixed_space_dimension": int(observed_fixed),
                }
            )
    max_logdet_error = max(logdet_errors) if logdet_errors else math.inf
    passed = usable_draws >= 990 and max_logdet_error <= 1.0e-7 and kernel_match and len(cases) == 18
    return result(
        "CHK-OBS-HOLONOMY-DET-KERNEL",
        "Reciprocal-pair determinant and fixed-space kernel",
        ["NUM-OBS-HOLONOMY-DET-KERNEL"],
        status="PASS" if passed else "FAIL",
        seed=seed,
        sample_count={"determinant_draws": 1000, "prescribed_kernel_cases": len(cases)},
        expected={
            "logdet_J": "2 log|det(I-H)| - logdet(R_uv) - logdet(R_vu)",
            "J_nullity": "dim ker(H-I)",
        },
        tolerances={"logdet_absolute": 1.0e-7, "rank_relative": 1.0e-9},
        observed={
            "usable_determinant_draws": usable_draws,
            "maximum_logdet_identity_error": max_logdet_error,
            "all_kernel_cases_match": kernel_match,
            "kernel_cases": cases,
        },
        interpretation="Orthogonal similarities control rank conditioning in the prescribed-multiplicity cases.",
    )


def check_obs_normalizer_witness() -> dict[str, Any]:
    a, p0 = sp.symbols("a p0", nonzero=True)
    j = sp.Matrix(
        [[1 + a ** -2, -(a + a ** -1)], [-(a + a ** -1), 1 + a**2]]
    )
    determinant = sp.factor((j + p0 * sp.eye(2)).det())
    expected = sp.factor(p0**2 + p0 * (a + a**-1) ** 2)
    derivative = sp.factor(sp.diff(expected, a))
    matched = sp.simplify(determinant - expected) == 0
    numeric = {str(value): float(expected.subs({a: value, p0: 1})) for value in [1, 2, 3]}
    passed = matched and numeric["1"] < numeric["2"] < numeric["3"]
    return result(
        "CHK-OBS-NORMALIZER-WITNESS",
        "Exact scalar reciprocal-pair normalizer witness",
        ["NUM-OBS-HOLONOMY-DET-KERNEL"],
        status="PASS" if passed else "FAIL",
        seed=None,
        sample_count="one exact symbolic family and three evaluation points",
        expected={"determinant": "p0^2 + p0(a+a^-1)^2", "nonconstant": True},
        tolerances={"arithmetic": "exact symbolic"},
        observed={"determinant": str(determinant), "derivative": str(derivative), "p0_equals_1_values": numeric},
        evidence_kind="exact_symbolic_witness",
        interpretation="The determinant varies with transport. The sign of the induced log-normalizer force must be read from the chosen optimization objective, not inferred from determinant minimization alone.",
    )


CHECKS: list[Callable[[], dict[str, Any]]] = [
    check_gauss_projection,
    check_gauss_trivialization,
    check_gauss_conditioning,
    check_kron_exact_witness,
    check_kron_monte_carlo,
    check_restriction_schur,
    check_ig_expectation_metric,
    check_ig_pullback_pushforward,
    check_generalized_spectrum,
    check_cg_aggregation,
    check_graph_holonomy,
    check_cg_maximal_clusters,
    check_cg_lambda_continuum,
    check_cg_pair_merge,
    check_cg_biadditive,
    check_cg_epsilon_divergence,
    check_cg_factor_gap,
    check_cg_factor_gap_stress,
    check_cg_frame_cancellation,
    check_cg_equivariance,
    check_rg_ray_kernel,
    check_rg_sector_split,
    check_rg_invariant_faces,
    check_rg_homogeneous_gate,
    check_rg_noncommuting_limits_symbolic,
    check_rg_noncommuting_limits_floating,
    check_rg_mass_pencil,
    check_obs_star_fold_new_protocol,
    check_obs_holonomy_det_kernel,
    check_obs_normalizer_witness,
]

PRODUCTION_CHECK_IDS = (
    "CHK-GAUSS-PROJECTION",
    "CHK-GAUSS-TRIVIALIZATION",
    "CHK-GAUSS-CONDITIONING",
    "CHK-KRON-EXACT-WITNESS",
    "CHK-KRON-MONTE-CARLO",
    "CHK-RESTRICTION-SCHUR",
    "CHK-IG-EXPECTATION-METRIC",
    "CHK-IG-PULLBACK-PUSHFORWARD",
    "CHK-GENERALIZED-SPECTRUM",
    "CHK-CG-AGGREGATION",
    "CHK-GRAPH-HOLONOMY",
    "CHK-CG-MAXIMAL-CLUSTERS",
    "CHK-CG-LAMBDA-CONTINUUM",
    "CHK-CG-PAIR-MERGE",
    "CHK-CG-BIADDITIVE",
    "CHK-CG-EPSILON-DIVERGENCE",
    "CHK-CG-FACTOR-GAP",
    "CHK-CG-FACTOR-GAP-STRESS-3138",
    "CHK-CG-FRAME-CANCELLATION",
    "CHK-CG-EQUIVARIANCE",
    "CHK-RG-RAY-KERNEL",
    "CHK-RG-SECTOR-SPLIT",
    "CHK-RG-INVARIANT-FACES",
    "CHK-RG-HOMOGENEOUS-GATE",
    "CHK-RG-NONCOMMUTING-LIMITS",
    "CHK-RG-NONCOMMUTING-FLOATING",
    "CHK-RG-MASS-PENCIL",
    "CHK-OBS-STAR-FOLD-NEW-PROTOCOL",
    "CHK-OBS-HOLONOMY-DET-KERNEL",
    "CHK-OBS-NORMALIZER-WITNESS",
)
PRODUCTION_REQUIRED_CHECK_IDS = ("CHK-SOURCE-INVENTORY", *PRODUCTION_CHECK_IDS)


def _issue(
    code: str,
    location: str,
    message: str,
    *,
    expected: Any = None,
    observed: Any = None,
) -> VerificationIssue:
    if code not in ISSUE_CODES:
        raise ValueError(f"unknown verification issue code: {code}")
    return VerificationIssue(code, location, message, expected, observed)


def _stable_executable_identity(path: Path, role: str) -> dict[str, Any]:
    """Hash one fixed executable while rejecting reparse-mediated identity."""

    absolute = Path(os.path.abspath(os.fspath(path)))
    if not absolute.is_absolute():
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            str(path),
            f"fixed {role} executable path is not absolute",
        )
    parts = absolute.parts
    current = Path(parts[0])
    for part in parts[1:]:
        current /= part
        try:
            current.lstat()
        except OSError as exc:
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                str(absolute),
                f"fixed {role} executable component cannot be inspected: {current}",
            ) from exc
        if _is_link_or_reparse(current):
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                str(absolute),
                f"fixed {role} executable is reparse-mediated at {current}",
            )
    try:
        payload, identity_before = _open_stable_regular_file(absolute)
    except OSError as exc:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            str(absolute),
            f"fixed {role} executable cannot be read safely: {exc}",
        ) from exc
    return {
        "path": str(path),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "byte_count": len(payload),
        "filesystem_identity": list(identity_before),
    }


def _guarded_executable_snapshot(
    guard: _WindowsExecutableGuard,
    path: Path,
    role: str,
) -> dict[str, Any]:
    """Cross-check a held Windows handle against a stable lexical-path read."""

    guard_snapshot = guard.snapshot()
    path_snapshot = _stable_executable_identity(path, role)
    for field in ("path", "sha256", "byte_count"):
        if guard_snapshot[field] != path_snapshot[field]:
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                str(path),
                f"guarded {role} handle does not equal the fixed executable path",
                expected=guard_snapshot,
                observed=path_snapshot,
            )
    return {
        **path_snapshot,
        "guard_filesystem_identity": guard_snapshot[
            "guard_filesystem_identity"
        ],
    }


def _acquire_executable_guards() -> dict[str, _WindowsExecutableGuard]:
    """Acquire both fixed executable guards, closing partial state on failure."""

    guards: dict[str, _WindowsExecutableGuard] = {}
    try:
        guards["python"] = _WindowsExecutableGuard(
            _FIXED_PYTHON_EXECUTABLE,
            "Python",
        )
        guards["git"] = _WindowsExecutableGuard(
            _FIXED_GIT_EXECUTABLE,
            "Git",
        )
    except BaseException:
        _close_executable_guards(guards)
        raise
    return guards


def _close_executable_guards(
    guards: dict[str, _WindowsExecutableGuard],
) -> None:
    """Close fixed executable guards in reverse acquisition order."""

    first_error: BaseException | None = None
    for name in ("git", "python"):
        guard = guards.get(name)
        if guard is None:
            continue
        try:
            guard.close()
        except BaseException as exc:
            if first_error is None:
                first_error = exc
    if first_error is not None:
        raise first_error


def _verification_executable_snapshot() -> dict[str, dict[str, Any]]:
    """Return private byte and filesystem identities for both fixed tools."""

    actual_python = Path(os.path.abspath(sys.executable))
    expected_python = Path(os.path.abspath(os.fspath(_FIXED_PYTHON_EXECUTABLE)))
    if os.path.normcase(str(actual_python)) != os.path.normcase(str(expected_python)):
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            "$.environment.python_executable",
            "verification must run under the fixed production Python executable",
            expected=str(_FIXED_PYTHON_EXECUTABLE),
            observed=sys.executable,
        )
    guards = _ACTIVE_EXECUTABLE_GUARDS.get()
    owned_guards = guards is None
    if guards is None:
        guards = _acquire_executable_guards()
    try:
        current_snapshot = {
            "python": _guarded_executable_snapshot(
                guards["python"],
                _FIXED_PYTHON_EXECUTABLE,
                "Python",
            ),
            "git": _guarded_executable_snapshot(
                guards["git"],
                _FIXED_GIT_EXECUTABLE,
                "Git",
            ),
        }
    finally:
        if owned_guards:
            _close_executable_guards(guards)
    expected_snapshot = _ACTIVE_EXECUTABLE_IDENTITIES.get()
    if expected_snapshot is not None and current_snapshot != expected_snapshot:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            "$.environment",
            "fixed verification executable identities changed after M0",
            expected=expected_snapshot,
            observed=current_snapshot,
        )
    return current_snapshot


def _public_executable_identities(
    snapshot: dict[str, dict[str, Any]],
) -> dict[str, str]:
    """Project a private tool snapshot into the closed public result shape."""

    return {
        "python_executable": snapshot["python"]["path"],
        "python_executable_sha256": snapshot["python"]["sha256"],
        "git_executable": snapshot["git"]["path"],
        "git_executable_sha256": snapshot["git"]["sha256"],
    }


def _verification_executable_identities() -> dict[str, str]:
    """Return the closed public projection of the current fixed tool snapshot."""

    return _public_executable_identities(_verification_executable_snapshot())


def _require_production_cli_runtime() -> None:
    """Require isolated startup before any ordinary production CLI evidence."""

    if sys.flags.isolated != 1 or sys.flags.no_site != 1:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            "$.environment.python_executable",
            "ordinary production CLI execution requires Python modes -I -S",
            expected={"isolated": 1, "no_site": 1},
            observed={
                "isolated": sys.flags.isolated,
                "no_site": sys.flags.no_site,
            },
        )
    _verification_executable_identities()
    fixed_site = str(_FIXED_SITE_PACKAGES)
    if sys.path.count(fixed_site) != 1:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            "$.environment.dependency_provenance",
            "isolated production startup must append exactly one fixed package root",
            expected=fixed_site,
            observed=list(sys.path),
        )


def _sanitized_git_environment() -> dict[str, str]:
    """Return the caller environment with every Git override removed."""

    return {
        key: value
        for key, value in os.environ.items()
        if not key.upper().startswith("GIT_")
    }


def _git(
    repo_root: Path,
    *arguments: str,
    input_bytes: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    environment = _sanitized_git_environment()
    active_guards = _ACTIVE_EXECUTABLE_GUARDS.get()
    owned_guard = active_guards is None
    guard = (
        _WindowsExecutableGuard(_FIXED_GIT_EXECUTABLE, "Git")
        if active_guards is None
        else active_guards["git"]
    )
    try:
        git_identity = _guarded_executable_snapshot(
            guard,
            _FIXED_GIT_EXECUTABLE,
            "Git",
        )
        expected_snapshot = _ACTIVE_EXECUTABLE_IDENTITIES.get()
        if expected_snapshot is not None:
            expected_git_identity = expected_snapshot["git"]
            if git_identity != expected_git_identity:
                raise VerificationFailure(
                    "EXECUTABLE_IDENTITY",
                    "$.environment.git_executable",
                    "fixed Git executable identity changed after M0",
                    expected=expected_git_identity,
                    observed=git_identity,
                )
        stream_arguments: dict[str, Any] = (
            {"stdin": subprocess.DEVNULL}
            if input_bytes is None
            else {"input": input_bytes}
        )
        metadata_roots = _reject_git_metadata_overrides(
            repo_root,
            git_guard=guard,
        )
        _reject_git_metadata_overrides(
            repo_root,
            git_guard=guard,
            expected_roots=metadata_roots,
        )

        def close_subprocess_attempt() -> None:
            postflight_errors: list[BaseException] = []
            try:
                _reject_git_metadata_overrides(
                    repo_root,
                    git_guard=guard,
                    expected_roots=metadata_roots,
                )
            except BaseException as exc:
                postflight_errors.append(exc)
            try:
                closing_git_identity = _guarded_executable_snapshot(
                    guard,
                    _FIXED_GIT_EXECUTABLE,
                    "Git",
                )
                if closing_git_identity != git_identity:
                    raise VerificationFailure(
                        "EXECUTABLE_IDENTITY",
                        "$.environment.git_executable",
                        "fixed Git executable changed across one subprocess invocation",
                        expected=git_identity,
                        observed=closing_git_identity,
                    )
                if (
                    expected_snapshot is not None
                    and closing_git_identity != expected_snapshot["git"]
                ):
                    raise VerificationFailure(
                        "EXECUTABLE_IDENTITY",
                        "$.environment.git_executable",
                        "fixed Git executable identity changed after M0",
                        expected=expected_snapshot["git"],
                        observed=closing_git_identity,
                    )
            except BaseException as exc:
                postflight_errors.append(exc)
            if len(postflight_errors) == 1:
                raise postflight_errors[0]
            if postflight_errors:
                raise VerificationFailure(
                    "EXECUTABLE_IDENTITY",
                    "$.environment.git_executable",
                    "multiple Git subprocess postflight checks failed",
                    observed=[
                        f"{type(error).__name__}: {error}"
                        for error in postflight_errors
                    ],
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
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                **stream_arguments,
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
        if owned_guard:
            guard.close()


def _decode_git_path(
    completed: subprocess.CompletedProcess[bytes],
    location: str,
    description: str,
) -> str:
    """Decode one strict, single-line path emitted by Git."""

    if completed.returncode != 0:
        raise VerificationFailure(
            "GIT_METADATA_OVERRIDE",
            location,
            f"cannot resolve {description}",
            observed=completed.stderr.decode("utf-8", errors="replace").strip(),
        )
    try:
        rendered = completed.stdout.decode("utf-8", errors="strict").rstrip("\r\n")
    except UnicodeDecodeError as exc:
        raise VerificationFailure(
            "GIT_METADATA_OVERRIDE",
            location,
            f"{description} is not valid UTF-8: {exc}",
        ) from exc
    if not rendered or "\n" in rendered or "\r" in rendered:
        raise VerificationFailure(
            "GIT_METADATA_OVERRIDE",
            location,
            f"Git returned a malformed path for {description}",
        )
    return rendered


def _lexical_git_path(repo_root: Path, emitted: str) -> Path:
    """Make a Git-emitted path absolute without following reparse components."""

    candidate = Path(emitted)
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    return Path(os.path.abspath(os.fspath(candidate)))


def _git_metadata_roots(
    repo_root: Path,
    *,
    git_guard: _WindowsExecutableGuard | None = None,
) -> tuple[Path, ...]:
    """Resolve admin/common roots locally, without a recursive Git subprocess."""

    del git_guard  # The local parser deliberately performs no Git execution.
    worktree_root = Path(repo_root).resolve(strict=True)
    dot_git = worktree_root / ".git"
    try:
        metadata = dot_git.lstat()
    except OSError as exc:
        raise VerificationFailure(
            "GIT_METADATA_OVERRIDE",
            str(dot_git),
            f"cannot inspect the Git administrative entry: {exc}",
        ) from exc
    if _is_link_or_reparse(dot_git):
        raise VerificationFailure(
            "GIT_METADATA_OVERRIDE",
            str(dot_git),
            "the Git administrative entry is reparse-mediated",
        )
    if stat.S_ISDIR(metadata.st_mode):
        admin = dot_git
    elif stat.S_ISREG(metadata.st_mode):
        try:
            raw, _identity = _open_stable_regular_file(dot_git)
            pointer = raw.decode("utf-8", errors="strict")
        except (OSError, UnicodeDecodeError) as exc:
            raise VerificationFailure(
                "GIT_METADATA_OVERRIDE",
                str(dot_git),
                f"cannot parse the linked-worktree Git pointer safely: {exc}",
            ) from exc
        match = re.fullmatch(r"gitdir: ([^\r\n]+)\n", pointer)
        if match is None:
            raise VerificationFailure(
                "GIT_METADATA_OVERRIDE",
                str(dot_git),
                "linked-worktree Git pointer is not one strict gitdir line",
            )
        admin = _lexical_git_path(worktree_root, match.group(1))
    else:
        raise VerificationFailure(
            "GIT_METADATA_OVERRIDE",
            str(dot_git),
            "the Git administrative entry is neither a directory nor a regular pointer file",
        )
    admin = _require_nonreparse_directory(admin, "Git administrative root")

    commondir_path = admin / "commondir"
    try:
        raw_common, _identity = _open_stable_regular_file(commondir_path)
    except FileNotFoundError:
        common = admin
    except OSError as exc:
        raise VerificationFailure(
            "GIT_METADATA_OVERRIDE",
            str(commondir_path),
            f"cannot parse the Git common-directory pointer safely: {exc}",
        ) from exc
    else:
        try:
            rendered_common = raw_common.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise VerificationFailure(
                "GIT_METADATA_OVERRIDE",
                str(commondir_path),
                "Git common-directory pointer is not UTF-8",
            ) from exc
        if re.fullmatch(r"[^\r\n]+\n", rendered_common) is None:
            raise VerificationFailure(
                "GIT_METADATA_OVERRIDE",
                str(commondir_path),
                "Git common-directory pointer is not one strict path line",
            )
        common = _lexical_git_path(admin, rendered_common[:-1])
        common = _require_nonreparse_directory(common, "Git common root")
    return tuple(dict.fromkeys((admin, common)))


def _git_metadata_path(
    repo_root: Path,
    relative: str,
    *,
    git_guard: _WindowsExecutableGuard | None = None,
    roots: tuple[Path, ...] | None = None,
) -> Path:
    active_roots = (
        _git_metadata_roots(repo_root, git_guard=git_guard)
        if roots is None
        else roots
    )
    return active_roots[-1] / Path(*PurePosixPath(relative).parts)


def _require_nonreparse_git_metadata_path(
    path: Path,
    roots: tuple[Path, ...],
    relative: str,
) -> None:
    """Reject reparse points at an admin root or any existing child component."""

    candidates: list[Path] = []
    for root in roots:
        try:
            path.relative_to(root)
        except ValueError:
            continue
        candidates.append(root)
    if not candidates:
        raise VerificationFailure(
            "GIT_METADATA_OVERRIDE",
            str(path),
            f"controlled Git metadata path {relative!r} is outside Git admin roots",
        )
    anchor = max(candidates, key=lambda candidate: len(candidate.parts))
    current = anchor
    components = [anchor]
    for part in path.relative_to(anchor).parts:
        current /= part
        components.append(current)
    for component in components:
        try:
            component.lstat()
        except FileNotFoundError:
            break
        except OSError as exc:
            raise VerificationFailure(
                "GIT_METADATA_OVERRIDE",
                str(component),
                f"cannot inspect Git metadata component for {relative!r}: {exc}",
            ) from exc
        if _is_link_or_reparse(component):
            raise VerificationFailure(
                "GIT_METADATA_OVERRIDE",
                str(component),
                f"Git metadata override {relative!r} is reparse-mediated",
            )


def _reject_git_metadata_overrides(
    repo_root: Path,
    *,
    git_guard: _WindowsExecutableGuard | None = None,
    expected_roots: tuple[Path, ...] | None = None,
) -> tuple[Path, ...]:
    """Reject persistent metadata that can replace object or ancestry identity."""

    roots = _git_metadata_roots(repo_root, git_guard=git_guard)
    if expected_roots is not None and roots != expected_roots:
        raise VerificationFailure(
            "GIT_METADATA_OVERRIDE",
            "$repository:.git",
            "Git administrative roots changed across one subprocess",
            expected=[str(path) for path in expected_roots],
            observed=[str(path) for path in roots],
        )
    for relative in (
        "info/grafts",
        "shallow",
        "objects/info/alternates",
        "objects/info/http-alternates",
    ):
        for root in roots:
            _require_nonreparse_git_metadata_path(
                root / Path(*PurePosixPath(relative).parts),
                roots,
                relative,
            )
        path = _git_metadata_path(
            repo_root,
            relative,
            git_guard=git_guard,
            roots=roots,
        )
        _require_nonreparse_git_metadata_path(path, roots, relative)
        try:
            raw, _identity = _open_stable_regular_file(path)
        except FileNotFoundError:
            continue
        except OSError as exc:
            raise VerificationFailure(
                "GIT_METADATA_OVERRIDE",
                str(path),
                f"cannot read Git identity metadata safely: {exc}",
            ) from exc
        _require_nonreparse_git_metadata_path(path, roots, relative)
        if raw:
            raise VerificationFailure(
                "GIT_METADATA_OVERRIDE",
                str(path),
                "nonempty Git ancestry/object redirection metadata is forbidden",
                expected="absent or empty file",
                observed={
                    "byte_count": len(raw),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                },
            )
    return roots


def _git_top_level(repo_root: Path) -> Path:
    completed = _git(repo_root, "rev-parse", "--show-toplevel")
    if completed.returncode != 0:
        raise VerificationFailure(
            "SOURCE_REVISION_NOT_FOUND",
            "$repository",
            "repository root is not a Git worktree",
            observed=completed.stderr.decode("utf-8", errors="replace").strip(),
        )
    try:
        top = Path(
            completed.stdout.decode("utf-8", errors="strict").strip()
        ).resolve()
    except (UnicodeDecodeError, OSError) as exc:
        raise VerificationFailure(
            "SOURCE_REVISION_NOT_FOUND",
            "$repository",
            f"cannot resolve Git top level: {exc}",
        ) from exc
    expected = Path(repo_root).resolve()
    if os.path.normcase(str(top)) != os.path.normcase(str(expected)):
        raise VerificationFailure(
            "SOURCE_REVISION_NOT_FOUND",
            "$repository",
            "repo_root must be the resolved Git top level",
            expected=str(top),
            observed=str(expected),
        )
    return top


def _resolve_current_head(repo_root: Path) -> str:
    """Resolve symbolic HEAD once to one exact full commit identity."""

    completed = _git(
        repo_root,
        "rev-parse",
        "--verify",
        "--end-of-options",
        "HEAD^{commit}",
    )
    if completed.returncode != 0:
        raise VerificationFailure(
            "SOURCE_REVISION_NOT_FOUND",
            "$repository:HEAD",
            "cannot resolve current HEAD to a commit",
            observed=completed.stderr.decode("utf-8", errors="replace").strip(),
        )
    try:
        head_revision = completed.stdout.decode("ascii", errors="strict").strip()
    except UnicodeDecodeError as exc:
        raise VerificationFailure(
            "SOURCE_REVISION_NOT_FOUND",
            "$repository:HEAD",
            "current HEAD identity is not strict ASCII",
        ) from exc
    if re.fullmatch(r"[0-9a-f]{40}", head_revision) is None:
        raise VerificationFailure(
            "SOURCE_REVISION_NOT_FOUND",
            "$repository:HEAD",
            "current HEAD did not resolve to one lowercase full commit ID",
            observed=head_revision,
        )
    return head_revision


def _source_revision_governed_path_issues(
    repo_root: Path,
    source_revision: str,
    current_inputs: dict[str, Any],
    *,
    test_fixture: bool = False,
) -> list[VerificationIssue]:
    """Compare the governed tree at *source_revision* with current discovery."""

    completed = _git(
        repo_root,
        "--literal-pathspecs",
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        source_revision,
    )
    if completed.returncode != 0:
        return [
            _issue(
                "SOURCE_REVISION_NOT_FOUND",
                "$.source_revision",
                "cannot enumerate the source revision tree",
                observed=completed.stderr.decode("utf-8", errors="replace").strip(),
            )
        ]
    if completed.stdout and not completed.stdout.endswith(b"\0"):
        return [
            _issue(
                "SOURCE_BLOB_TYPE",
                "$.source_revision",
                "source tree enumeration is not NUL terminated",
            )
        ]

    entries: dict[str, tuple[bytes, bytes, bytes]] = {}
    issues: list[VerificationIssue] = []
    records = completed.stdout.split(b"\0")
    if records and records[-1] == b"":
        records.pop()
    for index, record in enumerate(records):
        try:
            header, raw_path = record.split(b"\t", 1)
            mode, object_type, object_id = header.split(b" ", 2)
            relative = raw_path.decode("utf-8", errors="strict")
        except (ValueError, UnicodeDecodeError) as exc:
            issues.append(
                _issue(
                    "SOURCE_BLOB_TYPE",
                    f"$.source_revision.tree[{index}]",
                    f"cannot parse source tree entry: {exc}",
                )
            )
            continue
        path_identity = PurePosixPath(relative)
        if (
            not relative
            or "\\" in relative
            or path_identity.is_absolute()
            or any(part in {"", ".", ".."} for part in path_identity.parts)
        ):
            issues.append(
                _issue(
                    "SOURCE_BLOB_TYPE",
                    relative or f"$.source_revision.tree[{index}]",
                    "source tree path is not normalized repository-relative POSIX text",
                )
            )
            continue
        if relative in entries:
            issues.append(
                _issue(
                    "SOURCE_BLOB_TYPE",
                    relative,
                    "source tree enumeration repeated one path identity",
                )
            )
            continue
        manuscript_prefix = f"{_MANUSCRIPT_RELATIVE}/"
        if (
            relative.casefold().startswith(manuscript_prefix.casefold())
            and not relative.startswith(manuscript_prefix)
        ):
            issues.append(
                _issue(
                    "UNEXPECTED_GOVERNED_PATH",
                    relative,
                    "source revision uses noncanonical casing for the governed manuscript namespace",
                    expected=manuscript_prefix,
                    observed=relative,
                )
            )
        entries[relative] = (mode, object_type, object_id)

    try:
        policy = _load_manifest_policy(
            repo_root,
            test_fixture=test_fixture,
        )
    except VerificationFailure as exc:
        issues.append(
            _issue(
                exc.code,
                exc.location,
                str(exc),
                expected=exc.expected,
                observed=exc.observed,
            )
        )
        return issues

    selected = set(_EXACT_REQUIRED_PATHS)
    selected.update(
        relative
        for relative in _STYLE_CANDIDATES
        if relative in entries
    )
    selected.update(
        relative
        for relative in entries
        if relative.startswith(f"{_MANUSCRIPT_RELATIVE}/")
        and relative.endswith(".tex")
    )
    selected.update(
        relative
        for relative in entries
        if relative.startswith(f"{_TESTS_RELATIVE}/")
        and PurePosixPath(relative).name.startswith("test_")
        and PurePosixPath(relative).suffix == ".py"
    )
    declared_bound = policy.get("bound_paths")
    if isinstance(declared_bound, list):
        selected.update(declared_bound)

    if not any(relative in entries for relative in _STYLE_CANDIDATES):
        issues.append(
            _issue(
                "SOURCE_BLOB_MISSING",
                "|".join(_STYLE_CANDIDATES),
                "neither style candidate exists at the source revision",
            )
        )

    for relative in sorted(selected):
        entry = entries.get(relative)
        if entry is None:
            issues.append(
                _issue(
                    "SOURCE_BLOB_MISSING",
                    relative,
                    "governed policy path is absent at the source revision",
                )
            )
            continue
        mode, object_type, _object_id = entry
        if object_type != b"blob" or mode not in {b"100644", b"100755"}:
            issues.append(
                _issue(
                    "SOURCE_BLOB_TYPE",
                    relative,
                    "source governed entry is not a regular Git blob",
                    expected="100644 or 100755 blob",
                    observed=(
                        f"{mode.decode(errors='replace')} "
                        f"{object_type.decode(errors='replace')}"
                    ),
                )
            )

    exclusions = tuple(policy.get("explicit_exclusions", []))
    for relative in sorted(entries):
        if not (
            relative == _MANUSCRIPT_RELATIVE
            or relative.startswith(f"{_MANUSCRIPT_RELATIVE}/")
        ):
            continue
        if relative not in selected and not _matches_exclusion(relative, exclusions):
            issues.append(
                _issue(
                    "UNEXPECTED_GOVERNED_PATH",
                    relative,
                    "source revision contains an undeclared governed path",
                )
            )

    folded: dict[str, str] = {}
    for relative in sorted(selected):
        other = folded.get(relative.casefold())
        if other is not None and other != relative:
            issues.append(
                _issue(
                    "SOURCE_BLOB_TYPE",
                    relative,
                    f"source governed path case-fold collides with {other}",
                )
            )
        folded[relative.casefold()] = relative

    current_paths = set(current_inputs)
    if selected != current_paths:
        issues.append(
            _issue(
                "MANIFEST_PATH_SET_MISMATCH",
                "$.manifest.bound_inputs",
                "source-revision and independently discovered governed path sets differ",
                expected=sorted(selected),
                observed=sorted(current_paths),
            )
        )
    return issues


def _source_binding_issues(
    repo_root: Path,
    source_revision: Any,
    current_manifest: dict[str, Any],
    stored_manifest: dict[str, Any] | None = None,
    *,
    test_fixture: bool = False,
) -> list[VerificationIssue]:
    issues: list[VerificationIssue] = []
    active_evidence = _ACTIVE_RUN_EVIDENCE.get()
    active_root_matches = (
        active_evidence is not None
        and os.path.normcase(active_evidence.repo_root)
        == os.path.normcase(str(Path(repo_root).resolve(strict=True)))
    )
    if not isinstance(source_revision, str) or re.fullmatch(
        r"[0-9a-f]{40}", source_revision
    ) is None:
        return [
            _issue(
                "SOURCE_REVISION_FORMAT",
                "$.source_revision",
                "source revision must be one full lowercase 40-hex commit ID",
                observed=source_revision,
            )
        ]
    try:
        _git_top_level(repo_root)
        _reject_git_metadata_overrides(repo_root)
        head_revision = (
            active_evidence.head_revision
            if active_root_matches
            else _resolve_current_head(repo_root)
        )
    except VerificationFailure as exc:
        return [
            _issue(
                exc.code,
                exc.location,
                str(exc),
                expected=exc.expected,
                observed=exc.observed,
            )
        ]
    resolved = _git(repo_root, "rev-parse", "--verify", f"{source_revision}^{{commit}}")
    if resolved.returncode != 0:
        return [
            _issue(
                "SOURCE_REVISION_NOT_FOUND",
                "$.source_revision",
                "recorded source revision does not resolve to a commit",
                observed=source_revision,
            )
        ]
    resolved_text = resolved.stdout.decode("ascii", errors="replace").strip().lower()
    if resolved_text != source_revision:
        issues.append(
            _issue(
                "SOURCE_REVISION_NOT_FOUND",
                "$.source_revision",
                "recorded revision does not resolve to itself",
                expected=source_revision,
                observed=resolved_text,
            )
        )
        return issues
    ancestry = _git(
        repo_root,
        "merge-base",
        "--is-ancestor",
        source_revision,
        head_revision,
    )
    if ancestry.returncode != 0:
        issues.append(
            _issue(
                "SOURCE_REVISION_NOT_ANCESTOR",
                "$.source_revision",
                "recorded source revision is not an ancestor of current HEAD",
                observed=source_revision,
            )
        )

    current_inputs = current_manifest.get("bound_inputs")
    if not isinstance(current_inputs, dict):
        return issues + [
            _issue(
                "MANIFEST_ENTRY_MISMATCH",
                "$.manifest.bound_inputs",
                "current manifest has no bound-input mapping",
            )
        ]
    issues.extend(
        _source_revision_governed_path_issues(
            repo_root,
            source_revision,
            current_inputs,
            test_fixture=test_fixture,
        )
    )
    stored_inputs: dict[str, Any] | None = None
    if stored_manifest is not None:
        candidate = stored_manifest.get("bound_inputs")
        if isinstance(candidate, dict):
            stored_inputs = candidate
            if set(candidate) != set(current_inputs):
                issues.append(
                    _issue(
                        "MANIFEST_PATH_SET_MISMATCH",
                        "$.manifest.bound_inputs",
                        "stored and independently discovered path sets differ",
                        expected=sorted(current_inputs),
                        observed=sorted(candidate),
                    )
                )
        else:
            issues.append(
                _issue(
                    "MANIFEST_ENTRY_MISMATCH",
                    "$.manifest.bound_inputs",
                    "stored manifest has no bound-input mapping",
                )
            )

    for relative in sorted(current_inputs):
        tree = _git(
            repo_root,
            "--literal-pathspecs",
            "ls-tree",
            "-z",
            source_revision,
            "--",
            relative,
        )
        if tree.returncode != 0 or not tree.stdout:
            issues.append(
                _issue(
                    "SOURCE_BLOB_MISSING",
                    relative,
                    "governed path has no Git object at the source revision",
                )
            )
            continue
        if not tree.stdout.endswith(b"\0") or tree.stdout.count(b"\0") != 1:
            issues.append(
                _issue(
                    "SOURCE_BLOB_TYPE",
                    relative,
                    "source tree lookup did not return exactly one NUL-terminated record",
                )
            )
            continue
        record = tree.stdout[:-1]
        try:
            header, recorded_path = record.split(b"\t", 1)
            mode, object_type, object_id = header.split(b" ", 2)
            recorded_relative = recorded_path.decode("utf-8", errors="strict")
        except (ValueError, UnicodeDecodeError) as exc:
            issues.append(
                _issue(
                    "SOURCE_BLOB_TYPE",
                    relative,
                    f"cannot parse source tree entry: {exc}",
                )
            )
            continue
        if recorded_relative != relative:
            issues.append(
                _issue(
                    "SOURCE_BLOB_MISSING",
                    relative,
                    "Git tree returned a different path identity",
                    expected=relative,
                    observed=recorded_relative,
                )
            )
            continue
        if object_type != b"blob" or mode not in {b"100644", b"100755"}:
            issues.append(
                _issue(
                    "SOURCE_BLOB_TYPE",
                    relative,
                    "source object is not a regular Git blob",
                    expected="100644 or 100755 blob",
                    observed=f"{mode.decode(errors='replace')} {object_type.decode(errors='replace')}",
                )
            )
            continue
        blob = _git(repo_root, "cat-file", "blob", object_id.decode("ascii"))
        if blob.returncode != 0:
            issues.append(
                _issue(
                    "SOURCE_BLOB_MISSING",
                    relative,
                    "cannot read source blob bytes",
                )
            )
            continue
        blob_entry = {
            "byte_count": len(blob.stdout),
            "sha256": hashlib.sha256(blob.stdout).hexdigest(),
        }
        current_entry = current_inputs.get(relative)
        if current_entry != blob_entry:
            issues.append(
                _issue(
                    "SOURCE_BLOB_MISMATCH",
                    relative,
                    "current retained raw bytes differ from the source-revision blob",
                    expected=blob_entry,
                    observed=current_entry,
                )
            )
        if stored_inputs is not None and stored_inputs.get(relative) != current_inputs.get(
            relative
        ):
            issues.append(
                _issue(
                    "MANIFEST_ENTRY_MISMATCH",
                    relative,
                    "stored manifest entry differs from current raw-byte entry",
                    expected=current_inputs.get(relative),
                    observed=stored_inputs.get(relative),
                )
            )
    if not active_root_matches:
        try:
            _reject_git_metadata_overrides(repo_root)
            closing_head_revision = _resolve_current_head(repo_root)
            if closing_head_revision != head_revision:
                issues.append(
                    _issue(
                        "SOURCE_REVISION_NOT_ANCESTOR",
                        "$repository:HEAD",
                        "HEAD changed during source-binding verification",
                        expected=head_revision,
                        observed=closing_head_revision,
                    )
                )
        except VerificationFailure as exc:
            issues.append(
                _issue(
                    exc.code,
                    exc.location,
                    str(exc),
                    expected=exc.expected,
                    observed=exc.observed,
                )
            )
    return issues


def _require_source_binding(
    repo_root: Path,
    source_revision: str,
    manifest: dict[str, Any],
    *,
    test_fixture: bool = False,
) -> None:
    issues = _source_binding_issues(
        repo_root,
        source_revision,
        manifest,
        test_fixture=test_fixture,
    )
    if issues:
        first = issues[0]
        raise VerificationFailure(
            first.code,
            first.location,
            first.message,
            expected=first.expected,
            observed=first.observed,
        )


def _load_claims_document(
    repo_root: Path,
    protocol_profile: str,
) -> dict[str, Any]:
    path = repo_root / f"{_VERIFICATION_RELATIVE}/claims.json"
    try:
        document = _strict_json_file(path)
    except ValueError as exc:
        raise VerificationFailure(
            "RECOMPUTATION_EXCEPTION",
            f"{_VERIFICATION_RELATIVE}/claims.json",
            str(exc),
        ) from exc
    if not isinstance(document, dict):
        raise VerificationFailure(
            "RECOMPUTATION_EXCEPTION",
            f"{_VERIFICATION_RELATIVE}/claims.json",
            "claims document must be a JSON object",
        )
    declared_profile = document.get("protocol_profile")
    if protocol_profile == SYNTHETIC_PROTOCOL_PROFILE:
        if document.get("schema_version") != "1.0":
            raise VerificationFailure(
                "PROTOCOL_PROFILE_MISMATCH",
                "claims.json:schema_version",
                "synthetic fixture claims schema_version must be 1.0",
                expected="1.0",
                observed=document.get("schema_version"),
            )
        if declared_profile != SYNTHETIC_PROTOCOL_PROFILE:
            raise VerificationFailure(
                "PROTOCOL_PROFILE_MISMATCH",
                "claims.json:protocol_profile",
                "synthetic fixtures require an independent matching claims marker",
                expected=SYNTHETIC_PROTOCOL_PROFILE,
                observed=declared_profile,
            )
        if set(document) != {"schema_version", "protocol_profile", "checks"}:
            raise VerificationFailure(
                "PROTOCOL_PROFILE_MISMATCH",
                "claims.json",
                "synthetic fixture claims must use the closed fixture envelope",
                expected=["checks", "protocol_profile", "schema_version"],
                observed=sorted(document),
            )
    elif protocol_profile == PRODUCTION_PROTOCOL_PROFILE:
        expected_keys = {
            "schema_version",
            "protocol_profile",
            "source_state",
            "inventory_note",
            "claims",
            "supplemental_check_ids",
        }
        if document.get("schema_version") != "2.1":
            raise VerificationFailure(
                "PROTOCOL_PROFILE_MISMATCH",
                "claims.json:schema_version",
                "production claims schema_version must be the frozen 2.1 envelope",
                expected="2.1",
                observed=document.get("schema_version"),
            )
        if (
            set(document) != expected_keys
            or declared_profile != PRODUCTION_PROTOCOL_PROFILE
        ):
            raise VerificationFailure(
                "PROTOCOL_PROFILE_MISMATCH",
                "claims.json",
                "production claims must use the exact frozen top-level envelope",
                expected={
                    "protocol_profile": PRODUCTION_PROTOCOL_PROFILE,
                    "keys": sorted(expected_keys),
                },
                observed={
                    "protocol_profile": declared_profile,
                    "keys": sorted(document),
                },
            )
    else:
        raise VerificationFailure(
            "PROTOCOL_PROFILE_MISMATCH",
            "manifest-policy.json:protocol_profile",
            "unknown protocol profile",
            expected=sorted(_PROTOCOL_PROFILES),
            observed=protocol_profile,
        )
    return document


def _required_check_ids(
    claims_document: dict[str, Any],
    protocol_profile: str,
) -> tuple[str, ...]:
    if protocol_profile == SYNTHETIC_PROTOCOL_PROFILE:
        fixture_checks = claims_document.get("checks")
        if not isinstance(fixture_checks, list) or not fixture_checks:
            raise VerificationFailure(
                "RECOMPUTATION_EXCEPTION",
                "claims.json:checks",
                "fixture checks must be a nonempty list",
            )
        identifiers: list[str] = []
        for index, declaration in enumerate(fixture_checks):
            if not isinstance(declaration, dict) or not isinstance(
                declaration.get("check_id"), str
            ):
                raise VerificationFailure(
                    "RECOMPUTATION_EXCEPTION",
                    f"claims.json:checks[{index}]",
                    "each fixture check needs a string check_id",
                )
            identifiers.append(declaration["check_id"])
        if len(identifiers) != len(set(identifiers)):
            raise VerificationFailure(
                "CHECK_ID_DUPLICATE",
                "claims.json:checks",
                "fixture claims contain duplicate check IDs",
            )
        return tuple(identifiers)

    if protocol_profile != PRODUCTION_PROTOCOL_PROFILE:
        raise VerificationFailure(
            "PROTOCOL_PROFILE_MISMATCH",
            "manifest-policy.json:protocol_profile",
            "check inventory requested for an unknown protocol profile",
            expected=sorted(_PROTOCOL_PROFILES),
            observed=protocol_profile,
        )

    claims = claims_document.get("claims")
    supplemental = claims_document.get("supplemental_check_ids")
    if not isinstance(claims, list) or not isinstance(supplemental, list):
        raise VerificationFailure(
            "RECOMPUTATION_EXCEPTION",
            "claims.json",
            "production claims require claims and supplemental_check_ids lists",
        )
    declared: list[str] = []
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise VerificationFailure(
                "RECOMPUTATION_EXCEPTION",
                f"claims.json:claims[{index}]",
                "claim entry must be an object",
            )
        mapped = claim.get("check_ids", [])
        if not isinstance(mapped, list) or any(not isinstance(item, str) for item in mapped):
            raise VerificationFailure(
                "RECOMPUTATION_EXCEPTION",
                f"claims.json:claims[{index}].check_ids",
                "claim check_ids must be strings",
            )
        declared.extend(mapped)
    if any(not isinstance(item, str) for item in supplemental):
        raise VerificationFailure(
            "RECOMPUTATION_EXCEPTION",
            "claims.json:supplemental_check_ids",
            "supplemental check IDs must be strings",
        )
    declared.extend(supplemental)
    if set(declared) != set(PRODUCTION_CHECK_IDS):
        raise VerificationFailure(
            "RECOMPUTATION_EXCEPTION",
            "claims.json",
            "declared production check IDs do not equal the nonshrinkable 30-check protocol",
            expected=list(PRODUCTION_CHECK_IDS),
            observed=sorted(set(declared)),
        )
    return PRODUCTION_REQUIRED_CHECK_IDS


def _dependency_versions() -> dict[str, str]:
    dependencies = {
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "sympy": sp.__version__,
        "mpmath": mpmath.__version__,
    }
    for name in ("pypdf", "pytest"):
        try:
            dependencies[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            dependencies[name] = "not-installed"
    return dependencies


def _canonical_distribution_name(value: str) -> str:
    """Return the normalized distribution identity used by core metadata."""

    return re.sub(r"[-_.]+", "-", value).casefold()


def _dependency_pins(path: Path | None = None) -> dict[str, str]:
    """Parse the exact six-line, stdlib-only production dependency contract."""

    requirements_path = REQUIREMENTS_PATH if path is None else Path(path)
    if path is None:
        registry = _ACTIVE_GOVERNED_REGISTRY.get()
        if registry is not None:
            relative = f"{_VERIFICATION_RELATIVE}/requirements.txt"
            matching = [
                record.path
                for record in registry.values()
                if record.relative_path == relative
            ]
            if len(matching) != 1:
                raise VerificationFailure(
                    "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
                    relative,
                    "retained registry does not contain exactly one requirements input",
                    expected=1,
                    observed=len(matching),
                )
            requirements_path = matching[0]
    try:
        raw, _identity = _read_registered_or_stable_file(requirements_path)
    except OSError as exc:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            str(requirements_path),
            f"cannot read exact dependency pins through one stable handle: {exc}",
        ) from exc
    if raw.startswith(b"\xef\xbb\xbf") or not raw.endswith(b"\n"):
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            str(requirements_path),
            "dependency pins must be BOM-free text ending in a newline",
        )
    if b"\r" in raw:
        bare_carriage_returns = raw.replace(b"\r\n", b"")
        if b"\r" in bare_carriage_returns or raw.count(b"\r\n") != raw.count(b"\n"):
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                str(requirements_path),
                "dependency pins must use uniform LF or uniform CRLF line endings",
            )
        normalized_raw = raw.replace(b"\r\n", b"\n")
    else:
        normalized_raw = raw
    try:
        text = normalized_raw.decode("ascii", errors="strict")
    except UnicodeDecodeError as exc:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            str(requirements_path),
            "dependency pins must contain ASCII only",
        ) from exc
    lines = text[:-1].split("\n")
    if len(lines) != len(_REQUIRED_DEPENDENCY_NAMES):
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            str(requirements_path),
            "dependency contract must contain exactly six nonblank pin lines",
            expected=len(_REQUIRED_DEPENDENCY_NAMES),
            observed=len(lines),
        )
    pins: dict[str, str] = {}
    for index, line in enumerate(lines, start=1):
        match = _REQUIREMENT_LINE.fullmatch(line)
        if match is None:
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                f"{requirements_path}:{index}",
                "dependency pin must use normalized-name==numeric-exact-version with no whitespace",
                observed=line,
            )
        name = match.group("name")
        version = match.group("version")
        if _canonical_distribution_name(name) != name:
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                f"{requirements_path}:{index}",
                "dependency pin name is not normalized",
                observed=name,
            )
        if name in pins:
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                f"{requirements_path}:{index}",
                "dependency contract repeats one normalized package name",
                observed=name,
            )
        pins[name] = version
    if tuple(pins) != _REQUIRED_DEPENDENCY_NAMES:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            str(requirements_path),
            "dependency contract must contain the exact six names in canonical order",
            expected=list(_REQUIRED_DEPENDENCY_NAMES),
            observed=list(pins),
        )
    return pins


def _find_dependency_spec(name: str) -> Any:
    """Resolve one top-level dependency without invoking meta-path import hooks."""

    return importlib.machinery.PathFinder.find_spec(
        name,
        [str(_FIXED_SITE_PACKAGES)],
    )


def _stable_provenance_file(
    path: Path,
    location: str,
    *,
    containment_root: Path,
    validated_directories: set[str] | None = None,
) -> bytes:
    """Read one regular file under a fixed non-reparse containment root."""

    absolute = Path(os.path.abspath(os.fspath(path)))
    fixed_root = Path(os.path.abspath(os.fspath(containment_root)))
    try:
        relative = absolute.relative_to(fixed_root)
    except ValueError as exc:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            location,
            "dependency provenance path escapes its fixed containment root",
            expected=str(containment_root),
            observed=str(absolute),
        ) from exc
    validated = set() if validated_directories is None else validated_directories
    parent = absolute.parent
    parent_parts = parent.parts
    current = Path(parent_parts[0])
    directories = [current]
    for part in parent_parts[1:]:
        current /= part
        directories.append(current)
    for component in directories:
        identity = os.path.normcase(str(component))
        if identity in validated:
            continue
        try:
            metadata = component.lstat()
        except OSError as exc:
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                location,
                f"dependency provenance component cannot be inspected: {component}",
            ) from exc
        if _is_link_or_reparse(component):
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                location,
                f"dependency provenance is reparse-mediated at {component}",
            )
        if not stat.S_ISDIR(metadata.st_mode):
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                location,
                f"dependency provenance parent is not a directory: {component}",
            )
        validated.add(identity)
    try:
        payload, _identity = _open_stable_regular_file(absolute)
    except OSError as exc:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            location,
            f"dependency provenance file cannot be read safely: {exc}",
        ) from exc
    return payload


def _dependency_record_path(
    distribution: importlib.metadata.Distribution,
    location: str,
) -> tuple[object, Path]:
    """Find the sole dist-info RECORD declared by one distribution."""

    distribution_files = tuple(distribution.files or ())
    candidates = tuple(
        item
        for item in distribution_files
        if PurePosixPath(str(item).replace("\\", "/")).name == "RECORD"
        and ".dist-info" in str(item).replace("\\", "/")
    )
    if len(candidates) != 1:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            location,
            "dependency distribution must expose exactly one dist-info RECORD",
            expected=1,
            observed=len(candidates),
        )
    return candidates[0], Path(distribution.locate_file(candidates[0]))


def _normalized_record_target(
    distribution: importlib.metadata.Distribution,
    raw_path: str,
    location: str,
) -> tuple[Path, str]:
    """Resolve one RECORD path beneath the fixed user base without reparses."""

    normalized_text = raw_path.replace("\\", "/")
    path_identity = PurePosixPath(normalized_text)
    if (
        not raw_path
        or "\\" in raw_path
        or "\x00" in raw_path
        or path_identity.is_absolute()
        or re.match(r"[A-Za-z]:", normalized_text)
        or any(part in {"", "."} for part in path_identity.parts)
    ):
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            location,
            "distribution RECORD contains a malformed path",
            observed=raw_path,
        )
    package_path = importlib.metadata.PackagePath(normalized_text)
    located = Path(os.path.abspath(os.fspath(distribution.locate_file(package_path))))
    user_base = Path(os.path.abspath(os.fspath(_FIXED_USER_BASE)))
    try:
        relative = located.relative_to(user_base).as_posix()
    except ValueError as exc:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            location,
            "distribution RECORD entry escapes the fixed Python user base",
            expected=str(_FIXED_USER_BASE),
            observed=str(located),
        ) from exc
    return located, relative


def _installed_distribution_provenance(
    name: str,
    module_origin: Path,
    distribution: importlib.metadata.Distribution,
    *,
    validated_directories: set[str] | None = None,
    authenticated_files: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Hash every actual file named by one strict RECORD inventory."""

    location = f"$.environment.dependency_provenance.{name}"
    validated = (
        set() if validated_directories is None else validated_directories
    )
    _record_item, record_path = _dependency_record_path(distribution, location)
    fixed_site = Path(os.path.abspath(os.fspath(_FIXED_SITE_PACKAGES)))
    distribution_root = Path(
        os.path.abspath(os.fspath(distribution.locate_file("")))
    )
    if os.path.normcase(str(distribution_root)) != os.path.normcase(str(fixed_site)):
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            location,
            "dependency distribution root is not the exact fixed site-packages",
            expected=str(_FIXED_SITE_PACKAGES),
            observed=str(distribution_root),
        )
    dist_info_value = getattr(distribution, "_path", None)
    if dist_info_value is None:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            location,
            "dependency distribution has no exact dist-info directory identity",
        )
    dist_info = Path(os.path.abspath(os.fspath(dist_info_value)))
    if (
        os.path.normcase(str(dist_info.parent)) != os.path.normcase(str(fixed_site))
        or not dist_info.name.casefold().endswith(".dist-info")
    ):
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            location,
            "dependency dist-info directory is outside exact fixed site-packages",
            expected=str(_FIXED_SITE_PACKAGES),
            observed=str(dist_info),
        )
    record_absolute = Path(os.path.abspath(os.fspath(record_path)))
    if (
        record_absolute.name != "RECORD"
        or os.path.normcase(str(record_absolute.parent))
        != os.path.normcase(str(dist_info))
    ):
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            f"{location}.record_path",
            "selected RECORD is not the exact file inside the authenticated dist-info",
            expected=str(dist_info / "RECORD"),
            observed=str(record_absolute),
        )
    record_bytes = _stable_provenance_file(
        record_absolute,
        f"{location}.record_path",
        containment_root=_FIXED_SITE_PACKAGES,
        validated_directories=validated,
    )
    if record_bytes.startswith(b"\xef\xbb\xbf"):
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            f"{location}.record_path",
            "distribution RECORD may not contain a UTF-8 BOM",
        )
    try:
        record_text = record_bytes.decode("utf-8", errors="strict")
        rows = list(csv.reader(record_text.splitlines()))
    except (UnicodeDecodeError, csv.Error) as exc:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            f"{location}.record_path",
            f"distribution RECORD cannot be parsed strictly: {exc}",
        ) from exc
    if not rows:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            f"{location}.record_path",
            "distribution RECORD is empty",
        )

    entries: list[dict[str, Any]] = []
    identities: dict[str, str] = {}
    actual_paths: dict[str, dict[str, Any]] = {}
    total_bytes = 0
    for index, row in enumerate(rows):
        row_location = f"{location}.RECORD[{index}]"
        if len(row) != 3:
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                row_location,
                "distribution RECORD row must contain exactly three fields",
                observed=len(row),
            )
        raw_path, declared_hash, declared_size = row
        actual_path, user_relative = _normalized_record_target(
            distribution,
            raw_path,
            row_location,
        )
        folded = user_relative.casefold()
        previous = identities.get(folded)
        if previous is not None:
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                row_location,
                "distribution RECORD repeats or case-fold-collides one file identity",
                expected=previous,
                observed=user_relative,
            )
        identities[folded] = user_relative
        payload = _stable_provenance_file(
            actual_path,
            row_location,
            containment_root=_FIXED_USER_BASE,
            validated_directories=validated,
        )
        actual_sha256 = hashlib.sha256(payload).hexdigest()
        if declared_size:
            try:
                expected_size = int(declared_size)
            except ValueError as exc:
                raise VerificationFailure(
                    "EXECUTABLE_IDENTITY",
                    row_location,
                    "distribution RECORD size is not a nonnegative integer",
                    observed=declared_size,
                ) from exc
            if expected_size < 0 or expected_size != len(payload):
                raise VerificationFailure(
                    "EXECUTABLE_IDENTITY",
                    row_location,
                    "actual dependency byte count disagrees with RECORD",
                    expected=expected_size,
                    observed=len(payload),
                )
        if declared_hash:
            try:
                algorithm, encoded_digest = declared_hash.split("=", 1)
            except ValueError as exc:
                raise VerificationFailure(
                    "EXECUTABLE_IDENTITY",
                    row_location,
                    "distribution RECORD hash is malformed",
                    observed=declared_hash,
                ) from exc
            if (
                re.fullmatch(r"[a-z0-9_]+", algorithm) is None
                or re.fullmatch(r"[A-Za-z0-9_-]+", encoded_digest) is None
            ):
                raise VerificationFailure(
                    "EXECUTABLE_IDENTITY",
                    row_location,
                    "distribution RECORD hash has a malformed algorithm or URL-safe digest",
                    observed=declared_hash,
                )
            try:
                declared_algorithm_digest = hashlib.new(algorithm, payload).digest()
            except (TypeError, ValueError) as exc:
                raise VerificationFailure(
                    "EXECUTABLE_IDENTITY",
                    row_location,
                    "distribution RECORD declares an unsupported hash algorithm",
                    observed=algorithm,
                ) from exc
            actual_encoded = base64.urlsafe_b64encode(
                declared_algorithm_digest
            ).decode("ascii").rstrip("=")
            if len(encoded_digest) != len(actual_encoded):
                raise VerificationFailure(
                    "EXECUTABLE_IDENTITY",
                    row_location,
                    "distribution RECORD hash digest has the wrong encoded length",
                    expected=len(actual_encoded),
                    observed=len(encoded_digest),
                )
            if actual_encoded != encoded_digest:
                raise VerificationFailure(
                    "EXECUTABLE_IDENTITY",
                    row_location,
                    "actual dependency bytes disagree with the declared RECORD hash",
                    expected=encoded_digest,
                    observed=actual_encoded,
                )
        entry = {
            "path": user_relative,
            "byte_count": len(payload),
            "sha256": actual_sha256,
        }
        entries.append(entry)
        actual_paths[os.path.normcase(str(actual_path))] = entry
        total_bytes += len(payload)

    module_absolute = Path(os.path.abspath(os.fspath(module_origin)))
    try:
        module_absolute.relative_to(fixed_site)
    except ValueError as exc:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            f"{location}.module_origin",
            "resolved dependency module origin escapes fixed site-packages",
            expected=str(_FIXED_SITE_PACKAGES),
            observed=str(module_absolute),
        ) from exc
    module_entry = actual_paths.get(os.path.normcase(str(module_absolute)))
    if module_entry is None:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            f"{location}.module_origin",
            "resolved dependency module origin is absent from its RECORD inventory",
            observed=str(module_absolute),
        )
    record_entry = actual_paths.get(
        os.path.normcase(str(record_absolute))
    )
    if record_entry is None:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            f"{location}.record_path",
            "the selected RECORD file does not inventory itself",
            observed=str(record_path),
        )
    entries.sort(key=lambda item: item["path"])
    if authenticated_files is not None:
        authenticated_files.update(copy.deepcopy(actual_paths))
    return {
        "installed": True,
        "version": distribution.version,
        "module_origin": str(module_absolute),
        "module_origin_sha256": module_entry["sha256"],
        "record_path": str(record_absolute),
        "record_sha256": hashlib.sha256(record_bytes).hexdigest(),
        "record_byte_count": len(record_bytes),
        "record_entry_count": len(entries),
        "actual_tree_sha256": hashlib.sha256(
            canonical_json_bytes(entries)
        ).hexdigest(),
        "actual_file_count": len(entries),
        "actual_byte_count": total_bytes,
    }


def _dependency_provenance(
    *,
    verify_imported_versions: bool = True,
    authenticated_files: dict[str, dict[str, dict[str, Any]]] | None = None,
) -> dict[str, dict[str, Any]]:
    """Bind exact module origins and stable actual bytes for each dependency."""

    if type(verify_imported_versions) is not bool:
        raise TypeError("verify_imported_versions must be an explicit bool")
    provenance: dict[str, dict[str, Any]] = {}
    validated_directories: set[str] = set()
    pinned_versions = _dependency_pins()
    expected_versions = _dependency_versions() if verify_imported_versions else None
    fixed_site = Path(os.path.abspath(os.fspath(_FIXED_SITE_PACKAGES)))
    try:
        discovered_distributions = tuple(
            importlib.metadata.distributions(path=[str(fixed_site)])
        )
    except (OSError, TypeError, ValueError) as exc:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            "$.environment.dependency_provenance",
            f"cannot enumerate the exact fixed dependency metadata root: {exc}",
        ) from exc

    for name in _REQUIRED_DEPENDENCY_NAMES:
        canonical_name = _canonical_distribution_name(name)
        matching_distributions: list[importlib.metadata.Distribution] = []
        for distribution in discovered_distributions:
            try:
                declared_name = distribution.metadata["Name"]
            except (KeyError, TypeError, ValueError) as exc:
                raise VerificationFailure(
                    "EXECUTABLE_IDENTITY",
                    f"$.environment.dependency_provenance.{name}",
                    "dependency distribution metadata has no strict Name identity",
                ) from exc
            if not isinstance(declared_name, str) or not declared_name:
                raise VerificationFailure(
                    "EXECUTABLE_IDENTITY",
                    f"$.environment.dependency_provenance.{name}",
                    "dependency distribution metadata Name is malformed",
                    observed=declared_name,
                )
            if _canonical_distribution_name(declared_name) == canonical_name:
                matching_distributions.append(distribution)
        spec = _find_dependency_spec(name)
        if spec is None or spec.origin is None:
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                f"$.environment.dependency_provenance.{name}",
                "required production dependency module is not importable",
                expected="installed module and exactly one matching dist-info",
                observed={"matching_dist_info_count": len(matching_distributions)},
            )
        if len(matching_distributions) != 1:
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                f"$.environment.dependency_provenance.{name}",
                "installed dependency must have exactly one matching dist-info identity in fixed site-packages",
                expected=1,
                observed=len(matching_distributions),
            )
        installed = _installed_distribution_provenance(
            name,
            Path(spec.origin),
            matching_distributions[0],
            validated_directories=validated_directories,
            authenticated_files=(
                authenticated_files.setdefault(name, {})
                if authenticated_files is not None
                else None
            ),
        )
        pinned_version = pinned_versions[name]
        if installed["version"] != pinned_version:
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                f"$.environment.dependency_provenance.{name}.version",
                "dependency metadata version does not equal the exact requirements pin",
                expected=pinned_version,
                observed=installed["version"],
            )
        expected_version = (
            expected_versions.get(name)
            if expected_versions is not None
            else None
        )
        if (
            expected_versions is not None
            and installed["version"] != expected_version
        ):
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                f"$.environment.dependency_provenance.{name}.version",
                "dependency metadata version disagrees with the imported dependency version",
                expected=expected_version,
                observed=installed["version"],
            )
        provenance[name] = installed
    bootstrap_provenance = globals().get(
        "_PREIMPORT_DEPENDENCY_PROVENANCE"
    )
    if (
        verify_imported_versions
        and bootstrap_provenance is not None
        and provenance != bootstrap_provenance
    ):
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            "$.environment.dependency_provenance",
            "dependency bytes differ from the stdlib-only pre-import M0 snapshot",
            expected=bootstrap_provenance,
            observed=provenance,
        )
    return provenance


def _require_dependency_import_window(
    before: dict[str, dict[str, Any]],
    after: dict[str, dict[str, Any]],
    imported_modules: dict[str, Any],
) -> None:
    """Bind imported module origins and versions to the pre-import M0 bytes."""

    if before != after:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            "$.environment.dependency_provenance",
            "dependency bytes changed across the third-party import window",
            expected=before,
            observed=after,
        )
    imported_versions = _dependency_versions()
    for name, provenance in before.items():
        module = imported_modules.get(name)
        if module is None:
            if name in {"pypdf", "pytest"}:
                if imported_versions.get(name) != provenance["version"]:
                    raise VerificationFailure(
                        "EXECUTABLE_IDENTITY",
                        f"$.environment.dependency_provenance.{name}.version",
                        "metadata-only dependency version differs from pre-import M0",
                        expected=provenance["version"],
                        observed=imported_versions.get(name),
                    )
                continue
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                f"$.environment.dependency_provenance.{name}",
                "runtime dependency was not imported for origin validation",
            )
        module_spec = getattr(module, "__spec__", None)
        module_origin = getattr(module_spec, "origin", None)
        if not isinstance(module_origin, str):
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                f"$.environment.dependency_provenance.{name}.module_origin",
                "imported dependency has no exact module origin",
                observed=module_origin,
            )
        observed_origin = str(Path(os.path.abspath(module_origin)))
        expected_origin = provenance["module_origin"]
        if os.path.normcase(observed_origin) != os.path.normcase(expected_origin):
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                f"$.environment.dependency_provenance.{name}.module_origin",
                "imported dependency origin differs from pre-import M0",
                expected=expected_origin,
                observed=observed_origin,
            )
        if imported_versions.get(name) != provenance["version"]:
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                f"$.environment.dependency_provenance.{name}.version",
                "imported dependency version differs from pre-import M0",
                expected=provenance["version"],
                observed=imported_versions.get(name),
            )


class _AuthenticatedSiteLoader(importlib.abc.Loader):
    """Execute one delegated site module while its exact M0 file is locked."""

    def __init__(
        self,
        delegate: Any,
        origin: Path,
        expected: dict[str, Any],
        fullname: str,
    ) -> None:
        self._delegate = delegate
        self._origin = origin
        self._expected = expected
        self._fullname = fullname
        self._guard: _WindowsExecutableGuard | None = None
        self._before: dict[str, Any] | None = None

    def __getattr__(self, name: str) -> Any:
        return getattr(self._delegate, name)

    def create_module(self, spec: Any) -> Any:
        self._acquire_guard()
        creator = getattr(self._delegate, "create_module", None)
        try:
            return None if creator is None else creator(spec)
        except BaseException:
            self._close_guard()
            raise

    def exec_module(self, module: Any) -> None:
        self._acquire_guard()
        try:
            self._delegate.exec_module(module)
            after = self._guard.snapshot()
            if after != self._before:
                raise ImportError(
                    f"authenticated module {self._fullname!r} changed during execution"
                )
        finally:
            self._close_guard()

    def _acquire_guard(self) -> None:
        if self._guard is not None:
            return
        guard = _WindowsExecutableGuard(
            self._origin,
            f"authenticated module {self._fullname}",
        )
        try:
            before = guard.snapshot()
            if (
                before["byte_count"] != self._expected["byte_count"]
                or before["sha256"] != self._expected["sha256"]
            ):
                raise ImportError(
                    f"authenticated module {self._fullname!r} differs from pre-import M0"
                )
        except BaseException:
            guard.close()
            raise
        self._guard = guard
        self._before = before

    def _close_guard(self) -> None:
        guard = self._guard
        self._guard = None
        self._before = None
        if guard is not None:
            guard.close()


class _AuthenticatedSiteFinder(importlib.abc.MetaPathFinder):
    """Block execution of fixed-site modules outside authenticated inventories."""

    def __init__(self, allowed_files: dict[str, dict[str, Any]]) -> None:
        self._allowed_files = copy.deepcopy(allowed_files)
        self._fixed_site = Path(os.path.abspath(os.fspath(_FIXED_SITE_PACKAGES)))

    def find_spec(
        self,
        fullname: str,
        path: Any = None,
        target: Any = None,
    ) -> Any:
        spec = importlib.machinery.PathFinder.find_spec(fullname, path, target)
        if spec is None:
            return None
        origin = getattr(spec, "origin", None)
        if not isinstance(origin, str) or origin in {"built-in", "frozen"}:
            return spec
        absolute = Path(os.path.abspath(origin))
        try:
            absolute.relative_to(self._fixed_site)
        except ValueError:
            return spec
        identity = os.path.normcase(str(absolute))
        expected = self._allowed_files.get(identity)
        if expected is None:
            raise ImportError(
                "blocked unauthenticated fixed-site import "
                f"{fullname!r} from {absolute}"
            )
        if spec.loader is None or not hasattr(spec.loader, "exec_module"):
            raise ImportError(
                f"authenticated fixed-site import {fullname!r} has no executable loader"
            )
        spec.loader = _AuthenticatedSiteLoader(
            spec.loader,
            absolute,
            expected,
            fullname,
        )
        return spec


def _require_nonreparse_directory(path: Path, role: str) -> Path:
    """Require every existing component to be a non-reparse directory."""

    absolute = Path(os.path.abspath(os.fspath(path)))
    parts = absolute.parts
    current = Path(parts[0])
    for part in parts[1:]:
        current /= part
        try:
            metadata = current.lstat()
        except OSError as exc:
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                str(current),
                f"cannot inspect {role} directory component: {exc}",
            ) from exc
        if _is_link_or_reparse(current) or not stat.S_ISDIR(metadata.st_mode):
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                str(current),
                f"{role} directory is reparse-mediated or non-directory",
            )
    return absolute


def _require_empty_nonreparse_directory(path: Path, role: str) -> None:
    """Require a component-checked directory to have an empty inventory."""

    absolute = _require_nonreparse_directory(path, role)
    try:
        entries = tuple(absolute.iterdir())
    except OSError as exc:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            str(absolute),
            f"cannot enumerate {role} directory: {exc}",
        ) from exc
    if entries:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            str(absolute),
            f"{role} directory is not empty",
            expected=[],
            observed=sorted(entry.name for entry in entries),
        )


_PREIMPORT_DEPENDENCY_PROVENANCE: dict[str, dict[str, Any]] | None = None
_PREIMPORT_DEPENDENCY_FILES: dict[str, dict[str, dict[str, Any]]] = {}
_IMPORTED_DEPENDENCY_MODULES: dict[str, Any] = {}
_AUTHENTICATED_PYCACHE_DIRECTORY: tempfile.TemporaryDirectory[str] | None = None
if __name__ == "__main__":
    _startup_python = Path(os.path.abspath(sys.executable))
    _required_python = Path(
        os.path.abspath(os.fspath(_FIXED_PYTHON_EXECUTABLE))
    )
    if (
        os.path.normcase(str(_startup_python))
        != os.path.normcase(str(_required_python))
        or sys.flags.isolated != 1
        or sys.flags.no_site != 1
    ):
        sys.stderr.write(
            "production verifier startup requires "
            r"C:\Python314\python.exe -I -S"
            " before third-party imports\n"
        )
        raise SystemExit(2)
if sys.flags.isolated == 1 and sys.flags.no_site == 1:
    _PREIMPORT_DEPENDENCY_PROVENANCE = _dependency_provenance(
        verify_imported_versions=False,
        authenticated_files=_PREIMPORT_DEPENDENCY_FILES,
    )
    _runtime_allowed_files = {
        path: identity
        for name in ("numpy", "scipy", "sympy", "mpmath")
        for path, identity in _PREIMPORT_DEPENDENCY_FILES[name].items()
    }
    sys.meta_path.insert(0, _AuthenticatedSiteFinder(_runtime_allowed_files))
    pycache_base = Path(r"C:\tmp")
    _require_nonreparse_directory(pycache_base, "fixed bytecode cache base")
    _AUTHENTICATED_PYCACHE_DIRECTORY = tempfile.TemporaryDirectory(
        prefix="gauge-vfe-rg-pycache-",
        dir=pycache_base,
    )
    pycache_path = Path(_AUTHENTICATED_PYCACHE_DIRECTORY.name)
    _require_empty_nonreparse_directory(
        pycache_path,
        "controlled bytecode cache",
    )
    sys.pycache_prefix = str(pycache_path)
    sys.dont_write_bytecode = True

import mpmath
import numpy as np
import scipy
import scipy.linalg as sla
import sympy as sp

_IMPORTED_DEPENDENCY_MODULES.update(
    {
        "numpy": np,
        "scipy": scipy,
        "sympy": sp,
        "mpmath": mpmath,
    }
)
if _PREIMPORT_DEPENDENCY_PROVENANCE is not None:
    _POSTIMPORT_DEPENDENCY_PROVENANCE = _dependency_provenance(
        verify_imported_versions=True
    )
    _require_dependency_import_window(
        _PREIMPORT_DEPENDENCY_PROVENANCE,
        _POSTIMPORT_DEPENDENCY_PROVENANCE,
        _IMPORTED_DEPENDENCY_MODULES,
    )
    _require_empty_nonreparse_directory(
        Path(_AUTHENTICATED_PYCACHE_DIRECTORY.name),
        "controlled bytecode cache",
    )


def _require_governed_registry_unchanged(
    repo_root: Path,
    registry: dict[str, Any],
    *,
    test_fixture: bool,
    expected_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Rebind every governed path to its retained M0 handle and exact set."""

    root = Path(repo_root).resolve(strict=True)
    discovered = discover_bound_inputs(root, test_fixture=test_fixture)
    expected_relatives = sorted(record.relative_path for record in registry.values())
    observed_relatives = sorted(discovered)
    if observed_relatives != expected_relatives:
        raise VerificationFailure(
            "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
            "$.manifest.bound_inputs",
            "governed path discovery changed after the retained registry was acquired",
            expected=expected_relatives,
            observed=observed_relatives,
        )

    for relative in expected_relatives:
        path = discovered[relative]
        record = registry.get(_registry_path_key(path))
        if record is None or record.relative_path != relative:
            raise VerificationFailure(
                "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
                relative,
                "rediscovered governed path is not bound to its retained M0 handle",
            )
        payload, held_snapshot = record.guard.read()
        if payload != record.payload or held_snapshot != record.snapshot:
            raise VerificationFailure(
                "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
                relative,
                "retained governed handle changed after M0",
                expected=record.snapshot,
                observed=held_snapshot,
            )
        path_guard = _WindowsExecutableGuard(
            path,
            f"{relative} path recheck",
            issue_code="GOVERNED_INPUT_CHANGED_DURING_VERIFY",
            subject="governed input",
        )
        try:
            path_payload, path_snapshot = path_guard.read()
        finally:
            path_guard.close()
        if (
            path_payload != record.payload
            or path_snapshot["guard_filesystem_identity"]
            != record.snapshot["guard_filesystem_identity"]
        ):
            raise VerificationFailure(
                "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
                relative,
                "governed pathname no longer resolves to its retained M0 file identity",
                expected=record.snapshot,
                observed=path_snapshot,
            )

    manifest = build_manifest(root, test_fixture=test_fixture)
    if expected_manifest is not None and not _json_value_equal(
        manifest,
        expected_manifest,
    ):
        raise VerificationFailure(
            "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
            "$.manifest",
            "raw governed manifest changed after M0",
            expected=expected_manifest,
            observed=manifest,
        )
    return manifest


def _acquire_governed_registry(
    repo_root: Path,
    *,
    test_fixture: bool,
) -> tuple[dict[str, Any], dict[str, Any], Any]:
    """Lock policy first, then transactionally retain the exact governed set."""

    root = Path(repo_root).resolve(strict=True)
    policy_relative = f"{_VERIFICATION_RELATIVE}/manifest-policy.json"
    policy_path = _checked_regular_file(root, policy_relative)
    registry: dict[str, Any] = {}
    registry_token: Any | None = None
    try:
        policy_record = _open_governed_input_record(policy_relative, policy_path)
        registry[_registry_path_key(policy_path)] = policy_record
        registry_token = _ACTIVE_GOVERNED_REGISTRY.set(registry)

        discovered = discover_bound_inputs(root, test_fixture=test_fixture)
        for relative, path in discovered.items():
            key = _registry_path_key(path)
            if key in registry:
                if registry[key].relative_path != relative:
                    raise VerificationFailure(
                        "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
                        relative,
                        "two governed paths resolved to one retained file identity",
                        expected=registry[key].relative_path,
                        observed=relative,
                    )
                continue
            registry[key] = _open_governed_input_record(relative, path)

        manifest = _require_governed_registry_unchanged(
            root,
            registry,
            test_fixture=test_fixture,
        )
        return registry, manifest, registry_token
    except BaseException as primary:
        cleanup_errors: list[BaseException] = []
        if registry_token is not None:
            try:
                _ACTIVE_GOVERNED_REGISTRY.reset(registry_token)
            except BaseException as cleanup_error:
                cleanup_errors.append(cleanup_error)
        try:
            _close_governed_registry(registry)
        except BaseException as cleanup_error:
            cleanup_errors.append(cleanup_error)
        for cleanup_error in cleanup_errors:
            primary.add_note(
                f"governed-registry cleanup also failed: {cleanup_error!r}"
            )
        raise


def _acquire_run_evidence(
    repo_root: Path,
    *,
    test_fixture: bool = False,
) -> tuple[Any, Any | None]:
    """Capture one exact M0 snapshot, or reuse the enclosing run snapshot."""

    root = Path(repo_root).resolve(strict=True)
    active = _ACTIVE_RUN_EVIDENCE.get()
    if active is not None:
        if os.path.normcase(active.repo_root) != os.path.normcase(str(root)):
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                "$repository",
                "nested verification run changed repository identity",
                expected=active.repo_root,
                observed=str(root),
            )
        if active.test_fixture is not test_fixture:
            raise VerificationFailure(
                "PROTOCOL_PROFILE_MISMATCH",
                "$repository",
                "nested verification run changed the authorized protocol profile",
                expected=_expected_protocol_profile(active.test_fixture),
                observed=_expected_protocol_profile(test_fixture),
            )
        _verification_executable_identities()
        return active, None

    guards = _acquire_executable_guards()
    guard_token = _ACTIVE_EXECUTABLE_GUARDS.set(guards)
    try:
        executable_snapshot = _verification_executable_snapshot()
        executable_identities = _public_executable_identities(executable_snapshot)
        executable_token = _ACTIVE_EXECUTABLE_IDENTITIES.set(
            copy.deepcopy(executable_snapshot)
        )
        governed_registry, governed_manifest, registry_token = (
            _acquire_governed_registry(
                root,
                test_fixture=test_fixture,
            )
        )
        _git_top_level(root)
        _reject_git_metadata_overrides(root)
        head_revision = _resolve_current_head(root)
        _require_source_binding(
            root,
            head_revision,
            governed_manifest,
            test_fixture=test_fixture,
        )
        dependency_provenance = _dependency_provenance()
        evidence = _RunEvidence(
            repo_root=str(root),
            head_revision=head_revision,
            executable_snapshot=copy.deepcopy(executable_snapshot),
            executable_identities=copy.deepcopy(executable_identities),
            dependency_provenance=copy.deepcopy(dependency_provenance),
            governed_manifest=copy.deepcopy(governed_manifest),
            governed_registry=governed_registry,
            test_fixture=test_fixture,
        )
        run_token = _ACTIVE_RUN_EVIDENCE.set(evidence)
    except BaseException as primary:
        cleanup_errors: list[BaseException] = []
        if "executable_token" in locals():
            try:
                _ACTIVE_EXECUTABLE_IDENTITIES.reset(executable_token)
            except BaseException as cleanup_error:
                cleanup_errors.append(cleanup_error)
        if "registry_token" in locals():
            try:
                _ACTIVE_GOVERNED_REGISTRY.reset(registry_token)
            except BaseException as cleanup_error:
                cleanup_errors.append(cleanup_error)
            try:
                _close_governed_registry(governed_registry)
            except BaseException as cleanup_error:
                cleanup_errors.append(cleanup_error)
        try:
            _ACTIVE_EXECUTABLE_GUARDS.reset(guard_token)
        except BaseException as cleanup_error:
            cleanup_errors.append(cleanup_error)
        try:
            _close_executable_guards(guards)
        except BaseException as cleanup_error:
            cleanup_errors.append(cleanup_error)
        for cleanup_error in cleanup_errors:
            primary.add_note(f"run-evidence cleanup also failed: {cleanup_error!r}")
        raise
    return evidence, (
        executable_token,
        run_token,
        guard_token,
        guards,
        registry_token,
        governed_registry,
    )


def _require_run_evidence_unchanged(
    repo_root: Path,
    evidence: Any,
) -> None:
    """Recompute all run-scoped M1 identities and require exact equality."""

    root = Path(repo_root).resolve(strict=True)
    if _AUTHENTICATED_PYCACHE_DIRECTORY is not None:
        expected_pycache = str(
            Path(_AUTHENTICATED_PYCACHE_DIRECTORY.name)
        )
        if (
            sys.pycache_prefix != expected_pycache
            or sys.dont_write_bytecode is not True
        ):
            raise VerificationFailure(
                "EXECUTABLE_IDENTITY",
                "$.environment.dependency_provenance",
                "controlled bytecode-cache policy changed after M0",
                expected={
                    "pycache_prefix": expected_pycache,
                    "dont_write_bytecode": True,
                },
                observed={
                    "pycache_prefix": sys.pycache_prefix,
                    "dont_write_bytecode": sys.dont_write_bytecode,
                },
            )
        _require_empty_nonreparse_directory(
            Path(expected_pycache),
            "controlled bytecode cache",
        )
    if os.path.normcase(str(root)) != os.path.normcase(evidence.repo_root):
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            "$repository",
            "verification repository identity changed after M0",
            expected=evidence.repo_root,
            observed=str(root),
        )
    governed_manifest = _require_governed_registry_unchanged(
        root,
        evidence.governed_registry,
        test_fixture=evidence.test_fixture,
        expected_manifest=evidence.governed_manifest,
    )
    executable_snapshot = _verification_executable_snapshot()
    if executable_snapshot != evidence.executable_snapshot:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            "$.environment",
            "fixed verification executable identities changed between M0 and M1",
            expected=evidence.executable_snapshot,
            observed=executable_snapshot,
        )
    _git_top_level(root)
    _reject_git_metadata_overrides(root)
    head_revision = _resolve_current_head(root)
    if head_revision != evidence.head_revision:
        raise VerificationFailure(
            "SOURCE_REVISION_NOT_ANCESTOR",
            "$repository:HEAD",
            "HEAD changed between run-scoped M0 and M1",
            expected=evidence.head_revision,
            observed=head_revision,
        )
    _require_source_binding(
        root,
        head_revision,
        governed_manifest,
        test_fixture=evidence.test_fixture,
    )
    dependency_provenance = _dependency_provenance()
    if not _json_value_equal(
        dependency_provenance,
        evidence.dependency_provenance,
    ):
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            "$.environment.dependency_provenance",
            "actual dependency provenance changed between M0 and M1",
            expected=evidence.dependency_provenance,
            observed=dependency_provenance,
        )


def _release_run_evidence(
    tokens: Any | None,
) -> None:
    """Restore enclosing run contexts after an owned run completes."""

    if tokens is None:
        return
    (
        executable_token,
        run_token,
        guard_token,
        guards,
        registry_token,
        governed_registry,
    ) = tokens
    cleanup_errors: list[BaseException] = []
    for cleanup in (
        lambda: _ACTIVE_RUN_EVIDENCE.reset(run_token),
        lambda: _ACTIVE_EXECUTABLE_IDENTITIES.reset(executable_token),
        lambda: _ACTIVE_GOVERNED_REGISTRY.reset(registry_token),
        lambda: _ACTIVE_EXECUTABLE_GUARDS.reset(guard_token),
        lambda: _close_governed_registry(governed_registry),
        lambda: _close_executable_guards(guards),
    ):
        try:
            cleanup()
        except BaseException as cleanup_error:
            cleanup_errors.append(cleanup_error)
    if cleanup_errors:
        primary = cleanup_errors[0]
        for cleanup_error in cleanup_errors[1:]:
            primary.add_note(f"additional cleanup failure: {cleanup_error!r}")
        raise primary


def _normalize_legacy_check(
    legacy: dict[str, Any],
    expected_check_id: str,
) -> dict[str, Any]:
    actual_id = legacy.get("check_id")
    status = legacy.get("status")
    evidence_kind = legacy.get("evidence_kind")
    metadata = {
        key: value
        for key, value in legacy.items()
        if key not in {"check_id", "status", "evidence_kind"}
    }
    if actual_id != expected_check_id:
        status = "FAIL"
        metadata = {
            "protocol_error": "check returned a different ID than its bound callable",
            "actual_check_id": actual_id,
            "legacy_result": metadata,
        }
    if status not in {"PASS", "FAIL", "INCONCLUSIVE"}:
        actual_status = status
        status = "FAIL"
        metadata = {
            "protocol_error": "check returned an invalid status",
            "actual_status": actual_status,
            "legacy_result": metadata,
        }
    if not isinstance(evidence_kind, str) or not evidence_kind:
        evidence_kind = "mechanical_failure"
    return _jsonable(
        {
            "check_id": expected_check_id,
            "status": status,
            "evidence_kind": evidence_kind,
            "observed": {"legacy_result": metadata},
        }
    )


def _fixture_checks(claims_document: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    for declaration in claims_document["checks"]:
        check_id = declaration["check_id"]
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS",
                "evidence_kind": "fixture_protocol",
                "observed": {
                    "fixture_complete": True,
                    "declaration": _jsonable(declaration),
                },
            }
        )
    return checks


def _production_checks(
    repo_root: Path,
    claims_document: dict[str, Any],
) -> list[dict[str, Any]]:
    raw_checks: list[dict[str, Any]] = []
    for check, expected_id in zip(CHECKS, PRODUCTION_CHECK_IDS, strict=True):
        try:
            raw_checks.append(check())
        except Exception as exc:
            raw_checks.append(
                {
                    "check_id": expected_id,
                    "status": "FAIL",
                    "evidence_kind": "mechanical_failure",
                    "title": check.__name__,
                    "claim_ids": [],
                    "seed": None,
                    "sample_count": 0,
                    "expected": {},
                    "tolerances": {},
                    "observed": {
                        "exception_type": type(exc).__name__,
                        "exception_message": str(exc),
                        "traceback": traceback.format_exc(),
                    },
                    "interpretation": "The check raised and provides no supporting evidence.",
                }
            )
    completed = {item.get("check_id"): item for item in raw_checks}
    claims = claims_document["claims"]
    inventory, current_claims, tex_source_manifest = scan_inventory(
        claims,
        repo_root=repo_root,
    )
    dispositions = [
        recommended_disposition(claim, completed) for claim in current_claims
    ]
    mapping_failures = [
        item["claim_id"]
        for item in dispositions
        if item["endpoint_mapping_status"] != "PASS"
    ]
    supplemental_ids = claims_document.get("supplemental_check_ids", [])
    supplemental_unknown = [item for item in supplemental_ids if item not in completed]
    supplemental_nonpassing = [
        item
        for item in supplemental_ids
        if item in completed and completed[item].get("status") != "PASS"
    ]
    inventory_status = (
        "PASS"
        if inventory.get("status") == "PASS"
        and not mapping_failures
        and not supplemental_unknown
        and not supplemental_nonpassing
        else "FAIL"
    )
    normalized: list[dict[str, Any]] = [
        _jsonable(
            {
                "check_id": "CHK-SOURCE-INVENTORY",
                "status": inventory_status,
                "evidence_kind": "source_inventory",
                "observed": {
                    "inventory": inventory,
                    "current_claims": current_claims,
                    "tex_source_manifest": tex_source_manifest,
                    "claim_dispositions": dispositions,
                    "mapping_validation": {
                        "claim_failures": mapping_failures,
                        "supplemental_unknown": supplemental_unknown,
                        "supplemental_nonpassing": supplemental_nonpassing,
                    },
                },
            }
        )
    ]
    normalized.extend(
        _normalize_legacy_check(item, expected_id)
        for item, expected_id in zip(raw_checks, PRODUCTION_CHECK_IDS, strict=True)
    )
    return normalized


def _build_result_body(
    repo_root: Path,
    source_revision: str,
    *,
    test_fixture: bool = False,
) -> dict[str, Any]:
    """Purely construct a source-bound schema-3 result in memory."""

    root = Path(repo_root).resolve(strict=True)
    protocol_profile = _expected_protocol_profile(test_fixture)
    run_evidence = _ACTIVE_RUN_EVIDENCE.get()
    if run_evidence is None:
        raise VerificationFailure(
            "EXECUTABLE_IDENTITY",
            "$repository",
            "result construction requires an active run-scoped M0 snapshot",
        )
    executable_identities = copy.deepcopy(run_evidence.executable_identities)
    manifest = build_manifest(root, test_fixture=test_fixture)
    _require_source_binding(
        root,
        source_revision,
        manifest,
        test_fixture=test_fixture,
    )
    policy = _load_manifest_policy(root, test_fixture=test_fixture)
    if policy["protocol_profile"] != protocol_profile:
        raise VerificationFailure(
            "PROTOCOL_PROFILE_MISMATCH",
            f"{_EXACT_REQUIRED_PATHS[8]}:protocol_profile",
            "manifest policy profile changed during result construction",
            expected=protocol_profile,
            observed=policy["protocol_profile"],
        )
    claims_document = _load_claims_document(root, protocol_profile)
    required_ids = _required_check_ids(claims_document, protocol_profile)
    checks = (
        _fixture_checks(claims_document)
        if protocol_profile == SYNTHETIC_PROTOCOL_PROFILE
        else _production_checks(root, claims_document)
    )
    check_ids = tuple(item["check_id"] for item in checks)
    if check_ids != required_ids:
        raise VerificationFailure(
            "CHECK_ID_ORDER",
            "$.checks",
            "constructed check IDs do not equal the required ordered protocol",
            expected=list(required_ids),
            observed=list(check_ids),
        )
    overall_status = (
        "PASS" if checks and all(item["status"] == "PASS" for item in checks) else "FAIL"
    )
    document: dict[str, Any] = {
        "schema_version": "3.0",
        "protocol_profile": protocol_profile,
        "generated_at_utc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_revision": source_revision,
        "source_dirty": False,
        "overall_status": overall_status,
        "environment": {
            "python": sys.version,
            **executable_identities,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "dependencies": _dependency_versions(),
            "dependency_provenance": copy.deepcopy(
                run_evidence.dependency_provenance
            ),
        },
        "manifest": manifest,
        "checks": checks,
        "semantic_payload_digest": "",
    }
    document["semantic_payload_digest"] = hashlib.sha256(
        canonical_json_bytes(semantic_payload(document))
    ).hexdigest()
    shape_errors = _validate_result_shape_with_schema(
        document,
        root / f"{_VERIFICATION_RELATIVE}/result.schema.json",
    )
    if shape_errors:
        raise VerificationFailure(
            "SCHEMA_VIOLATION",
            "$",
            "constructed result violates the bound result schema",
            observed=shape_errors,
        )
    return document


def build_result(
    repo_root: Path,
    source_revision: str,
    *,
    test_fixture: bool = False,
) -> dict[str, Any]:
    """Construct a result under exact run-scoped M0/M1 identities."""

    root = Path(repo_root).resolve(strict=True)
    run_evidence, tokens = _acquire_run_evidence(
        root,
        test_fixture=test_fixture,
    )
    try:
        document = _build_result_body(
            root,
            source_revision,
            test_fixture=test_fixture,
        )
        if tokens is not None:
            _require_run_evidence_unchanged(root, run_evidence)
        return document
    finally:
        _release_run_evidence(tokens)


def _check_binding_issues(
    document: dict[str, Any],
    required_ids: tuple[str, ...],
) -> list[VerificationIssue]:
    issues: list[VerificationIssue] = []
    checks = document.get("checks")
    if not isinstance(checks, list):
        return [
            _issue(
                "CHECK_ID_MISSING",
                "$.checks",
                "result has no check list",
                expected=list(required_ids),
            )
        ]
    identifiers = [
        item.get("check_id") if isinstance(item, dict) else None for item in checks
    ]
    duplicates = sorted(
        {
            item
            for item in identifiers
            if isinstance(item, str) and identifiers.count(item) > 1
        }
    )
    unknown = sorted(
        {
            item
            for item in identifiers
            if isinstance(item, str) and item not in required_ids
        }
    )
    missing = [item for item in required_ids if item not in identifiers]
    if duplicates:
        issues.append(
            _issue(
                "CHECK_ID_DUPLICATE",
                "$.checks",
                "result repeats check IDs",
                observed=duplicates,
            )
        )
    if unknown:
        issues.append(
            _issue(
                "CHECK_ID_UNKNOWN",
                "$.checks",
                "result contains unknown check IDs",
                observed=unknown,
            )
        )
    if missing:
        issues.append(
            _issue(
                "CHECK_ID_MISSING",
                "$.checks",
                "result omits required check IDs",
                observed=missing,
            )
        )
    if tuple(identifiers) != required_ids:
        issues.append(
            _issue(
                "CHECK_ID_ORDER",
                "$.checks",
                "check IDs are not in the required exact order",
                expected=list(required_ids),
                observed=identifiers,
            )
        )
    for index, item in enumerate(checks):
        if not isinstance(item, dict) or item.get("status") != "PASS":
            issues.append(
                _issue(
                    "CHECK_STATUS_NOT_PASS",
                    f"$.checks[{index}].status",
                    "every bound check must have PASS status",
                    expected="PASS",
                    observed=item.get("status") if isinstance(item, dict) else None,
                )
            )
    expected_overall = (
        "PASS"
        if checks
        and all(isinstance(item, dict) and item.get("status") == "PASS" for item in checks)
        else "FAIL"
    )
    if document.get("overall_status") != expected_overall:
        issues.append(
            _issue(
                "OVERALL_STATUS_INCONSISTENT",
                "$.overall_status",
                "overall status is inconsistent with check statuses",
                expected=expected_overall,
                observed=document.get("overall_status"),
            )
        )
    if document.get("overall_status") != "PASS":
        issues.append(
            _issue(
                "RESULT_STATUS_NOT_PASS",
                "$.overall_status",
                "only a complete PASS result can verify",
                expected="PASS",
                observed=document.get("overall_status"),
            )
        )
    return issues


def _report(
    result_path: Path,
    document: dict[str, Any] | None,
    before_hash: str | None,
    after_hash: str | None,
    issues: list[VerificationIssue],
    *,
    test_fixture: bool = False,
) -> VerificationReport:
    protocol_profile = _expected_protocol_profile(test_fixture)
    run_evidence = _ACTIVE_RUN_EVIDENCE.get()
    if run_evidence is not None:
        executable_identities: dict[str, str | None] = copy.deepcopy(
            run_evidence.executable_identities
        )
        head_revision: str | None = run_evidence.head_revision
    else:
        head_revision = None
        try:
            executable_identities = _verification_executable_identities()
        except VerificationFailure:
            executable_identities = {
                "python_executable": str(_FIXED_PYTHON_EXECUTABLE),
                "python_executable_sha256": None,
                "git_executable": str(_FIXED_GIT_EXECUTABLE),
                "git_executable_sha256": None,
            }
    source_revision = (
        document.get("source_revision")
        if isinstance(document, dict) and isinstance(document.get("source_revision"), str)
        else None
    )
    semantic_digest = (
        document.get("semantic_payload_digest")
        if isinstance(document, dict)
        and isinstance(document.get("semantic_payload_digest"), str)
        else None
    )
    manifest_count: int | None = None
    check_count: int | None = None
    if isinstance(document, dict):
        manifest = document.get("manifest")
        if isinstance(manifest, dict) and isinstance(manifest.get("bound_inputs"), dict):
            manifest_count = len(manifest["bound_inputs"])
        checks = document.get("checks")
        if isinstance(checks, list):
            check_count = len(checks)
    receipt_id = _ACTIVE_TRANSACTION_RECEIPT_ID.get() or uuid.uuid4().hex
    ok = not issues
    input_unchanged = (
        before_hash is not None and after_hash is not None and before_hash == after_hash
    )
    return VerificationReport(
        ok=ok,
        result_path=str(Path(os.path.abspath(os.fspath(result_path)))),
        source_revision=source_revision,
        input_sha256_before=before_hash,
        input_sha256_after=after_hash,
        input_unchanged=input_unchanged,
        transaction_receipt_id=receipt_id,
        published_result_sha256=(after_hash if ok and input_unchanged else None),
        semantic_payload_digest=semantic_digest,
        manifest_path_count=manifest_count,
        check_count=check_count,
        protocol_profile=protocol_profile,
        head_revision=head_revision,
        python_executable=executable_identities["python_executable"],
        python_executable_sha256=executable_identities[
            "python_executable_sha256"
        ],
        git_executable=executable_identities["git_executable"],
        git_executable_sha256=executable_identities["git_executable_sha256"],
        issues=tuple(issues),
    )


def _verify_result_body(
    result_path: Path,
    repo_root: Path,
    *,
    test_fixture: bool = False,
    result_guard: _WindowsExecutableGuard,
) -> VerificationReport:
    """Verify a stored result without mutating it or any governed input."""

    path = Path(result_path)
    root = Path(repo_root).resolve(strict=True)
    issues: list[VerificationIssue] = []
    document: dict[str, Any] | None = None
    manifest_zero: dict[str, Any] | None = None
    before_hash: str | None = None
    after_hash: str | None = None
    protocol_profile = _expected_protocol_profile(test_fixture)
    run_evidence = _ACTIVE_RUN_EVIDENCE.get()
    executable_identities: dict[str, str] | None = None
    try:
        executable_identities = _verification_executable_identities()
    except VerificationFailure as exc:
        issues.append(
            _issue(
                exc.code,
                exc.location,
                str(exc),
                expected=exc.expected,
                observed=exc.observed,
            )
        )
    try:
        before_bytes, before_result_snapshot = result_guard.read()
        before_hash = hashlib.sha256(before_bytes).hexdigest()
    except (OSError, VerificationFailure) as exc:
        return _report(
            path,
            None,
            None,
            None,
            [_issue("RESULT_IO", str(path), f"cannot read result: {exc}")],
            test_fixture=test_fixture,
        )

    try:
        parsed = _strict_json_loads(before_bytes, location=str(path))
        if isinstance(parsed, dict):
            document = parsed
        else:
            issues.append(
                _issue(
                    "SCHEMA_VIOLATION",
                    "$",
                    "result root must be a JSON object",
                )
            )
    except _InvalidUtf8JsonError as exc:
        issues.append(_issue("INVALID_UTF8", str(path), str(exc)))
    except DuplicateJsonKeyError as exc:
        issues.append(_issue("DUPLICATE_JSON_KEY", str(path), str(exc)))
    except NonFiniteJsonError as exc:
        issues.append(_issue("NONFINITE_JSON", str(path), str(exc)))
    except _MalformedJsonError as exc:
        issues.append(_issue("MALFORMED_JSON", str(path), str(exc)))

    if document is not None:
        if document.get("protocol_profile") != protocol_profile:
            issues.append(
                _issue(
                    "PROTOCOL_PROFILE_MISMATCH",
                    "$.protocol_profile",
                    "stored result profile does not match the authorized call boundary",
                    expected=protocol_profile,
                    observed=document.get("protocol_profile"),
                )
            )
        if executable_identities is not None:
            environment = document.get("environment")
            observed_identities = (
                {
                    key: environment.get(key)
                    for key in executable_identities
                }
                if isinstance(environment, dict)
                else None
            )
            if observed_identities != executable_identities:
                issues.append(
                    _issue(
                        "EXECUTABLE_IDENTITY",
                        "$.environment",
                        "stored executable identities do not equal the current fixed tools",
                        expected=executable_identities,
                        observed=observed_identities,
                    )
                )
            observed_provenance = (
                environment.get("dependency_provenance")
                if isinstance(environment, dict)
                else None
            )
            observed_dependencies = (
                environment.get("dependencies")
                if isinstance(environment, dict)
                else None
            )
            try:
                expected_dependencies = _dependency_pins(
                    root / f"{_VERIFICATION_RELATIVE}/requirements.txt"
                )
            except VerificationFailure as exc:
                issues.append(
                    _issue(
                        exc.code,
                        exc.location,
                        str(exc),
                        expected=exc.expected,
                        observed=exc.observed,
                    )
                )
                expected_dependencies = None
            if (
                expected_dependencies is not None
                and observed_dependencies != expected_dependencies
            ):
                issues.append(
                    _issue(
                        "EXECUTABLE_IDENTITY",
                        "$.environment.dependencies",
                        "stored dependency versions do not equal the exact requirements pins",
                        expected=expected_dependencies,
                        observed=observed_dependencies,
                    )
                )
            if (
                expected_dependencies is not None
                and isinstance(observed_provenance, dict)
            ):
                provenance_versions = {
                    name: (
                        value.get("version")
                        if isinstance(value, dict)
                        else None
                    )
                    for name, value in observed_provenance.items()
                }
                if provenance_versions != expected_dependencies:
                    issues.append(
                        _issue(
                            "EXECUTABLE_IDENTITY",
                            "$.environment.dependency_provenance",
                            "stored provenance versions do not equal dependencies and exact requirements pins",
                            expected=expected_dependencies,
                            observed=provenance_versions,
                        )
                    )
            expected_provenance = (
                run_evidence.dependency_provenance
                if run_evidence is not None
                else None
            )
            if not _json_value_equal(observed_provenance, expected_provenance):
                issues.append(
                    _issue(
                        "EXECUTABLE_IDENTITY",
                        "$.environment.dependency_provenance",
                        "stored dependency provenance does not equal the run-scoped M0 actual bytes",
                        expected=expected_provenance,
                        observed=observed_provenance,
                    )
                )
        try:
            rendered = canonical_json_bytes(document)
        except NonFiniteJsonError as exc:
            issues.append(_issue("NONFINITE_JSON", "$", str(exc)))
            rendered = None
        except (TypeError, ValueError) as exc:
            issues.append(_issue("SCHEMA_VIOLATION", "$", str(exc)))
            rendered = None
        if rendered is not None and rendered != before_bytes:
            issues.append(
                _issue(
                    "NONCANONICAL_RESULT_BYTES",
                    str(path),
                    "stored result is not exact compact sorted UTF-8 canonical JSON",
                )
            )
        shape_errors = _validate_result_shape_with_schema(
            document,
            root / f"{_VERIFICATION_RELATIVE}/result.schema.json",
        )
        if shape_errors:
            issues.append(
                _issue(
                    "SCHEMA_VIOLATION",
                    "$",
                    "stored result violates the bound result schema",
                    observed=shape_errors,
                )
            )
        digest = document.get("semantic_payload_digest")
        try:
            recomputed_digest = hashlib.sha256(
                canonical_json_bytes(semantic_payload(document))
            ).hexdigest()
        except (TypeError, ValueError) as exc:
            recomputed_digest = None
            issues.append(_issue("NONFINITE_JSON", "$", str(exc)))
        if digest != recomputed_digest:
            issues.append(
                _issue(
                    "SEMANTIC_DIGEST_MISMATCH",
                    "$.semantic_payload_digest",
                    "stored semantic digest does not match the strict semantic payload",
                    expected=recomputed_digest,
                    observed=digest,
                )
            )

    try:
        manifest_zero = build_manifest(root, test_fixture=test_fixture)
    except VerificationFailure as exc:
        issues.append(
            _issue(
                exc.code,
                exc.location,
                str(exc),
                expected=exc.expected,
                observed=exc.observed,
            )
        )
    except (OSError, ValueError) as exc:
        issues.append(
            _issue(
                "MANIFEST_POLICY_INVALID",
                "$manifest",
                f"cannot discover initial manifest: {exc}",
            )
        )

    required_ids: tuple[str, ...] | None = None
    try:
        policy_profile = _load_manifest_policy(
            root,
            test_fixture=test_fixture,
        )["protocol_profile"]
        claims_document = _load_claims_document(root, policy_profile)
        required_ids = _required_check_ids(claims_document, policy_profile)
    except VerificationFailure as exc:
        issues.append(
            _issue(
                exc.code,
                exc.location,
                str(exc),
                expected=exc.expected,
                observed=exc.observed,
            )
        )

    if document is not None and manifest_zero is not None:
        stored_manifest = document.get("manifest")
        issues.extend(
            _source_binding_issues(
                root,
                document.get("source_revision"),
                manifest_zero,
                stored_manifest if isinstance(stored_manifest, dict) else None,
                test_fixture=test_fixture,
            )
        )
        if required_ids is not None:
            issues.extend(_check_binding_issues(document, required_ids))

        source_revision = document.get("source_revision")
        if isinstance(source_revision, str):
            try:
                fresh = build_result(
                    root,
                    source_revision,
                    test_fixture=test_fixture,
                )
                if canonical_json_bytes(semantic_payload(fresh)) != canonical_json_bytes(
                    semantic_payload(document)
                ):
                    issues.append(
                        _issue(
                            "SEMANTIC_RECOMPUTATION_MISMATCH",
                            "$",
                            "stored semantics differ from a fresh in-memory recomputation",
                        )
                    )
            except VerificationFailure as exc:
                issues.append(
                    _issue(
                        exc.code,
                        exc.location,
                        str(exc),
                        expected=exc.expected,
                        observed=exc.observed,
                    )
                )
            except Exception as exc:
                issues.append(
                    _issue(
                        "RECOMPUTATION_EXCEPTION",
                        "$",
                        f"fresh in-memory recomputation raised {type(exc).__name__}: {exc}",
                    )
                )

    try:
        manifest_one = build_manifest(root, test_fixture=test_fixture)
        if manifest_zero is not None and manifest_one != manifest_zero:
            issues.append(
                _issue(
                    "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
                    "$manifest",
                    "governed input manifest changed between M0 and M1",
                )
            )
    except VerificationFailure as exc:
        issues.append(
            _issue(
                exc.code,
                exc.location,
                str(exc),
                expected=exc.expected,
                observed=exc.observed,
            )
        )
    except (OSError, ValueError) as exc:
        issues.append(
            _issue(
                "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
                "$manifest",
                f"cannot discover final manifest: {exc}",
            )
        )

    try:
        after_bytes, after_result_snapshot = result_guard.read()
        after_hash = hashlib.sha256(after_bytes).hexdigest()
        if (
            after_bytes != before_bytes
            or after_result_snapshot != before_result_snapshot
        ):
            issues.append(
                _issue(
                    "RESULT_CHANGED_DURING_VERIFY",
                    str(path),
                    "result bytes changed while verification was running",
                    expected=before_hash,
                    observed=after_hash,
                )
            )
    except (OSError, VerificationFailure) as exc:
        issues.append(
            _issue(
                "RESULT_CHANGED_DURING_VERIFY",
                str(path),
                f"cannot re-read result after verification: {exc}",
            )
        )
    return _report(
        path,
        document,
        before_hash,
        after_hash,
        issues,
        test_fixture=test_fixture,
    )


def verify_result(
    result_path: Path,
    repo_root: Path,
    *,
    test_fixture: bool = False,
    _retained_result_guard: _WindowsExecutableGuard | None = None,
) -> VerificationReport:
    """Verify a stored result under exact run-scoped M0/M1 identities."""

    path = Path(result_path)
    root = Path(repo_root).resolve(strict=True)
    unsafe_result = _unsafe_target_component(path)
    if unsafe_result is not None:
        component, message = unsafe_result
        return _report(
            path,
            None,
            None,
            None,
            [
                _issue(
                    "RESULT_IO",
                    str(path),
                    f"unsafe verification result component {component}: {message}",
                )
            ],
            test_fixture=test_fixture,
        )
    owns_result_guard = _retained_result_guard is None
    result_guard = _retained_result_guard
    if result_guard is None:
        try:
            result_guard = _WindowsExecutableGuard(path, "verification result")
        except VerificationFailure as exc:
            return _report(
                path,
                None,
                None,
                None,
                [_issue("RESULT_IO", str(path), str(exc))],
                test_fixture=test_fixture,
            )
    try:
        run_evidence, tokens = _acquire_run_evidence(
            root,
            test_fixture=test_fixture,
        )
    except VerificationFailure as exc:
        try:
            result_bytes, _snapshot = result_guard.read()
            digest = hashlib.sha256(result_bytes).hexdigest()
            return _report(
                path,
                None,
                digest,
                digest,
                [
                    _issue(
                        exc.code,
                        exc.location,
                        str(exc),
                        expected=exc.expected,
                        observed=exc.observed,
                    )
                ],
                test_fixture=test_fixture,
            )
        finally:
            if owns_result_guard:
                result_guard.close()
    try:
        report = _verify_result_body(
            path,
            root,
            test_fixture=test_fixture,
            result_guard=result_guard,
        )
        held_snapshot = result_guard.snapshot()
        path_guard = _WindowsExecutableGuard(path, "verification result path recheck")
        try:
            path_snapshot = path_guard.snapshot()
        finally:
            path_guard.close()
        if (
            held_snapshot["guard_filesystem_identity"]
            != path_snapshot["guard_filesystem_identity"]
            or held_snapshot["sha256"] != path_snapshot["sha256"]
        ):
            report = _with_issue(
                report,
                _issue(
                    "RESULT_CHANGED_DURING_VERIFY",
                    str(path),
                    "result path no longer resolves to the held verification file identity",
                    expected=held_snapshot,
                    observed=path_snapshot,
                ),
            )
        if tokens is not None:
            try:
                _require_run_evidence_unchanged(root, run_evidence)
            except VerificationFailure as exc:
                report = _with_issue(
                    report,
                    _issue(
                        exc.code,
                        exc.location,
                        str(exc),
                        expected=exc.expected,
                        observed=exc.observed,
                    ),
                )
        return report
    finally:
        _release_run_evidence(tokens)
        if owns_result_guard:
            result_guard.close()


def verification_report_document(report: VerificationReport) -> dict[str, Any]:
    """Convert an immutable report to its strict JSON interchange shape."""

    return {
        "ok": report.ok,
        "result_path": report.result_path,
        "source_revision": report.source_revision,
        "input_sha256_before": report.input_sha256_before,
        "input_sha256_after": report.input_sha256_after,
        "input_unchanged": report.input_unchanged,
        "transaction_receipt_id": report.transaction_receipt_id,
        "published_result_sha256": report.published_result_sha256,
        "semantic_payload_digest": report.semantic_payload_digest,
        "manifest_path_count": report.manifest_path_count,
        "check_count": report.check_count,
        "protocol_profile": report.protocol_profile,
        "head_revision": report.head_revision,
        "python_executable": report.python_executable,
        "python_executable_sha256": report.python_executable_sha256,
        "git_executable": report.git_executable,
        "git_executable_sha256": report.git_executable_sha256,
        "issues": [dict(issue._asdict()) for issue in report.issues],
    }


def scan_inventory(
    claims: list[dict[str, Any]],
    *,
    repo_root: Path | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    active_repo_root = REPO_ROOT if repo_root is None else Path(repo_root).resolve()
    active_tex_root = active_repo_root / _MANUSCRIPT_RELATIVE
    grouped: dict[str, list[dict[str, Any]]] = {}
    for claim in claims:
        grouped.setdefault(claim["source_file"], []).append(claim)

    current_claims: list[dict[str, Any]] = []
    file_counts: dict[str, dict[str, int]] = {}
    source_manifest: dict[str, dict[str, Any]] = {}
    bare_table_status_entries: list[dict[str, Any]] = []
    failures: list[str] = []
    discovered_paths = sorted(
        active_tex_root.rglob("*.tex"),
        key=lambda path: path.relative_to(active_tex_root).as_posix(),
    )
    discovered_files = {
        path.relative_to(active_tex_root).as_posix(): path for path in discovered_paths
    }
    missing_declared_files = sorted(set(grouped) - set(discovered_files))
    for source_file in missing_declared_files:
        failures.append(f"{source_file}: declared source file was not discovered")

    for source_file, path in discovered_files.items():
        expected_claims = grouped.get(source_file, [])
        raw_source = _read_stable_file(path)
        text = raw_source.decode("utf-8")
        source_manifest[source_file] = manifest_entry(
            path,
            raw_source,
            repo_root=active_repo_root,
        )
        matches = list(re.finditer(re.escape(NUMERICAL_TOKEN), text))
        bare_matches = list(re.finditer(r"&\s*NUMERICAL\s*&", text))
        for match in bare_matches:
            bare_table_status_entries.append(
                {
                    "source_file": source_file,
                    "source_line": text.count("\n", 0, match.start()) + 1,
                    "matched_text": match.group(0),
                }
            )
        if bare_matches:
            failures.append(
                f"{source_file}: found {len(bare_matches)} bare NUMERICAL status-table cells"
            )
        file_counts[source_file] = {"expected": len(expected_claims), "observed": len(matches)}
        if len(matches) != len(expected_claims):
            failures.append(
                f"{source_file}: expected {len(expected_claims)} NUMERICAL tokens, found {len(matches)}"
            )
        for claim in expected_claims:
            index = int(claim["occurrence_index"]) - 1
            item = dict(claim)
            if index < len(matches):
                item["current_source_line"] = text.count("\n", 0, matches[index].start()) + 1
                item["source_token_found"] = True
            else:
                item["current_source_line"] = None
                item["source_token_found"] = False
                failures.append(f"{claim['id']}: occurrence index not found")
            current_claims.append(item)

    for source_file in missing_declared_files:
        for claim in grouped[source_file]:
            item = dict(claim)
            item["current_source_line"] = None
            item["source_token_found"] = False
            current_claims.append(item)
            failures.append(f"{claim['id']}: source file not found")

    status = "PASS" if not failures else "FAIL"
    return (
        {
            "status": status,
            "scan_scope": {
                "source_root": active_tex_root.relative_to(active_repo_root).as_posix(),
                "recursive_glob": "**/*.tex",
                "discovered_tex_files": len(discovered_files),
            },
            "expected_total": len(claims),
            "observed_total": sum(value["observed"] for value in file_counts.values()),
            "bare_status_table_entries": {
                "count": len(bare_table_status_entries),
                "required_count": 0,
                "role": "forbidden unwrapped status cells; every semantic NUMERICAL status must use the macro and appear in the claim inventory",
                "entries": bare_table_status_entries,
            },
            "file_counts": file_counts,
            "failures": failures,
        },
        current_claims,
        source_manifest,
    )


def recommended_disposition(
    claim: dict[str, Any], completed_checks: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    claim_id = claim["id"]
    mapped = claim.get("check_ids", [])
    mapped_results = [completed_checks[cid] for cid in mapped if cid in completed_checks]
    replacement_ids = [item["check_id"] for item in mapped_results if item["status"] == "PASS"]
    unknown_check_ids = [cid for cid in mapped if cid not in completed_checks]
    disposition = claim["recommended_disposition"]
    reproducible = claim.get("current_protocol_reproducible")
    if reproducible is None:
        current_status = "NOT_APPLICABLE"
    elif reproducible is False:
        current_status = "INCONCLUSIVE"
    elif (
        mapped
        and not unknown_check_ids
        and len(mapped_results) == len(mapped)
        and all(item["status"] == "PASS" for item in mapped_results)
    ):
        current_status = "PASS"
    else:
        current_status = "FAIL"
    endpoint_mapping_status = (
        "PASS"
        if (
            current_status in {"PASS", "NOT_APPLICABLE"}
            or (
                current_status == "INCONCLUSIVE"
                and disposition == "retain_as_inconclusive"
                and bool(claim.get("missing_obligation"))
            )
        )
        else "FAIL"
    )
    return {
        "claim_id": claim_id,
        "source_file": claim["source_file"],
        "current_source_line": claim["current_source_line"],
        "load_bearing": claim["load_bearing"],
        "role": claim["role"],
        "current_protocol_status": current_status,
        "endpoint_mapping_status": endpoint_mapping_status,
        "recommended_disposition": disposition,
        "replacement_check_ids": replacement_ids,
        "declared_check_ids": mapped,
        "unknown_check_ids": unknown_check_ids,
        "missing_obligation": claim.get("missing_obligation"),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        usage=(
            "%(prog)s (--update RESULT | --verify RESULT) "
            "[--source-revision SHA] [--report REPORT]"
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--update",
        metavar="RESULT",
        type=Path,
        help="construct and atomically replace the explicit RESULT",
    )
    mode.add_argument(
        "--verify",
        metavar="RESULT",
        type=Path,
        help="nonmutating verification of the explicit RESULT",
    )
    parser.add_argument(
        "--source-revision",
        metavar="SHA",
        help="full source commit for update mode (default: current HEAD)",
    )
    parser.add_argument(
        "--report",
        metavar="REPORT",
        type=Path,
        help="optional separate strict JSON operation report",
    )
    args = parser.parse_args(argv)
    if args.verify is not None and args.source_revision is not None:
        parser.error("--source-revision is valid only with --update RESULT")
    return args


def _same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(_lexical_absolute(left))) == os.path.normcase(
        str(_lexical_absolute(right))
    )


def _lexical_absolute(path: Path) -> Path:
    """Return an absolute normalized path without following reparse components."""

    return Path(os.path.abspath(os.fspath(path)))


def _is_within(path: Path, root: Path) -> bool:
    try:
        _lexical_absolute(path).relative_to(_lexical_absolute(root))
        return True
    except ValueError:
        return False


def _unsafe_target_component(path: Path) -> tuple[Path, str] | None:
    absolute = _lexical_absolute(path)
    if any(part.casefold() == ".git" for part in absolute.parts):
        return absolute, "a .git path component is forbidden for every result/report target"

    parts = absolute.parts
    if not parts:
        return absolute, "target path has no absolute identity"
    current = Path(parts[0])
    for part in parts[1:]:
        current /= part
        try:
            current.lstat()
        except FileNotFoundError:
            break
        except OSError as exc:
            return current, f"cannot safely inspect target component: {exc}"
        if _is_link_or_reparse(current):
            return current, "symlink, junction, or reparse target components are forbidden"
    return None


def _destructive_target_issue(
    path: Path,
    *,
    role: str,
    allow_canonical_current_result: bool,
) -> VerificationIssue | None:
    unsafe = _unsafe_target_component(path)
    if unsafe is not None:
        component, message = unsafe
        return _issue(
            "REPORT_TARGET_CONFLICT",
            str(path),
            f"unsafe {role} target component {component}: {message}",
        )
    if _is_within(path, REPO_ROOT):
        current_result = REPO_ROOT / f"{_VERIFICATION_RELATIVE}/current-results.json"
        if not (
            allow_canonical_current_result
            and _same_path(path, current_result)
        ):
            return _issue(
                "REPORT_TARGET_CONFLICT",
                str(path),
                f"{role} target inside the repository is forbidden",
            )
    absolute = _lexical_absolute(path)
    try:
        mode = absolute.lstat().st_mode
    except FileNotFoundError:
        return None
    except OSError as exc:
        return _issue(
            "REPORT_TARGET_CONFLICT",
            str(path),
            f"cannot safely inspect {role} target: {exc}",
        )
    if not stat.S_ISREG(mode):
        return _issue(
            "REPORT_TARGET_CONFLICT",
            str(path),
            f"existing {role} target is not a regular file",
        )
    return None


def _target_issue(
    result_path: Path,
    report_path: Path | None,
    *,
    update: bool,
) -> VerificationIssue | None:
    if report_path is not None and _same_path(result_path, report_path):
        return _issue(
            "REPORT_TARGET_CONFLICT",
            str(report_path),
            "report target must be distinct from result target",
        )
    unsafe_result = _unsafe_target_component(result_path)
    if unsafe_result is not None:
        component, message = unsafe_result
        return _issue(
            "REPORT_TARGET_CONFLICT",
            str(result_path),
            f"unsafe result target component {component}: {message}",
        )
    if update:
        result_issue = _destructive_target_issue(
            result_path,
            role="update",
            allow_canonical_current_result=True,
        )
        if result_issue is not None:
            return result_issue
    if report_path is not None:
        report_issue = _destructive_target_issue(
            report_path,
            role="report",
            allow_canonical_current_result=False,
        )
        if report_issue is not None:
            return report_issue
    return None


def _report_target_is_safe(result_path: Path, report_path: Path | None) -> bool:
    if report_path is None or _same_path(result_path, report_path):
        return False
    return _destructive_target_issue(
        report_path,
        role="report",
        allow_canonical_current_result=False,
    ) is None


def _hash_existing(path: Path) -> str | None:
    try:
        payload, _identity = _open_stable_regular_file(path)
        return hashlib.sha256(payload).hexdigest()
    except OSError:
        return None


def _failure_report(
    result_path: Path,
    source_revision: str | None,
    issue: VerificationIssue,
    *,
    test_fixture: bool = False,
) -> VerificationReport:
    digest = _hash_existing(result_path)
    document = {"source_revision": source_revision} if source_revision is not None else None
    return _report(
        result_path,
        document,
        digest,
        _hash_existing(result_path),
        [issue],
        test_fixture=test_fixture,
    )


def _write_optional_report(
    report_path: Path | None,
    report: VerificationReport,
) -> VerificationIssue | None:
    if report_path is None:
        return None
    target_issue = _destructive_target_issue(
        report_path,
        role="report",
        allow_canonical_current_result=False,
    )
    if target_issue is not None:
        return target_issue
    try:
        atomic_write_json(report_path, verification_report_document(report))
    except (TypeError, ValueError) as exc:
        return _issue(
            "ATOMIC_SERIALIZATION",
            str(report_path),
            f"cannot serialize operation report: {exc}",
        )
    except PermissionError as exc:
        return _issue(
            "ATOMIC_REPLACE",
            str(report_path),
            f"cannot replace operation report: {exc}",
        )
    except OSError as exc:
        return _issue(
            "ATOMIC_WRITE",
            str(report_path),
            f"cannot write operation report: {exc}",
        )
    return None


def _with_issue(
    report: VerificationReport,
    issue: VerificationIssue,
) -> VerificationReport:
    return report._replace(
        ok=False,
        published_result_sha256=None,
        issues=(*report.issues, issue),
    )


def _with_issue_once(
    report: VerificationReport,
    issue: VerificationIssue,
) -> VerificationReport:
    """Append one closing issue without duplicating an earlier identical finding."""

    identity = (issue.code, issue.location, issue.message)
    if any(
        (existing.code, existing.location, existing.message) == identity
        for existing in report.issues
    ):
        return report
    return _with_issue(report, issue)


def _remove_fresh_failed_update(
    result_path: Path,
    expected_sha256: str | None,
) -> VerificationIssue | None:
    """Remove only a fresh result whose current stable bytes are this run's output."""

    unsafe = _unsafe_target_component(result_path)
    if unsafe is not None:
        component, message = unsafe
        return _issue(
            "ATOMIC_WRITE",
            str(result_path),
            f"cannot remove fresh failed update through unsafe component {component}: {message}",
        )
    absolute = _lexical_absolute(result_path)
    try:
        payload, _identity = _open_stable_regular_file(absolute)
    except FileNotFoundError:
        return None
    except OSError as exc:
        return _issue(
            "ATOMIC_WRITE",
            str(result_path),
            f"cannot authenticate fresh failed update before removal: {exc}",
        )
    observed_sha256 = hashlib.sha256(payload).hexdigest()
    if expected_sha256 is None or observed_sha256 != expected_sha256:
        return _issue(
            "ATOMIC_WRITE",
            str(result_path),
            "refused to remove fresh failed update because its bytes no longer equal this run's output",
            expected=expected_sha256,
            observed=observed_sha256,
        )
    try:
        absolute.unlink()
    except OSError as exc:
        return _issue(
            "ATOMIC_WRITE",
            str(result_path),
            f"cannot remove fresh failed update: {exc}",
        )
    return None


def _print_report_summary(report: VerificationReport) -> None:
    payload = canonical_json_bytes(verification_report_document(report)) + b"\n"
    sys.stdout.buffer.write(payload)
    sys.stdout.buffer.flush()


def _head_revision(repo_root: Path) -> str:
    _git_top_level(repo_root)
    _reject_git_metadata_overrides(repo_root)
    completed = _git(repo_root, "rev-parse", "HEAD")
    if completed.returncode != 0:
        raise VerificationFailure(
            "SOURCE_REVISION_NOT_FOUND",
            "$repository",
            "cannot resolve current HEAD",
            observed=completed.stderr.decode("utf-8", errors="replace").strip(),
        )
    revision = completed.stdout.decode("ascii", errors="strict").strip().lower()
    if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        raise VerificationFailure(
            "SOURCE_REVISION_NOT_FOUND",
            "$repository",
            "current HEAD did not resolve to one full commit ID",
            observed=revision,
        )
    return revision


def _run_update(args: argparse.Namespace, *, test_fixture: bool = False) -> int:
    result_path: Path = args.update
    report_path: Path | None = args.report
    report_existed_at_entry = (
        report_path is not None and _lexical_absolute(report_path).exists()
    )
    if not test_fixture:
        try:
            _require_production_cli_runtime()
        except VerificationFailure as exc:
            report = _failure_report(
                result_path,
                args.source_revision,
                _issue(
                    exc.code,
                    exc.location,
                    str(exc),
                    expected=exc.expected,
                    observed=exc.observed,
                ),
                test_fixture=False,
            )
            if (
                not report_existed_at_entry
                and _report_target_is_safe(result_path, report_path)
            ):
                report_issue = _write_optional_report(report_path, report)
                if report_issue is not None:
                    report = _with_issue(report, report_issue)
            _print_report_summary(report)
            return 1
    conflict = _target_issue(result_path, report_path, update=True)
    if conflict is not None:
        report = _failure_report(
            result_path,
            args.source_revision,
            conflict,
            test_fixture=test_fixture,
        )
        if (
            not report_existed_at_entry
            and _report_target_is_safe(result_path, report_path)
        ):
            report_issue = _write_optional_report(report_path, report)
            if report_issue is not None:
                report = _with_issue(report, report_issue)
        _print_report_summary(report)
        return 1
    source_revision: str | None = args.source_revision
    report_existed_before = report_existed_at_entry
    run_evidence: Any | None = None
    run_tokens: Any | None = None
    document: dict[str, Any] | None = None
    result_stage: Any | None = None
    report_stage: Any | None = None
    receipt_token = _ACTIVE_TRANSACTION_RECEIPT_ID.set(uuid.uuid4().hex)
    stage_paths_token = _ACTIVE_OUTPUT_STAGE_PATHS.set(set())
    try:
        try:
            run_evidence, run_tokens = _acquire_run_evidence(
                REPO_ROOT,
                test_fixture=test_fixture,
            )
            if source_revision is None:
                source_revision = run_evidence.head_revision
            document = build_result(
                REPO_ROOT,
                source_revision,
                test_fixture=test_fixture,
            )
            if document["overall_status"] != "PASS":
                raise VerificationFailure(
                    "RESULT_STATUS_NOT_PASS",
                    "$.overall_status",
                    "update refuses to persist a non-PASS result",
                    expected="PASS",
                    observed=document["overall_status"],
                )
            protocol_profile = _load_manifest_policy(
                REPO_ROOT,
                test_fixture=test_fixture,
            )["protocol_profile"]
            required_ids = _required_check_ids(
                _load_claims_document(REPO_ROOT, protocol_profile),
                protocol_profile,
            )
            binding_issues = _check_binding_issues(document, required_ids)
            if binding_issues:
                first = binding_issues[0]
                raise VerificationFailure(
                    first.code,
                    first.location,
                    first.message,
                    expected=first.expected,
                    observed=first.observed,
                )
            final_manifest = build_manifest(
                REPO_ROOT,
                test_fixture=test_fixture,
            )
            if not _json_value_equal(final_manifest, document["manifest"]):
                raise VerificationFailure(
                    "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
                    "$manifest",
                    "governed input manifest changed between update M0 and staging",
                    expected=document["manifest"],
                    observed=final_manifest,
                )
            _require_source_binding(
                REPO_ROOT,
                source_revision,
                final_manifest,
                test_fixture=test_fixture,
            )
            late_conflict = _target_issue(result_path, report_path, update=True)
            if late_conflict is not None:
                raise VerificationFailure(
                    late_conflict.code,
                    late_conflict.location,
                    late_conflict.message,
                    expected=late_conflict.expected,
                    observed=late_conflict.observed,
                )
            _require_run_evidence_unchanged(REPO_ROOT, run_evidence)
            intended_hash = hashlib.sha256(canonical_json_bytes(document)).hexdigest()
            report = _report(
                result_path,
                document,
                intended_hash,
                intended_hash,
                [],
                test_fixture=test_fixture,
            )
        except VerificationFailure as exc:
            report = _failure_report(
                result_path,
                source_revision,
                _issue(
                    exc.code,
                    exc.location,
                    str(exc),
                    expected=exc.expected,
                    observed=exc.observed,
                ),
                test_fixture=test_fixture,
            )
        except (TypeError, NonFiniteJsonError) as exc:
            report = _failure_report(
                result_path,
                source_revision,
                _issue(
                    "ATOMIC_SERIALIZATION",
                    str(result_path),
                    f"update serialization failed: {exc}",
                ),
                test_fixture=test_fixture,
            )
        except PermissionError as exc:
            report = _failure_report(
                result_path,
                source_revision,
                _issue(
                    "ATOMIC_REPLACE",
                    str(result_path),
                    f"update replacement failed: {exc}",
                ),
                test_fixture=test_fixture,
            )
        except (OSError, ValueError) as exc:
            report = _failure_report(
                result_path,
                source_revision,
                _issue(
                    "ATOMIC_WRITE",
                    str(result_path),
                    f"update failed: {type(exc).__name__}: {exc}",
                ),
                test_fixture=test_fixture,
            )

        try:
            if report.ok:
                if document is None:
                    raise RuntimeError("successful update has no result document")
                result_stage = _stage_json_document(result_path, document)
            should_stage_report = report_path is not None and (
                report.ok or not report_existed_before
            )
            if should_stage_report:
                report_stage = _stage_json_document(
                    report_path,
                    verification_report_document(report),
                )
        except (TypeError, NonFiniteJsonError, ValueError) as exc:
            report = _with_issue_once(
                report,
                _issue(
                    "ATOMIC_SERIALIZATION",
                    str(report_path if report_path is not None else result_path),
                    f"transaction staging serialization failed: {exc}",
                ),
            )
        except PermissionError as exc:
            report = _with_issue_once(
                report,
                _issue(
                    "ATOMIC_REPLACE",
                    str(report_path if report_path is not None else result_path),
                    f"transaction staging failed: {exc}",
                ),
            )
        except OSError as exc:
            report = _with_issue_once(
                report,
                _issue(
                    "ATOMIC_WRITE",
                    str(report_path if report_path is not None else result_path),
                    f"transaction staging failed: {exc}",
                ),
            )

        staging_complete = (
            (not report.ok or result_stage is not None)
            and (
                report_path is None
                or (not report.ok and report_existed_before)
                or report_stage is not None
            )
        )
        if staging_complete and run_evidence is not None:
            try:
                _require_run_evidence_unchanged(REPO_ROOT, run_evidence)
            except VerificationFailure as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        exc.code,
                        exc.location,
                        str(exc),
                        expected=exc.expected,
                        observed=exc.observed,
                    ),
                )
                staging_complete = False

        if staging_complete and run_tokens is not None:
            try:
                _release_run_evidence(run_tokens)
                run_tokens = None
            except BaseException as exc:
                run_tokens = None
                report = _with_issue_once(
                    report,
                    _issue(
                        "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
                        "$transaction.close",
                        f"retained evidence cleanup failed before publication: {exc}",
                    ),
                )
                staging_complete = False

        if staging_complete and report.ok and result_stage is not None:
            try:
                _publish_staged_json(result_stage, retain_handle=True)
                expected_hash = result_stage.payload_sha256
                published_hash = _hash_existing(result_path)
                if published_hash != expected_hash:
                    raise OSError(
                        "published result hash does not equal its authenticated stage: "
                        f"expected {expected_hash}, observed {published_hash}"
                    )
            except PermissionError as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        "ATOMIC_REPLACE",
                        str(result_path),
                        f"result commit failed: {exc}",
                    ),
                )
                staging_complete = False
            except OSError as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        "ATOMIC_WRITE",
                        str(result_path),
                        f"result commit validation failed: {exc}",
                    ),
                )
                staging_complete = False

        if staging_complete and report_path is not None and report_stage is not None:
            try:
                _publish_staged_json(report_stage)
                report_stage = None
            except PermissionError as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        "ATOMIC_REPLACE",
                        str(report_path),
                        f"final report commit failed after result commit: {exc}",
                    ),
                )
            except OSError as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        "ATOMIC_WRITE",
                        str(report_path),
                        f"final report commit failed after result commit: {exc}",
                    ),
                )
        if result_stage is not None and result_stage._published:
            try:
                result_stage.validate()
            except OSError as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        "ATOMIC_WRITE",
                        str(result_path),
                        f"published result changed across report commit: {exc}",
                    ),
                )
    except BaseException:
        if run_tokens is not None:
            try:
                _release_run_evidence(run_tokens)
            except BaseException:
                pass
        raise
    finally:
        _run_cleanup_actions(
            (
                ("report stage", lambda: _cleanup_staged_json(report_stage)),
                ("result stage", lambda: _cleanup_staged_json(result_stage)),
                (
                    "run evidence",
                    lambda: _release_run_evidence(run_tokens)
                    if run_tokens is not None
                    else None,
                ),
                (
                    "output-stage context",
                    lambda: _ACTIVE_OUTPUT_STAGE_PATHS.reset(stage_paths_token),
                ),
                (
                    "transaction-receipt context",
                    lambda: _ACTIVE_TRANSACTION_RECEIPT_ID.reset(receipt_token),
                ),
            )
        )
    _print_report_summary(report)
    return 0 if report.ok else 1


def _run_verify(args: argparse.Namespace, *, test_fixture: bool = False) -> int:
    result_path: Path = args.verify
    report_path: Path | None = args.report
    report_existed_at_entry = (
        report_path is not None and _lexical_absolute(report_path).exists()
    )
    if not test_fixture:
        try:
            _require_production_cli_runtime()
        except VerificationFailure as exc:
            report = _failure_report(
                result_path,
                None,
                _issue(
                    exc.code,
                    exc.location,
                    str(exc),
                    expected=exc.expected,
                    observed=exc.observed,
                ),
                test_fixture=False,
            )
            if (
                not report_existed_at_entry
                and _report_target_is_safe(result_path, report_path)
            ):
                report_issue = _write_optional_report(report_path, report)
                if report_issue is not None:
                    report = _with_issue(report, report_issue)
            _print_report_summary(report)
            return 1
    conflict = _target_issue(result_path, report_path, update=False)
    if conflict is not None:
        report = _failure_report(
            result_path,
            None,
            conflict,
            test_fixture=test_fixture,
        )
        if (
            not report_existed_at_entry
            and _report_target_is_safe(result_path, report_path)
        ):
            report_issue = _write_optional_report(report_path, report)
            if report_issue is not None:
                report = _with_issue(report, report_issue)
        _print_report_summary(report)
        return 1
    run_evidence: Any | None = None
    run_tokens: Any | None = None
    result_guard: _WindowsExecutableGuard | None = None
    report_stage: Any | None = None
    receipt_token = _ACTIVE_TRANSACTION_RECEIPT_ID.set(uuid.uuid4().hex)
    stage_paths_token = _ACTIVE_OUTPUT_STAGE_PATHS.set(set())
    try:
        try:
            run_evidence, run_tokens = _acquire_run_evidence(
                REPO_ROOT,
                test_fixture=test_fixture,
            )
            result_guard = _WindowsExecutableGuard(
                result_path,
                "verification result transaction",
                issue_code="RESULT_CHANGED_DURING_VERIFY",
                subject="verification result",
            )
            report = verify_result(
                result_path,
                REPO_ROOT,
                test_fixture=test_fixture,
                _retained_result_guard=result_guard,
            )
        except VerificationFailure as exc:
            report = _failure_report(
                result_path,
                None,
                _issue(
                    exc.code,
                    exc.location,
                    str(exc),
                    expected=exc.expected,
                    observed=exc.observed,
                ),
                test_fixture=test_fixture,
            )
        except (OSError, ValueError, TypeError) as exc:
            report = _failure_report(
                result_path,
                None,
                _issue(
                    "RESULT_IO",
                    str(result_path),
                    f"verification failed before report staging: {exc}",
                ),
                test_fixture=test_fixture,
            )

        should_stage_report = report_path is not None and (
            report.ok or not report_existed_at_entry
        )
        if should_stage_report:
            try:
                report_stage = _stage_json_document(
                    report_path,
                    verification_report_document(report),
                )
            except (TypeError, NonFiniteJsonError, ValueError) as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        "ATOMIC_SERIALIZATION",
                        str(report_path),
                        f"verification report staging serialization failed: {exc}",
                    ),
                )
            except PermissionError as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        "ATOMIC_REPLACE",
                        str(report_path),
                        f"verification report staging failed: {exc}",
                    ),
                )
            except OSError as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        "ATOMIC_WRITE",
                        str(report_path),
                        f"verification report staging failed: {exc}",
                    ),
                )

        staging_complete = not should_stage_report or report_stage is not None
        if staging_complete and run_evidence is not None:
            try:
                _require_run_evidence_unchanged(REPO_ROOT, run_evidence)
            except VerificationFailure as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        exc.code,
                        exc.location,
                        str(exc),
                        expected=exc.expected,
                        observed=exc.observed,
                    ),
                )
                staging_complete = False

        if staging_complete and report.ok and result_guard is not None:
            try:
                held_payload, _held_snapshot = result_guard.read()
                held_hash = hashlib.sha256(held_payload).hexdigest()
                if (
                    held_hash != report.input_sha256_after
                    or held_hash != report.published_result_sha256
                ):
                    raise OSError(
                        "retained result hash no longer equals the staged success report"
                    )
            except (OSError, VerificationFailure) as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        "RESULT_CHANGED_DURING_VERIFY",
                        str(result_path),
                        f"retained result changed before report publication: {exc}",
                    ),
                )
                staging_complete = False

        if staging_complete and run_tokens is not None:
            try:
                _release_run_evidence(run_tokens)
                run_tokens = None
            except BaseException as exc:
                run_tokens = None
                report = _with_issue_once(
                    report,
                    _issue(
                        "GOVERNED_INPUT_CHANGED_DURING_VERIFY",
                        "$transaction.close",
                        f"retained evidence cleanup failed before report publication: {exc}",
                    ),
                )
                staging_complete = False

        if staging_complete and report_stage is not None:
            try:
                _publish_staged_json(report_stage)
                report_stage = None
            except PermissionError as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        "ATOMIC_REPLACE",
                        str(report_path),
                        f"verification report commit failed: {exc}",
                    ),
                )
            except OSError as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        "ATOMIC_WRITE",
                        str(report_path),
                        f"verification report commit failed: {exc}",
                    ),
                )
        if result_guard is not None:
            try:
                result_guard.read()
            except (OSError, VerificationFailure) as exc:
                report = _with_issue_once(
                    report,
                    _issue(
                        "RESULT_CHANGED_DURING_VERIFY",
                        str(result_path),
                        f"retained result changed across report commit: {exc}",
                    ),
                )
    except BaseException:
        if run_tokens is not None:
            try:
                _release_run_evidence(run_tokens)
            except BaseException:
                pass
        raise
    finally:
        _run_cleanup_actions(
            (
                ("report stage", lambda: _cleanup_staged_json(report_stage)),
                (
                    "run evidence",
                    lambda: _release_run_evidence(run_tokens)
                    if run_tokens is not None
                    else None,
                ),
                (
                    "result guard",
                    lambda: result_guard.close()
                    if result_guard is not None
                    else None,
                ),
                (
                    "output-stage context",
                    lambda: _ACTIVE_OUTPUT_STAGE_PATHS.reset(stage_paths_token),
                ),
                (
                    "transaction-receipt context",
                    lambda: _ACTIVE_TRANSACTION_RECEIPT_ID.reset(receipt_token),
                ),
            )
        )
    _print_report_summary(report)
    return 0 if report.ok else 1


def main(
    argv: list[str] | None = None,
    *,
    test_fixture: bool = False,
) -> int:
    _expected_protocol_profile(test_fixture)
    args = parse_args(argv)
    return (
        _run_update(args, test_fixture=test_fixture)
        if args.update is not None
        else _run_verify(args, test_fixture=test_fixture)
    )


if __name__ == "__main__":
    raise SystemExit(main())
