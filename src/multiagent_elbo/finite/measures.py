"""Validated finite measures, Markov kernels, and evidence submeasures."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np

from multiagent_elbo.config import NumericsConfig


def _labels(labels: Sequence[str]) -> tuple[str, ...]:
    result = tuple(labels)
    if not result:
        raise ValueError("labels must be nonempty")
    if len(set(result)) != len(result):
        raise ValueError("labels must be unique")
    return result


def _masses(values: Sequence[float], length: int, name: str) -> np.ndarray:
    result = np.array(values, dtype=np.float64, copy=True, order="C")
    if result.ndim != 1 or result.shape[0] != length:
        raise ValueError(f"{name} must have one mass per label")
    if not np.all(np.isfinite(result)) or np.any(result < 0.0):
        raise ValueError(f"{name} must be finite nonnegative")
    result.setflags(write=False)
    return result


@dataclass(frozen=True, init=False)
class FiniteMeasure:
    """A finite nonnegative measure on an explicitly ordered finite support."""

    labels: tuple[str, ...]
    masses: np.ndarray
    numerics: NumericsConfig

    def __init__(
        self, labels: Sequence[str], masses: Sequence[float], numerics: NumericsConfig
    ) -> None:
        ordered_labels = _labels(labels)
        object.__setattr__(self, "labels", ordered_labels)
        object.__setattr__(self, "masses", _masses(masses, len(ordered_labels), "masses"))
        object.__setattr__(self, "numerics", numerics)

    @property
    def total_mass(self) -> float:
        return float(np.sum(self.masses))

    def pushforward(self, kernel: "MarkovKernel") -> "FiniteMeasure":
        """Push this measure forward by a row-stochastic finite channel."""
        if self.labels != kernel.source_labels:
            raise ValueError("measure labels must equal kernel source labels")
        return FiniteMeasure(kernel.target_labels, self.masses @ kernel.matrix, self.numerics)


@dataclass(frozen=True, init=False)
class ProbabilityMeasure(FiniteMeasure):
    """A finite measure with unit total mass to configured tolerance."""

    def __init__(
        self, labels: Sequence[str], masses: Sequence[float], numerics: NumericsConfig
    ) -> None:
        super().__init__(labels, masses, numerics)
        if not math.isclose(
            self.total_mass, 1.0, rel_tol=numerics.rtol, abs_tol=numerics.atol
        ):
            raise ValueError("probability masses must sum to one")

    def pushforward(self, kernel: "MarkovKernel") -> "ProbabilityMeasure":
        if self.labels != kernel.source_labels:
            raise ValueError("measure labels must equal kernel source labels")
        return ProbabilityMeasure(kernel.target_labels, self.masses @ kernel.matrix, self.numerics)


@dataclass(frozen=True, init=False)
class MarkovKernel:
    """A finite row-stochastic channel from source labels to target labels."""

    source_labels: tuple[str, ...]
    target_labels: tuple[str, ...]
    matrix: np.ndarray
    numerics: NumericsConfig

    def __init__(
        self,
        source_labels: Sequence[str],
        target_labels: Sequence[str],
        matrix: Sequence[Sequence[float]],
        numerics: NumericsConfig,
    ) -> None:
        source = _labels(source_labels)
        target = _labels(target_labels)
        values = np.array(matrix, dtype=np.float64, copy=True, order="C")
        if values.shape != (len(source), len(target)):
            raise ValueError("kernel matrix shape must match source and target labels")
        if not np.all(np.isfinite(values)) or np.any(values < 0.0):
            raise ValueError("kernel entries must be finite nonnegative")
        if not np.allclose(values.sum(axis=1), 1.0, rtol=numerics.rtol, atol=numerics.atol):
            raise ValueError("kernel row sums must equal one")
        values.setflags(write=False)
        object.__setattr__(self, "source_labels", source)
        object.__setattr__(self, "target_labels", target)
        object.__setattr__(self, "matrix", values)
        object.__setattr__(self, "numerics", numerics)


@dataclass(frozen=True)
class MeasurePair:
    """A reference probability and an unnormalized evidence submeasure m_o << rho."""

    reference: ProbabilityMeasure
    evidence_measure: FiniteMeasure

    def __post_init__(self) -> None:
        if self.reference.labels != self.evidence_measure.labels:
            raise ValueError("reference and evidence labels must match")
        outside_support = (self.evidence_measure.masses > 0.0) & (
            self.reference.masses == 0.0
        )
        if np.any(outside_support):
            raise ValueError("evidence measure must be absolutely continuous with reference")

    @property
    def evidence(self) -> float:
        return self.evidence_measure.total_mass

    def evidence_density(self) -> np.ndarray:
        """Return dm_o/drho, defined as zero on rho-null states."""
        density = np.zeros_like(self.reference.masses)
        np.divide(
            self.evidence_measure.masses,
            self.reference.masses,
            out=density,
            where=self.reference.masses > 0.0,
        )
        density.setflags(write=False)
        return density

    def posterior(self) -> ProbabilityMeasure:
        if not math.isfinite(self.evidence) or self.evidence <= 0.0:
            raise ValueError("posterior requires positive evidence")
        return ProbabilityMeasure(
            self.evidence_measure.labels,
            self.evidence_measure.masses / self.evidence,
            self.reference.numerics,
        )

    def pushforward(self, kernel: MarkovKernel) -> "MeasurePair":
        return MeasurePair(
            self.reference.pushforward(kernel), self.evidence_measure.pushforward(kernel)
        )
