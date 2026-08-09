"""Stable matrix-weighted Gaussian interaction operators and coarse restrictions."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping, Sequence

import numpy as np
import scipy.linalg

from ...config import NumericsConfig


class GaussianNumericalError(ValueError):
    """Raised when a Gaussian operator violates a declared numerical domain."""


def _readonly(array: np.ndarray) -> np.ndarray:
    owned = np.array(array, dtype=np.float64, copy=True)
    owned.setflags(write=False)
    return owned


def _matrix_scale(matrix: np.ndarray) -> float:
    return max(float(np.linalg.norm(matrix, ord=2)), np.finfo(np.float64).tiny)


def _symmetrize_checked(
    matrix: object, label: str, numerics: NumericsConfig
) -> np.ndarray:
    value = np.asarray(matrix, dtype=np.float64)
    if value.ndim != 2 or value.shape[0] != value.shape[1]:
        raise GaussianNumericalError(f"{label} must be a square matrix")
    if not np.all(np.isfinite(value)):
        raise GaussianNumericalError(f"{label} must contain only finite values")
    scale = _matrix_scale(value)
    residual = float(np.linalg.norm(value - value.T, ord="fro")) / scale
    if residual > numerics.atol + numerics.rtol:
        raise GaussianNumericalError(f"{label} is not symmetric within tolerance")
    return (value + value.T) * 0.5


def _validate_psd(
    matrix: np.ndarray, label: str, numerics: NumericsConfig
) -> float:
    minimum = float(scipy.linalg.eigvalsh(matrix, check_finite=False)[0])
    tolerance = numerics.atol + numerics.rtol * _matrix_scale(matrix)
    if minimum < -tolerance:
        raise GaussianNumericalError(f"{label} is not positive semidefinite")
    return minimum


def _validate_spd(
    matrix: np.ndarray, label: str, numerics: NumericsConfig
) -> tuple[np.ndarray, float, float]:
    if not np.all(np.isfinite(matrix)):
        raise GaussianNumericalError(f"{label} must contain only finite values")
    symmetric = _symmetrize_checked(matrix, label, numerics)
    try:
        cholesky = scipy.linalg.cholesky(
            symmetric, lower=True, check_finite=False
        )
    except scipy.linalg.LinAlgError as error:
        raise GaussianNumericalError(f"{label} is not positive definite") from error
    condition = float(np.linalg.cond(symmetric))
    reciprocal_condition = 0.0 if not math_isfinite_positive(condition) else 1.0 / condition
    if reciprocal_condition < numerics.min_spd_rcond:
        raise GaussianNumericalError(
            f"{label} reciprocal condition {reciprocal_condition:.6g} is below min_spd_rcond"
        )
    return cholesky, reciprocal_condition, condition


def math_isfinite_positive(value: float) -> bool:
    return bool(np.isfinite(value) and value > 0.0)


def _coerce_blocks(
    self_terms: Sequence[object] | np.ndarray, numerics: NumericsConfig
) -> np.ndarray:
    try:
        raw = np.asarray(self_terms, dtype=np.float64)
    except (TypeError, ValueError) as error:
        raise GaussianNumericalError("mixed scalar and matrix block sizes") from error
    if raw.ndim == 1:
        if raw.size == 0:
            raise GaussianNumericalError("at least one self block is required")
        blocks = raw[:, None, None]
    elif raw.ndim == 3 and raw.shape[0] > 0 and raw.shape[1] == raw.shape[2]:
        blocks = raw
    else:
        raise GaussianNumericalError("self terms must have consistent square block sizes")
    normalized: list[np.ndarray] = []
    for index, block in enumerate(blocks):
        symmetric = _symmetrize_checked(block, f"self block {index}", numerics)
        _validate_psd(symmetric, f"self block {index}", numerics)
        normalized.append(symmetric)
    return np.stack(normalized)


@dataclass(frozen=True)
class GaussianInteraction:
    """An SPD self-plus-matrix-weighted-Laplacian precision operator."""

    self_blocks: np.ndarray
    edge_blocks: Mapping[tuple[int, int], np.ndarray]
    laplacian: np.ndarray
    precision: np.ndarray
    reciprocal_condition: float
    condition_number: float
    minimum_precision_eigenvalue: float
    numerics: NumericsConfig

    @property
    def n_vertices(self) -> int:
        return int(self.self_blocks.shape[0])

    @property
    def block_size(self) -> int:
        return int(self.self_blocks.shape[1])

    @classmethod
    def from_self_and_edges(
        cls,
        self_terms: Sequence[object] | np.ndarray,
        edges: Mapping[tuple[int, int], object],
        numerics: NumericsConfig,
    ) -> "GaussianInteraction":
        if not isinstance(numerics, NumericsConfig):
            raise TypeError("numerics must be a NumericsConfig")
        self_blocks = _coerce_blocks(self_terms, numerics)
        n_vertices, block_size, _ = self_blocks.shape
        normalized_edges: dict[tuple[int, int], np.ndarray] = {}
        undirected: set[tuple[int, int]] = set()
        for key, raw_weight in edges.items():
            if (
                type(key) is not tuple
                or len(key) != 2
                or type(key[0]) is not int
                or type(key[1]) is not int
            ):
                raise GaussianNumericalError("edge keys must be integer vertex pairs")
            source, target = key
            if source == target:
                raise GaussianNumericalError("self-loop edge is not allowed")
            if not (0 <= source < n_vertices and 0 <= target < n_vertices):
                raise GaussianNumericalError("edge vertex is outside the interaction")
            canonical = (min(source, target), max(source, target))
            if canonical in undirected:
                raise GaussianNumericalError("duplicate reversed edge is not allowed")
            undirected.add(canonical)
            raw = np.asarray(raw_weight, dtype=np.float64)
            if block_size == 1 and raw.ndim == 0:
                raw = raw.reshape(1, 1)
            elif raw.shape != (block_size, block_size):
                if raw.ndim == 0 or raw.shape == (1, 1):
                    raise GaussianNumericalError("mixed scalar and matrix block sizes")
                raise GaussianNumericalError("edge block shape does not match self blocks")
            symmetric = _symmetrize_checked(raw, f"edge {canonical}", numerics)
            _validate_psd(symmetric, f"edge {canonical}", numerics)
            normalized_edges[canonical] = _readonly(symmetric)

        dimension = n_vertices * block_size
        laplacian = np.zeros((dimension, dimension), dtype=np.float64)
        precision = scipy.linalg.block_diag(*self_blocks)
        for (source, target), weight in normalized_edges.items():
            source_slice = slice(source * block_size, (source + 1) * block_size)
            target_slice = slice(target * block_size, (target + 1) * block_size)
            laplacian[source_slice, source_slice] += weight
            laplacian[target_slice, target_slice] += weight
            laplacian[source_slice, target_slice] -= weight
            laplacian[target_slice, source_slice] -= weight
        precision = precision + laplacian
        laplacian = _symmetrize_checked(laplacian, "assembled laplacian", numerics)
        _validate_psd(laplacian, "assembled laplacian", numerics)
        precision = _symmetrize_checked(precision, "assembled precision", numerics)
        _, reciprocal_condition, condition = _validate_spd(
            precision, "assembled precision", numerics
        )
        minimum = float(scipy.linalg.eigvalsh(precision, check_finite=False)[0])
        owned_self = _readonly(self_blocks)
        owned_edges = MappingProxyType(dict(sorted(normalized_edges.items())))
        return cls(
            self_blocks=owned_self,
            edge_blocks=owned_edges,
            laplacian=_readonly(laplacian),
            precision=_readonly(precision),
            reciprocal_condition=reciprocal_condition,
            condition_number=condition,
            minimum_precision_eigenvalue=minimum,
            numerics=numerics,
        )


@dataclass(frozen=True)
class GaussianAggregationResult:
    """Operator-level hard-identification/Galerkin restriction result."""

    partition: tuple[tuple[int, ...], ...]
    prolongator: np.ndarray
    self_blocks: np.ndarray
    edge_blocks: Mapping[tuple[int, int], np.ndarray]
    laplacian: np.ndarray
    precision: np.ndarray
    method: str = "operator_level_hard_identification_galerkin"
    is_gaussian_marginal: bool = False
    is_probability_pushforward: bool = False


def _validate_partition(
    partition: Iterable[Iterable[int]], n_vertices: int
) -> tuple[tuple[int, ...], ...]:
    try:
        owned = tuple(tuple(block) for block in partition)
    except TypeError as error:
        raise GaussianNumericalError("partition must be an iterable of blocks") from error
    if not owned or any(not block for block in owned):
        raise GaussianNumericalError("partition contains an empty block")
    flattened = [vertex for block in owned for vertex in block]
    if any(type(vertex) is not int for vertex in flattened):
        raise GaussianNumericalError("partition vertices must be ints")
    if sorted(flattened) != list(range(n_vertices)):
        raise GaussianNumericalError("partition must own each vertex exactly once")
    return owned


def galerkin_aggregate_precision(
    interaction: GaussianInteraction, partition: Iterable[Iterable[int]]
) -> GaussianAggregationResult:
    """Restrict a fine operator to coordinates constant within each cluster."""
    if not isinstance(interaction, GaussianInteraction):
        raise TypeError("interaction must be a GaussianInteraction")
    owned_partition = _validate_partition(partition, interaction.n_vertices)
    block_size = interaction.block_size
    prolongator = np.zeros(
        (interaction.n_vertices * block_size, len(owned_partition) * block_size),
        dtype=np.float64,
    )
    cluster_of: dict[int, int] = {}
    for cluster, vertices in enumerate(owned_partition):
        for vertex in vertices:
            cluster_of[vertex] = cluster
            prolongator[
                vertex * block_size : (vertex + 1) * block_size,
                cluster * block_size : (cluster + 1) * block_size,
            ] = np.eye(block_size)
    self_blocks = np.stack(
        [np.sum(interaction.self_blocks[list(vertices)], axis=0) for vertices in owned_partition]
    )
    coarse_edges: dict[tuple[int, int], np.ndarray] = {}
    for (source, target), weight in interaction.edge_blocks.items():
        coarse_source = cluster_of[source]
        coarse_target = cluster_of[target]
        if coarse_source == coarse_target:
            continue
        key = (min(coarse_source, coarse_target), max(coarse_source, coarse_target))
        coarse_edges[key] = coarse_edges.get(key, np.zeros_like(weight)) + weight
    coarse = GaussianInteraction.from_self_and_edges(
        self_blocks, coarse_edges, interaction.numerics
    )
    restricted = prolongator.T @ interaction.precision @ prolongator
    tolerance = interaction.numerics.atol + interaction.numerics.rtol * _matrix_scale(restricted)
    if not np.allclose(restricted, coarse.precision, atol=tolerance, rtol=0.0):
        raise GaussianNumericalError("Galerkin restriction does not match coarse blocks")
    return GaussianAggregationResult(
        partition=owned_partition,
        prolongator=_readonly(prolongator),
        self_blocks=coarse.self_blocks,
        edge_blocks=coarse.edge_blocks,
        laplacian=coarse.laplacian,
        precision=_readonly(restricted),
    )


def schur_complement_precision(
    precision: object,
    *,
    retained_vertices: Sequence[int],
    block_size: int,
    numerics: NumericsConfig,
) -> np.ndarray:
    """Return the Gaussian marginal precision by eliminating all other blocks."""
    value = np.asarray(precision, dtype=np.float64)
    if type(block_size) is not int or block_size < 1:
        raise GaussianNumericalError("block_size must be a positive int")
    if value.ndim != 2 or value.shape[0] != value.shape[1] or value.shape[0] % block_size:
        raise GaussianNumericalError("precision shape is incompatible with block_size")
    value = _symmetrize_checked(value, "precision", numerics)
    _validate_spd(value, "precision", numerics)
    n_vertices = value.shape[0] // block_size
    retained = tuple(retained_vertices)
    if (
        not retained
        or len(set(retained)) != len(retained)
        or any(type(vertex) is not int or not 0 <= vertex < n_vertices for vertex in retained)
    ):
        raise GaussianNumericalError("retained_vertices must be unique valid vertices")
    eliminated = tuple(vertex for vertex in range(n_vertices) if vertex not in retained)
    if not eliminated:
        return _readonly(value)
    retained_indices = np.concatenate(
        [np.arange(vertex * block_size, (vertex + 1) * block_size) for vertex in retained]
    )
    eliminated_indices = np.concatenate(
        [np.arange(vertex * block_size, (vertex + 1) * block_size) for vertex in eliminated]
    )
    rr = value[np.ix_(retained_indices, retained_indices)]
    re = value[np.ix_(retained_indices, eliminated_indices)]
    ee = value[np.ix_(eliminated_indices, eliminated_indices)]
    er = value[np.ix_(eliminated_indices, retained_indices)]
    try:
        factor = scipy.linalg.cho_factor(ee, lower=True, check_finite=False)
        solved = scipy.linalg.cho_solve(factor, er, check_finite=False)
    except scipy.linalg.LinAlgError as error:
        raise GaussianNumericalError("eliminated precision block is not positive definite") from error
    schur = rr - re @ solved
    schur = _symmetrize_checked(schur, "Schur complement", numerics)
    _validate_spd(schur, "Schur complement", numerics)
    return _readonly(schur)
