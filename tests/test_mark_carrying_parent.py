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


def test_the_exact_posterior_is_normalized_and_covers_every_candidate() -> None:
    """Mutation caught: a posterior taken at frozen states rather than marginalized."""
    model = build_reference_model()
    posterior = marks.partition_posterior(model, 1.0, 1.0)
    assert set(posterior) == set(model.candidate_partitions)
    assert sum(posterior.values()) == pytest.approx(1.0, abs=1e-12)
    assert all(value >= 0.0 for value in posterior.values())
    with pytest.raises(ValueError):
        marks.partition_posterior(model, 1.0, 0.0)


def test_a_block_without_a_stabilized_route_shifts_rigidly_with_the_price() -> None:
    """Mutation caught: a retention charge that is not a uniform energy offset."""
    model = build_reference_model()
    block = (1, 2, 3)
    charge = marks.mark_retention_cost(model, block)
    base = marks.block_log_partition(model, block, 0.0)
    for price in (0.5, 2.0, 7.0):
        shifted = marks.block_log_partition(model, block, price)
        assert shifted == pytest.approx(base - price * charge, abs=1e-9)


def test_a_flat_block_log_partition_does_not_move_with_the_price() -> None:
    """Mutation caught: charging retention to a block that retains nothing."""
    model = build_reference_model()
    base = marks.block_log_partition(model, FLAT, 0.0)
    assert marks.block_log_partition(model, FLAT, 25.0) == pytest.approx(base)


def test_the_phase_boundary_is_exactly_linear_in_log_concentration() -> None:
    """Mutation caught: a boundary that is fitted rather than structural.

    Below the transition the modal partition carries the curved loop inside one
    block, whose energy shifts rigidly with the retention price, while the
    partition above it carries no curved block at all. The prior enters only
    through the block count, so the boundary is a straight line in the plane of
    retention price against log concentration, with slope minus one over the
    retention charge.
    """
    model = build_reference_model()
    charge = math.log(3.0)
    invariants = []
    for concentration in (0.05, 0.2, 0.5, 1.0):
        price = marks.critical_mark_price(model, concentration)
        assert price is not None
        invariants.append(price * charge + math.log(concentration))
    assert max(invariants) - min(invariants) < 1e-6


def test_the_boundary_constant_matches_its_closed_form() -> None:
    """Mutation caught: a transition located numerically without an explanation."""
    model = build_reference_model()
    whole = marks.block_log_partition(model, (1, 2, 3, 4, 5, 6), 0.0)
    singleton = marks.block_log_partition(model, (1,), 0.0)
    rest = marks.block_log_partition(model, (2, 3, 4, 5, 6), 0.0)
    predicted = whole - singleton - rest + math.log(120.0 / 24.0)
    measured = marks.critical_mark_price(model, 1.0) * math.log(3.0)
    assert measured == pytest.approx(predicted, abs=1e-8)


def test_a_large_concentration_removes_the_transition_entirely() -> None:
    """Mutation caught: a bisection that reports a boundary where none exists."""
    model = build_reference_model()
    assert marks.critical_mark_price(model, 5.0) is None
    assert marks.modal_partition(model, 0.0, 5.0) == marks.modal_partition(
        model, 30.0, 5.0
    )


def test_the_designed_partition_is_never_modal_in_the_swept_window() -> None:
    """Mutation caught: reporting a selection the sweep does not actually produce."""
    model = build_reference_model()
    designed = ((1, 2, 3), (4, 5, 6))
    assert designed in model.candidate_partitions
    for price in (0.0, 1.0, 4.0):
        for concentration in (0.1, 1.0, 10.0):
            assert marks.modal_partition(model, price, concentration) != designed


def test_the_retained_energy_never_exceeds_the_stabilized_energy() -> None:
    """Mutation caught: a disjunction implemented as a replacement."""
    model = build_reference_model()
    for partition in model.candidate_partitions:
        retained = marks.retained_block_energy(model, partition, STATES, 1.0)
        stabilized = sum(
            marks.stabilized_block_energy(model, block, STATES) for block in partition
        )
        assert retained <= stabilized + 1.0e-12
