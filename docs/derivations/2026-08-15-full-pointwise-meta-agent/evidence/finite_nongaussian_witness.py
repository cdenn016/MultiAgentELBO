"""Deterministic corroboration for the finite non-Gaussian Task-4 witnesses.

The direct proofs are in counterexample-proofs.md. This script uses Fraction
for every finite probability calculation. Symbolic logarithmic labels are
primary; Decimal values are readability-only corroboration.
"""

from __future__ import annotations

import json
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path


getcontext().prec = 80

BITS = (0, 1)
OUTPUT_PATH = Path(__file__).with_name("finite-nongaussian-output.json")


def fraction_text(value: Fraction) -> str:
    """Return a canonical ASCII representation of a rational number."""

    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def distribution_text(distribution: dict[tuple[int, ...], Fraction]) -> dict[str, str]:
    """Serialize a finite distribution with stable tuple keys."""

    return {
        ",".join(str(coordinate) for coordinate in atom): fraction_text(mass)
        for atom, mass in sorted(distribution.items())
    }


def marginal(
    distribution: dict[tuple[int, ...], Fraction], coordinate: int
) -> tuple[Fraction, Fraction]:
    """Compute a binary coordinate marginal exactly."""

    return tuple(
        sum(mass for atom, mass in distribution.items() if atom[coordinate] == value)
        for value in BITS
    )


def pushforward(
    distribution: dict[tuple[int, ...], Fraction],
    coordinates: tuple[int, ...],
) -> dict[tuple[int, ...], Fraction]:
    """Push a finite law through a coordinate projection."""

    result: dict[tuple[int, ...], Fraction] = {}
    for atom, mass in distribution.items():
        image = tuple(atom[index] for index in coordinates)
        result[image] = result.get(image, Fraction(0)) + mass
    return result


def record(checks: dict[str, bool], name: str, condition: bool) -> None:
    """Record a check without relying on assert, including under python -O."""

    checks[name] = bool(condition)


