from __future__ import annotations

import math

import numpy as np
import pytest

from multiagent_elbo.realizations.gaussian.fixed_ray import (
    FixedRaySystem,
    blocking_scheme_dispersion,
    build_preregistered_system,
    generate_initial_coefficients,
    iterate_fixed_ray,
    job_seed,
    projective_ray_angle,
    scalarized_ray_construction_residual,
)


def test_preregistered_system_pins_scalarized_cone_perron_factorization_and_noncommuting_control():
    system = build_preregistered_system()

    assert system.matrix_direction == pytest.approx(
        np.array([[2.0, 0.5], [0.5, 1.0]])
    )
    assert np.linalg.eigvalsh(system.matrix_direction) == pytest.approx(
        np.array([(3.0 - math.sqrt(2.0)) / 2.0, (3.0 + math.sqrt(2.0)) / 2.0])
    )
    assert system.perron_ray == pytest.approx(np.ones(6))
    assert system.node_factor == pytest.approx(np.ones(4))
    assert system.factorized_perron_ray() == pytest.approx(np.ones(6))
    assert system.primitive_powers == {
        "adjacent_pairs": 1,
        "balanced_alternating": 1,
    }
    assert system.noncommuting_gap == pytest.approx(1.0 / 100.0)


def test_adjacent_map_matches_independent_literal_and_uniform_ray_is_fixed():
    system = build_preregistered_system()
    initial = np.arange(1.0, 7.0)
    trajectory = iterate_fixed_ray(
        system, initial, scheme="adjacent_pairs", steps=1
    )

    np.testing.assert_allclose(
        trajectory.coefficients[1], np.array([2.5, 2.9, 3.3, 3.7, 4.1, 4.5])
    )
    fixed = iterate_fixed_ray(
        system, np.ones(6), scheme="adjacent_pairs", steps=3
    )
    np.testing.assert_array_equal(fixed.coefficients, np.ones((4, 6)))
    np.testing.assert_array_equal(fixed.projective_ray_angles, np.zeros(4))
    np.testing.assert_array_equal(fixed.normalized_coupling_distances, np.zeros(4))


def test_retained_beta_is_signed_comparison_typed_finite_difference():
    """Catches replacing (I-P)(c_next-c_now) by the unsigned next state."""
    system = build_preregistered_system()
    trajectory = iterate_fixed_ray(
        system, np.arange(1.0, 7.0), scheme="adjacent_pairs", steps=1
    )
    expected = np.array([1.5, 0.9, 0.3, -0.3, -0.9, -1.5]) / math.log(2.0)

    np.testing.assert_allclose(
        trajectory.retained_beta_residual_vectors[0],
        expected,
        rtol=1e-15,
        atol=1e-15,
    )
    assert trajectory.retained_beta_residuals[0] == pytest.approx(
        np.linalg.norm(expected)
    )
    assert trajectory.retained_beta_residual_vectors[0, 0] > 0.0
    assert trajectory.retained_beta_residual_vectors[0, -1] < 0.0

    fixed = iterate_fixed_ray(
        system, np.ones(6), scheme="adjacent_pairs", steps=1
    )
    np.testing.assert_array_equal(
        fixed.retained_beta_residual_vectors, np.zeros((1, 6))
    )


def test_job_substreams_are_immutable_schedule_independent_and_in_basin():
    first_seed = job_seed(202608090001, "P001")
    second_seed = job_seed(202608090001, "P002")
    first = generate_initial_coefficients(202608090001, "P001")
    repeat = generate_initial_coefficients(202608090001, "P001")
    second = generate_initial_coefficients(202608090001, "P002")

    assert first_seed == 2385454150537286366
    assert first_seed != second_seed
    np.testing.assert_array_equal(first, repeat)
    assert not np.array_equal(first, second)
    assert np.min(first) >= 0.25
    assert np.max(first) <= 4.0
    assert np.max(first) / np.min(first) <= 16.0


