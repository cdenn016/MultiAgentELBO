"""Executable contract for the exact finite canonical-selection witness.

Every expected value is hand-derived.  This file is intentionally committed
before the witness implementation so the first run records a genuine RED.
"""

from __future__ import annotations

import importlib.util
import io
import json
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path
from types import ModuleType

import pytest


ROOT = Path(__file__).resolve().parents[1]
WITNESS = ROOT / (
    "docs/derivations/2026-08-14-canonical-dependence-selection/"
    "evidence/exact_selection_witness.py"
)
REQUIRED_API = {
    "q_rho",
    "singleton_marginals",
    "product_coupling",
    "preparation_pushforward",
    "split_pushforward",
    "faithful_quasi_inverse_counterexample",
    "dependence_fisher",
    "pushforward",
    "deterministic_completion",
    "completion_conditional_defect",
    "reference_selector_control",
    "matrix_rank",
    "bsc_retained_quotient",
    "promoted_parity_rank",
    "main",
}
FAIR_MARGINALS = (
    (Fraction(1, 2), Fraction(1, 2)),
    (Fraction(1, 2), Fraction(1, 2)),
)


def _load_witness() -> ModuleType:
    assert WITNESS.is_file(), (
        "expected RED: exact_selection_witness.py has not been implemented"
    )
    spec = importlib.util.spec_from_file_location("exact_selection_witness", WITNESS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    missing = sorted(name for name in REQUIRED_API if not callable(getattr(module, name, None)))
    assert not missing, f"expected RED: witness API is missing {missing}"
    return module


def _matvec(matrix, vector):
    return tuple(
        sum((entry * vector[index] for index, entry in enumerate(row)), Fraction(0))
        for row in matrix
    )


def test_binary_correlation_family_has_exact_atoms_marginals_and_split_law():
    witness = _load_witness()
    expected = (
        Fraction(1, 3),
        Fraction(1, 6),
        Fraction(1, 6),
        Fraction(1, 3),
    )
    law = witness.q_rho(Fraction(1, 3))

    assert law == expected
    assert sum(law, Fraction(0)) == Fraction(1)
    assert all(atom > 0 for atom in law)
    assert witness.singleton_marginals(law) == FAIR_MARGINALS
    assert witness.split_pushforward(Fraction(1, 3)) == expected
    assert sorted(law) != sorted(witness.q_rho(Fraction(1, 2)))

    with pytest.raises(ValueError):
        witness.q_rho(Fraction(-1))
    with pytest.raises(ValueError):
        witness.q_rho(Fraction(1))


def test_preparation_pushforward_forces_the_hand_derived_product_coupling():
    witness = _load_witness()
    left = (Fraction(1, 3), Fraction(2, 3))
    right = (Fraction(1, 4), Fraction(3, 4))
    expected = (
        Fraction(1, 12),
        Fraction(1, 4),
        Fraction(1, 6),
        Fraction(1, 2),
    )

    assert witness.product_coupling(left, right) == expected
    assert witness.preparation_pushforward(left, right) == expected


def test_faithful_quasi_inverse_counterexample_survives_relabeling():
    witness = _load_witness()
    quasi = witness.faithful_quasi_inverse_counterexample(
        Fraction(1, 3), Fraction(1, 2)
    )

    assert quasi["same_marginals"] is True
    assert quasi["distinct_joints"] is True
    assert quasi["distinct_relabeling_orbits"] is True
    assert quasi["marginals"] == FAIR_MARGINALS


def test_dependence_fisher_is_computed_exactly_on_two_controls():
    witness = _load_witness()

    assert witness.dependence_fisher(Fraction(1, 3)) == Fraction(9, 8)
    assert witness.dependence_fisher(Fraction(1, 2)) == Fraction(4, 3)


def test_deterministic_completion_pushes_forward_and_composes_strictly():
    witness = _load_witness()
    reference = tuple(Fraction(index, 36) for index in range(1, 9))
    fine_to_middle = (0, 0, 1, 1, 2, 2, 3, 3)
    middle_to_coarse = (0, 0, 1, 1)
    fine_to_coarse = tuple(middle_to_coarse[cell] for cell in fine_to_middle)
    target = (Fraction(1, 3), Fraction(2, 3))
    expected_direct = (
        Fraction(1, 30),
        Fraction(1, 15),
        Fraction(1, 10),
        Fraction(2, 15),
        Fraction(5, 39),
        Fraction(2, 13),
        Fraction(7, 39),
        Fraction(8, 39),
    )
    expected_middle_reference = (
        Fraction(1, 12),
        Fraction(7, 36),
        Fraction(11, 36),
        Fraction(5, 12),
    )
    expected_middle_target = (
        Fraction(1, 10),
        Fraction(7, 30),
        Fraction(11, 39),
        Fraction(5, 13),
    )

    direct = witness.deterministic_completion(reference, fine_to_coarse, target)
    middle_reference = witness.pushforward(reference, fine_to_middle, 4)
    middle_target = witness.deterministic_completion(
        middle_reference, middle_to_coarse, target
    )
    staged = witness.deterministic_completion(
        reference, fine_to_middle, middle_target
    )

    assert direct == expected_direct
    assert middle_reference == expected_middle_reference
    assert middle_target == expected_middle_target
    assert witness.pushforward(direct, fine_to_coarse, 2) == target
    assert staged == direct
    assert sum(direct, Fraction(0)) == Fraction(1)


def test_completion_conditional_defect_is_exactly_selective():
    witness = _load_witness()
    reference = tuple(Fraction(index, 36) for index in range(1, 9))
    coarse_map = (0, 0, 0, 0, 1, 1, 1, 1)
    target = (Fraction(1, 3), Fraction(2, 3))
    selected = witness.deterministic_completion(reference, coarse_map, target)
    candidate = (
        Fraction(1, 3),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(2, 3),
        Fraction(0),
        Fraction(0),
        Fraction(0),
    )

    assert witness.pushforward(candidate, coarse_map, 2) == target
    selected_defect = witness.completion_conditional_defect(
        reference, coarse_map, target, selected
    )
    candidate_defect = witness.completion_conditional_defect(
        reference, coarse_map, target, candidate
    )
    assert isinstance(selected_defect, Fraction)
    assert isinstance(candidate_defect, Fraction)
    assert selected_defect == Fraction(0)
    assert candidate_defect > 0


def test_reference_relative_selector_inherits_feasible_reference_dependence():
    witness = _load_witness()
    first = witness.reference_selector_control(Fraction(1, 3))
    second = witness.reference_selector_control(Fraction(1, 2))

    for rho, control in ((Fraction(1, 3), first), (Fraction(1, 2), second)):
        expected = witness.q_rho(rho)
        assert control["feasible"] is True
        assert control["reference"] == expected
        assert control["selected"] == expected
        assert control["marginal_target"] == FAIR_MARGINALS
    assert first["selected"] != second["selected"]


def test_fraction_gaussian_elimination_reports_exact_ranks():
    witness = _load_witness()

    assert witness.matrix_rank(()) == 0
    assert witness.matrix_rank(((Fraction(0), Fraction(0)),)) == 0
    assert witness.matrix_rank(
        (
            (Fraction(1), Fraction(2), Fraction(3)),
            (Fraction(2), Fraction(4), Fraction(6)),
            (Fraction(0), Fraction(1), Fraction(1)),
        )
    ) == 2
    assert witness.matrix_rank(
        (
            (Fraction(1), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(1)),
        )
    ) == 3


def test_bsc_retained_quotient_has_rank_one_and_two_exact_null_vectors():
    witness = _load_witness()
    control = witness.bsc_retained_quotient(Fraction(1, 5), Fraction(1, 4))
    expected_jacobian = (Fraction(1, 2), Fraction(3, 5), Fraction(0))
    expected_fisher = (
        (Fraction(100, 91), Fraction(120, 91), Fraction(0)),
        (Fraction(120, 91), Fraction(144, 91), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0)),
    )
    expected_kernel = (
        (Fraction(3, 5), Fraction(-1, 2), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    )

    assert control["retained_probability"] == Fraction(7, 20)
    assert control["jacobian"] == expected_jacobian
    assert control["fisher_pullback"] == expected_fisher
    assert control["retained_rank"] == 1
    assert control["kernel_vectors"] == expected_kernel
    assert witness.matrix_rank(expected_fisher) == 1
    for vector in expected_kernel:
        assert sum(
            (entry * vector[index] for index, entry in enumerate(expected_jacobian)),
            Fraction(0),
        ) == 0
        assert _matvec(expected_fisher, vector) == (
            Fraction(0),
            Fraction(0),
            Fraction(0),
        )


def test_promoted_parity_retains_seven_joint_directions_but_six_marginal_directions():
    witness = _load_witness()
    control = witness.promoted_parity_rank()

    full_derivative = control["full_joint_derivative"]
    singleton_derivative = control["singleton_derivative"]
    assert len(full_derivative) == 64
    assert all(len(row) == 7 for row in full_derivative)
    assert len(singleton_derivative) == 6
    assert all(len(row) == 7 for row in singleton_derivative)
    assert control["full_joint_derivative_rank"] == 7
    assert control["singleton_derivative_rank"] == 6
    assert witness.matrix_rank(full_derivative) == 7
    assert witness.matrix_rank(singleton_derivative) == 6
    assert control["singleton_kernel_generator"] == (
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(1),
    )


def test_main_emits_one_byte_stable_json_document():
    witness = _load_witness()

    def invoke():
        stream = io.StringIO()
        with redirect_stdout(stream):
            status = witness.main()
        output = stream.getvalue()
        assert status == 0
        assert output.endswith("\n")
        assert output.count("\n") == 1
        payload = json.loads(output)
        assert isinstance(payload, dict)
        assert payload
        return output.encode("utf-8"), payload

    first_bytes, first_payload = invoke()
    second_bytes, second_payload = invoke()

    assert first_bytes == second_bytes
    assert first_payload == second_payload
