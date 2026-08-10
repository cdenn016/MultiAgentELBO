"""Finite graph-link transport, holonomy, and operational record primitives.

These graph links are declared interaction-complex data.  They are not
base-connection parallel transports without an additional curve assignment and
transport-identification hypothesis.  Frame changes below are passive
coordinate changes; covariance under them is not a dynamical symmetry.
Floating-point residual checks are implementation evidence, not proofs of the
finite mathematical criterion.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

import numpy as np


_ATOL = 1.0e-12
_RTOL = 1.0e-10


def _label(value: object, *, kind: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{kind} labels must be nonempty strings")
    return value


@dataclass(frozen=True)
class OrientedEdge:
    """One oriented copy ``source -> target`` and its reversal label."""

    label: str
    source: str
    target: str
    inverse: str


@dataclass(frozen=True)
class OrientedTwoCell:
    """A declared oriented 2-cell with its boundary in traversal order."""

    label: str
    boundary: tuple[str, ...]


def _validated_vertices(vertices: tuple[str, ...]) -> tuple[str, ...]:
    checked = tuple(_label(value, kind="vertex") for value in vertices)
    if not checked:
        raise ValueError("interaction complex must contain at least one vertex")
    if len(set(checked)) != len(checked):
        raise ValueError("vertex labels must be unique")
    return checked


def _validate_oriented_edge(
    edge: OrientedEdge,
    vertices: tuple[str, ...],
    edge_by_label: Mapping[str, OrientedEdge],
) -> None:
    if edge.source not in vertices or edge.target not in vertices:
        raise ValueError("edge endpoints must be declared vertices")
    _label(edge.inverse, kind="inverse edge")
    if edge.inverse == edge.label:
        raise ValueError("edge reversal must be fixed-point-free")
    if edge.inverse not in edge_by_label:
        raise ValueError("every edge reversal must be declared")
    inverse = edge_by_label[edge.inverse]
    if inverse.inverse != edge.label:
        raise ValueError("edge reversal must be an involution")
    if inverse.source != edge.target or inverse.target != edge.source:
        raise ValueError("reversed edge endpoints must be exchanged")


def _validated_edges(
    vertices: tuple[str, ...], edges: tuple[OrientedEdge, ...]
) -> tuple[tuple[OrientedEdge, ...], dict[str, OrientedEdge]]:
    checked = tuple(edges)
    labels = tuple(_label(edge.label, kind="edge") for edge in checked)
    if len(set(labels)) != len(labels):
        raise ValueError("edge labels must be unique")
    edge_by_label = {edge.label: edge for edge in checked}
    for edge in checked:
        _validate_oriented_edge(edge, vertices, edge_by_label)
    return checked, edge_by_label


def _validate_cell_boundary(
    boundary: tuple[str, ...], edge_by_label: Mapping[str, OrientedEdge]
) -> None:
    if not boundary:
        raise ValueError("2-cell boundary must be nonempty")
    try:
        boundary_edges = tuple(edge_by_label[label] for label in boundary)
    except KeyError as error:
        raise ValueError("2-cell boundary edges must be declared") from error
    for current, following in zip(
        boundary_edges, boundary_edges[1:] + boundary_edges[:1], strict=True
    ):
        if current.target != following.source:
            raise ValueError("2-cell boundary must be a closed oriented cycle")


def _validated_cells(
    two_cells: tuple[OrientedTwoCell, ...],
    edge_by_label: Mapping[str, OrientedEdge],
) -> tuple[OrientedTwoCell, ...]:
    raw_cells = tuple(two_cells)
    labels = tuple(_label(cell.label, kind="2-cell") for cell in raw_cells)
    if len(set(labels)) != len(labels):
        raise ValueError("2-cell labels must be unique")
    checked = []
    for cell in raw_cells:
        boundary = tuple(cell.boundary)
        _validate_cell_boundary(boundary, edge_by_label)
        checked.append(OrientedTwoCell(cell.label, boundary))
    return tuple(checked)


@dataclass(frozen=True, init=False)
class InteractionComplex:
    """A finite interaction multigraph with explicitly declared 2-cells."""

    vertices: tuple[str, ...]
    edges: tuple[OrientedEdge, ...]
    two_cells: tuple[OrientedTwoCell, ...]

    def __init__(
        self,
        vertices: tuple[str, ...],
        edges: tuple[OrientedEdge, ...],
        two_cells: tuple[OrientedTwoCell, ...],
    ) -> None:
        checked_vertices = _validated_vertices(vertices)
        checked_edges, edge_by_label = _validated_edges(checked_vertices, edges)
        checked_cells = _validated_cells(two_cells, edge_by_label)
        object.__setattr__(self, "vertices", checked_vertices)
        object.__setattr__(self, "edges", checked_edges)
        object.__setattr__(self, "two_cells", checked_cells)


def _readonly(values: object) -> np.ndarray:
    result = np.array(values, dtype=np.float64, copy=True)
    result.setflags(write=False)
    return result


def _gl_positive_2(values: object, *, name: str) -> np.ndarray:
    matrix = np.asarray(values, dtype=np.float64)
    if matrix.shape != (2, 2) or not np.all(np.isfinite(matrix)):
        raise ValueError(f"{name} must be a finite GL+(2) matrix")
    determinant = float(np.linalg.det(matrix))
    if not np.isfinite(determinant) or determinant <= 0.0:
        raise ValueError(f"{name} must be a finite GL+(2) matrix")
    return _readonly(matrix)


def _edge_map(complex_: InteractionComplex) -> dict[str, OrientedEdge]:
    if not isinstance(complex_, InteractionComplex):
        raise TypeError("complex_ must be an InteractionComplex")
    return {edge.label: edge for edge in complex_.edges}


@dataclass(frozen=True, init=False)
class OrientedLinks:
    """One validated ``GL+(2)`` link for every oriented edge copy."""

    complex: InteractionComplex
    matrices: Mapping[str, np.ndarray]

    def __init__(
        self, complex_: InteractionComplex, matrices: Mapping[str, object]
    ) -> None:
        edge_by_label = _edge_map(complex_)
        if not isinstance(matrices, Mapping):
            raise TypeError("matrices must be a mapping")
        if set(matrices) != set(edge_by_label):
            raise ValueError("links require exactly one matrix per oriented edge")
        checked = {
            label: _gl_positive_2(matrices[label], name=f"link {label!r}")
            for label in edge_by_label
        }
        for edge in complex_.edges:
            product = checked[edge.inverse] @ checked[edge.label]
            if not np.allclose(product, np.eye(2), atol=_ATOL, rtol=_RTOL):
                raise ValueError("reversed links must be inverse matrices")
        object.__setattr__(self, "complex", complex_)
        object.__setattr__(self, "matrices", MappingProxyType(checked))


@dataclass(frozen=True)
class PathTransport:
    """Endpoint-typed open-path transport; it is not an invariant scalar."""

    source: str
    target: str
    edge_labels: tuple[str, ...]
    matrix: np.ndarray


_CYCLE_FACTORY_TOKEN = object()


@dataclass(frozen=True, init=False)
class CycleHolonomy:
    """Factory-controlled ordered holonomy of a declared closed graph walk."""

    base_vertex: str
    edge_labels: tuple[str, ...]
    matrix: np.ndarray
    _complex: InteractionComplex = field(repr=False, compare=False)
    _factory_token: object = field(repr=False, compare=False)

    def __init__(self, *args: object, **kwargs: object) -> None:
        del args, kwargs
        raise TypeError("CycleHolonomy values require the cycle_holonomy factory")


@dataclass(frozen=True)
class ConjugacyInvariants:
    """Characteristic-polynomial invariants of a represented 2-cycle."""

    trace: float
    determinant: float
    discriminant: float


@dataclass(frozen=True)
class TrivializationResult:
    """Spanning-forest frames and the exact fundamental-cycle criterion."""

    is_trivializable: bool
    frames: Mapping[str, np.ndarray]
    fundamental_holonomies: tuple[CycleHolonomy, ...]
    max_edge_residual: float


@dataclass(frozen=True, init=False)
class OperationalRecordLaw:
    """A normalized marked-event law produced by declared measurements."""

    event_marks: tuple[str, ...]
    observation_vertex: str
    transported_state: np.ndarray
    logits: np.ndarray
    probabilities: np.ndarray

    def __init__(
        self,
        event_marks: tuple[str, ...],
        observation_vertex: str,
        transported_state: object,
        logits: object,
        probabilities: object,
    ) -> None:
        marks = tuple(_label(mark, kind="event mark") for mark in event_marks)
        if not marks or len(set(marks)) != len(marks):
            raise ValueError("event marks must be nonempty and unique")
        _label(observation_vertex, kind="observation vertex")
        state = np.asarray(transported_state, dtype=np.float64)
        checked_logits = np.asarray(logits, dtype=np.float64)
        checked_probabilities = np.asarray(probabilities, dtype=np.float64)
        if state.shape != (2,) or not np.all(np.isfinite(state)):
            raise ValueError("transported state must be a finite two-vector")
        if checked_logits.shape != (len(marks),) or not np.all(
            np.isfinite(checked_logits)
        ):
            raise ValueError("logits must be finite with one entry per event mark")
        if checked_probabilities.shape != (len(marks),) or not np.all(
            np.isfinite(checked_probabilities)
        ):
            raise ValueError(
                "probabilities must be finite with one entry per event mark"
            )
        if np.any(checked_probabilities < 0.0) or not np.isclose(
            np.sum(checked_probabilities), 1.0, atol=_ATOL, rtol=_RTOL
        ):
            raise ValueError("operational record law must be normalized")
        object.__setattr__(self, "event_marks", marks)
        object.__setattr__(self, "observation_vertex", observation_vertex)
        object.__setattr__(self, "transported_state", _readonly(state))
        object.__setattr__(self, "logits", _readonly(checked_logits))
        object.__setattr__(self, "probabilities", _readonly(checked_probabilities))


@dataclass(frozen=True)
class LinkOnlyHolonomyDiagnostic:
    """A link-only diagnostic that cannot establish an operational effect."""

    holonomy: CycleHolonomy
    invariants: ConjugacyInvariants
    supports_operational_claim: bool = False
    operational_conclusion: None = None
    limitation: str = (
        "graph-link holonomy alone is insufficient for an "
        "operational-holonomy conclusion"
    )


def invert_link(matrix: object) -> np.ndarray:
    """Validate and invert one represented graph link."""
    checked = _gl_positive_2(matrix, name="link")
    return _readonly(np.linalg.inv(checked))


def _require_matching_links(
    complex_: InteractionComplex, links: OrientedLinks
) -> dict[str, OrientedEdge]:
    edge_by_label = _edge_map(complex_)
    if not isinstance(links, OrientedLinks) or links.complex != complex_:
        raise ValueError("links must belong to the supplied interaction complex")
    return edge_by_label


def open_path_transport(
    complex_: InteractionComplex,
    links: OrientedLinks,
    edge_labels: tuple[str, ...],
) -> PathTransport:
    """Compose a nonempty path in traversal order, with the last link leftmost."""
    edge_by_label = _require_matching_links(complex_, links)
    labels = tuple(edge_labels)
    if not labels:
        raise ValueError("open path must contain at least one oriented edge")
    try:
        edges = tuple(edge_by_label[label] for label in labels)
    except KeyError as error:
        raise ValueError("path edges must be declared") from error
    for current, following in zip(edges, edges[1:]):
        if current.target != following.source:
            raise ValueError("path edges must form an endpoint-compatible walk")
    matrix = np.eye(2)
    for label in labels:
        matrix = links.matrices[label] @ matrix
    return PathTransport(
        source=edges[0].source,
        target=edges[-1].target,
        edge_labels=labels,
        matrix=_readonly(matrix),
    )


def cycle_holonomy(
    complex_: InteractionComplex,
    links: OrientedLinks,
    edge_labels: tuple[str, ...],
) -> CycleHolonomy:
    """Return ordered holonomy only after checking that the walk closes."""
    transport = open_path_transport(complex_, links, edge_labels)
    if transport.source != transport.target:
        raise ValueError("cycle holonomy requires a closed oriented walk")
    return _make_cycle_holonomy(
        complex_, transport.source, transport.edge_labels, transport.matrix
    )


def _make_cycle_holonomy(
    complex_: InteractionComplex,
    base_vertex: str,
    edge_labels: tuple[str, ...],
    matrix: object,
) -> CycleHolonomy:
    """Construct a cycle value after independently rechecking its public data."""
    edge_by_label = _edge_map(complex_)
    labels = tuple(edge_labels)
    if not labels:
        raise ValueError("cycle holonomy requires a nonempty declared walk")
    try:
        edges = tuple(edge_by_label[label] for label in labels)
    except KeyError as error:
        raise ValueError("cycle holonomy edges must be declared") from error
    if base_vertex != edges[0].source:
        raise ValueError("cycle base vertex must equal the walk source")
    for current, following in zip(edges, edges[1:]):
        if current.target != following.source:
            raise ValueError("cycle edges must form an endpoint-compatible walk")
    if edges[-1].target != base_vertex:
        raise ValueError("cycle holonomy requires a closed oriented walk")
    checked_matrix = _gl_positive_2(matrix, name="cycle holonomy")
    result = object.__new__(CycleHolonomy)
    object.__setattr__(result, "base_vertex", base_vertex)
    object.__setattr__(result, "edge_labels", labels)
    object.__setattr__(result, "matrix", checked_matrix)
    object.__setattr__(result, "_complex", complex_)
    object.__setattr__(result, "_factory_token", _CYCLE_FACTORY_TOKEN)
    return result


def _validated_cycle_holonomy(cycle: object) -> CycleHolonomy:
    if not isinstance(cycle, CycleHolonomy) or (
        getattr(cycle, "_factory_token", None) is not _CYCLE_FACTORY_TOKEN
    ):
        raise TypeError(
            "conjugacy invariants require a closed CycleHolonomy from the factory"
        )
    return _make_cycle_holonomy(
        cycle._complex, cycle.base_vertex, cycle.edge_labels, cycle.matrix
    )


def conjugacy_invariants(cycle: CycleHolonomy) -> ConjugacyInvariants:
    """Return trace, determinant, and discriminant for a closed holonomy."""
    checked_cycle = _validated_cycle_holonomy(cycle)
    trace = float(np.trace(checked_cycle.matrix))
    determinant = float(np.linalg.det(checked_cycle.matrix))
    return ConjugacyInvariants(
        trace=trace,
        determinant=determinant,
        discriminant=trace * trace - 4.0 * determinant,
    )


def _unoriented_edges(complex_: InteractionComplex) -> tuple[OrientedEdge, ...]:
    seen: set[str] = set()
    representatives: list[OrientedEdge] = []
    for edge in complex_.edges:
        if edge.label in seen:
            continue
        representatives.append(edge)
        seen.update((edge.label, edge.inverse))
    return tuple(representatives)


def _graph_has_cycle(complex_: InteractionComplex) -> bool:
    representatives = _unoriented_edges(complex_)
    parent = {vertex: vertex for vertex in complex_.vertices}

    def find(vertex: str) -> str:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in representatives:
        source_root = find(edge.source)
        target_root = find(edge.target)
        if source_root == target_root:
            return True
        parent[target_root] = source_root
    return False


def plaquette_curvature(
    complex_: InteractionComplex, links: OrientedLinks, cell_label: str
) -> np.ndarray:
    """Return ``H(boundary)-I`` for one declared oriented 2-cell."""
    _require_matching_links(complex_, links)
    if not _graph_has_cycle(complex_):
        raise ValueError("a tree has no plaquette curvature")
    cell_by_label = {cell.label: cell for cell in complex_.two_cells}
    if cell_label not in cell_by_label:
        raise ValueError("plaquette curvature requires a declared 2-cell")
    holonomy = cycle_holonomy(complex_, links, cell_by_label[cell_label].boundary)
    return _readonly(holonomy.matrix - np.eye(2))


def _spanning_adjacency(
    complex_: InteractionComplex, representatives: tuple[OrientedEdge, ...]
) -> dict[str, list[tuple[str, str, frozenset[str]]]]:
    adjacency: dict[str, list[tuple[str, str, frozenset[str]]]] = {
        vertex: [] for vertex in complex_.vertices
    }
    for edge in representatives:
        pair = frozenset((edge.label, edge.inverse))
        adjacency[edge.source].append((edge.target, edge.label, pair))
        adjacency[edge.target].append((edge.source, edge.inverse, pair))
    return adjacency


def _spanning_forest_frames(
    complex_: InteractionComplex,
    links: OrientedLinks,
    adjacency: Mapping[str, list[tuple[str, str, frozenset[str]]]],
) -> tuple[dict[str, np.ndarray], set[frozenset[str]]]:
    frames: dict[str, np.ndarray] = {}
    tree_pairs: set[frozenset[str]] = set()
    for root in complex_.vertices:
        if root in frames:
            continue
        frames[root] = _readonly(np.eye(2))
        queue = [root]
        while queue:
            current = queue.pop(0)
            for neighbor, label, pair in adjacency[current]:
                if neighbor in frames:
                    continue
                frames[neighbor] = _readonly(links.matrices[label] @ frames[current])
                tree_pairs.add(pair)
                queue.append(neighbor)
    return frames, tree_pairs


def _spanning_tree_path(
    start: str,
    target: str,
    adjacency: Mapping[str, list[tuple[str, str, frozenset[str]]]],
    tree_pairs: set[frozenset[str]],
) -> tuple[str, ...]:
    previous: dict[str, tuple[str | None, str | None]] = {start: (None, None)}
    queue = [start]
    while queue and target not in previous:
        current = queue.pop(0)
        for neighbor, label, pair in adjacency[current]:
            if pair not in tree_pairs or neighbor in previous:
                continue
            previous[neighbor] = (current, label)
            queue.append(neighbor)
    if target not in previous:
        raise RuntimeError("spanning-tree path construction failed")
    reverse_labels: list[str] = []
    current = target
    while previous[current][0] is not None:
        predecessor, label = previous[current]
        if predecessor is None or label is None:
            raise RuntimeError("spanning-tree predecessor is incomplete")
        reverse_labels.append(label)
        current = predecessor
    return tuple(reversed(reverse_labels))


def _fundamental_holonomies(
    complex_: InteractionComplex,
    links: OrientedLinks,
    representatives: tuple[OrientedEdge, ...],
    adjacency: Mapping[str, list[tuple[str, str, frozenset[str]]]],
    tree_pairs: set[frozenset[str]],
) -> tuple[CycleHolonomy, ...]:
    fundamentals = []
    for edge in representatives:
        pair = frozenset((edge.label, edge.inverse))
        if pair in tree_pairs:
            continue
        cycle_labels = (
            edge.label,
            *_spanning_tree_path(edge.target, edge.source, adjacency, tree_pairs),
        )
        fundamentals.append(cycle_holonomy(complex_, links, cycle_labels))
    return tuple(fundamentals)


def _max_coboundary_residual(
    complex_: InteractionComplex,
    links: OrientedLinks,
    frames: Mapping[str, np.ndarray],
) -> float:
    residuals = []
    for edge in complex_.edges:
        expected = frames[edge.target] @ np.linalg.inv(frames[edge.source])
        residuals.append(float(np.max(np.abs(links.matrices[edge.label] - expected))))
    return max(residuals, default=0.0)


def trivialization_via_spanning_tree(
    complex_: InteractionComplex, links: OrientedLinks
) -> TrivializationResult:
    """Construct tree frames and check every fundamental cycle/coboundary edge."""
    _require_matching_links(complex_, links)
    representatives = _unoriented_edges(complex_)
    adjacency = _spanning_adjacency(complex_, representatives)
    frames, tree_pairs = _spanning_forest_frames(complex_, links, adjacency)
    fundamentals = _fundamental_holonomies(
        complex_, links, representatives, adjacency, tree_pairs
    )
    max_residual = _max_coboundary_residual(complex_, links, frames)
    is_trivializable = all(
        np.allclose(cycle.matrix, np.eye(2), atol=_ATOL, rtol=_RTOL)
        for cycle in fundamentals
    )
    return TrivializationResult(
        is_trivializable=is_trivializable,
        frames=MappingProxyType(frames),
        fundamental_holonomies=fundamentals,
        max_edge_residual=max_residual,
    )


def _validated_frames(
    complex_: InteractionComplex, frames: Mapping[str, object]
) -> dict[str, np.ndarray]:
    _edge_map(complex_)
    if not isinstance(frames, Mapping) or set(frames) != set(complex_.vertices):
        raise ValueError("frames require exactly one GL+(2) matrix per vertex")
    return {
        vertex: _gl_positive_2(frames[vertex], name=f"frame {vertex!r}")
        for vertex in complex_.vertices
    }


def passive_transform_links(
    complex_: InteractionComplex,
    links: OrientedLinks,
    frames: Mapping[str, object],
) -> OrientedLinks:
    """Apply ``Theta'_e=A_target^-1 Theta_e A_source`` passively."""
    edge_by_label = _require_matching_links(complex_, links)
    checked_frames = _validated_frames(complex_, frames)
    transformed = {}
    for label, edge in edge_by_label.items():
        transformed[label] = (
            np.linalg.inv(checked_frames[edge.target])
            @ links.matrices[label]
            @ checked_frames[edge.source]
        )
    return OrientedLinks(complex_, transformed)


