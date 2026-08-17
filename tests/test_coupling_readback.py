"""Tests for the coupling read-back routes, the closed step, C3 and C4."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

import pytest

from multiagent_elbo.finite.coupling_readback import (
    PROJECTION_AGREEMENT_TOLERANCE,
    check_compatibility,
    couplings_action,
    initial_step,
    iterated_step,
    mobius_couplings,
    moment_matching_diagnostic,
    projection_agreement,
    variational_couplings,
)
from multiagent_elbo.finite.nested_tower import reference_tower, tower_blocks
from multiagent_elbo.finite.rescaling import coarse_action

OBSERVATION = (1, 0, 1, 0, 1, 0)
TRIANGLE_PAIRS = ((0, 1), (1, 2), (0, 2))


def planted_action(size: int, triple: Fraction):
    """Return a three-site action with declared site, pair, and triple terms."""
    action = {}
    for state in product(range(size), repeat=3):
        value = Fraction(7, 13)
        value += Fraction(1, 3) * state[0] + Fraction(1, 5) * state[2]
        value += Fraction(2, 7) * state[0] * state[1]
        value += Fraction(1, 9) * state[1] * state[2]
        value += triple * state[0] * state[1] * state[2]
        action[state] = value
    return action


def test_the_moebius_route_recovers_a_planted_pairwise_action_exactly() -> None:
    action = planted_action(3, Fraction(0))
    couplings, omitted = mobius_couplings(action, TRIANGLE_PAIRS)
    assert omitted == Fraction(0)
    assert couplings.constant == Fraction(7, 13)
    assert couplings.sites[0] == (Fraction(0), Fraction(1, 3), Fraction(2, 3))
    assert dict(couplings.pairs)[(0, 1)][1][1] == Fraction(2, 7)
    assert dict(couplings.pairs)[(0, 2)][2][2] == Fraction(0)


def test_the_variational_route_agrees_with_the_seed_on_a_pairwise_action() -> None:
    action = planted_action(3, Fraction(0))
    seed, _ = mobius_couplings(action, TRIANGLE_PAIRS)
    fitted, report = variational_couplings(action, TRIANGLE_PAIRS, seed)
    assert report.converged
    assert report.kl_projected <= 1.0e-12
    assert projection_agreement(fitted, seed) <= 1.0e-9


def test_the_variational_route_improves_on_the_seed_under_a_planted_triple() -> None:
    action = planted_action(3, Fraction(1, 2))
    seed, omitted = mobius_couplings(action, TRIANGLE_PAIRS)
    assert omitted > 0
    fitted, report = variational_couplings(action, TRIANGLE_PAIRS, seed)
    assert report.converged
    assert report.kl_projected < report.kl_seed
    assert report.family_leakage <= 1.0e-9


def test_the_reference_step_is_lossless_and_resolved_at_two_parents() -> None:
    tower = reference_tower()
    step = initial_step(tower, OBSERVATION, tower_blocks(2, 3))
    assert step.mobius_omitted_sup == Fraction(0)
    assert step.projection_ratio <= 1.0e-9
    assert step.resolved
    assert step.instance is not None
    assert step.instance.graph == step.connection.graph
    action, _ = coarse_action(tower, OBSERVATION, tower_blocks(2, 3))
    assert step.action == action


def test_the_reconstructed_coupling_action_matches_the_coarse_action() -> None:
    tower = reference_tower()
    step = initial_step(tower, OBSERVATION, tower_blocks(2, 3))
    rebuilt = couplings_action(step.mobius)
    for state, value in step.action.items():
        assert abs(float(value) - float(rebuilt[state])) <= 1.0e-12


def test_the_iterated_step_reaches_a_single_site_coupling_vector() -> None:
    tower = reference_tower()
    step = initial_step(tower, OBSERVATION, tower_blocks(2, 3))
    final = iterated_step(step.instance, ((1, 2),))
    assert final.connection is None
    assert final.instance is None
    assert final.mobius.width == 1
    assert final.mobius.pairs == ()
    assert final.projection_ratio == 0.0


def test_c3_is_deterministic_and_reports_the_reverse_ordering_as_not_performed() -> None:
    tower = reference_tower()
    first = check_compatibility(tower, OBSERVATION, tower_blocks(2, 3))
    second = check_compatibility(tower, OBSERVATION, tower_blocks(2, 3))
    assert first.deviation == second.deviation
    assert first.direct_sites == second.direct_sites
    assert first.route_c_status.startswith("not performed")
    assert first.deviation >= 0.0
    assert first.intermediate.resolved


def test_the_moment_diagnostic_is_clean_on_the_lossless_reference_step() -> None:
    tower = reference_tower()
    step = initial_step(tower, OBSERVATION, tower_blocks(2, 3))
    diagnostic = moment_matching_diagnostic(step)
    assert diagnostic.holonomy_matched
    assert dict(diagnostic.coarse_elements)["belief"] == (0, 2)
    for _, _, _, variational_dev, mobius_dev in diagnostic.divergence_rows:
        assert variational_dev <= 1.0e-9
        assert mobius_dev <= 1.0e-9
    for _, variational_dev, mobius_dev in diagnostic.occupancy_rows:
        assert variational_dev <= 1.0e-9
        assert mobius_dev <= 1.0e-9


def test_projection_agreement_rejects_mismatched_pairwise_blocks() -> None:
    action = planted_action(3, Fraction(0))
    full, _ = mobius_couplings(action, TRIANGLE_PAIRS)
    partial, _ = mobius_couplings(action, ((0, 1),))
    with pytest.raises(ValueError):
        projection_agreement(full, partial)


def test_the_initial_step_rejects_a_blocking_that_drops_an_agent() -> None:
    tower = reference_tower()
    with pytest.raises(ValueError):
        initial_step(tower, OBSERVATION, ((1, 2, 3), (4, 5)))


def test_c4_threshold_is_the_declared_constant() -> None:
    assert PROJECTION_AGREEMENT_TOLERANCE == 0.05
