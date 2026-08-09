from __future__ import annotations

import numpy as np
import pytest

from multiagent_elbo.config import NumericsConfig
from multiagent_elbo.finite.measures import (
    FiniteMeasure,
    MarkovKernel,
    MeasurePair,
    ProbabilityMeasure,
)


LABELS = ("00", "01", "10", "11")
NUMERICS = NumericsConfig(dtype="float64", atol=1e-12, rtol=1e-10)


def test_pushforward_preserves_evidence_mass_and_computes_literal_densities():
    reference = ProbabilityMeasure(LABELS, (0.25, 0.25, 0.25, 0.25), NUMERICS)
    evidence = FiniteMeasure(LABELS, (0.2, 0.4, 0.6, 0.8), NUMERICS)
    pair = MeasurePair(reference, evidence)
    channel = MarkovKernel(
        LABELS,
        ("A", "B"),
        ((1.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, 1.0)),
        NUMERICS,
    )

    coarse_pair = pair.pushforward(channel)

    assert evidence.total_mass == pytest.approx(2.0)
    assert coarse_pair.evidence_measure.total_mass == pytest.approx(2.0)
    assert coarse_pair.reference.masses.tolist() == pytest.approx([0.5, 0.5])
    assert coarse_pair.evidence_measure.masses.tolist() == pytest.approx([0.6, 1.4])
    assert pair.evidence_density().tolist() == pytest.approx([0.8, 1.6, 2.4, 3.2])
    assert coarse_pair.evidence_density().tolist() == pytest.approx([1.2, 2.8])


def test_measure_pair_rejects_evidence_outside_reference_support():
    reference = ProbabilityMeasure(("present", "absent"), (1.0, 0.0), NUMERICS)
    evidence = FiniteMeasure(("present", "absent"), (0.5, 0.1), NUMERICS)

    with pytest.raises(ValueError, match="absolutely continuous"):
        MeasurePair(reference, evidence)


def test_non_row_stochastic_kernel_is_rejected():
    with pytest.raises(ValueError, match="row sums"):
        MarkovKernel(
            ("x", "y"),
            ("A", "B"),
            ((0.5, 0.5), (0.7, 0.7)),
            NUMERICS,
        )


def test_posterior_normalizes_positive_evidence_submeasure_and_refuses_zero_evidence():
    reference = ProbabilityMeasure(LABELS, (0.25, 0.25, 0.25, 0.25), NUMERICS)
    pair = MeasurePair(reference, FiniteMeasure(LABELS, (0.2, 0.4, 0.6, 0.8), NUMERICS))
    zero_pair = MeasurePair(reference, FiniteMeasure(LABELS, (0.0, 0.0, 0.0, 0.0), NUMERICS))

    assert pair.posterior().masses.tolist() == pytest.approx([0.1, 0.2, 0.3, 0.4])
    with pytest.raises(ValueError, match="positive evidence"):
        zero_pair.posterior()


def test_measure_labels_are_unique_and_masses_are_finite_nonnegative():
    with pytest.raises(ValueError, match="unique"):
        FiniteMeasure(("x", "x"), (0.2, 0.8), NUMERICS)
    with pytest.raises(ValueError, match="finite nonnegative"):
        FiniteMeasure(("x",), (np.nan,), NUMERICS)


def test_finite_measure_defensively_owns_its_validated_masses():
    masses = np.array([0.2, 0.8])
    measure = FiniteMeasure(("x", "y"), masses, NUMERICS)

    masses.setflags(write=True)
    masses[0] = 0.9

    assert measure.masses.tolist() == pytest.approx([0.2, 0.8])


def test_markov_kernel_defensively_owns_its_validated_matrix():
    matrix = np.eye(2)
    kernel = MarkovKernel(("x", "y"), ("x", "y"), matrix, NUMERICS)

    matrix.setflags(write=True)
    matrix[0, 0] = 0.3

    assert np.array_equal(kernel.matrix, np.eye(2))
