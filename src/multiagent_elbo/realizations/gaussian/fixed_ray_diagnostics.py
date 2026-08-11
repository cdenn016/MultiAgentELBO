"""Exact identities and bounded certificates for the frozen fixed-ray maps."""

from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction
import math
from numbers import Real
from types import MappingProxyType

import numpy as np
from scipy import linalg as scipy_linalg

from .confirmatory_analysis import _ols_slope
from .fixed_ray import projective_ray_angle


FractionMatrix = tuple[tuple[Fraction, ...], ...]


_CANONICAL_FRACTION_MAPS: Mapping[str, FractionMatrix] = MappingProxyType(
    {
        "adjacent_pairs": (
            (
                Fraction(1, 2),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 10),
            ),
            (
                Fraction(1, 10),
                Fraction(1, 2),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 10),
            ),
            (
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 2),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 10),
            ),
            (
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 2),
                Fraction(1, 10),
                Fraction(1, 10),
            ),
            (
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 2),
                Fraction(1, 10),
            ),
            (
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 2),
            ),
        ),
        "balanced_alternating": (
            (
                Fraction(3, 10),
                Fraction(1, 5),
                Fraction(1, 5),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(1, 10),
            ),
            (
                Fraction(1, 10),
                Fraction(3, 10),
                Fraction(1, 5),
                Fraction(1, 5),
                Fraction(1, 10),
                Fraction(1, 10),
            ),
            (
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(3, 10),
                Fraction(1, 5),
                Fraction(1, 5),
                Fraction(1, 10),
            ),
            (
                Fraction(1, 5),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(3, 10),
                Fraction(1, 5),
                Fraction(1, 10),
            ),
            (
                Fraction(1, 10),
                Fraction(1, 5),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(3, 10),
                Fraction(1, 5),
            ),
            (
                Fraction(1, 5),
                Fraction(1, 10),
                Fraction(1, 5),
                Fraction(1, 10),
                Fraction(1, 10),
                Fraction(3, 10),
            ),
        ),
    }
)


def canonical_fraction_maps() -> Mapping[str, FractionMatrix]:
    """Return immutable, source-derived rational literals for both frozen maps."""

    return _CANONICAL_FRACTION_MAPS


def _require_fraction_square_matrix(matrix: object) -> FractionMatrix:
    if type(matrix) is not tuple:
        raise TypeError("matrix must be a canonical tuple of tuple rows")
    if not matrix:
        raise ValueError("matrix must be nonempty")
    dimension = len(matrix)
    for row in matrix:
        if type(row) is not tuple:
            raise TypeError("matrix rows must be canonical tuples")
        if len(row) != dimension:
            raise ValueError("matrix must be square")
        for value in row:
            if type(value) is float and not math.isfinite(value):
                raise ValueError("matrix entries must be finite")
            if type(value) is not Fraction:
                raise TypeError("matrix entries must be canonical Fraction values")
    return matrix


def _fraction_matrix_product(
    left: FractionMatrix,
    right: FractionMatrix,
) -> FractionMatrix:
    dimension = len(left)
    return tuple(
        tuple(
            sum(
                (left[row][index] * right[index][column] for index in range(dimension)),
                start=Fraction(0),
            )
            for column in range(dimension)
        )
        for row in range(dimension)
    )


def fraction_characteristic_polynomial(
    matrix: object,
) -> tuple[Fraction, ...]:
    """Return descending characteristic coefficients using exact arithmetic."""

    exact = _require_fraction_square_matrix(matrix)
    dimension = len(exact)
    identity: FractionMatrix = tuple(
        tuple(Fraction(int(row == column)) for column in range(dimension))
        for row in range(dimension)
    )
    auxiliary = identity
    coefficients = [Fraction(1)]
    for order in range(1, dimension + 1):
        product = _fraction_matrix_product(exact, auxiliary)
        coefficient = (
            -sum(
                (product[index][index] for index in range(dimension)),
                start=Fraction(0),
            )
            / order
        )
        coefficients.append(coefficient)
        auxiliary = tuple(
            tuple(
                product[row][column] + (coefficient if row == column else Fraction(0))
                for column in range(dimension)
            )
            for row in range(dimension)
        )
    return tuple(coefficients)


