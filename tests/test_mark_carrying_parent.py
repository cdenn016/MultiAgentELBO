"""Tests for the mark-carrying parent alternative on curved blocks."""

from __future__ import annotations

import math

import numpy as np
import pytest

from multiagent_elbo.finite.categorical_falsification_model import build_reference_model
from multiagent_elbo.finite import bidirected as bidi
from multiagent_elbo.finite import holonomy_selection as selection
from multiagent_elbo.finite import mark_carrying_parent as marks
from multiagent_elbo.finite import plaquette_action as plaquettes
from multiagent_elbo.finite.holonomy_retention import block_holonomy_group
from multiagent_elbo.finite.two_channel_gauge import TwoChannelGraph

STATES = [0, 1, 2, 3, 4, 5]
CURVED = (1, 2, 3)
FLAT = (4, 5, 6)


def _regauged(model, shifts: dict[int, int]):
    """Return the model with a per-agent regauging applied to both channels.

    An edge carries the source frame into the receiver frame, so a regauging adds
    the source shift and subtracts the receiver shift. This is the same convention
    the plaquette tests declare, and it is the action a root gauge induces on the
    connection once the shift is held constant over a block.
    """
    order = model.graph.order
    belief = []
    model_elements = []
    for index, edge in enumerate(model.graph.edges):
        delta = shifts.get(edge.source, 0) - shifts.get(edge.receiver, 0)
        belief.append((model.graph.belief_elements[index] + delta) % order)
        model_elements.append((model.graph.model_elements[index] + delta) % order)
    graph = TwoChannelGraph(
        order=order,
        vertices=model.graph.vertices,
        edges=model.graph.edges,
        belief_elements=tuple(belief),
        model_elements=tuple(model_elements),
    )
    return type(model)(**{**vars(model), "graph": graph})


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


def test_regauge_reproduces_the_datum_recomputed_from_a_regauged_connection() -> None:
    """Mutation caught: a uniform boundary shift where the gauge action is signed.

    A root gauge is the block-constant regauging of the connection, under which
    every tree transport is fixed. The boundary generators are not: a leg whose
    inside endpoint is the receiver absorbs minus the shift, while a leg whose inside
    endpoint is the source absorbs plus the shift, because the edge action carries
    opposite signs at its two endpoints. Block (1, 2, 3) has exactly one leg of each
    orientation, so charging both the same way preserves their difference and breaks
    their sum. The check is not circular: the right-hand side rebuilds the model and
    recomputes `mark_datum` from scratch.
    """
    model = build_reference_model()
    for channel in marks.CHANNELS:
        datum = marks.mark_datum(model, CURVED, channel, 0)
        assert {pair for pair, _ in datum.boundary} == {(3, 4), (6, 1)}
        for shift in range(model.graph.order):
            moved = _regauged(model, {agent: shift for agent in CURVED})
            recomputed = marks.mark_datum(moved, CURVED, channel, 0)
            predicted = marks.regauge(model, datum, shift)
            assert recomputed.boundary == predicted.boundary
            assert recomputed.holonomy == predicted.holonomy


def test_the_boundary_legs_of_a_bidirected_block_all_transform_correctly() -> None:
    """Mutation caught: a sign rule tuned to a block with one leg per orientation.

    On the bi-directed instance the same block leaves four boundary arcs, two in each
    orientation, so a rule that happened to fit the one-way skeleton by symmetry is
    separated from the induced action here.
    """
    model = bidi.build_bidirected_model("independent")
    for channel in marks.CHANNELS:
        datum = marks.mark_datum(model, CURVED, channel, 0)
        assert {pair for pair, _ in datum.boundary} == {(3, 4), (4, 3), (6, 1), (1, 6)}
        for shift in range(model.graph.order):
            moved = _regauged(model, {agent: shift for agent in CURVED})
            recomputed = marks.mark_datum(moved, CURVED, channel, 0)
            assert recomputed.boundary == marks.regauge(model, datum, shift).boundary


