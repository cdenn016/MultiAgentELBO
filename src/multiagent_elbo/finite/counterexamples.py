"""Exact, deterministic finite counterexample primitives for Session 3.

The module deliberately keeps rational enumeration separate from diagnostics
such as KL, whose logarithms are generally irrational.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
import math
from types import MappingProxyType
from typing import Iterable, Mapping, Sequence


Rational = Fraction


def _fraction(value: object) -> Fraction:
    if isinstance(value, Fraction):
        return value
    return Fraction(value)  # type: ignore[arg-type]


@dataclass(frozen=True)
class EnumerationBounds:
    """Explicit finite-search bounds retained by later artifact publication."""

    max_states: int
    max_denominator: int

    def __post_init__(self) -> None:
        if type(self.max_states) is not int or self.max_states < 1:
            raise ValueError("max_states must be a positive int")
        if type(self.max_denominator) is not int or self.max_denominator < 1:
            raise ValueError("max_denominator must be a positive int")


@dataclass(frozen=True)
class ExactLaw:
    """An immutable normalized rational probability law."""

    masses: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        masses = tuple(_fraction(value) for value in self.masses)
        if not masses or any(value < 0 for value in masses):
            raise ValueError("law masses must be nonnegative and nonempty")
        if sum(masses) != 1:
            raise ValueError("law masses must sum to one")
        object.__setattr__(self, "masses", masses)


@dataclass(frozen=True)
class ExactChannel:
    """A row-stochastic rational Markov channel in source-to-target orientation."""

    rows: tuple[tuple[Fraction, ...], ...]
    target_states: int | None = None

    def __post_init__(self) -> None:
        rows = tuple(tuple(_fraction(value) for value in row) for row in self.rows)
        if not rows:
            raise ValueError("channel must have at least one row")
        width = self.target_states if self.target_states is not None else len(rows[0])
        if type(width) is not int or width < 1:
            raise ValueError("target_states must be a positive int")
        if any(len(row) != width or any(value < 0 for value in row) or sum(row) != 1 for row in rows):
            raise ValueError("channel rows must be nonnegative normalized rows of common width")
        object.__setattr__(self, "rows", rows)
        object.__setattr__(self, "target_states", width)

    @property
    def source_states(self) -> int:
        return len(self.rows)


@dataclass(frozen=True)
class ExtendedRealKL:
    """KL result which represents support failure without arithmetic on infinity."""

    is_infinite: bool
    value: float | None
    support_violations: tuple[int, ...]


@dataclass(frozen=True)
class CandidateRecord:
    """The contract's complete scientific candidate schema, with no extra fields."""

    claim_id: str
    inside_declared_domain: bool
    assumptions_satisfied: bool
    smallest_witness: Mapping[str, object]
    exact_or_numeric: str
    observed_residual: str
    classification: str
    theorem_status: str
    verification_state: str
    claim_origin: str

    def __post_init__(self) -> None:
        if self.theorem_status not in {"ESTABLISHED", "HYPOTHESIS", "CONJECTURE", "NUMERICAL", "OPEN"}:
            raise ValueError("invalid theorem_status")
        if self.verification_state not in {"CANDIDATE", "LLM_SUPPORTED", "EVIDENCE_VERIFIED", "REFUTED", "INCONCLUSIVE"}:
            raise ValueError("invalid verification_state")
        if self.claim_origin not in {"STANDARD", "PROJECT_NOVEL", "APPLICATION_SPECIFIC"}:
            raise ValueError("invalid claim_origin")
        object.__setattr__(self, "smallest_witness", MappingProxyType(dict(self.smallest_witness)))


def _rational_values(max_denominator: int) -> tuple[Fraction, ...]:
    return tuple(sorted({Fraction(n, d) for d in range(1, max_denominator + 1) for n in range(d + 1)}))


