"""Independent exact-rational witnesses for the finite theory contracts."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import combinations
from itertools import product
import json
from math import gcd
from math import log
from math import prod
from pathlib import Path
import re


_RATIONAL_LITERAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")
TWO_SCALE_APPLICATION_ID = (
    "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"
)


def parse_fraction_literal(literal: object) -> Fraction:
    """Parse one canonical, reduced rational string without coercion."""

    if not isinstance(literal, str) or _RATIONAL_LITERAL.fullmatch(literal) is None:
        raise TypeError("rational literal must be a canonical string")
    if "/" not in literal:
        return Fraction(int(literal), 1)
    numerator_text, denominator_text = literal.split("/", 1)
    numerator = int(numerator_text)
    denominator = int(denominator_text)
    if gcd(abs(numerator), denominator) != 1:
        raise ValueError("rational literal must be reduced")
    return Fraction(numerator, denominator)


def _require_fraction_tuple(values: object, *, name: str) -> tuple[Fraction, ...]:
    if not isinstance(values, tuple):
        raise TypeError(f"{name} must be a tuple")
    if any(not isinstance(value, Fraction) for value in values):
        raise TypeError(f"{name} entries must be Fraction values")
    return values


@dataclass(frozen=True)
class FractionVector:
    values: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        _require_fraction_tuple(self.values, name="vector")
        if not self.values:
            raise ValueError("vector must be nonempty")

    def __len__(self) -> int:
        return len(self.values)


@dataclass(frozen=True)
class FractionMatrix:
    rows: tuple[tuple[Fraction, ...], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.rows, tuple):
            raise TypeError("matrix rows must be a tuple")
        if not self.rows:
            raise ValueError("matrix must be nonempty")
        widths: list[int] = []
        for row in self.rows:
            _require_fraction_tuple(row, name="matrix row")
            widths.append(len(row))
        if not widths[0] or any(width != widths[0] for width in widths):
            raise ValueError("matrix must be nonempty and rectangular")

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.rows), len(self.rows[0]))


@dataclass(frozen=True)
class FractionTensor:
    shape: tuple[int, ...]
    values: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if (
            not isinstance(self.shape, tuple)
            or not self.shape
            or any(not isinstance(size, int) or isinstance(size, bool) or size <= 0 for size in self.shape)
        ):
            raise ValueError("tensor shape must be a nonempty tuple of positive integers")
        _require_fraction_tuple(self.values, name="tensor values")
        if prod(self.shape) != len(self.values):
            raise ValueError("tensor values do not match shape")

    def at(self, index: tuple[int, ...]) -> Fraction:
        if not isinstance(index, tuple) or len(index) != len(self.shape):
            raise ValueError("tensor index does not match shape")
        offset = 0
        for coordinate, size in zip(index, self.shape, strict=True):
            if not isinstance(coordinate, int) or isinstance(coordinate, bool) or not 0 <= coordinate < size:
                raise IndexError("tensor index is out of bounds")
            offset = offset * size + coordinate
        return self.values[offset]


@dataclass(frozen=True)
class FormalLogTerm:
    atom: Fraction
    coefficient: Fraction


@dataclass(frozen=True)
class FormalLogSum:
    """Canonical sum over prime ``log(p/1)`` atoms."""

    terms: tuple[FormalLogTerm, ...]

    @property
    def term_pairs(self) -> tuple[tuple[Fraction, Fraction], ...]:
        return tuple((term.atom, term.coefficient) for term in self.terms)

    @property
    def is_zero(self) -> bool:
        return not self.terms

    def evaluate_float(self) -> float:
        return sum(float(term.coefficient) * log(float(term.atom)) for term in self.terms)

    def __add__(self, other: FormalLogSum) -> FormalLogSum:
        if not isinstance(other, FormalLogSum):
            return NotImplemented
        return _canonical_log_sum(
            tuple((term.atom, term.coefficient) for term in self.terms + other.terms)
        )

    def __neg__(self) -> FormalLogSum:
        return FormalLogSum(
            tuple(FormalLogTerm(term.atom, -term.coefficient) for term in self.terms)
        )

    def __sub__(self, other: FormalLogSum) -> FormalLogSum:
        return self + (-other)


@dataclass(frozen=True)
class EvidenceELBOOracle:
    evidence_log: FormalLogSum
    elbo: FormalLogSum | float
    kl: FormalLogSum | float
    residual: FormalLogSum | None
    branch: str
    offending_support_entries: tuple[int, ...]


@dataclass(frozen=True)
class FisherDefectOracle:
    joint_weights: FractionMatrix
    coarse_mass: FractionVector
    coarse_scores: FractionMatrix
    fine_fisher: FractionMatrix
    coarse_fisher: FractionMatrix
    defect: FractionMatrix
    conditional_covariance: FractionMatrix
    zero_mass_coarse_score_rows: tuple[int, ...]
    assumption_boundary: str = (
        "finite algebraic identity only; statistical Fisher interpretation requires "
        "a regular DQM family, a parameter-independent normalized channel, and "
        "square-integrable centered score versions; zero rows at zero coarse mass "
        "are nonsemantic version sentinels excluded by every mass-weighted result"
    )


@dataclass(frozen=True)
class MarkedEventPushforward:
    joint: FractionTensor
    coarse_state_mass: FractionVector
    conditional_events: tuple[FractionTensor | None, ...]
    receiver_mass: tuple[FractionVector | None, ...]
    conditional_source: tuple[tuple[FractionVector | None, ...] | None, ...]


@dataclass(frozen=True)
class HoeffdingComponent:
    subset: tuple[int, ...]
    values: FractionTensor


@dataclass(frozen=True)
class HoeffdingOracle:
    components: tuple[HoeffdingComponent, ...]
    reconstruction: FractionTensor
    reconstruction_residual: FractionTensor
    retained_order: int
    retained_values: FractionTensor
    retained_residual: FractionTensor

    def component(self, subset: tuple[int, ...]) -> FractionTensor:
        for component in self.components:
            if component.subset == subset:
                return component.values
        raise KeyError(subset)


@dataclass(frozen=True)
class TwoScaleApplicationOracle:
    application_id: str
    coarse_jacobian: FractionMatrix
    fine_comparison: FractionMatrix
    coarse_comparison: FractionMatrix
    fine_comparison_inverse: FractionMatrix
    coarse_comparison_inverse: FractionMatrix
    left_square: FractionMatrix
    right_square: FractionMatrix
    commutes: bool
    recognition_right_inverse_state: str
    application_theorem_status: str
    application_verification_state: str
    application_claim_origin: str


@dataclass(frozen=True)
class CommutingSquareOracle:
    left: FractionMatrix
    right: FractionMatrix
    commutes: bool


@dataclass(frozen=True)
class CommutingSquareWitness:
    packet_id: str
    coarse_map: FractionMatrix
    fine_comparison: FractionMatrix
    coarse_comparison: FractionMatrix
    lane_private: bool = True
    replacement_application_fixture: bool = False


@dataclass(frozen=True)
class TheoremAssumptionRecord:
    identity_id: str
    premises: tuple[str, ...]
    theory_source: str
    theorem_status: str
    verification_state: str
    claim_origin: str
    evidence_kind: str
    falsification_condition: str


@dataclass(frozen=True)
class AuxiliaryLiteralPacket:
    packet_id: str
    purpose: str
    literals: tuple[tuple[str, tuple[str, ...]], ...]
    lane_private: bool = True
    replacement_application_fixture: bool = False


LANE_PRIVATE_AUXILIARY_PACKETS = (
    AuxiliaryLiteralPacket(
        "oracle_aux_fisher_v1",
        "unequal conditional-weight Fisher witness",
        (
            ("probability", ("1/3", "2/3")),
            ("channel", ("1", "0", "1/4", "3/4")),
            ("score", ("2", "-1")),
        ),
    ),
    AuxiliaryLiteralPacket(
        "oracle_aux_marked_event_v1",
        "asymmetric two-stage state/receiver/source marked-event witness",
        (
            ("state_mass", ("1/3", "2/3")),
            ("conditional_events", ("1", "0", "0", "0", "0", "0", "0", "1")),
            ("state_kernel_stage_1", ("3/4", "1/4", "1/3", "2/3")),
            ("state_kernel_stage_2", ("1/5", "4/5", "3/7", "4/7")),
            ("receiver_kernel_stage_1", ("2/3", "1/3", "1/4", "3/4")),
            ("receiver_kernel_stage_2", ("3/4", "1/4", "2/5", "3/5")),
            ("source_kernel_stage_1", ("3/5", "2/5", "1/6", "5/6")),
            ("source_kernel_stage_2", ("1/3", "2/3", "4/7", "3/7")),
            ("intermediate_state_mass", ("17/36", "19/36")),
            (
                "intermediate_events",
                (
                    "59/255", "61/255", "14/85", "31/85",
                    "28/285", "62/285", "13/95", "52/95",
                ),
            ),
        ),
    ),
    AuxiliaryLiteralPacket(
        "oracle_aux_hoeffding_v1",
        "pure three-spin interaction witness",
        (
            ("action", ("-1", "1", "1", "-1", "1", "-1", "-1", "1")),
            ("axis_0_reference", ("1/2", "1/2")),
            ("axis_1_reference", ("1/2", "1/2")),
            ("axis_2_reference", ("1/2", "1/2")),
            ("retained_order", ("2",)),
        ),
    ),
    AuxiliaryLiteralPacket(
        "oracle_aux_gaussian_v1",
        "exact frame, Galerkin, and Schur witness",
        (
            (
                "fine_precision",
                (
                    "2", "0", "0", "0", "0", "3", "0", "0",
                    "0", "0", "4", "0", "0", "0", "0", "5",
                ),
            ),
            ("prolongator", ("1", "0", "0", "1", "1", "0", "0", "1")),
            (
                "fine_frame",
                (
                    "2", "0", "0", "0", "0", "1", "0", "0",
                    "0", "0", "1", "0", "0", "0", "0", "3",
                ),
            ),
            ("coarse_frame", ("5", "0", "0", "2")),
            (
                "schur_precision",
                ("4", "1", "0", "1", "3", "1", "0", "1", "2"),
            ),
            ("schur_retained", ("0", "2")),
            ("schur_eliminated", ("1",)),
        ),
    ),
)


LANE_PRIVATE_NONIDENTITY_COMMUTING_SQUARE = CommutingSquareWitness(
    packet_id="oracle_aux_nonidentity_commuting_square_v1",
    coarse_map=FractionMatrix(
        (
            (Fraction(1, 2), Fraction(1, 2), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(1, 2), Fraction(1, 2)),
        )
    ),
    fine_comparison=FractionMatrix(
        (
            (Fraction(2), Fraction(0), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(2), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(3), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(0), Fraction(3)),
        )
    ),
    coarse_comparison=FractionMatrix(
        ((Fraction(2), Fraction(0)), (Fraction(0), Fraction(3)))
    ),
)


THEOREM_ASSUMPTION_MATRIX = (
    TheoremAssumptionRecord(
        "evidence_elbo",
        ("positive finite evidence mass", "posterior is normalized evidence slice", "recognition is a probability law"),
        "Theory/05_elbo.tex:180-190,212-274",
        "ESTABLISHED",
        "CANDIDATE",
        "STANDARD",
        "exact_fraction_derivation_witness",
        "A nonzero canonical formal-log residual or mishandled support violation falsifies the encoding.",
    ),
    TheoremAssumptionRecord(
        "fixed_channel_fisher_defect_algebraic",
        (
            "finite normalized source probability law",
            "normalized nonnegative source-row channel",
            "finite centered score array",
            "coarse scores are joint-weighted conditional averages on positive-mass targets",
            "zero-mass coarse-score rows are arbitrary nonsemantic versions excluded by coarse mass",
        ),
        "Theory/05c_pullback_geometry.tex:1078-1152",
        "ESTABLISHED",
        "CANDIDATE",
        "STANDARD",
        "exact_fraction_derivation_witness",
        "A mismatch between the finite Fisher difference and mass-weighted conditional covariance falsifies the algebraic identity.",
    ),
    TheoremAssumptionRecord(
        "fixed_channel_fisher_statistical_interpretation",
        (
            "regular differentiable-in-quadratic-mean statistical family",
            "normalized Markov channel independent of the statistical parameter",
            "square-integrable centered score version",
            "positive-mass conditional disintegration with arbitrary zero-mass versions excluded almost surely",
        ),
        "Theory/05c_pullback_geometry.tex:1078-1152",
        "ESTABLISHED",
        "CANDIDATE",
        "STANDARD",
        "theory_derivation_boundary",
        "A parameter-dependent channel, non-DQM family, non-L2 score, or semantic use of a zero-mass version invalidates the Fisher interpretation.",
    ),
    TheoremAssumptionRecord(
        "marked_event_associativity",
        ("normalized state law", "normalized joint marked-event conditional", "normalized state, receiver, and source kernels"),
        "Theory/07b_agent_network_rg.tex:1748+",
        "ESTABLISHED",
        "CANDIDATE",
        "STANDARD",
        "exact_fraction_derivation_witness",
        "A direct/staged joint-law mismatch or a conditional formed on zero mass falsifies the encoding.",
    ),
    TheoremAssumptionRecord(
        "full_hoeffding_mobius",
        ("finite tensor product state space", "declared normalized product reference", "complete subset family including empty set"),
        "Theory/07b_agent_network_rg.tex:1182-1250,1468-1507",
        "ESTABLISHED",
        "CANDIDATE",
        "STANDARD",
        "exact_fraction_derivation_witness",
        "A nonzero full reconstruction residual or missing higher-order retained residual falsifies the encoding.",
    ),
    TheoremAssumptionRecord(
        "gaussian_inverse_congruence",
        ("invertible rational frame", "square rational precision"),
        "Theory/08_infogeometry.tex:424-431",
        "ESTABLISHED",
        "CANDIDATE",
        "STANDARD",
        "exact_fraction_derivation_witness",
        "Failure of G^-T A G^-1 or its transformed coarse square falsifies the encoding.",
    ),
    TheoremAssumptionRecord(
        "gaussian_galerkin_restriction",
        ("declared prolongator", "compatible square precision"),
        "Theory/09_coarsegraining.tex:50-88",
        "ESTABLISHED",
        "CANDIDATE",
        "STANDARD",
        "exact_fraction_derivation_witness",
        "A result different from S^T A S falsifies the encoding.",
    ),
    TheoremAssumptionRecord(
        "gaussian_schur_complement_algebraic",
        (
            "square rational block matrix",
            "retained/eliminated coordinate partition",
            "invertible eliminated block",
        ),
        "Theory/09_coarsegraining.tex:90-166",
        "ESTABLISHED",
        "CANDIDATE",
        "STANDARD",
        "exact_fraction_derivation_witness",
        "A result different from A_RR-A_RE A_EE^-1 A_ER falsifies the encoding.",
    ),
    TheoremAssumptionRecord(
        "gaussian_schur_gaussian_marginal_interpretation",
        (
            "symmetric positive-definite joint precision",
            "proper nondegenerate Gaussian law",
            "retained/eliminated coordinate partition",
        ),
        "Theory/09_coarsegraining.tex:90-166",
        "ESTABLISHED",
        "CANDIDATE",
        "STANDARD",
        "theory_derivation_boundary",
        "A non-SPD precision, improper Gaussian law, or marginal precision different from the Schur complement invalidates the probabilistic interpretation.",
    ),
    TheoremAssumptionRecord(
        "two_scale_literal_commuting_square",
        ("frozen application fixture", "declared block-average Jacobian", "declared comparison isomorphisms"),
        "Theory/SPEC.md:207+",
        "HYPOTHESIS",
        "CANDIDATE",
        "APPLICATION_SPECIFIC",
        "exact_fraction_derivation_witness",
        "A digest mismatch, noninvertible comparison, or I_c C != C I_f falsifies this application check.",
    ),
)


def _prime_factorization(value: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    divisor = 2
    remainder = value
    while divisor * divisor <= remainder:
        while remainder % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            remainder //= divisor
        divisor += 1
    if remainder > 1:
        factors[remainder] = factors.get(remainder, 0) + 1
    return factors


def _canonical_log_sum(
    pairs: tuple[tuple[Fraction, Fraction], ...],
) -> FormalLogSum:
    coefficients: dict[Fraction, Fraction] = {}
    for atom, coefficient in pairs:
        coefficients[atom] = coefficients.get(atom, Fraction(0)) + coefficient
    return FormalLogSum(
        tuple(
            FormalLogTerm(atom, coefficient)
            for atom, coefficient in sorted(coefficients.items())
            if coefficient
        )
    )


def _formal_rational_log(argument: Fraction, coefficient: Fraction = Fraction(1)) -> FormalLogSum:
    if argument <= 0:
        raise ValueError("formal logarithm argument must be positive")
    pairs: list[tuple[Fraction, Fraction]] = []
    for prime, exponent in _prime_factorization(argument.numerator).items():
        pairs.append((Fraction(prime), coefficient * exponent))
    for prime, exponent in _prime_factorization(argument.denominator).items():
        pairs.append((Fraction(prime), -coefficient * exponent))
    return _canonical_log_sum(tuple(pairs))


def _validate_probability(vector: FractionVector, *, name: str) -> None:
    if any(value < 0 for value in vector.values):
        raise ValueError(f"{name} must be nonnegative")
    if sum(vector.values, Fraction(0)) != 1:
        raise ValueError(f"{name} must sum to one")


def exact_evidence_elbo(
    evidence_submeasure: FractionVector,
    evidence_mass: Fraction,
    posterior: FractionVector,
    recognition: FractionVector,
) -> EvidenceELBOOracle:
    """Return the finite evidence identity as exact formal logarithms."""

    if not isinstance(evidence_mass, Fraction) or evidence_mass <= 0:
        raise ValueError("evidence mass must be a positive Fraction")
    if not (len(evidence_submeasure) == len(posterior) == len(recognition)):
        raise ValueError("evidence, posterior, and recognition lengths must agree")
    if any(value < 0 for value in evidence_submeasure.values):
        raise ValueError("evidence submeasure must be nonnegative")
    if sum(evidence_submeasure.values, Fraction(0)) != evidence_mass:
        raise ValueError("evidence submeasure must sum to evidence mass")
    _validate_probability(posterior, name="posterior")
    _validate_probability(recognition, name="recognition")
    if any(
        evidence != evidence_mass * probability
        for evidence, probability in zip(
            evidence_submeasure.values, posterior.values, strict=True
        )
    ):
        raise ValueError("posterior must normalize the evidence submeasure")

    evidence_log = _formal_rational_log(evidence_mass)
    offending_support_entries = tuple(
        index
        for index, (q, probability) in enumerate(
            zip(recognition.values, posterior.values, strict=True)
        )
        if q > 0 and probability == 0
    )
    if offending_support_entries:
        return EvidenceELBOOracle(
            evidence_log=evidence_log,
            elbo=float("-inf"),
            kl=float("inf"),
            residual=None,
            branch="recognition_not_absolutely_continuous",
            offending_support_entries=offending_support_entries,
        )

    elbo = FormalLogSum(())
    kl = FormalLogSum(())
    for evidence, probability, q in zip(
        evidence_submeasure.values, posterior.values, recognition.values, strict=True
    ):
        if q == 0:
            continue
        elbo = elbo + _formal_rational_log(evidence / q, q)
        kl = kl + _formal_rational_log(q / probability, q)
    residual = evidence_log - elbo - kl
    return EvidenceELBOOracle(
        evidence_log=evidence_log,
        elbo=elbo,
        kl=kl,
        residual=residual,
        branch="finite",
        offending_support_entries=(),
    )


def _matrix_from_rows(rows: list[list[Fraction]]) -> FractionMatrix:
    return FractionMatrix(tuple(tuple(value for value in row) for row in rows))


def _zero_rows(row_count: int, column_count: int) -> list[list[Fraction]]:
    return [[Fraction(0) for _ in range(column_count)] for _ in range(row_count)]


def exact_fisher_defect(
    probability: FractionVector,
    channel: FractionMatrix,
    scores: FractionMatrix,
) -> FisherDefectOracle:
    """Evaluate the fixed-channel score and conditional-covariance identity."""

    _validate_probability(probability, name="fine probability")
    source_count = len(probability)
    if channel.shape[0] != source_count or scores.shape[0] != source_count:
        raise ValueError("channel and score rows must use source-row orientation")
    if any(sum(row, Fraction(0)) != 1 for row in channel.rows):
        raise ValueError("channel must use normalized source-row orientation")
    if any(value < 0 for row in channel.rows for value in row):
        raise ValueError("channel entries must be nonnegative")
    parameter_count = scores.shape[1]
    for parameter in range(parameter_count):
        if sum(
            probability.values[source] * scores.rows[source][parameter]
            for source in range(source_count)
        ) != 0:
            raise ValueError("fine scores must be centered under the fine probability")

    target_count = channel.shape[1]
    joint_rows = [
        [probability.values[source] * channel.rows[source][target] for target in range(target_count)]
        for source in range(source_count)
    ]
    coarse_mass_values = tuple(
        sum((joint_rows[source][target] for source in range(source_count)), Fraction(0))
        for target in range(target_count)
    )
    coarse_score_rows = _zero_rows(target_count, parameter_count)
    for target, mass in enumerate(coarse_mass_values):
        if mass == 0:
            continue
        for parameter in range(parameter_count):
            coarse_score_rows[target][parameter] = sum(
                joint_rows[source][target] * scores.rows[source][parameter]
                for source in range(source_count)
            ) / mass

    fine = _zero_rows(parameter_count, parameter_count)
    coarse = _zero_rows(parameter_count, parameter_count)
    conditional = _zero_rows(parameter_count, parameter_count)
    for left in range(parameter_count):
        for right in range(parameter_count):
            fine[left][right] = sum(
                probability.values[source]
                * scores.rows[source][left]
                * scores.rows[source][right]
                for source in range(source_count)
            )
            coarse[left][right] = sum(
                coarse_mass_values[target]
                * coarse_score_rows[target][left]
                * coarse_score_rows[target][right]
                for target in range(target_count)
            )
            conditional[left][right] = sum(
                joint_rows[source][target]
                * (scores.rows[source][left] - coarse_score_rows[target][left])
                * (scores.rows[source][right] - coarse_score_rows[target][right])
                for source in range(source_count)
                for target in range(target_count)
            )
    defect = [
        [fine[row][column] - coarse[row][column] for column in range(parameter_count)]
        for row in range(parameter_count)
    ]
    return FisherDefectOracle(
        joint_weights=_matrix_from_rows(joint_rows),
        coarse_mass=FractionVector(coarse_mass_values),
        coarse_scores=_matrix_from_rows(coarse_score_rows),
        fine_fisher=_matrix_from_rows(fine),
        coarse_fisher=_matrix_from_rows(coarse),
        defect=_matrix_from_rows(defect),
        conditional_covariance=_matrix_from_rows(conditional),
        zero_mass_coarse_score_rows=tuple(
            target for target, mass in enumerate(coarse_mass_values) if mass == 0
        ),
    )


def _validate_markov_kernel(kernel: FractionMatrix, *, name: str) -> None:
    if any(value < 0 for row in kernel.rows for value in row):
        raise ValueError(f"{name} entries must be nonnegative")
    if any(sum(row, Fraction(0)) != 1 for row in kernel.rows):
        raise ValueError(f"{name} must use normalized source-row orientation")


def compose_markov_kernels(
    first: FractionMatrix, second: FractionMatrix
) -> FractionMatrix:
    """Compose normalized source-row kernels as ``first`` then ``second``."""

    _validate_markov_kernel(first, name="first kernel")
    _validate_markov_kernel(second, name="second kernel")
    if first.shape[1] != second.shape[0]:
        raise ValueError("kernel composition dimensions do not agree")
    rows = [
        [
            sum(
                first.rows[source][middle] * second.rows[middle][target]
                for middle in range(first.shape[1])
            )
            for target in range(second.shape[1])
        ]
        for source in range(first.shape[0])
    ]
    return _matrix_from_rows(rows)


def _validate_conditional_marked_events(
    conditional_events: FractionTensor,
) -> tuple[int, int, int]:
    if len(conditional_events.shape) != 3:
        raise ValueError(
            "conditional marked events must have shape (state, receiver, source)"
        )
    state_count, receiver_count, source_count = conditional_events.shape
    for state in range(state_count):
        state_values = tuple(
            conditional_events.at((state, receiver, source))
            for receiver in range(receiver_count)
            for source in range(source_count)
        )
        if sum(state_values, Fraction(0)) != 1:
            raise ValueError("each conditional marked-event law must sum to one")
        if any(value < 0 for value in state_values):
            raise ValueError("marked-event probabilities must be nonnegative")
    return state_count, receiver_count, source_count


def _validate_marked_pushforward_inputs(
    state_mass: FractionVector,
    conditional_events: FractionTensor,
    state_kernel: FractionMatrix,
    receiver_kernel: FractionMatrix,
    source_kernel: FractionMatrix,
) -> tuple[int, int, int]:
    _validate_probability(state_mass, name="state mass")
    state_count, receiver_count, source_count = _validate_conditional_marked_events(
        conditional_events
    )
    if state_count != len(state_mass):
        raise ValueError("marked-event state axis must match state mass")
    if state_kernel.shape[0] != state_count:
        raise ValueError("state kernel must use state source-row orientation")
    if receiver_kernel.shape[0] != receiver_count:
        raise ValueError("receiver kernel must use receiver source-row orientation")
    if source_kernel.shape[0] != source_count:
        raise ValueError("source kernel must use source source-row orientation")
    _validate_markov_kernel(state_kernel, name="state kernel")
    _validate_markov_kernel(receiver_kernel, name="receiver kernel")
    _validate_markov_kernel(source_kernel, name="source kernel")
    return state_count, receiver_count, source_count


def _push_marked_joint(
    state_mass: FractionVector,
    conditional_events: FractionTensor,
    state_kernel: FractionMatrix,
    receiver_kernel: FractionMatrix,
    source_kernel: FractionMatrix,
    fine_shape: tuple[int, int, int],
) -> FractionTensor:
    state_count, receiver_count, source_count = fine_shape
    coarse_states = state_kernel.shape[1]
    coarse_receivers = receiver_kernel.shape[1]
    coarse_sources = source_kernel.shape[1]
    coarse_shape = (coarse_states, coarse_receivers, coarse_sources)
    return FractionTensor(
        coarse_shape,
        tuple(
            sum(
                state_mass.values[state]
                * conditional_events.at((state, receiver, source))
                * state_kernel.rows[state][coarse_state]
                * receiver_kernel.rows[receiver][coarse_receiver]
                * source_kernel.rows[source][coarse_source]
                for state in range(state_count)
                for receiver in range(receiver_count)
                for source in range(source_count)
            )
            for coarse_state in range(coarse_states)
            for coarse_receiver in range(coarse_receivers)
            for coarse_source in range(coarse_sources)
        ),
    )


def _marked_coarse_state_masses(joint: FractionTensor) -> tuple[Fraction, ...]:
    coarse_states, coarse_receivers, coarse_sources = joint.shape
    return tuple(
        sum(
            (
                joint.at((coarse_state, coarse_receiver, coarse_source))
                for coarse_receiver in range(coarse_receivers)
                for coarse_source in range(coarse_sources)
            ),
            Fraction(0),
        )
        for coarse_state in range(coarse_states)
    )


def _disintegrate_marked_state(
    joint: FractionTensor,
    coarse_state: int,
    mass: Fraction,
) -> tuple[FractionTensor, FractionVector, tuple[FractionVector | None, ...]]:
    _, coarse_receivers, coarse_sources = joint.shape
    event = FractionTensor(
        (coarse_receivers, coarse_sources),
        tuple(
            joint.at((coarse_state, coarse_receiver, coarse_source)) / mass
            for coarse_receiver in range(coarse_receivers)
            for coarse_source in range(coarse_sources)
        ),
    )
    receiver_values = tuple(
        sum(
            (
                event.at((coarse_receiver, coarse_source))
                for coarse_source in range(coarse_sources)
            ),
            Fraction(0),
        )
        for coarse_receiver in range(coarse_receivers)
    )
    source_rows = tuple(
        None
        if receiver_mass == 0
        else FractionVector(
            tuple(
                event.at((coarse_receiver, coarse_source)) / receiver_mass
                for coarse_source in range(coarse_sources)
            )
        )
        for coarse_receiver, receiver_mass in enumerate(receiver_values)
    )
    return event, FractionVector(receiver_values), source_rows


def _disintegrate_marked_joint(
    joint: FractionTensor,
    coarse_state_values: tuple[Fraction, ...],
) -> tuple[
    tuple[FractionTensor | None, ...],
    tuple[FractionVector | None, ...],
    tuple[tuple[FractionVector | None, ...] | None, ...],
]:
    event_conditionals: list[FractionTensor | None] = []
    receiver_masses: list[FractionVector | None] = []
    source_conditionals: list[tuple[FractionVector | None, ...] | None] = []
    for coarse_state, mass in enumerate(coarse_state_values):
        if mass == 0:
            event_conditionals.append(None)
            receiver_masses.append(None)
            source_conditionals.append(None)
            continue
        event, receiver_mass, source_rows = _disintegrate_marked_state(
            joint, coarse_state, mass
        )
        event_conditionals.append(event)
        receiver_masses.append(receiver_mass)
        source_conditionals.append(source_rows)
    return (
        tuple(event_conditionals),
        tuple(receiver_masses),
        tuple(source_conditionals),
    )


def push_marked_event_law(
    state_mass: FractionVector,
    conditional_events: FractionTensor,
    state_kernel: FractionMatrix,
    receiver_kernel: FractionMatrix,
    source_kernel: FractionMatrix,
) -> MarkedEventPushforward:
    """Push ``p(y) eta(i,j|y)`` and only then form positive-mass conditionals."""

    fine_shape = _validate_marked_pushforward_inputs(
        state_mass,
        conditional_events,
        state_kernel,
        receiver_kernel,
        source_kernel,
    )
    joint = _push_marked_joint(
        state_mass,
        conditional_events,
        state_kernel,
        receiver_kernel,
        source_kernel,
        fine_shape,
    )
    coarse_state_values = _marked_coarse_state_masses(joint)
    event_conditionals, receiver_masses, source_conditionals = (
        _disintegrate_marked_joint(joint, coarse_state_values)
    )
    return MarkedEventPushforward(
        joint=joint,
        coarse_state_mass=FractionVector(coarse_state_values),
        conditional_events=event_conditionals,
        receiver_mass=receiver_masses,
        conditional_source=source_conditionals,
    )


def _all_subsets(axes: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        subset
        for size in range(len(axes) + 1)
        for subset in combinations(axes, size)
    )


def _validate_hoeffding_inputs(
    values: FractionTensor,
    product_reference: tuple[FractionVector, ...],
    retained_order: int,
) -> tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    if not isinstance(product_reference, tuple):
        raise TypeError("product reference must be a tuple")
    axis_count = len(values.shape)
    if len(product_reference) != axis_count:
        raise ValueError("one product reference is required per tensor axis")
    for axis, reference in enumerate(product_reference):
        if not isinstance(reference, FractionVector):
            raise TypeError("product references must be FractionVector values")
        if len(reference) != values.shape[axis]:
            raise ValueError("product reference length must match its tensor axis")
        _validate_probability(reference, name="product reference")
    if (
        not isinstance(retained_order, int)
        or isinstance(retained_order, bool)
        or not 0 <= retained_order <= axis_count
    ):
        raise ValueError("retained order must be an integer between zero and tensor rank")
    axes = tuple(range(axis_count))
    indices = tuple(product(*(range(size) for size in values.shape)))
    return axes, indices


def _conditional_projection(
    values: FractionTensor,
    product_reference: tuple[FractionVector, ...],
    axes: tuple[int, ...],
    indices: tuple[tuple[int, ...], ...],
    subset: tuple[int, ...],
) -> tuple[Fraction, ...]:
    active = frozenset(subset)
    return tuple(
        sum(
            values.at(integrated_index)
            * prod(
                product_reference[axis].values[integrated_index[axis]]
                for axis in axes
                if axis not in active
            )
            for integrated_index in indices
            if all(
                integrated_index[axis] == fixed_index[axis] for axis in active
            )
        )
        for fixed_index in indices
    )


def _build_hoeffding_components(
    values: FractionTensor,
    product_reference: tuple[FractionVector, ...],
    axes: tuple[int, ...],
    indices: tuple[tuple[int, ...], ...],
) -> tuple[HoeffdingComponent, ...]:
    projections = {
        subset: _conditional_projection(
            values, product_reference, axes, indices, subset
        )
        for subset in _all_subsets(axes)
    }
    components: list[HoeffdingComponent] = []
    for subset in _all_subsets(axes):
        component_values = [Fraction(0) for _ in indices]
        for inner in _all_subsets(subset):
            sign = -1 if (len(subset) - len(inner)) % 2 else 1
            for position, value in enumerate(projections[inner]):
                component_values[position] += sign * value
        components.append(
            HoeffdingComponent(
                subset, FractionTensor(values.shape, tuple(component_values))
            )
        )
    return tuple(components)


def _sum_hoeffding_components(
    components: tuple[HoeffdingComponent, ...],
    value_count: int,
    *,
    maximum_order: int | None = None,
) -> tuple[Fraction, ...]:
    included = tuple(
        component
        for component in components
        if maximum_order is None or len(component.subset) <= maximum_order
    )
    return tuple(
        sum(
            (component.values.values[position] for component in included),
            Fraction(0),
        )
        for position in range(value_count)
    )


def _tensor_value_difference(
    left: tuple[Fraction, ...], right: tuple[Fraction, ...]
) -> tuple[Fraction, ...]:
    return tuple(
        left_value - right_value
        for left_value, right_value in zip(left, right, strict=True)
    )


def exact_hoeffding_decomposition(
    values: FractionTensor,
    product_reference: tuple[FractionVector, ...],
    retained_order: int,
) -> HoeffdingOracle:
    """Compute every finite Hoeffding/Mobius component over a product law."""

    axes, indices = _validate_hoeffding_inputs(
        values, product_reference, retained_order
    )
    components = _build_hoeffding_components(
        values, product_reference, axes, indices
    )
    reconstruction_values = _sum_hoeffding_components(
        components, len(values.values)
    )
    retained_values = _sum_hoeffding_components(
        components, len(values.values), maximum_order=retained_order
    )
    return HoeffdingOracle(
        components=components,
        reconstruction=FractionTensor(values.shape, reconstruction_values),
        reconstruction_residual=FractionTensor(
            values.shape,
            _tensor_value_difference(values.values, reconstruction_values),
        ),
        retained_order=retained_order,
        retained_values=FractionTensor(values.shape, retained_values),
        retained_residual=FractionTensor(
            values.shape,
            _tensor_value_difference(values.values, retained_values),
        ),
    )


def matrix_transpose(matrix: FractionMatrix) -> FractionMatrix:
    return FractionMatrix(
        tuple(
            tuple(matrix.rows[row][column] for row in range(matrix.shape[0]))
            for column in range(matrix.shape[1])
        )
    )


def matrix_multiply(left: FractionMatrix, right: FractionMatrix) -> FractionMatrix:
    if left.shape[1] != right.shape[0]:
        raise ValueError("matrix multiplication dimensions do not agree")
    return FractionMatrix(
        tuple(
            tuple(
                sum(
                    (
                        left.rows[row][inner] * right.rows[inner][column]
                        for inner in range(left.shape[1])
                    ),
                    Fraction(0),
                )
                for column in range(right.shape[1])
            )
            for row in range(left.shape[0])
        )
    )


def evaluate_commuting_square(
    coarse_map: FractionMatrix,
    fine_comparison: FractionMatrix,
    coarse_comparison: FractionMatrix,
) -> CommutingSquareOracle:
    """Evaluate ``I_c C`` and ``C I_f`` without assuming they commute."""

    if coarse_comparison.shape[1] != coarse_map.shape[0]:
        raise ValueError("coarse comparison cannot left-compose with coarse map")
    if coarse_map.shape[1] != fine_comparison.shape[0]:
        raise ValueError("fine comparison cannot right-compose with coarse map")
    left = matrix_multiply(coarse_comparison, coarse_map)
    right = matrix_multiply(coarse_map, fine_comparison)
    return CommutingSquareOracle(left=left, right=right, commutes=left == right)


def exact_matrix_inverse(matrix: FractionMatrix) -> FractionMatrix:
    """Invert a rational square matrix by exact Gauss-Jordan elimination."""

    row_count, column_count = matrix.shape
    if row_count != column_count:
        raise ValueError("matrix inverse requires a square matrix")
    augmented = [
        list(row)
        + [Fraction(1 if row_index == column_index else 0) for column_index in range(row_count)]
        for row_index, row in enumerate(matrix.rows)
    ]
    for pivot_column in range(row_count):
        pivot_row = next(
            (
                row
                for row in range(pivot_column, row_count)
                if augmented[row][pivot_column] != 0
            ),
            None,
        )
        if pivot_row is None:
            raise ValueError("matrix is singular")
        if pivot_row != pivot_column:
            augmented[pivot_column], augmented[pivot_row] = (
                augmented[pivot_row],
                augmented[pivot_column],
            )
        pivot = augmented[pivot_column][pivot_column]
        augmented[pivot_column] = [value / pivot for value in augmented[pivot_column]]
        for row in range(row_count):
            if row == pivot_column:
                continue
            multiplier = augmented[row][pivot_column]
            if multiplier == 0:
                continue
            augmented[row] = [
                value - multiplier * pivot_value
                for value, pivot_value in zip(
                    augmented[row], augmented[pivot_column], strict=True
                )
            ]
    return FractionMatrix(
        tuple(tuple(row[row_count:]) for row in augmented)
    )


def inverse_congruence(
    matrix: FractionMatrix, frame: FractionMatrix
) -> FractionMatrix:
    """Return ``G^{-T} matrix G^{-1}`` for a coordinate frame ``G``."""

    if matrix.shape[0] != matrix.shape[1] or frame.shape != matrix.shape:
        raise ValueError("inverse congruence requires equally sized square matrices")
    inverse_frame = exact_matrix_inverse(frame)
    return matrix_multiply(
        matrix_transpose(inverse_frame), matrix_multiply(matrix, inverse_frame)
    )


def transform_prolongator(
    prolongator: FractionMatrix,
    fine_frame: FractionMatrix,
    coarse_frame: FractionMatrix,
    *,
    hold_fixed: bool = False,
) -> FractionMatrix:
    """Transform ``S`` as ``G_f S G_c^{-1}``, checking a requested fixed ``S``."""

    if fine_frame.shape != (prolongator.shape[0], prolongator.shape[0]):
        raise ValueError("fine frame shape does not match prolongator")
    if coarse_frame.shape != (prolongator.shape[1], prolongator.shape[1]):
        raise ValueError("coarse frame shape does not match prolongator")
    if hold_fixed:
        if matrix_multiply(fine_frame, prolongator) != matrix_multiply(
            prolongator, coarse_frame
        ):
            raise ValueError("fixed prolongator does not intertwine the frames")
        return prolongator
    return matrix_multiply(
        matrix_multiply(fine_frame, prolongator), exact_matrix_inverse(coarse_frame)
    )


def galerkin_restriction(
    precision: FractionMatrix, prolongator: FractionMatrix
) -> FractionMatrix:
    if precision.shape[0] != precision.shape[1]:
        raise ValueError("Galerkin precision must be square")
    if precision.shape[0] != prolongator.shape[0]:
        raise ValueError("Galerkin precision and prolongator dimensions do not agree")
    return matrix_multiply(
        matrix_transpose(prolongator), matrix_multiply(precision, prolongator)
    )


def _submatrix(
    matrix: FractionMatrix, rows: tuple[int, ...], columns: tuple[int, ...]
) -> FractionMatrix:
    return FractionMatrix(
        tuple(tuple(matrix.rows[row][column] for column in columns) for row in rows)
    )


def _matrix_subtract(left: FractionMatrix, right: FractionMatrix) -> FractionMatrix:
    if left.shape != right.shape:
        raise ValueError("matrix subtraction dimensions do not agree")
    return FractionMatrix(
        tuple(
            tuple(
                left.rows[row][column] - right.rows[row][column]
                for column in range(left.shape[1])
            )
            for row in range(left.shape[0])
        )
    )


def schur_complement(
    matrix: FractionMatrix,
    *,
    retained: tuple[int, ...],
    eliminated: tuple[int, ...],
) -> FractionMatrix:
    """Marginalize ``eliminated`` coordinates by an exact Schur complement."""

    size = matrix.shape[0]
    if matrix.shape[1] != size:
        raise ValueError("Schur complement requires a square matrix")
    if not retained or not eliminated:
        raise ValueError("Schur complement requires retained and eliminated indices")
    if (
        any(not isinstance(index, int) or isinstance(index, bool) for index in retained + eliminated)
        or len(set(retained + eliminated)) != size
        or set(retained + eliminated) != set(range(size))
    ):
        raise ValueError("retained and eliminated indices must partition the matrix")
    rr = _submatrix(matrix, retained, retained)
    re = _submatrix(matrix, retained, eliminated)
    ee = _submatrix(matrix, eliminated, eliminated)
    er = _submatrix(matrix, eliminated, retained)
    correction = matrix_multiply(
        re, matrix_multiply(exact_matrix_inverse(ee), er)
    )
    return _matrix_subtract(rr, correction)


def _literal_vector(raw: object, *, name: str) -> FractionVector:
    if not isinstance(raw, list):
        raise TypeError(f"{name} must be a JSON array of rational literals")
    return FractionVector(tuple(parse_fraction_literal(value) for value in raw))


def _literal_matrix(raw: object, *, name: str) -> FractionMatrix:
    if not isinstance(raw, list) or any(not isinstance(row, list) for row in raw):
        raise TypeError(f"{name} must be a JSON matrix of rational literals")
    return FractionMatrix(
        tuple(
            tuple(parse_fraction_literal(value) for value in row)
            for row in raw
        )
    )


@dataclass(frozen=True)
class _TwoScaleFixtureLiterals:
    channel: FractionMatrix
    coarse_jacobian: FractionMatrix
    fine_comparison: FractionMatrix
    coarse_comparison: FractionMatrix
    fine_factors: FractionMatrix
    coarse_factors: FractionMatrix
    fine_reference: FractionVector
    coarse_reference: FractionVector
    baseline: FractionVector
    observation_kernel: FractionMatrix
    evidence: FractionVector
    evidence_mass: Fraction
    posterior: FractionVector
    fine_recognition: FractionVector
    coarse_recognition: FractionVector


def _read_two_scale_payload(path: Path) -> dict[str, object]:
    if not isinstance(path, Path):
        raise TypeError("fixture path must be pathlib.Path")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("fixture root must be a JSON object")
    if payload.get("schema_version") != "two-scale-application-v1":
        raise ValueError("unexpected two-scale application schema")
    return payload


def _single_scale_arrow(payload: dict[str, object]) -> dict[str, object]:
    arrows = payload["channel"]["arrows"]
    if not isinstance(arrows, list) or len(arrows) != 1:
        raise ValueError("fixture must declare exactly one scale arrow")
    arrow = arrows[0]
    if not isinstance(arrow, dict):
        raise ValueError("scale arrow must be a JSON object")
    return arrow


def _parse_two_scale_literals(
    payload: dict[str, object], arrow: dict[str, object]
) -> _TwoScaleFixtureLiterals:
    configuration = payload["configuration"]
    comparisons = configuration["comparison_isomorphisms"]
    references = payload["reference_laws"]
    generative = payload["generative_structure"]
    recognition = payload["recognition"]
    return _TwoScaleFixtureLiterals(
        channel=_literal_matrix(arrow["rows"], name="fine-to-coarse channel"),
        coarse_jacobian=_literal_matrix(
            configuration["coarse_map_matrix"], name="coarse coordinate Jacobian"
        ),
        fine_comparison=_literal_matrix(
            comparisons["fine"], name="fine comparison isomorphism"
        ),
        coarse_comparison=_literal_matrix(
            comparisons["coarse"], name="coarse comparison isomorphism"
        ),
        fine_factors=_literal_matrix(
            references["fine"]["factor_values"], name="fine product factors"
        ),
        coarse_factors=_literal_matrix(
            references["coarse"]["factor_values"], name="coarse product factors"
        ),
        fine_reference=_literal_vector(
            references["fine"]["values"], name="fine reference"
        ),
        coarse_reference=_literal_vector(
            references["coarse"]["values"], name="coarse reference"
        ),
        baseline=_literal_vector(
            generative["correlated_baseline"], name="correlated baseline"
        ),
        observation_kernel=_literal_matrix(
            generative["observation_record_kernel"], name="observation record kernel"
        ),
        evidence=_literal_vector(
            generative["evidence_submeasure"], name="evidence submeasure"
        ),
        evidence_mass=parse_fraction_literal(generative["evidence_mass"]),
        posterior=_literal_vector(generative["posterior"], name="posterior"),
        fine_recognition=_literal_vector(
            recognition["fine_law"], name="fine recognition law"
        ),
        coarse_recognition=_literal_vector(
            recognition["coarse_law"], name="coarse recognition law"
        ),
    )


def _validate_fixture_channel_and_shapes(
    arrow: dict[str, object], literals: _TwoScaleFixtureLiterals
) -> None:
    source_labels = arrow["source_labels"]
    target_labels = arrow["target_labels"]
    if literals.channel.shape != (len(source_labels), len(target_labels)):
        raise ValueError("fine-to-coarse channel must use source-row orientation")
    _validate_markov_kernel(literals.channel, name="fine-to-coarse channel")
    if literals.coarse_jacobian.shape != (2, 4):
        raise ValueError("coarse coordinate Jacobian must have shape (2, 4)")
    if (
        literals.fine_comparison.shape != (4, 4)
        or literals.coarse_comparison.shape != (2, 2)
    ):
        raise ValueError("declared comparison map shapes do not match the coordinates")


def _validate_fixture_probability_literals(
    literals: _TwoScaleFixtureLiterals,
) -> None:
    for factors, name in (
        (literals.fine_factors, "fine product factors"),
        (literals.coarse_factors, "coarse product factors"),
    ):
        if any(sum(row, Fraction(0)) != 1 for row in factors.rows):
            raise ValueError(f"{name} rows must sum to one")
    for law, name in (
        (literals.fine_reference, "fine reference"),
        (literals.coarse_reference, "coarse reference"),
        (literals.baseline, "correlated baseline"),
        (literals.posterior, "posterior"),
        (literals.fine_recognition, "fine recognition law"),
        (literals.coarse_recognition, "coarse recognition law"),
    ):
        _validate_probability(law, name=name)
    _validate_markov_kernel(
        literals.observation_kernel, name="observation record kernel"
    )


def _validate_fixture_evidence(literals: _TwoScaleFixtureLiterals) -> None:
    if (
        literals.evidence_mass <= 0
        or sum(literals.evidence.values, Fraction(0)) != literals.evidence_mass
    ):
        raise ValueError("evidence submeasure does not match evidence mass")
    if any(
        evidence_value != literals.evidence_mass * posterior_value
        for evidence_value, posterior_value in zip(
            literals.evidence.values, literals.posterior.values, strict=True
        )
    ):
        raise ValueError("posterior does not normalize the evidence submeasure")


def _canonical_fixture_digest(payload: dict[str, object]) -> str:
    canonical_payload = {
        key: value for key, value in payload.items() if key != "application_id"
    }
    digest = hashlib.sha256(
        json.dumps(
            canonical_payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
    ).hexdigest()
    if payload.get("application_id") != digest or digest != TWO_SCALE_APPLICATION_ID:
        raise ValueError("two-scale application ID does not match canonical fixture digest")
    return digest


def _fixture_boundary_metadata(
    payload: dict[str, object],
) -> tuple[str, dict[str, str]]:
    right_inverse_state = payload["recognition"]["right_inverse"]["check_state"]
    conclusion = payload["claims"]["checked_conclusions"][0]
    if right_inverse_state != "NOT_CHECKED":
        raise ValueError("recognition right-inverse state must remain NOT_CHECKED")
    if (
        conclusion["check_state"] != "NOT_CHECKED"
        or conclusion["theorem_status"] != "HYPOTHESIS"
        or conclusion["verification_state"] != "CANDIDATE"
        or conclusion["claim_origin"] != "APPLICATION_SPECIFIC"
    ):
        raise ValueError("application premise metadata crossed its frozen boundary")
    return right_inverse_state, conclusion


def load_two_scale_application(path: Path) -> TwoScaleApplicationOracle:
    """Parse and validate the frozen two-scale application as exact literals."""

    payload = _read_two_scale_payload(path)
    arrow = _single_scale_arrow(payload)
    literals = _parse_two_scale_literals(payload, arrow)
    _validate_fixture_channel_and_shapes(arrow, literals)
    _validate_fixture_probability_literals(literals)
    _validate_fixture_evidence(literals)
    digest = _canonical_fixture_digest(payload)
    right_inverse_state, conclusion = _fixture_boundary_metadata(payload)
    fine_inverse = exact_matrix_inverse(literals.fine_comparison)
    coarse_inverse = exact_matrix_inverse(literals.coarse_comparison)
    square = evaluate_commuting_square(
        literals.coarse_jacobian,
        literals.fine_comparison,
        literals.coarse_comparison,
    )
    return TwoScaleApplicationOracle(
        application_id=digest,
        coarse_jacobian=literals.coarse_jacobian,
        fine_comparison=literals.fine_comparison,
        coarse_comparison=literals.coarse_comparison,
        fine_comparison_inverse=fine_inverse,
        coarse_comparison_inverse=coarse_inverse,
        left_square=square.left,
        right_square=square.right,
        commutes=square.commutes,
        recognition_right_inverse_state=right_inverse_state,
        application_theorem_status=conclusion["theorem_status"],
        application_verification_state=conclusion["verification_state"],
        application_claim_origin=conclusion["claim_origin"],
    )