def test_the_presentation_is_pushed_by_the_inverse_of_the_root_gauge() -> None:
    """Mutation caught: pushing the presentation forward by the gauge instead.

    Matter transforms by the inverse of the gauge, which is what leaves the
    transported mismatch invariant: the cost table of the regauged model, read at the
    parent and child states pushed by minus the per-agent shift, reproduces the
    original table exactly. A root gauge is block constant, so the parent state moves
    by minus the shift and that is the action `regauge` must implement on the
    presentation.
    """
    model = build_reference_model()
    size = len(model.model_family)
    table = marks._unrestricted_cost_table(model, CURVED)

    def pushed(index: int, element: int) -> int:
        belief_index, model_index = divmod(index, size)
        belief = model.belief_representation.act(
            element % model.graph.order, model.belief_family[belief_index]
        )
        law = model.model_representation.act(
            element % model.graph.order, model.model_family[model_index]
        )
        return model.belief_family.index(belief) * size + model.model_family.index(law)

    for shifts in ({1: 1, 2: 2, 3: 0}, {1: 2, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}):
        moved = marks._unrestricted_cost_table(_regauged(model, shifts), CURVED)
        for parent in range(table.shape[0]):
            for column, agent in enumerate(CURVED):
                for child in range(table.shape[2]):
                    assert moved[
                        pushed(parent, -shifts[min(CURVED)]), column,
                        pushed(child, -shifts[agent]),
                    ] == table[parent, column, child]
    datum = marks.mark_datum(model, CURVED, "belief", 0)
    for shift in range(model.graph.order):
        expected = pushed(0, -shift) // size
        assert marks.regauge(model, datum, shift).presentation // size == expected


def test_the_orbit_representative_is_stable_across_the_whole_orbit() -> None:
    """Mutation caught: an orbit label that depends on the chosen frame."""
    for source in (build_reference_model(), bidi.build_bidirected_model("independent")):
        for channel in marks.CHANNELS:
            datum = marks.mark_datum(source, CURVED, channel, 0)
            representative = marks.orbit_representative(source, datum)
            for shift in range(source.graph.order):
                moved = marks.regauge(source, datum, shift)
                assert marks.orbit_representative(source, moved) == representative
                rebuilt = marks.mark_datum(
                    _regauged(source, {agent: shift for agent in CURVED}), CURVED,
                    channel, moved.presentation,
                )
                assert marks.orbit_representative(source, rebuilt) == representative


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


def test_the_block_count_prior_is_neutral_on_block_balance() -> None:
    """Mutation caught: a prior that decides the balance question in advance."""
    balanced = ((1, 2, 3), (4, 5, 6))
    lopsided = ((1,), (2, 3, 4, 5, 6))
    for concentration in (0.2, 1.0, 7.0):
        neutral = marks.log_partition_prior(
            balanced, concentration, "block_count"
        ) - marks.log_partition_prior(lopsided, concentration, "block_count")
        assert neutral == pytest.approx(0.0, abs=1e-12)
        ewens = marks.log_partition_prior(
            balanced, concentration, "ewens"
        ) - marks.log_partition_prior(lopsided, concentration, "ewens")
        assert ewens == pytest.approx(-math.log(6.0), abs=1e-12)


def test_the_block_count_prior_still_charges_for_parent_nodes() -> None:
    """Mutation caught: a neutral prior that also stops penalizing block count."""
    one = ((1, 2, 3, 4, 5, 6),)
    three = ((1, 2), (3, 4), (5, 6))
    small = marks.log_partition_prior(three, 0.2, "block_count")
    assert small < marks.log_partition_prior(one, 0.2, "block_count")
    large = marks.log_partition_prior(three, 5.0, "block_count")
    assert large > marks.log_partition_prior(one, 5.0, "block_count")
    with pytest.raises(ValueError):
        marks.log_partition_prior(one, 1.0, "not_a_prior")


def test_the_designed_partition_carries_a_retention_charge() -> None:
    """Mutation caught: expecting selection of the very block the mechanism taxes."""
    model = build_reference_model()
    designed = ((1, 2, 3), (4, 5, 6))
    assert sum(marks.mark_retention_cost(model, b) for b in designed) > 0.0
    for partition in (((1, 2), (3, 4), (5, 6)), ((1,), (2, 3, 4, 5, 6))):
        assert sum(marks.mark_retention_cost(model, b) for b in partition) == 0.0


