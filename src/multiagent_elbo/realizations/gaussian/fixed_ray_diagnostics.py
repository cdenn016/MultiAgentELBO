"""Exact identities and bounded certificates for the frozen fixed-ray maps."""

from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction
import math
from numbers import Real
from types import MappingProxyType

import numpy as np


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
    """Certify endpoint infeasibility for the frozen adjacent-map reduction."""

    lower = _require_fraction(basin_lower, name="basin_lower")
    upper = _require_fraction(basin_upper, name="basin_upper")
    support_threshold = _require_fraction(threshold, name="threshold")
    if lower <= 0 or upper <= lower:
        raise ValueError("basin bounds must satisfy 0 < basin_lower < basin_upper")
    if support_threshold >= 0:
        raise ValueError("support threshold must be negative")

    transverse_factor = Fraction(2, 5)
    ols_weights = tuple(Fraction(value, 10) for value in (-2, -1, 0, 1, 2))
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
        "paired_reduction": "maximum",
        "support_comparison": "upper_percentile_at_or_below_threshold",
        "theorem_status": "ESTABLISHED",
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
    certified = rational_margin >= 0
    return MappingProxyType(
        {
            **common,
            "coefficient_of_variation_bound": coefficient_of_variation_bound,
            "tan_theta4_bound": tan_theta4_bound,
            "slope_lower_bound": slope_lower_bound,
            "rational_slope_lower_bound": rational_slope_lower_bound,
            "rational_margin_above_threshold": rational_margin,
            "certificate_status": (
                "certified_unreachable" if certified else "not_certified"
            ),
            "paired_support_boundary_reachable": False if certified else None,
            "not_certified_reason": (
                None
                if certified
                else "rational sufficient bound does not exclude threshold"
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
