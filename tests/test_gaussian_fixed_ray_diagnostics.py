from fractions import Fraction
import json
import math

import numpy as np
import pytest


def _multiply_polynomials(
    left: tuple[Fraction, ...],
    right: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    coefficients = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            coefficients[left_index + right_index] += left_value * right_value
    return tuple(coefficients)


def _differentiate_polynomial(
    coefficients: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    degree = len(coefficients) - 1
    return tuple(
        coefficient * (degree - index)
        for index, coefficient in enumerate(coefficients[:-1])
    )


def _evaluate_polynomial(
    coefficients: tuple[Fraction, ...],
    value: Fraction,
) -> Fraction:
    result = Fraction(0)
    for coefficient in coefficients:
        result = result * value + coefficient
    return result


def test_characteristic_polynomials_are_exact_source_derived_identities():
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        canonical_fraction_maps,
        fraction_characteristic_polynomial,
    )

    expected_maps = {
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
    exact = canonical_fraction_maps()

    assert dict(exact) == expected_maps
    adjacent_polynomial = fraction_characteristic_polynomial(exact["adjacent_pairs"])
    assert adjacent_polynomial == (
        Fraction(1),
        Fraction(-3),
        Fraction(18, 5),
        Fraction(-56, 25),
        Fraction(96, 125),
        Fraction(-432, 3125),
        Fraction(32, 3125),
    )
    assert fraction_characteristic_polynomial(exact["balanced_alternating"]) == (
        Fraction(1),
        Fraction(-9, 5),
        Fraction(27, 25),
        Fraction(-333, 1000),
        Fraction(73, 1250),
        Fraction(-141, 25000),
        Fraction(3, 12500),
    )

    adjacent_factorization = (Fraction(1), Fraction(-1))
    for _ in range(5):
        adjacent_factorization = _multiply_polynomials(
            adjacent_factorization,
            (Fraction(1), Fraction(-2, 5)),
        )
    assert adjacent_polynomial == adjacent_factorization

    derivative = adjacent_polynomial
    for order in range(5):
        assert _evaluate_polynomial(derivative, Fraction(2, 5)) == 0, order
        derivative = _differentiate_polynomial(derivative)
    assert _evaluate_polynomial(derivative, Fraction(2, 5)) == Fraction(-72)


@pytest.mark.parametrize(
    ("matrix", "expected_error"),
    (
        (True, TypeError),
        ([], TypeError),
        (([Fraction(1)],), TypeError),
        ((), ValueError),
        (((Fraction(1), Fraction(0)),), ValueError),
        (((Fraction(1),), (Fraction(0),)), ValueError),
        (((True,),), TypeError),
        (((1,),), TypeError),
        (((0.5,),), TypeError),
        (((float("inf"),),), ValueError),
        (((float("nan"),),), ValueError),
    ),
)
def test_characteristic_polynomial_rejects_noncanonical_matrices(
    matrix: object,
    expected_error: type[Exception],
):
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        fraction_characteristic_polynomial,
    )

    with pytest.raises(expected_error):
        fraction_characteristic_polynomial(matrix)  # type: ignore[arg-type]


def test_certificate_excludes_the_frozen_paired_support_boundary():
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        adjacent_support_certificate,
    )

    certificate = adjacent_support_certificate(
        basin_lower=Fraction(1, 4),
        basin_upper=Fraction(4),
        threshold=Fraction(-1, 50),
    )

    assert certificate["coefficient_of_variation_bound"] == Fraction(15, 8)
    assert certificate["tan_theta4_bound"] == Fraction(6, 125)
    assert certificate["ols_weights"] == tuple(
        Fraction(value, 10) for value in (-2, -1, 0, 1, 2)
    )
    assert certificate["slope_lower_bound"] == pytest.approx(
        -0.3 * math.atan(6 / 125),
        abs=1e-15,
    )
    assert certificate["rational_slope_lower_bound"] == Fraction(-9, 625)
    assert certificate["rational_margin_above_threshold"] == Fraction(7, 1250)
    assert certificate["slope_lower_bound"] > -0.02
    assert certificate["certificate_status"] == "certified_unreachable"
    assert certificate["paired_support_boundary_reachable"] is False
    assert certificate["matrix_dimension"] == 6
    assert certificate["endpoint_scales"] == (4, 5, 6, 7, 8)
    assert certificate["endpoint_angle"] == "raw_projective_angle"
    assert certificate["endpoint_estimator"] == "ordinary_least_squares_slope"
    assert certificate["paired_reduction"] == (
        "least_favorable_maximum_across_two_frozen_schemes"
    )
    assert certificate["support_comparison"] == (
        "upper_percentile_at_or_below_threshold"
    )
    assert certificate["required_application_premises"] == (
        "complete_uncensored_endpoints_for_adjacent_pairs_and_balanced_alternating",
        "initial_coefficients_admitted_in_basin",
        "frozen_maps_unchanged",
        "endpoint_scales_4_through_8_unchanged",
        "raw_angle_ols_unchanged",
        "paired_least_favorable_maximum_unchanged",
    )
    assert certificate["conclusion_is_conditional_on_required_premises"] is True
    assert certificate["actual_run_premises_validated"] is False
    assert certificate["frozen_input_scope_matches"] is True
    assert certificate["arithmetic_certificate_status"] == ("bound_excludes_threshold")
    assert certificate["application_conclusion"] == (
        "conditionally_paired_support_boundary_unreachable"
    )
    assert certificate["theorem_status"] == "ESTABLISHED"
    assert certificate["mathematical_verification_state"] == "CANDIDATE"
    assert certificate["verification_state"] == "CANDIDATE"
    assert certificate["claim_origin"] == "APPLICATION_SPECIFIC"
    assert certificate["attraction_claim"] == "not_established"
    assert certificate["universality_claim"] == "not_established"


