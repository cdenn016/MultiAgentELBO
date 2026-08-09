"""Orchestration for the exact Gaussian realization laboratory."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from pathlib import Path
from types import MappingProxyType
from typing import Callable, Literal, Mapping

import numpy as np
import scipy.linalg

from ...artifacts import RunStore
from ...config import ExperimentConfig, config_sha256
from ...rendering import record_figure_failure_safely, validated_renderer_status
from ...runtime import RngStreams, collect_provenance
from .gauge import apply_frame_change, generate_positive_orientation_frames
from .interactions import (
    GaussianInteraction,
    galerkin_aggregate_precision,
    schur_complement_precision,
)


MetricStatus = Literal["pass", "fail"]


@dataclass(frozen=True)
class GaussianMetricRecord:
    value: float
    tolerance: float
    status: MetricStatus
    interpretation: str
    assessment_scope: Literal["implementation_check"]
    theorem_status: Literal["established_conditional_identity", "negative_control"]


@dataclass(frozen=True)
class GaussianExperimentResult:
    run_dir: Path
    config_hash: str
    status: Literal["pass", "fail"]
    metrics: Mapping[str, GaussianMetricRecord]
    arrays: Mapping[str, np.ndarray]
    figure_status: Literal["not_requested", "complete", "failed"]
    figure_dir: Path | None


def _readonly(values: object) -> np.ndarray:
    array = np.array(values, dtype=np.float64, copy=True, order="C")
    array.setflags(write=False)
    return array


def _identity_metric(
    value: float, tolerance: float, interpretation: str
) -> GaussianMetricRecord:
    return GaussianMetricRecord(
        value=float(value),
        tolerance=float(tolerance),
        status="pass" if abs(value) <= tolerance else "fail",
        interpretation=interpretation,
        assessment_scope="implementation_check",
        theorem_status="established_conditional_identity",
    )


def _negative_control_metric(
    value: float, tolerance: float, interpretation: str
) -> GaussianMetricRecord:
    return GaussianMetricRecord(
        value=float(value),
        tolerance=float(tolerance),
        status="pass" if value > tolerance else "fail",
        interpretation=interpretation,
        assessment_scope="implementation_check",
        theorem_status="negative_control",
    )


def _fixtures(
    config: ExperimentConfig, problem_rng: np.random.Generator
) -> tuple[
    dict[str, GaussianMetricRecord],
    dict[str, np.ndarray],
    dict[str, np.ndarray],
]:
    numerics = config.numerics
    tolerance = numerics.atol + numerics.rtol
    weight = np.array([[1.0, 0.2], [0.2, 2.0]])
    interaction = GaussianInteraction.from_self_and_edges(
        (np.diag([2.0, 3.0]), np.diag([4.0, 5.0])),
        {(0, 1): weight},
        numerics,
    )
    frames = np.array([np.diag([2.0, 1.0]), np.diag([1.0, 3.0])])
    coordinates = np.array([1.0, 2.0, -1.0, 1.0])
    prolongator = np.vstack([np.eye(2), np.eye(2)])
    coarse_frames = np.array([np.diag([5.0, 2.0])])
    gauge = apply_frame_change(
        interaction.precision,
        interaction.laplacian,
        frames,
        numerics,
        prolongator=prolongator,
        coarse_frames=coarse_frames,
    )
    transformed_coordinates = gauge.block_frame @ coordinates
    expected_generalized = np.array(
        [
            0.0,
            0.0,
            (5077.0 - 5.0 * math.sqrt(14785.0)) / 10802.0,
            (5077.0 + 5.0 * math.sqrt(14785.0)) / 10802.0,
        ]
    )
    expected_ordinary = np.array(
        [0.0, 0.0, 3.0 - math.sqrt(29.0) / 5.0, 3.0 + math.sqrt(29.0) / 5.0]
    )
    expected_transformed_ordinary = np.array(
        [
            0.0,
            0.0,
            (125.0 - math.sqrt(1513.0)) / 72.0,
            (125.0 + math.sqrt(1513.0)) / 72.0,
        ]
    )
    original_energy = float(coordinates @ interaction.precision @ coordinates)
    transformed_energy = float(
        transformed_coordinates
        @ gauge.transformed_precision
        @ transformed_coordinates
    )
    original_laplacian_energy = float(
        coordinates @ interaction.laplacian @ coordinates
    )
    transformed_laplacian_energy = float(
        transformed_coordinates
        @ gauge.transformed_laplacian
        @ transformed_coordinates
    )

    scalar = GaussianInteraction.from_self_and_edges(
        (1.0, 2.0, 3.0), {(0, 1): 4.0, (1, 2): 5.0}, numerics
    )
    aggregation = galerkin_aggregate_precision(scalar, ((0, 1), (2,)))
    expected_galerkin = np.array([[8.0, -5.0], [-5.0, 8.0]])
    scalar_schur = schur_complement_precision(
        scalar.precision,
        retained_vertices=(0, 2),
        block_size=1,
        numerics=numerics,
    )

    identity = np.eye(2)
    kron_interaction = GaussianInteraction.from_self_and_edges(
        (identity, identity, identity),
        {
            (0, 1): np.zeros((2, 2)),
            (0, 2): np.diag([1.0, 2.0]),
            (1, 2): np.array([[2.0, 1.0], [1.0, 2.0]]),
        },
        numerics,
    )
    kron_schur = schur_complement_precision(
        kron_interaction.precision,
        retained_vertices=(0, 1),
        block_size=2,
        numerics=numerics,
    )
    manufactured_weight = -kron_schur[:2, 2:]
    expected_scalar_schur = np.array(
        [[39.0 / 11.0, -20.0 / 11.0], [-20.0 / 11.0, 63.0 / 11.0]]
    )
    expected_kron_schur = np.array(
        [
            [33.0, 2.0, -9.0, -3.0],
            [2.0, 41.0, -4.0, -14.0],
            [-9.0, -4.0, 37.0, 6.0],
            [-3.0, -14.0, 6.0, 40.0],
        ]
    ) / 19.0

    coarse_precision = prolongator.T @ interaction.precision @ prolongator
    transformed_coarse_precision = (
        gauge.transformed_prolongator.T
        @ gauge.transformed_precision
        @ gauge.transformed_prolongator
    )
    expected_coarse_precision = np.diag([6.0, 8.0])
    expected_transformed_coarse_precision = np.diag([6.0 / 25.0, 2.0])
    expected_transformed_prolongator = np.array(
        [
            [2.0 / 5.0, 0.0],
            [0.0, 1.0 / 2.0],
            [1.0 / 5.0, 0.0],
            [0.0, 3.0 / 2.0],
        ]
    )
    coarse_via_frame = scipy.linalg.solve(
        coarse_frames[0].T,
        scipy.linalg.solve(
            coarse_frames[0].T, coarse_precision.T, check_finite=False
        ).T,
        check_finite=False,
    )
    metrics = {
        "GAU-01_energy_residual": _identity_metric(
            max(
                abs(original_energy - 149.0 / 5.0),
                abs(transformed_energy - 149.0 / 5.0),
            ),
            tolerance,
            "Matched inverse congruence preserves the precision quadratic energy.",
        ),
        "GAU-01_laplacian_energy_residual": _identity_metric(
            max(
                abs(original_laplacian_energy - 34.0 / 5.0),
                abs(transformed_laplacian_energy - 34.0 / 5.0),
            ),
            tolerance,
            "Matched inverse congruence preserves the Laplacian quadratic energy.",
        ),
        "GAU-01_generalized_spectrum_residual": _identity_metric(
            float(
                max(
                    np.max(np.abs(gauge.generalized_eigenvalues - expected_generalized)),
                    np.max(
                        np.abs(
                            gauge.transformed_generalized_eigenvalues
                            - expected_generalized
                        )
                    ),
                )
            ),
            tolerance,
            "Generalized roots agree with an independent exact radical oracle.",
        ),
        "GAU-01_eigenpair_residual": _identity_metric(
            float(
                max(
                    np.max(gauge.eigenpair_residuals),
                    np.max(gauge.transformed_eigenpair_residuals),
                )
            ),
            tolerance,
            "Normalized generalized-eigenpair residual in both frames.",
        ),
        "GAU-01_metric_orthogonality_residual": _identity_metric(
            max(
                gauge.metric_orthogonality_residual,
                gauge.transformed_metric_orthogonality_residual,
            ),
            tolerance,
            "Generalized eigenvectors are precision-metric orthonormal.",
        ),
        "GAU-01_logdet_difference_residual": _identity_metric(
            gauge.transformed_logdet
            - gauge.original_logdet
            + 2.0 * math.log(6.0),
            tolerance,
            "Cholesky log-determinants obey inverse-congruence volume scaling.",
        ),
        "GAU-01_determinant_oracle_residual": _identity_metric(
            max(
                abs(float(np.linalg.det(interaction.precision)) - 10802.0 / 25.0),
                abs(
                    float(np.linalg.det(gauge.transformed_precision))
                    - 5401.0 / 450.0
                ),
            ),
            tolerance,
            "Both precision determinants agree with independent literal oracles.",
        ),
        "GAU-01_commuting_square_residual": _identity_metric(
            float(
                max(
                    np.max(np.abs(coarse_precision - expected_coarse_precision)),
                    np.max(
                        np.abs(
                            transformed_coarse_precision
                            - expected_transformed_coarse_precision
                        )
                    ),
                    np.max(
                        np.abs(transformed_coarse_precision - coarse_via_frame)
                    ),
                    np.max(
                        np.abs(
                            gauge.transformed_prolongator
                            - expected_transformed_prolongator
                        )
                    ),
                )
            ),
            tolerance,
            "The transformed prolongator closes the coarse inverse-congruence commuting square.",
        ),
        "GAU-01_ordinary_spectrum_oracle_residual": _identity_metric(
            float(
                max(
                    np.max(np.abs(gauge.ordinary_eigenvalues - expected_ordinary)),
                    np.max(
                        np.abs(
                            gauge.transformed_ordinary_eigenvalues
                            - expected_transformed_ordinary
                        )
                    ),
                )
            ),
            tolerance,
            "Ordinary spectra in both frames agree with independent radical oracles.",
        ),
        "GAU-01_ordinary_spectrum_change_control": _negative_control_metric(
            float(
                np.max(
                    np.abs(
                        gauge.ordinary_eigenvalues
                        - gauge.transformed_ordinary_eigenvalues
                    )
                )
            ),
            tolerance,
            "Ordinary Laplacian eigenvalues change under nonorthogonal frame congruence.",
        ),
        "GAU-02_galerkin_residual": _identity_metric(
            float(np.max(np.abs(aggregation.precision - expected_galerkin))),
            tolerance,
            "Hard-identification Galerkin restriction cancels the internal edge.",
        ),
        "GAU-02_schur_distinction_control": _negative_control_metric(
            float(np.max(np.abs(scalar_schur - aggregation.precision))),
            tolerance,
            "The scalar Schur marginal is distinct from Galerkin restriction.",
        ),
        "GAU-02_scalar_schur_oracle_residual": _identity_metric(
            float(np.max(np.abs(scalar_schur - expected_scalar_schur))),
            tolerance,
            "The scalar Schur marginal agrees with its independent literal oracle.",
        ),
        "GAU-02_kron_schur_oracle_residual": _identity_metric(
            float(np.max(np.abs(kron_schur - expected_kron_schur))),
            tolerance,
            "The unrestricted K=2 Schur matrix agrees with its independent literal oracle.",
        ),
        "GAU-02_kron_nonclosure_control": _negative_control_metric(
            float(np.max(np.abs(manufactured_weight - manufactured_weight.T))),
            tolerance,
            "Unrestricted matrix-weighted Kron reduction manufactures an asymmetric block weight.",
        ),
    }
    arrays = {
        "coarse_frames": coarse_frames,
        "coarse_precision": coarse_precision,
        "expected_coarse_precision": expected_coarse_precision,
        "expected_generalized_eigenvalues": expected_generalized,
        "expected_transformed_coarse_precision": expected_transformed_coarse_precision,
        "expected_transformed_prolongator": expected_transformed_prolongator,
        "fine_coordinates": coordinates,
        "fine_frames": frames,
        "fine_laplacian": interaction.laplacian,
        "fine_precision": interaction.precision,
        "generalized_eigenvalues": gauge.generalized_eigenvalues,
        "ordinary_eigenvalues": gauge.ordinary_eigenvalues,
        "prolongator": prolongator,
        "transformed_coarse_precision": transformed_coarse_precision,
        "transformed_coordinates": transformed_coordinates,
        "transformed_generalized_eigenvalues": gauge.transformed_generalized_eigenvalues,
        "transformed_laplacian": gauge.transformed_laplacian,
        "transformed_ordinary_eigenvalues": gauge.transformed_ordinary_eigenvalues,
        "transformed_precision": gauge.transformed_precision,
        "transformed_prolongator": gauge.transformed_prolongator,
    }
    diagnostics = {
        "frame_condition_numbers": gauge.frame_condition_numbers,
        "generalized_eigenvectors": gauge.generalized_eigenvectors,
        "generalized_eigenpair_residuals": gauge.eigenpair_residuals,
        "kron_manufactured_weight": manufactured_weight,
        "kron_schur_precision": kron_schur,
        "precision_condition_numbers": np.array(
            [gauge.original_condition_number, gauge.transformed_condition_number]
        ),
        "precision_logdeterminants": np.array(
            [gauge.original_logdet, gauge.transformed_logdet]
        ),
        "precision_minimum_eigenvalues": np.array(
            [gauge.original_minimum_eigenvalue, gauge.transformed_minimum_eigenvalue]
        ),
        "scalar_galerkin_precision": aggregation.precision,
        "scalar_schur_precision": scalar_schur,
        "seeded_positive_frames": generate_positive_orientation_frames(
            problem_rng,
            interaction.n_vertices,
            interaction.block_size,
            max_condition=100.0,
        ),
        "transformed_generalized_eigenvectors": gauge.transformed_generalized_eigenvectors,
        "transformed_generalized_eigenpair_residuals": gauge.transformed_eigenpair_residuals,
    }
    return metrics, arrays, diagnostics


def run_gaussian_experiment(
    config: ExperimentConfig, *, renderer: Callable[..., object] | None = None
) -> GaussianExperimentResult:
    """Run and finalize the exact Gaussian fixture before optional rendering."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    if config.theory.experiment != "gaussian_realization":
        raise ValueError(
            "gaussian experiment requires theory.experiment='gaussian_realization'"
        )
    streams = RngStreams.from_seed(config.run.seed)
    metrics, raw_arrays, raw_diagnostics = _fixtures(config, streams.problem)
    arrays = {name: _readonly(raw_arrays[name]) for name in sorted(raw_arrays)}
    diagnostics = {
        name: _readonly(raw_diagnostics[name]) for name in sorted(raw_diagnostics)
    }
    config_hash = config_sha256(config)
    repo_root = Path(__file__).resolve().parents[4]
    provenance = collect_provenance(
        repo_root, repo_root / "Theory", config_hash, streams
    )
    provenance["experiment_scope"] = "pre_registered_exact_gaussian_fixtures"
    store = RunStore.create(config, provenance)
    store.write_json(
        "metrics", {name: asdict(metrics[name]) for name in sorted(metrics)}
    )
    store.write_npz("arrays", arrays)
    artifacts = ["metrics.json", "arrays.npz"]
    if config.output.collect_diagnostics:
        store.write_npz("diagnostics", diagnostics)
        artifacts.append("diagnostics.npz")
    store.finalize(artifacts)
    numerical_status: MetricStatus = (
        "pass" if all(metric.status == "pass" for metric in metrics.values()) else "fail"
    )

    figure_status: Literal["not_requested", "complete", "failed"] = "not_requested"
    figure_dir: Path | None = None
    if config.output.render_figures:
        figure_dir = store.run_dir.parent / "figures" / store.run_dir.name
        requested = ("gaussian_spectrum",)
        if renderer is None:
            from ...figures import render_run

            renderer = render_run
        try:
            figure_manifest = renderer(
                store.run_dir,
                figure_dir,
                requested=requested,
            )
            figure_status = validated_renderer_status(
                figure_manifest, store.run_dir, figure_dir, requested
            )
        except Exception as error:
            figure_status = "failed"
            record_figure_failure_safely(store.run_dir, figure_dir, str(error))
    return GaussianExperimentResult(
        run_dir=store.run_dir,
        config_hash=store.config_hash,
        status=numerical_status,
        metrics=MappingProxyType(dict(metrics)),
        arrays=MappingProxyType(arrays),
        figure_status=figure_status,
        figure_dir=figure_dir,
    )
