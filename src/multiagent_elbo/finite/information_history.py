"""Finite categorical information histories and typed scale-flow defects.

The routines in this module stay inside smooth, strictly positive finite
softmax families.  Fisher singularities are handled on the identifiable
tangent quotient by a Moore--Penrose pseudoinverse; no ordinary inverse is
hidden behind the natural-gradient terminology.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from fractions import Fraction
import math
import time
from typing import Literal, Mapping, Sequence

import numpy as np

from multiagent_elbo.config import NumericsConfig
from multiagent_elbo.experiment_support import validate_two_scale_application_fixture

from .categorical import CategoricalExponentialFamily
from .categorical_dqm import (
    centered_log_probability_finite_difference,
    centered_pushed_log_probability_finite_difference,
)
from .fisher import FisherChannelResult, fisher_channel_decomposition
from .measures import MarkovKernel, ProbabilityMeasure


InverseRule = Literal["moore_penrose_identifiable_tangent_quotient"]
FamilyScope = Literal["finite_positive_categorical_softmax_open_chart"]
ChannelScope = Literal["declared_fixed_parameter_independent"]
CounterexampleClassification = Literal[
    "assumption_boundary_witness_not_theorem_refutation"
]


def _readonly(values: object, dtype: object = np.float64) -> np.ndarray:
    result = np.array(values, dtype=dtype, copy=True, order="C")
    result.setflags(write=False)
    return result


def _finite_vector(
    values: Sequence[float], expected_size: int, field: str
) -> np.ndarray:
    raw = np.asarray(values, dtype=object)
    if any(isinstance(value, (bool, np.bool_)) for value in raw.flat):
        raise TypeError(f"{field} must not contain Boolean values")
    result = np.array(values, dtype=np.float64, copy=True, order="C")
    if result.shape != (expected_size,):
        raise ValueError(f"{field} has the wrong shape")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{field} must be finite")
    return result


def _positive_probability(
    values: Sequence[float], expected_size: int, numerics: NumericsConfig
) -> np.ndarray:
    probability = _finite_vector(values, expected_size, "target_probability")
    if np.any(probability <= 0.0):
        raise ValueError("target_probability must be strictly positive")
    if not math.isclose(
        float(np.sum(probability)),
        1.0,
        rel_tol=numerics.rtol,
        abs_tol=numerics.atol,
    ):
        raise ValueError("target_probability must sum to one")
    return probability


def _spectral_diagnostics(
    matrix: np.ndarray, rcond: float
) -> tuple[int, int, float, np.ndarray]:
    symmetric = 0.5 * (matrix + matrix.T)
    eigenvalues = np.linalg.eigvalsh(symmetric)
    scale = max(1.0, float(np.max(np.abs(eigenvalues))))
    threshold = rcond * scale
    positive = eigenvalues[eigenvalues > threshold]
    rank = int(positive.size)
    nullity = int(matrix.shape[0] - rank)
    positive_condition = (
        float(positive[-1] / positive[0]) if positive.size else 0.0
    )
    return rank, nullity, positive_condition, eigenvalues


@dataclass(frozen=True)
class InformationPoint:
    """Fisher--Rao and VFE data in one declared categorical chart."""

    probability: np.ndarray
    score: np.ndarray
    fisher: np.ndarray
    vfe_gradient: np.ndarray
    natural_gradient: np.ndarray
    fisher_projector: np.ndarray
    rank: int
    nullity: int
    positive_spectrum_condition_number: float
    range_residual: float
    inverse_rule: InverseRule
    used_pseudoinverse: bool


def categorical_information_point(
    family: CategoricalExponentialFamily,
    theta: Sequence[float],
    target_probability: Sequence[float],
    *,
    rcond: float,
) -> InformationPoint:
    """Evaluate VFE and its Fisher natural-gradient field in one chart."""
    if not isinstance(family, CategoricalExponentialFamily):
        raise TypeError("family must be a CategoricalExponentialFamily")
    if isinstance(rcond, (bool, np.bool_)) or not isinstance(rcond, (int, float)):
        raise TypeError("rcond must be a finite positive real number")
    rcond_value = float(rcond)
    if not math.isfinite(rcond_value) or rcond_value <= 0.0:
        raise ValueError("rcond must be finite and positive")

    probability = family.probabilities(theta)
    target = _positive_probability(
        target_probability, len(family.labels), family.numerics
    )
    score = family.score(theta)
    fisher = family.fisher_information(theta)
    with np.errstate(divide="raise", invalid="raise", over="raise"):
        log_ratio = np.log(probability) - np.log(target)
        gradient = np.einsum("x,xi,x->i", probability, score, log_ratio)
    if not np.all(np.isfinite(gradient)):
        raise ValueError("nonfinite VFE gradient")

    rank, nullity, condition, _ = _spectral_diagnostics(fisher, rcond_value)
    pseudoinverse = np.linalg.pinv(fisher, rcond=rcond_value, hermitian=True)
    projector = fisher @ pseudoinverse
    range_residual = float(
        np.linalg.norm(gradient - projector @ gradient, ord=np.inf)
    )
    natural_gradient = -(pseudoinverse @ gradient)
    if not all(
        np.all(np.isfinite(array))
        for array in (pseudoinverse, projector, natural_gradient)
    ):
        raise ValueError("nonfinite natural-gradient result")
    return InformationPoint(
        probability=_readonly(probability),
        score=_readonly(score),
        fisher=_readonly(fisher),
        vfe_gradient=_readonly(gradient),
        natural_gradient=_readonly(natural_gradient),
        fisher_projector=_readonly(projector),
        rank=rank,
        nullity=nullity,
        positive_spectrum_condition_number=condition,
        range_residual=range_residual,
        inverse_rule="moore_penrose_identifiable_tangent_quotient",
        used_pseudoinverse=nullity > 0,
    )


def finite_difference_score(
    family: CategoricalExponentialFamily,
    theta: Sequence[float],
    step: float,
) -> np.ndarray:
    """Return a centered coordinatewise finite-difference score check."""
    return centered_log_probability_finite_difference(family, theta, step)


@dataclass(frozen=True)
class FixedChannelDiagnostics:
    fisher_result: FisherChannelResult
    pushed_finite_difference_score: np.ndarray
    score_finite_difference_residual: float
    fisher_defect_residual: float
    channel_scope: ChannelScope
    establishes_dqm: bool


def fixed_channel_diagnostics(
    family: CategoricalExponentialFamily,
    theta: Sequence[float],
    channel: MarkovKernel,
    *,
    finite_difference_step: float,
) -> FixedChannelDiagnostics:
    """Check score projection and Fisher loss for one declared fixed channel."""
    probability = family.probability_measure(theta)
    result = fisher_channel_decomposition(probability, family.score(theta), channel)
    finite_difference = centered_pushed_log_probability_finite_difference(
        family, theta, channel, finite_difference_step
    )
    return FixedChannelDiagnostics(
        fisher_result=result,
        pushed_finite_difference_score=_readonly(finite_difference),
        score_finite_difference_residual=float(
            np.max(np.abs(finite_difference - result.coarse_score))
        ),
        fisher_defect_residual=float(np.max(np.abs(result.residual))),
        channel_scope="declared_fixed_parameter_independent",
        establishes_dqm=False,
    )


@dataclass(frozen=True)
class ParameterDependentChannelControl:
    conditional_expected_score: np.ndarray
    actual_coarse_score: np.ndarray
    gap: float
    inside_fixed_channel_theorem: bool
    classification: CounterexampleClassification


def parameter_dependent_channel_counterexample(
    numerics: NumericsConfig, *, finite_difference_step: float
) -> ParameterDependentChannelControl:
    """Exhibit the missing channel-derivative term outside the fixed-channel theorem."""
    family = CategoricalExponentialFamily(
        ("y0", "y1"), (0.0, 0.0), ((1.0,), (0.0,)), numerics
    )
    theta = np.array((0.0,), dtype=np.float64)

    def channel_at(parameter: float) -> np.ndarray:
        probability = 1.0 / (1.0 + math.exp(-parameter))
        return np.array(
            ((probability, 1.0 - probability),) * 2, dtype=np.float64
        )

    fixed_channel = MarkovKernel(
        family.labels, ("z0", "z1"), channel_at(0.0), numerics
    )
    conditional_score = fisher_channel_decomposition(
        family.probability_measure(theta), family.score(theta), fixed_channel
    ).coarse_score
    step = float(finite_difference_step)
    if not math.isfinite(step) or step <= 0.0:
        raise ValueError("finite_difference_step must be finite and positive")
    pushed_plus = family.probabilities((step,)) @ channel_at(step)
    pushed_minus = family.probabilities((-step,)) @ channel_at(-step)
    actual_score = (
        np.log(pushed_plus) - np.log(pushed_minus)
    ) / (2.0 * step)
    actual_score = actual_score[:, np.newaxis]
    gap = float(np.max(np.abs(actual_score - conditional_score)))
    return ParameterDependentChannelControl(
        conditional_expected_score=_readonly(conditional_score),
        actual_coarse_score=_readonly(actual_score),
        gap=gap,
        inside_fixed_channel_theorem=False,
        classification="assumption_boundary_witness_not_theorem_refutation",
    )


@dataclass(frozen=True)
class RecoveryDiagnostics:
    fisher_defect: np.ndarray
    recoverable_direction_dimension: int
    pointwise_full_fisher_equality: bool
    global_experiment_recovery_claimed: bool


def recovery_diagnostics(
    probability: ProbabilityMeasure,
    score: Sequence[object],
    channel: MarkovKernel,
) -> RecoveryDiagnostics:
    """Separate pointwise directional recovery from stronger recovery claims."""
    result = fisher_channel_decomposition(probability, score, channel)
    defect = result.conditional_covariance
    scale = max(1.0, float(np.linalg.norm(defect, ord=2)))
    tolerance = probability.numerics.atol + probability.numerics.rtol * scale
    eigenvalues = np.linalg.eigvalsh(0.5 * (defect + defect.T))
    recoverable = int(np.count_nonzero(np.abs(eigenvalues) <= tolerance))
    return RecoveryDiagnostics(
        fisher_defect=_readonly(defect),
        recoverable_direction_dimension=recoverable,
        pointwise_full_fisher_equality=bool(np.max(np.abs(defect)) <= tolerance),
        global_experiment_recovery_claimed=False,
    )


def _metric_path_duration(
    history: np.ndarray, metric_at: object
) -> np.ndarray:
    if history.ndim != 2 or history.shape[0] == 0 or history.shape[1] == 0:
        raise ValueError("history must be a nonempty parameter matrix")
    if not np.all(np.isfinite(history)):
        raise ValueError("history parameters must be finite")
    cumulative = np.zeros(history.shape[0], dtype=np.float64)
    for index in range(1, history.shape[0]):
        delta = history[index] - history[index - 1]
        midpoint = 0.5 * (history[index] + history[index - 1])
        metric = np.asarray(metric_at(midpoint), dtype=np.float64)
        if metric.shape != (history.shape[1], history.shape[1]):
            raise ValueError("path metric has the wrong shape")
        squared_length = float(delta @ metric @ delta)
        tolerance = 32.0 * np.finfo(np.float64).eps * max(
            1.0, float(np.linalg.norm(metric, ord=2))
        )
        if squared_length < -tolerance:
            raise ValueError("path metric produced a negative squared length")
        cumulative[index] = cumulative[index - 1] + math.sqrt(
            max(0.0, squared_length)
        )
    return _readonly(cumulative)


def fisher_path_duration(
    family: CategoricalExponentialFamily, history: Sequence[Sequence[float]]
) -> np.ndarray:
    """Compute midpoint Fisher arc length along a saved polygonal history."""
    if not isinstance(family, CategoricalExponentialFamily):
        raise TypeError("family must be a CategoricalExponentialFamily")
    parameters = np.array(history, dtype=np.float64, copy=True, order="C")
    if parameters.ndim != 2 or parameters.shape[1] != family.parameter_count:
        raise ValueError("history must have one column per family parameter")
    return _metric_path_duration(parameters, family.fisher_information)


@dataclass(frozen=True)
class ChartReparameterizationDiagnostic:
    raw_coordinate_length_ratio: float
    information_duration_residual: float
    chart_parameters: np.ndarray
    chart_jacobian: np.ndarray
    original_segment_fisher: np.ndarray
    transformed_segment_fisher: np.ndarray
    original_information_duration: np.ndarray
    transformed_information_duration: np.ndarray
    untransformed_metric_duration: np.ndarray
    metric_pullback_mutation_gap: float


def linear_chart_reparameterization_diagnostic(
    family: CategoricalExponentialFamily,
    history: Sequence[Sequence[float]],
    *,
    chart_scale: float,
) -> ChartReparameterizationDiagnostic:
    """Compare raw coordinate speed with the covariantly transformed Fisher length."""
    scale = float(chart_scale)
    if not math.isfinite(scale) or scale <= 0.0:
        raise ValueError("chart_scale must be finite and positive")
    parameters = np.array(history, dtype=np.float64, copy=True, order="C")
    original_duration = fisher_path_duration(family, parameters)
    transformed = scale * parameters
    dimension = family.parameter_count
    chart_jacobian = scale * np.eye(dimension)
    segment_count = max(0, len(parameters) - 1)
    original_segment_fisher = np.empty((segment_count, dimension, dimension))
    transformed_segment_fisher = np.empty_like(original_segment_fisher)
    for index in range(segment_count):
        midpoint = 0.5 * (parameters[index] + parameters[index + 1])
        original_segment_fisher[index] = family.fisher_information(midpoint)
        transformed_segment_fisher[index] = (
            original_segment_fisher[index] / (scale * scale)
        )

    def transformed_metric(phi: np.ndarray) -> np.ndarray:
        return family.fisher_information(phi / scale) / (scale * scale)

    transformed_duration = _metric_path_duration(transformed, transformed_metric)
    untransformed_metric_duration = _metric_path_duration(
        transformed, lambda phi: family.fisher_information(phi / scale)
    )
    raw_original = float(np.sum(np.linalg.norm(np.diff(parameters, axis=0), axis=1)))
    raw_transformed = float(
        np.sum(np.linalg.norm(np.diff(transformed, axis=0), axis=1))
    )
    return ChartReparameterizationDiagnostic(
        raw_coordinate_length_ratio=(
            raw_transformed / raw_original if raw_original > 0.0 else scale
        ),
        information_duration_residual=abs(
            float(transformed_duration[-1] - original_duration[-1])
        ),
        chart_parameters=_readonly(transformed),
        chart_jacobian=_readonly(chart_jacobian),
        original_segment_fisher=_readonly(original_segment_fisher),
        transformed_segment_fisher=_readonly(transformed_segment_fisher),
        original_information_duration=original_duration,
        transformed_information_duration=transformed_duration,
        untransformed_metric_duration=untransformed_metric_duration,
        metric_pullback_mutation_gap=abs(
            float(untransformed_metric_duration[-1] - transformed_duration[-1])
        ),
    )


def semiconjugacy_defect(
    coarse_map_jacobian: Sequence[Sequence[float]],
    fine_vector: Sequence[float],
    coarse_vector: Sequence[float],
) -> np.ndarray:
    """Return the typed defect ``dC(v_fine) - v_coarse(C(theta))``."""
    matrix = np.array(
        coarse_map_jacobian, dtype=np.float64, copy=True, order="C"
    )
    fine = np.array(fine_vector, dtype=np.float64, copy=True, order="C")
    coarse = np.array(coarse_vector, dtype=np.float64, copy=True, order="C")
    if matrix.ndim != 2 or fine.shape != (matrix.shape[1],):
        raise ValueError("coarse_map_jacobian and fine_vector have incompatible shapes")
    if coarse.shape != (matrix.shape[0],):
        raise ValueError("coarse_vector has the wrong target dimension")
    if not all(np.all(np.isfinite(value)) for value in (matrix, fine, coarse)):
        raise ValueError("semiconjugacy inputs must be finite")
    return _readonly(matrix @ fine - coarse)


def _fraction_vector(values: Sequence[str]) -> np.ndarray:
    return np.array([float(Fraction(value)) for value in values], dtype=np.float64)


def _fraction_matrix(values: Sequence[Sequence[str]]) -> np.ndarray:
    return np.array(
        [[float(Fraction(value)) for value in row] for row in values],
        dtype=np.float64,
    )


@dataclass(frozen=True)
class ProbabilityCoordinateConfigurationMap:
    """Fixture block average transported between product-Bernoulli natural charts."""

    fine_family: CategoricalExponentialFamily
    coarse_family: CategoricalExponentialFamily
    probability_matrix: np.ndarray

    def __post_init__(self) -> None:
        for name, family in (
            ("fine_family", self.fine_family),
            ("coarse_family", self.coarse_family),
        ):
            if not isinstance(family, CategoricalExponentialFamily):
                raise TypeError(f"{name} must be a CategoricalExponentialFamily")
            expected_statistics = {
                tuple(float(bit) for bit in f"{value:0{family.parameter_count}b}")
                for value in range(2**family.parameter_count)
            }
            actual_statistics = {
                tuple(float(value) for value in row)
                for row in family.sufficient_statistics
            }
            if (
                not np.array_equal(family.base_logits, np.zeros(len(family.labels)))
                or len(family.labels) != len(expected_statistics)
                or actual_statistics != expected_statistics
            ):
                raise ValueError(
                    f"{name} must be the declared zero-base product-Bernoulli chart"
                )
        matrix = np.array(
            self.probability_matrix, dtype=np.float64, copy=True, order="C"
        )
        expected_shape = (
            self.coarse_family.parameter_count,
            self.fine_family.parameter_count,
        )
        if matrix.shape != expected_shape:
            raise ValueError("probability_matrix has the wrong configuration dimensions")
        if not np.all(np.isfinite(matrix)) or np.any(matrix < 0.0):
            raise ValueError("probability_matrix must be finite and nonnegative")
        if not np.allclose(
            np.sum(matrix, axis=1),
            1.0,
            atol=self.fine_family.numerics.atol,
            rtol=self.fine_family.numerics.rtol,
        ):
            raise ValueError("each probability-coordinate row must sum to one")
        object.__setattr__(self, "probability_matrix", _readonly(matrix))

    def fine_probability_coordinates(self, theta: Sequence[float]) -> np.ndarray:
        """Return the fixture coordinates p_i = E_theta[T_i]."""
        probabilities = self.fine_family.probabilities(theta)
        coordinates = probabilities @ self.fine_family.sufficient_statistics
        if np.any(coordinates <= 0.0) or np.any(coordinates >= 1.0):
            raise ValueError("fine probability coordinates must lie in the open unit cube")
        return _readonly(coordinates)

    def coarse_probability_coordinates(self, theta: Sequence[float]) -> np.ndarray:
        """Apply the frozen block-average matrix in its declared probability chart."""
        coarse = self.probability_matrix @ self.fine_probability_coordinates(theta)
        if np.any(coarse <= 0.0) or np.any(coarse >= 1.0):
            raise ValueError("coarse probability coordinates must lie in the open unit cube")
        return _readonly(coarse)

    def coarse_natural_parameters(self, theta: Sequence[float]) -> np.ndarray:
        """Transport the probability block average into coarse log-odds coordinates."""
        coarse = self.coarse_probability_coordinates(theta)
        return _readonly(np.log(coarse) - np.log1p(-coarse))

    def jacobian(self, theta: Sequence[float]) -> np.ndarray:
        """Return d(logit(A E[T]))/d theta at the supplied fine point."""
        coarse = self.coarse_probability_coordinates(theta)
        inverse_logit_derivative = 1.0 / (coarse * (1.0 - coarse))
        fine_probability_jacobian = self.fine_family.fisher_information(theta)
        jacobian = (
            inverse_logit_derivative[:, None]
            * (self.probability_matrix @ fine_probability_jacobian)
        )
        return _readonly(jacobian)


@dataclass(frozen=True)
class InformationHistoryModel:
    application_id: str
    fine_family: CategoricalExponentialFamily
    coarse_family: CategoricalExponentialFamily
    channel: MarkovKernel
    fine_target: np.ndarray
    coarse_target: np.ndarray
    configuration_map: ProbabilityCoordinateConfigurationMap
    initial_theta: np.ndarray
    family_scope: FamilyScope


def build_information_history_model(
    fixture_payload: Mapping[str, object], numerics: NumericsConfig
) -> InformationHistoryModel:
    """Build the two declared charts only after validating the frozen fixture."""
    if not isinstance(fixture_payload, Mapping):
        raise TypeError("fixture_payload must be a mapping")
    if not isinstance(numerics, NumericsConfig):
        raise TypeError("numerics must be a NumericsConfig")
    application_id = validate_two_scale_application_fixture(fixture_payload)
    state_spaces = fixture_payload["state_spaces"]
    fine_labels = tuple(state_spaces["fine"]["labels"])
    coarse_labels = tuple(state_spaces["coarse"]["labels"])
    fine_statistics = tuple(
        tuple(float(bit) for bit in label) for label in fine_labels
    )
    coarse_statistics = tuple(
        tuple(float(bit) for bit in label) for label in coarse_labels
    )
    fine_family = CategoricalExponentialFamily(
        fine_labels,
        np.zeros(len(fine_labels)),
        fine_statistics,
        numerics,
    )
    coarse_family = CategoricalExponentialFamily(
        coarse_labels,
        np.zeros(len(coarse_labels)),
        coarse_statistics,
        numerics,
    )
    channel_payload = fixture_payload["channel"]["arrows"][0]
    channel = MarkovKernel(
        fine_labels,
        coarse_labels,
        _fraction_matrix(channel_payload["rows"]),
        numerics,
    )
    fine_target = _fraction_vector(
        fixture_payload["generative_structure"]["posterior"]
    )
    coarse_target = fine_target @ channel.matrix
    coarse_probability_map = _fraction_matrix(
        fixture_payload["configuration"]["coarse_map_matrix"]
    )
    return InformationHistoryModel(
        application_id=application_id,
        fine_family=fine_family,
        coarse_family=coarse_family,
        channel=channel,
        fine_target=_readonly(fine_target),
        coarse_target=_readonly(coarse_target),
        configuration_map=ProbabilityCoordinateConfigurationMap(
            fine_family, coarse_family, coarse_probability_map
        ),
        initial_theta=_readonly((-0.4, 0.25, -0.2, 0.35)),
        family_scope="finite_positive_categorical_softmax_open_chart",
    )


@dataclass(frozen=True)
class InformationHistory:
    fine_parameters: np.ndarray
    coarse_parameters: np.ndarray
    fine_probability_coordinates: np.ndarray
    coarse_probability_coordinates: np.ndarray
    coarse_map_jacobian: np.ndarray
    inference_orbit_parameter: np.ndarray
    rg_depth: np.ndarray
    fine_score: np.ndarray
    fine_finite_difference_score: np.ndarray
    pushed_score: np.ndarray
    pushed_finite_difference_score: np.ndarray
    coarse_score: np.ndarray
    coarse_finite_difference_score: np.ndarray
    fine_fisher: np.ndarray
    pushed_fisher: np.ndarray
    fisher_defect: np.ndarray
    fisher_identity_residual: np.ndarray
    coarse_fisher: np.ndarray
    fine_vfe_gradient: np.ndarray
    coarse_vfe_gradient: np.ndarray
    fine_natural_gradient: np.ndarray
    coarse_natural_gradient: np.ndarray
    fine_range_residual: np.ndarray
    coarse_range_residual: np.ndarray
    fine_rank: np.ndarray
    pushed_rank: np.ndarray
    coarse_rank: np.ndarray
    fine_positive_condition: np.ndarray
    pushed_positive_condition: np.ndarray
    coarse_positive_condition: np.ndarray
    information_duration: np.ndarray
    reparameterized_information_duration: np.ndarray
    reparameterized_fine_parameters: np.ndarray
    chart_reparameterization_jacobian: np.ndarray
    fine_segment_fisher: np.ndarray
    reparameterized_segment_fisher: np.ndarray
    metric_pullback_mutation_duration: np.ndarray
    reparameterization_parameter: np.ndarray
    raw_coordinate_cumulative: np.ndarray
    semiconjugacy_defects: np.ndarray
    semiconjugacy_defect_norms: np.ndarray
    pushed_fine_vector: np.ndarray
    coarse_comparison_vector: np.ndarray
    wall_time_seconds: float

    def semantic_arrays(self) -> tuple[np.ndarray, ...]:
        """Return every deterministic numerical array in declaration order."""
        return tuple(
            getattr(self, field.name)
            for field in fields(self)
            if isinstance(getattr(self, field.name), np.ndarray)
        )


@dataclass(frozen=True)
class RequiredNegativeControls:
    """Pinned boundary witnesses kept separate from theorem residuals."""

    parameter_dependent_conditional_score: np.ndarray
    parameter_dependent_actual_score: np.ndarray
    parameter_dependent_gap: float
    rank_deficient_fisher: np.ndarray
    rank_deficient_gradient: np.ndarray
    rank_deficient_natural_gradient: np.ndarray
    rank_deficient_rank: int
    rank_deficient_range_residual: float
    straight_history: np.ndarray
    detour_history: np.ndarray
    straight_duration: np.ndarray
    detour_duration: np.ndarray
    chart_raw_length_ratio: float
    chart_information_duration_residual: float
    semiconjugacy_minus_oracle: np.ndarray
    semiconjugacy_plus_mutation: np.ndarray
    semiconjugacy_plus_mutation_gap: float


def required_negative_controls(
    numerics: NumericsConfig,
) -> RequiredNegativeControls:
    """Construct all preregistered controls with literal, independent targets."""
    parameter_dependent = parameter_dependent_channel_counterexample(
        numerics, finite_difference_step=1.0e-5
    )
    rank_family = CategoricalExponentialFamily(
        ("a", "b", "c"),
        (0.0, 0.0, 0.0),
        ((1.0, 2.0), (0.0, 0.0), (-1.0, -2.0)),
        numerics,
    )
    rank_point = categorical_information_point(
        rank_family, (0.2, 0.1), (0.2, 0.3, 0.5), rcond=numerics.min_spd_rcond
    )
    path_family = CategoricalExponentialFamily(
        ("x0", "x1", "x2"),
        (0.0, 0.0, 0.0),
        ((1.0, 0.0), (0.0, 1.0), (0.0, 0.0)),
        numerics,
    )
    straight = np.array(((-0.6, -0.4), (0.0, 0.0), (0.6, 0.4)))
    detour = np.array(((-0.6, -0.4), (-0.5, 0.9), (0.6, 0.4)))
    straight_duration = fisher_path_duration(path_family, straight)
    detour_duration = fisher_path_duration(path_family, detour)
    chart_history = np.array(((-0.4, 0.1), (-0.1, 0.2), (0.3, 0.25)))
    chart = linear_chart_reparameterization_diagnostic(
        path_family, chart_history, chart_scale=2.0
    )
    coarse_map = np.array(((0.5, 0.5, 0.0), (0.0, 0.5, 0.5)))
    fine_vector = np.array((2.0, -1.0, 3.0))
    coarse_vector = np.array((0.25, -0.75))
    minus_oracle = semiconjugacy_defect(coarse_map, fine_vector, coarse_vector)
    plus_mutation = coarse_map @ fine_vector + coarse_vector
    mutation_gap = float(np.max(np.abs(plus_mutation - minus_oracle)))
    return RequiredNegativeControls(
        parameter_dependent_conditional_score=parameter_dependent.conditional_expected_score,
        parameter_dependent_actual_score=parameter_dependent.actual_coarse_score,
        parameter_dependent_gap=parameter_dependent.gap,
        rank_deficient_fisher=rank_point.fisher,
        rank_deficient_gradient=rank_point.vfe_gradient,
        rank_deficient_natural_gradient=rank_point.natural_gradient,
        rank_deficient_rank=rank_point.rank,
        rank_deficient_range_residual=rank_point.range_residual,
        straight_history=_readonly(straight),
        detour_history=_readonly(detour),
        straight_duration=straight_duration,
        detour_duration=detour_duration,
        chart_raw_length_ratio=chart.raw_coordinate_length_ratio,
        chart_information_duration_residual=chart.information_duration_residual,
        semiconjugacy_minus_oracle=minus_oracle,
        semiconjugacy_plus_mutation=_readonly(plus_mutation),
        semiconjugacy_plus_mutation_gap=mutation_gap,
    )


def simulate_information_history(
    model: InformationHistoryModel, *, history_steps: int, step_size: float
) -> InformationHistory:
    """Integrate a finite Euler history and retain every metric input array."""
    if not isinstance(model, InformationHistoryModel):
        raise TypeError("model must be an InformationHistoryModel")
    if type(history_steps) is not int or history_steps <= 0:
        raise ValueError("history_steps must be a positive int")
    if type(step_size) is not float or not math.isfinite(step_size) or step_size <= 0.0:
        raise ValueError("step_size must be a positive finite float")
    started = time.perf_counter()
    finite_difference_step = 1.0e-5
    rcond = model.fine_family.numerics.min_spd_rcond
    fine_dimension = model.fine_family.parameter_count
    coarse_dimension = model.coarse_family.parameter_count
    fine_states = len(model.fine_family.labels)
    coarse_states = len(model.coarse_family.labels)

    fine_parameters = np.empty((history_steps, fine_dimension))
    coarse_parameters = np.empty((history_steps, coarse_dimension))
    fine_probability_coordinates = np.empty_like(fine_parameters)
    coarse_probability_coordinates = np.empty_like(coarse_parameters)
    coarse_map_jacobian = np.empty(
        (history_steps, coarse_dimension, fine_dimension)
    )
    fine_score = np.empty((history_steps, fine_states, fine_dimension))
    fine_fd = np.empty_like(fine_score)
    pushed_score = np.empty((history_steps, coarse_states, fine_dimension))
    pushed_fd = np.empty_like(pushed_score)
    coarse_score = np.empty((history_steps, coarse_states, coarse_dimension))
    coarse_fd = np.empty_like(coarse_score)
    fine_fisher = np.empty((history_steps, fine_dimension, fine_dimension))
    pushed_fisher = np.empty_like(fine_fisher)
    fisher_defect = np.empty_like(fine_fisher)
    fisher_residual = np.empty_like(fine_fisher)
    coarse_fisher = np.empty((history_steps, coarse_dimension, coarse_dimension))
    fine_gradient = np.empty((history_steps, fine_dimension))
    coarse_gradient = np.empty((history_steps, coarse_dimension))
    fine_natural = np.empty_like(fine_gradient)
    coarse_natural = np.empty_like(coarse_gradient)
    fine_range = np.empty(history_steps)
    coarse_range = np.empty(history_steps)
    fine_rank = np.empty(history_steps)
    pushed_rank = np.empty(history_steps)
    coarse_rank = np.empty(history_steps)
    fine_condition = np.empty(history_steps)
    pushed_condition = np.empty(history_steps)
    coarse_condition = np.empty(history_steps)
    defects = np.empty((history_steps, coarse_dimension))
    pushed_vectors = np.empty_like(defects)
    coarse_vectors = np.empty_like(defects)
    theta = np.array(model.initial_theta, copy=True)

    for index in range(history_steps):
        fine_configuration = model.configuration_map.fine_probability_coordinates(theta)
        coarse_configuration = model.configuration_map.coarse_probability_coordinates(theta)
        phi = model.configuration_map.coarse_natural_parameters(theta)
        configuration_jacobian = model.configuration_map.jacobian(theta)
        fine_point = categorical_information_point(
            model.fine_family, theta, model.fine_target, rcond=rcond
        )
        coarse_point = categorical_information_point(
            model.coarse_family, phi, model.coarse_target, rcond=rcond
        )
        channel_point = fixed_channel_diagnostics(
            model.fine_family,
            theta,
            model.channel,
            finite_difference_step=finite_difference_step,
        )
        fisher_channel = channel_point.fisher_result
        defect = semiconjugacy_defect(
            configuration_jacobian,
            fine_point.natural_gradient,
            coarse_point.natural_gradient,
        )
        pushed_vector = configuration_jacobian @ fine_point.natural_gradient

        fine_parameters[index] = theta
        coarse_parameters[index] = phi
        fine_probability_coordinates[index] = fine_configuration
        coarse_probability_coordinates[index] = coarse_configuration
        coarse_map_jacobian[index] = configuration_jacobian
        fine_score[index] = fine_point.score
        fine_fd[index] = finite_difference_score(
            model.fine_family, theta, finite_difference_step
        )
        pushed_score[index] = fisher_channel.coarse_score
        pushed_fd[index] = channel_point.pushed_finite_difference_score
        coarse_score[index] = coarse_point.score
        coarse_fd[index] = finite_difference_score(
            model.coarse_family, phi, finite_difference_step
        )
        fine_fisher[index] = fine_point.fisher
        pushed_fisher[index] = fisher_channel.coarse_fisher
        fisher_defect[index] = fisher_channel.conditional_covariance
        fisher_residual[index] = fisher_channel.residual
        coarse_fisher[index] = coarse_point.fisher
        fine_gradient[index] = fine_point.vfe_gradient
        coarse_gradient[index] = coarse_point.vfe_gradient
        fine_natural[index] = fine_point.natural_gradient
        coarse_natural[index] = coarse_point.natural_gradient
        fine_range[index] = fine_point.range_residual
        coarse_range[index] = coarse_point.range_residual
        fine_rank[index] = fine_point.rank
        coarse_rank[index] = coarse_point.rank
        fine_condition[index] = fine_point.positive_spectrum_condition_number
        coarse_condition[index] = coarse_point.positive_spectrum_condition_number
        pushed_rank_value, _, pushed_condition_value, _ = _spectral_diagnostics(
            fisher_channel.coarse_fisher, rcond
        )
        pushed_rank[index] = pushed_rank_value
        pushed_condition[index] = pushed_condition_value
        defects[index] = defect
        pushed_vectors[index] = pushed_vector
        coarse_vectors[index] = coarse_point.natural_gradient
        if index + 1 < history_steps:
            theta = theta + step_size * fine_point.natural_gradient

    chart_diagnostic = linear_chart_reparameterization_diagnostic(
        model.fine_family, fine_parameters, chart_scale=2.0
    )
    information_duration = chart_diagnostic.original_information_duration
    reparameterized_duration = chart_diagnostic.transformed_information_duration
    reparameterization_parameter = np.linspace(0.0, 1.0, history_steps) ** 2
    raw_cumulative = np.zeros(history_steps)
    if history_steps > 1:
        raw_cumulative[1:] = np.cumsum(
            np.linalg.norm(np.diff(fine_parameters, axis=0), axis=1)
        )
    defect_norms = np.linalg.norm(defects, axis=1)
    elapsed = time.perf_counter() - started

    return InformationHistory(
        fine_parameters=_readonly(fine_parameters),
        coarse_parameters=_readonly(coarse_parameters),
        fine_probability_coordinates=_readonly(fine_probability_coordinates),
        coarse_probability_coordinates=_readonly(coarse_probability_coordinates),
        coarse_map_jacobian=_readonly(coarse_map_jacobian),
        inference_orbit_parameter=_readonly(
            np.arange(history_steps, dtype=np.float64) * step_size
        ),
        rg_depth=_readonly((0.0, 1.0)),
        fine_score=_readonly(fine_score),
        fine_finite_difference_score=_readonly(fine_fd),
        pushed_score=_readonly(pushed_score),
        pushed_finite_difference_score=_readonly(pushed_fd),
        coarse_score=_readonly(coarse_score),
        coarse_finite_difference_score=_readonly(coarse_fd),
        fine_fisher=_readonly(fine_fisher),
        pushed_fisher=_readonly(pushed_fisher),
        fisher_defect=_readonly(fisher_defect),
        fisher_identity_residual=_readonly(fisher_residual),
        coarse_fisher=_readonly(coarse_fisher),
        fine_vfe_gradient=_readonly(fine_gradient),
        coarse_vfe_gradient=_readonly(coarse_gradient),
        fine_natural_gradient=_readonly(fine_natural),
        coarse_natural_gradient=_readonly(coarse_natural),
        fine_range_residual=_readonly(fine_range),
        coarse_range_residual=_readonly(coarse_range),
        fine_rank=_readonly(fine_rank),
        pushed_rank=_readonly(pushed_rank),
        coarse_rank=_readonly(coarse_rank),
        fine_positive_condition=_readonly(fine_condition),
        pushed_positive_condition=_readonly(pushed_condition),
        coarse_positive_condition=_readonly(coarse_condition),
        information_duration=information_duration,
        reparameterized_information_duration=reparameterized_duration,
        reparameterized_fine_parameters=chart_diagnostic.chart_parameters,
        chart_reparameterization_jacobian=chart_diagnostic.chart_jacobian,
        fine_segment_fisher=chart_diagnostic.original_segment_fisher,
        reparameterized_segment_fisher=chart_diagnostic.transformed_segment_fisher,
        metric_pullback_mutation_duration=(
            chart_diagnostic.untransformed_metric_duration
        ),
        reparameterization_parameter=_readonly(reparameterization_parameter),
        raw_coordinate_cumulative=_readonly(raw_cumulative),
        semiconjugacy_defects=_readonly(defects),
        semiconjugacy_defect_norms=_readonly(defect_norms),
        pushed_fine_vector=_readonly(pushed_vectors),
        coarse_comparison_vector=_readonly(coarse_vectors),
        wall_time_seconds=elapsed,
    )


__all__ = [
    "ChartReparameterizationDiagnostic",
    "FixedChannelDiagnostics",
    "InformationHistory",
    "InformationHistoryModel",
    "InformationPoint",
    "ParameterDependentChannelControl",
    "ProbabilityCoordinateConfigurationMap",
    "RecoveryDiagnostics",
    "RequiredNegativeControls",
    "build_information_history_model",
    "categorical_information_point",
    "finite_difference_score",
    "fisher_path_duration",
    "fixed_channel_diagnostics",
    "linear_chart_reparameterization_diagnostic",
    "parameter_dependent_channel_counterexample",
    "recovery_diagnostics",
    "required_negative_controls",
    "semiconjugacy_defect",
    "simulate_information_history",
]