def test_certificate_fails_closed_for_a_wider_basin():
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        adjacent_support_certificate,
    )

    certificate = adjacent_support_certificate(
        basin_lower=Fraction(1, 16),
        basin_upper=Fraction(16),
        threshold=Fraction(-1, 50),
    )

    assert certificate["coefficient_of_variation_bound"] == Fraction(255, 32)
    assert certificate["tan_theta4_bound"] == Fraction(51, 250)
    assert certificate["rational_slope_lower_bound"] == Fraction(-153, 2500)
    assert certificate["rational_margin_above_threshold"] == Fraction(-103, 2500)
    assert certificate["certificate_status"] == "not_certified"
    assert certificate["paired_support_boundary_reachable"] is None
    assert certificate["arithmetic_certificate_status"] == "not_certified"
    assert certificate["application_conclusion"] == "not_established"
    assert certificate["frozen_input_scope_matches"] is False
    assert certificate["theorem_status"] == "OPEN"
    assert certificate["mathematical_verification_state"] == "INCONCLUSIVE"
    assert certificate["verification_state"] == "CANDIDATE"


def test_certificate_fails_closed_when_the_exact_bound_is_not_rational():
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        adjacent_support_certificate,
    )

    certificate = adjacent_support_certificate(
        basin_lower=Fraction(1, 3),
        basin_upper=Fraction(2),
        threshold=Fraction(-1, 50),
    )

    assert certificate["coefficient_of_variation_bound"] is None
    assert certificate["tan_theta4_bound"] is None
    assert certificate["rational_slope_lower_bound"] is None
    assert certificate["rational_margin_above_threshold"] is None
    assert certificate["certificate_status"] == "not_certified"
    assert certificate["paired_support_boundary_reachable"] is None
    assert certificate["arithmetic_certificate_status"] == "not_certified"
    assert certificate["application_conclusion"] == "not_established"
    assert certificate["frozen_input_scope_matches"] is False
    assert certificate["theorem_status"] == "OPEN"
    assert certificate["mathematical_verification_state"] == "INCONCLUSIVE"
    assert certificate["not_certified_reason"] == (
        "Bhatia-Davis bound has no rational square root in this encoding"
    )


def test_generic_arithmetic_does_not_promote_a_synthetic_threshold():
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        adjacent_support_certificate,
    )

    certificate = adjacent_support_certificate(
        basin_lower=Fraction(1, 4),
        basin_upper=Fraction(4),
        threshold=Fraction(-1, 10),
    )

    assert certificate["arithmetic_certificate_status"] == ("bound_excludes_threshold")
    assert certificate["rational_margin_above_threshold"] == Fraction(107, 1250)
    assert certificate["certificate_status"] == "not_certified"
    assert certificate["paired_support_boundary_reachable"] is None
    assert certificate["application_conclusion"] == "not_established"
    assert certificate["frozen_input_scope_matches"] is False
    assert certificate["theorem_status"] == "OPEN"
    assert certificate["mathematical_verification_state"] == "INCONCLUSIVE"
    assert certificate["verification_state"] == "CANDIDATE"


def test_certificate_public_api_does_not_accept_run_evidence_flags():
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        adjacent_support_certificate,
    )

    with pytest.raises(TypeError, match="unexpected keyword argument"):
        adjacent_support_certificate(
            basin_lower=Fraction(1, 4),
            basin_upper=Fraction(4),
            threshold=Fraction(-1, 50),
            complete_endpoint_schemes=(
                "adjacent_pairs",
                "balanced_alternating",
            ),
        )