def enumerate_rational_laws(max_states: int, max_denominator: int) -> Iterable[ExactLaw]:
    """Yield all rational laws on exactly ``max_states`` ordered states."""
    bounds = EnumerationBounds(max_states, max_denominator)
    values = _rational_values(bounds.max_denominator)
    for masses in product(values, repeat=bounds.max_states):
        if sum(masses) == 1:
            yield ExactLaw(masses)


def enumerate_rational_channels(
    source_states: int, target_states: int, max_denominator: int
) -> Iterable[ExactChannel]:
    """Yield lexicographically ordered normalized channels with bounded rationals."""
    bounds = EnumerationBounds(max(source_states, target_states), max_denominator)
    if type(source_states) is not int or source_states < 1 or type(target_states) is not int or target_states < 1:
        raise ValueError("channel state counts must be positive ints")
    rows = tuple(enumerate_rational_laws(target_states, bounds.max_denominator))
    for selected in product(rows, repeat=source_states):
        yield ExactChannel(tuple(law.masses for law in selected), target_states)


def enumerate_partitions(state_count: int) -> Iterable[tuple[tuple[int, ...], ...]]:
    """Yield set partitions in restricted-growth-string order."""
    if type(state_count) is not int or state_count < 1:
        raise ValueError("state_count must be a positive int")
    def build(index: int, blocks: tuple[tuple[int, ...], ...]) -> Iterable[tuple[tuple[int, ...], ...]]:
        if index == state_count:
            yield blocks
            return
        for block_index in range(len(blocks)):
            updated = list(blocks)
            updated[block_index] = updated[block_index] + (index,)
            yield from build(index + 1, tuple(updated))
        yield from build(index + 1, blocks + ((index,),))
    yield from build(1, ((0,),))


def compose_channels(first: ExactChannel, second: ExactChannel) -> ExactChannel:
    """Compose source->middle then middle->target channels (row-vector convention)."""
    if first.target_states != second.source_states:
        raise ValueError("channels are not compatible for source-to-target composition")
    return ExactChannel(
        tuple(tuple(sum(row[k] * second.rows[k][j] for k in range(first.target_states)) for j in range(second.target_states)) for row in first.rows),
        second.target_states,
    )


def kl_divergence(q: ExactLaw, p: ExactLaw) -> ExtendedRealKL:
    if len(q.masses) != len(p.masses):
        raise ValueError("laws must have equal state counts")
    violations = tuple(index for index, (q_i, p_i) in enumerate(zip(q.masses, p.masses)) if q_i > 0 and p_i == 0)
    if violations:
        return ExtendedRealKL(True, None, violations)
    return ExtendedRealKL(False, sum(float(q_i) * math.log(float(q_i / p_i)) for q_i, p_i in zip(q.masses, p.masses) if q_i), ())


def relabel_law(law: ExactLaw, permutation: Sequence[int]) -> ExactLaw:
    if sorted(permutation) != list(range(len(law.masses))):
        raise ValueError("permutation must relabel every state exactly once")
    return ExactLaw(tuple(law.masses[index] for index in permutation))


def relabel_channel(
    channel: ExactChannel, source_permutation: Sequence[int], target_permutation: Sequence[int]
) -> ExactChannel:
    if sorted(source_permutation) != list(range(channel.source_states)) or sorted(target_permutation) != list(range(channel.target_states)):
        raise ValueError("permutations must coherently cover channel states")
    return ExactChannel(tuple(tuple(channel.rows[source][target] for target in target_permutation) for source in source_permutation), channel.target_states)


