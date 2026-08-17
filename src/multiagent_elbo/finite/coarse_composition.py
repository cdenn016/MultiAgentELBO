"""Transportable coarse-graining of the directed edge-event law.

The graph object that survives coarse-graining is the directed edge-event law on
ordered pairs, not the attention row. A coarse row is obtained by pushing that law
through a normalized kernel on ordered pairs and only then disintegrating, and
because the push is linear in the event law the normalization of the coarse object
is nothing more than the interchange of two finite sums. Linear aggregation is
therefore the unique rule compatible with an exact chain rule across scales, and
composing two coarse-grainings is composing two kernels.

The endpoint kernel is general. It is not required to factor into one membership
per endpoint, and the measurement built here deliberately does not factor: the
coarse label of the source is pulled toward the coarse label of the receiver, so
the two endpoint assignments are correlated. The product form is retained only as
a negative control, alongside the uniform row average, which is the aggregation
rule this module exists to refute.

Flattening ordered pairs into one alphabet lets ordinary finite kernel composition
carry the whole construction, so nothing here needs a bespoke composition law.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from multiagent_elbo.config import NumericsConfig
from multiagent_elbo.finite.attention import compose_kernels
from multiagent_elbo.finite.categorical_falsification_model import build_reference_model
from multiagent_elbo.finite.measures import MarkovKernel

DEFAULT_TOLERANCE = 1.0e-12

REFERENCE_PARENT_LABELS = ("A1", "A2", "A3")
REFERENCE_GRANDPARENT_LABELS = ("U1", "U2")

REFERENCE_SOFT_MEMBERSHIP = (
    (0.8, 0.1, 0.1),
    (0.8, 0.1, 0.1),
    (0.1, 0.8, 0.1),
    (0.1, 0.8, 0.1),
    (0.1, 0.1, 0.8),
    (0.1, 0.1, 0.8),
)
REFERENCE_PARENT_MEMBERSHIP = (
    (0.85, 0.15),
    (0.60, 0.40),
    (0.20, 0.80),
)
REFERENCE_HARD_MEMBERSHIP = (
    (1.0, 0.0, 0.0),
    (1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, 0.0, 1.0),
    (0.0, 0.0, 1.0),
)

REFERENCE_COPY_WEIGHT_FINE = 0.4
REFERENCE_COPY_WEIGHT_PARENT = 0.3

WITNESS_AGENT_LABELS = ("1", "2", "3")
WITNESS_BLOCK_LABELS = ("I", "J")
WITNESS_ALPHA = (0.9, 0.1, 0.0)
WITNESS_BETA = (
    (0.0, 0.0, 1.0),
    (1.0, 0.0, 0.0),
    (0.0, 0.0, 1.0),
)
WITNESS_MEMBERSHIP = (
    (1.0, 0.0),
    (1.0, 0.0),
    (0.0, 1.0),
)


def _labels(values: Sequence[str], name: str) -> tuple[str, ...]:
    """Coerce a sequence of distinct nonempty label strings to a tuple."""
    result = tuple(values)
    if not result:
        raise ValueError(f"{name} must be nonempty")
    for label in result:
        if type(label) is not str or not label:
            raise ValueError(f"{name} entries must be nonempty strings")
        if "|" in label:
            raise ValueError(f"{name} entries must not contain the pair separator")
    if len(set(result)) != len(result):
        raise ValueError(f"{name} must be unique")
    return result


def _matrix(values: object, name: str) -> np.ndarray:
    """Coerce a value to a finite nonnegative two-dimensional float64 array."""
    result = np.array(values, dtype=np.float64, copy=True, order="C")
    if result.ndim != 2:
        raise ValueError(f"{name} must be two dimensional")
    if not np.all(np.isfinite(result)) or np.any(result < 0.0):
        raise ValueError(f"{name} must be finite nonnegative")
    return result


def _readonly(values: object) -> np.ndarray:
    """Return an owned read-only float64 copy of an array."""
    result = np.array(values, dtype=np.float64, copy=True, order="C")
    result.setflags(write=False)
    return result


def _tolerance(value: float, name: str) -> float:
    """Validate a declared positive floating-point tolerance."""
    if type(value) is not float or not np.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be a positive finite float")
    return value


def _pair_alphabet(labels: tuple[str, ...]) -> tuple[str, ...]:
    """Return the flattened ordered-pair alphabet of one endpoint alphabet."""
    return tuple(f"{receiver}|{source}" for receiver in labels for source in labels)


def _membership_matrix(
    values: object,
    fine_labels: tuple[str, ...],
    coarse_labels: tuple[str, ...],
    tolerance: float,
) -> np.ndarray:
    """Coerce a value to a row-stochastic membership matrix matching its labels."""
    result = _matrix(values, "membership")
    if result.shape != (len(fine_labels), len(coarse_labels)):
        raise ValueError("membership shape must be fine labels by coarse labels")
    if not np.allclose(result.sum(axis=1), 1.0, rtol=0.0, atol=tolerance):
        raise ValueError("every membership row must sum to one")
    return result


@dataclass(frozen=True)
class PairEndpointKernel:
    """A normalized kernel from fine ordered pairs to coarse ordered pairs."""

    fine_labels: tuple[str, ...]
    coarse_labels: tuple[str, ...]
    matrix: np.ndarray
    tolerance: float = DEFAULT_TOLERANCE

    def __post_init__(self) -> None:
        fine = _labels(self.fine_labels, "fine_labels")
        coarse = _labels(self.coarse_labels, "coarse_labels")
        tolerance = _tolerance(self.tolerance, "tolerance")
        values = _matrix(self.matrix, "matrix")
        if values.shape != (len(fine) ** 2, len(coarse) ** 2):
            raise ValueError("matrix shape must be fine pairs by coarse pairs")
        if not np.allclose(values.sum(axis=1), 1.0, rtol=0.0, atol=tolerance):
            raise ValueError("every fine pair row must sum to one")
        object.__setattr__(self, "fine_labels", fine)
        object.__setattr__(self, "coarse_labels", coarse)
        object.__setattr__(self, "matrix", _readonly(values))

    @property
    def fine_pair_labels(self) -> tuple[str, ...]:
        """Return the flattened ordered-pair alphabet of the fine scale."""
        return _pair_alphabet(self.fine_labels)

    @property
    def coarse_pair_labels(self) -> tuple[str, ...]:
        """Return the flattened ordered-pair alphabet of the coarse scale."""
        return _pair_alphabet(self.coarse_labels)


def _blocks(kernel: PairEndpointKernel) -> np.ndarray:
    """Return one coarse receiver-by-source block per fine ordered pair."""
    size = len(kernel.coarse_labels)
    return kernel.matrix.reshape(kernel.matrix.shape[0], size, size)


def _markov_view(kernel: PairEndpointKernel, numerics: NumericsConfig) -> MarkovKernel:
    """Return the flattened pair-alphabet Markov kernel of an endpoint kernel."""
    return MarkovKernel(
        kernel.fine_pair_labels,
        kernel.coarse_pair_labels,
        kernel.matrix,
        numerics,
    )


def product_endpoint_kernel(
    membership: np.ndarray,
    fine_labels: Sequence[str],
    coarse_labels: Sequence[str],
    tolerance: float = DEFAULT_TOLERANCE,
) -> PairEndpointKernel:
    """Return the endpoint kernel that assigns each endpoint independently."""
    fine = _labels(fine_labels, "fine_labels")
    coarse = _labels(coarse_labels, "coarse_labels")
    tolerance = _tolerance(tolerance, "tolerance")
    values = _membership_matrix(membership, fine, coarse, tolerance)
    tensor = values[:, None, :, None] * values[None, :, None, :]
    return PairEndpointKernel(
        fine,
        coarse,
        tensor.reshape(len(fine) ** 2, len(coarse) ** 2),
        tolerance,
    )


def correlated_endpoint_kernel(
    membership: np.ndarray,
    fine_labels: Sequence[str],
    coarse_labels: Sequence[str],
    copy_weight: float,
    tolerance: float = DEFAULT_TOLERANCE,
) -> PairEndpointKernel:
    """Return an endpoint kernel whose source label is pulled toward the receiver label."""
    fine = _labels(fine_labels, "fine_labels")
    coarse = _labels(coarse_labels, "coarse_labels")
    tolerance = _tolerance(tolerance, "tolerance")
    if type(copy_weight) is not float or not 0.0 <= copy_weight <= 1.0:
        raise ValueError("copy_weight must be a float in the unit interval")
    values = _membership_matrix(membership, fine, coarse, tolerance)
    identity = np.eye(len(coarse), dtype=np.float64)
    source_given_receiver = (
        (1.0 - copy_weight) * values[None, :, :] + copy_weight * identity[:, None, :]
    )                                                          # (A, j, B)
    tensor = (
        values[:, None, :, None]
        * np.transpose(source_given_receiver, (1, 0, 2))[None, :, :, :]
    )                                                          # (i, j, A, B)
    return PairEndpointKernel(
        fine,
        coarse,
        tensor.reshape(len(fine) ** 2, len(coarse) ** 2),
        tolerance,
    )


def endpoint_marginal_product(kernel: PairEndpointKernel) -> PairEndpointKernel:
    """Return the kernel that replaces each fine pair by its own endpoint marginals."""
    if type(kernel) is not PairEndpointKernel:
        raise TypeError("kernel must be a PairEndpointKernel")
    blocks = _blocks(kernel)
    receiver = blocks.sum(axis=2)
    source = blocks.sum(axis=1)
    product = receiver[:, :, None] * source[:, None, :]
    return PairEndpointKernel(
        kernel.fine_labels,
        kernel.coarse_labels,
        product.reshape(product.shape[0], -1),
        kernel.tolerance,
    )


def is_product_form(
    kernel: PairEndpointKernel,
    tolerance: float = DEFAULT_TOLERANCE,
) -> bool:
    """Report whether an endpoint kernel equals the outer product of its own marginals."""
    if type(kernel) is not PairEndpointKernel:
        raise TypeError("kernel must be a PairEndpointKernel")
    tolerance = _tolerance(tolerance, "tolerance")
    factored = endpoint_marginal_product(kernel)
    return bool(
        np.allclose(kernel.matrix, factored.matrix, rtol=0.0, atol=tolerance)
    )


def push_event_law(eta: np.ndarray, kernel: PairEndpointKernel) -> np.ndarray:
    """Push a directed edge-event law forward through a normalized endpoint kernel."""
    if type(kernel) is not PairEndpointKernel:
        raise TypeError("kernel must be a PairEndpointKernel")
    values = _matrix(eta, "eta")
    size = len(kernel.fine_labels)
    if values.shape != (size, size):
        raise ValueError("eta shape must be fine labels by fine labels")
    coarse = len(kernel.coarse_labels)
    pushed = values.reshape(size * size) @ kernel.matrix
    return _readonly(pushed.reshape(coarse, coarse))


def disintegrate(eta_coarse: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Split an edge-event law into receiver occupancies and conditional source rows."""
    values = _matrix(eta_coarse, "eta_coarse")
    if values.shape[0] != values.shape[1]:
        raise ValueError("eta_coarse must be square")
    alpha = values.sum(axis=1)
    beta = np.zeros_like(values)
    np.divide(values, alpha[:, None], out=beta, where=(alpha > 0.0)[:, None])
    return _readonly(alpha), _readonly(beta)