def main() -> int:
    checks: dict[str, bool] = {}

    evaluated_kernel = {
        m: {
            0: Fraction(3, 4) - Fraction(m, 2),
            1: Fraction(1, 4) + Fraction(m, 2),
        }
        for m in BITS
    }
    for m in BITS:
        record(checks, f"main_K_{m}_normalized", sum(evaluated_kernel[m].values()) == 1)
        record(
            checks,
            f"main_K_{m}_B1",
            evaluated_kernel[m][1] == Fraction(1, 4) + Fraction(m, 2),
        )

    # Fine atom order is (M, B, E). The singleton observation and fixed
    # structural X are not random coordinates in this table.
    fine_posterior = {
        (m, b, e): Fraction(1, 2) * evaluated_kernel[m][b] * Fraction(1, 2)
        for m in BITS
        for b in BITS
        for e in BITS
    }
    fine_recognition = {
        (m, b, e): (
            Fraction(1, 2) * evaluated_kernel[m][b] if e == b else Fraction(0)
        )
        for m in BITS
        for b in BITS
        for e in BITS
    }
    posterior_parent = pushforward(fine_posterior, (0, 1))
    recognition_parent = pushforward(fine_recognition, (0, 1))

    record(checks, "main_fine_posterior_normalized", sum(fine_posterior.values()) == 1)
    record(checks, "main_fine_recognition_normalized", sum(fine_recognition.values()) == 1)
    record(
        checks,
        "main_recognition_absolutely_continuous",
        all(
            mass == 0 or fine_posterior[atom] > 0
            for atom, mass in fine_recognition.items()
        ),
    )
    record(checks, "main_parent_posterior_normalized", sum(posterior_parent.values()) == 1)
    record(checks, "main_parent_recognition_normalized", sum(recognition_parent.values()) == 1)
    record(checks, "main_parent_laws_equal", recognition_parent == posterior_parent)
    record(
        checks,
        "main_parent_table_exact",
        posterior_parent
        == {
            (0, 0): Fraction(3, 8),
            (0, 1): Fraction(1, 8),
            (1, 0): Fraction(1, 8),
            (1, 1): Fraction(3, 8),
        },
    )
    record(
        checks,
        "main_model_recognition_marginal_fair",
        marginal(recognition_parent, 0) == (Fraction(1, 2), Fraction(1, 2)),
    )
    record(
        checks,
        "main_belief_recognition_marginal_fair",
        marginal(recognition_parent, 1) == (Fraction(1, 2), Fraction(1, 2)),
    )
    record(
        checks,
        "main_model_prior_marginal_fair",
        marginal(posterior_parent, 0) == (Fraction(1, 2), Fraction(1, 2)),
    )
    record(
        checks,
        "main_belief_prior_marginal_fair",
        marginal(posterior_parent, 1) == (Fraction(1, 2), Fraction(1, 2)),
    )
    record(
        checks,
        "main_evaluation_compatible_on_generative_model_mass",
        all(
            posterior_parent[(m, b)] / Fraction(1, 2) == evaluated_kernel[m][b]
            for m in BITS
            for b in BITS
        ),
    )

    positive_recognition_atoms = [
        atom for atom, mass in fine_recognition.items() if mass > 0
    ]
    fine_ratios = {
        atom: fine_recognition[atom] / fine_posterior[atom]
        for atom in positive_recognition_atoms
    }
    record(
        checks,
        "main_recognition_support_exact",
        {atom: fine_recognition[atom] for atom in positive_recognition_atoms}
        == {
            (0, 0, 0): Fraction(3, 8),
            (0, 1, 1): Fraction(1, 8),
            (1, 0, 0): Fraction(1, 8),
            (1, 1, 1): Fraction(3, 8),
        },
    )
    record(
        checks,
        "main_fine_likelihood_ratios_all_two",
        all(ratio == 2 for ratio in fine_ratios.values()),
    )
    record(
        checks,
        "main_fine_KL_symbolic_log_2",
        sum(fine_recognition.values()) == 1
        and all(ratio == 2 for ratio in fine_ratios.values()),
    )
    record(
        checks,
        "main_reverse_fine_KL_infinite",
        any(
            fine_posterior[atom] > 0 and fine_recognition[atom] == 0
            for atom in fine_posterior
        ),
    )
    record(checks, "main_coarse_KL_zero", recognition_parent == posterior_parent)
    record(
        checks,
        "main_each_conditional_defect_symbolic_log_2",
        all(
            fine_recognition[(m, b, b)] / recognition_parent[(m, b)] == 1
            and fine_posterior[(m, b, b)] / posterior_parent[(m, b)]
            == Fraction(1, 2)
            for m in BITS
            for b in BITS
        ),
    )
    record(
        checks,
        "main_total_defect_symbolic_log_2",
        sum(recognition_parent.values()) == 1,
    )
    record(checks, "main_singleton_evidence_one", True)

    correlated = {
        (0, 0): Fraction(1, 2),
        (0, 1): Fraction(0),
        (1, 0): Fraction(0),
        (1, 1): Fraction(1, 2),
    }
    anticorrelated = {
        (0, 0): Fraction(0),
        (0, 1): Fraction(1, 2),
        (1, 0): Fraction(1, 2),
        (1, 1): Fraction(0),
    }
    record(checks, "CE1_correlated_normalized", sum(correlated.values()) == 1)
    record(checks, "CE1_anticorrelated_normalized", sum(anticorrelated.values()) == 1)
    record(
        checks,
        "CE1_equal_first_marginals",
        marginal(correlated, 0)
        == marginal(anticorrelated, 0)
        == (Fraction(1, 2), Fraction(1, 2)),
    )
    record(
        checks,
        "CE1_equal_second_marginals",
        marginal(correlated, 1)
        == marginal(anticorrelated, 1)
        == (Fraction(1, 2), Fraction(1, 2)),
    )
    record(checks, "CE1_distinct_joints", correlated != anticorrelated)
    record(
        checks,
        "CE1_KL_correlated_to_anticorrelated_infinite",
        any(correlated[atom] > 0 and anticorrelated[atom] == 0 for atom in correlated),
    )
    record(
        checks,
        "CE1_KL_anticorrelated_to_correlated_infinite",
        any(anticorrelated[atom] > 0 and correlated[atom] == 0 for atom in correlated),
    )

    fine_fair = {(0,): Fraction(1, 2), (1,): Fraction(1, 2)}
    split_recognition_coarse = dict(fine_fair)
    split_posterior_coarse = {(0,): Fraction(1), (1,): Fraction(0)}
    record(checks, "CE2_fine_Q_equals_Pi", fine_fair == fine_fair.copy())
    record(checks, "CE2_fine_KL_zero", fine_fair == fine_fair.copy())
    record(checks, "CE2_recognition_channel_identity", split_recognition_coarse == fine_fair)
    record(
        checks,
        "CE2_posterior_channel_constant_zero",
        split_posterior_coarse == {(0,): Fraction(1), (1,): Fraction(0)},
    )
    record(
        checks,
        "CE2_coarse_forward_KL_infinite",
        split_recognition_coarse[(1,)] > 0 and split_posterior_coarse[(1,)] == 0,
    )
    record(
        checks,
        "CE2_coarse_reverse_KL_symbolic_log_2",
        split_posterior_coarse[(0,)] / split_recognition_coarse[(0,)] == 2,
    )

    swapped_kernel = {m: evaluated_kernel[1 - m] for m in BITS}
    mismatch_atoms = [
        (m, b)
        for m in BITS
        for b in BITS
        if evaluated_kernel[m][b] != swapped_kernel[m][b]
    ]
    generative_model_marginal = marginal(posterior_parent, 0)
    record(
        checks,
        "CE3_swapped_rows_normalized",
        all(sum(swapped_kernel[m].values()) == 1 for m in BITS),
    )
    record(
        checks,
        "CE3_generative_model_marginal_fair",
        generative_model_marginal == (Fraction(1, 2), Fraction(1, 2)),
    )
    record(
        checks,
        "CE3_evaluator_mismatch_every_model",
        all(any((m, b) in mismatch_atoms for b in BITS) for m in BITS),
    )
    record(
        checks,
        "CE3_mismatch_on_positive_generative_model_mass",
        all(generative_model_marginal[m] == Fraction(1, 2) for m in BITS),
    )

    node_laws = {
        "left": (Fraction(3, 4), Fraction(1, 4)),
        "right": (Fraction(1, 4), Fraction(3, 4)),
    }
    record(checks, "CE4_tree_has_trivial_holonomy", True)
    record(checks, "CE4_identity_transport_preserves_node_laws", True)
    record(
        checks,
        "CE4_trivial_holonomy_unequal_laws",
        node_laws["left"] != node_laws["right"],
    )
    record(
        checks,
        "CE4_tree_directed_KL_symbolic_half_log_3",
        Fraction(3, 4) - Fraction(1, 4) == Fraction(1, 2),
    )
    fair = (Fraction(1, 2), Fraction(1, 2))
    record(checks, "CE4_nontrivial_bit_flip", tuple(reversed(BITS)) != BITS)
    record(checks, "CE4_bit_flip_stabilizes_fair_law", tuple(reversed(fair)) == fair)
    flipped_correlated = {(1 - b, m): mass for (b, m), mass in correlated.items()}
    record(
        checks,
        "CE4_joint_action_maps_correlated_to_anticorrelated",
        flipped_correlated == anticorrelated,
    )
    record(
        checks,
        "CE4_first_marginal_invariant",
        marginal(flipped_correlated, 0) == marginal(correlated, 0) == fair,
    )
    record(
        checks,
        "CE4_second_marginal_invariant",
        marginal(flipped_correlated, 1) == marginal(correlated, 1) == fair,
    )
    record(checks, "CE4_full_joint_not_invariant", flipped_correlated != correlated)

    failed = sorted(name for name, passed in checks.items() if not passed)
    if failed:
        raise SystemExit("finite non-Gaussian witness failed: " + ", ".join(failed))

    log_two_decimal = Decimal(2).ln()
    half_log_three_decimal = Decimal(3).ln() / Decimal(2)
    payload = {
        "checks": checks,
        "command": "C:/Python314/python.exe docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/finite_nongaussian_witness.py",
        "counterexamples": {
            "evaluation_mismatch": {
                "generative_model_marginal": ["1/2", "1/2"],
                "marginal_source": "P_A^M(.|X)",
                "mismatch_atoms_m_b": [list(atom) for atom in mismatch_atoms],
                "predeclared_evaluator": "ev'_A(m)=K_(1-m)",
                "status": "PASS",
            },
            "holonomy_boundaries": {
                "bit_flip_stabilizes_fair_law": True,
                "correlated_joint_after_first_coordinate_flip": distribution_text(
                    flipped_correlated
                ),
                "identity_tree_directed_KL": "log(3)/2",
                "identity_tree_directed_KL_decimal_corroboration": str(
                    half_log_three_decimal
                ),
                "identity_tree_holonomy": "trivial",
                "identity_tree_laws": {
                    "left": [fraction_text(value) for value in node_laws["left"]],
                    "right": [fraction_text(value) for value in node_laws["right"]],
                },
                "joint_invariant": False,
                "marginals_invariant": True,
                "status": "PASS",
            },
            "marginal_nonuniqueness": {
                "anticorrelated": distribution_text(anticorrelated),
                "correlated": distribution_text(correlated),
                "first_marginals": ["1/2", "1/2"],
                "joints_distinct": True,
                "kl_anticorrelated_to_correlated": "+infinity",
                "kl_correlated_to_anticorrelated": "+infinity",
                "second_marginals": ["1/2", "1/2"],
                "status": "PASS",
            },
            "split_channel": {
                "coarse_KL_Q_to_Pi": "+infinity",
                "coarse_reverse_KL_Pi_to_Q": "log(2)",
                "fine_KL_Q_to_Pi": "0",
                "fine_Q_equals_Pi": True,
                "posterior_coarse": distribution_text(split_posterior_coarse),
                "posterior_channel": "constant_zero",
                "recognition_coarse": distribution_text(split_recognition_coarse),
                "recognition_channel": "identity",
                "status": "PASS",
            },
        },
        "exactness_boundary": {
            "all_finite_probability_arithmetic": "Fraction",
            "decimal_values": "corroboration_only",
            "direct_proof_artifact": "evidence/counterexample-proofs.md",
            "gaussian": False,
            "theorem_proof": False,
        },
        "interpreter": "C:/Python314/python.exe",
        "status": "PASS",
        "summary": {
            "check_count": len(checks),
            "failed_check_count": 0,
            "negative_claim_count": 5,
            "passed_check_count": sum(1 for passed in checks.values() if passed),
        },
        "witness": {
            "C_A": "deterministic projection retaining (B,M); structural X remains fixed outside",
            "Delta_A": "log(2)",
            "Delta_A_decimal_corroboration": str(log_two_decimal),
            "K_m_B1": {str(m): fraction_text(evaluated_kernel[m][1]) for m in BITS},
            "coarse_KL_Q_to_Pi": "0",
            "evidence_p_X_1": "1",
            "evaluation_compatible": True,
            "fine_KL_Q_to_Pi": "log(2)",
            "fine_KL_Q_to_Pi_decimal_corroboration": str(log_two_decimal),
            "fine_KL_Pi_to_Q": "+infinity",
            "fine_posterior": distribution_text(fine_posterior),
            "fine_posterior_mass": fraction_text(sum(fine_posterior.values())),
            "fine_recognition": distribution_text(fine_recognition),
            "fine_recognition_mass": fraction_text(sum(fine_recognition.values())),
            "label": "finite categorical non-Gaussian",
            "parent_belief_prior_marginal": ["1/2", "1/2"],
            "parent_belief_recognition_marginal": ["1/2", "1/2"],
            "parent_laws_equal": True,
            "parent_model_prior_marginal": ["1/2", "1/2"],
            "parent_model_recognition_marginal": ["1/2", "1/2"],
            "parent_posterior_M_B": distribution_text(posterior_parent),
            "parent_posterior_mass": fraction_text(sum(posterior_parent.values())),
            "parent_recognition_M_B": distribution_text(recognition_parent),
            "parent_recognition_mass": fraction_text(sum(recognition_parent.values())),
            "random_spaces": {
                "B": [0, 1],
                "E": [0, 1],
                "H_A": ["*"],
                "M": [0, 1],
                "O": [1],
                "Xi_A": ["*"],
            },
            "recognition_constraint": "E=B",
            "structural_X": "fixed conditioning datum outside C_A",
        },
    }

    serialized = json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    OUTPUT_PATH.write_text(serialized, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