def _require_fraction(value: object, *, name: str) -> Fraction:
    if type(value) is not Fraction:
        raise TypeError(f"{name} must be a canonical Fraction value")
    return value


def _fraction_square_root(value: Fraction) -> Fraction | None:
    numerator_root = math.isqrt(value.numerator)
    denominator_root = math.isqrt(value.denominator)
    if (
        numerator_root * numerator_root != value.numerator
        or denominator_root * denominator_root != value.denominator
    ):
        return None
    return Fraction(numerator_root, denominator_root)


def adjacent_support_certificate(
    *,
    basin_lower: object,
    basin_upper: object,
    threshold: object,
) -> Mapping[str, object]:
    """Compute a generic bound and conditionally promote the frozen application."""

    lower = _require_fraction(basin_lower, name="basin_lower")
    upper = _require_fraction(basin_upper, name="basin_upper")
    support_threshold = _require_fraction(threshold, name="threshold")
    if lower <= 0 or upper <= lower:
        raise ValueError("basin bounds must satisfy 0 < basin_lower < basin_upper")
    if support_threshold >= 0:
        raise ValueError("support threshold must be negative")

    transverse_factor = Fraction(2, 5)
    ols_weights = tuple(Fraction(value, 10) for value in (-2, -1, 0, 1, 2))
    required_application_premises = (
        "complete_uncensored_endpoints_for_adjacent_pairs_and_balanced_alternating",
        "initial_coefficients_admitted_in_basin",
        "frozen_maps_unchanged",
        "endpoint_scales_4_through_8_unchanged",
        "raw_angle_ols_unchanged",
        "paired_least_favorable_maximum_unchanged",
    )
    frozen_input_scope_matches = (
        lower == Fraction(1, 4)
        and upper == Fraction(4)
        and support_threshold == Fraction(-1, 50)
    )
    common: dict[str, object] = {
        "basin_lower": lower,
        "basin_upper": upper,
        "threshold": support_threshold,
        "transverse_factor": transverse_factor,
        "ols_weights": ols_weights,
        "matrix_dimension": 6,
        "endpoint_scales": (4, 5, 6, 7, 8),
        "endpoint_angle": "raw_projective_angle",
        "endpoint_estimator": "ordinary_least_squares_slope",
        "paired_reduction": ("least_favorable_maximum_across_two_frozen_schemes"),
        "support_comparison": "upper_percentile_at_or_below_threshold",
        "required_application_premises": required_application_premises,
        "conclusion_is_conditional_on_required_premises": True,
        "actual_run_premises_validated": False,
        "frozen_input_scope_matches": frozen_input_scope_matches,
        "application_conclusion": "not_established",
        "theorem_status": "OPEN",
        "mathematical_verification_state": "INCONCLUSIVE",
        "verification_state": "CANDIDATE",
        "claim_origin": "APPLICATION_SPECIFIC",
        "attraction_claim": "not_established",
        "universality_claim": "not_established",
    }

    geometric_mean = _fraction_square_root(lower * upper)
    if geometric_mean is None:
        return MappingProxyType(
            {
                **common,
                "coefficient_of_variation_bound": None,
                "tan_theta4_bound": None,
                "slope_lower_bound": None,
                "rational_slope_lower_bound": None,
                "rational_margin_above_threshold": None,
                "arithmetic_certificate_status": "not_certified",
                "certificate_status": "not_certified",
                "paired_support_boundary_reachable": None,
                "not_certified_reason": (
                    "Bhatia-Davis bound has no rational square root in this encoding"
                ),
            }
        )

    coefficient_of_variation_bound = (upper - lower) / (2 * geometric_mean)
    tan_theta4_bound = transverse_factor**4 * coefficient_of_variation_bound
    slope_lower_bound = float(Fraction(-3, 10)) * math.atan(float(tan_theta4_bound))
    rational_slope_lower_bound = Fraction(-3, 10) * tan_theta4_bound
    rational_margin = rational_slope_lower_bound - support_threshold
    arithmetic_certified = rational_margin >= 0
    application_established = arithmetic_certified and frozen_input_scope_matches
    return MappingProxyType(
        {
            **common,
            "coefficient_of_variation_bound": coefficient_of_variation_bound,
            "tan_theta4_bound": tan_theta4_bound,
            "slope_lower_bound": slope_lower_bound,
            "rational_slope_lower_bound": rational_slope_lower_bound,
            "rational_margin_above_threshold": rational_margin,
            "arithmetic_certificate_status": (
                "bound_excludes_threshold" if arithmetic_certified else "not_certified"
            ),
            "certificate_status": (
                "certified_unreachable" if application_established else "not_certified"
            ),
            "paired_support_boundary_reachable": (
                False if application_established else None
            ),
            "application_conclusion": (
                "conditionally_paired_support_boundary_unreachable"
                if application_established
                else "not_established"
            ),
            "theorem_status": "ESTABLISHED" if application_established else "OPEN",
            "mathematical_verification_state": (
                "CANDIDATE" if application_established else "INCONCLUSIVE"
            ),
            "not_certified_reason": (
                None
                if application_established
                else (
                    "rational sufficient bound does not exclude threshold"
                    if not arithmetic_certified
                    else "frozen input scope does not match tracked derivation"
                )
            ),
        }
    )


