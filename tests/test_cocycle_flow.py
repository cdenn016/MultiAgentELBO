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


def test_the_circulant_builder_reproduces_the_declared_action() -> None:
    from multiagent_elbo.finite.cocycle_flow import homogeneous_circulant_instance

    instance = homogeneous_circulant_instance(6, (1, 2), SITE, PAIR)
    assert len(instance.graph.edges) == 12
    assert sum(instance.graph.belief_elements) == 6
    action = couplings_action(instance.couplings)
    state = (2, 5, 1, 0, 7, 3)
    expected = sum(float(SITE[value]) for value in state)
    for offset in (1, 2):
        for position in range(6):
            expected += float(PAIR[state[position]][state[(position + offset) % 6]])
    assert abs(float(action[state]) - expected) <= 1.0e-12
    with pytest.raises(ValueError):
        homogeneous_circulant_instance(6, (1, 3), SITE, PAIR)


def test_the_pair_retention_measurement_is_deterministic_and_typed() -> None:
    from multiagent_elbo.finite.cocycle_flow import (
        homogeneous_circulant_instance,
        one_step_pair_retention,
    )

    instance = homogeneous_circulant_instance(4, (1,), SITE, PAIR)
    first = one_step_pair_retention(instance, 2)
    second = one_step_pair_retention(instance, 2)
    assert first == second
    assert first.cut_per_boundary == 1
    assert first.fine_pair_sup > 0.0
    assert first.retention >= 0.0


def test_the_fixed_point_iteration_is_deterministic_and_reports_honestly() -> None:
    from multiagent_elbo.finite.cocycle_flow import reduced_fixed_point

    instance = homogeneous_cycle_instance(6, SITE, PAIR)
    first = reduced_fixed_point(instance, 2, max_iterations=3)
    second = reduced_fixed_point(instance, 2, max_iterations=3)
    assert first.iterations == 3
    assert not first.converged
    assert first.final_change == second.final_change
    assert np.array_equal(first.vector, second.vector)


def test_regeneration_injects_a_pair_source_with_normalized_rows() -> None:
    from multiagent_elbo.finite.cocycle_flow import regenerated_instance
    from multiagent_elbo.finite.coupling_readback import iterated_step

    instance = homogeneous_cycle_instance(6, SITE, PAIR)
    step = iterated_step(instance, consecutive_blocks(6, 2))
    regenerated = regenerated_instance(step)
    assert regenerated.injected_pair_sup > 0.0
    for _, rows in regenerated.rows:
        for row in rows:
            assert abs(sum(row) - 1.0) <= 1.0e-12
            assert all(value >= 0.0 for value in row)
    coarse_pair_sup = max(
        abs(float(value))
        for _, table in regenerated.instance.couplings.pairs
        for row in table
        for value in row
    )
    assert coarse_pair_sup > 0.0
    again = regenerated_instance(step)
    assert again.injected_pair_sup == regenerated.injected_pair_sup


def test_the_constant_sector_control_reproduces_the_plain_retention() -> None:
    from multiagent_elbo.finite.cocycle_flow import (
        capacity_pair_retention,
        one_step_pair_retention,
    )

    from multiagent_elbo.finite.cocycle_flow import homogeneous_circulant_instance

    instance = homogeneous_circulant_instance(4, (1,), SITE, PAIR)
    plain = one_step_pair_retention(instance, 2)
    control = capacity_pair_retention(instance, 2, constant_sector=True)
    assert abs(control.retention - plain.retention) <= 1.0e-12
    assert control.sector_count == 1
    capacity = capacity_pair_retention(instance, 2)
    assert capacity.sector_count == 3
    assert capacity.retention >= 0.0
    again = capacity_pair_retention(instance, 2)
    assert again == capacity


def test_the_regenerated_composition_defect_is_deterministic_and_typed() -> None:
    from multiagent_elbo.finite.cocycle_flow import regenerated_composition_defect

    instance = homogeneous_cycle_instance(4, SITE, PAIR)
    first = regenerated_composition_defect(instance, (2, 2), (4,))
    second = regenerated_composition_defect(instance, (2, 2), (4,))
    assert first.defect == second.defect
    assert first.defect >= 0.0
    with pytest.raises(ValueError):
        regenerated_composition_defect(instance, (2,), (4,))


