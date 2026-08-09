"""Fail-closed validation for renderer evidence published beside a run."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Literal


RendererStatus = Literal["complete", "failed"]


def validated_renderer_status(
    manifest: object,
    run_dir: Path,
    output_dir: Path,
    requested: tuple[str, ...],
) -> RendererStatus:
    """Return a renderer status only when its manifest backs every claim."""
    try:
        status = getattr(manifest, "status")
    except Exception as error:
        raise ValueError("renderer returned unbacked status") from error
    if type(status) is not str or status not in {"complete", "failed"}:
        raise ValueError(f"renderer returned invalid status: {status!r}")

    try:
        returned_run_dir = Path(getattr(manifest, "run_dir")).resolve(strict=True)
        returned_output_dir = Path(getattr(manifest, "output_dir")).resolve(
            strict=True
        )
        returned_requested = tuple(getattr(manifest, "requested"))
        manifest_path = Path(getattr(manifest, "manifest_path")).resolve(strict=True)
        resolved_run_dir = run_dir.resolve(strict=True)
        resolved_output_dir = output_dir.resolve(strict=True)
    except Exception as error:
        raise ValueError(f"renderer returned unbacked {status!r} status") from error

    if (
        returned_run_dir != resolved_run_dir
        or returned_output_dir != resolved_output_dir
        or returned_requested != requested
        or manifest_path.parent != resolved_output_dir
        or manifest_path.name not in {"figure-manifest.json", "figure-failure.json"}
        or not manifest_path.is_file()
    ):
        raise ValueError(f"renderer returned unbacked {status!r} status")

    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as error:
        raise ValueError(f"renderer returned unbacked {status!r} status") from error

    if (
        not isinstance(payload, dict)
        or payload.get("status") != status
        or payload.get("run_dir") != str(resolved_run_dir)
        or payload.get("requested") != list(requested)
        or not isinstance(payload.get("figures"), list)
    ):
        raise ValueError(f"renderer returned unbacked {status!r} status")

    figures = payload["figures"]
    if status == "failed":
        if figures or not isinstance(payload.get("message"), str) or not payload[
            "message"
        ].strip():
            raise ValueError("renderer returned unbacked 'failed' status")
        return "failed"

    if payload.get("message") is not None or len(figures) != len(requested):
        raise ValueError("renderer returned unbacked 'complete' status")
    for expected_name, record in zip(requested, figures, strict=True):
        if not isinstance(record, dict) or record.get("name") != expected_name:
            raise ValueError("renderer returned unbacked 'complete' status")
        _validate_publication_record(record, resolved_output_dir)
    return "complete"


def _validate_publication_record(record: dict[str, object], output_dir: Path) -> None:
    for kind in ("png", "pdf"):
        try:
            filename = record.get(kind)
            publication = (
                (output_dir / filename).resolve(strict=True)
                if type(filename) is str
                else None
            )
            if (
                type(filename) is not str
                or Path(filename).name != filename
                or publication is None
                or publication.parent != output_dir
                or not publication.is_file()
                or publication.stat().st_size == 0
            ):
                raise ValueError("invalid publication")
            actual_sha256 = hashlib.sha256(publication.read_bytes()).hexdigest()
            if record.get(f"{kind}_sha256") != actual_sha256:
                raise ValueError("invalid publication hash")
        except Exception as error:
            raise ValueError("renderer returned unbacked 'complete' status") from error


def record_figure_failure_safely(
    run_dir: Path, output_dir: Path, message: str
) -> None:
    """Best-effort renderer failure reporting that cannot alter numerical results."""
    try:
        from .figures import record_figure_failure

        record_figure_failure(run_dir, output_dir, message)
    except Exception:
        pass


__all__ = [
    "RendererStatus",
    "record_figure_failure_safely",
    "validated_renderer_status",
]
