"""Tests for the cocycle flow, its declared measurements, and the reduced map."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

import numpy as np
import pytest

from multiagent_elbo.finite.cocycle_flow import (
    cocycle_flow,
    composition_defect,
    consecutive_blocks,
    homogeneity_defect,
    homogeneous_cycle_instance,
    ray_comparison,
    reduced_couplings,
)
from multiagent_elbo.finite.cocycle_flow import _reduced_step_map
from multiagent_elbo.finite.coupling_readback import couplings_action

SITE = tuple(Fraction(index, 10) for index in range(9))
PAIR = tuple(
    tuple(Fraction(0) if 0 in (left, right) else Fraction(left * 3 + right, 100) for right in range(9))
    for left in range(9)
)


def test_the_homogeneous_builder_reproduces_the_declared_action() -> None:
    instance = homogeneous_cycle_instance(3, SITE, PAIR)
    action = couplings_action(instance.couplings)
    for state in [(0, 0, 0), (2, 5, 1), (8, 8, 8), (1, 0, 7)]:
        expected = sum(float(SITE[value]) for value in state)
        for position in range(3):
            left = state[position]
            right = state[(position + 1) % 3]
            expected += float(PAIR[left][right])
        assert abs(float(action[state]) - expected) <= 1.0e-12


def test_the_wrap_edge_carries_the_transposed_table() -> None:
    asymmetric = tuple(
        tuple(Fraction(0) if 0 in (left, right) else Fraction(left, 7) for right in range(9))
        for left in range(9)
    )
    instance = homogeneous_cycle_instance(3, SITE, asymmetric)
    stored = dict(instance.couplings.pairs)
    assert stored[(0, 2)][1][2] == asymmetric[2][1]


def test_consecutive_blocks_and_their_validation() -> None:
    assert consecutive_blocks(6, 3) == ((1, 2, 3), (4, 5, 6))
    with pytest.raises(ValueError):
        consecutive_blocks(6, 4)
    with pytest.raises(ValueError):
        consecutive_blocks(6, 1)
    with pytest.raises(ValueError):
        homogeneous_cycle_instance(2, SITE, PAIR)


def test_one_step_preserves_homogeneity_and_the_cycle_holonomy() -> None:
    instance = homogeneous_cycle_instance(4, SITE, PAIR, belief_element=1)
    steps = cocycle_flow(instance, (2,))
    step = steps[0]
    assert homogeneity_defect(step.variational) <= 1.0e-9
    belief_total = sum(step.connection.graph.belief_elements) % 3
    assert belief_total == (4 * 1) % 3


def test_the_ray_comparison_recovers_a_planted_scale_exactly() -> None:
    fine = homogeneous_cycle_instance(4, SITE, PAIR).couplings
    scaled_site = tuple(value * Fraction(1, 2) for value in SITE)
    scaled_pair = tuple(tuple(value * Fraction(1, 2) for value in row) for row in PAIR)
    coarse = homogeneous_cycle_instance(4, scaled_site, scaled_pair).couplings
    report = ray_comparison(fine, coarse)
    assert abs(report.scale - 0.5) <= 1.0e-12
    assert report.relative_residual <= 1.0e-12


def test_the_reduced_vector_refuses_the_merged_two_cycle_type() -> None:
    instance = homogeneous_cycle_instance(4, SITE, PAIR)
    steps = cocycle_flow(instance, (2,))
    with pytest.raises(ValueError):
        reduced_couplings(steps[0].variational)


def test_the_composition_defect_is_deterministic_and_type_checked() -> None:
    instance = homogeneous_cycle_instance(4, SITE, PAIR)
    first = composition_defect(instance, (2, 2), (4,))
    second = composition_defect(instance, (2, 2), (4,))
    assert first.defect == second.defect
    assert first.defect >= 0.0
    with pytest.raises(ValueError):
        composition_defect(instance, (2,), (4,))


def test_the_reduced_step_map_returns_a_finite_reduced_vector() -> None:
    instance = homogeneous_cycle_instance(6, SITE, PAIR)
    base = reduced_couplings(instance.couplings)
    image = _reduced_step_map(instance, 2, base)
    assert image.shape == base.shape
    assert np.all(np.isfinite(image))


def test_the_fixed_point_iteration_is_deterministic_and_reports_honestly() -> None:
    from multiagent_elbo.finite.cocycle_flow import reduced_fixed_point

    instance = homogeneous_cycle_instance(6, SITE, PAIR)
    first = reduced_fixed_point(instance, 2, max_iterations=3)
    second = reduced_fixed_point(instance, 2, max_iterations=3)
    assert first.iterations == 3
    assert not first.converged
    assert first.final_change == second.final_change
    assert np.array_equal(first.vector, second.vector)
