"""Atomic publication and non-clobbering ownership of experiment runs."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Mapping

import numpy as np

from .config import ExperimentConfig, canonical_config_json


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
        for name in declared_artifacts:
            filename = _artifact_filename(name, "")
            if not (self.run_dir / filename).is_file():
                raise FileNotFoundError(
                    f"declared artifact does not exist: {filename}"
                )

        inventory = {
            path.name: "complete"
            for path in sorted(self.run_dir.iterdir(), key=lambda item: item.name)
            if path.is_file() and not path.name.endswith(".tmp")
        }
        inventory["manifest.json"] = "complete"
        manifest["artifacts"] = inventory
        manifest["complete"] = True
        path = self.run_dir / "manifest.json"
        _atomic_json(path, manifest)
        return path

    def _require_incomplete(self) -> dict[str, object]:
        manifest_path = self.run_dir / "manifest.json"
        if not manifest_path.is_file():
            raise RuntimeError(f"run manifest is missing: {manifest_path}")
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
    candidate = Path(name)
    if candidate.name != name or name in {"", ".", ".."}:
        raise ValueError("artifact name must be a single filename")
    return name if name.endswith(suffix) else f"{name}{suffix}"


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