@pytest.mark.parametrize(
    "arguments",
    (
        {
            "basin_lower": True,
            "basin_upper": Fraction(4),
            "threshold": Fraction(-1, 50),
        },
        {
            "basin_lower": 0.25,
            "basin_upper": Fraction(4),
            "threshold": Fraction(-1, 50),
        },
        {
            "basin_lower": Fraction(1, 4),
            "basin_upper": 4,
            "threshold": Fraction(-1, 50),
        },
        {"basin_lower": Fraction(1, 4), "basin_upper": Fraction(4), "threshold": -0.02},
    ),
)
def test_certificate_rejects_noncanonical_exact_inputs(arguments: dict[str, object]):
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        adjacent_support_certificate,
    )

    with pytest.raises(TypeError, match="Fraction"):
        adjacent_support_certificate(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "arguments",
    (
        {
            "basin_lower": Fraction(0),
            "basin_upper": Fraction(4),
            "threshold": Fraction(-1, 50),
        },
        {
            "basin_lower": Fraction(4),
            "basin_upper": Fraction(1, 4),
            "threshold": Fraction(-1, 50),
        },
        {
            "basin_lower": Fraction(1, 4),
            "basin_upper": Fraction(4),
            "threshold": Fraction(0),
        },
    ),
)
def test_certificate_rejects_invalid_theorem_domain(arguments: dict[str, Fraction]):
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        adjacent_support_certificate,
    )

    with pytest.raises(ValueError):
        adjacent_support_certificate(**arguments)


def test_runtime_map_conformance_checks_float_encodings_without_snapping():
    from multiagent_elbo.realizations.gaussian import (
        runtime_map_conformance as exported_runtime_map_conformance,
    )
    from multiagent_elbo.realizations.gaussian.fixed_ray import (
        build_preregistered_system,
    )
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        canonical_fraction_maps,
        runtime_map_conformance,
    )

    system = build_preregistered_system()
    exact = canonical_fraction_maps()
    residuals = runtime_map_conformance(
        system.spatial_maps,
        exact,
        atol=1e-15,
    )

    assert exported_runtime_map_conformance is runtime_map_conformance
    assert dict(residuals) == {
        "adjacent_pairs": 0.0,
        "balanced_alternating": 5.551115123125783e-17,
    }
    assert all(
        type(value) is Fraction
        for matrix in exact.values()
        for row in matrix
        for value in row
    )

    mutated_runtime = {
        name: np.array(matrix, dtype=np.float64, copy=True)
        for name, matrix in system.spatial_maps.items()
    }
    mutated_runtime["adjacent_pairs"][0, 0] += 2e-12
    with pytest.raises(ValueError, match="exceeds atol"):
        runtime_map_conformance(mutated_runtime, exact, atol=1e-12)

    noncanonical_exact = dict(exact)
    rows = [list(row) for row in exact["adjacent_pairs"]]
    rows[0][0] = 0.5
    noncanonical_exact["adjacent_pairs"] = tuple(tuple(row) for row in rows)
    with pytest.raises(TypeError, match="Fraction"):
        runtime_map_conformance(
            system.spatial_maps,
            noncanonical_exact,
            atol=1e-15,
        )

    mutated_exact = dict(exact)
    rows = [list(row) for row in exact["adjacent_pairs"]]
    rows[0][0] += Fraction(1, 100)
    mutated_exact["adjacent_pairs"] = tuple(tuple(row) for row in rows)
    matching_mutated_runtime = {
        name: np.array(matrix, dtype=np.float64)
        for name, matrix in mutated_exact.items()
    }
    with pytest.raises(ValueError, match="canonical fixed-model literals"):
        runtime_map_conformance(
            matching_mutated_runtime,
            mutated_exact,
            atol=0.0,
        )


