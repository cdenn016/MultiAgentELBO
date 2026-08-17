"""Tests for the generated many-body terms and the declared closure residual."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import math

import numpy as np
import pytest

from multiagent_elbo.finite.categorical_falsification_model import build_reference_model
from multiagent_elbo.finite.closure_residual import (
    _block_action,
    _coarse_child_weights,
    _declared_parent_prior,
    _divergence_table,
    declared_family_projection,
    flow_weighted_residual,
    ising_star_convergence_ratios,
    ising_star_leading_order,
    ising_star_three_body_coefficient,
    largest_k_body_coefficient,
    coarse_closure_residual,
    model_closure_residual,
)
from multiagent_elbo.finite.scale_cocycle import anchored_mobius_decompose

PLANTED_CONSTANT = Fraction(7, 13)
PLANTED_FIELD = Fraction(3, 11)
PLANTED_PAIR = Fraction(2, 7)
PLANTED_TRIPLE = Fraction(5, 3)


def planted_decomposition():
    """Return the anchored decomposition of an action with a planted triple term."""
    action = {}
    for state in product((0, 1), repeat=3):
        value = PLANTED_CONSTANT
        value += PLANTED_FIELD * state[2]
        value += PLANTED_PAIR * state[0] * state[1]
        value += PLANTED_TRIPLE * state[0] * state[1] * state[2]
        action[state] = value
    return anchored_mobius_decompose(action, anchor=(0, 0, 0))


def test_the_largest_three_body_coefficient_recovers_the_planted_triple_term() -> None:
    decomposition = planted_decomposition()
    subset, coefficient = largest_k_body_coefficient(decomposition, 3)
    assert subset == frozenset({0, 1, 2})
    assert coefficient == PLANTED_TRIPLE


def test_the_largest_coefficient_at_each_lower_order_recovers_its_planted_term() -> None:
    decomposition = planted_decomposition()
    assert largest_k_body_coefficient(decomposition, 2) == (frozenset({0, 1}), PLANTED_PAIR)
    assert largest_k_body_coefficient(decomposition, 1) == (frozenset({2}), PLANTED_FIELD)
    assert largest_k_body_coefficient(decomposition, 0) == (frozenset(), PLANTED_CONSTANT)


def test_reconstruction_from_every_component_returns_the_action_exactly() -> None:
    decomposition = planted_decomposition()
    for state, value in decomposition.action.items():
        assert decomposition.reconstruct(state) == value


def test_admitting_every_subset_leaves_no_closure_residual() -> None:
    decomposition = planted_decomposition()
    projection = declared_family_projection(decomposition, decomposition.components)
    assert projection.omitted_subsets == ()
    assert projection.residual_sup_norm == Fraction(0)
    assert all(value == 0 for value in projection.omitted_value.values())
    assert projection.retained_value == dict(decomposition.action)


def test_a_declared_family_omitting_one_pair_is_not_an_order_cutoff() -> None:
    decomposition = planted_decomposition()
    admitted = [subset for subset in decomposition.components if subset != (0, 1)]
    projection = declared_family_projection(decomposition, admitted)
    assert projection.omitted_subsets == ((0, 1),)
    assert (0, 1, 2) in projection.admitted_subsets
    assert projection.residual_sup_norm == PLANTED_PAIR


def test_the_flow_weighted_residual_is_invariant_under_rescaling_the_weights() -> None:
    decomposition = planted_decomposition()
    admitted = [subset for subset in decomposition.components if len(subset) < 3]
    projection = declared_family_projection(decomposition, admitted)
    uniform = {state: Fraction(1, 8) for state in decomposition.action}
    rescaled = {state: Fraction(3) for state in decomposition.action}
    assert flow_weighted_residual(projection, uniform) == flow_weighted_residual(
        projection, rescaled
    )
    assert flow_weighted_residual(projection, uniform) > 0.0


def test_the_ising_star_ratio_approaches_one_as_the_couplings_shrink() -> None:
    scales = (1.0, 0.5, 0.25, 0.125, 0.0625)
    ratios = ising_star_convergence_ratios(0.7, (0.9, 0.6, 0.4), scales)
    assert tuple(scale for scale, _ in ratios) == scales
    gaps = [abs(ratio - 1.0) for _, ratio in ratios]
    assert all(later < earlier for earlier, later in zip(gaps, gaps[1:]))
    assert gaps[-1] < 1.0e-2


def test_the_exact_star_coefficient_differs_from_the_leading_form_at_finite_coupling() -> None:
    exact = ising_star_three_body_coefficient(0.7, (0.9, 0.6, 0.4))
    leading = ising_star_leading_order(0.7, (0.9, 0.6, 0.4))
    assert exact != leading
    assert exact * leading > 0.0


def test_the_star_three_body_coefficient_vanishes_when_one_coupling_vanishes() -> None:
    assert ising_star_three_body_coefficient(0.4, (0.3, 0.0, 0.5)) == 0.0
    assert ising_star_three_body_coefficient(0.4, (0.0, 0.7, 0.5)) == 0.0
    assert ising_star_three_body_coefficient(0.4, (0.3, 0.7, 0.0)) == 0.0


def test_the_star_three_body_coefficient_vanishes_at_zero_field() -> None:
    assert ising_star_three_body_coefficient(0.0, (0.3, 0.7, 0.5)) == 0.0


def test_the_declared_model_generates_a_nonzero_three_body_coefficient() -> None:
    report = model_closure_residual(build_reference_model(), (1, 0, 1, 0, 1, 0))
    assert report.partition == ((1, 2, 3), (4, 5, 6))
    assert len(report.blocks) == 2
    assert report.largest_three_body_coefficient != 0.0
    assert report.pairwise_closure_holds is False
    assert report.largest_three_body_subset == frozenset(report.largest_three_body_block)
    assert report.flow_weighted_residual > 0.0


def test_every_declared_block_omits_exactly_its_triple_component() -> None:
    report = model_closure_residual(build_reference_model(), (1, 0, 1, 0, 1, 0))
    for block in report.blocks:
        assert block.projection.omitted_subsets == ((0, 1, 2),)
        assert block.residual_sup_norm == pytest.approx(
            abs(block.largest_three_body_coefficient)
        )


def test_the_coarse_direction_eliminates_children_and_keeps_parents() -> None:
    """Mutation caught: measuring the elimination that runs against coarse-graining."""
    model = build_reference_model()
    report = coarse_closure_residual(model, (1, 0, 1, 0, 1, 0))
    assert len(report.partition) >= 3
    assert set(report.partition) <= set(model.candidate_partitions[1])
    orders = dict(report.order_magnitudes)
    assert set(orders) == {1, 2, 3}
    assert all(value > 0.0 for value in orders.values())


def test_the_generated_coarse_triple_is_small_against_the_pairwise_coupling() -> None:
    """Mutation caught: reporting a coarse residual that is not actually small.

    The bound sits below the against-direction ratios, which are 0.21 and 0.28 on
    this instance, so a swap of elimination direction fails here rather than
    passing inside the window.
    """
    model = build_reference_model()
    for partition in (
        ((1, 2), (3, 4), (5, 6)),
        ((2, 3), (1, 6), (4, 5)),
        ((1, 2, 3), (4, 5), (6,)),
    ):
        report = coarse_closure_residual(model, (1, 0, 1, 0, 1, 0), partition)
        assert 0.0 < report.three_to_two_ratio < 0.02
        assert 0.0 < report.flow_weighted_residual < 0.001


def test_the_blocking_kernel_preserves_the_partition_function() -> None:
    """Mutation caught: contracting an operand that is not normalized over parents."""
    model = build_reference_model()
    size = model.state_count
    prior = np.asarray(_declared_parent_prior(size), dtype=np.float64)
    for block in ((1, 2), (1, 2, 3)):
        kernel = prior.reshape((size,) + (1,) * len(block)).copy()
        for offset, agent in enumerate(block):
            rows = np.stack(
                [model.downward_kernel(block, agent, parent) for parent in range(size)]
            )
            shape = [1] * (1 + len(block))
            shape[0] = size
            shape[1 + offset] = size
            kernel = kernel * rows.reshape(shape)
        kernel = kernel / kernel.sum(axis=0, keepdims=True)
        assert np.allclose(kernel.sum(axis=0), 1.0, rtol=0.0, atol=1e-12)


def test_the_coarse_energy_carries_the_declared_receiver_source_orientation() -> None:
    """Mutation caught: placing a divergence table on the transposed axis pair."""
    model = build_reference_model()
    record = (1, 0, 1, 0, 1, 0)
    size = model.state_count
    agents = model.agents
    index_of = {agent: position for position, agent in enumerate(agents)}
    likelihood = model.likelihood_table()
    configuration = model.row_configurations[0]
    event_law = {
        channel: model.edge_event_law(configuration, channel)
        for channel in ("belief", "model")
    }
    kappa = {"belief": model.kappa_belief, "model": model.kappa_model}
    reversed_edges = [
        edge
        for edge in model.graph.edges
        if edge.receiver != edge.source
        and index_of[edge.receiver] > index_of[edge.source]
    ]
    assert reversed_edges, "the instance must exercise the transposed placement"
    tensor = _coarse_child_weights(model, record)
    rng = np.random.default_rng(0)
    for _ in range(25):
        state = tuple(int(value) for value in rng.integers(0, size, len(agents)))
        energy = 0.0
        for position, agent in enumerate(agents):
            energy -= math.log(likelihood[state[position], record[index_of[agent]]])
        for edge_index, edge in enumerate(model.graph.edges):
            if edge.receiver == edge.source:
                continue
            receiver = index_of[edge.receiver]
            source = index_of[edge.source]
            for channel in ("belief", "model"):
                strength = kappa[channel] * float(event_law[channel][receiver, source])
                element = model.graph.channel_elements(channel)[edge_index]
                table = _divergence_table(model, channel, element)
                energy += strength * table[state[receiver], state[source]]
        assert -math.log(tensor[state]) == pytest.approx(energy, abs=1e-12)


def test_a_partition_must_arrange_every_declared_agent_exactly_once() -> None:
    """Mutation caught: accepting a partition that drops or repeats an agent."""
    model = build_reference_model()
    for partition in (
        ((1, 2), (3, 4), (5,)),
        ((1, 2), (2, 3), (4, 5, 6)),
    ):
        with pytest.raises(ValueError):
            coarse_closure_residual(model, (1, 0, 1, 0, 1, 0), partition)


def test_the_coarse_interaction_orders_decay() -> None:
    """Mutation caught: claiming decay where the orders stay comparable."""
    model = build_reference_model()
    orders = dict(coarse_closure_residual(model, (1, 0, 1, 0, 1, 0)).order_magnitudes)
    assert orders[3] < orders[2] < orders[1]


def test_a_two_block_partition_cannot_carry_a_coarse_triple() -> None:
    """Mutation caught: asking for a three-body term where none is expressible."""
    model = build_reference_model()
    with pytest.raises(ValueError):
        coarse_closure_residual(model, (1, 0, 1, 0, 1, 0), ((1, 2, 3), (4, 5, 6)))


def test_the_against_direction_is_much_larger_than_the_coarse_one() -> None:
    """Mutation caught: conflating the two eliminations because both are nonzero.

    The comparison is on the dimensionless three-to-two ratio rather than on raw
    coefficients, whose gap is dominated by the difference in overall action
    scale between the two directions.
    """
    model = build_reference_model()
    coarse = coarse_closure_residual(model, (1, 0, 1, 0, 1, 0))
    against = model_closure_residual(model, (1, 0, 1, 0, 1, 0))
    against_ratios = []
    for block in against.blocks:
        action, _ = _block_action(model, (1, 0, 1, 0, 1, 0), block.block)
        decomposition = anchored_mobius_decompose(action, anchor=(0, 0, 0))
        _, pair = largest_k_body_coefficient(decomposition, 2)
        against_ratios.append(
            abs(block.largest_three_body_coefficient) / abs(float(pair))
        )
    assert min(against_ratios) > 0.10
    assert coarse.three_to_two_ratio < 0.02
