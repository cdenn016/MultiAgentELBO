from __future__ import annotations

import math

import numpy as np
import pytest

from multiagent_elbo.config import NumericsConfig
from multiagent_elbo.finite.measures import (
    FiniteMeasure,
    MarkovKernel,
    MeasurePair,
    ProbabilityMeasure,
)
from multiagent_elbo.finite.vfe import (
    block_update_decomposition,
    free_energy,
    kl_divergence,
    vfe_channel_decomposition,
)


LABELS = ("00", "01", "10", "11")
NUMERICS = NumericsConfig(dtype="float64", atol=1e-12, rtol=1e-10)


def exact_pair() -> MeasurePair:
    return MeasurePair(
        ProbabilityMeasure(LABELS, (0.25, 0.25, 0.25, 0.25), NUMERICS),
        FiniteMeasure(LABELS, (0.2, 0.4, 0.6, 0.8), NUMERICS),
    )


def test_vfe_channel_decomposition_matches_the_finite_chain_rule():
    pair = exact_pair()
    q = ProbabilityMeasure(LABELS, (0.2, 0.3, 0.1, 0.4), NUMERICS)
    channel = MarkovKernel(
        LABELS,
        ("A", "B"),
        ((1.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, 1.0)),
        NUMERICS,
    )
    result = vfe_channel_decomposition(q, pair, channel)

    fine_kl = 0.2 * math.log(2.0) + 0.3 * math.log(1.5) + 0.1 * math.log(1.0 / 3.0)
    coarse_kl = 0.5 * math.log(5.0 / 3.0) + 0.5 * math.log(5.0 / 7.0)
    assert free_energy(q, pair) == pytest.approx(fine_kl - math.log(2.0))
    assert result.fine_vfe == pytest.approx(fine_kl - math.log(2.0))
    assert result.coarse_vfe == pytest.approx(coarse_kl - math.log(2.0))
    assert result.conditional_kl == pytest.approx(fine_kl - coarse_kl)
    assert result.residual == pytest.approx(0.0, abs=1e-12)


def test_support_violation_is_extended_real_without_an_inf_minus_inf_residual():
    pair = MeasurePair(
        ProbabilityMeasure(LABELS, (0.25, 0.25, 0.25, 0.25), NUMERICS),
        FiniteMeasure(LABELS, (0.2, 0.4, 0.6, 0.0), NUMERICS),
    )
    q = ProbabilityMeasure(LABELS, (0.0, 0.0, 0.0, 1.0), NUMERICS)
    identity = MarkovKernel(LABELS, LABELS, np.eye(4), NUMERICS)

    result = vfe_channel_decomposition(q, pair, identity)

    assert result.fine_vfe == math.inf
    assert result.offending_state == "11"
    assert result.residual is None


def test_recoverable_channel_has_zero_conditional_kl_and_ordinary_residual():
    pair = exact_pair()
    q = ProbabilityMeasure(LABELS, (0.2, 0.3, 0.1, 0.4), NUMERICS)
    identity = MarkovKernel(LABELS, LABELS, np.eye(4), NUMERICS)

    result = vfe_channel_decomposition(q, pair, identity)

    assert result.conditional_kl == pytest.approx(0.0, abs=1e-12)
    assert result.residual == pytest.approx(0.0, abs=1e-12)


def test_kl_with_smallest_positive_subnormal_support_is_finite():
    tiny = np.nextafter(0.0, 1.0)
    q = ProbabilityMeasure(("rare", "other"), (1.0, 0.0), NUMERICS)
    p = ProbabilityMeasure(("rare", "other"), (tiny, 1.0), NUMERICS)
    pair = MeasurePair(p, FiniteMeasure(p.labels, p.masses, NUMERICS))
    identity = MarkovKernel(p.labels, p.labels, np.eye(2), NUMERICS)

    divergence = kl_divergence(q, p)
    result = vfe_channel_decomposition(q, pair, identity)

    assert p.total_mass == 1.0
    assert p.masses[0] == tiny
    assert divergence == pytest.approx(-math.log(tiny))
    assert math.isfinite(divergence)
    assert math.isfinite(result.fine_vfe)
    assert result.offending_state is None