@pytest.mark.parametrize(
    ("mutation", "expected_error"),
    (
        ("missing_name", ValueError),
        ("nonsquare", ValueError),
        ("boolean", TypeError),
        ("integer", TypeError),
        ("nonfinite", ValueError),
        ("negative_atol", ValueError),
        ("nonfinite_atol", ValueError),
        ("boolean_atol", TypeError),
    ),
)
def test_runtime_map_conformance_rejects_malformed_inputs(
    mutation: str,
    expected_error: type[Exception],
):
    from multiagent_elbo.realizations.gaussian.fixed_ray import (
        build_preregistered_system,
    )
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        canonical_fraction_maps,
        runtime_map_conformance,
    )

    system = build_preregistered_system()
    runtime_maps = dict(system.spatial_maps)
    exact_maps = canonical_fraction_maps()
    atol: object = 1e-15
    if mutation == "missing_name":
        runtime_maps.pop("balanced_alternating")
    elif mutation == "nonsquare":
        runtime_maps["adjacent_pairs"] = np.ones((2, 3), dtype=np.float64)
    elif mutation == "boolean":
        runtime_maps["adjacent_pairs"] = np.ones((6, 6), dtype=np.bool_)
    elif mutation == "integer":
        runtime_maps["adjacent_pairs"] = np.ones((6, 6), dtype=np.int64)
    elif mutation == "nonfinite":
        invalid = np.array(runtime_maps["adjacent_pairs"], copy=True)
        invalid[0, 0] = np.inf
        runtime_maps["adjacent_pairs"] = invalid
    elif mutation == "negative_atol":
        atol = -1e-15
    elif mutation == "nonfinite_atol":
        atol = np.inf
    elif mutation == "boolean_atol":
        atol = True

    with pytest.raises(expected_error):
        runtime_map_conformance(
            runtime_maps,
            exact_maps,
            atol=atol,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "representative",
    (
        np.array([2.0, -1.0, 3.0]),
        np.array([2.0e120, -1.0e120, 3.0e120]),
        np.array([-2.0e-120, 1.0e-120, -3.0e-120]),
    ),
)
def test_normalized_map_accepts_every_finite_nonzero_representative(
    representative: np.ndarray,
):
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        normalized_projective_map,
    )

    matrix = np.eye(3, dtype=np.float64)
    expected = representative / np.linalg.norm(representative)

    np.testing.assert_allclose(
        normalized_projective_map(matrix, representative),
        expected,
        rtol=2e-15,
        atol=0.0,
    )


@pytest.mark.parametrize(
    ("matrix", "representative"),
    (
        (np.eye(3), np.zeros(3)),
        (np.eye(3), np.array([1.0, np.inf, 2.0])),
        (np.eye(3), np.array([1.0, np.nan, 2.0])),
        (np.diag([1.0, 0.0, 1.0]), np.array([0.0, 1.0, 0.0])),
        (np.array([[1.0, 0.0], [0.0, np.inf]]), np.ones(2)),
    ),
)
def test_normalized_map_and_jacobian_reject_invalid_projective_inputs(
    matrix: np.ndarray,
    representative: np.ndarray,
):
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        normalized_projective_jacobian,
        normalized_projective_map,
    )

    with pytest.raises(ValueError):
        normalized_projective_map(matrix, representative)
    with pytest.raises(ValueError):
        normalized_projective_jacobian(matrix, representative)


def test_analytic_normalized_map_derivative_converges_on_a_geodesic_ladder():
    from multiagent_elbo.realizations.gaussian.fixed_ray import (
        build_preregistered_system,
    )
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        normalized_projective_jacobian,
        normalized_projective_map,
        orthonormal_tangent_basis,
    )

    matrix = build_preregistered_system().spatial_maps["balanced_alternating"]
    representative = np.array([1.7, 0.4, 2.3, 1.1, 0.8, 1.9])
    unit = representative / np.linalg.norm(representative)
    basis = orthonormal_tangent_basis(unit)
    direction = basis @ np.array([1.0, -0.3, 0.7, -0.2, 0.5])
    direction /= np.linalg.norm(direction)
    jacobian = normalized_projective_jacobian(matrix, unit)
    analytic = jacobian @ direction

    central_residuals = []
    base_step = np.finfo(np.float64).eps ** (1.0 / 3.0)
    for step in base_step * np.array([4.0, 2.0, 1.0]):
        plus = math.cos(step) * unit + math.sin(step) * direction
        minus = math.cos(step) * unit - math.sin(step) * direction
        finite_difference = (
            normalized_projective_map(matrix, plus)
            - normalized_projective_map(matrix, minus)
        ) / (2.0 * step)
        derivative_scale = max(np.linalg.norm(analytic), np.finfo(np.float64).tiny)
        central_residuals.append(
            float(np.linalg.norm(finite_difference - analytic) / derivative_scale)
        )

    assert central_residuals[1] < central_residuals[0]
    assert central_residuals[2] < central_residuals[1]
    assert central_residuals[2] < 2e-10
    np.testing.assert_allclose(jacobian @ unit, 0.0, rtol=0.0, atol=2e-15)


def test_tangent_bases_and_reduced_step_match_the_restricted_jacobian():
    from multiagent_elbo.realizations.gaussian.fixed_ray import (
        build_preregistered_system,
    )
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        normalized_projective_jacobian,
        normalized_projective_map,
        orthonormal_tangent_basis,
        reduced_tangent_step,
    )

    matrix = build_preregistered_system().spatial_maps["balanced_alternating"]
    representative = np.array([1.7, 0.4, 2.3, 1.1, 0.8, 1.9])
    next_unit = normalized_projective_map(matrix, representative)
    first_unit = representative / np.linalg.norm(representative)
    first_basis = orthonormal_tangent_basis(representative)
    next_basis = orthonormal_tangent_basis(next_unit)

    assert first_basis.shape == (6, 5)
    np.testing.assert_allclose(
        first_basis.T @ first_basis, np.eye(5), rtol=0.0, atol=2e-15
    )
    np.testing.assert_allclose(
        next_basis.T @ next_basis, np.eye(5), rtol=0.0, atol=2e-15
    )
    np.testing.assert_allclose(first_basis.T @ first_unit, 0.0, atol=2e-15)
    np.testing.assert_allclose(next_basis.T @ next_unit, 0.0, atol=2e-15)

    expected = (
        next_basis.T
        @ normalized_projective_jacobian(matrix, representative)
        @ first_basis
    )
    np.testing.assert_allclose(
        reduced_tangent_step(matrix, representative, next_unit),
        expected,
        rtol=2e-15,
        atol=2e-15,
    )


