"""Pure, replayable publication figures from finalized saved run artifacts."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Literal, Mapping, Sequence

import matplotlib as mpl
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np


FigureStatus = Literal["complete", "failed"]

OKABE_ITO = (
    "#000000",
    "#E69F00",
    "#56B4E9",
    "#009E73",
    "#F0E442",
    "#0072B2",
    "#D55E00",
    "#CC79A7",
)

_STYLE: Mapping[str, object] = {
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 8.0,
    "axes.titlesize": 9.0,
    "axes.labelsize": 9.0,
    "xtick.labelsize": 7.0,
    "ytick.labelsize": 7.0,
    "legend.fontsize": 7.0,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
}

_FIGURE_FILENAMES = {
    "finite_identity": "finite-identity-residuals",
    "gaussian_spectrum": "gaussian-generalized-spectrum",
}


@dataclass(frozen=True)
class FigureRecord:
    """Published vector/raster pair for one requested replay figure."""

    name: str
    png: Path
    pdf: Path


@dataclass(frozen=True)
class FigureManifest:
    """Frozen status of one figure replay attempt."""

    run_dir: Path
    output_dir: Path
    status: FigureStatus
    requested: tuple[str, ...]
    figures: tuple[FigureRecord, ...]
    message: str | None
    manifest_path: Path | None


def render_run(
    run_dir: Path | str,
    output_dir: Path | str,
    requested: Sequence[str] | None = None,
) -> FigureManifest:
    """Render requested figures using only a finalized numerical run bundle."""
    source = Path(run_dir)
    destination = Path(output_dir)
    normalized_requested: tuple[str, ...] = ()
    staged: list[Path] = []
    try:
        normalized_requested = _normalize_requested(requested)
        existing = _load_complete_figure_manifest(
            source, destination, normalized_requested
        )
        if existing is not None:
            return existing
        metrics, arrays = _load_finalized_artifacts(source)
        destination.mkdir(parents=True, exist_ok=True)
        publications: list[tuple[str, Path, Path, Path, Path]] = []
        for name in normalized_requested:
            stem = _FIGURE_FILENAMES[name]
            png_final = destination / f"{stem}.png"
            pdf_final = destination / f"{stem}.pdf"
            png_staged = _temporary_path(destination, stem, ".png")
            pdf_staged = _temporary_path(destination, stem, ".pdf")
            staged.extend((png_staged, pdf_staged))
            _render_requested_figure(
                name, metrics, arrays, png_path=png_staged, pdf_path=pdf_staged
            )
            _require_nonempty_image(png_staged, b"\x89PNG")
            _require_nonempty_image(pdf_staged, b"%PDF")
            publications.append(
                (name, png_staged, pdf_staged, png_final, pdf_final)
            )

        records: list[FigureRecord] = []
        for name, png_staged, pdf_staged, png_final, pdf_final in publications:
            os.replace(png_staged, png_final)
            staged.remove(png_staged)
            os.replace(pdf_staged, pdf_final)
            staged.remove(pdf_staged)
            records.append(FigureRecord(name=name, png=png_final, pdf=pdf_final))

        manifest_path = destination / "figure-manifest.json"
        _atomic_json(
            manifest_path,
            {
                "caption": "n=1 exact fixture",
                "figures": [
                    {
                        "name": record.name,
                        "pdf": record.pdf.name,
                        "pdf_sha256": _sha256(record.pdf),
                        "png": record.png.name,
                        "png_dpi": 300,
                        "png_sha256": _sha256(record.png),
                    }
                    for record in records
                ],
                "message": None,
                "requested": list(normalized_requested),
                "run_dir": str(source.resolve()),
                "status": "complete",
            },
        )
        return FigureManifest(
            run_dir=source,
            output_dir=destination,
            status="complete",
            requested=normalized_requested,
            figures=tuple(records),
            message=None,
            manifest_path=manifest_path,
        )
    except Exception as error:
        for path in staged:
            path.unlink(missing_ok=True)
        return _record_figure_failure(
            source,
            destination,
            str(error) or type(error).__name__,
            requested=normalized_requested,
        )


def record_figure_failure(
    run_dir: Path | str, output_dir: Path | str, message: str
) -> FigureManifest:
    """Atomically record a renderer failure outside the numerical run bundle."""
    return _record_figure_failure(
        Path(run_dir), Path(output_dir), message, requested=()
    )


def _record_figure_failure(
    run_dir: Path,
    output_dir: Path,
    message: str,
    *,
    requested: tuple[str, ...],
) -> FigureManifest:
    if type(message) is not str or not message.strip():
        raise ValueError("figure failure message must be a nonempty string")
    manifest_path: Path | None = None
    recorded_message = message
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        complete_manifest = output_dir / "figure-manifest.json"
        manifest_path = (
            output_dir / "figure-failure.json"
            if _is_complete_figure_manifest(complete_manifest)
            else complete_manifest
        )
        _atomic_json(
            manifest_path,
            {
                "caption": "n=1 exact fixture",
                "figures": [],
                "message": message,
                "requested": list(requested),
                "run_dir": str(run_dir.resolve()),
                "status": "failed",
            },
        )
    except Exception as recording_error:
        manifest_path = None
        recorded_message = (
            f"{message}; failure manifest unavailable: "
            f"{str(recording_error) or type(recording_error).__name__}"
        )
    return FigureManifest(
        run_dir=run_dir,
        output_dir=output_dir,
        status="failed",
        requested=requested,
        figures=(),
        message=recorded_message,
        manifest_path=manifest_path,
    )


def _normalize_requested(requested: Sequence[str] | None) -> tuple[str, ...]:
    if requested is None:
        raise ValueError("requested figure names must be supplied")
    if isinstance(requested, (str, bytes)):
        raise TypeError("requested must be a sequence of figure names")
    names = tuple(requested)
    if not names:
        raise ValueError("at least one figure must be requested")
    if any(type(name) is not str for name in names):
        raise TypeError("requested figure names must be strings")
    if len(set(names)) != len(names):
        raise ValueError("requested figure names must be unique")
    unsupported = [name for name in names if name not in _FIGURE_FILENAMES]
    if unsupported:
        raise ValueError(f"unsupported figure: {unsupported[0]}")
    return names


def _load_finalized_artifacts(
    run_dir: Path,
) -> tuple[dict[str, object], dict[str, np.ndarray]]:
    manifest_path = run_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text("utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("numerical run has no readable finalized manifest") from error
    if not isinstance(manifest, dict) or manifest.get("complete") is not True:
        raise ValueError("numerical run is not finalized")
    inventory = manifest.get("artifacts")
    if not isinstance(inventory, dict):
        raise ValueError("finalized numerical manifest has no artifact inventory")
    for filename in ("metrics.json", "arrays.npz"):
        if inventory.get(filename) != "complete" or not (run_dir / filename).is_file():
            raise ValueError(f"finalized numerical run lacks {filename}")
    try:
        metrics = json.loads((run_dir / "metrics.json").read_text("utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("metrics.json is not readable JSON") from error
    if not isinstance(metrics, dict):
        raise ValueError("metrics.json must contain an object")
    try:
        with np.load(run_dir / "arrays.npz", allow_pickle=False) as archive:
            arrays = {name: np.array(archive[name], copy=True) for name in archive.files}
    except (OSError, ValueError) as error:
        raise ValueError("arrays.npz is not a readable numeric archive") from error
    return metrics, arrays


def _render_requested_figure(
    name: str,
    metrics: Mapping[str, object],
    arrays: Mapping[str, np.ndarray],
    *,
    png_path: Path,
    pdf_path: Path,
) -> None:
    with mpl.rc_context(_STYLE):
        if name == "finite_identity":
            figure = _finite_identity_figure(metrics)
        elif name == "gaussian_spectrum":
            figure = _gaussian_spectrum_figure(metrics, arrays)
        else:  # guarded by _normalize_requested
            raise ValueError(f"unsupported figure: {name}")
        try:
            FigureCanvasAgg(figure)
            figure.savefig(png_path, dpi=300, format="png", bbox_inches="tight")
            figure.savefig(
                pdf_path,
                format="pdf",
                bbox_inches="tight",
                metadata={
                    "Creator": "multiagent_elbo",
                    "Producer": "multiagent_elbo",
                    "CreationDate": None,
                    "ModDate": None,
                },
            )
            _fsync_file(png_path)
            _fsync_file(pdf_path)
        finally:
            figure.clear()


def _finite_identity_figure(metrics: Mapping[str, object]) -> Figure:
    keys = (
        "FIN-01_evidence_residual",
        "FIN-02_vfe_chain_residual",
        "FIN-03_block_update_residual",
        "INF-01_fisher_identity_residual",
        "INT-01_reconstruction_residual",
        "GAUGE_finite_relabeling_residual",
    )
    labels = ("Evidence", "VFE", "Block", "Fisher", "Interaction", "Gauge")
    values: list[float] = []
    tolerances: list[float] = []
    for key in keys:
        record = metrics.get(key)
        if not isinstance(record, dict):
            raise ValueError(f"metrics.json lacks {key}")
        value = record.get("value")
        tolerance = record.get("tolerance")
        if not _finite_number(value) or not _finite_number(tolerance):
            raise ValueError(f"metric {key} has nonfinite value or tolerance")
        values.append(float(value))
        tolerances.append(float(tolerance))

    limit = max(max(abs(value) for value in values), max(tolerances), 1.0e-16) * 1.25
    figure = Figure(figsize=(3.5, 2.75), layout="constrained")
    axis = figure.subplots()
    positions = np.arange(len(values))
    colors = (OKABE_ITO[5], OKABE_ITO[1]) * 3
    hatches = ("", "//", "", "//", "", "//")
    bars = axis.bar(
        positions,
        values,
        color=colors,
        edgecolor=OKABE_ITO[0],
        linewidth=0.6,
        width=0.68,
    )
    for bar, hatch in zip(bars, hatches, strict=True):
        bar.set_hatch(hatch)
    axis.axhline(0.0, color=OKABE_ITO[0], linewidth=0.8, label="zero")
    tolerance = max(tolerances)
    axis.axhline(
        tolerance, color=OKABE_ITO[6], linewidth=0.8, linestyle="--", label="tolerance"
    )
    axis.axhline(-tolerance, color=OKABE_ITO[6], linewidth=0.8, linestyle="--")
    axis.set_ylim(-limit, limit)
    axis.set_xticks(positions, labels, rotation=28, ha="right")
    axis.set_ylabel("Signed residual")
    axis.set_title("Finite identity residuals")
    axis.legend(frameon=False, ncols=2, loc="upper right")
    for position, value in zip(positions, values, strict=True):
        if value == 0.0:
            axis.annotate(
                "exact 0",
                (position, 0.0),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=6,
                rotation=90,
            )
    figure.supxlabel("n=1 exact fixture", x=0.02, ha="left", fontsize=7)
    return figure


def _gaussian_spectrum_figure(
    metrics: Mapping[str, object], arrays: Mapping[str, np.ndarray]
) -> Figure:
    record = metrics.get("GAU-01_generalized_spectrum_residual")
    if not isinstance(record, dict) or not _finite_number(record.get("tolerance")):
        raise ValueError("metrics.json lacks Gaussian spectrum tolerance")
    required = (
        "expected_generalized_eigenvalues",
        "generalized_eigenvalues",
        "transformed_generalized_eigenvalues",
    )
    spectra: list[np.ndarray] = []
    for name in required:
        values = arrays.get(name)
        if values is None:
            raise ValueError(f"arrays.npz lacks {name}")
        vector = np.asarray(values, dtype=np.float64)
        if vector.ndim != 1 or vector.size == 0 or not np.all(np.isfinite(vector)):
            raise ValueError(f"array {name} must be a nonempty finite vector")
        spectra.append(vector)
    if len({spectrum.shape for spectrum in spectra}) != 1:
        raise ValueError("Gaussian generalized spectra must have matching shapes")

    expected, original, transformed = spectra
    modes = np.arange(expected.size)
    figure = Figure(figsize=(3.5, 2.75), layout="constrained")
    axis = figure.subplots()
    axis.plot(
        modes,
        expected,
        color=OKABE_ITO[0],
        linestyle="-",
        marker="o",
        markersize=3.5,
        linewidth=0.9,
        label="Exact roots",
    )
    axis.plot(
        modes,
        original,
        color=OKABE_ITO[5],
        linestyle="--",
        marker="s",
        markerfacecolor="none",
        markersize=4.0,
        linewidth=0.9,
        label="Original frame",
    )
    axis.plot(
        modes,
        transformed,
        color=OKABE_ITO[6],
        linestyle=":",
        marker="x",
        markersize=4.5,
        linewidth=1.0,
        label="Transformed frame",
    )
    axis.set_xlabel("Generalized mode index")
    axis.set_ylabel("Generalized eigenvalue")
    axis.set_title("Matched generalized spectrum")
    axis.set_xticks(modes)
    axis.legend(frameon=False)
    figure.supxlabel("n=1 exact fixture", x=0.02, ha="left", fontsize=7)
    return figure


def _finite_number(value: object) -> bool:
    return type(value) in {int, float} and np.isfinite(float(value))


def _temporary_path(directory: Path, stem: str, suffix: str) -> Path:
    with tempfile.NamedTemporaryFile(
        mode="w+b",
        dir=directory,
        prefix=f".{stem}-",
        suffix=suffix,
        delete=False,
    ) as handle:
        return Path(handle.name)


def _fsync_file(path: Path) -> None:
    with path.open("r+b") as handle:
        os.fsync(handle.fileno())


def _require_nonempty_image(path: Path, signature: bytes) -> None:
    if path.stat().st_size <= len(signature):
        raise ValueError(f"renderer produced an empty image: {path.name}")
    with path.open("rb") as handle:
        if handle.read(len(signature)) != signature:
            raise ValueError(f"renderer produced an invalid image: {path.name}")


def _is_complete_figure_manifest(path: Path) -> bool:
    try:
        payload = json.loads(path.read_text("utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return isinstance(payload, dict) and payload.get("status") == "complete"


def _load_complete_figure_manifest(
    run_dir: Path, output_dir: Path, requested: tuple[str, ...]
) -> FigureManifest | None:
    manifest_path = output_dir / "figure-manifest.json"
    if not _is_complete_figure_manifest(manifest_path):
        return None
    try:
        payload = json.loads(manifest_path.read_text("utf-8"))
        if payload.get("run_dir") != str(run_dir.resolve()):
            raise ValueError("complete figure manifest belongs to a different run")
        if tuple(payload.get("requested", ())) != requested:
            raise ValueError("complete figure manifest has different requested figures")
        raw_figures = payload.get("figures")
        if not isinstance(raw_figures, list) or len(raw_figures) != len(requested):
            raise ValueError("complete figure manifest has an invalid figure inventory")
        records: list[FigureRecord] = []
        for expected_name, raw in zip(requested, raw_figures, strict=True):
            if not isinstance(raw, dict) or raw.get("name") != expected_name:
                raise ValueError("complete figure manifest has an invalid figure record")
            png_name = raw.get("png")
            pdf_name = raw.get("pdf")
            if (
                type(png_name) is not str
                or type(pdf_name) is not str
                or Path(png_name).name != png_name
                or Path(pdf_name).name != pdf_name
            ):
                raise ValueError("complete figure manifest has an invalid image path")
            png = output_dir / png_name
            pdf = output_dir / pdf_name
            if (
                not png.is_file()
                or not pdf.is_file()
                or raw.get("png_sha256") != _sha256(png)
                or raw.get("pdf_sha256") != _sha256(pdf)
            ):
                raise ValueError("complete figure manifest image identity does not match")
            records.append(FigureRecord(expected_name, png, pdf))
    except (OSError, json.JSONDecodeError, TypeError) as error:
        raise ValueError("complete figure manifest is unreadable") from error
    return FigureManifest(
        run_dir=run_dir,
        output_dir=output_dir,
        status="complete",
        requested=requested,
        figures=tuple(records),
        message=None,
        manifest_path=manifest_path,
    )


def _atomic_json(path: Path, payload: object) -> None:
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}-",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_name = handle.name
            json.dump(
                payload,
                handle,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
                allow_nan=False,
            )
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)
        raise


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


__all__ = [
    "FigureManifest",
    "FigureRecord",
    "OKABE_ITO",
    "record_figure_failure",
    "render_run",
]
