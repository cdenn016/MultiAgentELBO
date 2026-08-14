"""Exact finite checks for the presentation-descent theorem package.

The rational identities corroborate the hand derivations. They are not a
proof of the universal statements in the accompanying mathematical artifacts.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction


def _text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _fisher(probabilities, derivatives_left, derivatives_right) -> Fraction:
    return sum(
        left * right / probability
        for probability, left, right in zip(
            probabilities, derivatives_left, derivatives_right, strict=True
        )
    )


def main() -> int:
    a = Fraction(1, 10)
    b = Fraction(1, 8)
    retained_crossover = a + b - 2 * a * b
    assert retained_crossover == Fraction(1, 5)

    retained_fisher = 1 / (retained_crossover * (1 - retained_crossover))
    derivative_b = 1 / (1 - 2 * a)
    full_fisher = derivative_b**2 / (b * (1 - b))
    assert retained_fisher == Fraction(25, 4)
    assert full_fisher == Fraction(100, 7)
    assert full_fisher - retained_fisher == Fraction(225, 28)

    failure_a = Fraction(1, 4)
    failure_b = Fraction(1, 3)
    eta = Fraction(2, 5)
    lam = Fraction(1, 2)
    failure_delta = failure_a + failure_b - 2 * failure_a * failure_b
    assert failure_delta == Fraction(5, 12)
    retained_tensor = [
        [Fraction(16, 35), Fraction(24, 35), Fraction(0)],
        [Fraction(24, 35), Fraction(36, 35), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0)],
    ]
    full_l0 = [Fraction(16, 3), Fraction(9, 2), Fraction(0)]
    full_lplus = [Fraction(16, 3), Fraction(9, 2), Fraction(25, 6)]
    null_kl = float(lam) * math.log(float(lam / eta)) + float(1 - lam) * math.log(
        float((1 - lam) / (1 - eta))
    )
    assert abs(null_kl - 0.5 * math.log(25.0 / 24.0)) < 1e-15
    assert 1 - failure_b == Fraction(2, 3)

    product = [Fraction(1, 4)] * 4
    correlated = [Fraction(9, 32), Fraction(7, 32), Fraction(7, 32), Fraction(9, 32)]
    assert correlated[0] + correlated[1] == Fraction(1, 2)
    assert correlated[0] + correlated[2] == Fraction(1, 2)

    derivative_q = [Fraction(1, 2), Fraction(1, 2), Fraction(-1, 2), Fraction(-1, 2)]
    derivative_r = [Fraction(1, 2), Fraction(-1, 2), Fraction(1, 2), Fraction(-1, 2)]
    product_metric = [
        [_fisher(product, derivative_q, derivative_q), _fisher(product, derivative_q, derivative_r)],
        [_fisher(product, derivative_r, derivative_q), _fisher(product, derivative_r, derivative_r)],
    ]
    correlated_metric = [
        [_fisher(correlated, derivative_q, derivative_q), _fisher(correlated, derivative_q, derivative_r)],
        [_fisher(correlated, derivative_r, derivative_q), _fisher(correlated, derivative_r, derivative_r)],
    ]
    assert product_metric == [[Fraction(4), Fraction(0)], [Fraction(0), Fraction(4)]]
    assert correlated_metric == [
        [Fraction(256, 63), Fraction(-32, 63)],
        [Fraction(-32, 63), Fraction(256, 63)],
    ]
    assert [
        correlated_metric[0][0] - Fraction(4) + correlated_metric[0][1],
        correlated_metric[0][0] - Fraction(4) - correlated_metric[0][1],
    ] == [Fraction(-4, 9), Fraction(4, 7)]

    kl_product_to_correlated = sum(
        source * math.log(float(source / target))
        for source, target in zip(product, correlated, strict=True)
    )
    expected_kl = 0.5 * math.log(64.0 / 63.0)
    assert abs(kl_product_to_correlated - expected_kl) < 1e-15

    correlated_to_uniform = sum(
        source * math.log(float(source / target))
        for source, target in zip(correlated, product, strict=True)
    )
    expected_correlated_vfe = (9.0 / 16.0) * math.log(9.0 / 8.0) + (
        7.0 / 16.0
    ) * math.log(7.0 / 8.0)
    assert abs(correlated_to_uniform - expected_correlated_vfe) < 1e-15
    assert correlated_to_uniform > 0

    payload = {
        "bsc": {
            "a": _text(a),
            "b": _text(b),
            "retained_crossover": _text(retained_crossover),
            "retained_fisher": _text(retained_fisher),
            "full_fisher": _text(full_fisher),
            "fisher_gap": _text(full_fisher - retained_fisher),
        },
        "failure_certificate": {
            "delta": _text(failure_delta),
            "retained_tensor": [[_text(value) for value in row] for row in retained_tensor],
            "full_l0_diagonal": [_text(value) for value in full_l0],
            "full_lplus_diagonal": [_text(value) for value in full_lplus],
            "null_kl_exact": "log(25/24)/2",
            "intervention_match_probability": "2/3",
        },
        "categorical_lifts": {
            "product_metric": [[_text(value) for value in row] for row in product_metric],
            "correlated_metric": [[_text(value) for value in row] for row in correlated_metric],
            "metric_difference_eigenvalues": ["-4/9", "4/7"],
            "kl_product_to_correlated": kl_product_to_correlated,
            "kl_exact": "log(64/63)/2",
            "correlated_vfe": correlated_to_uniform,
        },
    }
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
