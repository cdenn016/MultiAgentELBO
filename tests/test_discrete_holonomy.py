from __future__ import annotations

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
import pytest

from multiagent_elbo.geometry import discrete_holonomy as hol


def _edge_pair(
    forward: str, source: str, target: str, reverse: str
) -> tuple[hol.OrientedEdge, hol.OrientedEdge]:
    return (
        hol.OrientedEdge(forward, source, target, reverse),
        hol.OrientedEdge(reverse, target, source, forward),
    )


def _tree_complex() -> hol.InteractionComplex:
    return hol.InteractionComplex(
        vertices=("a", "b", "c"),
        edges=(
            *_edge_pair("ab", "a", "b", "ba"),
            *_edge_pair("bc", "b", "c", "cb"),
        ),
        two_cells=(),
    )


def _tree_links() -> hol.OrientedLinks:
    ab = np.array([[1.0, 1.0], [0.0, 1.0]])
    bc = np.array([[1.0, 0.0], [1.0, 1.0]])
    return hol.OrientedLinks(
        _tree_complex(),
        {
            "ab": ab,
            "ba": np.array([[1.0, -1.0], [0.0, 1.0]]),
            "bc": bc,
            "cb": np.array([[1.0, 0.0], [-1.0, 1.0]]),
        },
    )


def _flat_cycle() -> tuple[hol.InteractionComplex, hol.OrientedLinks]:
    complex_ = hol.InteractionComplex(
        vertices=("a", "b", "c"),
        edges=(
            *_edge_pair("ab", "a", "b", "ba"),
            *_edge_pair("bc", "b", "c", "cb"),
            *_edge_pair("ca", "c", "a", "ac"),
        ),
        two_cells=(hol.OrientedTwoCell("abc", ("ab", "bc", "ca")),),
    )
    links = hol.OrientedLinks(
        complex_,
        {
            "ab": [[1.0, 1.0], [0.0, 1.0]],
            "ba": [[1.0, -1.0], [0.0, 1.0]],
            "bc": [[1.0, 0.0], [1.0, 1.0]],
            "cb": [[1.0, 0.0], [-1.0, 1.0]],
            "ca": [[2.0, -1.0], [-1.0, 1.0]],
            "ac": [[1.0, 1.0], [1.0, 2.0]],
        },
    )
    return complex_, links


def _nonflat_plaquette() -> tuple[hol.InteractionComplex, hol.OrientedLinks]:
    complex_ = hol.InteractionComplex(
        vertices=("0", "1", "2", "3"),
        edges=(
            *_edge_pair("e01", "0", "1", "e10"),
            *_edge_pair("e12", "1", "2", "e21"),
            *_edge_pair("e23", "2", "3", "e32"),
            *_edge_pair("e30", "3", "0", "e03"),
        ),
        two_cells=(
            hol.OrientedTwoCell("square", ("e01", "e12", "e23", "e30")),
        ),
    )
    links = hol.OrientedLinks(
        complex_,
        {
            "e01": np.eye(2),
            "e10": np.eye(2),
            "e12": [[1.0, 1.0], [0.0, 1.0]],
            "e21": [[1.0, -1.0], [0.0, 1.0]],
            "e23": np.eye(2),
            "e32": np.eye(2),
            "e30": [[2.0, 0.0], [0.0, 1.0]],
            "e03": [[0.5, 0.0], [0.0, 1.0]],
        },
    )
    return complex_, links


def test_interaction_complex_rejects_a_reversal_that_is_not_fixed_point_free():
    """Mutation caught: accepting an oriented edge as its own inverse."""
    try:
        from multiagent_elbo.geometry import discrete_holonomy as hol
    except ModuleNotFoundError:
        pytest.fail("the discrete holonomy API is missing")

    with pytest.raises(ValueError, match="fixed-point-free"):
        hol.InteractionComplex(
            vertices=("a", "b"),
            edges=(hol.OrientedEdge("ab", "a", "b", "ab"),),
            two_cells=(),
        )


