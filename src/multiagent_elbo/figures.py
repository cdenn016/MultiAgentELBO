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
    "attention_composition": "attention-composition",
    "categorical_dqm": "categorical-dqm-diagnostic",
    "finite_counterexamples": "finite-counterexample-diagnostics",
    "finite_identity": "finite-identity-residuals",
    "gauge_holonomy": "gauge-holonomy-diagnostics",
    "gaussian_fixed_ray": "gaussian-fixed-ray-diagnostics",
    "gaussian_spectrum": "gaussian-generalized-spectrum",
    "information_history": "information-history-diagnostics",
    "multiagent_network": "multiagent-network-diagnostics",
    "scale_cocycle": "scale-cocycle-diagnostics",
    "theory_oracles": "theory-oracle-diagnostics",
}

_LABORATORY_FIGURES = {
    "multiagent_network": (
        "Multi-agent network identities",
        (
            "elbo_gap_residual",
            "evidence_residual",
            "hoeffding_reconstruction_residual",
            "local_collective_residual",
            "pairwise_retained_residual",
            "recognition_lift_residual",
        ),
    ),
    "theory_oracles": (
        "Independent theory-oracle residuals",
        (
            "elbo_oracle_residual",
            "fisher_defect_oracle_residual",
            "gaussian_linear_algebra_oracle_residual",
            "hoeffding_oracle_residual",
            "marked_event_associativity_residual",
        ),
    ),
    "finite_counterexamples": (
        "Finite counterexample witnesses",
        (
            "marked_event_source_mass_gap",
            "pairwise_truncation_residual",
            "parameter_dependent_channel_gap",
            "single_law_relabeling_gap",
            "support_violation_count",
        ),
    ),
    "information_history": (
        "Information-history diagnostics",
        (
            "arc_length_reparameterization_residual",
            "fisher_defect_residual",
            "natural_gradient_range_residual",
            "score_finite_difference_residual",
            "semiconjugacy_defect_norm",
        ),
    ),
    "gauge_holonomy": (
        "Gauge and holonomy diagnostics",
        (
            "broken_link_negative_control",
            "cycle_conjugacy_invariant_residual",
            "operational_observable_residual",
            "passive_covariance_residual",
            "trivialization_residual",
        ),
    ),
    "scale_cocycle": (
        "Scale-cocycle diagnostics",
        (
            "cocycle_composition_residual",
            "direct_staged_pushforward_residual",
            "generated_higher_order_coefficient",
            "pairwise_truncation_control",
            "retained_beta_residual",
            "wrong_order_negative_control",
        ),
    ),
    "gaussian_fixed_ray": (
        "Gaussian fixed-ray pilot diagnostics",
        (
            "basin_exit_rate",
            "blocking_scheme_dispersion",
            "cpu_cuda_parity_residual",
            "normalized_coupling_distance",
            "off_family_nonlinear_remainder",
            "projective_ray_angle",
        ),
    ),
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
    source_input = Path(run_dir)
    destination_input = Path(output_dir)
    try:
        source, destination = _resolve_replay_paths(source_input, destination_input)
    except Exception as error:
        return _unpublished_failure(
            source_input,
            destination_input,
            str(error) or type(error).__name__,
            requested=(),
        )
    normalized_requested: tuple[str, ...] = ()
    staged: list[Path] = []
    published: list[Path] = []
    try:
        normalized_requested = _normalize_requested(requested)
        existing = _load_complete_figure_manifest(
            source, destination, normalized_requested
        )
        if existing is not None:
            return existing
        metrics, arrays = _load_finalized_artifacts(source)
        destination.mkdir(parents=True, exist_ok=True)
        caption = " | ".join(
            _figure_caption(name, metrics, arrays)
            for name in normalized_requested
        )
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
            published.append(png_final)
            os.replace(pdf_staged, pdf_final)
            staged.remove(pdf_staged)
            published.append(pdf_final)
            records.append(FigureRecord(name=name, png=png_final, pdf=pdf_final))

        manifest_path = destination / "figure-manifest.json"
        _atomic_json(
            manifest_path,
            {
                "caption": caption,
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
        for path in published:
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
    if type(message) is not str or not message.strip():
        raise ValueError("figure failure message must be a nonempty string")
    source_input = Path(run_dir)
    destination_input = Path(output_dir)
    try:
        source, destination = _resolve_replay_paths(source_input, destination_input)
    except Exception as error:
        reason = str(error) or type(error).__name__
        return _unpublished_failure(
            source_input,
            destination_input,
            f"{message}; failure manifest unavailable: {reason}",
            requested=(),
        )
    return _record_figure_failure(source, destination, message, requested=())


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


def _unpublished_failure(
    run_dir: Path,
    output_dir: Path,
    message: str,
    *,
    requested: tuple[str, ...],
) -> FigureManifest:
    return FigureManifest(
        run_dir=run_dir,
        output_dir=output_dir,
        status="failed",
        requested=requested,
        figures=(),
        message=message,
        manifest_path=None,
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


def _resolve_replay_paths(run_dir: Path, output_dir: Path) -> tuple[Path, Path]:
    try:
        resolved_run = run_dir.resolve(strict=False)
    except OSError as error:
        raise ValueError("numerical run path cannot be resolved") from error
    resolved_output = output_dir.resolve(strict=False)
    if resolved_output == resolved_run or resolved_run in resolved_output.parents:
        raise ValueError("figure output_dir must be outside the numerical run_dir")
    return resolved_run, resolved_output


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
    if inventory.get("metrics.json") != "complete" or not (
        run_dir / "metrics.json"
    ).is_file():
        raise ValueError("finalized numerical run lacks metrics.json")
    numeric_archives = tuple(
        sorted(
            filename
            for filename, status in inventory.items()
            if filename.endswith(".npz") and status == "complete"
        )
    )
    if not numeric_archives:
        raise ValueError("finalized numerical run lacks a complete numeric archive")
    try:
        metrics = json.loads((run_dir / "metrics.json").read_text("utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("metrics.json is not readable JSON") from error
    if not isinstance(metrics, dict):
        raise ValueError("metrics.json must contain an object")
    arrays: dict[str, np.ndarray] = {}
    try:
        for filename in numeric_archives:
            archive_path = run_dir / filename
            if not archive_path.is_file():
                raise ValueError(f"finalized numerical run lacks {filename}")
            prefix = "" if filename == "arrays.npz" else f"{archive_path.stem}__"
            with np.load(archive_path, allow_pickle=False) as archive:
                for name in archive.files:
                    qualified = f"{prefix}{name}"
                    if qualified in arrays:
                        raise ValueError(
                            f"duplicate saved numeric array name: {qualified}"
                        )
                    arrays[qualified] = np.array(archive[name], copy=True)
    except (OSError, ValueError) as error:
        if str(error).startswith(("finalized numerical run", "duplicate saved")):
            raise
        raise ValueError("saved NPZ artifact is not a readable numeric archive") from error
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
        elif name == "attention_composition":
            figure = _attention_composition_figure(arrays)
        elif name == "categorical_dqm":
            figure = _categorical_dqm_figure(arrays)
        elif name in _LABORATORY_FIGURES:
            title, keys = _LABORATORY_FIGURES[name]
            figure = _laboratory_metric_figure(metrics, title, keys)
        else:  # guarded by _normalize_requested
            raise ValueError(f"unsupported figure: {name}")
        try:
            FigureCanvasAgg(figure)
            figure.savefig(png_path, dpi=300, format="png")
            figure.savefig(
                pdf_path,
                format="pdf",
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


def _attention_composition_figure(arrays: Mapping[str, np.ndarray]) -> Figure:
    direct = _saved_array(arrays, "direct_coarse_eta", ndim=3)
    staged = _saved_array(arrays, "staged_coarse_eta", ndim=3)
    beta_only = _saved_array(arrays, "beta_only_direct_beta", ndim=2)
    correct_beta = _saved_array(arrays, "beta_only_correct_beta", ndim=2)
    state_probability = _saved_array(
        arrays, "direct_coarse_state_probability", ndim=1
    )
    if direct.shape[0] != 2:
        raise ValueError("array direct_coarse_eta must contain exactly two final states")
    if staged.shape != direct.shape:
        raise ValueError("staged_coarse_eta must match direct_coarse_eta")
    if beta_only.shape != correct_beta.shape:
        raise ValueError("beta_only_direct_beta must match beta_only_correct_beta")
    if state_probability.shape != (2,):
        raise ValueError(
            "direct_coarse_state_probability must match the two final states"
        )

    figure = Figure(figsize=(3.5, 3.25), layout="constrained")
    axes = np.asarray(figure.subplots(2, 2), dtype=object)
    receiver_styles = (
        (OKABE_ITO[5], "-", "o"),
        (OKABE_ITO[1], "--", "s"),
        (OKABE_ITO[3], ":", "^"),
        (OKABE_ITO[6], "-.", "D"),
    )
    source_count = direct.shape[2]
    for state_index, axis in enumerate(axes[0]):
        for receiver_index, values in enumerate(direct[state_index]):
            color, linestyle, marker = receiver_styles[
                receiver_index % len(receiver_styles)
            ]
            positions = (
                np.arange(source_count, dtype=np.int64)
                + receiver_index * source_count
            )
            axis.plot(
                positions,
                values,
                color=color,
                linestyle=linestyle,
                marker=marker,
                markersize=3.2,
                linewidth=0.9,
                label=f"Receiver {receiver_index}",
            )
        axis.set_title(f"Direct eta | w{state_index}")
        axis.set_ylabel("Event mass")
        axis.set_xticks(np.arange(direct.shape[1] * source_count))
        axis.tick_params(axis="x", labelbottom=False)
    axes[0, 0].legend(frameon=False, loc="best")

    positions = np.arange(direct.shape[1] * source_count)
    composition_residual = staged - direct
    for state_index, values in enumerate(composition_residual):
        color, linestyle, marker = receiver_styles[state_index]
        axes[1, 0].plot(
            positions,
            values.ravel(),
            color=color,
            linestyle=linestyle,
            marker=marker,
            markersize=3.2,
            linewidth=0.9,
            label=f"State {state_index}",
        )
    axes[1, 0].axhline(0.0, color=OKABE_ITO[0], linewidth=0.6, linestyle=":")
    axes[1, 0].set_title("Staged - direct eta")
    axes[1, 0].set_xlabel("Event cell")
    axes[1, 0].set_ylabel("Residual")
    axes[1, 0].legend(frameon=False, loc="best")

    beta_residual = (beta_only - correct_beta).ravel()
    axes[1, 1].plot(
        np.arange(beta_residual.size),
        beta_residual,
        color=OKABE_ITO[6],
        linestyle="--",
        marker="D",
        markerfacecolor="none",
        markersize=3.6,
        linewidth=0.9,
    )
    axes[1, 1].axhline(0.0, color=OKABE_ITO[0], linewidth=0.6, linestyle=":")
    axes[1, 1].set_title("Beta-only residual")
    axes[1, 1].set_xlabel("Attention cell")
    axes[1, 1].set_ylabel("Residual")

    for label, axis in zip("ABCD", axes.ravel(), strict=True):
        axis.text(
            -0.18,
            1.08,
            label,
            transform=axis.transAxes,
            fontsize=9,
            fontweight="bold",
            va="top",
        )
    return figure


def _categorical_dqm_figure(arrays: Mapping[str, np.ndarray]) -> Figure:
    analytic_fine = _saved_array(arrays, "analytic_fine_score", ndim=2)
    finite_difference_fine = _saved_array(
        arrays, "finite_difference_fine_score", ndim=2
    )
    analytic_coarse = _saved_array(arrays, "analytic_coarse_score", ndim=2)
    finite_difference_coarse = _saved_array(
        arrays, "finite_difference_coarse_score", ndim=2
    )
    steps = _saved_array(arrays, "dqm_step_sizes", ndim=1)
    positive = _saved_array(arrays, "dqm_remainder_positive", ndim=1)
    negative = _saved_array(arrays, "dqm_remainder_negative", ndim=1)
    if finite_difference_fine.shape != analytic_fine.shape:
        raise ValueError(
            "finite_difference_fine_score must match analytic_fine_score"
        )
    if finite_difference_coarse.shape != analytic_coarse.shape:
        raise ValueError(
            "finite_difference_coarse_score must match analytic_coarse_score"
        )
    if analytic_fine.shape[1] != analytic_coarse.shape[1]:
        raise ValueError("fine and coarse scores must share a parameter dimension")
    if positive.shape != steps.shape or negative.shape != steps.shape or steps.size == 0:
        raise ValueError("DQM remainder ladders must match the nonempty step ladder")
    if np.any(steps <= 0.0):
        raise ValueError("array dqm_step_sizes must be strictly positive")
    if np.any(positive <= 0.0):
        raise ValueError("array dqm_remainder_positive must be strictly positive")
    if np.any(negative <= 0.0):
        raise ValueError("array dqm_remainder_negative must be strictly positive")

    figure = Figure(figsize=(3.5, 3.15), layout="constrained")
    grid = figure.add_gridspec(2, 2)
    fine_axis = figure.add_subplot(grid[0, 0])
    coarse_axis = figure.add_subplot(grid[0, 1])
    remainder_axis = figure.add_subplot(grid[1, :])

    def score_panel(
        axis: object,
        analytic: np.ndarray,
        finite_difference: np.ndarray,
        title: str,
    ) -> None:
        positions = np.arange(analytic.size)
        axis.plot(
            positions,
            analytic.ravel(),
            color=OKABE_ITO[0],
            linestyle="-",
            marker="o",
            markersize=3.2,
            linewidth=0.9,
            label="Analytic",
        )
        axis.plot(
            positions,
            finite_difference.ravel(),
            color=OKABE_ITO[5],
            linestyle="--",
            marker="x",
            markersize=3.8,
            linewidth=0.9,
            label="Finite difference",
        )
        axis.axhline(0.0, color=OKABE_ITO[0], linewidth=0.5, linestyle=":")
        axis.set_title(title)
        axis.set_xlabel("Component")
        axis.set_ylabel("Score")

    score_panel(fine_axis, analytic_fine, finite_difference_fine, "Fine score")
    score_panel(
        coarse_axis, analytic_coarse, finite_difference_coarse, "Coarse score"
    )
    fine_axis.legend(frameon=False, loc="best")

    order = np.argsort(steps)
    remainder_axis.loglog(
        steps[order],
        positive[order],
        color=OKABE_ITO[5],
        linestyle="-",
        marker="o",
        markersize=3.2,
        linewidth=0.9,
        label="Positive perturbation",
    )
    remainder_axis.loglog(
        steps[order],
        negative[order],
        color=OKABE_ITO[6],
        linestyle="--",
        marker="s",
        markerfacecolor="none",
        markersize=3.5,
        linewidth=0.9,
        label="Negative perturbation",
    )
    remainder_axis.set_title("Two-sided normalized DQM remainder")
    remainder_axis.set_xlabel("Step size")
    remainder_axis.set_ylabel("Remainder")
    tick_indices = np.linspace(
        0,
        steps.size - 1,
        num=min(steps.size, 4),
        dtype=np.int64,
    )
    display_steps = steps[order][np.unique(tick_indices)]
    remainder_axis.set_xticks(
        display_steps,
        labels=tuple(f"{value:.4g}" for value in display_steps),
        minor=False,
    )
    remainder_axis.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
    remainder_axis.legend(frameon=False, loc="best")
    for label, axis in zip(
        "ABC", (fine_axis, coarse_axis, remainder_axis), strict=True
    ):
        panel_position = (
            (0.01, 0.98) if axis is remainder_axis else (-0.16, 1.08)
        )
        axis.text(
            *panel_position,
            label,
            transform=axis.transAxes,
            fontsize=9,
            fontweight="bold",
            va="top",
        )
    return figure


def _laboratory_metric_figure(
    metrics: Mapping[str, object], title: str, keys: Sequence[str]
) -> Figure:
    values: list[float] = []
    statuses: list[str] = []
    for key in keys:
        record = metrics.get(key)
        if not isinstance(record, dict):
            raise ValueError(f"metrics.json lacks {key}")
        value = record.get("value")
        status = record.get("status")
        if not _finite_number(value):
            raise ValueError(f"metric {key} has a nonfinite value")
        if status not in {"pass", "fail", "inconclusive"}:
            raise ValueError(f"metric {key} has an unsupported status")
        values.append(float(value))
        statuses.append(str(status))

    colors = {
        "pass": OKABE_ITO[3],
        "inconclusive": OKABE_ITO[1],
        "fail": OKABE_ITO[6],
    }
    labels = tuple(key.replace("_", " ") for key in keys)
    positions = np.arange(len(values))
    figure = Figure(figsize=(4.5, 3.15), layout="constrained")
    axis = figure.subplots()
    bars = axis.bar(
        positions,
        values,
        color=[colors[status] for status in statuses],
        edgecolor=OKABE_ITO[0],
        linewidth=0.6,
        width=0.7,
    )
    for bar, status in zip(bars, statuses, strict=True):
        if status == "inconclusive":
            bar.set_hatch("//")
        elif status == "fail":
            bar.set_hatch("xx")
    nonzero = [abs(value) for value in values if value != 0.0]
    linthresh = min(nonzero) / 10.0 if nonzero else 1.0e-12
    axis.set_yscale("symlog", linthresh=max(linthresh, 1.0e-16))
    axis.axhline(0.0, color=OKABE_ITO[0], linewidth=0.7)
    axis.set_xticks(positions, labels, rotation=32, ha="right")
    axis.set_ylabel("Reported scalar value (symlog)")
    axis.set_title(title)
    for position, value, status in zip(positions, values, statuses, strict=True):
        if status != "pass":
            axis.annotate(
                status,
                (position, value),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=6,
                rotation=90,
            )
    return figure


def _figure_caption(
    name: str,
    metrics: Mapping[str, object],
    arrays: Mapping[str, np.ndarray],
) -> str:
    if name in {"finite_identity", "gaussian_spectrum"}:
        return "n=1 exact fixture"
    if name == "attention_composition":
        probabilities = _saved_array(
            arrays, "direct_coarse_state_probability", ndim=1
        )
        if probabilities.shape != (2,):
            raise ValueError(
                "direct_coarse_state_probability must match the two final states"
            )
        values = ", ".join(f"{value:.6g}" for value in probabilities)
        return (
            "Exact finite marked-event composition diagnostic from finalized saved "
            f"artifacts at final-state probabilities ({values}); no sampling, error "
            "bars, or significance tests."
        )
    if name == "categorical_dqm":
        theta = _saved_array(arrays, "theta", ndim=1)
        direction = _saved_array(arrays, "direction", ndim=1)
        steps = _saved_array(arrays, "dqm_step_sizes", ndim=1)
        if theta.size == 0 or direction.shape != theta.shape or steps.size == 0:
            raise ValueError(
                "categorical DQM theta, direction, and step ladder are inconsistent"
            )
        theta_text = ", ".join(f"{value:.6g}" for value in theta)
        direction_text = ", ".join(f"{value:.6g}" for value in direction)
        return (
            "Categorical DQM numerical diagnostic from finalized saved artifacts at "
            f"theta=({theta_text}), direction=({direction_text}), and step range "
            f"[{steps.min():.6g}, {steps.max():.6g}]; analytic/finite-difference "
            "agreement and the finite remainder ladder are implementation checks, "
            "not an analytic proof."
        )
    if name in _LABORATORY_FIGURES:
        title, keys = _LABORATORY_FIGURES[name]
        for key in keys:
            if not isinstance(metrics.get(key), dict):
                raise ValueError(f"metrics.json lacks {key}")
        scope = (
            " CUDA parity remains inconclusive and the heavy sweep was not run."
            if name == "gaussian_fixed_ray"
            else ""
        )
        return (
            f"{title} from finalized saved metrics. Values have heterogeneous units "
            "and are not comparable across bars; colors encode recorded metric status. "
            f"Numerical diagnostics are not analytic proofs.{scope}"
        )
    raise ValueError(f"unsupported figure: {name}")


def _saved_array(
    arrays: Mapping[str, np.ndarray], name: str, *, ndim: int
) -> np.ndarray:
    values = arrays.get(name)
    if values is None:
        raise ValueError(f"arrays.npz lacks {name}")
    try:
        array = np.asarray(values, dtype=np.float64)
    except (TypeError, ValueError) as error:
        raise ValueError(f"array {name} must be numeric") from error
    if array.ndim != ndim or array.size == 0:
        raise ValueError(f"array {name} must be a nonempty {ndim}-dimensional array")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"array {name} must be finite")
    return array


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