def runtime_map_conformance(
    runtime_maps: object,
    exact_maps: object,
    *,
    atol: object,
) -> Mapping[str, float]:
    """Compare runtime float maps with exact literals without rationalizing floats."""

    if isinstance(atol, bool) or not isinstance(atol, Real):
        raise TypeError("atol must be one finite nonnegative real value")
    tolerance = float(atol)
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("atol must be finite and nonnegative")
    if not isinstance(runtime_maps, Mapping) or not isinstance(exact_maps, Mapping):
        raise TypeError("runtime_maps and exact_maps must be mappings")

    runtime_names = tuple(runtime_maps)
    exact_names = tuple(exact_maps)
    if any(type(name) is not str or not name for name in runtime_names + exact_names):
        raise TypeError("map names must be nonempty strings")
    if set(runtime_names) != set(exact_names):
        raise ValueError("runtime and exact map names must match exactly")

    validated_exact = {
        name: _require_fraction_square_matrix(exact_maps[name]) for name in exact_names
    }
    if validated_exact != dict(_CANONICAL_FRACTION_MAPS):
        raise ValueError("exact_maps must equal the canonical fixed-model literals")

    residuals: dict[str, float] = {}
    for name in exact_names:
        exact = validated_exact[name]
        runtime = np.asarray(runtime_maps[name])
        if runtime.ndim != 2 or runtime.shape != (len(exact), len(exact)):
            raise ValueError(f"runtime map {name!r} must match the exact square shape")
        if runtime.dtype.kind != "f":
            raise TypeError(f"runtime map {name!r} must contain floating values")
        if not bool(np.all(np.isfinite(runtime))):
            raise ValueError(f"runtime map {name!r} must contain only finite values")

        encoded_exact = np.array(
            [[float(value) for value in row] for row in exact],
            dtype=np.float64,
        )
        max_abs_error = float(np.max(np.abs(runtime - encoded_exact)))
        if max_abs_error > tolerance:
            raise ValueError(
                f"runtime map {name!r} residual {max_abs_error!r} exceeds atol "
                f"{tolerance!r}"
            )
        residuals[name] = max_abs_error
    return MappingProxyType(residuals)


def _finite_square_matrix_and_unit_representative(
    matrix: object,
    representative: object,
) -> tuple[np.ndarray, np.ndarray, float]:
    linear_map = np.asarray(matrix, dtype=np.float64)
    vector = np.asarray(representative, dtype=np.float64)
    if linear_map.ndim != 2 or linear_map.shape[0] != linear_map.shape[1]:
        raise ValueError("projective map must be square")
    if vector.ndim != 1 or vector.shape != (linear_map.shape[1],):
        raise ValueError("projective representative must match the map dimension")
    if not bool(np.all(np.isfinite(linear_map))) or not bool(
        np.all(np.isfinite(vector))
    ):
        raise ValueError("projective inputs must be finite")

    vector_scale = float(np.max(np.abs(vector))) if vector.size else 0.0
    matrix_scale = float(np.max(np.abs(linear_map))) if linear_map.size else 0.0
    if vector_scale == 0.0:
        raise ValueError("projective representative must be nonzero")
    if matrix_scale == 0.0:
        raise ValueError("projective map must have a nonzero image")

    scaled_vector = vector / vector_scale
    scaled_norm = float(np.linalg.norm(scaled_vector))
    unit = scaled_vector / scaled_norm
    scaled_map = linear_map / matrix_scale
    inverse_representative_norm = (1.0 / vector_scale) / scaled_norm
    return scaled_map, unit, inverse_representative_norm


