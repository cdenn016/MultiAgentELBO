from __future__ import annotations

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import re
import struct

import matplotlib
import numpy as np
import pytest

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.figures import FigureManifest, record_figure_failure, render_run
from multiagent_elbo.finite.experiment import run_finite_experiment


def _finite_config(root: Path) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "figure fixture", "seed": 20260808},
        {"experiment": "finite_exact", "retained_interaction_order": 2},
        {
            "dtype": "float64",
            "atol": 1e-10,
            "rtol": 1e-9,
            "min_spd_rcond": 1e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(root),
            "collect_diagnostics": False,
            "render_figures": False,
        },
    )


def _png_pixels_per_meter(path: Path) -> tuple[int, int, int]:
    payload = path.read_bytes()
    assert payload.startswith(b"\x89PNG\r\n\x1a\n")
    offset = 8
    while offset < len(payload):
        length = struct.unpack(">I", payload[offset : offset + 4])[0]
        chunk_type = payload[offset + 4 : offset + 8]
        chunk = payload[offset + 8 : offset + 8 + length]
        if chunk_type == b"pHYs":
            return struct.unpack(">IIB", chunk)
        offset += 12 + length
    raise AssertionError("PNG has no physical-resolution metadata")


def _png_dimensions(path: Path) -> tuple[int, int]:
    payload = path.read_bytes()
    assert payload[12:16] == b"IHDR"
    return struct.unpack(">II", payload[16:24])


def _pdf_media_box(path: Path) -> tuple[float, float]:
    match = re.search(
        rb"/MediaBox\s*\[\s*0\s+0\s+([0-9.]+)\s+([0-9.]+)\s*\]",
        path.read_bytes(),
    )
    assert match is not None
    return float(match.group(1)), float(match.group(2))


def _write_gaussian_run(run_dir: Path) -> None:
    run_dir.mkdir(parents=True)
    metrics = {
        "GAU-01_generalized_spectrum_residual": {
            "value": 1.0e-15,
            "tolerance": 1.0e-9,
            "status": "pass",
            "interpretation": "fixture",
            "theorem_status": "established_conditional_identity",
        }
    }
    (run_dir / "metrics.json").write_text(
        json.dumps(metrics, sort_keys=True, separators=(",", ":")), "utf-8"
    )
    with (run_dir / "arrays.npz").open("wb") as handle:
        np.savez(
            handle,
            generalized_eigenvalues=np.array([0.0, 0.0, 0.4, 0.5]),
            transformed_generalized_eigenvalues=np.array(
                [0.0, 0.0, 0.4, 0.5]
            ),
            expected_generalized_eigenvalues=np.array([0.0, 0.0, 0.4, 0.5]),
        )
    manifest = {
        "complete": True,
        "artifacts": {
            "arrays.npz": "complete",
            "config.json": "complete",
            "manifest.json": "complete",
            "metrics.json": "complete",
        },
    }
    (run_dir / "config.json").write_text("{}", "utf-8")
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")), "utf-8"
    )


def test_finite_replay_uses_finalized_saved_artifacts_and_local_style(tmp_path: Path):
    run = run_finite_experiment(_finite_config(tmp_path / "runs"))
    output_dir = tmp_path / "figures"
    before = {
        "font.size": matplotlib.rcParams["font.size"],
        "axes.titlesize": matplotlib.rcParams["axes.titlesize"],
        "axes.spines.top": matplotlib.rcParams["axes.spines.top"],
    }

    manifest = render_run(
        run.run_dir, output_dir, requested=("finite_identity",)
    )

    assert isinstance(manifest, FigureManifest)
    assert manifest.status == "complete"
    assert manifest.requested == ("finite_identity",)
    assert manifest.message is None
    assert len(manifest.figures) == 1
    figure = manifest.figures[0]
    assert figure.name == "finite_identity"
    assert figure.png.read_bytes().startswith(b"\x89PNG")
    assert figure.pdf.read_bytes().startswith(b"%PDF")
    x_ppm, y_ppm, unit = _png_pixels_per_meter(figure.png)
    assert unit == 1
    assert x_ppm == pytest.approx(11811, abs=1)
    assert y_ppm == pytest.approx(11811, abs=1)
    assert _png_dimensions(figure.png)[0] == 1050
    assert _pdf_media_box(figure.pdf)[0] == pytest.approx(252.0)
    assert json.loads(manifest.manifest_path.read_text("utf-8"))["caption"] == (
        "n=1 exact fixture"
    )
    assert before == {
        "font.size": matplotlib.rcParams["font.size"],
        "axes.titlesize": matplotlib.rcParams["axes.titlesize"],
        "axes.spines.top": matplotlib.rcParams["axes.spines.top"],
    }


