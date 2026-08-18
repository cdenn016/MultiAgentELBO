"""Tests for the nested-cycle tower family and the phase-one rescaling checks."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

import pytest

from multiagent_elbo.finite.categorical_falsification_model import (
    build_reference_model,
)
from multiagent_elbo.finite.holonomy_retention import block_transport_elements
from multiagent_elbo.finite.nested_tower import (
    build_tower_model,
    reference_tower,
    tower_blocks,
    tower_edges,
)
from multiagent_elbo.finite.rescaling import (
    GAUGE_COVARIANCE_TOLERANCE,
    check_gauge_covariance,
    check_holonomy_conservation,
    check_wilson_charge_conservation,
    coarse_action,
    coarse_connection,
    gauge_transformed_model,
    state_shift_permutation,
)
from multiagent_elbo.finite.two_channel_gauge import holonomy_group

OBSERVATION = (1, 0, 1, 0, 1, 0)

LARGE_BELIEF = (1, 1, 0, 1, 1, 1, 0, 2, 1, 1, 2, 0)
LARGE_MODEL = (1, 1, 1, 2, 2, 2, 0, 1, 2, 0, 1, 2)


def large_tower(boundary: str = "last_observes_first"):
    """Return a C(3, 3) instance with nontrivial declared transports."""
    return build_tower_model(3, 3, LARGE_BELIEF, LARGE_MODEL, boundary=boundary)


def test_the_reference_tower_reproduces_the_reference_instance() -> None:
    tower = reference_tower()
    reference = build_reference_model()
    assert tower.graph == reference.graph
    assert tower.alpha_belief == reference.alpha_belief
    assert tower.alpha_model == reference.alpha_model
    assert tower.belief_family == reference.belief_family
    assert tower.model_family == reference.model_family
    assert tower.candidate_partitions[0] == reference.candidate_partitions[0]


def test_the_reversed_boundary_convention_flips_only_the_cross_arcs() -> None:
    forward = tower_edges(2, 3, "last_observes_first")
    reversed_ = tower_edges(2, 3, "first_observes_last")
    assert forward[:6] == reversed_[:6]
    assert [(e.receiver, e.source) for e in reversed_[6:]] == [
        (4, 3),
        (1, 6),
    ]


def test_the_tower_rejects_undeclared_sizes_elements_and_occupancies() -> None:
    with pytest.raises(ValueError):
        tower_blocks(1, 3)
    with pytest.raises(ValueError):
        tower_edges(2, 3, "undeclared")
    with pytest.raises(ValueError):
        build_tower_model(2, 3, (0,) * 7, (0,) * 8)
    with pytest.raises(ValueError):
        build_tower_model(
            2, 3, (0,) * 8, (0,) * 8, alpha_belief=(Fraction(1, 2),) * 6
        )


def test_the_coarse_links_match_the_direct_wilson_line_formula() -> None:
    tower = reference_tower()
    blocks = tower_blocks(2, 3)
    connection = coarse_connection(tower, blocks)
    block_of = {agent: index for index, block in enumerate(blocks) for agent in block}
    for channel in ("belief", "model"):
        transports = [
            block_transport_elements(tower, block, channel) for block in blocks
        ]
        for position, fine_index in enumerate(connection.fine_edge_indices):
            edge = tower.graph.edges[fine_index]
            bare = tower.graph.channel_elements(channel)[fine_index]
            expected = (
                transports[block_of[edge.receiver]][edge.receiver]
                + bare
                - transports[block_of[edge.source]][edge.source]
            ) % tower.graph.order
            assert (
                connection.graph.channel_elements(channel)[position] == expected
            )


def test_the_reference_coarse_links_carry_the_hand_computed_elements() -> None:
    connection = coarse_connection(reference_tower(), tower_blocks(2, 3))
    assert [
        (edge.receiver, edge.source) for edge in connection.graph.edges
    ] == [(1, 2), (2, 1)]
    assert connection.graph.belief_elements == (0, 2)
    assert connection.graph.model_elements == (2, 1)
    assert connection.retained_holonomy == (
        ((0, 1, 2), (0,)),
        ((0,), (0,)),
    )


def test_a_block_with_reciprocal_inner_arcs_is_refused() -> None:
    tower = build_tower_model(2, 2, (0,) * 6, (0,) * 6)
    with pytest.raises(ValueError, match="reciprocal"):
        coarse_connection(tower, tower_blocks(2, 2))


@pytest.mark.parametrize("boundary", ["last_observes_first", "first_observes_last"])
def test_c2_holds_on_the_reference_tower_under_both_conventions(
    boundary: str,
) -> None:
    tower = build_tower_model(
        2,
        3,
        reference_tower().graph.belief_elements,
        reference_tower().graph.model_elements,
        boundary=boundary,
    )
    report = check_holonomy_conservation(tower, tower_blocks(2, 3))
    assert report.passes
    assert report.coarse_elements == report.fine_elements


@pytest.mark.parametrize("boundary", ["last_observes_first", "first_observes_last"])
def test_c2_holds_on_a_three_by_three_tower_under_both_conventions(
    boundary: str,
) -> None:
    report = check_holonomy_conservation(large_tower(boundary), tower_blocks(3, 3))
    assert report.passes


def test_c2_reports_the_hand_computed_cycle_elements() -> None:
    report = check_holonomy_conservation(reference_tower(), tower_blocks(2, 3))
    assert dict(report.coarse_elements) == {"belief": 2, "model": 0}


def test_the_tree_dressing_of_the_coarse_links_is_load_bearing() -> None:
    tower = reference_tower()
    connection = coarse_connection(tower, tower_blocks(2, 3))
    report = check_holonomy_conservation(tower, tower_blocks(2, 3))
    bare = sum(
        tower.graph.belief_elements[index] for index in connection.fine_edge_indices
    ) % tower.graph.order
    assert bare != dict(report.fine_elements)["belief"]


def test_wilson_charge_is_conserved_and_the_marks_carry_it() -> None:
    tower = reference_tower()
    report = check_wilson_charge_conservation(tower, tower_blocks(2, 3))
    assert report.passes
    assert report.fine_rank == 3
    assert report.coarse_rank == 3
    assert report.retained_charges == (((2,), (0,)), ((0,), (0,)))
    marks = sum(len(belief) for belief, _ in report.retained_charges)
    assert report.coarse_rank - marks == 1
    assert report.fine_rank != report.coarse_rank - marks


@pytest.mark.parametrize("boundary", ["last_observes_first", "first_observes_last"])
def test_wilson_charge_is_conserved_on_the_three_by_three_tower(
    boundary: str,
) -> None:
    report = check_wilson_charge_conservation(
        large_tower(boundary), tower_blocks(3, 3)
    )
    assert report.passes
    assert report.fine_rank == 4


def test_the_state_shift_permutation_preserves_the_likelihood_exactly() -> None:
    tower = reference_tower()
    table = tower.likelihood_table()
    for shift in range(tower.graph.order):
        sigma = state_shift_permutation(tower, shift)
        assert sorted(sigma) == list(range(tower.state_count))
        for index in range(tower.state_count):
            assert table[sigma[index], 0] == table[index, 0]
            assert table[sigma[index], 1] == table[index, 1]


def test_the_state_shift_permutations_compose_as_the_group_does() -> None:
    tower = reference_tower()
    order = tower.graph.order
    for left, right in product(range(order), repeat=2):
        first = state_shift_permutation(tower, left)
        second = state_shift_permutation(tower, right)
        combined = state_shift_permutation(tower, (left + right) % order)
        assert tuple(second[first[i]] for i in range(len(first))) == combined


def test_regauging_leaves_every_based_holonomy_group_unchanged() -> None:
    tower = large_tower()
    shifts = {vertex: (2 * vertex + 1) % 3 for vertex in tower.agents}
    gauged = gauge_transformed_model(tower, shifts)
    for channel in ("belief", "model"):
        for root in tower.agents:
            assert holonomy_group(gauged.graph, channel, root) == holonomy_group(
                tower.graph, channel, root
            )


C1_SHIFTS = {1: 1, 2: 2, 3: 0, 4: 2, 5: 1, 6: 2}


@pytest.mark.parametrize("boundary", ["last_observes_first", "first_observes_last"])
def test_c1_holds_under_a_root_moving_gauge_on_both_conventions(
    boundary: str,
) -> None:
    tower = build_tower_model(
        2,
        3,
        reference_tower().graph.belief_elements,
        reference_tower().graph.model_elements,
        alpha_belief=reference_tower().alpha_belief,
        alpha_model=reference_tower().alpha_model,
        boundary=boundary,
    )
    report = check_gauge_covariance(tower, OBSERVATION, tower_blocks(2, 3), C1_SHIFTS)
    assert report.connection_covariant
    assert report.max_action_deviation <= GAUGE_COVARIANCE_TOLERANCE
    assert report.passes


def test_c1_holds_under_an_interior_only_gauge() -> None:
    report = check_gauge_covariance(
        reference_tower(), OBSERVATION, tower_blocks(2, 3), {2: 1, 5: 2}
    )
    assert report.passes


def test_c1_fails_when_the_parent_law_is_not_treated_as_frame_data() -> None:
    tower = reference_tower()
    blocks = tower_blocks(2, 3)
    gauged = gauge_transformed_model(tower, C1_SHIFTS)
    reference, _ = coarse_action(tower, OBSERVATION, blocks)
    wrong, _ = coarse_action(gauged, OBSERVATION, blocks)
    inverses = []
    for block in blocks:
        sigma = state_shift_permutation(tower, C1_SHIFTS[min(block)])
        inverses.append(tuple(sorted(range(len(sigma)), key=sigma.__getitem__)))
    deviation = max(
        abs(
            float(wrong[state])
            - float(
                reference[
                    tuple(
                        inverses[position][value]
                        for position, value in enumerate(state)
                    )
                ]
            )
        )
        for state in product(range(tower.state_count), repeat=len(blocks))
    )
    assert deviation > 1.0e-3