def _finite_unit_vector(values: object) -> np.ndarray:
    vector = np.asarray(values, dtype=np.float64)
    if vector.ndim != 1 or not bool(np.all(np.isfinite(vector))):
        raise ValueError("projective representative must be a finite vector")
    scale = float(np.max(np.abs(vector))) if vector.size else 0.0
    if scale == 0.0:
        raise ValueError("projective representative must be nonzero")
    scaled = vector / scale
    return scaled / float(np.linalg.norm(scaled))


def normalized_projective_map(
    A: object,
    u: object,
) -> np.ndarray:
    """Apply one linear map and return its finite unit-sphere representative."""

    scaled_map, unit, _ = _finite_square_matrix_and_unit_representative(A, u)
    image = scaled_map @ unit
    return _finite_unit_vector(image)


def normalized_projective_jacobian(
    A: object,
    u: object,
) -> np.ndarray:
    """Return the ambient derivative of the unit-normalized projective map."""

    scaled_map, unit, inverse_norm = _finite_square_matrix_and_unit_representative(A, u)
    image = scaled_map @ unit
    next_unit = _finite_unit_vector(image)
    image_norm = float(np.linalg.norm(image))
    projector = np.eye(unit.size, dtype=np.float64) - np.outer(next_unit, next_unit)
    jacobian = (projector @ scaled_map) * (inverse_norm / image_norm)
    if not bool(np.all(np.isfinite(jacobian))):
        raise ValueError("normalized projective Jacobian is not finite")
    return jacobian


def orthonormal_tangent_basis(u: object) -> np.ndarray:
    """Return an orthonormal basis for the sphere tangent at ``u``."""

    unit = _finite_unit_vector(u)
    basis = scipy_linalg.null_space(unit.reshape(1, -1))
    basis = np.array(basis, dtype=np.float64, copy=True, order="C")
    basis.setflags(write=False)
    return basis


def reduced_tangent_step(
    A: object,
    u: object,
    next_u: object,
) -> np.ndarray:
    """Restrict one normalized-map derivative between orthonormal tangents."""

    first_basis = orthonormal_tangent_basis(u)
    next_basis = orthonormal_tangent_basis(next_u)
    jacobian = normalized_projective_jacobian(A, u)
    if next_basis.shape[0] != jacobian.shape[0]:
        raise ValueError("next projective representative must match the map dimension")
    reduced = np.array(
        next_basis.T @ jacobian @ first_basis,
        dtype=np.float64,
        copy=True,
        order="C",
    )
    reduced.setflags(write=False)
    return reduced


def _readonly_array(values: object, *, dtype: object = np.float64) -> np.ndarray:
    array = np.array(values, dtype=dtype, copy=True, order="C")
    array.setflags(write=False)
    return array


def _eigenvalue_multiplicities(
    eigenvalues: np.ndarray,
) -> tuple[Mapping[str, object], ...]:
    tolerance = 512.0 * np.finfo(np.float64).eps
    ordered = sorted(
        (complex(value) for value in eigenvalues),
        key=lambda value: (round(value.real, 13), round(value.imag, 13)),
    )
    groups: list[list[complex]] = []
    for value in ordered:
        if not groups:
            groups.append([value])
            continue
        representative = sum(groups[-1], start=0j) / len(groups[-1])
        scale = max(1.0, abs(value), abs(representative))
        if abs(value - representative) <= tolerance * scale:
            groups[-1].append(value)
        else:
            groups.append([value])

    records: list[Mapping[str, object]] = []
    for group in groups:
        representative = sum(group, start=0j) / len(group)
        real = 0.0 if abs(representative.real) <= tolerance else representative.real
        imag = 0.0 if abs(representative.imag) <= tolerance else representative.imag
        records.append(
            MappingProxyType(
                {
                    "real": float(real),
                    "imag": float(imag),
                    "multiplicity": len(group),
                }
            )
        )
    return tuple(records)