def test_interaction_complex_defensively_copies_two_cell_boundaries():
    """Mutation caught: retaining a caller-owned mutable boundary list."""
    boundary = ["ab", "bc", "ca"]
    complex_ = hol.InteractionComplex(
        vertices=("a", "b", "c"),
        edges=(
            *_edge_pair("ab", "a", "b", "ba"),
            *_edge_pair("bc", "b", "c", "cb"),
            *_edge_pair("ca", "c", "a", "ac"),
        ),
        two_cells=(hol.OrientedTwoCell("abc", boundary),),
    )

    boundary[:] = ["ab"]

    assert complex_.two_cells[0].boundary == ("ab", "bc", "ca")
    assert isinstance(complex_.two_cells[0].boundary, tuple)


@pytest.mark.parametrize(
    ("complex_", "message"),
    [
        (
            lambda: hol.InteractionComplex(
                ("a",),
                (hol.OrientedEdge("ab", "a", "missing", "ba"),),
                (),
            ),
            "endpoints",
        ),
        (
            lambda: hol.InteractionComplex(
                ("a", "b"),
                (hol.OrientedEdge("ab", "a", "b", "ba"),),
                (),
            ),
            "reversal must be declared",
        ),
        (
            lambda: hol.InteractionComplex(
                ("a", "b", "c"),
                (*_edge_pair("ab", "a", "b", "ba"),),
                (hol.OrientedTwoCell("broken", ("ab", "ba", "ab")),),
            ),
            "closed oriented cycle",
        ),
    ],
)
def test_interaction_complex_rejects_bad_endpoints_reversals_and_cell_closure(
    complex_, message: str
):
    """Mutation caught: computing on malformed declared combinatorial data."""
    with pytest.raises(ValueError, match=message):
        complex_()


def test_link_inversion_and_open_path_transport_match_literal_order():
    """Mutation caught: composing traversal-ordered links left-to-right."""
    complex_ = _tree_complex()
    links = _tree_links()

    inverse = hol.invert_link([[1.0, 2.0], [0.0, 1.0]])
    transport = hol.open_path_transport(complex_, links, ("ab", "bc"))

    assert_array_equal(inverse, [[1.0, -2.0], [0.0, 1.0]])
    assert transport.source == "a"
    assert transport.target == "c"
    assert transport.edge_labels == ("ab", "bc")
    assert_array_equal(transport.matrix, [[1.0, 1.0], [1.0, 2.0]])
    assert not inverse.flags.writeable
    assert not transport.matrix.flags.writeable


def test_open_path_transport_is_not_accepted_as_a_conjugacy_invariant_scalar():
    """Mutation caught: treating endpoint-typed open transport as gauge invariant."""
    transport = hol.open_path_transport(_tree_complex(), _tree_links(), ("ab",))

    with pytest.raises(TypeError, match="closed CycleHolonomy"):
        hol.conjugacy_invariants(transport)


def test_open_path_cannot_be_rewrapped_as_a_cycle_holonomy():
    """Mutation caught: exposing a constructor that blesses open transport."""
    transport = hol.open_path_transport(_tree_complex(), _tree_links(), ("ab",))

    with pytest.raises(TypeError, match="cycle_holonomy factory"):
        hol.CycleHolonomy(
            base_vertex=transport.source,
            edge_labels=transport.edge_labels,
            matrix=transport.matrix,
        )


@pytest.mark.parametrize(
    ("base_vertex", "edge_labels", "matrix"),
    [
        ("a", ("ab", "ba"), np.eye(3)),
        ("a", ("ab", "ba"), [[1.0, np.nan], [0.0, 1.0]]),
        ("ghost", ("undeclared",), np.eye(2)),
    ],
)
def test_cycle_constructor_rejects_wrong_shape_nonfinite_and_undeclared_cycles(
    base_vertex: str, edge_labels: tuple[str, ...], matrix: np.ndarray
):
    """Mutation caught: accepting an unvalidated public cycle value."""
    with pytest.raises(TypeError, match="cycle_holonomy factory"):
        hol.CycleHolonomy(base_vertex, edge_labels, matrix)


def test_flat_cycle_has_literal_identity_holonomy_and_conjugacy_invariants():
    """Mutation caught: reversing the ordered cycle product."""
    complex_, links = _flat_cycle()

    cycle = hol.cycle_holonomy(complex_, links, ("ab", "bc", "ca"))
    invariants = hol.conjugacy_invariants(cycle)

    assert cycle.base_vertex == "a"
    assert_array_equal(cycle.matrix, np.eye(2))
    assert invariants.trace == pytest.approx(2.0)
    assert invariants.determinant == pytest.approx(1.0)
    assert invariants.discriminant == pytest.approx(0.0)