def coarsen_marked_event(
    source: ExactLaw, beta: Sequence[Sequence[Fraction]], channel: ExactChannel
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    """Return correct joint-mass pushforward and the deliberately wrong beta-only control."""
    if len(source.masses) != channel.source_states or len(beta) != channel.source_states:
        raise ValueError("source, beta, and channel source sizes must agree")
    event_count = len(beta[0]) if beta else 0
    if event_count < 1 or any(len(row) != event_count or sum(map(_fraction, row)) != 1 for row in beta):
        raise ValueError("beta rows must be normalized with a common event width")
    joint = tuple(sum(source.masses[source_index] * _fraction(beta[source_index][event]) * channel.rows[source_index][target] for source_index in range(channel.source_states) for target in range(channel.target_states)) for event in range(event_count))
    beta_only = tuple(sum(_fraction(beta[source_index][event]) for source_index in range(channel.source_states)) / channel.source_states for event in range(event_count))
    return joint, beta_only


def pairwise_interaction_residual(components: Mapping[tuple[int, ...], Fraction], retained_order: int) -> Fraction:
    if type(retained_order) is not int or retained_order < 0:
        raise ValueError("retained_order must be a nonnegative int")
    return sum(abs(_fraction(value)) for subset, value in components.items() if len(subset) > retained_order)


def fixed_channel_score_gap(theta: Fraction) -> Fraction:
    """Pinned parameter-dependent-channel fixture: independently derived gap 2 theta^2."""
    theta = _fraction(theta)
    if theta < 0 or theta > 1:
        raise ValueError("theta must be a probability parameter")
    return 2 * theta * theta


def _determinant(matrix: Sequence[Sequence[Fraction]]) -> Fraction:
    size = len(matrix)
    if size == 1:
        return _fraction(matrix[0][0])
    return sum(((-1) ** column) * _fraction(matrix[0][column]) * _determinant(tuple(tuple(matrix[row][col] for col in range(size) if col != column) for row in range(1, size))) for column in range(size))


def validate_full_rank_spd(matrix: Sequence[Sequence[Fraction]]) -> int:
    values = tuple(tuple(_fraction(entry) for entry in row) for row in matrix)
    size = len(values)
    if size < 1 or any(len(row) != size for row in values) or any(values[i][j] != values[j][i] for i in range(size) for j in range(size)):
        raise ValueError("SPD matrix must be square and symmetric")
    if any(_determinant(tuple(tuple(values[row][column] for column in range(k)) for row in range(k))) <= 0 for k in range(1, size + 1)):
        raise ValueError("matrix is not positive definite; near-singular inputs require a different model")
    return size


def scale_tolerance(base_tolerance: Fraction, state_count: int) -> Fraction:
    """Exact linear tolerance scaling used by finite stress matrices."""
    tolerance = _fraction(base_tolerance)
    if tolerance < 0 or type(state_count) is not int or state_count < 1:
        raise ValueError("tolerance must be nonnegative and state_count positive")
    return tolerance * state_count


def diagonal_spd_conditioning(diagonal: Sequence[Fraction]) -> Fraction:
    """Exact condition ratio for an explicitly diagonal positive-definite input."""
    values = tuple(_fraction(entry) for entry in diagonal)
    if not values or any(value <= 0 for value in values):
        raise ValueError("diagonal SPD entries must be positive")
    return max(values) / min(values)


def _candidate_key(record: CandidateRecord) -> tuple[object, ...]:
    witness = json.dumps(dict(record.smallest_witness), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return (record.claim_id, witness, record.classification, record.observed_residual)


def minimize_candidates(records: Iterable[CandidateRecord]) -> tuple[CandidateRecord, ...]:
    grouped: dict[str, CandidateRecord] = {}
    for record in records:
        prior = grouped.get(record.claim_id)
        if prior is None or _candidate_key(record) < _candidate_key(prior):
            grouped[record.claim_id] = record
    return tuple(grouped[claim_id] for claim_id in sorted(grouped))


def canonical_candidates_json(records: Iterable[CandidateRecord]) -> str:
    payload = [
        {
            "claim_id": record.claim_id,
            "inside_declared_domain": record.inside_declared_domain,
            "assumptions_satisfied": record.assumptions_satisfied,
            "smallest_witness": dict(record.smallest_witness),
            "exact_or_numeric": record.exact_or_numeric,
            "observed_residual": record.observed_residual,
            "classification": record.classification,
            "theorem_status": record.theorem_status,
            "verification_state": record.verification_state,
            "claim_origin": record.claim_origin,
        }
        for record in minimize_candidates(records)
    ]
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