def test_the_regenerated_coarse_action_is_gauge_covariant() -> None:
    from multiagent_elbo.finite.cocycle_flow import regenerated_instance
    from multiagent_elbo.finite.coupling_readback import couplings_action
    from multiagent_elbo.finite.coupling_readback import _readback_from_action
    from multiagent_elbo.finite.closure_residual import _declared_parent_prior
    from multiagent_elbo.finite.nested_tower import reference_tower, tower_blocks
    from multiagent_elbo.finite.rescaling import (
        coarse_action,
        gauge_transformed_model,
        state_shift_permutation,
    )

    tower = reference_tower()
    blocks = tower_blocks(2, 3)
    observation = (1, 0, 1, 0, 1, 0)
    shifts = {1: 1, 2: 2, 3: 0, 4: 2, 5: 1, 6: 2}
    gauged = gauge_transformed_model(tower, shifts)
    base_prior = _declared_parent_prior(tower.state_count)
    permutations = []
    priors = {}
    for block in blocks:
        sigma = state_shift_permutation(tower, shifts[min(block)])
        permutations.append(sigma)
        moved = [0.0] * len(base_prior)
        for state, weight in enumerate(base_prior):
            moved[sigma[state]] = weight
        priors[min(block)] = tuple(moved)
    plain_action, plain_flow = coarse_action(tower, observation, blocks)
    gauged_action, gauged_flow = coarse_action(gauged, observation, blocks, priors)
    plain_step = _readback_from_action(tower, plain_action, plain_flow, blocks)
    gauged_step = _readback_from_action(gauged, gauged_action, gauged_flow, blocks)
    plain_total = couplings_action(regenerated_instance(plain_step).instance.couplings)
    gauged_total = couplings_action(regenerated_instance(gauged_step).instance.couplings)
    inverses = [
        tuple(sorted(range(len(sigma)), key=sigma.__getitem__))
        for sigma in permutations
    ]
    deviation = 0.0
    size = tower.state_count
    for state in product(range(size), repeat=len(blocks)):
        pulled = tuple(
            inverses[position][value] for position, value in enumerate(state)
        )
        deviation = max(
            deviation,
            abs(float(gauged_total[state]) - float(plain_total[pulled])),
        )
    assert deviation <= 1.0e-11


def test_an_unreachable_sector_count_is_refused() -> None:
    from multiagent_elbo.finite.cocycle_flow import (
        capacity_pair_retention,
        homogeneous_circulant_instance,
    )

    instance = homogeneous_circulant_instance(4, (1,), SITE, PAIR)
    with pytest.raises(ValueError, match="reachable"):
        capacity_pair_retention(instance, 2, sector_count=6)
    with pytest.raises(ValueError, match="positive integer"):
        capacity_pair_retention(instance, 2, sector_count=0)


def test_the_capacity_sector_charge_is_gauge_covariant() -> None:
    from multiagent_elbo.finite.cocycle_flow import (
        capacity_pair_retention,
        homogeneous_circulant_instance,
    )
    from multiagent_elbo.finite.coupling_readback import (
        PairwiseInstance,
        _kernel_model,
        mobius_couplings,
    )
    from multiagent_elbo.finite.rescaling import (
        gauge_transformed_model,
        state_shift_permutation,
    )

    instance = homogeneous_circulant_instance(4, (1,), SITE, PAIR)
    model = _kernel_model(instance.graph, "capacity-gauge")
    shifts = {1: 0, 2: 1, 3: 0, 4: 2}
    sigma = {
        vertex: state_shift_permutation(model, shifts[vertex])
        for vertex in instance.graph.vertices
    }
    action = couplings_action(instance.couplings)
    size = model.state_count
    permuted = {}
    for state in product(range(size), repeat=4):
        image = tuple(
            sigma[position + 1][value] for position, value in enumerate(state)
        )
        permuted[image] = Fraction(float(action[state]))
    admitted = tuple(pair for pair, _ in instance.couplings.pairs)
    gauged_couplings, omitted = mobius_couplings(permuted, admitted)
    assert float(omitted) <= 1.0e-12
    gauged = PairwiseInstance(
        graph=gauge_transformed_model(model, shifts).graph,
        couplings=gauged_couplings,
    )
    plain = capacity_pair_retention(instance, 2)
    moved = capacity_pair_retention(gauged, 2)
    assert abs(plain.coarse_pair_sup - moved.coarse_pair_sup) <= 1.0e-9
    from multiagent_elbo.finite.cocycle_flow import capacity_information_retention

    plain_information = capacity_information_retention(instance, 2)
    moved_information = capacity_information_retention(gauged, 2)
    assert abs(
        plain_information.coarse_information - moved_information.coarse_information
    ) <= 1.0e-9
    assert abs(
        plain_information.retention - moved_information.retention
    ) <= 1.0e-9


def test_the_information_retention_control_ceiling_and_determinism() -> None:
    from multiagent_elbo.finite.cocycle_flow import (
        capacity_information_retention,
        homogeneous_circulant_instance,
    )

    instance = homogeneous_circulant_instance(4, (1,), SITE, PAIR)
    nine_state = capacity_information_retention(instance, 2, sector_count=1)
    control = capacity_information_retention(instance, 2, constant_sector=True)
    assert abs(control.retention - nine_state.retention) <= 1.0e-12
    assert control.sector_count == 1
    sectored = capacity_information_retention(instance, 2)
    assert sectored.sector_count == 3
    assert sectored.fine_information > 0.0
    assert sectored.coarse_information >= 0.0
    assert sectored.retention <= 1.0 + 1.0e-9
    assert nine_state.retention <= 1.0 + 1.0e-9
    assert abs(sectored.fine_information - nine_state.fine_information) <= 1.0e-12
    again = capacity_information_retention(instance, 2)
    assert again == sectored
