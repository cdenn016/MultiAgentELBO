"""Deterministic random streams and read-only execution provenance."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import platform
from pathlib import Path
import subprocess
import sys

import numpy as np
import scipy


_STREAM_NAMES = ("problem", "recognition", "controls", "figures")
_GIT_STATUS_FORMAT = "git-status-porcelain-v1-z-untracked-files-all"


@dataclass(frozen=True)
class RngStreams:
    """Independent named generators derived from one explicit seed."""

    seed: int
    problem: np.random.Generator
    recognition: np.random.Generator
    controls: np.random.Generator
    figures: np.random.Generator
    spawn_keys: dict[str, tuple[int, ...]]

    @classmethod
    def from_seed(cls, seed: int) -> "RngStreams":
        if type(seed) is bool or type(seed) is not int:
            raise TypeError("seed must be an int, not bool" if type(seed) is bool else "seed must be an int")
        sequence = np.random.SeedSequence(seed)
        children = sequence.spawn(len(_STREAM_NAMES))
        generators = [np.random.default_rng(child) for child in children]
        return cls(
            seed=seed,
            problem=generators[0],
            recognition=generators[1],
            controls=generators[2],
            figures=generators[3],
            spawn_keys={name: child.spawn_key for name, child in zip(_STREAM_NAMES, children)},
        )

    def provenance(self) -> dict[str, object]:
        return {
            "seed": self.seed,
            "named_streams": {
                name: list(self.spawn_keys[name]) for name in _STREAM_NAMES
            },
        }


def collect_provenance(
    repo_root: Path, theory_root: Path, config_hash: str, streams: RngStreams
) -> dict[str, object]:
    """Collect current, non-mutating environment and source identity metadata."""
    repo_root = Path(repo_root)
    theory_root = Path(theory_root)
    git_status = _git_status_bytes(repo_root)
    theory_exists = theory_root.is_dir()
    theory_sha256 = _tree_sha256(theory_root) if theory_exists else None
    return {
        "config_hash": config_hash,
        "git_commit": _git_output(repo_root, "rev-parse", "HEAD"),
        "git_dirty": None if git_status is None else bool(git_status),
        "git_status_format": _GIT_STATUS_FORMAT,
        "git_status_sha256": (
            None if git_status is None else hashlib.sha256(git_status).hexdigest()
        ),
        "theory_root": str(theory_root),
        "theory_exists": theory_exists,
        "theory_sha256": theory_sha256,
        "input_hashes": {
            "resolved_config_sha256": config_hash,
            "theory_tree_sha256": theory_sha256,
        },
        "python_version": sys.version,
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "platform": platform.platform(),
        "rng": streams.provenance(),
    }


def _git_output(repo_root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True,
            check=False,
            text=True,
        )
    except OSError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def _git_status_bytes(repo_root: Path) -> bytes | None:
    """Return the exact stable porcelain-v1 status byte stream, if available."""
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(repo_root),
                "status",
                "--porcelain=v1",
                "-z",
                "--untracked-files=all",
            ],
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    return result.stdout if result.returncode == 0 else None


def _git_dirty(repo_root: Path) -> bool | None:
    status = _git_status_bytes(repo_root)
    return None if status is None else bool(status)


def _tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.is_dir():
        return digest.hexdigest()
    for path in sorted(
        root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()
    ):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()