def spectral_diagnostics(
    A: object,
    perron_ray: object,
) -> Mapping[str, object]:
    """Return reduced Perron-tangent spectra and basis-invariant Schur data."""

    linear_map = np.asarray(A, dtype=np.float64)
    if linear_map.ndim != 2 or linear_map.shape[0] != linear_map.shape[1]:
        raise ValueError("spectral map must be square")
    if not bool(np.all(np.isfinite(linear_map))):
        raise ValueError("spectral map must be finite")
    perron_unit = _finite_unit_vector(perron_ray)
    if perron_unit.shape != (linear_map.shape[0],):
        raise ValueError("Perron ray must match the map dimension")

    image = linear_map @ perron_unit
    if not bool(np.all(np.isfinite(image))):
        raise ValueError("Perron image must be finite")
    perron_eigenvalue = float(np.dot(perron_unit, image))
    perron_scale = max(
        float(np.linalg.norm(image)),
        abs(perron_eigenvalue),
        np.finfo(np.float64).tiny,
    )
    perron_residual = float(
        np.linalg.norm(image - perron_eigenvalue * perron_unit) / perron_scale
    )
    tolerance = 512.0 * np.finfo(np.float64).eps
    if perron_eigenvalue <= 0.0 or perron_residual > tolerance:
        raise ValueError("declared Perron ray must be one positive eigenray")
    if abs(perron_eigenvalue - 1.0) > tolerance * max(1.0, perron_eigenvalue):
        raise ValueError("fixed-ray spectral diagnostics require unit Perron scaling")

    dimension = linear_map.shape[0]
    projector = np.eye(dimension, dtype=np.float64) - np.outer(perron_unit, perron_unit)
    tangent_basis = orthonormal_tangent_basis(perron_unit)
    tangent = tangent_basis.T @ projector @ linear_map @ tangent_basis
    tangent_dimension = tangent.shape[0]
    if tangent_dimension == 0:
        raise ValueError("spectral diagnostics require dimension at least two")

    tangent_scale = max(float(np.linalg.norm(tangent, ord="fro")), 1.0)
    scalar = float(np.trace(tangent) / tangent_dimension)
    canonical_adjacent = np.array(
        [
            [float(value) for value in row]
            for row in _CANONICAL_FRACTION_MAPS["adjacent_pairs"]
        ],
        dtype=np.float64,
    )
    scalar_tangent = np.array_equal(linear_map, canonical_adjacent)
    if scalar_tangent:
        eigenvalues = np.full(tangent_dimension, complex(scalar), dtype=np.complex128)
        singular_values = np.full(tangent_dimension, abs(scalar), dtype=np.float64)
        spectral_radius = abs(scalar)
    else:
        eigenvalues = np.linalg.eigvals(tangent)
        singular_values = np.linalg.svd(tangent, compute_uv=False)
        spectral_radius = float(np.max(np.abs(eigenvalues)))

    cluster_tolerance = (
        512.0 * np.finfo(np.float64).eps * max(1.0, spectral_radius, tangent_scale)
    )

    def select_slow_cluster(real: float, imag: float) -> bool:
        return abs(abs(complex(real, imag)) - spectral_radius) <= cluster_tolerance

    schur_form, schur_basis, slow_dimension = scipy_linalg.schur(
        tangent,
        output="real",
        sort=select_slow_cluster,
    )
    schur_residual = float(
        np.linalg.norm(
            tangent @ schur_basis - schur_basis @ schur_form,
            ord="fro",
        )
        / max(float(np.linalg.norm(tangent, ord="fro")), np.finfo(np.float64).tiny)
    )
    slow_tangent_basis = schur_basis[:, :slow_dimension]
    slow_projector = (
        tangent_basis @ slow_tangent_basis @ slow_tangent_basis.T @ tangent_basis.T
    )
    ambient_tangent_operator = projector @ linear_map @ projector
    slow_projector_residual = float(
        np.linalg.norm(
            (np.eye(dimension) - slow_projector)
            @ ambient_tangent_operator
            @ slow_projector,
            ord="fro",
        )
        / max(
            float(np.linalg.norm(ambient_tangent_operator, ord="fro")),
            np.finfo(np.float64).tiny,
        )
    )

    if scalar_tangent:
        absolute_gain = tuple(float(abs(scalar) ** horizon) for horizon in range(1, 9))
        spectral_excess = (1.0,) * 8
    else:
        gains: list[float] = []
        excess: list[float] = []
        for horizon in range(1, 9):
            gain = float(np.linalg.norm(np.linalg.matrix_power(tangent, horizon), 2))
            gains.append(gain)
            excess.append(
                float(gain / spectral_radius**horizon)
                if spectral_radius > 0.0
                else math.inf
            )
        absolute_gain = tuple(gains)
        spectral_excess = tuple(excess)

    return MappingProxyType(
        {
            "perron_unit": _readonly_array(perron_unit),
            "perron_projector": _readonly_array(projector),
            "perron_eigenvalue": perron_eigenvalue,
            "perron_residual": perron_residual,
            "tangent_basis": _readonly_array(tangent_basis),
            "tangent_operator": _readonly_array(tangent),
            "tangent_eigenvalues": _readonly_array(eigenvalues, dtype=np.complex128),
            "eigenvalue_multiplicities": _eigenvalue_multiplicities(eigenvalues),
            "tangent_singular_values": _readonly_array(singular_values),
            "spectral_radius": spectral_radius,
            "schur_form": _readonly_array(schur_form),
            "schur_basis": _readonly_array(schur_basis),
            "schur_residual": schur_residual,
            "slow_cluster_dimension": int(slow_dimension),
            "slow_tangent_basis": _readonly_array(slow_tangent_basis),
            "slow_projector": _readonly_array(slow_projector),
            "slow_projector_residual": slow_projector_residual,
            "absolute_gain": absolute_gain,
            "spectral_excess": spectral_excess,
            "transient_amplification": any(gain > 1.0 for gain in absolute_gain),
            "seed_alignment": (
                "not_applicable_degenerate_spectrum"
                if slow_dimension == tangent_dimension
                else "continuous_slow_projector_energy"
            ),
            "theorem_status": "NUMERICAL",
            "verification_state": "CANDIDATE",
        }
    )


