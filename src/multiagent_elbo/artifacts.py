"""Atomic publication and non-clobbering ownership of experiment runs."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Mapping

import numpy as np

from .config import ExperimentConfig, canonical_config_json


_CORE_ARTIFACTS = frozenset({"config.json", "manifest.json"})
_CORE_ARTIFACT_KEYS = frozenset(name.casefold() for name in _CORE_ARTIFACTS)
_PORTABLE_FILENAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_WINDOWS_RESERVED_BASENAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{index}" for index in range(1, 10)}
    | {f"LPT{index}" for index in range(1, 10)}
)


@dataclass(frozen=True)
class RunStore:
    """The owned directory for a single immutable configuration run."""

    run_dir: Path
    config_hash: str

    @classmethod
    def create(
        cls, config: ExperimentConfig, provenance: Mapping[str, object]
    ) -> "RunStore":
        resolved_config_json = canonical_config_json(config)
        config_hash = hashlib.sha256(resolved_config_json.encode("utf-8")).hexdigest()
        recorded_provenance = dict(provenance)
        supplied_hash = recorded_provenance.setdefault("config_hash", config_hash)
        if supplied_hash != config_hash:
            raise ValueError("provenance config_hash does not match resolved configuration")
        run_dir = (
            config.output.root
            / _sanitize_run_name(config.run.name)
            / f"{config_hash}-{config.run.seed}"
        )
        if run_dir.exists():
            if _manifest_is_complete(run_dir / "manifest.json"):
                raise FileExistsError(f"complete run exists: {run_dir}")
            raise FileExistsError(f"run path already exists: {run_dir}")
        run_dir.mkdir(parents=True, exist_ok=False)

        store = cls(run_dir=run_dir, config_hash=config_hash)
        resolved_config = json.loads(resolved_config_json)
        _atomic_json(
            run_dir / "config.json",
            {"config_hash": config_hash, "resolved_config": resolved_config},
        )
        _atomic_json(
            run_dir / "manifest.json",
            {
                "config_hash": config_hash,
                "provenance": recorded_provenance,
                "artifacts": {
                    "config.json": "complete",
                    "manifest.json": "incomplete",
                },
                "complete": False,
            },
        )
        return store

    def write_json(self, name: str, payload: object) -> Path:
        self._require_incomplete()
        path = self.run_dir / _artifact_filename(name, ".json")
        _reject_existing_artifact(path)
        _atomic_json(path, payload)
        return path

    def write_npz(self, name: str, arrays: Mapping[str, np.ndarray]) -> Path:
        self._require_incomplete()
        path = self.run_dir / _artifact_filename(name, ".npz")
        _reject_existing_artifact(path)
        _atomic_npz(path, arrays)
        return path

    def finalize(self, declared_artifacts: Iterable[str]) -> Path:
        manifest = self._require_incomplete()
        declared_names = _materialize_declarations(declared_artifacts)
        resolved_run_dir = _strict_resolved_run_dir(self.run_dir)
        config_path = _require_owned_regular_file(
            self.run_dir / "config.json",
            resolved_run_dir,
            missing_label="required",
        )
        _require_owned_regular_file(
            self.run_dir / "manifest.json",
            resolved_run_dir,
            missing_label="required",
        )
        _validate_config_identity(config_path, self.config_hash)

        for filename in declared_names:
            _require_owned_regular_file(
                self.run_dir / filename,
                resolved_run_dir,
                missing_label="declared",
            )

        expected_names = _CORE_ARTIFACTS | set(declared_names)
        actual_entries = {entry.name for entry in self.run_dir.iterdir()}
        undeclared_entries = sorted(actual_entries - expected_names)
        if undeclared_entries:
            raise ValueError(f"undeclared run entry: {undeclared_entries[0]}")

        inventory = {name: "complete" for name in sorted(expected_names)}
        manifest["artifacts"] = inventory
        manifest["complete"] = True
        path = self.run_dir / "manifest.json"
        _atomic_json(path, manifest)
        return path

    def _require_incomplete(self) -> dict[str, object]:
        manifest_path = self.run_dir / "manifest.json"
        resolved_run_dir = _strict_resolved_run_dir(self.run_dir)
        try:
            manifest_path = _require_owned_regular_file(
                manifest_path, resolved_run_dir, missing_label="required"
            )
        except FileNotFoundError as error:
            raise RuntimeError(f"run manifest is missing: {manifest_path}") from error
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise RuntimeError(f"run manifest is invalid: {manifest_path}")
        if manifest.get("config_hash") != self.config_hash:
            raise RuntimeError("run manifest config_hash does not match run store")
        if manifest.get("complete") is not False:
            raise RuntimeError(f"run is complete: {self.run_dir}")
        return manifest


def _sanitize_run_name(name: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip(".-_")
    return sanitized or "run"


def _artifact_filename(name: str, suffix: str) -> str:
    if type(name) is not str:
        raise ValueError(f"invalid artifact filename: {name!r}")
    filename = name if name.endswith(suffix) else f"{name}{suffix}"
    if (
        _PORTABLE_FILENAME.fullmatch(filename) is None
        or filename.endswith(".")
        or filename.split(".", 1)[0].upper() in _WINDOWS_RESERVED_BASENAMES
    ):
        raise ValueError(f"invalid artifact filename: {name}")
    return filename


def _materialize_declarations(declared_artifacts: Iterable[str]) -> tuple[str, ...]:
    names = tuple(_artifact_filename(name, "") for name in declared_artifacts)
    seen: set[str] = set()
    for name in names:
        portable_key = name.casefold()
        if portable_key in _CORE_ARTIFACT_KEYS:
            raise ValueError(f"core artifact must not be declared: {name}")
        if portable_key in seen:
            raise ValueError(f"duplicate artifact declaration: {name}")
        seen.add(portable_key)
    return names


def _strict_resolved_run_dir(run_dir: Path) -> Path:
    try:
        if _is_reparse_path(run_dir):
            raise ValueError(f"run directory must not be a symlink or reparse path: {run_dir}")
        resolved = run_dir.resolve(strict=True)
    except FileNotFoundError as error:
        raise RuntimeError(f"run directory is missing: {run_dir}") from error
    if not resolved.is_dir():
        raise RuntimeError(f"run path is not a directory: {run_dir}")
    return resolved


def _require_owned_regular_file(
    path: Path, resolved_run_dir: Path, *, missing_label: str
) -> Path:
    try:
        path_stat = path.lstat()
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"{missing_label} artifact does not exist: {path.name}"
        ) from error
    if _is_reparse_stat(path, path_stat):
        raise ValueError(
            f"artifact must not be a symlink or reparse path: {path.name}"
        )
    if not stat.S_ISREG(path_stat.st_mode):
        raise ValueError(f"artifact is not a regular file: {path.name}")
    resolved = path.resolve(strict=True)
    if resolved.parent != resolved_run_dir:
        raise ValueError(f"artifact is not owned by run directory: {path.name}")
    return resolved


def _is_reparse_path(path: Path) -> bool:
    try:
        return _is_reparse_stat(path, path.lstat())
    except FileNotFoundError:
        return False


def _is_reparse_stat(path: Path, path_stat: os.stat_result) -> bool:
    if stat.S_ISLNK(path_stat.st_mode):
        return True
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    file_attributes = getattr(path_stat, "st_file_attributes", 0)
    if reparse_flag and file_attributes & reparse_flag:
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(is_junction is not None and is_junction())


def _validate_config_identity(path: Path, config_hash: str) -> None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or not isinstance(
            payload.get("resolved_config"), dict
        ):
            raise ValueError("invalid config payload")
        canonical = json.dumps(
            payload["resolved_config"],
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError("config.json identity does not match run") from error
    recomputed_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    if payload.get("config_hash") != config_hash or recomputed_hash != config_hash:
        raise RuntimeError("config.json identity does not match run")


def _reject_existing_artifact(path: Path) -> None:
    if path.exists():
        raise FileExistsError(f"artifact already exists: {path.name}")


def _manifest_is_complete(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return isinstance(manifest, dict) and manifest.get("complete") is True


def _atomic_json(path: Path, payload: object) -> None:
    _atomic_write(path, lambda handle: json.dump(payload, handle, sort_keys=True, separators=(",", ":"), allow_nan=False))


def _atomic_npz(path: Path, arrays: Mapping[str, np.ndarray]) -> None:
    def write(handle: object) -> None:
        np.savez(handle, **arrays)

    _atomic_write(path, write, binary=True)


def _atomic_write(path: Path, write: object, *, binary: bool = False) -> None:
    mode = "w+b" if binary else "w"
    kwargs: dict[str, object] = {"mode": mode, "dir": path.parent, "prefix": f".{path.name}-", "suffix": ".tmp", "delete": False}
    if not binary:
        kwargs["encoding"] = "utf-8"
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(**kwargs) as handle:  # type: ignore[arg-type]
            temporary_name = handle.name
            write(handle)  # type: ignore[operator]
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)
        raise