def compose_endpoint_kernels(
    first: PairEndpointKernel,
    second: PairEndpointKernel,
) -> PairEndpointKernel:
    """Compose two endpoint kernels into the single kernel of the two-step push."""
    if type(first) is not PairEndpointKernel:
        raise TypeError("first must be a PairEndpointKernel")
    if type(second) is not PairEndpointKernel:
        raise TypeError("second must be a PairEndpointKernel")
    if first.coarse_labels != second.fine_labels:
        raise ValueError("first coarse labels must equal second fine labels")
    tolerance = max(first.tolerance, second.tolerance)
    numerics = NumericsConfig(dtype="float64", atol=tolerance, rtol=tolerance)
    composed = compose_kernels(
        _markov_view(first, numerics),
        _markov_view(second, numerics),
    )
    return PairEndpointKernel(
        first.fine_labels,
        second.coarse_labels,
        composed.matrix,
        tolerance,
    )


def naive_row_average(
    alpha: np.ndarray,
    beta: np.ndarray,
    membership: np.ndarray,
) -> np.ndarray:
    """Return the wrong uniform row average that discards occupancy, kept as a control."""
    occupancy = np.array(alpha, dtype=np.float64, copy=True, order="C")
    if occupancy.ndim != 1:
        raise ValueError("alpha must be one dimensional")
    if not np.all(np.isfinite(occupancy)) or np.any(occupancy < 0.0):
        raise ValueError("alpha must be finite nonnegative")
    rows = _matrix(beta, "beta")
    if rows.shape != (occupancy.shape[0], occupancy.shape[0]):
        raise ValueError("beta shape must be agents by agents")
    blocks = _matrix(membership, "membership")
    if blocks.shape[0] != occupancy.shape[0]:
        raise ValueError("membership rows must match the agent count")
    if not np.all((blocks == 0.0) | (blocks == 1.0)):
        raise ValueError("the row average control requires a hard membership")
    if not np.array_equal(blocks.sum(axis=1), np.ones(blocks.shape[0])):
        raise ValueError("every agent must belong to exactly one block")
    counts = blocks.sum(axis=0)
    if np.any(counts == 0.0):
        raise ValueError("every block must contain at least one agent")
    aggregated = rows @ blocks
    return _readonly((blocks.T @ aggregated) / counts[:, None])