def test_nonflat_declared_plaquette_has_literal_holonomy_and_curvature():
    """Mutation caught: dropping one boundary link from plaquette curvature."""
    complex_, links = _nonflat_plaquette()

    cycle = hol.cycle_holonomy(
        complex_, links, ("e01", "e12", "e23", "e30")
    )
    curvature = hol.plaquette_curvature(complex_, links, "square")

    assert_array_equal(cycle.matrix, [[2.0, 2.0], [0.0, 1.0]])
    assert_array_equal(curvature, [[1.0, 2.0], [0.0, 0.0]])


def test_tree_rejects_a_plaquette_curvature_request():
    """Mutation caught: manufacturing curvature without a declared 2-cell."""
    with pytest.raises(ValueError, match="tree has no plaquette curvature"):
        hol.plaquette_curvature(_tree_complex(), _tree_links(), "invented")


def test_spanning_tree_criterion_pins_flat_tree_flat_cycle_and_nonflat_cycle():
    """Mutation caught: checking only spanning-tree edges and missing chords."""
    tree_result = hol.trivialization_via_spanning_tree(_tree_complex(), _tree_links())
    cycle_complex, cycle_links = _flat_cycle()
    cycle_result = hol.trivialization_via_spanning_tree(cycle_complex, cycle_links)
    square_complex, square_links = _nonflat_plaquette()
    square_result = hol.trivialization_via_spanning_tree(square_complex, square_links)

    assert tree_result.is_trivializable
    assert_array_equal(tree_result.frames["a"], np.eye(2))
    assert_array_equal(tree_result.frames["b"], [[1.0, 1.0], [0.0, 1.0]])
    assert_array_equal(tree_result.frames["c"], [[1.0, 1.0], [1.0, 2.0]])
    assert tree_result.fundamental_holonomies == ()
    assert cycle_result.is_trivializable
    assert len(cycle_result.fundamental_holonomies) == 1
    assert_array_equal(cycle_result.fundamental_holonomies[0].matrix, np.eye(2))
    assert not square_result.is_trivializable
    assert square_result.max_edge_residual == pytest.approx(1.0)


def test_oriented_links_reject_an_omitted_inverse_and_invalid_gl_positive_matrix():
    """Mutation caught: inferring a missing reverse copy or accepting det <= 0."""
    complex_ = hol.InteractionComplex(
        ("a", "b"), (*_edge_pair("ab", "a", "b", "ba"),), ()
    )

    with pytest.raises(ValueError, match="exactly one matrix per oriented edge"):
        hol.OrientedLinks(complex_, {"ab": np.eye(2)})
    with pytest.raises(ValueError, match=r"GL\+\(2\)"):
        hol.OrientedLinks(
            complex_,
            {"ab": [[-1.0, 0.0], [0.0, 1.0]], "ba": [[-1.0, 0.0], [0.0, 1.0]]},
        )
    with pytest.raises(ValueError, match="inverse matrices"):
        hol.OrientedLinks(complex_, {"ab": np.eye(2), "ba": [[2.0, 0.0], [0.0, 1.0]]})


def _operational_fixture() -> tuple[hol.InteractionComplex, hol.OrientedLinks]:
    complex_ = hol.InteractionComplex(
        ("a", "b"), (*_edge_pair("ab", "a", "b", "ba"),), ()
    )
    return complex_, hol.OrientedLinks(
        complex_, {"ab": np.eye(2), "ba": np.eye(2)}
    )


