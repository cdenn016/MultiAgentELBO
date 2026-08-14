"""Exact finite controls for the canonical-dependence selection boundary.

Every algebraic result in this module uses :class:`fractions.Fraction`.
The executable controls corroborate the accompanying proofs; finite
enumeration does not replace those proofs.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from typing import Iterable, Sequence


BinaryLaw = tuple[Fraction, Fraction]
JointLaw = tuple[Fraction, Fraction, Fraction, Fraction]
SIX_BIT_STATES = tuple(itertools.product((0, 1), repeat=6))


def _fraction(value: Fraction | int) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def _validate_law(law: Sequence[Fraction], *, name: str) -> tuple[Fraction, ...]:
    result = tuple(_fraction(atom) for atom in law)
    if not result:
        raise ValueError(f"{name} must not be empty")
    if any(atom < 0 for atom in result):
        raise ValueError(f"{name} must be nonnegative")
    if sum(result, Fraction(0)) != 1:
        raise ValueError(f"{name} must be normalized")
    return result


def q_rho(rho: Fraction) -> JointLaw:
    """Return the strictly positive binary correlation family in 00,01,10,11 order."""
    rho = _fraction(rho)
    if not -1 < rho < 1:
        raise ValueError("the strictly positive witness requires -1 < rho < 1")
    return (
        (1 + rho) / 4,
        (1 - rho) / 4,
        (1 - rho) / 4,
        (1 + rho) / 4,
    )


def singleton_marginals(law: Sequence[Fraction]) -> tuple[BinaryLaw, BinaryLaw]:
    """Marginalize a two-bit law given in 00,01,10,11 order."""
    joint = _validate_law(law, name="joint law")
    if len(joint) != 4:
        raise ValueError("a two-bit joint law must have four atoms")
    return (
        (joint[0] + joint[1], joint[2] + joint[3]),
        (joint[0] + joint[2], joint[1] + joint[3]),
    )


def product_coupling(left: Sequence[Fraction], right: Sequence[Fraction]) -> JointLaw:
    """Form the product coupling of two binary laws."""
    left_law = _validate_law(left, name="left law")
    right_law = _validate_law(right, name="right law")
    if len(left_law) != 2 or len(right_law) != 2:
        raise ValueError("product_coupling expects two binary laws")
    return tuple(
        left_law[left_bit] * right_law[right_bit]
        for left_bit, right_bit in ((0, 0), (0, 1), (1, 0), (1, 1))
    )  # type: ignore[return-value]


def preparation_pushforward(
    left: Sequence[Fraction], right: Sequence[Fraction]
) -> JointLaw:
    """Push the singleton law through independent preparation kernels."""
    left_law = _validate_law(left, name="left preparation")
    right_law = _validate_law(right, name="right preparation")
    if len(left_law) != 2 or len(right_law) != 2:
        raise ValueError("preparation kernels must have binary targets")
    source = (Fraction(1),)
    atoms = []
    for left_bit, right_bit in ((0, 0), (0, 1), (1, 0), (1, 1)):
        atoms.append(source[0] * left_law[left_bit] * right_law[right_bit])
    return tuple(atoms)  # type: ignore[return-value]


def split_pushforward(rho: Fraction) -> JointLaw:
    """Push a fair bit through the correlation split y=x, z=x with bias rho."""
    rho = _fraction(rho)
    if not -1 < rho < 1:
        raise ValueError("the strictly positive split output requires -1 < rho < 1")
    source = (Fraction(1, 2), Fraction(1, 2))
    output = [Fraction(0) for _ in range(4)]
    for source_bit, source_mass in enumerate(source):
        for z_bit in (0, 1):
            agreement = z_bit == source_bit
            conditional = (1 + rho) / 2 if agreement else (1 - rho) / 2
            output[2 * source_bit + z_bit] += source_mass * conditional
    return tuple(output)  # type: ignore[return-value]


def faithful_quasi_inverse_counterexample(
    first_rho: Fraction, second_rho: Fraction
) -> dict[str, object]:
    """Exhibit two relabeling-inequivalent joints with identical marginals."""
    first = q_rho(first_rho)
    second = q_rho(second_rho)
    first_marginals = singleton_marginals(first)
    second_marginals = singleton_marginals(second)
    return {
        "distinct_joints": first != second,
        "distinct_relabeling_orbits": sorted(first) != sorted(second),
        "first": first,
        "marginals": first_marginals,
        "same_marginals": first_marginals == second_marginals,
        "second": second,
    }


def _dependence_atom_derivatives(
    rho: Fraction,
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Return the four atom derivatives for the declared correlation parameter."""
    _fraction(rho)
    return (
        Fraction(1, 4),
        Fraction(-1, 4),
        Fraction(-1, 4),
        Fraction(1, 4),
    )