@dataclass(frozen=True)
class RowAverageWitness:
    """The coarse row, the uniform row average, and the gap between them."""

    beta_coarse: float
    beta_naive: float
    discrepancy: float


@dataclass(frozen=True)
class CoarseCompositionCase:
    """The composition and control residuals of one channel and row configuration."""

    channel: str
    configuration: str
    composition_residual: float
    kernel_matrix_residual: float
    mass_residual: float
    product_form_discrepancy: float
    row_average_discrepancy: float


@dataclass(frozen=True)
class CoarseCompositionMeasurement:
    """The assembled coarse-edge composition measurement of the reference instance."""

    three_node_witness: RowAverageWitness
    cases: tuple[CoarseCompositionCase, ...]
    correlated_is_product_form: bool
    substituted_is_product_form: bool
    max_composition_residual: float
    max_kernel_matrix_residual: float
    max_mass_residual: float
    min_product_form_discrepancy: float
    max_row_average_discrepancy: float


def three_node_row_average_witness() -> RowAverageWitness:
    """Return the declared three-node witness separating the coarse row from its average."""
    alpha = np.array(WITNESS_ALPHA, dtype=np.float64)
    beta = np.array(WITNESS_BETA, dtype=np.float64)
    membership = np.array(WITNESS_MEMBERSHIP, dtype=np.float64)
    eta = alpha[:, None] * beta
    kernel = product_endpoint_kernel(
        membership, WITNESS_AGENT_LABELS, WITNESS_BLOCK_LABELS
    )
    _, beta_coarse = disintegrate(push_event_law(eta, kernel))
    beta_naive = naive_row_average(alpha, beta, membership)
    return RowAverageWitness(
        beta_coarse=float(beta_coarse[0, 1]),
        beta_naive=float(beta_naive[0, 1]),
        discrepancy=float(beta_coarse[0, 1] - beta_naive[0, 1]),
    )


