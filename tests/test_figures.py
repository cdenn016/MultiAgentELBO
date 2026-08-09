from __future__ import annotations

from dataclasses import FrozenInstanceError
import hashlib
import json
import math
from pathlib import Path
import re
import struct

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import pytest

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.figures import FigureManifest, record_figure_failure, render_run
from multiagent_elbo.finite.attention_experiment import run_attention_experiment
from multiagent_elbo.finite.categorical_dqm_experiment import (
    run_categorical_dqm_experiment,
)
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


def _attention_config(root: Path) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "attention figure fixture", "seed": 20260809},
        {"experiment": "attention_marked_event", "fixture": "nested_nonuniform_v1"},
        {
            "dtype": "float64",
            "atol": 1e-12,
            "rtol": 1e-10,
            "min_spd_rcond": 1e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(root),
            "collect_diagnostics": True,
            "render_figures": False,
        },
    )


def _categorical_dqm_config(root: Path) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "categorical DQM figure fixture", "seed": 20260809},
        {
            "experiment": "categorical_dqm",
            "fixture": "three_category_softmax_v1",
            "theta": [math.log(2.0), math.log(3.0)],
            "finite_difference_step": 1.0e-5,
            "dqm_step_sizes": [0.1, 0.05, 0.025, 0.0125],
        },
        {
            "dtype": "float64",
            "atol": 1e-12,
            "rtol": 1e-10,
            "min_spd_rcond": 1e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(root),
            "collect_diagnostics": True,
            "render_figures": False,
        },
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bundle_hashes(run_dir: Path) -> dict[str, str]:
    return {
        path.name: _sha256(path)
        for path in sorted(run_dir.iterdir())
        if path.is_file()
    }


def _replace_npz_array(
    path: Path,
    name: str,
    *,
    replacement: np.ndarray | None = None,
    remove: bool = False,
) -> None:
    with np.load(path, allow_pickle=False) as archive:
        arrays = {key: np.array(archive[key], copy=True) for key in archive.files}
    if remove:
        del arrays[name]
    else:
        assert replacement is not None
        arrays[name] = replacement
    with path.open("wb") as handle:
        np.savez(handle, **arrays)


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


