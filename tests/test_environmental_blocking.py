"""Tests for the environmental agent class and the coupled-descent instrument."""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import pytest

from multiagent_elbo.finite.cocycle_flow import (
    consecutive_blocks,
    homogeneous_cycle_instance,
)
from multiagent_elbo.finite.coupling_readback import _kernel_model, couplings_action
from multiagent_elbo.finite.environmental_blocking import (
    EnvironmentalDressing,
    anchored_posterior,
    coupled_blocking_descent,
    dressed_instance,
    environmental_parent,
    environmental_step,
)
from multiagent_elbo.finite.participatory_blocking import blocking_posterior

SITE = tuple(Fraction(index, 10) for index in range(9))
PAIR = tuple(
    tuple(Fraction(0) if 0 in (left, right) else Fraction(left * 3 + right, 100) for right in range(9))
    for left in range(9)
)


def test_dressing_adds_the_anchored_field_exactly() -> None:
    instance = homogeneous_cycle_instance(4, SITE, PAIR)
    dressing = EnvironmentalDressing(pinned=(0, 4, 8, 2), strength=2.0)
    dressed = dressed_instance(instance, dressing)
    for table in dressed.couplings.sites:
        assert table[0] == Fraction(0)
    bare = couplings_action(instance.couplings)
    total = couplings_action(dressed.couplings)
    difference = total - bare
    assert np.all(np.isfinite(difference))
    assert float(difference.min()) >= -1.0e-12
    assert float(difference.max()) > 0.0
    zero_pin = EnvironmentalDressing(pinned=(0, 0, 0, 0), strength=0.0)
    unchanged = dressed_instance(instance, zero_pin)
    assert couplings_action(unchanged.couplings)[(1, 2, 3, 4)] == pytest.approx(
        float(bare[(1, 2, 3, 4)])
    )
    with pytest.raises(ValueError):
        dressed_instance(instance, EnvironmentalDressing(pinned=(0, 0, 0), strength=1.0))
    with pytest.raises(ValueError):
        dressed_instance(instance, EnvironmentalDressing(pinned=(0, 0, 0, 9), strength=1.0))


def test_the_environmental_step_re_dresses_to_the_audited_coarse_exactly() -> None:
    instance = homogeneous_cycle_instance(4, SITE, PAIR)
    dressing = EnvironmentalDressing(pinned=(0, 4, 8, 2), strength=2.0)
    blocks = consecutive_blocks(4, 2)
    step, undressed, coarse_dressing = environmental_step(instance, dressing, blocks)
    assert undressed is not None
    assert len(coarse_dressing.pinned) == 2
    model = _kernel_model(instance.graph, "test-env-parent")
    for index, block in enumerate(blocks):
        pin = environmental_parent(model, tuple(block), dressing)
        assert coarse_dressing.pinned[index] == pin
        assert 0 <= pin < model.state_count
    redressed = dressed_instance(undressed, coarse_dressing)
    assert redressed.couplings == step.instance.couplings


def test_the_anchored_posterior_is_a_law_the_field_actually_moves() -> None:
    instance = homogeneous_cycle_instance(4, SITE, PAIR)
    dressing = EnvironmentalDressing(pinned=(3, 3, 7, 7), strength=2.0)
    anchored = anchored_posterior(instance, dressing)
    bare = blocking_posterior(instance)
    assert abs(sum(anchored.masses) - 1.0) <= 1.0e-12
    assert max(
        abs(left - right) for left, right in zip(anchored.masses, bare.masses)
    ) > 1.0e-6


def test_the_coupled_descent_is_deterministic_and_reports_a_law() -> None:
    instance = homogeneous_cycle_instance(4, SITE, PAIR)
    first = coupled_blocking_descent(
        instance, steps=300, burn_in=100, seeds=(0,)
    )
    second = coupled_blocking_descent(
        instance, steps=300, burn_in=100, seeds=(0,)
    )
    assert first == second
    assert abs(sum(mass for _, mass in first.class_occupancies) - 1.0) <= 1.0e-9
    assert 0.0 < first.acceptance_rate <= 1.0
    assert len(first.per_replica_modal) == 1