def test_gaussian_replay_renders_matched_saved_generalized_spectra(tmp_path: Path):
    run_dir = tmp_path / "gaussian-run"
    _write_gaussian_run(run_dir)

    manifest = render_run(
        run_dir, tmp_path / "figures", requested=("gaussian_spectrum",)
    )

    assert manifest.status == "complete"
    assert manifest.figures[0].name == "gaussian_spectrum"
    assert manifest.figures[0].png.is_file()
    assert manifest.figures[0].pdf.is_file()


def test_complete_figure_output_is_immutable_under_a_later_renderer_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.figures as figures_module

    run = run_finite_experiment(_finite_config(tmp_path / "runs"))
    output_dir = tmp_path / "figures"
    complete = render_run(
        run.run_dir, output_dir, requested=("finite_identity",)
    )
    image_bytes = complete.figures[0].png.read_bytes()
    manifest_bytes = complete.manifest_path.read_bytes()

    def fail_renderer(*args, **kwargs):
        raise RuntimeError("injected renderer failure")

    monkeypatch.setattr(figures_module, "_render_requested_figure", fail_renderer)
    replay = render_run(
        run.run_dir, output_dir, requested=("finite_identity",)
    )

    assert replay.status == "complete"
    assert replay.message is None
    assert complete.figures[0].png.read_bytes() == image_bytes
    assert complete.manifest_path.read_bytes() == manifest_bytes
    assert not (output_dir / "figure-failure.json").exists()