def diagnose_trajectory(
    A: object,
    coefficients: object,
    perron_ray: object,
    scale_labels: object,
) -> Mapping[str, object]:
    """Reconstruct one frozen path and report only continuous diagnostics."""

    linear_map = np.asarray(A, dtype=np.float64)
    trajectory = np.asarray(coefficients, dtype=np.float64)
    if linear_map.ndim != 2 or linear_map.shape[0] != linear_map.shape[1]:
        raise ValueError("trajectory map must be square")
    if not bool(np.all(np.isfinite(linear_map))):
        raise ValueError("trajectory map must be finite")
    if trajectory.shape != (9, linear_map.shape[0]):
        raise ValueError("frozen trajectory must contain scales zero through eight")
    if not bool(np.all(np.isfinite(trajectory))):
        raise ValueError("trajectory coefficients must be finite")
    if bool(np.any(np.max(np.abs(trajectory), axis=1) == 0.0)):
        raise ValueError("every trajectory row must be a nonzero representative")

    labels = np.asarray(scale_labels, dtype=np.float64)
    frozen_labels = np.arange(9, dtype=np.float64)
    if labels.shape != frozen_labels.shape or not np.array_equal(labels, frozen_labels):
        raise ValueError("scale labels must equal the frozen zero-through-eight path")

    expected_rows = np.empty_like(trajectory[1:])
    bit_identity = True
    for index in range(8):
        expected_rows[index] = linear_map @ trajectory[index]
        bit_identity = bit_identity and np.array_equal(
            trajectory[index + 1], expected_rows[index]
        )
    recurrence_residuals = np.abs(trajectory[1:] - expected_rows)
    max_recurrence_residual = float(np.max(recurrence_residuals))
    max_abs_coefficient = float(np.max(np.abs(trajectory)))
    recurrence_tolerance = (
        8.0 * np.finfo(np.float64).eps * max(1.0, max_abs_coefficient)
    )
    if not bit_identity and max_recurrence_residual > recurrence_tolerance:
        raise ValueError("trajectory recurrence residual exceeds the frozen tolerance")

    units = tuple(_finite_unit_vector(row) for row in trajectory)
    all_angles = tuple(projective_ray_angle(row, perron_ray) for row in trajectory)
    endpoint_scales = (4, 5, 6, 7, 8)
    raw_angles = tuple(float(all_angles[scale]) for scale in endpoint_scales)
    log_angles: tuple[float | None, ...] = tuple(
        None if angle == 0.0 else float(math.log(angle)) for angle in raw_angles
    )
    one_step_ratios: tuple[float | None, ...] = tuple(
        (
            None
            if all_angles[scale - 1] == 0.0
            else float(all_angles[scale] / all_angles[scale - 1])
        )
        for scale in endpoint_scales
    )
    raw_angle_ols_slope = _ols_slope(np.asarray(raw_angles, dtype=np.float64))
    log_angle_ols_slope = (
        None
        if any(value is None for value in log_angles)
        else _ols_slope(np.asarray(log_angles, dtype=np.float64))
    )

    tangent_steps: list[np.ndarray] = []
    endpoint_propagators: list[np.ndarray] = []
    propagator = np.eye(linear_map.shape[0] - 1, dtype=np.float64)
    for index in range(8):
        tangent_step = np.asarray(
            reduced_tangent_step(linear_map, units[index], units[index + 1])
        )
        tangent_steps.append(tangent_step)
        propagator = tangent_step @ propagator
        if index + 1 in endpoint_scales:
            endpoint_propagators.append(np.array(propagator, copy=True))
    reduced_propagators = np.stack(endpoint_propagators)
    reduced_propagator_norms = tuple(
        float(np.linalg.norm(propagator_value, 2))
        for propagator_value in reduced_propagators
    )
    reduced_propagator_condition_numbers = tuple(
        float(np.linalg.cond(propagator_value))
        for propagator_value in reduced_propagators
    )

    spectrum = spectral_diagnostics(linear_map, perron_ray)
    perron_projector = np.asarray(spectrum["perron_projector"])
    delta = perron_projector @ units[0]
    zero_transverse = all_angles[0] == 0.0
    if zero_transverse:
        actual_direction_gains: tuple[float | None, ...] = (None,) * 8
        slow_energy: float | None = None
        seed_alignment = "not_applicable_zero_transverse_deviation"
    else:
        tangent_basis = np.asarray(spectrum["tangent_basis"])
        tangent_operator = np.asarray(spectrum["tangent_operator"])
        coordinates = tangent_basis.T @ delta
        coordinate_norm = float(np.linalg.norm(coordinates))
        actual_direction_gains = tuple(
            float(
                np.linalg.norm(
                    np.linalg.matrix_power(tangent_operator, horizon) @ coordinates
                )
                / coordinate_norm
            )
            for horizon in range(1, 9)
        )
        seed_alignment = str(spectrum["seed_alignment"])
        if seed_alignment == "not_applicable_degenerate_spectrum":
            slow_energy = None
        else:
            slow_projector = np.asarray(spectrum["slow_projector"])
            slow_energy = float(
                np.linalg.norm(slow_projector @ delta) ** 2 / np.linalg.norm(delta) ** 2
            )

    return MappingProxyType(
        {
            "endpoint_scales": endpoint_scales,
            "raw_angles": raw_angles,
            "log_angles": log_angles,
            "one_step_angle_ratios": one_step_ratios,
            "raw_angle_ols_slope": raw_angle_ols_slope,
            "log_angle_ols_slope": log_angle_ols_slope,
            "recurrence_bit_identical": bit_identity,
            "max_recurrence_residual": max_recurrence_residual,
            "recurrence_tolerance": recurrence_tolerance,
            "reduced_tangent_steps": _readonly_array(tangent_steps),
            "reduced_propagators": _readonly_array(reduced_propagators),
            "reduced_propagator_norms": reduced_propagator_norms,
            "reduced_propagator_condition_numbers": (
                reduced_propagator_condition_numbers
            ),
            "actual_direction_gains": actual_direction_gains,
            "actual_gain": MappingProxyType(
                {
                    horizon: actual_direction_gains[horizon - 1]
                    for horizon in range(1, 9)
                }
            ),
            "slow_energy": slow_energy,
            "continuous_mode_projector_energy": slow_energy,
            "seed_alignment": seed_alignment,
            "theorem_status": "NUMERICAL",
            "verification_state": "CANDIDATE",
        }
    )