def dependence_fisher(rho: Fraction) -> Fraction:
    """Compute dependence Fisher information from categorical atom scores."""
    law = q_rho(rho)
    derivatives = _dependence_atom_derivatives(rho)
    if sum(derivatives, Fraction(0)) != 0:
        raise AssertionError("categorical atom derivatives must sum to zero")
    return sum(
        (derivative * derivative) / atom
        for atom, derivative in zip(law, derivatives, strict=True)
    )


def pushforward(
    law: Sequence[Fraction], coarse_map: Sequence[int], cell_count: int
) -> tuple[Fraction, ...]:
    """Push a finite law through a deterministic map."""
    source = _validate_law(law, name="source law")
    if len(source) != len(coarse_map):
        raise ValueError("coarse_map must have one cell for every source atom")
    if cell_count <= 0:
        raise ValueError("cell_count must be positive")
    if any(not isinstance(cell, int) or not 0 <= cell < cell_count for cell in coarse_map):
        raise ValueError("coarse_map contains an out-of-range cell")
    result = [Fraction(0) for _ in range(cell_count)]
    for atom, cell in zip(source, coarse_map, strict=True):
        result[cell] += atom
    return tuple(result)


def deterministic_completion(
    reference: Sequence[Fraction],
    coarse_map: Sequence[int],
    target: Sequence[Fraction],
) -> tuple[Fraction, ...]:
    """Return the exact reference-posterior completion along a deterministic map."""
    reference_law = _validate_law(reference, name="reference law")
    target_law = _validate_law(target, name="target law")
    if len(reference_law) != len(coarse_map):
        raise ValueError("coarse_map must have one cell for every reference atom")
    pushed_reference = pushforward(reference_law, coarse_map, len(target_law))
    for cell, reference_mass in enumerate(pushed_reference):
        if reference_mass == 0 and target_law[cell] != 0:
            raise ValueError("target charges a zero-reference coarse cell")
    completed = tuple(
        Fraction(0)
        if pushed_reference[cell] == 0
        else target_law[cell] * atom / pushed_reference[cell]
        for atom, cell in zip(reference_law, coarse_map, strict=True)
    )
    if sum(completed, Fraction(0)) != 1:
        raise AssertionError("completion lost normalization")
    if pushforward(completed, coarse_map, len(target_law)) != target_law:
        raise AssertionError("completion does not push forward to the target")
    return completed


def completion_conditional_defect(
    reference: Sequence[Fraction],
    coarse_map: Sequence[int],
    target: Sequence[Fraction],
    candidate: Sequence[Fraction],
) -> Fraction:
    """Return the exact within-cell cross-product conditional defect."""
    reference_law = _validate_law(reference, name="reference law")
    target_law = _validate_law(target, name="target law")
    candidate_law = _validate_law(candidate, name="candidate law")
    if len(reference_law) != len(coarse_map) or len(candidate_law) != len(coarse_map):
        raise ValueError("map, reference, and candidate lengths must agree")
    if pushforward(candidate_law, coarse_map, len(target_law)) != target_law:
        raise ValueError("candidate is not feasible for the declared target")
    selected = deterministic_completion(reference_law, coarse_map, target_law)
    defect = Fraction(0)
    for first in range(len(candidate_law)):
        for second in range(first + 1, len(candidate_law)):
            if coarse_map[first] != coarse_map[second]:
                continue
            cross_product = (
                candidate_law[first] * reference_law[second]
                - candidate_law[second] * reference_law[first]
            )
            defect += cross_product * cross_product
    if candidate_law == selected and defect != 0:
        raise AssertionError("selected completion has nonzero conditional defect")
    return defect


def reference_selector_control(rho: Fraction) -> dict[str, object]:
    """Show that a feasible positive reference selects its own dependence."""
    reference = q_rho(rho)
    target = singleton_marginals(reference)
    return {
        "feasible": target == (
            (Fraction(1, 2), Fraction(1, 2)),
            (Fraction(1, 2), Fraction(1, 2)),
        ),
        "marginal_target": target,
        "reference": reference,
        "selected": reference,
    }


