import importlib.util
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WITNESS = (
    ROOT
    / "docs/derivations/2026-08-14-collective-joint-lift-fisher"
    / "evidence/exact_collective_witness.py"
)


def _load_witness():
    specification = importlib.util.spec_from_file_location(
        "exact_collective_joint_lift_witness", WITNESS
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def test_all_63_proper_marginals_are_product() -> None:
    module = _load_witness()
    theta = (
        Fraction(1, 3),
        Fraction(2, 5),
        Fraction(3, 7),
        Fraction(4, 9),
        Fraction(5, 11),
        Fraction(6, 13),
    )
    kappa = Fraction(1, 2)
    probabilities = tuple(
        module.q_probability(theta, kappa, state)
        for state in itertools.product((0, 1), repeat=6)
    )
    assert all(probability > 0 for probability in probabilities)
    assert sum(probabilities) == 1
    checked = 0
    for size in range(6):
        for kept in itertools.combinations(range(6), size):
            for values in itertools.product((0, 1), repeat=size):
                assert module.marginal(theta, kappa, kept, values) == (
                    module.product_marginal(theta, kept, values)
                )
            checked += 1
    assert checked == 63


def test_paired_complements_are_equivariant_but_odd_flip_is_not() -> None:
    module = _load_witness()
    theta = (
        Fraction(1, 3),
        Fraction(2, 5),
        Fraction(3, 7),
        Fraction(4, 9),
        Fraction(5, 11),
        Fraction(6, 13),
    )
    kappa = Fraction(1, 2)
    states = tuple(itertools.product((0, 1), repeat=6))

    for selected_pairs in itertools.product((0, 1), repeat=3):
        flipped = tuple(
            coordinate
            for pair, selected in enumerate(selected_pairs)
            if selected
            for coordinate in (2 * pair, 2 * pair + 1)
        )
        transformed_theta = module.flip_theta(theta, flipped)
        for state in states:
            transformed_state = module.flip_state(state, flipped)
            assert module.q_probability(
                transformed_theta, kappa, transformed_state
            ) == module.q_probability(theta, kappa, state)

    odd_flip = (0,)
    transformed_theta = module.flip_theta(theta, odd_flip)
    mismatches = 0
    for state in states:
        transformed_state = module.flip_state(state, odd_flip)
        if module.q_probability(
            transformed_theta, kappa, transformed_state
        ) != module.q_probability(theta, kappa, state):
            mismatches += 1
        assert module.q_probability(
            transformed_theta, -kappa, transformed_state
        ) == module.q_probability(theta, kappa, state)
    assert mismatches == 64


def test_exact_center_fisher_and_residual() -> None:
    module = _load_witness()
    fisher, residual = module.center_fisher(Fraction(1, 2))
    expected_fisher = Fraction(65536, 16383)
    assert fisher == [
        [expected_fisher if row == column else Fraction(0) for column in range(6)]
        for row in range(6)
    ]
    assert residual == [
        [Fraction(4, 16383) if row == column else Fraction(0) for column in range(6)]
        for row in range(6)
    ]

    theta = (
        Fraction(1, 3),
        Fraction(2, 5),
        Fraction(3, 7),
        Fraction(4, 9),
        Fraction(5, 11),
        Fraction(6, 13),
    )
    off_center_fisher = module.fisher_matrix(theta, Fraction(1, 2))
    off_center_residual = [
        [
            off_center_fisher[row][column]
            - (
                Fraction(1, theta[row] * (1 - theta[row]))
                if row == column
                else Fraction(0)
            )
            for column in range(6)
        ]
        for row in range(6)
    ]
    leading_principal_minors = [
        module._determinant([row[:size] for row in off_center_residual[:size]])
        for size in range(1, 7)
    ]
    assert all(value > 0 for value in leading_principal_minors)


def test_hyperedge_record_and_block_local_global_identity() -> None:
    module = _load_witness()
    record = module.hyperedge_record(Fraction(1, 2))
    assert record["c"] == Fraction(1, 128)
    assert record["evidence"] == Fraction(1, 2)
    assert record["posterior_matches_center_lift"] is True
    assert record["correlated_lift_vfe_exact"] == "log(2)"
    assert record["product_lift_excess_exact"] == "-log(1-c^2)/2"
    assert math.isclose(
        record["product_lift_vfe"],
        math.log(2.0) - 0.5 * math.log(1.0 - float(record["c"] ** 2)),
        rel_tol=0.0,
        abs_tol=1e-15,
    )

    pairwise_control = module.pairwise_record_cancellation(Fraction(1, 3))
    assert pairwise_control == {
        "eta": Fraction(1, 3),
        "all_strictly_positive": True,
        "all_normalized": True,
        "same_marginal_kernels": True,
        "cancelling_ab_coefficient": Fraction(0),
        "product_ab_coefficient": Fraction(1, 4),
        "minimum_atom": Fraction(1, 12),
    }

    block = module.block_vfe_witness()
    assert block["direction_kind"] == "kappa_lift"
    assert block["outside_marginal_equal"] is True
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

    for agent_pair_index, expected_coordinates in enumerate(((0, 1), (2, 3), (4, 5))):
        agent = module.agent_theta_block_vfe_witness(agent_pair_index)
        assert agent["direction_kind"] == "agent_theta_block"
        assert agent["agent_pair_index"] == agent_pair_index
        assert agent["agent_coordinates"] == expected_coordinates
        assert agent["outside_theta_equal"] is True
        assert agent["outside_marginal_equal"] is True
        assert agent["outside_tangent_zero"] is True
        assert math.isclose(
            agent["global_difference"],
            agent["outside_weighted_local_difference"],
            rel_tol=0.0,
            abs_tol=1e-15,
        )
        assert math.isclose(
            agent["global_differential"],
            agent["outside_weighted_local_differential"],
            rel_tol=0.0,
            abs_tol=1e-15,
        )


def test_json_output_is_deterministic(capsys) -> None:
    module = _load_witness()
    assert module.main() == 0
    first = capsys.readouterr().out
    assert module.main() == 0
    second = capsys.readouterr().out
    assert first == second
    payload = json.loads(first)
    assert payload["proper_marginal_subset_count"] == 63
    assert payload["paired_complement_group_size"] == 8
    assert payload["typed_agent_permutation_count"] == 6
    assert payload["pair_partition_preserving_coordinate_symmetry_count"] == 48
    assert payload["pairwise_record_cancellation"] == {
        "cancelling_ab_coefficient": "0",
        "eta": "1/3",
        "minimum_atom": "1/12",
        "product_ab_coefficient": "1/4",
        "same_marginal_kernels": True,
        "strictly_positive": True,
    }
    assert payload["odd_flip_scalar_equivariant"] is False
    assert payload["odd_flip_pseudoscalar_equivariant"] is True
    assert payload["center"]["c"] == "1/128"
    assert payload["center"]["residual_diagonal"] == "4/16383"
    assert payload["record"]["evidence"] == "1/2"
    assert payload["block_vfe"]["direction_kind"] == "kappa_lift"
    assert payload["block_vfe"]["outside_marginal_equal"] is True
    assert [item["agent_coordinates"] for item in payload["agent_theta_block_vfe"]] == [
        [0, 1],
        [2, 3],
        [4, 5],
    ]
    assert all(
        item["direction_kind"] == "agent_theta_block"
        and item["outside_theta_equal"]
        and item["outside_marginal_equal"]
        and item["outside_tangent_zero"]
        for item in payload["agent_theta_block_vfe"]
    )