def summarize_population(
    records: object,
    *,
    population: str,
) -> Mapping[str, object]:
    """Reduce one frozen population without inspecting the other population."""

    if population not in {"C", "H"}:
        if population == "C+H":
            raise ValueError("pooled C+H population summaries are prohibited")
        raise ValueError("population must be exactly 'C' or 'H'")
    if isinstance(records, (str, bytes, Mapping)):
        raise TypeError("records must be an iterable of diagnostic mappings")
    try:
        supplied_records = tuple(records)  # type: ignore[arg-type]
    except TypeError as error:
        raise TypeError("records must be an iterable of diagnostic mappings") from error

    expected_count = 30 if population == "C" else 10
    expected_job_ids = tuple(
        f"{population}{index:03d}" for index in range(1, expected_count + 1)
    )
    expected_job_set = set(expected_job_ids)
    schemes = ("adjacent_pairs", "balanced_alternating")
    by_job: dict[str, dict[str, float]] = {job_id: {} for job_id in expected_job_ids}

    for record in supplied_records:
        if not isinstance(record, Mapping):
            raise TypeError("every population record must be a mapping")
        job_id = record.get("job_id")
        if type(job_id) is not str or not job_id:
            raise ValueError("every population record must carry one job_id")
        if not job_id.startswith(population):
            continue
        if job_id not in expected_job_set:
            raise ValueError("selected population contains an unexpected job ID")

        scheme = record.get("scheme")
        if scheme not in schemes:
            raise ValueError("selected population records require both frozen schemes")
        if scheme in by_job[job_id]:
            raise ValueError("duplicate selected population job/scheme record")
        slope = record.get("raw_angle_ols_slope")
        if isinstance(slope, bool) or not isinstance(slope, Real):
            raise TypeError("raw-angle OLS slopes must be real scalars")
        numeric_slope = float(slope)
        if not math.isfinite(numeric_slope):
            raise ValueError("raw-angle OLS slopes must be finite")
        if record.get("verification_state") != "CANDIDATE":
            raise ValueError("producer population records must remain CANDIDATE")

        master_seed = record.get("master_seed")
        expected_seed = (202608090100 if population == "C" else 202608090200) + int(
            job_id[1:]
        )
        if type(master_seed) is not int or master_seed != expected_seed:
            raise ValueError("selected population master seed does not match its job")
        by_job[job_id][str(scheme)] = numeric_slope

    for job_id in expected_job_ids:
        if set(by_job[job_id]) != set(schemes):
            raise ValueError("every selected job must contain exactly two schemes")

    map_specific = {
        scheme: tuple(by_job[job_id][scheme] for job_id in expected_job_ids)
        for scheme in schemes
    }
    paired = tuple(
        max(by_job[job_id][scheme] for scheme in schemes) for job_id in expected_job_ids
    )
    per_job = tuple(
        MappingProxyType(
            {
                "job_id": job_id,
                "adjacent_pairs": by_job[job_id]["adjacent_pairs"],
                "balanced_alternating": by_job[job_id]["balanced_alternating"],
                "least_favorable": paired[index],
            }
        )
        for index, job_id in enumerate(expected_job_ids)
    )
    return MappingProxyType(
        {
            "population": population,
            "scope": (
                "confirmatory_primary"
                if population == "C"
                else "descriptive_replication_only"
            ),
            "job_count": expected_count,
            "job_ids": expected_job_ids,
            "scheme_ids": schemes,
            "map_specific_raw_angle_ols_slopes": MappingProxyType(map_specific),
            "paired_least_favorable_raw_angle_ols_slopes": paired,
            "per_job": per_job,
            "paired_reduction": ("least_favorable_maximum_across_two_frozen_schemes"),
            "estimate": float(np.median(np.asarray(paired, dtype=np.float64))),
            "theorem_status": "NUMERICAL",
            "verification_state": "CANDIDATE",
        }
    )