def reference_endpoint_kernels() -> tuple[PairEndpointKernel, PairEndpointKernel]:
    """Return the declared correlated six-to-three and three-to-two endpoint kernels."""
    model = build_reference_model()
    agents = tuple(str(agent) for agent in model.agents)
    first = correlated_endpoint_kernel(
        np.array(REFERENCE_SOFT_MEMBERSHIP, dtype=np.float64),
        agents,
        REFERENCE_PARENT_LABELS,
        REFERENCE_COPY_WEIGHT_FINE,
    )
    second = correlated_endpoint_kernel(
        np.array(REFERENCE_PARENT_MEMBERSHIP, dtype=np.float64),
        REFERENCE_PARENT_LABELS,
        REFERENCE_GRANDPARENT_LABELS,
        REFERENCE_COPY_WEIGHT_PARENT,
    )
    return first, second


def run_coarse_composition_measurement() -> CoarseCompositionMeasurement:
    """Run the coarse-edge composition measurement on the declared reference instance."""
    model = build_reference_model()
    agents = tuple(str(agent) for agent in model.agents)
    first, second = reference_endpoint_kernels()
    composed = compose_endpoint_kernels(first, second)
    substituted = endpoint_marginal_product(first)
    hard_membership = np.array(REFERENCE_HARD_MEMBERSHIP, dtype=np.float64)
    hard = product_endpoint_kernel(hard_membership, agents, REFERENCE_PARENT_LABELS)
    kernel_matrix_residual = float(
        np.max(np.abs(composed.matrix - first.matrix @ second.matrix))
    )
    cases: list[CoarseCompositionCase] = []
    for channel in ("belief", "model"):
        for configuration in model.row_configurations:
            eta = model.edge_event_law(configuration, channel)
            parent = push_event_law(eta, first)
            staged = push_event_law(parent, second)
            direct = push_event_law(eta, composed)
            factored = push_event_law(eta, substituted)
            blocked = push_event_law(eta, hard)
            _, beta_coarse = disintegrate(blocked)
            alpha, beta = disintegrate(eta)
            beta_naive = naive_row_average(alpha, beta, hard_membership)
            cases.append(
                CoarseCompositionCase(
                    channel=channel,
                    configuration=configuration,
                    composition_residual=float(np.max(np.abs(staged - direct))),
                    kernel_matrix_residual=kernel_matrix_residual,
                    mass_residual=max(
                        abs(float(eta.sum()) - 1.0),
                        abs(float(parent.sum()) - 1.0),
                        abs(float(staged.sum()) - 1.0),
                        abs(float(direct.sum()) - 1.0),
                        abs(float(blocked.sum()) - 1.0),
                    ),
                    product_form_discrepancy=float(np.max(np.abs(parent - factored))),
                    row_average_discrepancy=float(
                        np.max(np.abs(beta_coarse - beta_naive))
                    ),
                )
            )
    return CoarseCompositionMeasurement(
        three_node_witness=three_node_row_average_witness(),
        cases=tuple(cases),
        correlated_is_product_form=is_product_form(first),
        substituted_is_product_form=is_product_form(substituted),
        max_composition_residual=max(case.composition_residual for case in cases),
        max_kernel_matrix_residual=kernel_matrix_residual,
        max_mass_residual=max(case.mass_residual for case in cases),
        min_product_form_discrepancy=min(
            case.product_form_discrepancy for case in cases
        ),
        max_row_average_discrepancy=max(
            case.row_average_discrepancy for case in cases
        ),
    )


__all__ = [
    "CoarseCompositionCase",
    "CoarseCompositionMeasurement",
    "PairEndpointKernel",
    "RowAverageWitness",
    "compose_endpoint_kernels",
    "correlated_endpoint_kernel",
    "disintegrate",
    "endpoint_marginal_product",
    "is_product_form",
    "naive_row_average",
    "product_endpoint_kernel",
    "push_event_law",
    "reference_endpoint_kernels",
    "run_coarse_composition_measurement",
    "three_node_row_average_witness",
]
