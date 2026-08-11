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


def _require_bool(value: object, *, name: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f"{name} must be a Boolean value")
    return value


def _require_endpoint_schemes(
    value: object,
    *,
    name: str,
    required_schemes: tuple[str, ...],
) -> tuple[str, ...]:
    if type(value) is not tuple or any(type(item) is not str for item in value):
        raise TypeError(f"{name} must be a tuple of frozen scheme names")
    if len(set(value)) != len(value):
        raise ValueError(f"{name} must not contain duplicate scheme names")
    if not set(value).issubset(required_schemes):
        raise ValueError(f"{name} contains an unknown frozen scheme name")
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
    complete_endpoint_schemes: object = (),
    censored_endpoint_schemes: object = (),
    initial_coefficients_admitted_in_basin: object = False,
    frozen_maps_unchanged: object = False,
    endpoint_scales_4_through_8_unchanged: object = False,
    raw_angle_ols_unchanged: object = False,
    paired_least_favorable_max_unchanged: object = False,
) -> Mapping[str, object]:
    """Compute a generic bound and conditionally promote the frozen application."""

    lower = _require_fraction(basin_lower, name="basin_lower")
    upper = _require_fraction(basin_upper, name="basin_upper")
    support_threshold = _require_fraction(threshold, name="threshold")
    if lower <= 0 or upper <= lower:
        raise ValueError("basin bounds must satisfy 0 < basin_lower < basin_upper")
    if support_threshold >= 0:
        raise ValueError("support threshold must be negative")

    required_endpoint_schemes = (
        "adjacent_pairs",
        "balanced_alternating",
    )
    complete_schemes = _require_endpoint_schemes(
        complete_endpoint_schemes,
        name="complete_endpoint_schemes",
        required_schemes=required_endpoint_schemes,
    )
    censored_schemes = _require_endpoint_schemes(
        censored_endpoint_schemes,
        name="censored_endpoint_schemes",
        required_schemes=required_endpoint_schemes,
    )
    admitted_initial_coefficients = _require_bool(
        initial_coefficients_admitted_in_basin,
        name="initial_coefficients_admitted_in_basin",
    )
    unchanged_maps = _require_bool(
        frozen_maps_unchanged,
        name="frozen_maps_unchanged",
    )
    unchanged_scales = _require_bool(
        endpoint_scales_4_through_8_unchanged,
        name="endpoint_scales_4_through_8_unchanged",
    )
    unchanged_raw_angle_ols = _require_bool(
        raw_angle_ols_unchanged,
        name="raw_angle_ols_unchanged",
    )
    unchanged_paired_max = _require_bool(
        paired_least_favorable_max_unchanged,
        name="paired_least_favorable_max_unchanged",
    )

    transverse_factor = Fraction(2, 5)
    ols_weights = tuple(Fraction(value, 10) for value in (-2, -1, 0, 1, 2))
    complete_endpoints = (
        set(complete_schemes) == set(required_endpoint_schemes)
        and not censored_schemes
    )
    application_premises_satisfied = all(
        (
            complete_endpoints,
            admitted_initial_coefficients,
            unchanged_maps,
            unchanged_scales,
            unchanged_raw_angle_ols,
            unchanged_paired_max,
        )
    )
    frozen_input_scope_matches = (
        lower == Fraction(1, 4)
        and upper == Fraction(4)
        and support_threshold == Fraction(-1, 50)
    )
    application_scope_matches = (
        frozen_input_scope_matches and application_premises_satisfied
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
        "paired_reduction": (
            "least_favorable_maximum_across_two_frozen_schemes"
        ),
        "support_comparison": "upper_percentile_at_or_below_threshold",
        "required_complete_endpoint_schemes": required_endpoint_schemes,
        "complete_endpoint_schemes": complete_schemes,
        "censored_endpoint_schemes": censored_schemes,
        "complete_endpoints_for_both_frozen_schemes": complete_endpoints,
        "initial_coefficients_admitted_in_basin": admitted_initial_coefficients,
        "frozen_maps_unchanged": unchanged_maps,
        "endpoint_scales_4_through_8_unchanged": unchanged_scales,
        "raw_angle_ols_unchanged": unchanged_raw_angle_ols,
        "paired_least_favorable_max_unchanged": unchanged_paired_max,
        "application_premises_satisfied": application_premises_satisfied,
        "frozen_input_scope_matches": frozen_input_scope_matches,
        "application_scope_matches": application_scope_matches,
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
    application_established = arithmetic_certified and application_scope_matches
    return MappingProxyType(
        {
            **common,
            "coefficient_of_variation_bound": coefficient_of_variation_bound,
            "tan_theta4_bound": tan_theta4_bound,
            "slope_lower_bound": slope_lower_bound,
            "rational_slope_lower_bound": rational_slope_lower_bound,
            "rational_margin_above_threshold": rational_margin,
            "arithmetic_certificate_status": (
                "bound_excludes_threshold"
                if arithmetic_certified
                else "not_certified"
            ),
            "certificate_status": (
                "certified_unreachable"
                if application_established
                else "not_certified"
            ),
            "paired_support_boundary_reachable": (
                False if application_established else None
            ),
            "application_conclusion": (
                "paired_support_boundary_unreachable"
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
                    else "application premises or frozen input scope do not match"
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
