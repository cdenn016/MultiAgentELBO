from __future__ import annotations

import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ALLOWED_CONTROLS = {0x0A, 0x0D}


def _tracked_markdown_paths() -> list[Path]:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    return [
        REPO_ROOT / os.fsdecode(raw_path)
        for raw_path in completed.stdout.split(b"\0")
        if raw_path and Path(os.fsdecode(raw_path)).suffix.lower() in {".md", ".markdown"}
    ]


def test_tracked_markdown_has_no_forbidden_c0_controls() -> None:
    violations: list[str] = []
    for path in _tracked_markdown_paths():
        for offset, value in enumerate(path.read_bytes()):
            if value < 0x20 and value not in ALLOWED_CONTROLS:
                relative_path = path.relative_to(REPO_ROOT).as_posix()
                violations.append(f"{relative_path}: byte {offset}: 0x{value:02x}")

    assert not violations, "Forbidden C0 control bytes found:\n" + "\n".join(violations)
