"""Atomic publication and non-clobbering ownership of experiment runs."""

from __future__ import annotations

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
        run_dir = (
            config.output.root
            / _sanitize_run_name(config.run.name)
            / f"{config_hash}-{config.run.seed}"
        )
        if run_dir.exists():
            if (run_dir / "manifest.json").is_file():
                raise FileExistsError(f"complete run exists: {run_dir}")
            raise FileExistsError(f"run path already exists: {run_dir}")
        run_dir.mkdir(parents=True, exist_ok=False)

        store = cls(run_dir=run_dir, config_hash=config_hash)
        resolved_config = json.loads(resolved_config_json)
        store.write_json(
            "config",
            {"config_hash": config_hash, "resolved_config": resolved_config},
        )
        recorded_provenance = dict(provenance)
        supplied_hash = recorded_provenance.setdefault("config_hash", config_hash)
        if supplied_hash != config_hash:
            raise ValueError("provenance config_hash does not match resolved configuration")
        store.write_json(
            "manifest",
            {
                "config_hash": config_hash,
                "provenance": recorded_provenance,
                "artifacts": {"config.json": "complete", "manifest.json": "complete"},
                "complete": True,
            },
        )
        return store

    def write_json(self, name: str, payload: object) -> Path:
        path = self.run_dir / _artifact_filename(name, ".json")
        _reject_existing_artifact(path)
        _atomic_json(path, payload)
        return path

    def write_npz(self, name: str, arrays: Mapping[str, np.ndarray]) -> Path:
        path = self.run_dir / _artifact_filename(name, ".npz")
        _reject_existing_artifact(path)
        _atomic_npz(path, arrays)
        return path


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