def test_passive_frame_change_conjugates_cycle_and_preserves_only_invariants():
    """Mutation caught: applying the source and target frame factors backward."""
    complex_, links = _nonflat_plaquette()
    frames = {
        "0": [[2.0, 0.0], [0.0, 1.0]],
        "1": [[1.0, 1.0], [0.0, 1.0]],
        "2": [[1.0, 0.0], [1.0, 1.0]],
        "3": [[3.0, 0.0], [0.0, 1.0]],
    }
    baseline = hol.cycle_holonomy(
        complex_, links, ("e01", "e12", "e23", "e30")
    )

    transformed_links = hol.passive_transform_links(complex_, links, frames)
    transformed = hol.cycle_holonomy(
        complex_, transformed_links, ("e01", "e12", "e23", "e30")
    )

    assert_array_equal(transformed.matrix, [[2.0, 1.0], [0.0, 1.0]])
    assert hol.conjugacy_invariants(transformed) == hol.conjugacy_invariants(baseline)


def test_normalized_operational_law_matches_literal_probabilities_and_observable():
    """Mutation caught: emitting unnormalized exponential mark weights."""
    complex_, links = _operational_fixture()

    law = hol.operational_record_law(
        complex_,
        links,
        states={"a": [1.0, 0.0], "b": [1.0, 1.0]},
        observation_vertex="a",
        source_paths={"a": (), "b": ("ba",)},
        event_marks=("quiet", "signal"),
        mark_covectors=[[0.0, 0.0], [1.0, 0.0]],
    )

    assert_array_equal(law.transported_state, [2.0, 1.0])
    assert_array_equal(law.logits, [0.0, 2.0])
    assert_allclose(
        law.probabilities,
        [0.11920292202211755, 0.8807970779778823],
        atol=1e-15,
        rtol=0.0,
    )
    assert law.probabilities.sum() == pytest.approx(1.0)
    observable = hol.operational_observable(
        law, {"quiet": -1.0, "signal": 2.0}
    )
    assert observable == pytest.approx(
        (-1.0 + 2.0 * np.exp(2.0)) / (1.0 + np.exp(2.0))
    )


def test_coherent_passive_transform_preserves_law_but_broken_link_does_not():
    """Mutation caught: calling link covariance alone operationally sufficient."""
    complex_, links = _operational_fixture()
    states = {"a": [1.0, 0.0], "b": [1.0, 1.0]}
    covectors = np.array([[0.0, 0.0], [1.0, 0.0]])
    frames = {"a": [[2.0, 0.0], [0.0, 1.0]], "b": np.eye(2)}
    paths = {"a": (), "b": ("ba",)}
    baseline = hol.operational_record_law(
        complex_, links, states, "a", paths, ("quiet", "signal"), covectors
    )

    transformed_states = hol.passive_transform_states(complex_, states, frames)
    transformed_covectors = hol.passive_transform_covectors(
        complex_, covectors, "a", frames
    )
    transformed_links = hol.passive_transform_links(complex_, links, frames)
    coherent = hol.operational_record_law(
        complex_,
        transformed_links,
        transformed_states,
        "a",
        paths,
        ("quiet", "signal"),
        transformed_covectors,
    )
    broken = hol.operational_record_law(
        complex_,
        links,
        transformed_states,
        "a",
        paths,
        ("quiet", "signal"),
        transformed_covectors,
    )

    assert_array_equal(coherent.logits, baseline.logits)
    assert_array_equal(coherent.probabilities, baseline.probabilities)
    assert_array_equal(broken.logits, [0.0, 3.0])
    gap = hol.operational_observable(
        broken, {"quiet": 0.0, "signal": 1.0}
    ) - hol.operational_observable(
        baseline,
        {"quiet": 0.0, "signal": 1.0},
    )
    assert gap == pytest.approx(0.07177704884455077, abs=1e-15)


def test_link_only_diagnostic_disclaims_an_operational_holonomy_conclusion():
    """Mutation caught: promoting link holonomy alone to an operational claim."""
    complex_, links = _nonflat_plaquette()
    diagnostic = hol.link_only_diagnostic(
        hol.cycle_holonomy(complex_, links, ("e01", "e12", "e23", "e30"))
    )

    assert diagnostic.supports_operational_claim is False
    assert diagnostic.operational_conclusion is None
    assert "graph-link" in diagnostic.limitation


def test_operational_claim_rejects_raw_unnormalized_weights():
    """Mutation caught: accepting raw weights as a normalized record law."""
    with pytest.raises(TypeError, match="normalized OperationalRecordLaw"):
        hol.operational_observable(np.array([1.0, 2.0]), {"a": 0.0, "b": 1.0})
