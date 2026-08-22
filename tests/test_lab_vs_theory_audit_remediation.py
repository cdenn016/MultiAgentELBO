"""Regression tests for the 2026-08-18 lab-versus-theory audit punch list.

Each test pins one repaired behavior against the number the audit's verifier
derived independently, so a regression is caught as a wrong number rather than as
a silently different reading.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

import numpy as np
import pytest

from multiagent_elbo.finite.closure_residual import (
    _blocked_action,
    _declared_parent_prior,
)
from multiagent_elbo.finite.cocycle_flow import (
    MI_CEILING_FLOOR,
    capacity_information_retention,
    consecutive_blocks,
    homogeneous_circulant_instance,
    one_step_pair_retention,
)
from multiagent_elbo.finite.coupling_readback import (
    DECLARED_CONCENTRATION,
    PairwiseCouplings,
    PairwiseInstance,
    _kernel_model,
    anchor_swept_sup,
    couplings_action,
    initial_step,
    mobius_couplings,
)
from multiagent_elbo.finite.nested_tower import build_tower_model, tower_blocks
from multiagent_elbo.finite.participatory_blocking import (
    blocking_posterior,
    concentration_surface,
)
from multiagent_elbo.finite.partition_dynamics import (
    _evaluate_batch,
    _parent_state_energy,
    _partition_tables,
)
from multiagent_elbo.finite.rescaling import (
    _generates_full_lattice,
    check_wilson_charge_conservation,
    gauge_transformed_model,
    state_shift_permutation,
)
from multiagent_elbo.finite.tower_vfe import PARENT_STATE_WEIGHTS


@pytest.fixture(scope="module")
def declared_seed():
    """Return the validated C(3, 3) working-case site and pair tables."""
    tower = build_tower_model(
        3,
        3,
        (1, 1, 0, 1, 1, 1, 0, 2, 1, 1, 2, 0),
        (1, 1, 1, 2, 2, 2, 0, 1, 2, 0, 1, 2),
    )
    step = initial_step(tower, (1, 0, 1, 0, 1, 0, 1, 0, 1), tower_blocks(3, 3))
    site = step.variational.sites[0]
    pair = dict(step.variational.pairs)[(0, 1)]
    assert max(abs(float(v)) for v in site) == pytest.approx(1.432150, abs=1.0e-6)
    assert max(
        abs(float(v)) for row in pair for v in row
    ) == pytest.approx(0.016265, abs=1.0e-6)
    return site, pair


@pytest.fixture(scope="module")
def k1_instance(declared_seed):
    site, pair = declared_seed
    return homogeneous_circulant_instance(6, (1,), site, pair)


# ---------------------------------------------------------------- punch list 1


def test_the_block_energy_charges_the_declared_top_prior_for_each_parent(k1_instance):
    """Mutation caught: reverting to a parent that costs nothing to open."""
    model = _kernel_model(k1_instance.graph, "audit-regression")
    energy = _parent_state_energy(model)

    expected = -np.log(np.array([float(w) for w in PARENT_STATE_WEIGHTS]))
    assert energy == pytest.approx(expected)
    assert energy.min() > 0.0


def test_singletons_are_no_longer_the_free_minimizer_of_the_cross_scale_group(
    k1_instance,
):
    """Mutation caught: dropping the parent charge and restoring the free minimum.

    With an unpriced parent the per-block minimum decomposes agent by agent, so
    the all-singleton partition minimizes the cross-scale group at every
    configuration by construction. Priced, the direct block is cheaper here.
    """
    model = _kernel_model(k1_instance.graph, "audit-regression")
    states = np.array([[0, 3, 1, 8, 2, 5]], dtype=np.int64)
    singletons = _partition_tables(model, tuple((site,) for site in range(1, 7)))
    direct = _partition_tables(model, ((1, 2, 3, 4, 5, 6),))

    singleton_cross, _, _ = _evaluate_batch(singletons, states)
    direct_cross, _, _ = _evaluate_batch(direct, states)

    assert float(direct_cross[0]) < float(singleton_cross[0])


def test_the_partition_posterior_selects_the_direct_block_at_the_declared_seed(
    k1_instance,
):
    """Mutation caught: republishing the retired unpriced-parent verdict."""
    posterior = blocking_posterior(k1_instance)
    masses = dict(posterior.class_masses)

    assert posterior.modal_ratio == 6
    assert masses[6] == pytest.approx(0.958252, abs=1.0e-6)
    assert masses[1] == pytest.approx(0.000112, abs=1.0e-6)


# ---------------------------------------------------------------- punch list 2


def test_no_coupling_scale_moves_the_block_energy_landscape(declared_seed):
    """Mutation caught: reading an M-bind coupling sweep as a landscape sweep.

    The kernel model carries level-invariant declared structure and not the
    instance's couplings, so U(R, x) is identical across coupling scales and a
    sweep acts only through the flow. Making that structural fact a test keeps it
    from being rediscovered as a measured absence of a transition.
    """
    site, pair = declared_seed
    scaled = tuple(tuple(v * Fraction(100) for v in row) for row in pair)
    weak = homogeneous_circulant_instance(6, (1,), site, pair)
    strong = homogeneous_circulant_instance(6, (1,), site, scaled)
    states = np.array(
        [[0, 3, 1, 8, 2, 5], [4, 4, 4, 4, 4, 4], [8, 0, 7, 1, 6, 2]], dtype=np.int64
    )
    partition = ((1, 2), (3, 4), (5, 6))

    weak_tables = _partition_tables(_kernel_model(weak.graph, "weak"), partition)
    strong_tables = _partition_tables(_kernel_model(strong.graph, "strong"), partition)
    weak_cross, weak_graph, _ = _evaluate_batch(weak_tables, states)
    strong_cross, strong_graph, _ = _evaluate_batch(strong_tables, states)

    assert np.array_equal(weak_cross + weak_graph, strong_cross + strong_graph)


# ---------------------------------------------------------------- punch list 3


def test_a_same_cardinality_non_charge_readout_beats_the_gauge_charge(k1_instance):
    """Mutation caught: reading the sector gain as evidence about the charge.

    The enlarged label is a deterministic refinement, so a gain is a data
    processing theorem for any readout. The operative control carries the same
    number of labels and no gauge charge, and it gains far more.
    """
    nine = capacity_information_retention(k1_instance, 2, sector_count=1).retention
    charge = capacity_information_retention(k1_instance, 2, sector_count=3).retention
    control = capacity_information_retention(
        k1_instance, 2, sector_count=3, readout="first_member"
    ).retention

    assert charge / nine - 1.0 == pytest.approx(0.1016, abs=5.0e-4)
    assert control / nine - 1.0 == pytest.approx(0.6743, abs=5.0e-4)
    assert control > charge


def test_every_declared_readout_can_only_raise_the_information_retention(k1_instance):
    """Mutation caught: presenting the sign of a sector gain as a measurement."""
    nine = capacity_information_retention(k1_instance, 2, sector_count=1).retention
    for readout in ("charge", "first_member"):
        enlarged = capacity_information_retention(
            k1_instance, 2, sector_count=3, readout=readout
        ).retention
        assert enlarged >= nine


def test_an_undeclared_sector_readout_is_refused(k1_instance):
    with pytest.raises(ValueError, match="readout must be one of"):
        capacity_information_retention(k1_instance, 2, readout="whatever")


# ---------------------------------------------------------------- punch list 4


def test_the_wilson_charge_check_spans_the_fine_cycle_lattice():
    """Mutation caught: falling back to the Euler-identity rank comparison."""
    tower = build_tower_model(
        3,
        3,
        (1, 1, 0, 1, 1, 1, 0, 2, 1, 1, 2, 0),
        (1, 1, 1, 2, 2, 2, 0, 1, 2, 0, 1, 2),
    )
    report = check_wilson_charge_conservation(tower, tower_blocks(3, 3))

    assert report.spans is True
    assert report.passes is True
    assert report.lattice_columns == report.fine_rank


@pytest.mark.parametrize(
    ("rows", "columns", "expected"),
    [
        (((1, 0), (0, 1)), 2, True),
        (((1, 1), (0, 1), (1, 2)), 2, True),
        (((2, 0), (0, 1)), 2, False),
        (((1, 0), (2, 0)), 2, False),
        (((1, 0, 0), (0, 1, 0)), 3, False),
    ],
)
def test_the_lattice_span_refuses_sublattices_and_rank_deficiency(
    rows, columns, expected
):
    """Mutation caught: accepting a finite-index sublattice as full conservation."""
    assert _generates_full_lattice(rows, columns) is expected


# ---------------------------------------------------------------- punch list 6


def test_threading_the_parent_prior_makes_the_retention_gauge_invariant(k1_instance):
    """Mutation caught: dropping parent_priors and calling the result invariant.

    A gauge transformation moves the graph, the matter, and the parent law
    together. Left fixed, the parent law drags the statistic; re-expressed at each
    root, the statistic returns to its bare value.
    """
    model = _kernel_model(k1_instance.graph, "gauge-probe")
    base_prior = _declared_parent_prior(model.state_count)
    roots = [min(block) for block in consecutive_blocks(6, 2)]
    bare = capacity_information_retention(k1_instance, 2, sector_count=3).retention

    shifts = {1: 1, 2: 2, 3: 1, 4: 0, 5: 2, 6: 1}
    gauged_model = gauge_transformed_model(model, shifts)
    sigma = {v: state_shift_permutation(model, shifts[v]) for v in model.agents}
    inverse = [
        tuple(sorted(range(len(sigma[v])), key=sigma[v].__getitem__)) for v in model.agents
    ]
    couplings = k1_instance.couplings
    moved = PairwiseCouplings(
        width=couplings.width,
        constant=couplings.constant,
        sites=tuple(
            tuple(table[inverse[position][state]] for state in range(len(table)))
            for position, table in enumerate(couplings.sites)
        ),
        pairs=tuple(
            (
                (left, right),
                tuple(
                    tuple(
                        table[inverse[left][a]][inverse[right][b]]
                        for b in range(len(table))
                    )
                    for a in range(len(table))
                ),
            )
            for (left, right), table in couplings.pairs
        ),
    )
    gauged = PairwiseInstance(graph=gauged_model.graph, couplings=moved)
    priors = {}
    for root in roots:
        law = [0.0] * len(base_prior)
        for state, weight in enumerate(base_prior):
            law[sigma[root][state]] = weight
        priors[root] = tuple(law)

    untied = capacity_information_retention(gauged, 2, sector_count=3).retention
    tied = capacity_information_retention(
        gauged, 2, sector_count=3, parent_priors=priors
    ).retention

    assert tied == pytest.approx(bare, rel=1.0e-7)
    assert abs(untied - bare) / bare > 1.0e-3


# ---------------------------------------------------------------- punch list 7


def test_the_mobius_anchor_is_reachable_and_moves_the_sup_norm(k1_instance):
    """Mutation caught: re-pinning the anchor and reporting a gauge-fixed sup."""
    blocks = consecutive_blocks(6, 2)
    model = _kernel_model(k1_instance.graph, "anchor-probe")
    array = couplings_action(k1_instance.couplings)
    action, _ = _blocked_action(model, np.exp(-(array - array.min())), blocks)
    admitted = ((0, 1), (0, 2), (1, 2))
    fine_sup = max(
        abs(float(value))
        for _, table in k1_instance.couplings.pairs
        for row in table
        for value in row
    )

    pinned, _ = mobius_couplings(action, admitted)
    shifted, _ = mobius_couplings(action, admitted, (1, 1, 1))
    measure = lambda c: max(
        abs(float(v)) for _, table in c.pairs for row in table for v in row
    )

    assert measure(pinned) / fine_sup == pytest.approx(0.155747, abs=1.0e-6)
    assert measure(shifted) / fine_sup == pytest.approx(0.129497, abs=1.0e-6)


def test_the_anchor_sweep_reports_the_range_beside_the_pinned_value(k1_instance):
    """Mutation caught: publishing an anchored sup without its anchor range."""
    blocks = consecutive_blocks(6, 2)
    model = _kernel_model(k1_instance.graph, "anchor-sweep")
    array = couplings_action(k1_instance.couplings)
    action, _ = _blocked_action(model, np.exp(-(array - array.min())), blocks)
    admitted = ((0, 1), (0, 2), (1, 2))
    anchors = tuple(product(range(model.state_count), repeat=3))

    sweep = anchor_swept_sup(action, admitted, anchors, block="pair")

    assert sweep.pinned_anchor == (0, 0, 0)
    assert sweep.swept_count == 729
    assert sweep.minimum_value < sweep.pinned_value < sweep.maximum_value
    assert sweep.relative_range == pytest.approx(0.37154, abs=1.0e-4)


# ---------------------------------------------------------------- punch list 8


def test_the_partition_verdict_is_a_surface_in_the_ewens_concentration(k1_instance):
    """Mutation caught: hardwiring the concentration and reporting one point."""
    grid = (Fraction(1), Fraction(5), Fraction(7), Fraction(10))
    surface = concentration_surface(k1_instance, grid)

    assert surface.modal_ratios == (6, 6, 1, 1)
    assert len(surface.crossings) == 1
    assert surface.crossings[0][2:] == (6, 1)


def test_the_declared_concentration_is_the_default_and_is_recorded(k1_instance):
    posterior = blocking_posterior(k1_instance)
    assert posterior.concentration == DECLARED_CONCENTRATION
    assert blocking_posterior(k1_instance, Fraction(10)).concentration == Fraction(10)


# ---------------------------------------------------------------- punch list 9


def test_a_roundoff_scale_information_ceiling_raises_instead_of_dividing(declared_seed):
    """Mutation caught: reporting a retention ratio of two roundoff residues."""
    site, pair = declared_seed
    flat = tuple(tuple(v * Fraction(0) for v in row) for row in pair)
    instance = homogeneous_circulant_instance(6, (1,), site, flat)

    with pytest.raises(ValueError, match="roundoff scale"):
        capacity_information_retention(instance, 2, sector_count=1)


def test_the_declared_instances_sit_far_above_the_ceiling_floor(k1_instance):
    ceiling = capacity_information_retention(
        k1_instance, 2, sector_count=1
    ).fine_information
    assert ceiling > MI_CEILING_FLOOR * 1.0e3


def test_the_published_retentions_are_unchanged_by_the_remediation(k1_instance):
    """Mutation caught: moving a number the audit reproduced and cleared."""
    assert one_step_pair_retention(k1_instance, 2).retention == pytest.approx(
        0.15574727, abs=1.0e-8
    )
    assert capacity_information_retention(
        k1_instance, 2, sector_count=1
    ).retention == pytest.approx(0.023012, abs=1.0e-6)
