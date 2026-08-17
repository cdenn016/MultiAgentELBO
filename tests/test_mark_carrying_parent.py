"""Tests for the mark-carrying parent alternative on curved blocks."""

from __future__ import annotations

import math

import numpy as np
import pytest

from multiagent_elbo.finite.categorical_falsification_model import build_reference_model
from multiagent_elbo.finite import holonomy_selection as selection
from multiagent_elbo.finite import mark_carrying_parent as marks
from multiagent_elbo.finite.holonomy_retention import block_holonomy_group

STATES = [0, 1, 2, 3, 4, 5]
CURVED = (1, 2, 3)
FLAT = (4, 5, 6)


def test_the_retention_route_gives_every_block_a_finite_energy() -> None:
    """Mutation caught: an exclusion surviving where the theory offers a parent."""
    model = build_reference_model()
    for block in (CURVED, FLAT, (1, 2, 3, 4), (1, 2, 3, 4, 5, 6), (1, 2)):
        energy = marks.mark_carrying_block_energy(model, block, STATES, 1.0)
        assert np.isfinite(energy)
    assert selection.admissible_parent_states(model, CURVED, False) == ()
    assert marks.stabilized_block_energy(model, CURVED, STATES) == float("inf")


def test_a_flat_block_is_charged_nothing_and_a_curved_block_pays_the_group() -> None:
    """Mutation caught: a retention charge that does not track the holonomy."""
    model = build_reference_model()
    assert block_holonomy_group(model, FLAT, "belief") == (0,)
    assert marks.mark_space_size(model, FLAT, "belief") == 1
    assert marks.mark_retention_cost(model, FLAT) == pytest.approx(0.0, abs=1e-15)
    assert block_holonomy_group(model, CURVED, "belief") == (0, 1, 2)
    assert marks.mark_space_size(model, CURVED, "belief") == 3
    assert marks.mark_retention_cost(model, CURVED) == pytest.approx(math.log(3))


def test_a_flat_block_takes_the_stabilized_route_at_any_positive_price() -> None:
    """Mutation caught: charging retention where no marks need retaining."""
    model = build_reference_model()
    for price in (0.0, 1.0, 10.0):
        choice = marks.block_route(model, FLAT, STATES, price)
        assert choice.route == "stabilized"
        assert choice.stabilized_energy == pytest.approx(choice.mark_carrying_energy)


def test_a_curved_block_can_only_take_the_retention_route() -> None:
    """Mutation caught: a curved block silently reported as stabilized."""
    model = build_reference_model()
    choice = marks.block_route(model, CURVED, STATES, 1.0)
    assert choice.route == "mark_carrying"
    assert choice.stabilized_energy == float("inf")
    assert np.isfinite(choice.mark_carrying_energy)


def test_the_holonomy_is_gauge_invariant_and_the_boundary_legs_are_not() -> None:
    """Mutation caught: quotienting the holonomy separately from the boundary."""
    model = build_reference_model()
    datum = marks.mark_datum(model, CURVED, "belief", 0)
    orbit = marks.root_gauge_orbit(model, datum)
    assert len(orbit) == model.graph.order
    assert len({item.holonomy for item in orbit}) == 1
    assert len({item.boundary for item in orbit}) > 1
    assert len({item.presentation for item in orbit}) > 1


def test_a_root_regauge_moves_presentation_and_boundary_together() -> None:
    """Mutation caught: regauging one component of the retained datum alone."""
    model = build_reference_model()
    datum = marks.mark_datum(model, CURVED, "belief", 0)
    assert marks.regauge(model, datum, 0) == datum
    once = marks.regauge(model, datum, 1)
    assert once.presentation != datum.presentation
    assert once.boundary != datum.boundary
    twice = marks.regauge(model, once, 1)
    assert twice == marks.regauge(model, datum, 2)
    assert marks.regauge(model, twice, 1) == datum


def test_the_orbit_representative_is_stable_across_the_whole_orbit() -> None:
    """Mutation caught: an orbit label that depends on the chosen frame."""
    model = build_reference_model()
    datum = marks.mark_datum(model, CURVED, "belief", 0)
    representative = marks.orbit_representative(model, datum)
    for shift in range(model.graph.order):
        moved = marks.regauge(model, datum, shift)
        assert marks.orbit_representative(model, moved) == representative


def test_the_boundary_generators_are_the_declared_leaving_edges() -> None:
    """Mutation caught: retaining internal edges as if they were boundary legs."""
    model = build_reference_model()
    datum = marks.mark_datum(model, CURVED, "belief", 0)
    endpoints = {pair for pair, _ in datum.boundary}
    assert endpoints == {(3, 4), (6, 1)}


def test_no_partition_is_excluded_once_retention_is_available() -> None:
    """Mutation caught: the prohibition surviving as a price in name only."""
    model = build_reference_model()
    for partition in model.candidate_partitions:
        energy = marks.retained_block_energy(model, partition, STATES, 1.0)
        assert np.isfinite(energy)
    forbidden = ((1, 2, 3), (4, 5, 6))
    assert selection.constrained_block_energy(model, forbidden, STATES) == float("inf")


def test_a_high_retention_price_reproduces_the_stabilized_exclusion() -> None:
    """Mutation caught: a retention route that does not limit to the hard selector."""
    model = build_reference_model()
    forbidden = ((1, 2, 3), (4, 5, 6))
    allowed = ((1, 2), (3, 4), (5, 6))
    cheap = marks.retained_free_energy(model, forbidden, STATES, 0.0)
    dear = marks.retained_free_energy(model, forbidden, STATES, 1.0e6)
    assert np.isfinite(cheap)
    assert dear > 1.0e5
    steady = marks.retained_free_energy(model, allowed, STATES, 1.0e6)
    assert steady == pytest.approx(
        marks.retained_free_energy(model, allowed, STATES, 0.0)
    )


def test_the_selected_partition_moves_with_the_retention_price() -> None:
    """Mutation caught: a declared price that does not change any outcome."""
    model = build_reference_model()
    cheap = marks.selected_partition(model, STATES, 0.0)
    dear = marks.selected_partition(model, STATES, 20.0)
    assert cheap != dear
    assert any(
        block_holonomy_group(model, block, "belief") != (0,) for block in cheap
    )
    assert all(
        block_holonomy_group(model, block, "belief") == (0,) for block in dear
    )


def test_the_retained_energy_never_exceeds_the_stabilized_energy() -> None:
    """Mutation caught: a disjunction implemented as a replacement."""
    model = build_reference_model()
    for partition in model.candidate_partitions:
        retained = marks.retained_block_energy(model, partition, STATES, 1.0)
        stabilized = sum(
            marks.stabilized_block_energy(model, block, STATES) for block in partition
        )
        assert retained <= stabilized + 1.0e-12
