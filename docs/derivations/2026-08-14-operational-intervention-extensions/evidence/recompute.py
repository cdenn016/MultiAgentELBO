#!/usr/bin/env python3
"""Exact corroboration for the operational-intervention extension proofs.

Only the Python standard library is used. Rational calculations corroborate
finite identities; Decimal heat calculations are explicitly numerical and do
not prove the analytic theorems.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import itertools
import json
import math
import sys
from typing import Iterable, Sequence


CONTRACT_ID = (
    "contract-sha256-"
    "af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1"
)
TARGET_DIGEST = "af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1"

Context = tuple[int | None, int | None, int | None]
Law = tuple[Fraction, Fraction, Fraction, Fraction]
Matrix = list[list[Fraction]]


class CorroborationError(RuntimeError):
    """Raised when an exact or corroborative invariant fails."""


def require(condition: bool, message: str) -> None:
    """Fail closed even when Python is run with optimization enabled."""

    if not condition:
        raise CorroborationError(message)


# Released hard-class order: noop, O0, O1, E0, E1, R0, R0O0, R0O1,
# R0E0, R0E1, R1, R1O0, R1O1, R1E0, R1E1.
CLASS_NAMES = (
    "noop", "O0", "O1", "E0", "E1", "R0", "R0O0", "R0O1",
    "R0E0", "R0E1", "R1", "R1O0", "R1O1", "R1E0", "R1E1",
)
CLASS_REPRESENTATIVES: tuple[Context, ...] = (
    (None, None, None), (None, None, 0), (None, None, 1),
    (None, 0, None), (None, 1, None), (0, None, None),
    (0, None, 0), (0, None, 1), (0, 0, None), (0, 1, None),
    (1, None, None), (1, None, 0), (1, None, 1),
    (1, 0, None), (1, 1, None),
)

# A complete signature coordinate is flattened as
# 4 * (15 * left_class + right_class) + retained_atom.
SELECTED_COLUMNS = (
    0, 1, 2, 3, 12, 14, 16, 18, 20, 42, 300, 301, 302, 312, 316,
)
ATOM_NAMES = ("00", "01", "10", "11")


def right_override(left: Context, right: Context) -> Context:
    values = tuple(
        right[index] if right[index] is not None else left[index]
        for index in range(3)
    )
    return values  # type: ignore[return-value]


def hard_response(context: Context, *, b: Fraction, delta: Fraction) -> Law:
    assigned_r, assigned_e, assigned_o = context
    atoms: list[Fraction] = []
    for retained, output in itertools.product((0, 1), repeat=2):
        retained_factor = (
            Fraction(1, 2)
            if assigned_r is None
            else Fraction(int(retained == assigned_r))
        )
        if assigned_o is not None:
            output_factor = Fraction(int(output == assigned_o))
        elif assigned_e is not None:
            output_factor = Fraction(1) - b if output == assigned_e else b
        else:
            output_factor = Fraction(1) - delta if output == retained else delta
        atoms.append(retained_factor * output_factor)
    law = tuple(atoms)
    require(sum(law, Fraction(0)) == 1, "hard response is not normalized")
    return law  # type: ignore[return-value]


def complete_signature_matrix(*, b: Fraction, delta: Fraction) -> Matrix:
    matrix: Matrix = []
    for central in CLASS_REPRESENTATIVES:
        row: list[Fraction] = []
        for left in CLASS_REPRESENTATIVES:
            for right in CLASS_REPRESENTATIVES:
                composed = right_override(right_override(left, central), right)
                row.extend(hard_response(composed, b=b, delta=delta))
        require(len(row) == 900, "contextual signature width changed")
        matrix.append(row)
    return matrix


def selected_minor(matrix: Matrix) -> Matrix:
    return [[row[column] for column in SELECTED_COLUMNS] for row in matrix]


def require_square(matrix: Matrix, algorithm: str) -> int:
    size = len(matrix)
    require(
        size > 0 and all(len(row) == size for row in matrix),
        f"{algorithm} requires a nonempty square matrix",
    )
    return size


def determinant_fraction(matrix: Matrix) -> Fraction:
    """Exact Gaussian determinant over Fraction."""

    work = [row[:] for row in matrix]
    size = require_square(work, "Fraction determinant")
    sign = 1
    determinant = Fraction(1)
    for column in range(size):
        pivot_row = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        if pivot_row is None:
            return Fraction(0)
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign *= -1
        pivot = work[column][column]
        determinant *= pivot
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            multiplier = work[row][column] / pivot
            for inner_column in range(column, size):
                work[row][inner_column] -= multiplier * work[column][inner_column]
    return sign * determinant


def lcm(values: Iterable[int]) -> int:
    result = 1
    for value in values:
        result = math.lcm(result, value)
    return result


def determinant_integer_bareiss(matrix: Matrix) -> Fraction:
    """Independent exact determinant via row scaling and integer Bareiss."""

    row_scales = [lcm(entry.denominator for entry in row) for row in matrix]
    work = [
        [int(entry * scale) for entry in row]
        for scale, row in zip(row_scales, matrix)
    ]
    size = require_square(work, "Bareiss determinant")  # type: ignore[arg-type]
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot_row = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        if pivot_row is None:
            return Fraction(0)
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign *= -1
        pivot = work[column][column]
        for row in range(column + 1, size):
            for inner_column in range(column + 1, size):
                numerator = (
                    work[row][inner_column] * pivot
                    - work[row][column] * work[column][inner_column]
                )
                require(
                    numerator % previous == 0,
                    "Bareiss division ceased to be exact",
                )
                work[row][inner_column] = numerator // previous
            work[row][column] = 0
        previous = pivot
    return Fraction(sign * work[-1][-1], math.prod(row_scales))


def rank_fraction(matrix: Matrix) -> int:
    """Exact row rank, independent of either determinant calculation."""

    work = [row[:] for row in matrix]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    require(
        all(len(row) == column_count for row in work),
        "rank matrix has inconsistent row lengths",
    )
    rank = 0
    for column in range(column_count):
        pivot_row = next(
            (row for row in range(rank, row_count) if work[row][column]), None
        )
        if pivot_row is None:
            continue
        work[rank], work[pivot_row] = work[pivot_row], work[rank]
        pivot = work[rank][column]
        for inner_column in range(column, column_count):
            work[rank][inner_column] /= pivot
        for row in range(row_count):
            if row == rank or not work[row][column]:
                continue
            multiplier = work[row][column]
            for inner_column in range(column, column_count):
                work[row][inner_column] -= multiplier * work[rank][inner_column]
        rank += 1
        if rank == row_count:
            break
    return rank


def fraction_matrix_hash(matrix: Matrix) -> str:
    payload = json.dumps(
        [[str(entry) for entry in row] for row in matrix],
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def soft_response(b: Fraction, t: tuple[Fraction, Fraction]) -> Law:
    atoms: list[Fraction] = []
    for retained in (0, 1):
        output_zero = b + (Fraction(1) - 2 * b) * t[retained]
        atoms.extend((output_zero / 2, (Fraction(1) - output_zero) / 2))
    law = tuple(atoms)
    require(all(atom >= 0 for atom in law), "soft response has a negative atom")
    require(sum(law, Fraction(0)) == 1, "soft response is not normalized")
    return law  # type: ignore[return-value]


def total_variation(left: Sequence[Fraction], right: Sequence[Fraction]) -> Fraction:
    require(len(left) == len(right), "total variation laws have unequal sizes")
    return sum((abs(a - b) for a, b in zip(left, right)), Fraction(0)) / 2


def affine_mix(
    weight: Fraction, left: Sequence[Fraction], right: Sequence[Fraction]
) -> tuple[Fraction, ...]:
    require(len(left) == len(right), "affine mixture laws have unequal sizes")
    return tuple(
        weight * a + (Fraction(1) - weight) * b
        for a, b in zip(left, right)
    )


def decoded_selected_columns() -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for flat_index in SELECTED_COLUMNS:
        context_index, atom_index = divmod(flat_index, 4)
        left_index, right_index = divmod(context_index, 15)
        result.append(
            {
                "atom": ATOM_NAMES[atom_index],
                "flat_index": flat_index,
                "left_class": left_index,
                "left_name": CLASS_NAMES[left_index],
                "right_class": right_index,
                "right_name": CLASS_NAMES[right_index],
            }
        )
    return result


def determinant_record(*, name: str, b: Fraction, delta: Fraction) -> dict[str, object]:
    complete = complete_signature_matrix(b=b, delta=delta)
    minor = selected_minor(complete)
    gaussian = determinant_fraction(minor)
    bareiss = determinant_integer_bareiss(minor)
    formula = (2 * b - 1) ** 6 * (2 * delta - 1) ** 3 / 32
    minor_rank = rank_fraction(minor)
    complete_rank = rank_fraction(complete)
    require(
        gaussian == bareiss == formula,
        f"{name} determinant implementations or closed formula disagree",
    )
    require(
        minor_rank == complete_rank == 15,
        f"{name} contextual signature does not have rank fifteen",
    )
    return {
        "b": str(b),
        "complete_contextual_rank": complete_rank,
        "complete_contextual_shape": [15, 900],
        "delta": str(delta),
        "determinant_formula_value": str(formula),
        "determinant_fraction_elimination": str(gaussian),
        "determinant_integer_bareiss": str(bareiss),
        "full_signature_sha256": fraction_matrix_hash(complete),
        "minor_rank": minor_rank,
        "minor_sha256": fraction_matrix_hash(minor),
        "model": name,
    }


def decimal_heat_record() -> dict[str, object]:
    with localcontext() as context:
        context.prec = 60
        s = Decimal(1) / Decimal(4)
        t = Decimal(3) / Decimal(4)
        rho = Decimal(1) / Decimal(4)
        passive_first_mode = (-(s + t)).exp()
        forward_garbling = (-(t - s)).exp()
        reverse_required = (t - s).exp()
        strictness_required = (t - s - rho).exp()
        preparation_first_mode = (-rho).exp()
        witness_first_mode = (-(rho + s)).exp()
        require(reverse_required > 1, "reverse coefficient is not greater than one")
        require(
            strictness_required > 1,
            "strict-inclusion coefficient is not greater than one",
        )
        require(rho > 0 and rho < t - s, "rho is outside the witness interval")
        return {
            "corroborative_only": True,
            "forward_garbling_first_mode_exp_minus_t_minus_s": str(forward_garbling),
            "passive_first_mode_exp_minus_s_plus_t": str(passive_first_mode),
            "preparation_first_mode_exp_minus_rho": str(preparation_first_mode),
            "reverse_required_coefficient_exp_t_minus_s": str(reverse_required),
            "reverse_required_coefficient_gt_one": reverse_required > 1,
            "rho": str(rho),
            "s": str(s),
            "strictness_required_coefficient_exp_t_minus_s_minus_rho": str(
                strictness_required
            ),
            "strictness_required_coefficient_gt_one": strictness_required > 1,
            "t": str(t),
            "witness_response_first_mode_exp_minus_rho_plus_s": str(
                witness_first_mode
            ),
        }


def main() -> int:
    a_left, b_left = Fraction(1, 4), Fraction(1, 3)
    a_right, b_right = Fraction(1, 3), Fraction(1, 4)
    delta_left = a_left + b_left - 2 * a_left * b_left
    delta_right = a_right + b_right - 2 * a_right * b_right
    require(
        delta_left == delta_right == Fraction(5, 12),
        "the BSC chains do not have the expected common crossover",
    )
    delta = delta_left
    passive_expected = (
        Fraction(7, 24), Fraction(5, 24),
        Fraction(5, 24), Fraction(7, 24),
    )
    passive_left = hard_response(CLASS_REPRESENTATIVES[0], b=b_left, delta=delta)
    passive_right = hard_response(CLASS_REPRESENTATIVES[0], b=b_right, delta=delta)
    require(
        passive_left == passive_right == passive_expected,
        "the exact passive retained laws disagree",
    )

    epsilon = Fraction(1, 8)
    low = (epsilon, epsilon)
    high = (Fraction(1) - epsilon, Fraction(1) - epsilon)
    interior_low = (Fraction(1, 4), Fraction(1, 4))
    interior_high = (Fraction(3, 4), Fraction(3, 4))
    left_diameter = total_variation(
        soft_response(b_left, low), soft_response(b_left, high)
    )
    right_diameter = total_variation(
        soft_response(b_right, low), soft_response(b_right, high)
    )
    require(
        left_diameter == (1 - 2 * epsilon) * abs(1 - 2 * b_left)
        == Fraction(1, 4),
        "the left soft-face diameter is incorrect",
    )
    require(
        right_diameter == (1 - 2 * epsilon) * abs(1 - 2 * b_right)
        == Fraction(3, 8),
        "the right soft-face diameter is incorrect",
    )
    left_interior = total_variation(
        soft_response(b_left, interior_low),
        soft_response(b_left, interior_high),
    )
    right_interior = total_variation(
        soft_response(b_right, interior_low),
        soft_response(b_right, interior_high),
    )
    require(left_interior == Fraction(1, 6), "left interior separation is incorrect")
    require(
        right_interior == Fraction(1, 4),
        "right interior separation is incorrect",
    )

    mediator_zero_left = soft_response(b_left, (Fraction(1), Fraction(1)))
    mediator_zero_right = soft_response(b_right, (Fraction(1), Fraction(1)))
    mediator_one_right = soft_response(b_right, (Fraction(0), Fraction(0)))
    mixture_weight = Fraction(5, 6)
    mixture = affine_mix(mixture_weight, mediator_zero_right, mediator_one_right)
    require(mixture == mediator_zero_left, "the convex-mixture identity failed")

    boundary_vertices = (
        hard_response((0, None, 0), b=b_left, delta=delta),
        hard_response((0, None, 1), b=b_left, delta=delta),
        hard_response((1, None, 0), b=b_left, delta=delta),
        hard_response((1, None, 1), b=b_left, delta=delta),
    )
    expected_vertices = tuple(
        tuple(Fraction(int(index == atom)) for atom in range(4))
        for index in range(4)
    )
    require(
        boundary_vertices == expected_vertices,
        "boundary point interventions are not the four retained vertices",
    )

    payload = {
        "bsc_passive": {
            "atom_order": list(ATOM_NAMES),
            "expected_law": [str(value) for value in passive_expected],
            "left_a": str(a_left),
            "left_b": str(b_left),
            "left_crossover": str(delta_left),
            "left_law": [str(value) for value in passive_left],
            "passive_equal": passive_left == passive_right,
            "right_a": str(a_right),
            "right_b": str(b_right),
            "right_crossover": str(delta_right),
            "right_law": [str(value) for value in passive_right],
        },
        "circle_fourier_decimal": decimal_heat_record(),
        "contract_id": CONTRACT_ID,
        "exact_contextual_minors": {
            "class_order": list(CLASS_NAMES),
            "determinant_identity": "(2*b-1)^6*(2*delta-1)^3/32",
            "left": determinant_record(name="L1", b=b_left, delta=delta),
            "right": determinant_record(name="L2", b=b_right, delta=delta),
            "selected_columns": decoded_selected_columns(),
        },
        "randomized_convexification": {
            "boundary_point_interventions": [
                [str(value) for value in law] for law in boundary_vertices
            ],
            "boundary_points_are_four_simplex_vertices": True,
            "left_do_E0": [str(value) for value in mediator_zero_left],
            "mixture": [str(value) for value in mixture],
            "mixture_equal": mixture == mediator_zero_left,
            "right_do_E0": [str(value) for value in mediator_zero_right],
            "right_do_E1": [str(value) for value in mediator_one_right],
            "weight_on_right_do_E0": str(mixture_weight),
            "weight_on_right_do_E1": str(1 - mixture_weight),
        },
        "scope": {
            "decimal_values_are_corroborative_only": True,
            "exact_rational_values_are_corroborative_not_proofs": True,
            "gpu_or_model_workload_used": False,
            "python_assertions_used": False,
            "python_standard_library_only": True,
        },
        "soft_face_epsilon_one_eighth": {
            "epsilon": str(epsilon),
            "interior_pair": [str(interior_low[0]), str(interior_high[0])],
            "left_b": str(b_left),
            "left_diameter": str(left_diameter),
            "left_interior_separation": str(left_interior),
            "right_b": str(b_right),
            "right_diameter": str(right_diameter),
            "right_interior_separation": str(right_interior),
        },
        "target_digest": TARGET_DIGEST,
    }
    output = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ) + "\n"
    binary_stdout = getattr(sys.stdout, "buffer", None)
    if binary_stdout is None:
        sys.stdout.write(output)
    else:
        binary_stdout.write(output.encode("ascii"))
        binary_stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
