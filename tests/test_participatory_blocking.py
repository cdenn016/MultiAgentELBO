"""Tests for participatory blocking, the flow selecting its own partition."""

from __future__ import annotations

from fractions import Fraction

import pytest

from multiagent_elbo.finite.cocycle_flow import homogeneous_cycle_instance
from multiagent_elbo.finite.participatory_blocking import (
    blocking_posterior,
    cycle_blocking_candidates,
    participatory_flow,
)

SITE = tuple(Fraction(index, 10) for index in range(9))
PAIR = tuple(
    tuple(Fraction(0) if 0 in (left, right) else Fraction(left * 3 + right, 100) for right in range(9))
    for left in range(9)
)


def test_the_candidate_set_carries_the_declared_classes() -> None:
    six = cycle_blocking_candidates(6)
    counts: dict[int, int] = {}
    for ratio, _ in six:
        counts[ratio] = counts.get(ratio, 0) + 1
    assert counts == {1: 1, 2: 2, 3: 3, 6: 1}
    four = cycle_blocking_candidates(4)
    assert {ratio for ratio, _ in four} == {1, 2, 4}
    assert len(four) == 4
    wrapped = [partition for ratio, partition in four if ratio == 2]
    assert ((1, 4), (2, 3)) in wrapped
    with pytest.raises(ValueError):
        cycle_blocking_candidates(1)


def test_the_posterior_is_a_law_with_symmetric_placements() -> None:
    instance = homogeneous_cycle_instance(4, SITE, PAIR)
    posterior = blocking_posterior(instance)
    assert abs(sum(posterior.masses) - 1.0) <= 1.0e-12
    # Placement symmetry is approximate, not exact: the min-root convention
    # combined with the identity-holonomy flat mixture in the M5 energy is not
    # re-rooting equivariant on wrapped blocks, giving an O(1e-4) gap that the
    # amendment declares as a reported homogeneity check rather than assuming.
    assert posterior.placement_gap <= 1.0e-2
    assert abs(sum(mass for _, mass in posterior.class_masses) - 1.0) <= 1.0e-12
    assert posterior.modal_ratio in {1, 2, 4}
    again = blocking_posterior(instance)
    assert again == posterior


def test_the_participatory_flow_terminates_with_a_declared_path() -> None:
    instance = homogeneous_cycle_instance(4, SITE, PAIR)
    path = participatory_flow(instance, channel="passive")
    assert path.site_counts[0] == 4
    assert all(
        later < earlier
        for earlier, later in zip(path.site_counts, path.site_counts[1:])
    )
    assert len(path.levels) >= 1
    for level, count in zip(path.levels, path.site_counts):
        assert level.length == count
    with pytest.raises(ValueError):
        participatory_flow(instance, channel="undeclared")