@pytest.mark.parametrize(
    "representative",
    (
        np.zeros(3),
        np.array([1.0, np.inf, 2.0]),
        np.array([1.0, np.nan, 2.0]),
    ),
)
def test_tangent_basis_rejects_zero_or_nonfinite_representatives(
    representative: np.ndarray,
):
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        orthonormal_tangent_basis,
    )

    with pytest.raises(ValueError):
        orthonormal_tangent_basis(representative)


def _assert_eigenvalue_multiset(
    actual: object,
    expected: tuple[complex, ...],
    *,
    atol: float,
) -> None:
    remaining = list(np.asarray(actual, dtype=np.complex128))
    assert len(remaining) == len(expected)
    for wanted in expected:
        distances = [abs(value - wanted) for value in remaining]
        match = int(np.argmin(distances))
        assert distances[match] <= atol
        remaining.pop(match)


def test_adjacent_spectrum_is_the_fivefold_scalar_tangent_contraction():
    from multiagent_elbo.realizations.gaussian.fixed_ray import (
        build_preregistered_system,
    )
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        spectral_diagnostics,
    )

    system = build_preregistered_system()
    diagnostic = spectral_diagnostics(
        system.spatial_maps["adjacent_pairs"], system.perron_ray
    )

    _assert_eigenvalue_multiset(
        diagnostic["tangent_eigenvalues"],
        (complex(2 / 5),) * 5,
        atol=2e-15,
    )
    np.testing.assert_allclose(
        diagnostic["tangent_singular_values"],
        np.full(5, 2 / 5),
        rtol=0.0,
        atol=2e-15,
    )
    assert diagnostic["eigenvalue_multiplicities"] == (
        {"real": pytest.approx(2 / 5, abs=2e-15), "imag": 0.0, "multiplicity": 5},
    )
    assert diagnostic["spectral_radius"] == pytest.approx(2 / 5, abs=2e-15)
    np.testing.assert_allclose(
        diagnostic["absolute_gain"],
        np.array([(2 / 5) ** horizon for horizon in range(1, 9)]),
        rtol=2e-14,
        atol=0.0,
    )
    assert diagnostic["spectral_excess"] == (1.0,) * 8
    assert diagnostic["transient_amplification"] is False
    assert diagnostic["slow_cluster_dimension"] == 5
    assert diagnostic["seed_alignment"] == ("not_applicable_degenerate_spectrum")
    assert diagnostic["verification_state"] == "CANDIDATE"
    assert "mechanism_label" not in diagnostic


