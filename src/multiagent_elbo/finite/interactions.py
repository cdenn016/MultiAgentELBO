"""Full finite Hoeffding interactions against declared product references."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from types import MappingProxyType
from typing import Mapping, Sequence

import numpy as np


Subset = tuple[int, ...]


def _readonly(values: object) -> np.ndarray:
    result = np.array(values, dtype=np.float64, copy=True, order="C")
    result.setflags(write=False)
    return result


def _readonly_mapping(values: Mapping[Subset, np.ndarray]) -> Mapping[Subset, np.ndarray]:
    return MappingProxyType({subset: _readonly(array) for subset, array in values.items()})


@dataclass(frozen=True)
class InteractionDecomposition:
    """Complete product-reference subset decomposition of one finite action."""

    values: np.ndarray
    axis_references: tuple[np.ndarray, ...]
    components: Mapping[Subset, np.ndarray]
    reconstruction: np.ndarray
    reconstruction_residual_sup: float


@dataclass(frozen=True)
class InteractionProjection:
    """Explicit retained-order projection and three separately typed diagnostics."""

    maximum_order: int
    retained_values: np.ndarray
    omitted_values: np.ndarray
    omitted_components: Mapping[Subset, np.ndarray]
    theorem_coordinate_g_norm: float
    quotient_sup_norm: float
    weighted_l2_diagnostic: float


def _subsets(axis_count: int):
    for size in range(axis_count + 1):
        yield from combinations(range(axis_count), size)


def _conditional_average(
    values: np.ndarray, references: tuple[np.ndarray, ...], subset: Subset
) -> np.ndarray:
    result = values
    kept = set(subset)
    for axis in range(values.ndim - 1, -1, -1):
        if axis not in kept:
            result = np.tensordot(result, references[axis], axes=(axis, 0))
    return np.asarray(result, dtype=np.float64)


def _broadcast_component(
    component: np.ndarray,
    component_subset: Subset,
    target_subset: Subset,
    full_shape: tuple[int, ...],
) -> np.ndarray:
    component_axes = set(component_subset)
    shape = tuple(full_shape[axis] if axis in component_axes else 1 for axis in target_subset)
    return component.reshape(shape)


def _validate_references(
    references: Sequence[Sequence[float]], shape: tuple[int, ...]
) -> tuple[np.ndarray, ...]:
    if len(references) != len(shape):
        raise ValueError("axis_references must contain one reference per value axis")
    validated: list[np.ndarray] = []
    for axis, (reference, length) in enumerate(zip(references, shape)):
        values = np.array(reference, dtype=np.float64, copy=True, order="C")
        if values.ndim != 1 or values.shape[0] != length:
            raise ValueError(f"axis reference {axis} length must match its value axis")
        if not np.all(np.isfinite(values)):
            raise ValueError(f"axis reference {axis} must be finite")
        if np.any(values < 0.0):
            raise ValueError(f"axis reference {axis} must be nonnegative")
        total = float(values.sum())
        if not np.isclose(total, 1.0, rtol=1e-10, atol=1e-12):
            raise ValueError(f"axis reference {axis} must sum to one")
        values /= total
        validated.append(values)
    return tuple(validated)


def hoeffding_decompose(
    values: Sequence[object], axis_references: Sequence[Sequence[float]]
) -> InteractionDecomposition:
    """Extract every subset component by conditional averaging and Mobius inversion."""
    action = np.array(values, dtype=np.float64, copy=True, order="C")
    if action.ndim == 0:
        raise ValueError("values must have at least one axis")
    if not np.all(np.isfinite(action)):
        raise ValueError("values must be finite")
    references = _validate_references(axis_references, action.shape)

    components: dict[Subset, np.ndarray] = {}
    for subset in _subsets(action.ndim):
        component = np.array(
            _conditional_average(action, references, subset),
            dtype=np.float64,
            copy=True,
        )
        with np.errstate(over="ignore", invalid="ignore"):
            for proper_subset, proper_component in components.items():
                if set(proper_subset).issubset(subset):
                    component -= _broadcast_component(
                        proper_component, proper_subset, subset, action.shape
                    )
        if not np.all(np.isfinite(component)):
            raise ValueError("interaction components overflowed to nonfinite values")
        components[subset] = component

    reconstruction = np.zeros_like(action)
    full_subset = tuple(range(action.ndim))
    for subset, component in components.items():
        reconstruction += _broadcast_component(
            component, subset, full_subset, action.shape
        )
    reconstruction_residual_sup = float(np.max(np.abs(action - reconstruction)))
    return InteractionDecomposition(
        values=_readonly(action),
        axis_references=tuple(_readonly(reference) for reference in references),
        components=_readonly_mapping(components),
        reconstruction=_readonly(reconstruction),
        reconstruction_residual_sup=reconstruction_residual_sup,
    )


def _product_weights(references: tuple[np.ndarray, ...]) -> np.ndarray:
    result = np.array(1.0)
    for reference in references:
        result = np.multiply.outer(result, reference)
    return result


def retain_interaction_order(
    decomposition: InteractionDecomposition, maximum_order: int
) -> InteractionProjection:
    """Project to subset order and report coordinate, quotient, and L2 residuals."""
    if not isinstance(decomposition, InteractionDecomposition):
        raise TypeError("decomposition must be an InteractionDecomposition")
    if type(maximum_order) is not int:
        raise TypeError("maximum_order must be an int")
    axis_count = decomposition.values.ndim
    if maximum_order < 1 or maximum_order > axis_count:
        raise ValueError("maximum_order must be between one and the number of axes")

    retained = np.zeros_like(decomposition.values)
    omitted = np.zeros_like(decomposition.values)
    omitted_components: dict[Subset, np.ndarray] = {}
    full_subset = tuple(range(axis_count))
    for subset, component in decomposition.components.items():
        broadcast = _broadcast_component(
            component, subset, full_subset, decomposition.values.shape
        )
        if len(subset) <= maximum_order:
            retained += broadcast
        else:
            omitted += broadcast
            omitted_components[subset] = component

    theorem_coordinate_g_norm = float(
        sum(np.max(np.abs(component)) for component in omitted_components.values())
    )
    quotient_sup_norm = (
        0.5 * float(np.max(omitted)) - 0.5 * float(np.min(omitted))
        if omitted.size
        else 0.0
    )
    weights = _product_weights(decomposition.axis_references)
    residual_scale = float(np.max(np.abs(omitted))) if omitted.size else 0.0
    if residual_scale == 0.0:
        weighted_l2_diagnostic = 0.0
    else:
        scaled_residual = omitted / residual_scale
        weighted_l2_diagnostic = residual_scale * float(
            np.sqrt(np.sum(weights * scaled_residual * scaled_residual))
        )
    return InteractionProjection(
        maximum_order=maximum_order,
        retained_values=_readonly(retained),
        omitted_values=_readonly(omitted),
        omitted_components=_readonly_mapping(omitted_components),
        theorem_coordinate_g_norm=theorem_coordinate_g_norm,
        quotient_sup_norm=quotient_sup_norm,
        weighted_l2_diagnostic=weighted_l2_diagnostic,
    )