def passive_transform_states(
    complex_: InteractionComplex,
    states: Mapping[str, object],
    frames: Mapping[str, object],
) -> Mapping[str, np.ndarray]:
    """Apply the matching passive vector law ``z'_i=A_i^-1 z_i``."""
    checked_frames = _validated_frames(complex_, frames)
    if not isinstance(states, Mapping) or set(states) != set(complex_.vertices):
        raise ValueError("states require exactly one two-vector per vertex")
    transformed = {}
    for vertex in complex_.vertices:
        state = np.asarray(states[vertex], dtype=np.float64)
        if state.shape != (2,) or not np.all(np.isfinite(state)):
            raise ValueError("states must be finite two-vectors")
        transformed[vertex] = _readonly(np.linalg.solve(checked_frames[vertex], state))
    return MappingProxyType(transformed)


def passive_transform_covectors(
    complex_: InteractionComplex,
    covectors: object,
    observation_vertex: str,
    frames: Mapping[str, object],
) -> np.ndarray:
    """Apply the dual passive law ``c'=A_observation^T c``."""
    checked_frames = _validated_frames(complex_, frames)
    if observation_vertex not in complex_.vertices:
        raise ValueError("observation vertex must be declared")
    checked = np.asarray(covectors, dtype=np.float64)
    if checked.ndim != 2 or checked.shape[1:] != (2,) or checked.shape[0] < 1:
        raise ValueError("mark covectors must have shape (M, 2)")
    if not np.all(np.isfinite(checked)):
        raise ValueError("mark covectors must be finite")
    return _readonly(checked @ checked_frames[observation_vertex])