def test_alternating_spectrum_uses_a_three_dimensional_real_schur_projector():
    from multiagent_elbo.realizations.gaussian.fixed_ray import (
        build_preregistered_system,
    )
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        spectral_diagnostics,
    )

    system = build_preregistered_system()
    diagnostic = spectral_diagnostics(
        system.spatial_maps["balanced_alternating"], system.perron_ray
    )
    expected_eigenvalues = (
        complex(1 / 5),
        complex(3 / 20, math.sqrt(7) / 20),
        complex(3 / 20, -math.sqrt(7) / 20),
        complex(3 / 20, math.sqrt(3) / 20),
        complex(3 / 20, -math.sqrt(3) / 20),
    )
    _assert_eigenvalue_multiset(
        diagnostic["tangent_eigenvalues"], expected_eigenvalues, atol=2e-15
    )
    assert tuple(
        group["multiplicity"] for group in diagnostic["eigenvalue_multiplicities"]
    ) == (1, 1, 1, 1, 1)
    assert diagnostic["spectral_radius"] == pytest.approx(1 / 5, abs=2e-15)
    assert diagnostic["slow_cluster_dimension"] == 3

    tangent = np.asarray(diagnostic["tangent_operator"])
    schur_form = np.asarray(diagnostic["schur_form"])
    schur_basis = np.asarray(diagnostic["schur_basis"])
    scale = np.linalg.norm(tangent, ord="fro")
    residual = (
        np.linalg.norm(tangent @ schur_basis - schur_basis @ schur_form, ord="fro")
        / scale
    )
    assert residual == pytest.approx(diagnostic["schur_residual"], abs=1e-16)
    assert residual < 8e-15

    expected_projector = np.array(
        [
            [23 / 42, 5 / 42, -19 / 42, -1 / 6, -1 / 42, -1 / 42],
            [5 / 42, 23 / 42, 5 / 42, -1 / 6, -13 / 42, -13 / 42],
            [-19 / 42, 5 / 42, 23 / 42, -1 / 6, -1 / 42, -1 / 42],
            [-1 / 6, -1 / 6, -1 / 6, 5 / 6, -1 / 6, -1 / 6],
            [-1 / 42, -13 / 42, -1 / 42, -1 / 6, 11 / 42, 11 / 42],
            [-1 / 42, -13 / 42, -1 / 42, -1 / 6, 11 / 42, 11 / 42],
        ],
        dtype=np.float64,
    )
    projector = np.asarray(diagnostic["slow_projector"])
    np.testing.assert_allclose(projector, expected_projector, rtol=0.0, atol=3e-15)
    np.testing.assert_allclose(projector, projector.T, rtol=0.0, atol=2e-15)
    np.testing.assert_allclose(projector @ projector, projector, rtol=0.0, atol=3e-15)
    assert diagnostic["slow_projector_residual"] < 8e-15
    assert max(diagnostic["absolute_gain"]) < 1.0
    assert max(diagnostic["spectral_excess"]) > 2.0
    assert diagnostic["transient_amplification"] is False
    assert diagnostic["seed_alignment"] == "continuous_slow_projector_energy"
    assert "mechanism_label" not in diagnostic


def test_spectral_diagnostic_rejects_a_nonperron_ray_despite_an_unrelated_scale():
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        spectral_diagnostics,
    )

    matrix = np.array([[1.0, 0.0], [1.0, 1.0e16]], dtype=np.float64)
    with pytest.raises(ValueError, match="Perron ray"):
        spectral_diagnostics(matrix, np.array([1.0, 0.0]))


def test_near_scalar_runtime_perturbation_is_not_canonicalized_away():
    from multiagent_elbo.realizations.gaussian.fixed_ray import (
        build_preregistered_system,
    )
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        spectral_diagnostics,
    )

    system = build_preregistered_system()
    perturbed = np.array(system.spatial_maps["adjacent_pairs"], copy=True)
    perturbed[0, 0] += 2e-14
    perturbed[0, 1] -= 2e-14
    diagnostic = spectral_diagnostics(perturbed, system.perron_ray)
    tangent = np.asarray(diagnostic["tangent_operator"])
    direct_singular_values = np.linalg.svd(tangent, compute_uv=False)
    direct_radius = float(np.max(np.abs(np.linalg.eigvals(tangent))))
    direct_excess = tuple(
        float(
            np.linalg.norm(np.linalg.matrix_power(tangent, horizon), 2)
            / direct_radius**horizon
        )
        for horizon in range(1, 9)
    )

    assert np.array_equal(diagnostic["tangent_singular_values"], direct_singular_values)
    assert diagnostic["spectral_excess"] == direct_excess
    assert diagnostic["spectral_excess"] != (1.0,) * 8


def test_trajectory_diagnostic_reconstructs_the_frozen_same_path_endpoint():
    from multiagent_elbo.realizations.gaussian.confirmatory_analysis import (
        _ols_slope,
    )
    from multiagent_elbo.realizations.gaussian.fixed_ray import (
        build_preregistered_system,
        generate_initial_coefficients,
        iterate_fixed_ray,
    )
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        diagnose_trajectory,
    )

    system = build_preregistered_system()
    initial = generate_initial_coefficients(202608090101, "C001")
    trajectory = iterate_fixed_ray(
        system,
        initial,
        scheme="balanced_alternating",
        steps=8,
    )
    diagnostic = diagnose_trajectory(
        system.spatial_maps["balanced_alternating"],
        trajectory.coefficients,
        system.perron_ray,
        tuple(range(9)),
    )

    expected_angles = tuple(
        float(value) for value in trajectory.projective_ray_angles[4:9]
    )
    assert diagnostic["endpoint_scales"] == (4, 5, 6, 7, 8)
    assert diagnostic["raw_angles"] == expected_angles
    assert diagnostic["raw_angle_ols_slope"] == _ols_slope(
        trajectory.projective_ray_angles[4:9]
    )
    assert diagnostic["raw_angle_ols_slope"] == pytest.approx(
        np.polyfit(np.arange(4.0, 9.0), expected_angles, 1)[0], abs=2e-15
    )
    np.testing.assert_allclose(
        diagnostic["log_angles"], np.log(expected_angles), rtol=0.0, atol=2e-15
    )
    expected_ratios = tuple(
        float(
            trajectory.projective_ray_angles[scale]
            / trajectory.projective_ray_angles[scale - 1]
        )
        for scale in range(4, 9)
    )
    assert diagnostic["one_step_angle_ratios"] == expected_ratios
    assert diagnostic["recurrence_bit_identical"] is True
    assert diagnostic["max_recurrence_residual"] == 0.0
    assert diagnostic["recurrence_tolerance"] == (
        8.0
        * np.finfo(np.float64).eps
        * max(1.0, float(np.max(np.abs(trajectory.coefficients))))
    )

    propagators = np.asarray(diagnostic["reduced_propagators"])
    assert propagators.shape == (5, 5, 5)
    np.testing.assert_allclose(
        diagnostic["reduced_propagator_norms"],
        [np.linalg.norm(propagator, 2) for propagator in propagators],
        rtol=2e-15,
        atol=0.0,
    )
    np.testing.assert_allclose(
        diagnostic["reduced_propagator_condition_numbers"],
        [np.linalg.cond(propagator) for propagator in propagators],
        rtol=2e-15,
        atol=0.0,
    )
    assert np.all(np.isfinite(diagnostic["reduced_propagator_condition_numbers"]))
    assert "ambient_jacobian_condition_number" not in diagnostic
    assert "mechanism_label" not in diagnostic
    assert diagnostic["theorem_status"] == "NUMERICAL"
    assert diagnostic["verification_state"] == "CANDIDATE"