@pytest.mark.parametrize("invalid_argument", ["q", "p"])
def test_kl_requires_probability_measures_at_runtime(invalid_argument: str):
    probability = ProbabilityMeasure(("x", "y"), (0.5, 0.5), NUMERICS)
    merely_finite = FiniteMeasure(("x", "y"), (0.5, 0.5), NUMERICS)
    q, p = (
        (merely_finite, probability)
        if invalid_argument == "q"
        else (probability, merely_finite)
    )

    with pytest.raises(TypeError, match=f"{invalid_argument} must be a ProbabilityMeasure"):
        kl_divergence(q, p)  # type: ignore[arg-type]


def test_block_update_matches_collective_vfe_difference_with_fixed_outside_marginal():
    posterior = np.array([[0.10, 0.20], [0.30, 0.40]])
    q_before = np.array([[0.21, 0.13], [0.14, 0.52]])
    q_after = np.array([[0.14, 0.325], [0.21, 0.325]])

    result = block_update_decomposition(posterior, q_before, q_after, block_axes=(0,))

    posterior_conditionals = ((0.25, 0.75), (1.0 / 3.0, 2.0 / 3.0))
    before_conditionals = ((0.6, 0.4), (0.2, 0.8))
    after_conditionals = ((0.4, 0.6), (0.5, 0.5))
    outside = (0.35, 0.65)
    conditional_kl = lambda q, p: sum(value * math.log(value / target) for value, target in zip(q, p))
    expected = sum(
        weight * (conditional_kl(after, target) - conditional_kl(before, target))
        for weight, before, after, target in zip(
            outside, before_conditionals, after_conditionals, posterior_conditionals
        )
    )
    assert expected == pytest.approx(-0.06702325206172067)
    assert result.local_difference == pytest.approx(expected)
    assert result.collective_difference == pytest.approx(expected)
    assert result.residual == pytest.approx(0.0, abs=1e-12)


def test_block_update_requires_exactly_equal_outside_marginals():
    posterior = np.array([[0.10, 0.20], [0.30, 0.40]])
    q_before = np.array([[0.21, 0.13], [0.14, 0.52]])
    q_after = np.array([[0.15, 0.325], [0.21, 0.315]])

    with pytest.raises(ValueError, match="outside marginals"):
        block_update_decomposition(posterior, q_before, q_after, block_axes=(0,))


def test_block_update_supports_a_nonleading_block_axis():
    posterior = np.array([[0.10, 0.20], [0.30, 0.40]]).T
    q_before = np.array([[0.21, 0.13], [0.14, 0.52]]).T
    q_after = np.array([[0.14, 0.325], [0.21, 0.325]]).T

    result = block_update_decomposition(posterior, q_before, q_after, block_axes=(1,))

    assert result.local_difference == pytest.approx(-0.06702325206172067)
    assert result.collective_difference == pytest.approx(result.local_difference)
    assert result.residual == pytest.approx(0.0, abs=1e-12)


def test_block_update_supports_multiple_noncontiguous_block_axes():
    def table_from_block_outside(rows: list[list[float]]) -> np.ndarray:
        return np.asarray(rows).reshape(2, 2, 2).transpose(0, 2, 1)

    posterior = table_from_block_outside(
        [[0.125, 0.0625], [0.125, 0.125], [0.125, 0.125], [0.125, 0.1875]]
    )
    q_before = table_from_block_outside(
        [[0.125, 0.125], [0.0625, 0.125], [0.125, 0.125], [0.0625, 0.25]]
    )
    q_after = table_from_block_outside(
        [[0.0625, 0.25], [0.125, 0.125], [0.0625, 0.125], [0.125, 0.125]]
    )

    result = block_update_decomposition(
        posterior, q_before, q_after, block_axes=(0, 2)
    )

    assert result.outside_marginal.tolist() == pytest.approx([0.375, 0.625])
    assert result.collective_difference == pytest.approx(result.local_difference)
    assert result.residual == pytest.approx(0.0, abs=1e-12)
