"""Finite-difference diagnostics for positive categorical families."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Literal, Sequence

import numpy as np

from .categorical import CategoricalExponentialFamily
from .fisher import FisherChannelResult, fisher_channel_decomposition
from .measures import MarkovKernel, ProbabilityMeasure


FamilyDqmScope = Literal["finite_positive_smooth_exponential_family"]
FixedChannelScope = Literal["declared_fixed_parameter_independent"]


def _readonly(values: np.ndarray) -> np.ndarray:
    result = np.array(values, dtype=np.float64, copy=True, order="C")
    result.setflags(write=False)
    return result


def _validated_family(family: object) -> CategoricalExponentialFamily:
    if not isinstance(family, CategoricalExponentialFamily):
        raise TypeError("family must be a CategoricalExponentialFamily")
    return family


@dataclass(frozen=True, init=False)
class DqmRemainderLadder:
    """Two-sided normalized square-root-likelihood DQM remainders."""

    step_sizes: np.ndarray
    positive: np.ndarray
    negative: np.ndarray

    def __init__(
        self,
        step_sizes: Sequence[float],
        positive: Sequence[float],
        negative: Sequence[float],
    ) -> None:
        steps = _readonly(np.asarray(step_sizes))
        positive_values = _readonly(np.asarray(positive))
        negative_values = _readonly(np.asarray(negative))
        if steps.ndim != 1 or steps.shape[0] == 0:
            raise ValueError("DQM step_sizes must be a nonempty vector")
        if (
            positive_values.shape != steps.shape
            or negative_values.shape != steps.shape
        ):
            raise ValueError("DQM remainder vectors must match step_sizes")
        if not all(
            np.all(np.isfinite(values))
            for values in (steps, positive_values, negative_values)
        ):
            raise ValueError("DQM ladder values must be finite")
        object.__setattr__(self, "step_sizes", steps)
        object.__setattr__(self, "positive", positive_values)
        object.__setattr__(self, "negative", negative_values)


@dataclass(frozen=True, init=False)
class CategoricalDqmAnalysis:
    """Finite-family DQM numerics and fixed-channel Fisher decomposition."""

    base_probability: np.ndarray
    analytic_fine_score: np.ndarray
    finite_difference_fine_score: np.ndarray
    finite_difference_pushed_score: np.ndarray
    fisher_channel_result: FisherChannelResult
    remainder_ladder: DqmRemainderLadder
    family_scope: FamilyDqmScope
    channel_scope: FixedChannelScope

    def __init__(
        self,
        base_probability: Sequence[float],
        analytic_fine_score: Sequence[Sequence[float]],
        finite_difference_fine_score: Sequence[Sequence[float]],
        finite_difference_pushed_score: Sequence[Sequence[float]],
        fisher_channel_result: FisherChannelResult,
        remainder_ladder: DqmRemainderLadder,
    ) -> None:
        if not isinstance(fisher_channel_result, FisherChannelResult):
            raise TypeError("fisher_channel_result must be a FisherChannelResult")
        if not isinstance(remainder_ladder, DqmRemainderLadder):
            raise TypeError("remainder_ladder must be a DqmRemainderLadder")
        arrays = (
            _readonly(np.asarray(base_probability)),
            _readonly(np.asarray(analytic_fine_score)),
            _readonly(np.asarray(finite_difference_fine_score)),
            _readonly(np.asarray(finite_difference_pushed_score)),
        )
        if not all(np.all(np.isfinite(values)) for values in arrays):
            raise ValueError("analysis arrays must be finite")
        object.__setattr__(self, "base_probability", arrays[0])
        object.__setattr__(self, "analytic_fine_score", arrays[1])
        object.__setattr__(self, "finite_difference_fine_score", arrays[2])
        object.__setattr__(self, "finite_difference_pushed_score", arrays[3])
        object.__setattr__(self, "fisher_channel_result", fisher_channel_result)
        object.__setattr__(self, "remainder_ladder", remainder_ladder)
        object.__setattr__(
            self, "family_scope", "finite_positive_smooth_exponential_family"
        )
        object.__setattr__(
            self, "channel_scope", "declared_fixed_parameter_independent"
        )


def _positive_step(step: float) -> float:
    if isinstance(step, (bool, np.bool_)):
        raise TypeError("step must be a finite positive real number")
    try:
        value = float(step)
    except (TypeError, ValueError) as error:
        raise TypeError("step must be a finite positive real number") from error
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError("step must be finite and positive")
    return value


def _coordinate_perturbations(
    family: CategoricalExponentialFamily,
    theta: Sequence[float],
    step: float,
):
    theta_values = family._theta(theta)
    step_value = _positive_step(step)
    for coordinate in range(family.parameter_count):
        theta_plus = theta_values.copy()
        theta_minus = theta_values.copy()
        theta_plus[coordinate] += step_value
        theta_minus[coordinate] -= step_value
        if (
            not np.isfinite(theta_plus[coordinate])
            or not np.isfinite(theta_minus[coordinate])
        ):
            raise ValueError("finite-difference perturbation must remain finite")
        if (
            theta_plus[coordinate] == theta_values[coordinate]
            or theta_minus[coordinate] == theta_values[coordinate]
        ):
            raise ValueError("finite-difference perturbation rounds back to theta")
        yield coordinate, theta_plus, theta_minus, step_value


def centered_log_probability_finite_difference(
    family: CategoricalExponentialFamily,
    theta: Sequence[float],
    step: float,
) -> np.ndarray:
    """Independently difference each coordinate of the fine log probability."""
    validated_family = _validated_family(family)
    result = np.empty(
        (len(validated_family.labels), validated_family.parameter_count),
        dtype=np.float64,
    )
    for coordinate, theta_plus, theta_minus, step_value in _coordinate_perturbations(
        validated_family, theta, step
    ):
        log_plus = validated_family.log_probabilities(theta_plus)
        log_minus = validated_family.log_probabilities(theta_minus)
        with np.errstate(over="ignore", invalid="ignore"):
            difference = (log_plus - log_minus) / (2.0 * step_value)
        if not np.all(np.isfinite(difference)):
            raise ValueError("nonfinite fine finite-difference result")
        result[:, coordinate] = difference
    return _readonly(result)


def centered_pushed_log_probability_finite_difference(
    family: CategoricalExponentialFamily,
    theta: Sequence[float],
    channel: MarkovKernel,
    step: float,
) -> np.ndarray:
    """Independently difference log probabilities after a fixed channel."""
    validated_family = _validated_family(family)
    if not isinstance(channel, MarkovKernel):
        raise TypeError("channel must be a MarkovKernel")
    if validated_family.labels != channel.source_labels:
        raise ValueError("family labels must equal channel source labels")
    if validated_family.numerics != channel.numerics:
        raise ValueError("family and channel numerics must match")

    result = np.empty(
        (len(channel.target_labels), validated_family.parameter_count),
        dtype=np.float64,
    )
    for coordinate, theta_plus, theta_minus, step_value in _coordinate_perturbations(
        validated_family, theta, step
    ):
        with np.errstate(over="ignore", invalid="ignore"):
            pushed_plus = validated_family.probabilities(theta_plus) @ channel.matrix
            pushed_minus = validated_family.probabilities(theta_minus) @ channel.matrix
        if not np.all(np.isfinite(pushed_plus)) or not np.all(
            np.isfinite(pushed_minus)
        ):
            raise ValueError("nonfinite pushed probability")
        if np.any(pushed_plus <= 0.0) or np.any(pushed_minus <= 0.0):
            raise ValueError("pushed probabilities must remain strictly positive")
        with np.errstate(divide="ignore", invalid="ignore"):
            difference = (
                np.log(pushed_plus) - np.log(pushed_minus)
            ) / (2.0 * step_value)
        if not np.all(np.isfinite(difference)):
            raise ValueError("nonfinite pushed finite-difference result")
        result[:, coordinate] = difference
    return _readonly(result)


def _direction_vector(
    family: CategoricalExponentialFamily, direction: Sequence[float]
) -> np.ndarray:
    values = np.array(direction, dtype=np.float64, copy=True, order="C")
    if values.shape != (family.parameter_count,):
        raise ValueError("direction must have one entry per parameter")
    if not np.all(np.isfinite(values)):
        raise ValueError("direction must be finite")
    with np.errstate(over="ignore", invalid="ignore"):
        norm = float(np.linalg.norm(values))
    if not math.isfinite(norm):
        raise ValueError("direction norm must be finite")
    if not math.isclose(
        norm, 1.0, rel_tol=family.numerics.rtol, abs_tol=family.numerics.atol
    ):
        raise ValueError("direction must have unit Euclidean norm")
    return values


def _dqm_step_sizes(step_sizes: Sequence[float]) -> np.ndarray:
    values = np.array(step_sizes, dtype=np.float64, copy=True, order="C")
    if values.ndim != 1 or values.shape[0] == 0:
        raise ValueError("DQM step_sizes must be a nonempty vector")
    if not np.all(np.isfinite(values)) or np.any(values <= 0.0):
        raise ValueError("DQM step_sizes must be finite and positive")
    if np.any(np.diff(values) >= 0.0):
        raise ValueError("DQM step_sizes must be strictly decreasing")
    return values


def normalized_dqm_remainder_ladder(
    family: CategoricalExponentialFamily,
    theta: Sequence[float],
    direction: Sequence[float],
    step_sizes: Sequence[float],
) -> DqmRemainderLadder:
    """Evaluate signed finite-family DQM remainders along a unit direction."""
    validated_family = _validated_family(family)
    theta_values = validated_family._theta(theta)
    direction_values = _direction_vector(validated_family, direction)
    steps = _dqm_step_sizes(step_sizes)
    base_log = validated_family.log_probabilities(theta_values)
    base_probability = validated_family.probabilities(theta_values)
    analytic_score = validated_family.score(theta_values)
    score_direction = analytic_score @ direction_values
    if not np.all(np.isfinite(score_direction)):
        raise ValueError("nonfinite directional score")

    signed_results: list[np.ndarray] = []
    for sign in (1.0, -1.0):
        remainders = np.empty_like(steps)
        for index, step in enumerate(steps):
            signed_step = sign * float(step)
            with np.errstate(over="ignore", invalid="ignore"):
                perturbed_theta = theta_values + signed_step * direction_values
            if not np.all(np.isfinite(perturbed_theta)):
                raise ValueError("DQM perturbation must remain finite")
            nonzero_direction = direction_values != 0.0
            if np.any(
                perturbed_theta[nonzero_direction]
                == theta_values[nonzero_direction]
            ):
                raise ValueError("DQM perturbation rounds back to theta")
            delta_log = (
                validated_family.log_probabilities(perturbed_theta) - base_log
            )
            with np.errstate(over="ignore", invalid="ignore", under="ignore"):
                ratio_minus_one = np.expm1(0.5 * delta_log)
                linear = 0.5 * signed_step * score_direction
                squared_norm = np.sum(
                    base_probability * (ratio_minus_one - linear) ** 2
                )
                normalized = math.sqrt(float(squared_norm)) / float(step)
            if not math.isfinite(normalized):
                raise ValueError("nonfinite normalized DQM remainder")
            remainders[index] = normalized
        signed_results.append(remainders)
    return DqmRemainderLadder(steps, signed_results[0], signed_results[1])


def analyze_categorical_dqm(
    family: CategoricalExponentialFamily,
    theta: Sequence[float],
    channel: MarkovKernel,
    finite_difference_step: float,
    direction: Sequence[float],
    dqm_step_sizes: Sequence[float],
) -> CategoricalDqmAnalysis:
    """Assemble finite-family DQM and fixed-channel Fisher diagnostics."""
    validated_family = _validated_family(family)
    probability: ProbabilityMeasure = validated_family.probability_measure(theta)
    analytic_score = validated_family.score(theta)
    finite_difference_score = centered_log_probability_finite_difference(
        validated_family, theta, finite_difference_step
    )
    pushed_finite_difference_score = (
        centered_pushed_log_probability_finite_difference(
            validated_family, theta, channel, finite_difference_step
        )
    )
    fisher_result = fisher_channel_decomposition(
        probability, analytic_score, channel
    )
    remainder_ladder = normalized_dqm_remainder_ladder(
        validated_family, theta, direction, dqm_step_sizes
    )
    return CategoricalDqmAnalysis(
        probability.masses,
        analytic_score,
        finite_difference_score,
        pushed_finite_difference_score,
        fisher_result,
        remainder_ladder,
    )