def _write_combined_run(run_dir: Path, *source_dirs: Path) -> None:
    run_dir.mkdir(parents=True)
    metrics: dict[str, object] = {}
    arrays: dict[str, np.ndarray] = {}
    for source_dir in source_dirs:
        metrics.update(json.loads((source_dir / "metrics.json").read_text("utf-8")))
        with np.load(source_dir / "arrays.npz", allow_pickle=False) as archive:
            for name in archive.files:
                assert name not in arrays
                arrays[name] = np.array(archive[name], copy=True)
    (run_dir / "config.json").write_text("{}", "utf-8")
    (run_dir / "metrics.json").write_text(
        json.dumps(metrics, sort_keys=True, separators=(",", ":")), "utf-8"
    )
    with (run_dir / "arrays.npz").open("wb") as handle:
        np.savez(handle, **arrays)
    (run_dir / "manifest.json").write_text(
        json.dumps(
            {
                "complete": True,
                "artifacts": {
                    "arrays.npz": "complete",
                    "config.json": "complete",
                    "manifest.json": "complete",
                    "metrics.json": "complete",
                },
            },
            sort_keys=True,
            separators=(",", ":"),
        ),
        "utf-8",
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


def test_attention_saved_artifact_replay_is_deterministic_and_read_only(
    tmp_path: Path,
):
    run = run_attention_experiment(_attention_config(tmp_path / "runs"))
    bundle_before = _bundle_hashes(run.run_dir)

    first = render_run(
        run.run_dir,
        tmp_path / "figures-first",
        requested=("attention_composition",),
    )
    second = render_run(
        run.run_dir,
        tmp_path / "figures-second",
        requested=("attention_composition",),
    )

    assert first.status == "complete"
    assert first.requested == ("attention_composition",)
    assert tuple(record.name for record in first.figures) == (
        "attention_composition",
    )
    assert first.figures[0].png.stat().st_size > 0
    assert first.figures[0].pdf.stat().st_size > 0
    assert _png_dimensions(first.figures[0].png)[0] == 1050
    assert _pdf_media_box(first.figures[0].pdf)[0] == pytest.approx(252.0)
    assert _sha256(first.figures[0].png) == _sha256(second.figures[0].png)
    assert _sha256(first.figures[0].pdf) == _sha256(second.figures[0].pdf)
    assert _bundle_hashes(run.run_dir) == bundle_before
    payload = json.loads(first.manifest_path.read_text("utf-8"))
    assert payload["figures"][0]["png_dpi"] == 300
    assert payload["figures"][0]["png_sha256"] == _sha256(
        first.figures[0].png
    )
    assert "exact finite marked-event" in payload["caption"].lower()
    assert "no sampling" in payload["caption"].lower()


def test_categorical_dqm_saved_artifact_replay_has_numerical_scope_caption(
    tmp_path: Path,
):
    run = run_categorical_dqm_experiment(
        _categorical_dqm_config(tmp_path / "runs")
    )
    bundle_before = _bundle_hashes(run.run_dir)

    manifest = render_run(
        run.run_dir,
        tmp_path / "figures",
        requested=("categorical_dqm",),
    )

    assert manifest.status == "complete"
    assert manifest.figures[0].png.read_bytes().startswith(b"\x89PNG")
    assert manifest.figures[0].pdf.read_bytes().startswith(b"%PDF")
    assert _png_dimensions(manifest.figures[0].png)[0] == 1050
    assert _pdf_media_box(manifest.figures[0].pdf)[0] == pytest.approx(252.0)
    payload = json.loads(manifest.manifest_path.read_text("utf-8"))
    assert payload["figures"][0]["png_dpi"] == 300
    assert "categorical dqm numerical diagnostic" in payload["caption"].lower()
    assert "theta=" in payload["caption"].lower()
    assert "not an analytic proof" in payload["caption"].lower()
    assert payload["caption"] != "n=1 exact fixture"
    assert _bundle_hashes(run.run_dir) == bundle_before


def test_new_replay_bundle_preserves_the_requested_figure_order(tmp_path: Path):
    attention = run_attention_experiment(_attention_config(tmp_path / "attention"))
    dqm = run_categorical_dqm_experiment(_categorical_dqm_config(tmp_path / "dqm"))
    run_dir = tmp_path / "combined-run"
    _write_combined_run(run_dir, attention.run_dir, dqm.run_dir)

    manifest = render_run(
        run_dir,
        tmp_path / "figures",
        requested=("categorical_dqm", "attention_composition"),
    )

    assert manifest.status == "complete"
    assert manifest.requested == ("categorical_dqm", "attention_composition")
    assert tuple(record.name for record in manifest.figures) == manifest.requested
    payload = json.loads(manifest.manifest_path.read_text("utf-8"))
    assert tuple(payload["requested"]) == manifest.requested
    assert tuple(record["name"] for record in payload["figures"]) == manifest.requested


def test_attention_replay_rejects_a_missing_saved_array(tmp_path: Path):
    run = run_attention_experiment(_attention_config(tmp_path / "runs"))
    _replace_npz_array(
        run.run_dir / "arrays.npz", "staged_coarse_eta", remove=True
    )

    manifest = render_run(
        run.run_dir,
        tmp_path / "figures",
        requested=("attention_composition",),
    )

    assert manifest.status == "failed"
    assert "staged_coarse_eta" in str(manifest.message)
    assert list((tmp_path / "figures").glob("*.png")) == []
    assert list((tmp_path / "figures").glob("*.pdf")) == []


def test_categorical_dqm_replay_rejects_a_nonfinite_saved_array(tmp_path: Path):
    run = run_categorical_dqm_experiment(
        _categorical_dqm_config(tmp_path / "runs")
    )
    _replace_npz_array(
        run.run_dir / "arrays.npz",
        "dqm_remainder_positive",
        replacement=np.array([0.1, 0.05, np.nan, 0.01]),
    )

    manifest = render_run(
        run.run_dir,
        tmp_path / "figures",
        requested=("categorical_dqm",),
    )

    assert manifest.status == "failed"
    assert "dqm_remainder_positive" in str(manifest.message)
    assert "finite" in str(manifest.message)
    assert list((tmp_path / "figures").glob("*.png")) == []
    assert list((tmp_path / "figures").glob("*.pdf")) == []


def test_new_replay_rejects_a_corrupt_complete_figure_hash(tmp_path: Path):
    run = run_categorical_dqm_experiment(
        _categorical_dqm_config(tmp_path / "runs")
    )
    output_dir = tmp_path / "figures"
    complete = render_run(
        run.run_dir, output_dir, requested=("categorical_dqm",)
    )
    payload = json.loads(complete.manifest_path.read_text("utf-8"))
    payload["figures"][0]["png_sha256"] = "0" * 64
    complete.manifest_path.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")), "utf-8"
    )

    replay = render_run(
        run.run_dir, output_dir, requested=("categorical_dqm",)
    )

    assert replay.status == "failed"
    assert "image identity does not match" in str(replay.message)
    assert complete.figures[0].png.is_file()
    assert (output_dir / "figure-failure.json").is_file()


