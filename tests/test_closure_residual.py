"""Tests for the generated many-body terms and the declared closure residual."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

import pytest

from multiagent_elbo.finite.categorical_falsification_model import build_reference_model
from multiagent_elbo.finite.closure_residual import (
    declared_family_projection,
    flow_weighted_residual,
    ising_star_convergence_ratios,
    ising_star_leading_order,
    ising_star_three_body_coefficient,
    largest_k_body_coefficient,
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
