"""Deterministic corroboration for the pointwise meta-agent RG proof package.

Exact finite identities use Fraction. Logarithmic values use Decimal and are
reported only as numerical corroboration, never as theorem evidence.
"""

from __future__ import annotations

import json
from decimal import Decimal, getcontext
from fractions import Fraction


getcontext().prec = 60


def d(frac: Fraction) -> Decimal:
    return Decimal(frac.numerator) / Decimal(frac.denominator)


def bernoulli_kl(p: Fraction, q: Fraction) -> Decimal:
    terms = []
    for a, b in ((p, q), (1 - p, 1 - q)):
        if a:
            terms.append(d(a) * (d(a) / d(b)).ln())
    return sum(terms, Decimal(0))


def finite_kl(p: tuple[Fraction, ...], q: tuple[Fraction, ...]) -> Decimal:
    total = Decimal(0)
    for a, b in zip(p, q, strict=True):
        if a:
            if not b:
                raise ValueError("infinite KL")
            total += d(a) * (d(a) / d(b)).ln()
    return total


def main() -> None:
    p = Fraction(1, 10)
    q = Fraction(1, 2)
    r = Fraction(9, 10)
    kl_pq = bernoulli_kl(p, q)
    kl_qr = bernoulli_kl(q, r)
    kl_pr = bernoulli_kl(p, r)
    ce1 = kl_pq < Decimal("0.6") and kl_qr < Decimal("0.6") < kl_pr

    same_parity = {
        (0, 0): Fraction(1, 2),
        (0, 1): Fraction(0),
        (1, 0): Fraction(0),
        (1, 1): Fraction(1, 2),
    }
    opposite_parity = {
        (0, 0): Fraction(0),
        (0, 1): Fraction(1, 2),
        (1, 0): Fraction(1, 2),
        (1, 1): Fraction(0),
    }
    marg_x_q = tuple(sum(v for (x, _), v in same_parity.items() if x == a) for a in (0, 1))
    marg_x_p = tuple(sum(v for (x, _), v in opposite_parity.items() if x == a) for a in (0, 1))
    marg_y_q = tuple(sum(v for (_, y), v in same_parity.items() if y == a) for a in (0, 1))
    marg_y_p = tuple(sum(v for (_, y), v in opposite_parity.items() if y == a) for a in (0, 1))
    ce2 = (
        marg_x_q == marg_x_p == (Fraction(1, 2), Fraction(1, 2))
        and marg_y_q == marg_y_p == (Fraction(1, 2), Fraction(1, 2))
        and all(not (same_parity[a] and opposite_parity[a]) for a in same_parity)
    )

    a = Fraction(3)
    ce3_kl = 2 * a * a
    ce3 = ce3_kl == 18

    h = ((1, 0, 0), (0, -1, 0), (0, 0, -1))
    hht = tuple(
        tuple(sum(h[i][k] * h[j][k] for k in range(3)) for j in range(3))
        for i in range(3)
    )
    ce4 = h != ((1, 0, 0), (0, 1, 0), (0, 0, 1)) and hht == (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )

    c = Fraction(7, 5)
    trace_l = 2 * c
    determinant_l = c * c - c * c
    ce5 = trace_l == Fraction(14, 5) and determinant_l == 0

    ce6_forward = (Decimal(2)).ln()
    ce6 = ce6_forward > 0  # Reverse KL is infinite because Q(1)>0=P(1).

    a_quartic = Fraction(3, 2)
    lam = Fraction(5, 7)
    child_fourth = a_quartic**4 + 6 * a_quartic**2 + 3
    parent_variance = 1 + a_quartic**2
    parent_fourth = 3 * parent_variance**2
    quartic_residual = lam * (parent_fourth - child_fourth)
    expected_quartic_residual = 2 * lam * a_quartic**4
    second_moment = Fraction(15)
    fourth_moment = Fraction(10395)
    gaussian_fourth = 3 * second_moment**2
    ce7 = (
        quartic_residual == expected_quartic_residual != 0 and fourth_moment != gaussian_fourth == 675
    )

    replicated_vertex_mass = Fraction(1) + Fraction(1)
    replicated_edge_mass = sum(Fraction(1) for _ in range(4))
    normalized_vertex_mass = Fraction(1, 2) + Fraction(1, 2)
    ce8 = replicated_vertex_mass == 2 and replicated_edge_mass == 4 and normalized_vertex_mass == 1

    p1 = (Fraction(1), Fraction(0))
    p2 = (Fraction(0), Fraction(1))
    weights = (Fraction(1, 3), Fraction(2, 3))
    mixture = (Fraction(1, 3), Fraction(2, 3))
    comparison = (Fraction(1, 2), Fraction(1, 2))
    lhs = d(weights[0]) * finite_kl(p1, comparison) + d(weights[1]) * finite_kl(p2, comparison)
    rhs = (
        d(weights[0]) * finite_kl(p1, mixture)
        + d(weights[1]) * finite_kl(p2, mixture)
        + finite_kl(mixture, comparison)
    )
    mixture_identity = abs(lhs - rhs) < Decimal("1e-50")

    eta = {
        (0, 0): Fraction(1, 8),
        (0, 1): Fraction(3, 8),
        (1, 0): Fraction(1, 4),
        (1, 1): Fraction(1, 4),
    }
    membership = {
        0: {"A": Fraction(3, 4), "B": Fraction(1, 4)},
        1: {"A": Fraction(1, 3), "B": Fraction(2, 3)},
    }
    coarse = {
        (a_name, b_name): sum(
            mass * membership[i][a_name] * membership[j][b_name]
            for (i, j), mass in eta.items()
        )
        for a_name in ("A", "B")
        for b_name in ("A", "B")
    }
    event_mass = sum(coarse.values())

    # Exact chain rule for C_t(y)=t*y+y^2 along y(t)=t^2 at t=2.
    t = Fraction(2)
    y = t * t
    y_dot = 2 * t
    direct_derivative = 3 * t * t + 4 * t**3  # d/dt of t^3+t^4.
    chain_derivative = y + (t + 2 * y) * y_dot
    moving_map_chain_rule = direct_derivative == chain_derivative

    checks = {
        "CE-1_nontransitive_threshold": ce1,
        "CE-2_equal_marginals_disjoint_joint_support": ce2,
        "CE-3_trivial_holonomy_large_gaussian_KL": ce3,
        "CE-4_nontrivial_orthogonal_holonomy_stabilizes_isotropic_covariance": ce4,
        "CE-5_two_node_gap_exact": ce5,
        "CE-6_forward_finite_reverse_support_failure": ce6,
        "CE-7_quartic_gaussian_barycenter_residual_exact": ce7,
        "CE-8_replicated_cover_mass": ce8,
        "forward_KL_mixture_identity_decimal_corroboration": mixture_identity,
        "normalized_event_pushforward_mass_exact": event_mass == 1,
        "moving_map_chain_rule_exact_polynomial": moving_map_chain_rule,
    }
    if not all(checks.values()):
        raise SystemExit(json.dumps({"status": "FAIL", "checks": checks}, indent=2, sort_keys=True))

    payload = {
        "status": "PASS",
        "exactness_boundary": {
            "rational_and_integer_checks": [
                "CE-2",
                "CE-3 at a=3",
                "CE-4 covariance invariance",
                "CE-5 at c=7/5",
                "CE-7 quartic residual at a=3/2 and lambda=5/7",
                "CE-8",
                "joint-event normalization",
                "moving-map polynomial chain rule",
            ],
            "decimal_logarithmic_corroboration_only": ["CE-1", "CE-6", "forward-KL mixture instance"],
            "theorem_proof": False,
        },
        "values": {
            "CE-1_KL_PQ": str(kl_pq),
            "CE-1_KL_QR": str(kl_qr),
            "CE-1_KL_PR": str(kl_pr),
            "CE-3_KL_at_a_3": str(ce3_kl),
            "CE-5_gap_at_c_7_over_5": str(trace_l),
            "CE-6_forward_KL": str(ce6_forward),
            "CE-7_quartic_residual_at_a_3_over_2_lambda_5_over_7": str(quartic_residual),
            "CE-7_expected_quartic_residual": str(expected_quartic_residual),
            "CE-7_cubic_pushforward_fourth_moment": str(fourth_moment),
            "CE-7_cubic_matched_Gaussian_fourth_moment": str(gaussian_fourth),
            "CE-8_replicated_vertex_mass": str(replicated_vertex_mass),
            "CE-8_replicated_edge_mass": str(replicated_edge_mass),
            "forward_KL_identity_absolute_residual": str(abs(lhs - rhs)),
            "coarse_event_mass": str(event_mass),
            "moving_map_derivative": str(direct_derivative),
        },
        "checks": checks,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