def test_c001_alternating_seed_values_are_invariant_under_tangent_rotation():
    from scipy import linalg as scipy_linalg

    from multiagent_elbo.realizations.gaussian.fixed_ray import (
        build_preregistered_system,
        generate_initial_coefficients,
        iterate_fixed_ray,
    )
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        diagnose_trajectory,
        orthonormal_tangent_basis,
    )

    system = build_preregistered_system()
    matrix = system.spatial_maps["balanced_alternating"]
    initial = generate_initial_coefficients(202608090101, "C001")
    coefficients = iterate_fixed_ray(
        system, initial, scheme="balanced_alternating", steps=8
    ).coefficients
    diagnostic = diagnose_trajectory(
        matrix, coefficients, system.perron_ray, tuple(range(9))
    )

    assert diagnostic["slow_energy"] == pytest.approx(0.24294168484640577, abs=1e-12)
    assert diagnostic["actual_direction_gains"][0] == pytest.approx(
        0.19447462201557028, abs=1e-12
    )
    assert diagnostic["actual_direction_gains"][7] == pytest.approx(
        3.422752480391632e-06, abs=1e-12
    )

    perron_unit = system.perron_ray / np.linalg.norm(system.perron_ray)
    projector = np.eye(6) - np.outer(perron_unit, perron_unit)
    base_basis = orthonormal_tangent_basis(perron_unit)
    generator = np.random.default_rng(314159)
    rotation, _ = np.linalg.qr(generator.normal(size=(5, 5)))
    rotated_basis = base_basis @ rotation
    rotated_tangent = rotated_basis.T @ projector @ matrix @ rotated_basis
    eigenvalues = np.linalg.eigvals(rotated_tangent)
    radius = float(np.max(np.abs(eigenvalues)))
    tolerance = 512.0 * np.finfo(np.float64).eps
    _, schur_basis, slow_dimension = scipy_linalg.schur(
        rotated_tangent,
        output="real",
        sort=lambda real, imag: abs(abs(complex(real, imag)) - radius) <= tolerance,
    )
    assert slow_dimension == 3
    slow_basis = schur_basis[:, :slow_dimension]
    rotated_slow_projector = rotated_basis @ slow_basis @ slow_basis.T @ rotated_basis.T
    delta = projector @ (initial / np.linalg.norm(initial))
    rotated_energy = float(
        np.linalg.norm(rotated_slow_projector @ delta) ** 2 / np.linalg.norm(delta) ** 2
    )
    rotated_coordinates = rotated_basis.T @ delta
    rotated_gains = tuple(
        float(
            np.linalg.norm(
                np.linalg.matrix_power(rotated_tangent, horizon) @ rotated_coordinates
            )
            / np.linalg.norm(rotated_coordinates)
        )
        for horizon in range(1, 9)
    )

    assert rotated_energy == pytest.approx(diagnostic["slow_energy"], abs=2e-14)
    np.testing.assert_allclose(
        rotated_gains,
        diagnostic["actual_direction_gains"],
        rtol=0.0,
        atol=2e-14,
    )


