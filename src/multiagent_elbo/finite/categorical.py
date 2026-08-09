"""Positive finite categorical exponential families."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np

from multiagent_elbo.config import NumericsConfig

from .measures import ProbabilityMeasure


def _readonly(values: np.ndarray) -> np.ndarray:
    result = np.array(values, dtype=np.float64, copy=True, order="C")
    result.setflags(write=False)
    return result


def _ordered_labels(labels: Sequence[str]) -> tuple[str, ...]:
    ordered = tuple(labels)
    if len(ordered) < 2:
        raise ValueError("labels must contain at least two categories")
    if len(set(ordered)) != len(ordered):
        raise ValueError("labels must be unique")
    return ordered


@dataclass(frozen=True, init=False)
class CategoricalExponentialFamily:
    """A stable positive categorical family in natural coordinates."""

    labels: tuple[str, ...]
    base_logits: np.ndarray
    sufficient_statistics: np.ndarray
    numerics: NumericsConfig

    def __init__(
        self,
        labels: Sequence[str],
        base_logits: Sequence[float],
        sufficient_statistics: Sequence[Sequence[float]],
        numerics: NumericsConfig,
    ) -> None:
        ordered_labels = _ordered_labels(labels)
        logits = np.array(base_logits, dtype=np.float64, copy=True, order="C")
        statistics = np.array(
            sufficient_statistics, dtype=np.float64, copy=True, order="C"
        )
        if logits.shape != (len(ordered_labels),):
            raise ValueError("base_logits must have one entry per label")
        if statistics.ndim != 2 or statistics.shape[0] != len(ordered_labels):
            raise ValueError("sufficient_statistics must have one row per label")
        if statistics.shape[1] == 0:
            raise ValueError(
                "sufficient_statistics must contain at least one parameter"
            )
        if not np.all(np.isfinite(logits)):
            raise ValueError("base_logits must be finite")
        if not np.all(np.isfinite(statistics)):
            raise ValueError("sufficient_statistics must be finite")

        object.__setattr__(self, "labels", ordered_labels)
        object.__setattr__(self, "base_logits", _readonly(logits))
        object.__setattr__(self, "sufficient_statistics", _readonly(statistics))
        object.__setattr__(self, "numerics", numerics)

    @property
    def parameter_count(self) -> int:
        return int(self.sufficient_statistics.shape[1])

    def _theta(self, theta: Sequence[float]) -> np.ndarray:
        raw_values = np.asarray(theta, dtype=object)
        if any(isinstance(value, (bool, np.bool_)) for value in raw_values.flat):
            raise TypeError("theta must not contain Boolean values")
        values = np.array(theta, dtype=np.float64, copy=True, order="C")
        if values.shape != (self.parameter_count,):
            raise ValueError("theta must have one entry per parameter")
        if not np.all(np.isfinite(values)):
            raise ValueError("theta must be finite")
        return values

    def _log_probability_pair(
        self, theta: Sequence[float]
    ) -> tuple[np.ndarray, np.ndarray]:
        values = self._theta(theta)
        with np.errstate(over="ignore", invalid="ignore", under="ignore"):
            natural_term = self.sufficient_statistics @ values
            logits = self.base_logits + natural_term
        if not np.all(np.isfinite(natural_term)) or not np.all(np.isfinite(logits)):
            raise ValueError("nonfinite categorical matrix product or logits")

        maximum = float(np.max(logits))
        with np.errstate(over="ignore", invalid="ignore", under="ignore"):
            shifted = logits - maximum
            exponentials = np.exp(shifted)
            shifted_normalizer = float(np.sum(exponentials))
            log_probabilities = shifted - math.log(shifted_normalizer)
            probabilities = np.exp(log_probabilities)
        if not math.isfinite(shifted_normalizer) or shifted_normalizer <= 0.0:
            raise ValueError("nonfinite categorical normalization")
        if not np.all(np.isfinite(log_probabilities)) or not np.all(
            np.isfinite(probabilities)
        ):
            raise ValueError("nonfinite categorical probability result")
        if np.any(probabilities <= 0.0):
            raise ValueError("categorical probabilities must remain strictly positive")
        total = float(np.sum(probabilities))
        if not math.isclose(
            total, 1.0, rel_tol=self.numerics.rtol, abs_tol=self.numerics.atol
        ):
            raise ValueError("categorical probabilities must sum to one")
        return log_probabilities, probabilities

    def log_probabilities(self, theta: Sequence[float]) -> np.ndarray:
        log_probabilities, _ = self._log_probability_pair(theta)
        return _readonly(log_probabilities)

    def probabilities(self, theta: Sequence[float]) -> np.ndarray:
        _, probabilities = self._log_probability_pair(theta)
        return _readonly(probabilities)

    def probability_measure(self, theta: Sequence[float]) -> ProbabilityMeasure:
        return ProbabilityMeasure(self.labels, self.probabilities(theta), self.numerics)

    def score(self, theta: Sequence[float]) -> np.ndarray:
        probabilities = self.probabilities(theta)
        with np.errstate(over="ignore", invalid="ignore"):
            expected_statistics = probabilities @ self.sufficient_statistics
            score = self.sufficient_statistics - expected_statistics
        if not np.all(np.isfinite(score)):
            raise ValueError("nonfinite categorical score")
        return _readonly(score)

    def fisher_information(self, theta: Sequence[float]) -> np.ndarray:
        probabilities = self.probabilities(theta)
        score = self.score(theta)
        with np.errstate(over="ignore", invalid="ignore"):
            fisher = np.einsum("x,xi,xj->ij", probabilities, score, score)
        if not np.all(np.isfinite(fisher)):
            raise ValueError("nonfinite categorical Fisher information")
        return _readonly(fisher)