def _transported_state_sum(
    complex_: InteractionComplex,
    links: OrientedLinks,
    states: Mapping[str, object],
    observation_vertex: str,
    source_paths: Mapping[str, tuple[str, ...]],
) -> np.ndarray:
    total = np.zeros(2)
    for source, raw_state in states.items():
        if source not in complex_.vertices:
            raise ValueError("state sources must be declared vertices")
        state = np.asarray(raw_state, dtype=np.float64)
        if state.shape != (2,) or not np.all(np.isfinite(state)):
            raise ValueError("states must be finite two-vectors")
        path = tuple(source_paths[source])
        if not path:
            if source != observation_vertex:
                raise ValueError(
                    "an empty source path must start at the observation vertex"
                )
            total += state
            continue
        transport = open_path_transport(complex_, links, path)
        if transport.source != source or transport.target != observation_vertex:
            raise ValueError("each source path must end at the observation vertex")
        total += transport.matrix @ state
    return total


def _record_logits_and_probabilities(
    total: np.ndarray, marks: tuple[str, ...], mark_covectors: object
) -> tuple[np.ndarray, np.ndarray]:
    covectors = np.asarray(mark_covectors, dtype=np.float64)
    if covectors.shape != (len(marks), 2) or not np.all(np.isfinite(covectors)):
        raise ValueError("mark covectors must be finite with shape (M, 2)")
    logits = covectors @ total
    shifted = logits - np.max(logits)
    weights = np.exp(shifted)
    return logits, weights / np.sum(weights)


