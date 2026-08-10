"""Exact finite scale composition and comparison-typed residual diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
import math
from types import MappingProxyType
from typing import Mapping, Sequence


ExactVector = tuple[Fraction, ...]
ExactMatrix = tuple[tuple[Fraction, ...], ...]
State = tuple[int, ...]
Subset = tuple[int, ...]


def _fraction(value: object, field: str) -> Fraction:
    if isinstance(value, bool):
        raise TypeError(f"{field} must be rational, not bool")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise TypeError(f"{field} must be rational") from error


def _vector(values: Sequence[object], *, length: int, field: str) -> ExactVector:
    if len(values) != length:
        raise ValueError(f"{field} must have length {length}")
    return tuple(_fraction(value, f"{field}[{index}]") for index, value in enumerate(values))


def _matrix(values: Sequence[Sequence[object]], *, field: str) -> ExactMatrix:
    rows = tuple(tuple(_fraction(value, field) for value in row) for row in values)
    if not rows or not rows[0]:
        raise ValueError(f"{field} must be nonempty")
    if any(len(row) != len(rows[0]) for row in rows):
        raise ValueError(f"{field} rows must have equal length")
    return rows


def _identity(size: int) -> ExactMatrix:
    return tuple(
        tuple(Fraction(int(row == column)) for column in range(size))
        for row in range(size)
    )


def _matmul(left: ExactMatrix, right: ExactMatrix) -> ExactMatrix:
    if len(left[0]) != len(right):
        raise ValueError("matrix dimensions do not compose")
    return tuple(
        tuple(
            sum(
                (left[row][inner] * right[inner][column] for inner in range(len(right))),
                Fraction(0),
            )
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def _matvec(matrix: ExactMatrix, vector: ExactVector) -> ExactVector:
    if len(matrix[0]) != len(vector):
        raise ValueError("matrix and vector dimensions do not match")
    return tuple(
        sum((entry * value for entry, value in zip(row, vector)), Fraction(0))
        for row in matrix
    )


def _row_vector_matrix(vector: ExactVector, matrix: ExactMatrix) -> ExactVector:
    if len(vector) != len(matrix):
        raise ValueError("law length must match channel source")
    return tuple(
        sum((vector[row] * matrix[row][column] for row in range(len(matrix))), Fraction(0))
        for column in range(len(matrix[0]))
    )


def _subtract(left: ExactVector, right: ExactVector) -> ExactVector:
    if len(left) != len(right):
        raise ValueError("vector dimensions do not match")
    return tuple(a - b for a, b in zip(left, right))


def _scale(vector: ExactVector, scalar: Fraction) -> ExactVector:
    if scalar == 0:
        raise ValueError("scale divisor must be nonzero")
    return tuple(value / scalar for value in vector)


def _inverse(matrix: ExactMatrix) -> ExactMatrix:
    size = len(matrix)
    if len(matrix[0]) != size:
        raise ValueError("isomorphism matrix must be square")
    augmented = [list(row) + list(identity_row) for row, identity_row in zip(matrix, _identity(size))]
    for column in range(size):
        pivot = next((row for row in range(column, size) if augmented[row][column] != 0), None)
        if pivot is None:
            raise ValueError("isomorphism matrix must be invertible")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(augmented[row], augmented[column])
            ]
    return tuple(tuple(row[size:]) for row in augmented)


@dataclass(frozen=True, init=False)
class ExactMarkovChannel:
    """Normalized recognition-independent finite channel with exact entries."""

    source_labels: tuple[str, ...]
    target_labels: tuple[str, ...]
    matrix: ExactMatrix
    recognition_independent: bool

    def __init__(
        self,
        source_labels: Sequence[str],
        target_labels: Sequence[str],
        matrix: Sequence[Sequence[object]],
        *,
        recognition_independent: bool = True,
    ) -> None:
        source = tuple(source_labels)
        target = tuple(target_labels)
        if not source or len(set(source)) != len(source):
            raise ValueError("source labels must be nonempty and unique")
        if not target or len(set(target)) != len(target):
            raise ValueError("target labels must be nonempty and unique")
        if recognition_independent is not True:
            raise ValueError("scale channels must be recognition-independent")
        exact_matrix = _matrix(matrix, field="channel matrix")
        if len(exact_matrix) != len(source) or len(exact_matrix[0]) != len(target):
            raise ValueError("channel matrix shape must match labels")
        if any(value < 0 for row in exact_matrix for value in row):
            raise ValueError("channel entries must be nonnegative")
        if any(sum(row, Fraction(0)) != 1 for row in exact_matrix):
            raise ValueError("channel rows must sum to one exactly")
        object.__setattr__(self, "source_labels", source)
        object.__setattr__(self, "target_labels", target)
        object.__setattr__(self, "matrix", exact_matrix)
        object.__setattr__(self, "recognition_independent", True)

    def compose(self, downstream: "ExactMarkovChannel") -> "ExactMarkovChannel":
        """Return the right-acting composite whose staged law is ``(mu K) D``."""
        if self.target_labels != downstream.source_labels:
            raise ValueError("channel target labels must equal downstream source labels")
        return ExactMarkovChannel(
            self.source_labels,
            downstream.target_labels,
            _matmul(self.matrix, downstream.matrix),
        )

    def pushforward(self, law: Sequence[object]) -> ExactVector:
        exact_law = _vector(law, length=len(self.source_labels), field="law")
        return _row_vector_matrix(exact_law, self.matrix)


@dataclass(frozen=True)
class CoarseAction:
    coarse_reference: ExactVector
    coarse_evidence: ExactVector
    likelihood: ExactVector
    action: tuple[float, ...]


def conditional_log_laplace_action(
    reference: Sequence[object],
    evidence: Sequence[object],
    channel: ExactMarkovChannel,
) -> CoarseAction:
    """Push a measure pair and return its exact density and log-Laplace action."""
    rho = _vector(reference, length=len(channel.source_labels), field="reference")
    measure = _vector(evidence, length=len(channel.source_labels), field="evidence")
    if any(value < 0 for value in rho + measure) or sum(rho, Fraction(0)) != 1:
        raise ValueError("reference must be a probability and evidence nonnegative")
    if any(mass > 0 and base == 0 for mass, base in zip(measure, rho)):
        raise ValueError("evidence must be absolutely continuous with reference")
    coarse_rho = channel.pushforward(rho)
    coarse_measure = channel.pushforward(measure)
    likelihood: list[Fraction] = []
    action: list[float] = []
    for base, mass in zip(coarse_rho, coarse_measure):
        if base == 0:
            likelihood.append(Fraction(0))
            action.append(math.inf)
            continue
        density = mass / base
        likelihood.append(density)
        action.append(math.inf if density == 0 else -math.log(float(density)))
    return CoarseAction(coarse_rho, coarse_measure, tuple(likelihood), tuple(action))


@dataclass(frozen=True)
class PosteriorBridge:
    joint: tuple[ExactVector, ...]
    coarse_posterior: ExactVector
    reverse: tuple[ExactVector, ...]


def posterior_bridge(
    posterior: Sequence[object], channel: ExactMarkovChannel
) -> PosteriorBridge:
    """Build the exact posterior joint and Bayes reverse kernel."""
    fine = _vector(posterior, length=len(channel.source_labels), field="posterior")
    if any(value < 0 for value in fine) or sum(fine, Fraction(0)) != 1:
        raise ValueError("posterior must be a probability law")
    joint = tuple(
        tuple(fine[row] * channel.matrix[row][column] for column in range(len(channel.target_labels)))
        for row in range(len(channel.source_labels))
    )
    coarse = channel.pushforward(fine)
    reverse = tuple(
        tuple(
            Fraction(0) if coarse[column] == 0 else joint[row][column] / coarse[column]
            for row in range(len(channel.source_labels))
        )
        for column in range(len(channel.target_labels))
    )
    return PosteriorBridge(joint, coarse, reverse)


@dataclass(frozen=True, init=False)
class ExactLinearIsomorphism:
    """Exact native-to-reference comparison map."""

    native_type: str
    reference_type: str
    matrix: ExactMatrix
    inverse: ExactMatrix

    def __init__(
        self,
        native_type: str,
        reference_type: str,
        matrix: Sequence[Sequence[object]],
    ) -> None:
        if not native_type or not reference_type:
            raise ValueError("comparison types must be nonempty")
        exact_matrix = _matrix(matrix, field="comparison matrix")
        inverse = _inverse(exact_matrix)
        object.__setattr__(self, "native_type", native_type)
        object.__setattr__(self, "reference_type", reference_type)
        object.__setattr__(self, "matrix", exact_matrix)
        object.__setattr__(self, "inverse", inverse)


def identified_linear_step(
    source_identification: ExactLinearIsomorphism,
    native_step: Sequence[Sequence[object]],
    target_identification: ExactLinearIsomorphism,
) -> ExactMatrix:
    """Form ``I_(l+1) C_(l,l+1) I_l^-1`` in the reference space."""
    if source_identification.reference_type != target_identification.reference_type:
        raise ValueError("comparison maps must share one reference type")
    step = _matrix(native_step, field="native step")
    return _matmul(
        target_identification.matrix,
        _matmul(step, source_identification.inverse),
    )


def ordered_derivative_cocycle(
    derivatives: Sequence[Sequence[Sequence[object]]],
) -> ExactMatrix:
    """Compose adjacent derivatives with the rightmost scale acting first."""
    if not derivatives:
        raise ValueError("at least one derivative is required")
    exact = [_matrix(derivative, field="derivative") for derivative in derivatives]
    result = exact[0]
    for derivative in exact[1:]:
        result = _matmul(derivative, result)
    return result


@dataclass(frozen=True)
class RetainedBetaDiagnostics:
    exact_beta: ExactVector
    retained_beta: ExactVector
    residual_from_difference: ExactVector
    residual_from_identified_projection: ExactVector
    residual_from_native_transport: ExactVector


def retained_beta_diagnostics(
    *,
    exact_step: Sequence[Sequence[object]],
    reference_input: Sequence[object],
    source_identification: ExactLinearIsomorphism,
    target_identification: ExactLinearIsomorphism,
    source_projection: Sequence[Sequence[object]],
    target_projection: Sequence[Sequence[object]],
    delta_log_scale: object,
) -> RetainedBetaDiagnostics:
    """Return exact, retained, and exact signed transported beta residuals."""
    delta = _fraction(delta_log_scale, "delta_log_scale")
    if delta <= 0:
        raise ValueError("delta_log_scale must be positive")
    source_r = _matrix(source_projection, field="source projection")
    target_r = _matrix(target_projection, field="target projection")
    if _matmul(source_r, source_r) != source_r or _matmul(target_r, target_r) != target_r:
        raise ValueError("retained projections must be idempotent")
    g = _vector(reference_input, length=len(source_identification.matrix), field="reference_input")
    source_r_hat = _matmul(
        source_identification.matrix,
        _matmul(source_r, source_identification.inverse),
    )
    if _matvec(source_r_hat, g) != g:
        raise ValueError("reference_input must lie in the retained source sector")
    native_step_matrix = _matrix(exact_step, field="exact_step")
    native_input = _matvec(source_identification.inverse, g)
    native_output = _matvec(native_step_matrix, native_input)
    exact_output = _matvec(target_identification.matrix, native_output)
    if len(exact_output) != len(g):
        raise ValueError("beta subtraction requires one common reference-space dimension")
    target_r_hat = _matmul(
        target_identification.matrix,
        _matmul(target_r, target_identification.inverse),
    )
    retained_output = _matvec(target_r_hat, exact_output)
    exact_beta = _scale(_subtract(exact_output, g), delta)
    retained_beta = _scale(_subtract(retained_output, g), delta)
    residual_difference = _subtract(exact_beta, retained_beta)
    residual_identified = _scale(
        _matvec(
            _subtract_matrix(_identity(len(target_r_hat)), target_r_hat),
            exact_output,
        ),
        delta,
    )
    residual_native = _scale(
        _matvec(
            target_identification.matrix,
            _matvec(
                _subtract_matrix(_identity(len(target_r)), target_r), native_output
            ),
        ),
        delta,
    )
    if not (residual_difference == residual_identified == residual_native):
        raise ArithmeticError("retained beta residual forms disagree")
    return RetainedBetaDiagnostics(
        exact_beta,
        retained_beta,
        residual_difference,
        residual_identified,
        residual_native,
    )


def _subtract_matrix(left: ExactMatrix, right: ExactMatrix) -> ExactMatrix:
    if len(left) != len(right) or len(left[0]) != len(right[0]):
        raise ValueError("matrix dimensions do not match")
    return tuple(
        tuple(a - b for a, b in zip(left_row, right_row))
        for left_row, right_row in zip(left, right)
    )


def projection_intertwining_residual(
    identification: ExactLinearIsomorphism,
    native_projection: Sequence[Sequence[object]],
    claimed_reference_projection: Sequence[Sequence[object]],
) -> Fraction:
    """Return the exact entrywise gap in the projection intertwiner."""
    native = _matrix(native_projection, field="native projection")
    claimed = _matrix(claimed_reference_projection, field="reference projection")
    transported = _matmul(identification.matrix, _matmul(native, identification.inverse))
    difference = _subtract_matrix(transported, claimed)
    return max(abs(value) for row in difference for value in row)


@dataclass(frozen=True)
class FisherCocycleResidualForms:
    from_norm_difference: Fraction
    from_coarse_jet_cross_terms: Fraction
    from_pushed_jet_cross_terms: Fraction


def _bilinear(metric: ExactMatrix, left: ExactVector, right: ExactVector) -> Fraction:
    return sum((a * b for a, b in zip(left, _matvec(metric, right))), Fraction(0))


def base_fisher_cocycle_residual_forms(
    *,
    fisher_defect: Sequence[Sequence[object]],
    pushed_fine_jet: Sequence[object],
    horizontal_anomaly: Sequence[object],
) -> FisherCocycleResidualForms:
    """Evaluate the three sign-sensitive exact residual forms of the base cocycle."""
    metric = _matrix(fisher_defect, field="fisher defect")
    v = _vector(pushed_fine_jet, length=len(metric), field="pushed fine jet")
    anomaly = _vector(horizontal_anomaly, length=len(metric), field="horizontal anomaly")
    coarse = tuple(value + defect for value, defect in zip(v, anomaly))
    form_a = _bilinear(metric, v, v) - _bilinear(metric, coarse, coarse)
    form_b = -_bilinear(metric, coarse, anomaly) - _bilinear(metric, anomaly, coarse) + _bilinear(metric, anomaly, anomaly)
    form_c = -_bilinear(metric, v, anomaly) - _bilinear(metric, anomaly, v) - _bilinear(metric, anomaly, anomaly)
    if not (form_a == form_b == form_c):
        raise ArithmeticError("Fisher cocycle residual forms disagree")
    return FisherCocycleResidualForms(form_a, form_b, form_c)


def _all_subsets(size: int):
    for count in range(size + 1):
        yield from combinations(range(size), count)


@dataclass(frozen=True)
class AnchoredMobiusDecomposition:
    anchor: State
    action: Mapping[State, Fraction]
    components: Mapping[Subset, Mapping[tuple[int, ...], Fraction]]

    def component_value(self, subset: Subset, state: State) -> Fraction:
        return self.components[subset][tuple(state[index] for index in subset)]

    def reconstruct(self, state: State, maximum_order: int | None = None) -> Fraction:
        if state not in self.action:
            raise ValueError("state is outside the declared finite product")
        limit = len(self.anchor) if maximum_order is None else maximum_order
        return sum(
            (
                self.components[subset][tuple(state[index] for index in subset)]
                for subset in self.components
                if len(subset) <= limit
            ),
            Fraction(0),
        )

    def maximum_residual(self, maximum_order: int) -> Fraction:
        if type(maximum_order) is not int or not 0 <= maximum_order <= len(self.anchor):
            raise ValueError("maximum_order is outside the interaction hierarchy")
        return max(
            abs(value - self.reconstruct(state, maximum_order))
            for state, value in self.action.items()
        )


def anchored_mobius_decompose(
    action: Mapping[State, object], *, anchor: State
) -> AnchoredMobiusDecomposition:
    """Decompose a complete finite-product action into every subset potential."""
    if not anchor:
        raise ValueError("anchor must have at least one coordinate")
    exact_action = {state: _fraction(value, "action") for state, value in action.items()}
    alphabets: list[tuple[int, ...]] = []
    for axis in range(len(anchor)):
        values = tuple(sorted({state[axis] for state in exact_action if len(state) == len(anchor)}))
        if anchor[axis] not in values:
            raise ValueError("anchor must belong to every coordinate alphabet")
        alphabets.append(values)
    expected_states = set(product(*alphabets))
    if set(exact_action) != expected_states:
        raise ValueError("action must cover the complete finite product exactly")
    components: dict[Subset, Mapping[tuple[int, ...], Fraction]] = {}
    for subset in _all_subsets(len(anchor)):
        table: dict[tuple[int, ...], Fraction] = {}
        for subset_state in product(*(alphabets[index] for index in subset)):
            value = Fraction(0)
            for count in range(len(subset) + 1):
                for active_positions in combinations(range(len(subset)), count):
                    active = set(active_positions)
                    full_state = list(anchor)
                    for position, axis in enumerate(subset):
                        if position in active:
                            full_state[axis] = subset_state[position]
                    value += (-1) ** (len(subset) - count) * exact_action[tuple(full_state)]
            table[tuple(subset_state)] = value
        components[subset] = MappingProxyType(table)
    return AnchoredMobiusDecomposition(
        anchor=tuple(anchor),
        action=MappingProxyType(exact_action),
        components=MappingProxyType(components),
    )


__all__ = [
    "AnchoredMobiusDecomposition",
    "CoarseAction",
    "ExactLinearIsomorphism",
    "ExactMarkovChannel",
    "FisherCocycleResidualForms",
    "PosteriorBridge",
    "RetainedBetaDiagnostics",
    "anchored_mobius_decompose",
    "base_fisher_cocycle_residual_forms",
    "conditional_log_laplace_action",
    "identified_linear_step",
    "ordered_derivative_cocycle",
    "posterior_bridge",
    "projection_intertwining_residual",
    "retained_beta_diagnostics",
]
