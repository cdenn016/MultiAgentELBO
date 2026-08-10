"""Finite diagnostics for the preregistered scalarized Gaussian fixed-ray attack."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from types import MappingProxyType
from typing import Mapping, Sequence

import numpy as np


def _readonly(values: object, *, dtype: object = np.float64) -> np.ndarray:
    array = np.array(values, dtype=dtype, copy=True, order="C")
    array.setflags(write=False)
    return array


def _primitive_power(matrix: np.ndarray) -> int | None:
    power = np.eye(matrix.shape[0], dtype=np.float64)
    for exponent in range(1, matrix.shape[0] ** 2 + 1):
        power = power @ matrix
        if np.all(power > 0.0):
            return exponent
    return None


@dataclass(frozen=True, init=False)
class FixedRaySystem:
    """One frozen matrix ray and one or more primitive spatial endomorphisms."""

    matrix_direction: np.ndarray
    spatial_maps: Mapping[str, np.ndarray]
    perron_ray: np.ndarray
    node_factor: np.ndarray
    edge_labels: tuple[tuple[int, int], ...]
    basin_lower: float
    basin_upper: float
    log_block_scale: float
    primitive_powers: Mapping[str, int]
    noncommuting_gap: float

    def __init__(
        self,
        *,
        matrix_direction: object,
        spatial_maps: Mapping[str, object],
        perron_ray: object,
        node_factor: object,
        edge_labels: Sequence[tuple[int, int]],
        basin_lower: float,
        basin_upper: float,
        log_block_scale: float,
    ) -> None:
        matrix = np.array(matrix_direction, dtype=np.float64, copy=True, order="C")
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("matrix direction must be square")
        if not np.array_equal(matrix, matrix.T) or np.min(np.linalg.eigvalsh(matrix)) <= 0.0:
            raise ValueError("matrix direction must be symmetric positive definite")
        labels = tuple(edge_labels)
        if not labels or len(set(labels)) != len(labels):
            raise ValueError("edge labels must be nonempty and unique")
        perron = np.array(perron_ray, dtype=np.float64, copy=True, order="C")
        factor = np.array(node_factor, dtype=np.float64, copy=True, order="C")
        if perron.shape != (len(labels),) or np.any(perron <= 0.0):
            raise ValueError("Perron ray must be strictly positive with one entry per edge")
        if factor.ndim != 1 or np.any(factor <= 0.0):
            raise ValueError("node factor must be a strictly positive vector")
        try:
            factorized = np.array([factor[i] * factor[j] for i, j in labels])
        except IndexError as error:
            raise ValueError("edge labels exceed the node factor") from error
        if not np.allclose(factorized, perron, rtol=1e-13, atol=1e-15):
            raise ValueError("Perron ray must factorize as x_i x_j")
        if not spatial_maps:
            raise ValueError("at least one spatial map is required")
        validated_maps: dict[str, np.ndarray] = {}
        primitive_powers: dict[str, int] = {}
        for name, raw_map in spatial_maps.items():
            if type(name) is not str or not name:
                raise ValueError("spatial map names must be nonempty strings")
            spatial = np.array(raw_map, dtype=np.float64, copy=True, order="C")
            if spatial.shape != (len(labels), len(labels)):
                raise ValueError("spatial maps must act on the edge-coordinate space")
            if not np.all(np.isfinite(spatial)) or np.any(spatial < 0.0):
                raise ValueError("spatial maps must be finite nonnegative")
            primitive = _primitive_power(spatial)
            if primitive is None:
                raise ValueError("every spatial map must be primitive")
            image = spatial @ perron
            ratio = image / perron
            if not np.allclose(ratio, ratio[0], rtol=1e-12, atol=1e-14):
                raise ValueError("declared Perron ray is not an eigenray")
            spatial.setflags(write=False)
            validated_maps[name] = spatial
            primitive_powers[name] = primitive
        if not (
            np.isfinite(basin_lower)
            and np.isfinite(basin_upper)
            and 0.0 < basin_lower < basin_upper
        ):
            raise ValueError("basin bounds must be finite, positive, and ordered")
        if not np.isfinite(log_block_scale) or log_block_scale <= 0.0:
            raise ValueError("log block scale must be finite and positive")
        map_values = tuple(validated_maps.values())
        noncommuting_gap = 0.0
        for left_index in range(len(map_values)):
            for right_index in range(left_index + 1, len(map_values)):
                commutator = (
                    map_values[left_index] @ map_values[right_index]
                    - map_values[right_index] @ map_values[left_index]
                )
                noncommuting_gap = max(
                    noncommuting_gap, float(np.max(np.abs(commutator)))
                )
        matrix.setflags(write=False)
        perron.setflags(write=False)
        factor.setflags(write=False)
        object.__setattr__(self, "matrix_direction", matrix)
        object.__setattr__(self, "spatial_maps", MappingProxyType(validated_maps))
        object.__setattr__(self, "perron_ray", perron)
        object.__setattr__(self, "node_factor", factor)
        object.__setattr__(self, "edge_labels", labels)
        object.__setattr__(self, "basin_lower", float(basin_lower))
        object.__setattr__(self, "basin_upper", float(basin_upper))
        object.__setattr__(self, "log_block_scale", float(log_block_scale))
        object.__setattr__(self, "primitive_powers", MappingProxyType(primitive_powers))
        object.__setattr__(self, "noncommuting_gap", noncommuting_gap)

    def factorized_perron_ray(self) -> np.ndarray:
        return _readonly(
            [self.node_factor[i] * self.node_factor[j] for i, j in self.edge_labels]
        )


def build_preregistered_system() -> FixedRaySystem:
    """Return the exact finite system frozen in the preregistration."""
    adjacent = np.full((6, 6), 0.1, dtype=np.float64)
    np.fill_diagonal(adjacent, 0.5)
    alternating = 0.1 * np.array(
        [
            [3, 2, 2, 1, 1, 1],
            [1, 3, 2, 2, 1, 1],
            [1, 1, 3, 2, 2, 1],
            [2, 1, 1, 3, 2, 1],
            [1, 2, 1, 1, 3, 2],
            [2, 1, 2, 1, 1, 3],
        ],
        dtype=np.float64,
    )
    return FixedRaySystem(
        matrix_direction=((2.0, 0.5), (0.5, 1.0)),
        spatial_maps={
            "adjacent_pairs": adjacent,
            "balanced_alternating": alternating,
        },
        perron_ray=np.ones(6),
        node_factor=np.ones(4),
        edge_labels=((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)),
        basin_lower=0.25,
        basin_upper=4.0,
        log_block_scale=math.log(2.0),
    )


def job_seed(master_seed: int, job_id: str) -> int:
    """Derive one immutable unsigned 64-bit substream seed from a job ID."""
    if type(master_seed) is bool or type(master_seed) is not int or master_seed < 0:
        raise ValueError("master seed must be one nonnegative integer")
    if type(job_id) is not str or not job_id:
        raise ValueError("job ID must be a nonempty string")
    preimage = (
        b"gaussian-fixed-ray-v1\0"
        + str(master_seed).encode("ascii")
        + b"\0"
        + job_id.encode("ascii")
    )
    return int.from_bytes(hashlib.sha256(preimage).digest()[:8], "big")


def generate_initial_coefficients(
    master_seed: int, job_id: str, *, edge_count: int = 6
) -> np.ndarray:
    """Generate the preregistered positive CPU literal from its job substream."""
    if type(edge_count) is not int or edge_count <= 0:
        raise ValueError("edge_count must be a positive integer")
    generator = np.random.default_rng(job_seed(master_seed, job_id))
    values = np.exp(
        generator.uniform(math.log(0.25), math.log(4.0), size=edge_count)
    )
    return _readonly(values)


def _normalized(vector: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(vector))
    if not np.isfinite(norm) or norm <= 0.0:
        raise ValueError("projective vectors must have positive finite norm")
    return vector / norm


def projective_ray_angle(values: object, ray: object) -> float:
    """Return the Euclidean projective angle between two positive rays."""
    vector = np.asarray(values, dtype=np.float64)
    target = np.asarray(ray, dtype=np.float64)
    if vector.shape != target.shape or vector.ndim != 1:
        raise ValueError("projective vectors must have equal one-dimensional shape")
    chord = float(np.linalg.norm(_normalized(vector) - _normalized(target)))
    half_chord = min(max(0.5 * chord, 0.0), 1.0)
    return float(2.0 * math.asin(half_chord))


def scalarized_ray_construction_residual(
    coupling_matrices: object, matrix_direction: object
) -> float:
    """Measure roundoff consistency of the constructed frozen matrix ray."""
    couplings = np.asarray(coupling_matrices, dtype=np.float64)
    direction = np.asarray(matrix_direction, dtype=np.float64)
    if couplings.ndim != 3 or couplings.shape[1:] != direction.shape:
        raise ValueError("couplings must contain one matrix per spatial edge")
    direction_norm_sq = float(np.sum(direction * direction))
    if direction_norm_sq <= 0.0:
        raise ValueError("matrix direction must be nonzero")
    coefficients = np.einsum("eij,ij->e", couplings, direction) / direction_norm_sq
    residual = couplings - coefficients[:, None, None] * direction
    scale = float(np.linalg.norm(couplings))
    return 0.0 if scale == 0.0 else float(np.linalg.norm(residual) / scale)


@dataclass(frozen=True)
class FixedRayTrajectory:
    scheme: str
    coefficients: np.ndarray
    coupling_matrices: np.ndarray
    projective_ray_angles: np.ndarray
    normalized_coupling_distances: np.ndarray
    scalarized_ray_construction_residuals: np.ndarray
    retained_beta_residual_vectors: np.ndarray
    retained_beta_residuals: np.ndarray
    basin_exits: np.ndarray
    coefficient_conditioning: np.ndarray
    matrix_condition: float


def iterate_fixed_ray(
    system: FixedRaySystem,
    initial_coefficients: object,
    *,
    scheme: str,
    steps: int,
) -> FixedRayTrajectory:
    """Run one finite scalarized trajectory and retain every preregistered diagnostic."""
    if not isinstance(system, FixedRaySystem):
        raise TypeError("system must be a FixedRaySystem")
    if scheme not in system.spatial_maps:
        raise ValueError("unknown blocking scheme")
    if type(steps) is not int or steps < 0:
        raise ValueError("steps must be a nonnegative integer")
    initial = np.array(initial_coefficients, dtype=np.float64, copy=True, order="C")
    if initial.shape != system.perron_ray.shape or not np.all(np.isfinite(initial)) or np.any(initial <= 0.0):
        raise ValueError("initial coefficients must be one strictly positive finite spatial vector")
    coefficients = np.empty((steps + 1, initial.size), dtype=np.float64)
    coefficients[0] = initial
    spatial_map = system.spatial_maps[scheme]
    for index in range(steps):
        coefficients[index + 1] = spatial_map @ coefficients[index]
    couplings = coefficients[:, :, None, None] * system.matrix_direction
    angles = np.array(
        [projective_ray_angle(row, system.perron_ray) for row in coefficients]
    )
    target = _normalized(system.perron_ray)
    distances = np.array(
        [np.linalg.norm(_normalized(row) - target) for row in coefficients]
    )
    construction_residuals = np.array(
        [
            scalarized_ray_construction_residual(level, system.matrix_direction)
            for level in couplings
        ]
    )
    projection = np.outer(system.perron_ray, system.perron_ray) / float(
        np.dot(system.perron_ray, system.perron_ray)
    )
    finite_differences = coefficients[1:] - coefficients[:-1]
    retained_beta_vectors = np.array(
        [
            (np.eye(initial.size) - projection) @ difference
            / system.log_block_scale
            for difference in finite_differences
        ]
    )
    if steps == 0:
        retained_beta_vectors = np.empty((0, initial.size), dtype=np.float64)
    retained_beta = np.linalg.norm(retained_beta_vectors, axis=1)
    basin_exits = np.any(
        (coefficients < system.basin_lower) | (coefficients > system.basin_upper),
        axis=1,
    )
    conditioning = np.max(coefficients, axis=1) / np.min(coefficients, axis=1)
    return FixedRayTrajectory(
        scheme=scheme,
        coefficients=_readonly(coefficients),
        coupling_matrices=_readonly(couplings),
        projective_ray_angles=_readonly(angles),
        normalized_coupling_distances=_readonly(distances),
        scalarized_ray_construction_residuals=_readonly(construction_residuals),
        retained_beta_residual_vectors=_readonly(retained_beta_vectors),
        retained_beta_residuals=_readonly(retained_beta),
        basin_exits=_readonly(basin_exits, dtype=np.bool_),
        coefficient_conditioning=_readonly(conditioning),
        matrix_condition=float(np.linalg.cond(system.matrix_direction)),
    )


def blocking_scheme_dispersion(first: object, second: object) -> np.ndarray:
    """Return per-scale normalized-ray distance between paired schemes."""
    left = np.asarray(first, dtype=np.float64)
    right = np.asarray(second, dtype=np.float64)
    if left.shape != right.shape or left.ndim != 2:
        raise ValueError("paired scheme trajectories must have equal matrix shapes")
    values = np.array(
        [np.linalg.norm(_normalized(a) - _normalized(b)) for a, b in zip(left, right)]
    )
    return _readonly(values)


__all__ = [
    "FixedRaySystem",
    "FixedRayTrajectory",
    "blocking_scheme_dispersion",
    "build_preregistered_system",
    "generate_initial_coefficients",
    "iterate_fixed_ray",
    "job_seed",
    "projective_ray_angle",
    "scalarized_ray_construction_residual",
]
