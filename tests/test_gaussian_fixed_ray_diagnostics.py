from fractions import Fraction
import math

import numpy as np
import pytest


def _complete_application_premises() -> dict[str, object]:
    return {
        "complete_endpoint_schemes": (
            "adjacent_pairs",
            "balanced_alternating",
        ),
        "censored_endpoint_schemes": (),
        "initial_coefficients_admitted_in_basin": True,
        "frozen_maps_unchanged": True,
        "endpoint_scales_4_through_8_unchanged": True,
        "raw_angle_ols_unchanged": True,
        "paired_least_favorable_max_unchanged": True,
    }


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
        **_complete_application_premises(),
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
    assert certificate["required_complete_endpoint_schemes"] == (
        "adjacent_pairs",
        "balanced_alternating",
    )
    assert certificate["complete_endpoint_schemes"] == (
        "adjacent_pairs",
        "balanced_alternating",
    )
    assert certificate["censored_endpoint_schemes"] == ()
    assert certificate["complete_endpoints_for_both_frozen_schemes"] is True
    assert certificate["initial_coefficients_admitted_in_basin"] is True
    assert certificate["frozen_maps_unchanged"] is True
    assert certificate["endpoint_scales_4_through_8_unchanged"] is True
    assert certificate["raw_angle_ols_unchanged"] is True
    assert certificate["paired_least_favorable_max_unchanged"] is True
    assert certificate["application_premises_satisfied"] is True
    assert certificate["frozen_input_scope_matches"] is True
    assert certificate["application_scope_matches"] is True
    assert certificate["arithmetic_certificate_status"] == (
        "bound_excludes_threshold"
    )
    assert certificate["application_conclusion"] == (
        "paired_support_boundary_unreachable"
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
        **_complete_application_premises(),
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
    assert certificate["application_scope_matches"] is False
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
        **_complete_application_premises(),
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
    assert certificate["application_scope_matches"] is False
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
        **_complete_application_premises(),
    )

    assert certificate["arithmetic_certificate_status"] == (
        "bound_excludes_threshold"
    )
    assert certificate["rational_margin_above_threshold"] == Fraction(107, 1250)
    assert certificate["certificate_status"] == "not_certified"
    assert certificate["paired_support_boundary_reachable"] is None
    assert certificate["application_conclusion"] == "not_established"
    assert certificate["frozen_input_scope_matches"] is False
    assert certificate["application_scope_matches"] is False
    assert certificate["theorem_status"] == "OPEN"
    assert certificate["mathematical_verification_state"] == "INCONCLUSIVE"
    assert certificate["verification_state"] == "CANDIDATE"


@pytest.mark.parametrize(
    "premise_overrides",
    (
        pytest.param({"complete_endpoint_schemes": ()}, id="missing"),
        pytest.param(
            {"complete_endpoint_schemes": ("adjacent_pairs",)},
            id="incomplete",
        ),
        pytest.param(
            {
                "complete_endpoint_schemes": ("adjacent_pairs",),
                "censored_endpoint_schemes": ("balanced_alternating",),
            },
            id="censored",
        ),
        pytest.param(
            {"initial_coefficients_admitted_in_basin": False},
            id="out_of_basin",
        ),
        pytest.param(
            {"frozen_maps_unchanged": False},
            id="changed_maps",
        ),
        pytest.param(
            {"endpoint_scales_4_through_8_unchanged": False},
            id="changed_scales",
        ),
        pytest.param(
            {"raw_angle_ols_unchanged": False},
            id="changed_estimator",
        ),
        pytest.param(
            {"paired_least_favorable_max_unchanged": False},
            id="changed_reduction",
        ),
    ),
)
def test_incomplete_application_premises_never_inherit_the_theorem_conclusion(
    premise_overrides: dict[str, object],
):
    from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostics import (
        adjacent_support_certificate,
    )

    premises = _complete_application_premises()
    premises.update(premise_overrides)
    certificate = adjacent_support_certificate(
        basin_lower=Fraction(1, 4),
        basin_upper=Fraction(4),
        threshold=Fraction(-1, 50),
        **premises,
    )

    assert certificate["arithmetic_certificate_status"] == (
        "bound_excludes_threshold"
    )
    assert certificate["application_premises_satisfied"] is False
    assert certificate["application_scope_matches"] is False
    assert certificate["certificate_status"] == "not_certified"
    assert certificate["paired_support_boundary_reachable"] is None
    assert certificate["application_conclusion"] == "not_established"
    assert certificate["theorem_status"] == "OPEN"
    assert certificate["mathematical_verification_state"] == "INCONCLUSIVE"
    assert certificate["verification_state"] == "CANDIDATE"


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
