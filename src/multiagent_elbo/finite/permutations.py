"""Canonical finite permutations and pullbacks for ordered finite objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


def _validated_old_to_new(old_to_new: Sequence[int]) -> tuple[int, ...]:
    values = tuple(old_to_new)
    if not values:
        raise ValueError("old_to_new permutation must be nonempty")
    if any(type(value) is not int for value in values):
        raise TypeError("old_to_new entries must be ints")
    if sorted(values) != list(range(len(values))):
        raise ValueError("old_to_new must be a bijection over 0..n-1")
    return values


def _old_to_new_from_matrix(matrix: Sequence[Sequence[float]]) -> tuple[int, ...]:
    values = np.array(matrix, dtype=np.float64, copy=True, order="C")
    if values.ndim != 2 or values.shape[0] != values.shape[1]:
        raise ValueError("permutation matrix must be square")
    if values.shape[0] == 0:
        raise ValueError("permutation matrix must be nonempty")
    if not np.all(np.isfinite(values)):
        raise ValueError("permutation matrix must be finite")
    if not np.all((values == 0.0) | (values == 1.0)):
        raise ValueError("permutation matrix must be exactly zero-one")
    if not (
        np.all(values.sum(axis=0) == 1.0) and np.all(values.sum(axis=1) == 1.0)
    ):
        raise ValueError("each permutation row and column must contain one unit entry")
    return tuple(int(index) for index in np.argmax(values, axis=1))


@dataclass(frozen=True, init=False)
class FinitePermutation:
    """An immutable finite permutation with old-to-new canonical storage."""

    old_to_new: tuple[int, ...]

    def __init__(self, old_to_new: Sequence[int] | Sequence[Sequence[float]]) -> None:
        """Create from an index map; accept legacy matrices for compatibility."""
        raw_values = tuple(old_to_new)
        if np.asarray(raw_values).ndim == 2:
            values = _old_to_new_from_matrix(raw_values)  # type: ignore[arg-type]
        else:
            values = _validated_old_to_new(raw_values)  # type: ignore[arg-type]
        object.__setattr__(self, "old_to_new", values)

    @classmethod
    def from_old_to_new(cls, old_to_new: Sequence[int]) -> "FinitePermutation":
        return cls(_validated_old_to_new(old_to_new))

    @classmethod
    def from_matrix(
        cls, matrix: Sequence[Sequence[float]]
    ) -> "FinitePermutation":
        return cls.from_old_to_new(_old_to_new_from_matrix(matrix))

    @property
    def size(self) -> int:
        return len(self.old_to_new)

    @property
    def new_to_old(self) -> tuple[int, ...]:
        inverse = [0] * self.size
        for old, new in enumerate(self.old_to_new):
            inverse[new] = old
        return tuple(inverse)

    @property
    def matrix(self) -> np.ndarray:
        """Materialize the old-to-new permutation matrix as a read-only array."""
        result = np.zeros((self.size, self.size), dtype=np.float64)
        result[np.arange(self.size), self.old_to_new] = 1.0
        result.setflags(write=False)
        return result

    def inverse(self) -> "FinitePermutation":
        return self.from_old_to_new(self.new_to_old)

    def then(self, after: "FinitePermutation") -> "FinitePermutation":
        """Return the permutation that applies this map and then ``after``."""
        if not isinstance(after, FinitePermutation):
            raise TypeError("after must be a FinitePermutation")
        if self.size != after.size:
            raise ValueError("permutations must have the same size")
        return self.from_old_to_new(
            tuple(after.old_to_new[new] for new in self.old_to_new)
        )

    def pullback_axis(self, values: object, axis: int = 0) -> np.ndarray:
        return np.take(np.asarray(values), self.new_to_old, axis=axis)

    def pullback_law(self, values: Sequence[object]) -> tuple[object, ...]:
        if len(values) != self.size:
            raise ValueError("law must have one value per permutation index")
        return tuple(values[old] for old in self.new_to_old)

    def pullback_channel(
        self, rows: object, target_permutation: "FinitePermutation"
    ) -> np.ndarray:
        """Pull a row-stochastic channel back on its source and target supports."""
        if not isinstance(target_permutation, FinitePermutation):
            raise TypeError("target_permutation must be a FinitePermutation")
        values = np.asarray(rows)
        if values.ndim != 2:
            raise ValueError("channel rows must be two-dimensional")
        if values.shape != (self.size, target_permutation.size):
            raise ValueError("channel shape must match source and target permutations")
        return target_permutation.pullback_axis(
            self.pullback_axis(values, axis=0), axis=1
        )
