from fractions import Fraction

import numpy as np

from multiagent_elbo.finite.permutations import FinitePermutation
from multiagent_elbo.geometry import FinitePermutation as GeometryFinitePermutation
from multiagent_elbo.geometry.finite_gauge import (
    FinitePermutation as FiniteGaugePermutation,
)


def test_three_cycle_has_one_canonical_direction_and_explicit_inverse():
    cycle = FinitePermutation.from_old_to_new((1, 2, 0))

    assert cycle.old_to_new == (1, 2, 0)
    assert cycle.new_to_old == (2, 0, 1)
    assert cycle.pullback_law(
        (Fraction(1, 5), Fraction(3, 10), Fraction(1, 2))
    ) == (Fraction(1, 2), Fraction(1, 5), Fraction(3, 10))
    assert cycle.then(cycle.inverse()).old_to_new == (0, 1, 2)


def test_composition_matches_sequential_pullback():
    p = FinitePermutation.from_old_to_new((1, 2, 0))
    q = FinitePermutation.from_old_to_new((2, 0, 1))
    values = np.arange(9).reshape(3, 3)

    np.testing.assert_array_equal(
        p.then(q).pullback_axis(values, axis=0),
        q.pullback_axis(p.pullback_axis(values, axis=0), axis=0),
    )


def test_geometry_matrix_adapter_builds_the_same_permutation():
    matrix = ((0, 1, 0), (0, 0, 1), (1, 0, 0))
    expected = FinitePermutation.from_old_to_new((1, 2, 0))

    assert FinitePermutation.from_matrix(matrix) == expected
    assert GeometryFinitePermutation is FinitePermutation
    assert FiniteGaugePermutation is FinitePermutation


def test_channel_pullback_reindexes_source_and_target_supports():
    source = FinitePermutation.from_old_to_new((1, 2, 0))
    target = FinitePermutation.from_old_to_new((2, 0, 1))
    rows = ((0, 1, 2), (3, 4, 5), (6, 7, 8))

    np.testing.assert_array_equal(
        source.pullback_channel(rows, target),
        ((7, 8, 6), (1, 2, 0), (4, 5, 3)),
    )