def test_finite_trajectory_records_all_preregistered_diagnostics_without_basin_exit():
    system = build_preregistered_system()
    initial = generate_initial_coefficients(202608090001, "P001")
    result = iterate_fixed_ray(
        system, initial, scheme="balanced_alternating", steps=8
    )

    assert result.coefficients.shape == (9, 6)
    assert result.coupling_matrices.shape == (9, 6, 2, 2)
    assert result.projective_ray_angles.shape == (9,)
    assert result.normalized_coupling_distances.shape == (9,)
    assert result.scalarized_ray_construction_residuals.shape == (9,)
    assert result.retained_beta_residual_vectors.shape == (8, 6)
    assert result.retained_beta_residuals.shape == (8,)
    assert result.basin_exits.shape == (9,)
    assert result.coefficient_conditioning.shape == (9,)
    assert result.projective_ray_angles[-1] < result.projective_ray_angles[0]
    assert result.normalized_coupling_distances[-1] < result.normalized_coupling_distances[0]
    assert np.max(result.scalarized_ray_construction_residuals) < 1e-15
    assert not np.any(result.basin_exits)
    assert np.all(np.isfinite(result.retained_beta_residuals))


def test_scalarized_ray_construction_residual_detects_matrix_mutation_without_selecting_m():
    system = build_preregistered_system()
    coefficients = np.arange(1.0, 7.0)
    first_family = coefficients[:, None, None] * system.matrix_direction
    alternate_direction = np.array([[3.0, 0.25], [0.25, 2.0]])
    alternate_family = coefficients[:, None, None] * alternate_direction
    mutated = first_family.copy()
    mutated[0, 0, 1] += 0.125

    assert scalarized_ray_construction_residual(first_family, system.matrix_direction) < 1e-15
    assert scalarized_ray_construction_residual(alternate_family, alternate_direction) < 1e-15
    assert scalarized_ray_construction_residual(mutated, system.matrix_direction) > 1e-3
    assert projective_ray_angle(coefficients, system.perron_ray) == pytest.approx(
        projective_ray_angle(coefficients, np.ones(6))
    )


def test_projective_ray_angle_is_stable_for_nearly_parallel_positive_rays():
    target = np.ones(6, dtype=np.float64)
    target /= np.linalg.norm(target)
    tangent = np.array([1.0, -1.0, 0.0, 0.0, 0.0, 0.0])
    tangent /= np.linalg.norm(tangent)
    expected_angle = 1.0e-6
    nearby = (
        math.cos(expected_angle) * target
        + math.sin(expected_angle) * tangent
    )

    assert np.all(nearby > 0.0)
    assert projective_ray_angle(nearby, target) == pytest.approx(
        expected_angle, rel=1.0e-10, abs=1.0e-15
    )


def test_paired_scheme_dispersion_is_zero_at_start_and_detectable_after_noncommuting_steps():
    system = build_preregistered_system()
    initial = np.arange(1.0, 7.0)
    adjacent = iterate_fixed_ray(system, initial, scheme="adjacent_pairs", steps=3)
    alternating = iterate_fixed_ray(
        system, initial, scheme="balanced_alternating", steps=3
    )
    dispersion = blocking_scheme_dispersion(
        adjacent.coefficients, alternating.coefficients
    )

    assert dispersion[0] == pytest.approx(0.0)
    assert np.max(dispersion[1:]) > 1e-3


def test_system_rejects_missing_primitivity_or_perron_factorization():
    system = build_preregistered_system()
    nonprimitive = np.eye(6)

    with pytest.raises(ValueError, match="primitive"):
        FixedRaySystem(
            matrix_direction=system.matrix_direction,
            spatial_maps={"adjacent_pairs": nonprimitive},
            perron_ray=np.ones(6),
            node_factor=np.ones(4),
            edge_labels=system.edge_labels,
            basin_lower=0.25,
            basin_upper=4.0,
            log_block_scale=math.log(2.0),
        )
    with pytest.raises(ValueError, match="factorize"):
        FixedRaySystem(
            matrix_direction=system.matrix_direction,
            spatial_maps={"adjacent_pairs": system.spatial_maps["adjacent_pairs"]},
            perron_ray=np.ones(6),
            node_factor=np.array([1.0, 1.0, 1.0, 2.0]),
            edge_labels=system.edge_labels,
            basin_lower=0.25,
            basin_upper=4.0,
            log_block_scale=math.log(2.0),
        )