def test_injected_renderer_failure_on_fresh_output_publishes_no_image(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.figures as figures_module

    run = run_finite_experiment(_finite_config(tmp_path / "runs"))

    def fail_renderer(*args, **kwargs):
        raise RuntimeError("injected renderer failure")

    monkeypatch.setattr(figures_module, "_render_requested_figure", fail_renderer)
    failed = render_run(
        run.run_dir, tmp_path / "figures", requested=("finite_identity",)
    )

    assert failed.status == "failed"
    assert failed.message == "injected renderer failure"
    assert list((tmp_path / "figures").glob("*.png")) == []
    assert list((tmp_path / "figures").glob("*.pdf")) == []


def test_same_saved_inputs_render_byte_identical_png_and_pdf(tmp_path: Path):
    run = run_finite_experiment(_finite_config(tmp_path / "runs"))

    first = render_run(
        run.run_dir, tmp_path / "figures-first", requested=("finite_identity",)
    )
    second = render_run(
        run.run_dir, tmp_path / "figures-second", requested=("finite_identity",)
    )

    assert first.figures[0].png.read_bytes() == second.figures[0].png.read_bytes()
    assert first.figures[0].pdf.read_bytes() == second.figures[0].pdf.read_bytes()


def test_failure_record_is_frozen_and_does_not_touch_numerical_artifacts(
    tmp_path: Path,
):
    run = run_finite_experiment(_finite_config(tmp_path / "runs"))
    metrics_bytes = (run.run_dir / "metrics.json").read_bytes()
    manifest_bytes = (run.run_dir / "manifest.json").read_bytes()

    failure = record_figure_failure(
        run.run_dir, tmp_path / "figures", "renderer unavailable"
    )

    assert failure.status == "failed"
    assert failure.figures == ()
    assert failure.message == "renderer unavailable"
    with pytest.raises(FrozenInstanceError):
        failure.status = "complete"  # type: ignore[misc]
    assert (run.run_dir / "metrics.json").read_bytes() == metrics_bytes
    assert (run.run_dir / "manifest.json").read_bytes() == manifest_bytes


def test_replay_refuses_an_incomplete_numerical_run(tmp_path: Path):
    run_dir = tmp_path / "incomplete"
    run_dir.mkdir()
    (run_dir / "manifest.json").write_text('{"complete":false}', "utf-8")

    manifest = render_run(
        run_dir, tmp_path / "figures", requested=("finite_identity",)
    )

    assert manifest.status == "failed"
    assert manifest.figures == ()
    assert "finalized" in str(manifest.message)


def test_failure_status_survives_when_the_failure_manifest_cannot_be_written(
    tmp_path: Path,
):
    blocked_output = tmp_path / "blocked-output"
    blocked_output.write_text("not a directory", "utf-8")

    failure = record_figure_failure(
        tmp_path / "finalized-run", blocked_output, "renderer failed"
    )

    assert failure.status == "failed"
    assert failure.manifest_path is None
    assert "renderer failed" in str(failure.message)
    assert "failure manifest unavailable" in str(failure.message)


def test_second_final_image_replace_failure_rolls_back_the_whole_bundle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.figures as figures_module

    run = run_finite_experiment(_finite_config(tmp_path / "runs"))
    output_dir = tmp_path / "figures"
    real_replace = figures_module.os.replace
    final_image_replacements = 0

    def fail_second_final_image_replace(source, destination):
        nonlocal final_image_replacements
        final_path = Path(destination)
        if final_path.parent == output_dir and final_path.suffix in {".png", ".pdf"}:
            final_image_replacements += 1
            if final_image_replacements == 2:
                raise OSError("injected second replace failure")
        return real_replace(source, destination)

    monkeypatch.setattr(figures_module.os, "replace", fail_second_final_image_replace)

    result = render_run(
        run.run_dir, output_dir, requested=("finite_identity",)
    )

    assert result.status == "failed"
    assert "injected second replace failure" in str(result.message)
    assert list(output_dir.glob("*.png")) == []
    assert list(output_dir.glob("*.pdf")) == []
    failure = json.loads((output_dir / "figure-manifest.json").read_text("utf-8"))
    assert failure["status"] == "failed"


@pytest.mark.parametrize("relative_output", [Path("."), Path("nested/figures")])
def test_replay_rejects_output_inside_the_numerical_run_without_mutation(
    tmp_path: Path, relative_output: Path
):
    run = run_finite_experiment(_finite_config(tmp_path / "runs"))
    before_names = {path.name for path in run.run_dir.iterdir()}
    before_bytes = {
        name: (run.run_dir / name).read_bytes() for name in before_names
    }
    output_dir = run.run_dir / relative_output

    result = render_run(
        run.run_dir, output_dir, requested=("finite_identity",)
    )

    assert result.status == "failed"
    assert result.manifest_path is None
    assert "outside the numerical run" in str(result.message)
    assert {path.name for path in run.run_dir.iterdir()} == before_names
    assert {
        name: (run.run_dir / name).read_bytes() for name in before_names
    } == before_bytes


@pytest.mark.parametrize("relative_output", [Path("."), Path("nested/figures")])
def test_failure_recorder_rejects_output_inside_the_numerical_run_without_mutation(
    tmp_path: Path, relative_output: Path
):
    run = run_finite_experiment(_finite_config(tmp_path / "runs"))
    before_names = {path.name for path in run.run_dir.iterdir()}
    before_bytes = {
        name: (run.run_dir / name).read_bytes() for name in before_names
    }

    result = record_figure_failure(
        run.run_dir, run.run_dir / relative_output, "renderer failed"
    )

    assert result.status == "failed"
    assert result.manifest_path is None
    assert "outside the numerical run" in str(result.message)
    assert {path.name for path in run.run_dir.iterdir()} == before_names
    assert {
        name: (run.run_dir / name).read_bytes() for name in before_names
    } == before_bytes
