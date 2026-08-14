"""Exact finite checks for the collective joint-lift theorem package.

All probability, marginal, symmetry, derivative, and Fisher calculations use
``fractions.Fraction``.  Floating-point arithmetic is used only to evaluate
the displayed logarithmic VFE expressions.  These checks corroborate the
accompanying derivations; finite enumeration is not their mathematical proof.
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction


DIMENSION = 6
PAIRS = ((0, 1), (2, 3), (4, 5))
STATES = tuple(itertools.product((0, 1), repeat=DIMENSION))


def _product(values):
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def _text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def parity(state) -> int:
    return -1 if sum(state) % 2 else 1


def product_probability(theta, state) -> Fraction:
    return _product(
        parameter if bit else 1 - parameter
        for parameter, bit in zip(theta, state, strict=True)
    )


def q_probability(theta, kappa: Fraction, state) -> Fraction:
    determinant_factor = _product(parameter * (1 - parameter) for parameter in theta)
    return product_probability(theta, state) + kappa * parity(state) * determinant_factor


def product_marginal(theta, kept, values) -> Fraction:
    return _product(
        theta[index] if bit else 1 - theta[index]
        for index, bit in zip(kept, values, strict=True)
    )


def marginal(theta, kappa: Fraction, kept, values) -> Fraction:
    fixed = dict(zip(kept, values, strict=True))
    omitted = tuple(index for index in range(DIMENSION) if index not in fixed)
    total = Fraction(0)
    for completion in itertools.product((0, 1), repeat=len(omitted)):
        state = [0] * DIMENSION
        for index, bit in fixed.items():
            state[index] = bit
        for index, bit in zip(omitted, completion, strict=True):
            state[index] = bit
        total += q_probability(theta, kappa, tuple(state))
    return total


def flip_state(state, coordinates):
    selected = frozenset(coordinates)
    return tuple(1 - bit if index in selected else bit for index, bit in enumerate(state))


def flip_theta(theta, coordinates):
    selected = frozenset(coordinates)
    return tuple(
        1 - parameter if index in selected else parameter
        for index, parameter in enumerate(theta)
    )


def _typed_agent_permutation_orders():
    """Permute identically typed agent pairs while preserving channel position."""
    for pair_order in itertools.permutations(range(3)):
        order = []
        for old_pair in pair_order:
            order.extend(PAIRS[old_pair])
        yield tuple(order)


def _pair_partition_preserving_coordinate_symmetry_orders():
    """Tested 48-element pair-partition-preserving subgroup, not full S6."""
    for pair_order in itertools.permutations(range(3)):
        for reversals in itertools.product((0, 1), repeat=3):
            order = []
            for new_pair, old_pair in enumerate(pair_order):
                old_coordinates = list(PAIRS[old_pair])
                if reversals[new_pair]:
                    old_coordinates.reverse()
                order.extend(old_coordinates)
            yield tuple(order)


def _permute(values, order):
    return tuple(values[index] for index in order)


def q_derivative(theta, kappa: Fraction, state, coordinate: int) -> Fraction:
    product_term = product_probability(theta, state)
    parameter = theta[coordinate]
    product_score = (
        Fraction(1, parameter) if state[coordinate] else -Fraction(1, 1 - parameter)
    )
    determinant_factor = _product(value * (1 - value) for value in theta)
    determinant_derivative = determinant_factor * Fraction(1 - 2 * parameter, parameter * (1 - parameter))
    return product_term * product_score + kappa * parity(state) * determinant_derivative


def fisher_matrix(theta, kappa: Fraction):
    result = [[Fraction(0) for _ in range(DIMENSION)] for _ in range(DIMENSION)]
    for state in STATES:
        probability = q_probability(theta, kappa, state)
        derivatives = [q_derivative(theta, kappa, state, index) for index in range(DIMENSION)]
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                result[row][column] += derivatives[row] * derivatives[column] / probability
    return result


def center_fisher(kappa: Fraction):
    theta = (Fraction(1, 2),) * DIMENSION
    fisher = fisher_matrix(theta, kappa)
    product_fisher = [
        [Fraction(4) if row == column else Fraction(0) for column in range(DIMENSION)]
        for row in range(DIMENSION)
    ]
    residual = [
        [fisher[row][column] - product_fisher[row][column] for column in range(DIMENSION)]
        for row in range(DIMENSION)
    ]
    return fisher, residual


def _determinant(matrix) -> Fraction:
    work = [list(row) for row in matrix]
    determinant = Fraction(1)
    for pivot_column in range(len(work)):
        pivot_row = next(
            row for row in range(pivot_column, len(work)) if work[row][pivot_column]
        )
        if pivot_row != pivot_column:
            work[pivot_column], work[pivot_row] = work[pivot_row], work[pivot_column]
            determinant = -determinant
        pivot = work[pivot_column][pivot_column]
        determinant *= pivot
        for column in range(pivot_column, len(work)):
            work[pivot_column][column] /= pivot
        for row in range(pivot_column + 1, len(work)):
            factor = work[row][pivot_column]
            for column in range(pivot_column, len(work)):
                work[row][column] -= factor * work[pivot_column][column]
    return determinant


def _two_bit_counterexample():
    probabilities = (
        Fraction(9, 32),
        Fraction(7, 32),
        Fraction(7, 32),
        Fraction(9, 32),
    )
    derivative_left = (
        Fraction(-1, 2),
        Fraction(-1, 2),
        Fraction(1, 2),
        Fraction(1, 2),
    )
    derivative_right = (
        Fraction(-1, 2),
        Fraction(1, 2),
        Fraction(-1, 2),
        Fraction(1, 2),
    )
    fisher = [
        [
            sum(
                left * right / probability
                for probability, left, right in zip(
                    probabilities, derivative_row, derivative_column, strict=True
                )
            )
            for derivative_column in (derivative_left, derivative_right)
        ]
        for derivative_row in (derivative_left, derivative_right)
    ]
    difference = [
        [fisher[row][column] - (Fraction(4) if row == column else Fraction(0)) for column in range(2)]
        for row in range(2)
    ]
    eigenvalues = (
        difference[0][0] + difference[0][1],
        difference[0][0] - difference[0][1],
    )
    return fisher, eigenvalues


def hyperedge_record(kappa: Fraction):
    theta = (Fraction(1, 2),) * DIMENSION
    uniform = Fraction(1, 64)
    c = kappa / 64
    evidence = sum(
        uniform * Fraction(1 + c * parity(state), 2) for state in STATES
    )
    posterior_matches = all(
        uniform * Fraction(1 + c * parity(state), 2) / evidence
        == q_probability(theta, kappa, state)
        for state in STATES
    )
    product_excess = -0.5 * math.log(1.0 - float(c * c))
    return {
        "c": c,
        "evidence": evidence,
        "posterior_matches_center_lift": posterior_matches,
        "correlated_lift_vfe": math.log(2.0),
        "correlated_lift_vfe_exact": "log(2)",
        "product_lift_excess": product_excess,
        "product_lift_excess_exact": "-log(1-c^2)/2",
        "product_lift_vfe": math.log(2.0) + product_excess,
    }


def pairwise_record_cancellation(eta: Fraction):
    """Exact same-marginal joint-kernel control with the product ab term erased."""
    assert 0 <= eta < Fraction(1, 2)
    checks = []
    for sign_a, sign_b in itertools.product((-1, 1), repeat=2):
        a = sign_a * eta
        b = sign_b * eta
        cancelling = {
            "11": Fraction(1 + a + b, 4),
            "10": Fraction(1 + a - b, 4),
            "01": Fraction(1 - a + b, 4),
            "00": Fraction(1 - a - b, 4),
        }
        product_joint = {
            "11": Fraction((1 + a) * (1 + b), 4),
            "10": Fraction((1 + a) * (1 - b), 4),
            "01": Fraction((1 - a) * (1 + b), 4),
            "00": Fraction((1 - a) * (1 - b), 4),
        }
        assert all(value > 0 for value in cancelling.values())
        assert sum(cancelling.values()) == 1
        assert cancelling["11"] + cancelling["10"] == Fraction(1 + a, 2)
        assert cancelling["11"] + cancelling["01"] == Fraction(1 + b, 2)
        assert product_joint["11"] + product_joint["10"] == Fraction(1 + a, 2)
        assert product_joint["11"] + product_joint["01"] == Fraction(1 + b, 2)
        assert product_joint["11"] - cancelling["11"] == a * b / 4
        checks.append((a, b, cancelling, product_joint))
    return {
        "eta": eta,
        "all_strictly_positive": True,
        "all_normalized": True,
        "same_marginal_kernels": True,
        "cancelling_ab_coefficient": Fraction(0),
        "product_ab_coefficient": Fraction(1, 4),
        "minimum_atom": min(
            value for _, _, cancelling, _ in checks for value in cancelling.values()
        ),
    }


def _kl(left, right) -> float:
    return sum(
        float(source) * math.log(float(source / target))
        for source, target in zip(left, right, strict=True)
    )


def block_vfe_witness():
    """Corroborate the fixed-outside identity along a lift direction.

    This varies kappa with theta fixed.  It is not a single-agent theta update,
    and the reported differential is along Q_alternate-Q_base rather than per
    unit kappa.
    """
    theta = (
        Fraction(1, 3),
        Fraction(2, 5),
        Fraction(3, 7),
        Fraction(4, 9),
        Fraction(5, 11),
        Fraction(6, 13),
    )
    base_kappa = Fraction(1, 4)
    alternate_kappa = Fraction(1, 2)
    target_kappa = Fraction(-1, 3)
    base = tuple(q_probability(theta, base_kappa, state) for state in STATES)
    alternate = tuple(q_probability(theta, alternate_kappa, state) for state in STATES)
    target = tuple(q_probability(theta, target_kappa, state) for state in STATES)
    outside_states = tuple(itertools.product((0, 1), repeat=4))
    block_states = tuple(itertools.product((0, 1), repeat=2))

    def joint_value(law, block_state, outside_state):
        state = tuple(block_state) + tuple(outside_state)
        return law[STATES.index(state)]

    outside_base = []
    outside_alternate = []
    outside_target = []
    for outside_state in outside_states:
        outside_base.append(sum(joint_value(base, block, outside_state) for block in block_states))
        outside_alternate.append(
            sum(joint_value(alternate, block, outside_state) for block in block_states)
        )
        outside_target.append(
            sum(joint_value(target, block, outside_state) for block in block_states)
        )
    outside_equal = outside_base == outside_alternate == outside_target

    local_difference = 0.0
    local_differential = 0.0
    for outside_index, outside_state in enumerate(outside_states):
        weight = outside_base[outside_index]
        base_conditional = tuple(
            joint_value(base, block, outside_state) / weight for block in block_states
        )
        alternate_conditional = tuple(
            joint_value(alternate, block, outside_state) / weight for block in block_states
        )
        target_conditional = tuple(
            joint_value(target, block, outside_state) / weight for block in block_states
        )
        local_difference += float(weight) * (
            _kl(alternate_conditional, target_conditional)
            - _kl(base_conditional, target_conditional)
        )
        local_differential += float(weight) * sum(
            float(alternate_value - base_value)
            * math.log(float(base_value / target_value))
            for alternate_value, base_value, target_value in zip(
                alternate_conditional,
                base_conditional,
                target_conditional,
                strict=True,
            )
        )

    global_difference = _kl(alternate, target) - _kl(base, target)
    global_differential = sum(
        float(alternate_value - base_value) * math.log(float(base_value / target_value))
        for alternate_value, base_value, target_value in zip(
            alternate, base, target, strict=True
        )
    )
    return {
        "direction_kind": "kappa_lift",
        "outside_marginal_equal": outside_equal,
        "global_difference": global_difference,
        "outside_weighted_local_difference": local_difference,
        "global_differential": global_differential,
        "outside_weighted_local_differential": local_differential,
    }


def agent_theta_block_vfe_witness(agent_pair_index: int):
    """Vary one selected agent pair's theta coordinates at fixed outside theta."""
    if agent_pair_index not in range(3):
        raise ValueError("agent_pair_index must be 0, 1, or 2")
    agent_coordinates = PAIRS[agent_pair_index]
    outside_coordinates = tuple(
        index for index in range(DIMENSION) if index not in agent_coordinates
    )
    base_theta = (
        Fraction(1, 3),
        Fraction(2, 5),
        Fraction(3, 7),
        Fraction(4, 9),
        Fraction(5, 11),
        Fraction(6, 13),
    )
    alternate_pairs = (
        (Fraction(2, 7), Fraction(3, 8)),
        (Fraction(5, 12), Fraction(7, 15)),
        (Fraction(4, 13), Fraction(7, 12)),
    )
    target_pairs = (
        (Fraction(4, 9), Fraction(5, 12)),
        (Fraction(3, 10), Fraction(5, 8)),
        (Fraction(2, 7), Fraction(8, 15)),
    )
    theta_directions = (
        (Fraction(1, 7), Fraction(-1, 11)),
        (Fraction(2, 13), Fraction(-1, 9)),
        (Fraction(1, 8), Fraction(-2, 15)),
    )
    alternate_theta_values = list(base_theta)
    target_theta_values = list(base_theta)
    for coordinate, value in zip(
        agent_coordinates, alternate_pairs[agent_pair_index], strict=True
    ):
        alternate_theta_values[coordinate] = value
    for coordinate, value in zip(
        agent_coordinates, target_pairs[agent_pair_index], strict=True
    ):
        target_theta_values[coordinate] = value
    alternate_theta = tuple(alternate_theta_values)
    target_theta = tuple(target_theta_values)
    theta_direction = theta_directions[agent_pair_index]
    kappa = Fraction(1, 2)
    target_kappa = Fraction(-1, 3)
    base = tuple(q_probability(base_theta, kappa, state) for state in STATES)
    alternate = tuple(q_probability(alternate_theta, kappa, state) for state in STATES)
    target = tuple(q_probability(target_theta, target_kappa, state) for state in STATES)
    tangent = tuple(
        sum(
            direction * q_derivative(base_theta, kappa, state, coordinate)
            for coordinate, direction in zip(
                agent_coordinates, theta_direction, strict=True
            )
        )
        for state in STATES
    )
    assert sum(tangent) == 0

    outside_states = tuple(itertools.product((0, 1), repeat=4))
    block_states = tuple(itertools.product((0, 1), repeat=2))

    def joint_value(law, block_state, outside_state):
        state = [0] * DIMENSION
        for coordinate, bit in zip(agent_coordinates, block_state, strict=True):
            state[coordinate] = bit
        for coordinate, bit in zip(outside_coordinates, outside_state, strict=True):
            state[coordinate] = bit
        return law[STATES.index(tuple(state))]

    outside_base = []
    outside_alternate = []
    outside_target = []
    outside_tangent = []
    for outside_state in outside_states:
        outside_base.append(sum(joint_value(base, block, outside_state) for block in block_states))
        outside_alternate.append(
            sum(joint_value(alternate, block, outside_state) for block in block_states)
        )
        outside_target.append(
            sum(joint_value(target, block, outside_state) for block in block_states)
        )
        outside_tangent.append(
            sum(joint_value(tangent, block, outside_state) for block in block_states)
        )

    outside_equal = outside_base == outside_alternate == outside_target
    outside_tangent_zero = all(value == 0 for value in outside_tangent)
    assert outside_equal
    assert outside_tangent_zero

    local_difference = 0.0
    local_differential = 0.0
    for outside_index, outside_state in enumerate(outside_states):
        weight = outside_base[outside_index]
        base_conditional = tuple(
            joint_value(base, block, outside_state) / weight for block in block_states
        )
        alternate_conditional = tuple(
            joint_value(alternate, block, outside_state) / weight for block in block_states
        )
        target_conditional = tuple(
            joint_value(target, block, outside_state) / weight for block in block_states
        )
        tangent_conditional = tuple(
            joint_value(tangent, block, outside_state) / weight for block in block_states
        )
        assert sum(tangent_conditional) == 0
        local_difference += float(weight) * (
            _kl(alternate_conditional, target_conditional)
            - _kl(base_conditional, target_conditional)
        )
        local_differential += float(weight) * sum(
            float(tangent_value) * math.log(float(base_value / target_value))
            for tangent_value, base_value, target_value in zip(
                tangent_conditional,
                base_conditional,
                target_conditional,
                strict=True,
            )
        )

    global_difference = _kl(alternate, target) - _kl(base, target)
    global_differential = sum(
        float(tangent_value) * math.log(float(base_value / target_value))
        for tangent_value, base_value, target_value in zip(
            tangent, base, target, strict=True
        )
    )
    return {
        "direction_kind": "agent_theta_block",
        "agent_pair_index": agent_pair_index,
        "agent_coordinates": agent_coordinates,
        "outside_theta_equal": (
            tuple(base_theta[index] for index in outside_coordinates)
            == tuple(alternate_theta[index] for index in outside_coordinates)
            == tuple(target_theta[index] for index in outside_coordinates)
        ),
        "outside_marginal_equal": outside_equal,
        "outside_tangent_zero": outside_tangent_zero,
        "global_difference": global_difference,
        "outside_weighted_local_difference": local_difference,
        "global_differential": global_differential,
        "outside_weighted_local_differential": local_differential,
    }


