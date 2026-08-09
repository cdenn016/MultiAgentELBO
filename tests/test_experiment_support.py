from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from multiagent_elbo.experiment_support import (
    lower_bounded_metric,
    readonly_array,
    target_metric,
)
from multiagent_elbo.rendering import validated_renderer_status


def test_target_and_lower_bound_metrics_keep_established_json_schema():
    exact = target_metric(
        1.0e-13,
        1.0e-10,
        target=0.0,
        interpretation="identity",
        theorem_status="established_conditional_identity",
    )
    control = lower_bounded_metric(
        0.2,
        1.0e-10,
        lower_bound=0.1,
        interpretation="negative control",
        theorem_status="negative_control",
    )

    assert asdict(exact).keys() == {
        "value", "tolerance", "status", "interpretation",
        "assessment_scope", "theorem_status",
    }
    assert exact.status == "pass"
    assert control.status == "pass"


def test_readonly_array_makes_a_c_contiguous_float64_copy():
    source = np.array([[1, 2], [3, 4]], dtype=np.int64, order="F")

    result = readonly_array(source)

    assert result.dtype == np.float64
    assert result.flags.c_contiguous
    assert not result.flags.writeable
    source[0, 0] = 99
    assert result[0, 0] == 1.0
    with pytest.raises(ValueError):
        result[0, 0] = 0.0


def _renderer_manifest(
    run_dir: Path,
    output_dir: Path,
    requested: tuple[str, ...],
    *,
    status: str = "complete",
) -> SimpleNamespace:
    output_dir.mkdir(parents=True, exist_ok=True)
    figures: list[dict[str, str]] = []
    message: str | None = None
    if status == "complete":
        for name in requested:
            png = output_dir / f"{name}.png"
            pdf = output_dir / f"{name}.pdf"
            png.write_bytes(b"\x89PNG\r\n\x1a\nfixture")
            pdf.write_bytes(b"%PDF-1.7\nfixture")
            figures.append(
                {
                    "name": name,
                    "png": png.name,
                    "png_sha256": hashlib.sha256(png.read_bytes()).hexdigest(),
                    "pdf": pdf.name,
                    "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
                }
            )
    else:
        message = "renderer reported failure"
    manifest_path = output_dir / "figure-manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "figures": figures,
                "message": message,
                "requested": list(requested),
                "run_dir": str(run_dir.resolve()),
                "status": status,
            }
        ),
        encoding="utf-8",
    )
    return SimpleNamespace(
        status=status,
        run_dir=run_dir,
        output_dir=output_dir,
        requested=requested,
        manifest_path=manifest_path,
    )


def test_validated_renderer_status_accepts_backed_complete_and_failed_manifests(
    tmp_path: Path,
):
    run_dir = tmp_path / "run"
    output_dir = tmp_path / "figures"
    requested = ("first", "second")
    run_dir.mkdir()

    complete = _renderer_manifest(run_dir, output_dir, requested)
    assert validated_renderer_status(complete, run_dir, output_dir, requested) == "complete"

    failed = _renderer_manifest(run_dir, output_dir, requested, status="failed")
    assert validated_renderer_status(failed, run_dir, output_dir, requested) == "failed"


@pytest.mark.parametrize(
    "forge",
    [
        "wrong_run_directory",
        "wrong_request_ordering",
        "uncontained_manifest_path",
        "wrong_image_sha256",
        "missing_image",
        "empty_failure_message",
        "status_only_object",
    ],
)
def test_validated_renderer_status_rejects_unbacked_renderer_output(
    tmp_path: Path, forge: str
):
    run_dir = tmp_path / "run"
    output_dir = tmp_path / "figures"
    requested = ("first", "second")
    run_dir.mkdir()
    manifest = _renderer_manifest(run_dir, output_dir, requested)

    if forge == "wrong_run_directory":
        manifest.run_dir = tmp_path / "other-run"
    elif forge == "wrong_request_ordering":
        manifest.requested = tuple(reversed(requested))
    elif forge == "uncontained_manifest_path":
        outside = tmp_path / "outside.json"
        outside.write_text(manifest.manifest_path.read_text("utf-8"), encoding="utf-8")
        manifest.manifest_path = outside
    elif forge == "wrong_image_sha256":
        payload = json.loads(manifest.manifest_path.read_text("utf-8"))
        payload["figures"][0]["png_sha256"] = "0" * 64
        manifest.manifest_path.write_text(json.dumps(payload), encoding="utf-8")
    elif forge == "missing_image":
        (output_dir / "first.png").unlink()
    elif forge == "empty_failure_message":
        manifest = _renderer_manifest(run_dir, output_dir, requested, status="failed")
        payload = json.loads(manifest.manifest_path.read_text("utf-8"))
        payload["message"] = ""
        manifest.manifest_path.write_text(json.dumps(payload), encoding="utf-8")
    else:
        manifest = SimpleNamespace(status="complete")

    with pytest.raises(ValueError, match="unbacked|invalid status"):
        validated_renderer_status(manifest, run_dir, output_dir, requested)