def operational_record_law(
    complex_: InteractionComplex,
    links: OrientedLinks,
    states: Mapping[str, object],
    observation_vertex: str,
    source_paths: Mapping[str, tuple[str, ...]],
    event_marks: tuple[str, ...],
    mark_covectors: object,
) -> OperationalRecordLaw:
    """Transport declared states, measure them, and normalize over event marks."""
    _require_matching_links(complex_, links)
    if observation_vertex not in complex_.vertices:
        raise ValueError("observation vertex must be declared")
    if not isinstance(states, Mapping) or not isinstance(source_paths, Mapping):
        raise TypeError("states and source_paths must be mappings")
    if set(states) != set(source_paths) or not states:
        raise ValueError("states and source_paths must have the same nonempty sources")
    total = _transported_state_sum(
        complex_, links, states, observation_vertex, source_paths
    )
    marks = tuple(event_marks)
    logits, probabilities = _record_logits_and_probabilities(
        total, marks, mark_covectors
    )
    return OperationalRecordLaw(marks, observation_vertex, total, logits, probabilities)


def operational_observable(
    law: OperationalRecordLaw, mark_values: Mapping[str, float]
) -> float:
    """Return one scalar expectation under a validated normalized record law."""
    if not isinstance(law, OperationalRecordLaw):
        raise TypeError(
            "operational observable requires a normalized OperationalRecordLaw"
        )
    if not isinstance(mark_values, Mapping) or set(mark_values) != set(law.event_marks):
        raise ValueError("mark values require exactly one value per event mark")
    values = np.array([mark_values[mark] for mark in law.event_marks], dtype=np.float64)
    if not np.all(np.isfinite(values)):
        raise ValueError("mark values must be finite")
    return float(law.probabilities @ values)


def link_only_diagnostic(cycle: CycleHolonomy) -> LinkOnlyHolonomyDiagnostic:
    """Describe link holonomy while explicitly withholding an operational claim."""
    checked_cycle = _validated_cycle_holonomy(cycle)
    return LinkOnlyHolonomyDiagnostic(
        checked_cycle, conjugacy_invariants(checked_cycle)
    )