def test_new_replay_bundle_rolls_back_if_the_second_renderer_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.figures as figures_module

    attention = run_attention_experiment(_attention_config(tmp_path / "attention"))
    dqm = run_categorical_dqm_experiment(_categorical_dqm_config(tmp_path / "dqm"))
    run_dir = tmp_path / "combined-run"
    _write_combined_run(run_dir, attention.run_dir, dqm.run_dir)
    original = figures_module._render_requested_figure
    calls: list[str] = []

    def fail_second(name, *args, **kwargs):
        calls.append(name)
        if len(calls) == 2:
            raise RuntimeError("injected second new-renderer failure")
        return original(name, *args, **kwargs)

    monkeypatch.setattr(figures_module, "_render_requested_figure", fail_second)
    output_dir = tmp_path / "figures"

    manifest = render_run(
        run_dir,
        output_dir,
        requested=("categorical_dqm", "attention_composition"),
    )

    assert calls == ["categorical_dqm", "attention_composition"]
    assert manifest.status == "failed"
    assert "injected second new-renderer failure" in str(manifest.message)
    assert list(output_dir.glob("*.png")) == []
    assert list(output_dir.glob("*.pdf")) == []


@pytest.mark.parametrize("experiment", ["attention", "categorical_dqm"])
def test_new_renderer_construction_keeps_final_size_text_inside_exact_width(
    tmp_path: Path, experiment: str
):
    import multiagent_elbo.figures as figures_module

    with matplotlib.rc_context(figures_module._STYLE):
        if experiment == "attention":
            run = run_attention_experiment(_attention_config(tmp_path / "runs"))
            figure = figures_module._attention_composition_figure(run.arrays)
        else:
            run = run_categorical_dqm_experiment(
                _categorical_dqm_config(tmp_path / "runs")
            )
            figure = figures_module._categorical_dqm_figure(run.arrays)
        try:
            assert figure.get_figwidth() == pytest.approx(3.5)
            canvas = FigureCanvasAgg(figure)
            canvas.draw()
            renderer = canvas.get_renderer()
            figure_box = figure.bbox
            for axis in figure.axes:
                artists = [
                    axis.title,
                    axis.xaxis.label,
                    axis.yaxis.label,
                    *axis.texts,
                ]
                legend = axis.get_legend()
                if legend is not None:
                    artists.append(legend)
                for artist in artists:
                    if hasattr(artist, "get_text") and not artist.get_text():
                        continue
                    box = artist.get_window_extent(renderer)
                    assert box.x0 >= figure_box.x0 - 1.0
                    assert box.x1 <= figure_box.x1 + 1.0
                    assert box.y0 >= figure_box.y0 - 1.0
                    assert box.y1 <= figure_box.y1 + 1.0
            if experiment == "attention":
                left = figure.axes[0].title.get_window_extent(renderer)
                right = figure.axes[1].title.get_window_extent(renderer)
                assert not left.overlaps(right)
        finally:
            figure.clear()


