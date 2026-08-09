"""Passive local-frame changes and generalized Gaussian spectral diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import scipy.linalg

from ...config import NumericsConfig
from .interactions import (
    GaussianNumericalError,
    _matrix_scale,
    _readonly,
    _symmetrize_checked,
    _validate_psd,
    _validate_spd,
)


def _validate_frames(
    frames: object,
    *,
    dimension: int | None,
    numerics: NumericsConfig,
    label: str,
) -> tuple[np.ndarray, np.ndarray]:
    value = np.asarray(frames, dtype=np.float64)
    if value.ndim != 3 or value.shape[0] < 1 or value.shape[1] != value.shape[2]:
        raise GaussianNumericalError(f"{label} must have shape (N, K, K)")
    if dimension is not None and value.shape[0] * value.shape[1] != dimension:
        raise GaussianNumericalError(f"{label} dimensions do not match the operator")
    if not np.all(np.isfinite(value)):
        raise GaussianNumericalError(f"{label} must contain only finite values")
    conditions: list[float] = []
    for index, block in enumerate(value):
        determinant_sign, log_absolute_determinant = np.linalg.slogdet(block)
        if determinant_sign <= 0.0 or not np.isfinite(log_absolute_determinant):
            raise GaussianNumericalError(
                f"{label} block {index} must have positive determinant"
            )
        condition = float(np.linalg.cond(block))
        boundary_tolerance = numerics.atol + numerics.rtol * max(
            numerics.max_frame_condition, 1.0
        )
        if (
            not np.isfinite(condition)
            or condition - numerics.max_frame_condition > boundary_tolerance
        ):
            raise GaussianNumericalError(
                f"{label} block {index} condition number exceeds max_frame_condition"
            )
        conditions.append(condition)
    return np.array(value, copy=True), np.asarray(conditions)


def _inverse_congruence(operator: np.ndarray, frame: np.ndarray) -> np.ndarray:
    left = scipy.linalg.solve(
        frame.T, operator, assume_a="gen", check_finite=False
    )
    return scipy.linalg.solve(
        frame.T, left.T, assume_a="gen", check_finite=False
    ).T


def _block_frame(frames: np.ndarray) -> np.ndarray:
    return scipy.linalg.block_diag(*frames)


def _generalized_diagnostics(
    laplacian: np.ndarray, precision: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    eigenvalues, eigenvectors = scipy.linalg.eigh(
        laplacian, precision, check_finite=False, driver="gvd"
    )
    laplacian_norm = _matrix_scale(laplacian)
    precision_norm = _matrix_scale(precision)
    residuals = []
    for value, vector in zip(eigenvalues, eigenvectors.T):
        residual = laplacian @ vector - value * (precision @ vector)
        denominator = max(
            (laplacian_norm + abs(float(value)) * precision_norm)
            * float(np.linalg.norm(vector)),
            np.finfo(np.float64).tiny,
        )
        residuals.append(float(np.linalg.norm(residual)) / denominator)
    metric = eigenvectors.T @ precision @ eigenvectors
    orthogonality = float(np.max(np.abs(metric - np.eye(metric.shape[0]))))
    return eigenvalues, eigenvectors, np.asarray(residuals), orthogonality


def _logdet(cholesky: np.ndarray) -> float:
    return float(2.0 * np.sum(np.log(np.diag(cholesky))))


def transform_prolongator(
    prolongator: object,
    fine_frames: object,
    coarse_frames: object,
    numerics: NumericsConfig,
    *,
    hold_fixed: bool = False,
) -> np.ndarray:
    """Transform ``S`` as ``T_f S T_c^-1`` or validate a fixed intertwiner."""
    fine, _ = _validate_frames(
        fine_frames, dimension=None, numerics=numerics, label="fine frames"
    )
    coarse, _ = _validate_frames(
        coarse_frames, dimension=None, numerics=numerics, label="coarse frames"
    )
    fine_frame = _block_frame(fine)
    coarse_frame = _block_frame(coarse)
    value = np.asarray(prolongator, dtype=np.float64)
    if value.shape != (fine_frame.shape[0], coarse_frame.shape[0]):
        raise GaussianNumericalError("prolongator shape does not match frame dimensions")
    if not np.all(np.isfinite(value)):
        raise GaussianNumericalError("prolongator must contain only finite values")
    left = fine_frame @ value
    if hold_fixed:
        right = value @ coarse_frame
        tolerance = numerics.atol + numerics.rtol * max(
            _matrix_scale(left), _matrix_scale(right)
        )
        if not np.allclose(left, right, atol=tolerance, rtol=0.0):
            raise GaussianNumericalError(
                "fixed prolongator does not intertwine fine and coarse frames"
            )
        return _readonly(value)
    transformed = scipy.linalg.solve(
        coarse_frame.T, left.T, assume_a="gen", check_finite=False
    ).T
    return _readonly(transformed)


@dataclass(frozen=True)
class GaussianGaugeResult:
    frames: np.ndarray
    block_frame: np.ndarray
    frame_condition_numbers: np.ndarray
    transformed_precision: np.ndarray
    transformed_laplacian: np.ndarray
    generalized_eigenvalues: np.ndarray
    transformed_generalized_eigenvalues: np.ndarray
    generalized_eigenvectors: np.ndarray
    transformed_generalized_eigenvectors: np.ndarray
    eigenpair_residuals: np.ndarray
    transformed_eigenpair_residuals: np.ndarray
    metric_orthogonality_residual: float
    transformed_metric_orthogonality_residual: float
    ordinary_eigenvalues: np.ndarray
    transformed_ordinary_eigenvalues: np.ndarray
    original_logdet: float
    transformed_logdet: float
    original_condition_number: float
    transformed_condition_number: float
    original_minimum_eigenvalue: float
    transformed_minimum_eigenvalue: float
    transformed_prolongator: np.ndarray | None


def apply_frame_change(
    precision: object,
    laplacian: object,
    frames: object,
    numerics: NumericsConfig,
    *,
    prolongator: object | None = None,
    coarse_frames: object | None = None,
) -> GaussianGaugeResult:
    """Apply a matched passive inverse congruence and compute independent checks."""
    if not isinstance(numerics, NumericsConfig):
        raise TypeError("numerics must be a NumericsConfig")
    raw_precision = np.asarray(precision, dtype=np.float64)
    raw_laplacian = np.asarray(laplacian, dtype=np.float64)
    if (
        raw_precision.ndim != 2
        or raw_precision.shape[0] != raw_precision.shape[1]
        or raw_laplacian.shape != raw_precision.shape
    ):
        raise GaussianNumericalError("precision and laplacian must be same-size square matrices")
    checked_precision = _symmetrize_checked(raw_precision, "precision", numerics)
    checked_laplacian = _symmetrize_checked(raw_laplacian, "laplacian", numerics)
    _validate_psd(checked_laplacian, "laplacian", numerics)
    original_cholesky, _, original_condition = _validate_spd(
        checked_precision, "precision", numerics
    )
    checked_frames, frame_conditions = _validate_frames(
        frames,
        dimension=checked_precision.shape[0],
        numerics=numerics,
        label="frames",
    )
    block_frame = _block_frame(checked_frames)
    transformed_precision = _inverse_congruence(checked_precision, block_frame)
    transformed_laplacian = _inverse_congruence(checked_laplacian, block_frame)
    transformed_precision = _symmetrize_checked(
        transformed_precision, "transformed precision", numerics
    )
    transformed_laplacian = _symmetrize_checked(
        transformed_laplacian, "transformed laplacian", numerics
    )
    _validate_psd(transformed_laplacian, "transformed laplacian", numerics)
    transformed_cholesky, _, transformed_condition = _validate_spd(
        transformed_precision, "transformed precision", numerics
    )
    (
        generalized,
        eigenvectors,
        eigenpair_residuals,
        orthogonality,
    ) = _generalized_diagnostics(checked_laplacian, checked_precision)
    (
        transformed_generalized,
        transformed_eigenvectors,
        transformed_eigenpair_residuals,
        transformed_orthogonality,
    ) = _generalized_diagnostics(transformed_laplacian, transformed_precision)
    if (prolongator is None) != (coarse_frames is None):
        raise GaussianNumericalError(
            "prolongator and coarse_frames must be supplied together"
        )
    transformed_prolongator = (
        None
        if prolongator is None
        else transform_prolongator(
            prolongator, checked_frames, coarse_frames, numerics
        )
    )
    return GaussianGaugeResult(
        frames=_readonly(checked_frames),
        block_frame=_readonly(block_frame),
        frame_condition_numbers=_readonly(frame_conditions),
        transformed_precision=_readonly(transformed_precision),
        transformed_laplacian=_readonly(transformed_laplacian),
        generalized_eigenvalues=_readonly(generalized),
        transformed_generalized_eigenvalues=_readonly(transformed_generalized),
        generalized_eigenvectors=_readonly(eigenvectors),
        transformed_generalized_eigenvectors=_readonly(transformed_eigenvectors),
        eigenpair_residuals=_readonly(eigenpair_residuals),
        transformed_eigenpair_residuals=_readonly(transformed_eigenpair_residuals),
        metric_orthogonality_residual=orthogonality,
        transformed_metric_orthogonality_residual=transformed_orthogonality,
        ordinary_eigenvalues=_readonly(scipy.linalg.eigvalsh(checked_laplacian)),
        transformed_ordinary_eigenvalues=_readonly(
            scipy.linalg.eigvalsh(transformed_laplacian)
        ),
        original_logdet=_logdet(original_cholesky),
        transformed_logdet=_logdet(transformed_cholesky),
        original_condition_number=original_condition,
        transformed_condition_number=transformed_condition,
        original_minimum_eigenvalue=float(scipy.linalg.eigvalsh(checked_precision)[0]),
        transformed_minimum_eigenvalue=float(
            scipy.linalg.eigvalsh(transformed_precision)[0]
        ),
        transformed_prolongator=transformed_prolongator,
    )


def generate_positive_orientation_frames(
    rng: np.random.Generator,
    n_vertices: int,
    block_size: int,
    *,
    max_condition: float,
) -> np.ndarray:
    """Generate deterministic positive-orientation frames with prescribed spectra."""
    if not isinstance(rng, np.random.Generator):
        raise TypeError("rng must be a numpy.random.Generator")
    if type(n_vertices) is not int or n_vertices < 1:
        raise ValueError("n_vertices must be a positive int")
    if type(block_size) is not int or block_size < 1:
        raise ValueError("block_size must be a positive int")
    if (
        type(max_condition) is not float
        or not np.isfinite(max_condition)
        or max_condition < 1.0
    ):
        raise ValueError("max_condition must be a finite float at least 1")
    singular_values = np.geomspace(1.0, max_condition, block_size)
    frames = []
    for _ in range(n_vertices):
        left, _ = np.linalg.qr(rng.normal(size=(block_size, block_size)))
        right, _ = np.linalg.qr(rng.normal(size=(block_size, block_size)))
        frame = left @ np.diag(singular_values) @ right.T
        determinant_sign, _ = np.linalg.slogdet(frame)
        if determinant_sign <= 0.0:
            left[:, 0] *= -1.0
            frame = left @ np.diag(singular_values) @ right.T
        frames.append(frame)
    return _readonly(np.stack(frames))