def matrix_rank(matrix: Iterable[Sequence[Fraction]]) -> int:
    """Compute matrix rank by fraction-preserving Gaussian elimination."""
    work = [list(map(_fraction, row)) for row in matrix]
    if not work:
        return 0
    width = len(work[0])
    if any(len(row) != width for row in work):
        raise ValueError("matrix rows must have equal length")
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column] != 0),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def bsc_retained_quotient(a: Fraction, b: Fraction) -> dict[str, object]:
    """Return the exact rank-one Fisher pullback for a retained BSC law."""
    a = _fraction(a)
    b = _fraction(b)
    retained_probability = a + b - 2 * a * b
    if not 0 < retained_probability < 1:
        raise ValueError("the retained Bernoulli law must be strictly positive")
    jacobian = (1 - 2 * b, 1 - 2 * a, Fraction(0))
    denominator = retained_probability * (1 - retained_probability)
    fisher_pullback = tuple(
        tuple(row_entry * column_entry / denominator for column_entry in jacobian)
        for row_entry in jacobian
    )
    kernel_vectors = (
        (1 - 2 * a, -(1 - 2 * b), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    )
    return {
        "fisher_pullback": fisher_pullback,
        "jacobian": jacobian,
        "kernel_vectors": kernel_vectors,
        "retained_probability": retained_probability,
        "retained_rank": matrix_rank(fisher_pullback),
    }


def _product(values: Iterable[Fraction]) -> Fraction:
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def _parity(state: Sequence[int]) -> int:
    return -1 if sum(state) % 2 else 1


def _product_probability(theta: Sequence[Fraction], state: Sequence[int]) -> Fraction:
    return _product(
        parameter if bit else 1 - parameter
        for parameter, bit in zip(theta, state, strict=True)
    )


def _theta_derivative(
    theta: Sequence[Fraction], kappa: Fraction, state: Sequence[int], coordinate: int
) -> Fraction:
    product_term = _product_probability(theta, state)
    parameter = theta[coordinate]
    product_score = Fraction(1, parameter) if state[coordinate] else -Fraction(1, 1 - parameter)
    determinant = _product(value * (1 - value) for value in theta)
    determinant_derivative = determinant * Fraction(
        1 - 2 * parameter, parameter * (1 - parameter)
    )
    return product_term * product_score + kappa * _parity(state) * determinant_derivative


def promoted_parity_rank() -> dict[str, object]:
    """Build exact full-joint and singleton derivative matrices for (theta,kappa)."""
    theta = (Fraction(1, 2),) * 6
    kappa = Fraction(1, 2)
    determinant = _product(value * (1 - value) for value in theta)
    full_joint_derivative = tuple(
        tuple(_theta_derivative(theta, kappa, state, coordinate) for coordinate in range(6))
        + (Fraction(_parity(state)) * determinant,)
        for state in SIX_BIT_STATES
    )
    singleton_derivative = tuple(
        tuple(Fraction(1) if row == column else Fraction(0) for column in range(6))
        + (Fraction(0),)
        for row in range(6)
    )
    return {
        "full_joint_derivative": full_joint_derivative,
        "full_joint_derivative_rank": matrix_rank(full_joint_derivative),
        "singleton_derivative": singleton_derivative,
        "singleton_derivative_rank": matrix_rank(singleton_derivative),
        "singleton_kernel_generator": (Fraction(0),) * 6 + (Fraction(1),),
    }


def _jsonable(value: object) -> object:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def main() -> int:
    """Print one deterministic JSON document containing the exact controls."""
    parity = promoted_parity_rank()
    payload = {
        "binary": faithful_quasi_inverse_counterexample(Fraction(1, 3), Fraction(1, 2)),
        "bsc": bsc_retained_quotient(Fraction(1, 5), Fraction(1, 4)),
        "dependence_fisher": {
            "rho_1_2": dependence_fisher(Fraction(1, 2)),
            "rho_1_3": dependence_fisher(Fraction(1, 3)),
        },
        "parity_rank": {
            "full_joint": parity["full_joint_derivative_rank"],
            "singleton": parity["singleton_derivative_rank"],
            "singleton_kernel_generator": parity["singleton_kernel_generator"],
        },
        "reference_selector": reference_selector_control(Fraction(1, 3)),
    }
    print(json.dumps(_jsonable(payload), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
