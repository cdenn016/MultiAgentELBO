"""Tests for measurement M5, partition persistence on the finite categorical instance."""

from __future__ import annotations

import math
from itertools import product

import numpy as np

from multiagent_elbo.finite.categorical_falsification_model import (
    build_reduced_model,
    build_reference_model,
    crp_partition_prior,
)
from multiagent_elbo.finite.partition_dynamics import (
    block_energy,
    belief_relaxation_time,
    co_membership_matrix,
    coupled_descent,
    downward_law,
    energy_terms,
    ensemble_residence_times,
    exit_time_scaling,
    modal_partition,
    null_control_comparison,
    partition_log_normalizer,
    partition_posterior,
    residence_times,
)

REFERENCE_STATES = (0, 1, 2, 0, 1, 2)


def test_the_partition_posterior_is_normalized_over_the_candidate_partitions() -> None:
    model = build_reference_model()
    law = partition_posterior(model, REFERENCE_STATES)
    assert set(law) == set(model.candidate_partitions)
    assert math.isclose(sum(law.values()), 1.0, rel_tol=0.0, abs_tol=1e-12)
    assert all(value > 0.0 for value in law.values())


def test_the_partition_posterior_matches_the_negative_log_normalizer() -> None:
    model = build_reference_model()
    law = partition_posterior(model, REFERENCE_STATES)
    minimum = partition_log_normalizer(model, REFERENCE_STATES)
    for partition, mass in law.items():
        prior = float(crp_partition_prior(partition, model.crp_concentration))
        energy = block_energy(model, partition, REFERENCE_STATES)
        assert math.isclose(
            math.log(mass),
            math.log(prior) - energy + minimum,
            rel_tol=0.0,
            abs_tol=1e-10,
        )


def test_the_derived_block_energy_is_finite_and_nonnegative_on_every_candidate() -> None:
    model = build_reference_model()
    for partition in model.candidate_partitions:
        terms = energy_terms(model, partition, REFERENCE_STATES)
        assert math.isfinite(terms.total)
        assert terms.total >= 0.0
        assert terms.graph_divergence >= 0.0
        assert terms.holonomy_divergence == 0.0
        assert terms.cross_scale_divergence >= 0.0
        assert math.isclose(
            terms.total,
            terms.graph_divergence + terms.holonomy_divergence + terms.cross_scale_divergence,
            rel_tol=0.0,
            abs_tol=1e-12,
        )


def test_the_derived_block_energy_is_dominated_by_the_cross_scale_group() -> None:
    model = build_reference_model()
    for partition in model.candidate_partitions:
        terms = energy_terms(model, partition, REFERENCE_STATES)
        assert terms.cross_scale_divergence > terms.graph_divergence


def test_the_exposed_downward_law_reproduces_the_declared_kernel() -> None:
    model = build_reference_model()
    block = (1, 2, 3)
    for agent in block:
        for parent in range(model.state_count):
            declared = model.downward_kernel(block, agent, parent)
            exposed = downward_law(model, block, agent, parent, False)
            assert np.allclose(declared, exposed, rtol=0.0, atol=1e-15)


def test_the_metropolis_chain_approximately_preserves_the_target_law() -> None:
    model = build_reduced_model()
    weights: list[float] = []
    for partition in model.candidate_partitions:
        energies = np.array(
            [
                -block_energy(model, partition, states)
                for states in product(range(model.state_count), repeat=len(model.agents))
            ],
            dtype=np.float64,
        )
        peak = float(energies.max())
        prior = float(crp_partition_prior(partition, model.crp_concentration))
        weights.append(math.log(prior) + peak + math.log(float(np.exp(energies - peak).sum())))
    exact = np.exp(np.array(weights) - max(weights))
    exact = exact / exact.sum()
    trace = coupled_descent(model, 7, 1.0, 4000)
    empirical = np.array(
        [
            sum(1 for step in trace.partitions if step == partition) / len(trace.partitions)
            for partition in model.candidate_partitions
        ],
        dtype=np.float64,
    )
    assert 0.5 * float(np.abs(empirical - exact).sum()) < 0.08


def test_the_residence_times_of_a_visited_partition_are_positive() -> None:
    model = build_reference_model()
    trace = coupled_descent(model, 3, 1.0, 200)
    single = residence_times(trace)
    pooled = ensemble_residence_times([trace, coupled_descent(model, 4, 1.0, 200)])
    assert single
    assert all(value >= 1.0 for value in single.values())
    assert all(value >= 1.0 for value in pooled.values())
    assert modal_partition([trace]) in single


def test_the_co_membership_matrix_is_a_frequency_matrix_with_unit_diagonal() -> None:
    model = build_reference_model()
    traces = [coupled_descent(model, seed, 1.0, 120) for seed in range(3)]
    matrix = co_membership_matrix(traces)
    assert matrix.shape == (len(model.agents), len(model.agents))
    assert np.allclose(np.diag(matrix), 1.0, rtol=0.0, atol=1e-12)
    assert matrix.min() >= 0.0 and matrix.max() <= 1.0
    assert np.allclose(matrix, matrix.T, rtol=0.0, atol=1e-12)


def test_the_measured_relaxation_time_is_a_positive_number_of_steps() -> None:
    model = build_reference_model()
    measured = belief_relaxation_time(model, 5, 1.0, 32, 40)
    assert type(measured) is float
    assert 1.0 <= measured <= 40.0


def test_the_exit_time_fit_reports_its_own_coefficient_of_determination() -> None:
    model = build_reference_model()
    fit = exit_time_scaling(
        model,
        (11, 12, 13),
        (0.8, 1.2),
        40,
        model.candidate_partitions[0],
    )
    assert fit.partition == model.candidate_partitions[0]
    assert len(fit.mean_exit_times) == 2
    assert all(value >= 1.0 for value in fit.mean_exit_times)
    assert all(0.0 <= value <= 1.0 for value in fit.censored_fraction)
    assert math.isfinite(fit.slope) and math.isfinite(fit.intercept)
    assert 0.0 <= fit.r_squared <= 1.0 + 1e-12
    assert type(fit.linearity_falsifier_fired) is bool


def test_the_null_control_returns_a_distribution_rather_than_a_point() -> None:
    report = null_control_comparison((101, 102, 103), 1.0, 60, 6)
    assert report.reference.model_name == "reference"
    assert len(report.nulls) == 3
    assert len(report.null_maximum_residence_time) == 3
    assert len(report.null_modal_occupancy) == 3
    assert len(report.null_residence_ratio) == 3
    assert len(set(report.null_maximum_residence_time)) > 1
    assert all(name.startswith("null-") for name in (item.model_name for item in report.nulls))
