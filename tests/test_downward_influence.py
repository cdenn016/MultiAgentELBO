"""Tests for measurement M6, downward influence of the parent on its children."""

from __future__ import annotations

import math

import numpy as np

from multiagent_elbo.finite.categorical_falsification_model import build_reference_model
from multiagent_elbo.finite.downward_influence import (
    child_optimum,
    coarse_statistic,
    deterministic_control,
    downward_influence,
    fiber_disintegration,
    influence_report,
    total_variation,
)

CYCLE_BLOCK = (1, 2, 3)
FULL_BLOCK = (1, 2, 3, 4, 5, 6)


def test_the_child_optimum_is_a_normalized_strictly_positive_law() -> None:
    model = build_reference_model()
    for parent in range(model.state_count):
        optimum = child_optimum(model, CYCLE_BLOCK, 2, parent)
        assert optimum.shape == (model.state_count,)
        assert math.isclose(float(optimum.sum()), 1.0, rel_tol=0.0, abs_tol=1e-12)
        assert float(optimum.min()) > 0.0


def test_the_declared_kernel_factorizes_across_the_two_channels() -> None:
    model = build_reference_model()
    belief_size, model_size = len(model.belief_family), len(model.model_family)
    for parent in range(model.state_count):
        kernel = model.downward_kernel(CYCLE_BLOCK, 3, parent).reshape(belief_size, model_size)
        product = np.outer(kernel.sum(axis=1), kernel.sum(axis=0))
        assert np.allclose(kernel, product, rtol=0.0, atol=1e-12)


def test_the_downward_influence_supremum_is_strictly_positive() -> None:
    model = build_reference_model()
    for agent in CYCLE_BLOCK:
        assert downward_influence(model, CYCLE_BLOCK, agent) > 0.0


def test_the_deterministic_statistic_recovers_a_consistent_parent_state() -> None:
    model = build_reference_model()
    for parent in range(model.state_count):
        configuration = [
            int(np.argmax(model.downward_kernel(CYCLE_BLOCK, agent, parent)))
            for agent in CYCLE_BLOCK
        ]
        assert coarse_statistic(model, CYCLE_BLOCK, configuration) == parent


def test_the_fiber_disintegration_is_normalized_on_the_range_of_the_statistic() -> None:
    model = build_reference_model()
    kernel = fiber_disintegration(model, CYCLE_BLOCK, 2)
    columns = kernel.sum(axis=0)
    assert kernel.shape == (model.state_count, model.state_count)
    assert float(kernel.min()) >= 0.0
    for column in columns:
        assert math.isclose(column, 1.0, rel_tol=0.0, abs_tol=1e-12) or column == 0.0
    assert float(columns.max()) > 0.0


def test_the_deterministic_control_collapses_strictly_below_the_declared_influence() -> None:
    model = build_reference_model()
    influence = downward_influence(model, FULL_BLOCK, 2)
    control = deterministic_control(model, FULL_BLOCK, 2, 1, "exchangeable")
    assert control < influence


def test_the_deterministic_control_does_not_collapse_on_the_three_member_blocks() -> None:
    model = build_reference_model()
    for agent in CYCLE_BLOCK:
        influence = downward_influence(model, CYCLE_BLOCK, agent)
        for reference in ("exchangeable", "generative"):
            assert deterministic_control(model, CYCLE_BLOCK, agent, 1, reference) > influence


def test_the_total_variation_distance_is_symmetric_and_vanishes_on_equal_laws() -> None:
    left = np.array([0.5, 0.25, 0.25], dtype=np.float64)
    right = np.array([0.25, 0.5, 0.25], dtype=np.float64)
    assert total_variation(left, left) == 0.0
    assert math.isclose(total_variation(left, right), total_variation(right, left))
    assert math.isclose(total_variation(left, right), 0.25, rel_tol=0.0, abs_tol=1e-12)


def test_the_influence_report_covers_every_agent_of_every_block() -> None:
    model = build_reference_model()
    reports = influence_report(model)
    partition = model.candidate_partitions[0]
    assert len(reports) == sum(len(block) for block in partition)
    assert {(item.block, item.agent) for item in reports} == {
        (block, agent) for block in partition for agent in block
    }
    for item in reports:
        assert item.influence > 0.0
        assert not item.influence_falsifier_fired
        assert item.control > 0.0
        assert item.generative_reference_control > 0.0