def test_attention_figure_titles_name_the_final_states(tmp_path: Path):
    import multiagent_elbo.figures as figures_module

    run = run_attention_experiment(_attention_config(tmp_path / "runs"))

    with matplotlib.rc_context(figures_module._STYLE):
        figure = figures_module._attention_composition_figure(run.arrays)
        try:
            assert [axis.get_title() for axis in figure.axes[:2]] == [
                "Direct eta | w0",
                "Direct eta | w1",
            ]
        finally:
            figure.clear()


def test_dqm_figure_uses_sparse_nonoverlapping_saved_step_labels(tmp_path: Path):
    import multiagent_elbo.figures as figures_module

    run = run_categorical_dqm_experiment(
        _categorical_dqm_config(tmp_path / "runs")
    )

    with matplotlib.rc_context(figures_module._STYLE):
        figure = figures_module._categorical_dqm_figure(run.arrays)
        try:
            canvas = FigureCanvasAgg(figure)
            canvas.draw()
            axis = figure.axes[2]
            renderer = canvas.get_renderer()
            np.testing.assert_allclose(
                axis.get_xticks(minor=False),
                np.array([0.0125, 0.025, 0.05, 0.1]),
            )
            labels = [
                label
                for label in axis.get_xticklabels(minor=False)
                if label.get_visible() and label.get_text()
            ]
            assert [label.get_text() for label in labels] == [
                "0.0125",
                "0.025",
                "0.05",
                "0.1",
            ]
            assert not any(
                label.get_visible() and label.get_text()
                for label in axis.get_xticklabels(minor=True)
            )
            boxes = [label.get_window_extent(renderer) for label in labels]
            assert all(
                not left.overlaps(right)
                for left, right in zip(boxes, boxes[1:])
            )
        finally:
            figure.clear()


def test_dqm_panel_c_is_inside_the_axis_and_clear_of_y_tick_labels(
    tmp_path: Path,
):
    import multiagent_elbo.figures as figures_module

    run = run_categorical_dqm_experiment(
        _categorical_dqm_config(tmp_path / "runs")
    )

    with matplotlib.rc_context(figures_module._STYLE):
        figure = figures_module._categorical_dqm_figure(run.arrays)
        figure.set_dpi(300)
        try:
            canvas = FigureCanvasAgg(figure)
            canvas.draw()
            assert figure.get_figwidth() == pytest.approx(3.5)
            assert canvas.get_width_height()[0] == 1050
            axis = figure.axes[2]
            renderer = canvas.get_renderer()
            panel = next(text for text in axis.texts if text.get_text() == "C")
            panel_box = panel.get_window_extent(renderer)
            tick_boxes = [
                label.get_window_extent(renderer)
                for label in (
                    *axis.get_yticklabels(minor=False),
                    *axis.get_yticklabels(minor=True),
                )
                if label.get_visible() and label.get_text()
            ]
            assert tick_boxes
            assert not any(panel_box.overlaps(box) for box in tick_boxes)
            axis_box = axis.get_window_extent(renderer)
            assert panel_box.x0 >= axis_box.x0
            assert panel_box.x1 <= axis_box.x1
            assert panel_box.y0 >= axis_box.y0
            assert panel_box.y1 <= axis_box.y1
            assert not panel_box.overlaps(axis.title.get_window_extent(renderer))
            legend = axis.get_legend()
            assert legend is not None
            assert not panel_box.overlaps(legend.get_window_extent(renderer))
        finally:
            figure.clear()


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