def test_a_neutral_prior_lets_the_designed_partition_win_only_at_zero_price() -> None:
    """Mutation caught: claiming a gauge selection the retention charge forbids."""
    model = build_reference_model()
    designed = ((1, 2, 3), (4, 5, 6))
    assert marks.modal_partition(model, 0.0, 0.5, "block_count") == designed
    for price in (0.5, 1.0, 3.0):
        assert marks.modal_partition(model, price, 0.5, "block_count") != designed


def test_the_neutral_prior_changes_which_partition_is_selected() -> None:
    """Mutation caught: a prior argument that is accepted and then ignored."""
    model = build_reference_model()
    assert marks.modal_partition(model, 0.0, 1.0, "ewens") != marks.modal_partition(
        model, 0.0, 1.0, "block_count"
    )


def test_the_wilson_term_is_a_state_independent_offset() -> None:
    """Mutation caught: a face charge that leaks into the per-state enumeration."""
    model = build_reference_model()
    block = (1, 2, 3)
    base = marks.block_log_partition(model, block, 0.0)
    charge = plaquettes.block_wilson_action(model, block, "peaked")
    assert charge > 0.0
    for coupling in (1.0, 5.0):
        shifted = marks.block_log_partition(model, block, 0.0, coupling, "peaked")
        assert shifted == pytest.approx(base - coupling * charge, abs=1e-9)


def test_a_zero_wilson_coupling_leaves_the_earlier_results_untouched() -> None:
    """Mutation caught: a new term that is active when it was not asked for."""
    model = build_reference_model()
    for price in (0.0, 1.0):
        assert marks.modal_partition(model, price, 1.0) == marks.modal_partition(
            model, price, 1.0, "ewens", 0.0, "peaked"
        )


def test_the_attention_configuration_changes_the_selected_partition() -> None:
    """Mutation caught: attention that still cannot reach partition selection.

    This is the property the earlier block energy lacked. With the face charge in
    place the two declared row configurations disagree over a band of couplings,
    so the attention weights select rather than merely accompany.
    """
    model = build_reference_model()
    disagreements = [
        marks.modal_partition(model, 0.0, 1.0, "ewens", coupling, "peaked")
        != marks.modal_partition(model, 0.0, 1.0, "ewens", coupling, "uniform")
        for coupling in (4.0, 5.0, 6.0)
    ]
    assert all(disagreements)


def test_every_curvature_charge_enters_one_additive_budget() -> None:
    """Mutation caught: a face charge on a different footing from the mark price.

    At the transition the charge carried by the whole-graph block plus the log
    concentration is one constant, whether that charge is bought with the retention
    price against the holonomy group or with the Wilson coupling against the
    attention-weighted faces.
    """
    model = build_reference_model()
    invariants = []
    for configuration in ("peaked", "uniform"):
        weight = plaquettes.partition_wilson_action(
            model, ((1, 2, 3, 4, 5, 6),), configuration
        )
        for concentration in (0.2, 1.0):
            low, high = 0.0, 400.0
            start = marks.modal_partition(
                model, 0.0, concentration, "ewens", low, configuration
            )
            for _ in range(45):
                middle = (low + high) / 2.0
                if (
                    marks.modal_partition(
                        model, 0.0, concentration, "ewens", middle, configuration
                    )
                    == start
                ):
                    low = middle
                else:
                    high = middle
            critical = (low + high) / 2.0
            invariants.append(critical * weight + math.log(concentration))
    price = marks.critical_mark_price(model, 1.0)
    invariants.append(price * math.log(3.0) + math.log(1.0))
    assert max(invariants) - min(invariants) < 1e-6


def test_the_retained_energy_never_exceeds_the_stabilized_energy() -> None:
    """Mutation caught: a disjunction implemented as a replacement."""
    model = build_reference_model()
    for partition in model.candidate_partitions:
        retained = marks.retained_block_energy(model, partition, STATES, 1.0)
        stabilized = sum(
            marks.stabilized_block_energy(model, block, STATES) for block in partition
        )
        assert retained <= stabilized + 1.0e-12