def test_zero_transverse_trajectory_is_not_applicable_and_recurrence_fails_closed():
    from multiagent_elbo.realizations.gaussian.fixed_ray import (
        build_preregistered_system,
        generate_initial_coefficients,
        iterate_fixed_ray,
    )
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        diagnose_trajectory,
    )

    system = build_preregistered_system()
    matrix = system.spatial_maps["balanced_alternating"]
    perron_coefficients = np.repeat(system.perron_ray[None, :], 9, axis=0)
    diagnostic = diagnose_trajectory(
        matrix, perron_coefficients, system.perron_ray, tuple(range(9))
    )
    assert diagnostic["slow_energy"] is None
    assert diagnostic["actual_direction_gains"] == (None,) * 8
    assert diagnostic["seed_alignment"] == ("not_applicable_zero_transverse_deviation")
    assert diagnostic["log_angles"] == (None,) * 5
    assert diagnostic["one_step_angle_ratios"] == (None,) * 5

    initial = generate_initial_coefficients(202608090101, "C001")
    corrupted = np.array(
        iterate_fixed_ray(
            system, initial, scheme="balanced_alternating", steps=8
        ).coefficients,
        copy=True,
    )
    corrupted[6, 2] += 1e-9
    with pytest.raises(ValueError, match="recurrence"):
        diagnose_trajectory(matrix, corrupted, system.perron_ray, tuple(range(9)))


def _synthetic_population_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for population, count, seed_prefix in (
        ("C", 30, 202608090100),
        ("H", 10, 202608090200),
    ):
        for index in range(1, count + 1):
            job_id = f"{population}{index:03d}"
            adjacent = -0.001 * index
            alternating = adjacent + (0.0001 if index % 2 == 0 else -0.0001)
            for scheme, slope in (
                ("adjacent_pairs", adjacent),
                ("balanced_alternating", alternating),
            ):
                records.append(
                    {
                        "job_id": job_id,
                        "master_seed": seed_prefix + index,
                        "scheme": scheme,
                        "raw_angle_ols_slope": slope,
                        "verification_state": "CANDIDATE",
                    }
                )
    return records


def test_population_summaries_use_exact_jobs_and_per_job_least_favorable_map():
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        summarize_population,
    )

    records = _synthetic_population_records()
    confirmatory = summarize_population(records, population="C")
    holdout = summarize_population(records, population="H")

    assert confirmatory["population"] == "C"
    assert confirmatory["scope"] == "confirmatory_primary"
    assert confirmatory["job_count"] == 30
    assert confirmatory["job_ids"] == tuple(f"C{index:03d}" for index in range(1, 31))
    expected_confirmatory = tuple(
        max(
            -0.001 * index,
            -0.001 * index + (0.0001 if index % 2 == 0 else -0.0001),
        )
        for index in range(1, 31)
    )
    assert confirmatory["paired_least_favorable_raw_angle_ols_slopes"] == (
        expected_confirmatory
    )
    assert confirmatory["estimate"] == float(np.median(expected_confirmatory))
    assert confirmatory["paired_reduction"] == (
        "least_favorable_maximum_across_two_frozen_schemes"
    )
    assert confirmatory["verification_state"] == "CANDIDATE"

    assert holdout["population"] == "H"
    assert holdout["scope"] == "descriptive_replication_only"
    assert holdout["job_count"] == 10
    assert holdout["job_ids"] == tuple(f"H{index:03d}" for index in range(1, 11))
    assert holdout["verification_state"] == "CANDIDATE"
    assert "mechanism_label" not in confirmatory
    assert "mechanism_label" not in holdout


def test_h_mutation_cannot_change_c_summary_bytes_and_pooling_is_rejected():
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        summarize_population,
    )

    records = _synthetic_population_records()
    before = json.dumps(
        summarize_population(records, population="C"),
        default=dict,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    mutated = [dict(record) for record in records]
    holdout_record = next(record for record in mutated if record["job_id"] == "H004")
    holdout_record["raw_angle_ols_slope"] = 999.0
    holdout_record["master_seed"] = -1
    holdout_record["verification_state"] = "REFUTED"
    after = json.dumps(
        summarize_population(mutated, population="C"),
        default=dict,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    assert after == before
    with pytest.raises(ValueError, match="pool"):
        summarize_population(records, population="C+H")


def test_population_summary_rejects_missing_or_duplicate_selected_records():
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        summarize_population,
    )

    records = _synthetic_population_records()
    missing = [
        record
        for record in records
        if not (
            record["job_id"] == "C030" and record["scheme"] == "balanced_alternating"
        )
    ]
    with pytest.raises(ValueError, match="exactly two schemes"):
        summarize_population(missing, population="C")

    duplicate = records + [dict(records[0])]
    with pytest.raises(ValueError, match="duplicate"):
        summarize_population(duplicate, population="C")

    missing_seed = [dict(record) for record in records]
    missing_seed[0].pop("master_seed")
    with pytest.raises(ValueError, match="master seed"):
        summarize_population(missing_seed, population="C")
