"""Measurement M1: the depth-one tower free energy computed two independent ways."""

from __future__ import annotations

import math

import numpy as np

from multiagent_elbo.finite.categorical_falsification_model import build_reduced_model
from multiagent_elbo.finite.tower_vfe import (
    decomposed_tower_free_energy,
    flat_tower_free_energy,
    flat_tower_joint,
    naive_local_potential_sum,
    posterior_tower_recognition,
    seeded_tower_recognition,
    tower_accounting_residual,
    tower_observation_records,
)

RECORDS = ((0, 0, 0), (1, 0, 1), (1, 1, 0))
SEEDS = (11, 4243)


def test_the_flat_route_and_the_decomposed_route_agree_below_the_declared_falsifier() -> None:
    model = build_reduced_model()
    residuals = []
    for record in RECORDS:
        for seed in SEEDS:
            recognition = seeded_tower_recognition(model, record, seed)
            flat = flat_tower_free_energy(model, record, recognition)
            decomposed = decomposed_tower_free_energy(model, record, recognition)
            residual = tower_accounting_residual(model, record, recognition)
            assert math.isfinite(flat)
            assert residual == abs(flat - decomposed.total)
            residuals.append(residual)
    assert max(residuals) < 1e-12


def test_the_flat_tower_joint_normalizes_over_every_record_and_tower_state() -> None:
    model = build_reduced_model()
    records = tower_observation_records(model)

    assert len(records) == 2 ** len(model.agents)
    joint = flat_tower_joint(model, records[0])
    assert joint.shape == (81, 4, 2, 2, 729)
    assert joint.size == 944_784
    total = sum(float(flat_tower_joint(model, record).sum()) for record in records)

    assert abs(total - 1.0) < 1e-12


def test_the_recognition_gap_is_nonnegative_and_vanishes_at_the_exact_tower_posterior() -> None:
    model = build_reduced_model()
    for record in RECORDS:
        evidence = float(flat_tower_joint(model, record).sum())
        log_evidence = math.log(evidence)
        for seed in SEEDS:
            recognition = seeded_tower_recognition(model, record, seed)
            gap = flat_tower_free_energy(model, record, recognition) + log_evidence
            assert gap >= 0.0
        exact = posterior_tower_recognition(model, record)
        free_energy = flat_tower_free_energy(model, record, exact)

        assert abs(free_energy + log_evidence) < 1e-12
        assert abs(free_energy - (-log_evidence)) < 1e-12


def test_every_decomposition_group_except_the_observation_term_is_nonnegative() -> None:
    model = build_reduced_model()
    for record in RECORDS:
        for seed in SEEDS:
            recognition = seeded_tower_recognition(model, record, seed)
            decomposed = decomposed_tower_free_energy(model, record, recognition)
            groups = (
                decomposed.top_prior_term,
                decomposed.partition_term,
                decomposed.row_term,
                decomposed.holonomy_term,
                decomposed.cross_scale_term,
            )
            for group in groups:
                assert group >= 0.0
            assert abs(decomposed.total - (decomposed.observation_term + sum(groups))) < 1e-12


def test_the_observation_term_is_finite_under_the_declared_likelihood() -> None:
    model = build_reduced_model()
    table = model.likelihood_table()

    assert np.all(table > 0.0)
    assert np.all(table < 1.0)
    for record in RECORDS:
        for seed in SEEDS:
            recognition = seeded_tower_recognition(model, record, seed)
            decomposed = decomposed_tower_free_energy(model, record, recognition)

            assert math.isfinite(decomposed.observation_term)


def test_the_naive_local_potential_sum_is_not_the_free_energy_and_overcounts_every_edge() -> None:
    model = build_reduced_model()
    for record in RECORDS:
        for seed in SEEDS:
            recognition = seeded_tower_recognition(model, record, seed)
            naive_sum, overcount = naive_local_potential_sum(model, record, recognition)
            free_energy = flat_tower_free_energy(model, record, recognition)

            assert overcount > 0.0
            assert abs(naive_sum - 2.0 * overcount) < 1e-12
            assert abs(naive_sum - free_energy) > 1e-6


def test_the_recognition_tower_is_correlated_rather_than_a_product_of_its_marginals() -> None:
    model = build_reduced_model()
    recognition = seeded_tower_recognition(model, RECORDS[1], SEEDS[0])
    joint = recognition.top
    for factor in (
        recognition.partition,
        recognition.rows,
        recognition.holonomy,
        recognition.child,
    ):
        joint = joint[..., np.newaxis] * factor

    assert abs(float(joint.sum()) - 1.0) < 1e-12
    product = np.ones_like(joint)
    for axis in range(joint.ndim):
        marginal = joint.sum(axis=tuple(a for a in range(joint.ndim) if a != axis))
        shape = [1] * joint.ndim
        shape[axis] = joint.shape[axis]
        product = product * marginal.reshape(shape)

    assert float(np.abs(joint - product).sum()) > 1e-3
