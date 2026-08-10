from fractions import Fraction

import numpy as np
import pytest

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


@pytest.mark.parametrize(
    ("old_to_new", "error", "message"),
    [
        ((), ValueError, "nonempty"),
        ((0, 1.0), TypeError, "entries must be ints"),
        ((0, 0), ValueError, "bijection"),
    ],
)
def test_index_constructor_rejects_invalid_public_permutations(
    old_to_new: tuple[object, ...], error: type[Exception], message: str
):
    with pytest.raises(error, match=message):
        FinitePermutation.from_old_to_new(old_to_new)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("matrix", "message"),
    [
        (np.zeros((2, 3)), "square"),
        (np.empty((0, 0)), "nonempty"),
        (np.array([[np.nan]]), "finite"),
        (np.array([[0.5]]), "zero-one"),
        (np.array([[1.0, 0.0], [1.0, 0.0]]), "row and column"),
    ],
)
def test_matrix_constructor_rejects_nonpermutation_matrices(
    matrix: np.ndarray, message: str
):
    with pytest.raises(ValueError, match=message):
        FinitePermutation.from_matrix(matrix)


def test_legacy_matrix_constructor_materializes_the_public_matrix_contract():
    permutation = FinitePermutation(((0, 1), (1, 0)))

    assert permutation.old_to_new == (1, 0)
    np.testing.assert_array_equal(permutation.matrix, ((0.0, 1.0), (1.0, 0.0)))
    assert not permutation.matrix.flags.writeable


def test_composition_and_pullback_reject_incompatible_public_inputs():
    permutation = FinitePermutation.from_old_to_new((1, 0))

    with pytest.raises(TypeError, match="FinitePermutation"):
        permutation.then("after")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="same size"):
        permutation.then(FinitePermutation.from_old_to_new((1, 2, 0)))
    with pytest.raises(ValueError, match="one value"):
        permutation.pullback_law((Fraction(1),))
    with pytest.raises(IndexError, match="axis"):
        permutation.pullback_axis(np.arange(2), axis=1)


def test_channel_pullback_rejects_invalid_target_rank_and_shape():
    permutation = FinitePermutation.from_old_to_new((1, 0))

    with pytest.raises(TypeError, match="target_permutation"):
        permutation.pullback_channel(np.eye(2), "target")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="two-dimensional"):
        permutation.pullback_channel(np.array([1.0, 2.0]), permutation)
    with pytest.raises(ValueError, match="channel shape"):
        permutation.pullback_channel(np.ones((2, 3)), permutation)