def main() -> int:
    theta = (
        Fraction(1, 3),
        Fraction(2, 5),
        Fraction(3, 7),
        Fraction(4, 9),
        Fraction(5, 11),
        Fraction(6, 13),
    )
    kappa = Fraction(1, 2)
    probabilities = tuple(q_probability(theta, kappa, state) for state in STATES)
    assert all(probability > 0 for probability in probabilities)
    assert sum(probabilities) == 1

    checked_subsets = 0
    for size in range(DIMENSION):
        for kept in itertools.combinations(range(DIMENSION), size):
            for values in itertools.product((0, 1), repeat=size):
                assert marginal(theta, kappa, kept, values) == product_marginal(
                    theta, kept, values
                )
            checked_subsets += 1
    assert checked_subsets == 63

    paired_group_size = 0
    for selected_pairs in itertools.product((0, 1), repeat=3):
        coordinates = tuple(
            coordinate
            for pair_index, selected in enumerate(selected_pairs)
            if selected
            for coordinate in PAIRS[pair_index]
        )
        transformed_theta = flip_theta(theta, coordinates)
        assert all(
            q_probability(transformed_theta, kappa, flip_state(state, coordinates))
            == q_probability(theta, kappa, state)
            for state in STATES
        )
        paired_group_size += 1

    typed_agent_permutation_count = 0
    for order in _typed_agent_permutation_orders():
        assert all(
            q_probability(_permute(theta, order), kappa, _permute(state, order))
            == q_probability(theta, kappa, state)
            for state in STATES
        )
        typed_agent_permutation_count += 1
    assert typed_agent_permutation_count == 6

    pair_partition_preserving_coordinate_symmetry_count = 0
    for order in _pair_partition_preserving_coordinate_symmetry_orders():
        assert all(
            q_probability(_permute(theta, order), kappa, _permute(state, order))
            == q_probability(theta, kappa, state)
            for state in STATES
        )
        pair_partition_preserving_coordinate_symmetry_count += 1
    assert pair_partition_preserving_coordinate_symmetry_count == 48

    odd_coordinates = (0,)
    odd_theta = flip_theta(theta, odd_coordinates)
    scalar_equalities = [
        q_probability(odd_theta, kappa, flip_state(state, odd_coordinates))
        == q_probability(theta, kappa, state)
        for state in STATES
    ]
    pseudoscalar_equalities = [
        q_probability(odd_theta, -kappa, flip_state(state, odd_coordinates))
        == q_probability(theta, kappa, state)
        for state in STATES
    ]
    assert not any(scalar_equalities)
    assert all(pseudoscalar_equalities)

    fisher, residual = center_fisher(kappa)
    c = kappa / 64
    center_diagonal = Fraction(4, 1) / (1 - c * c)
    residual_diagonal = center_diagonal - 4
    assert fisher == [
        [center_diagonal if row == column else Fraction(0) for column in range(DIMENSION)]
        for row in range(DIMENSION)
    ]
    assert residual == [
        [residual_diagonal if row == column else Fraction(0) for column in range(DIMENSION)]
        for row in range(DIMENSION)
    ]

    sample_fisher = fisher_matrix(theta, kappa)
    product_diagonal = [Fraction(1, value * (1 - value)) for value in theta]
    sample_residual = [
        [
            sample_fisher[row][column]
            - (product_diagonal[row] if row == column else Fraction(0))
            for column in range(DIMENSION)
        ]
        for row in range(DIMENSION)
    ]
    leading_principal_minors = [
        _determinant([row[:size] for row in sample_residual[:size]])
        for size in range(1, DIMENSION + 1)
    ]
    assert all(value > 0 for value in leading_principal_minors)

    two_bit_fisher, two_bit_difference_eigenvalues = _two_bit_counterexample()
    assert two_bit_fisher == [
        [Fraction(256, 63), Fraction(-32, 63)],
        [Fraction(-32, 63), Fraction(256, 63)],
    ]
    assert two_bit_difference_eigenvalues == (Fraction(-4, 9), Fraction(4, 7))

    record = hyperedge_record(kappa)
    assert record["posterior_matches_center_lift"]
    pairwise_control = pairwise_record_cancellation(Fraction(1, 3))
    assert pairwise_control["all_strictly_positive"]
    assert pairwise_control["same_marginal_kernels"]
    assert pairwise_control["cancelling_ab_coefficient"] == 0
    block = block_vfe_witness()
    assert block["direction_kind"] == "kappa_lift"
    assert block["outside_marginal_equal"]
    assert math.isclose(
        block["global_difference"],
        block["outside_weighted_local_difference"],
        rel_tol=0.0,
        abs_tol=1e-15,
    )
    assert math.isclose(
        block["global_differential"],
        block["outside_weighted_local_differential"],
        rel_tol=0.0,
        abs_tol=1e-15,
    )
    agent_blocks = [agent_theta_block_vfe_witness(index) for index in range(3)]
    for agent_block in agent_blocks:
        assert agent_block["outside_theta_equal"]
        assert agent_block["outside_marginal_equal"]
        assert agent_block["outside_tangent_zero"]
        assert math.isclose(
            agent_block["global_difference"],
            agent_block["outside_weighted_local_difference"],
            rel_tol=0.0,
            abs_tol=1e-15,
        )
        assert math.isclose(
            agent_block["global_differential"],
            agent_block["outside_weighted_local_differential"],
            rel_tol=0.0,
            abs_tol=1e-15,
        )

    payload = {
        "agent_theta_block_vfe": agent_blocks,
        "block_vfe": block,
        "center": {
            "c": _text(c),
            "fisher_diagonal": _text(center_diagonal),
            "residual_diagonal": _text(residual_diagonal),
        },
        "odd_flip_pseudoscalar_equivariant": all(pseudoscalar_equalities),
        "odd_flip_scalar_equivariant": all(scalar_equalities),
        "paired_complement_group_size": paired_group_size,
        "pairwise_record_cancellation": {
            "cancelling_ab_coefficient": _text(pairwise_control["cancelling_ab_coefficient"]),
            "eta": _text(pairwise_control["eta"]),
            "minimum_atom": _text(pairwise_control["minimum_atom"]),
            "product_ab_coefficient": _text(pairwise_control["product_ab_coefficient"]),
            "same_marginal_kernels": pairwise_control["same_marginal_kernels"],
            "strictly_positive": pairwise_control["all_strictly_positive"],
        },
        "proper_marginal_subset_count": checked_subsets,
        "record": {
            "c": _text(record["c"]),
            "correlated_lift_vfe_exact": record["correlated_lift_vfe_exact"],
            "evidence": _text(record["evidence"]),
            "posterior_matches_center_lift": record["posterior_matches_center_lift"],
            "product_lift_excess_exact": record["product_lift_excess_exact"],
        },
        "residual_positive_definite_sample": {
            "leading_principal_minors": [_text(value) for value in leading_principal_minors]
        },
        "two_bit_counterexample": {
            "difference_eigenvalues": [
                _text(value) for value in two_bit_difference_eigenvalues
            ],
            "fisher": [[_text(value) for value in row] for row in two_bit_fisher],
        },
        "pair_partition_preserving_coordinate_symmetry_count": pair_partition_preserving_coordinate_symmetry_count,
        "typed_agent_permutation_count": typed_agent_permutation_count,
    }
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
