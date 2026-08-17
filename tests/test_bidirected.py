"""Tests for the bi-directed instance and its two reverse-transport conventions."""

from __future__ import annotations

import numpy as np
import pytest

from multiagent_elbo.finite.categorical_falsification_model import build_reference_model
from multiagent_elbo.finite import bidirected as bidi
from multiagent_elbo.finite import plaquette_action as plaquettes
from multiagent_elbo.finite.two_channel_gauge import TwoChannelGraph


def test_the_declared_instance_is_one_way_so_its_asymmetry_is_vacuous() -> None:
    """Mutation caught: calling a one-way skeleton a bi-directed network."""
    model = build_reference_model()
    arcs = {(edge.source, edge.receiver) for edge in model.graph.edges}
    assert not [pair for pair in arcs if pair[::-1] in arcs]
    rows = model.attention_rows("peaked")["belief"]
    position = {agent: index for index, agent in enumerate(model.agents)}
    assert rows[position[1], position[2]] > 0.0
    assert rows[position[2], position[1]] == 0.0


@pytest.mark.parametrize("convention", ["reciprocal", "independent"])
def test_the_bidirected_instance_carries_both_directions(convention: str) -> None:
    """Mutation caught: adding reverse arcs without giving them their own weights."""
    model = bidi.build_bidirected_model(convention)
    arcs = {(edge.source, edge.receiver) for edge in model.graph.edges}
    assert len(arcs) == 16
    assert all(pair[::-1] in arcs for pair in arcs)
    rows = model.attention_rows("peaked")["belief"]
    position = {agent: index for index, agent in enumerate(model.agents)}
    forward = rows[position[1], position[2]]
    reverse = rows[position[2], position[1]]
    assert forward > 0.0 and reverse > 0.0
    assert forward != reverse
    assert np.allclose(rows.sum(axis=1), 1.0, atol=1e-12)


def test_reciprocity_is_detectable_from_the_faces_alone() -> None:
    """Mutation caught: a declared convention with no observable consequence."""
    assert bidi.reversal_is_inverse(bidi.build_bidirected_model("reciprocal"))
    assert not bidi.reversal_is_inverse(bidi.build_bidirected_model("independent"))
    with pytest.raises(ValueError):
        bidi.build_bidirected_model("neither")


def test_a_missing_orientation_is_reported_apart_from_a_failure_of_reciprocity() -> None:
    """Mutation caught: reading a one-way skeleton as a refutation of reciprocity.

    The declared instance carries no reverse arc at all, so there is no reverse
    transport that could disagree with the inverse and the hypothesis is untestable
    rather than refuted. Returning False there would read as evidence against
    reciprocity produced by a graph that cannot supply any.
    """
    with pytest.raises(ValueError):
        bidi.reversal_is_inverse(build_reference_model())


def test_the_face_set_is_the_directed_cycle_basis_in_both_orientations() -> None:
    """Mutation caught: a face set at the undirected rank, blind to two-cycles.

    A two-cycle is a two-cell of the bi-directed complex and it is exactly where the
    independent convention puts curvature the reciprocal one cannot. The basis is
    therefore one loop per reciprocal pair plus one fundamental loop per chord, which
    is the directed cycle rank, edges minus vertices plus one: eight plus three on
    this skeleton against the three the undirected count would report.
    """
    model = bidi.build_bidirected_model("reciprocal")
    loops = bidi.basis_loops(model)
    rank = len(model.graph.edges) - len(model.graph.vertices) + 1
    assert len(loops) == rank == 11
    assert len([loop for loop in loops if len(loop) == 2]) == 8
    arcs = {
        (edge.source, edge.receiver): index
        for index, edge in enumerate(model.graph.edges)
    }
    incidence = np.zeros((len(loops), len(model.graph.edges)))
    for row, loop in enumerate(loops):
        for step, source in enumerate(loop):
            incidence[row, arcs[(source, loop[(step + 1) % len(loop)])]] += 1.0
    assert np.linalg.matrix_rank(incidence) == rank
    faces = bidi.oriented_faces(model)
    assert len(faces) == 2 * len(loops)
    assert {face.orientation for face in faces} == {"forward", "reverse"}


def test_the_two_orientations_carry_different_attention_weights() -> None:
    """Mutation caught: an orientation-blind weight on a two-sided network.

    A two-cycle is its own reversal, so its two traversals visit the same pair of
    arcs and necessarily carry the same weight. The claim is about the loops that
    have two genuinely distinct traversals, so it is asserted there and the
    coincidence is asserted on the two-cycles rather than left unstated.
    """
    model = bidi.build_bidirected_model("reciprocal")
    paired: dict[tuple, list] = {}
    for face in bidi.oriented_faces(model):
        paired.setdefault(tuple(sorted(face.cycle)), []).append(face)
    longer = [entry for entry in paired.values() if len(entry[0].cycle) > 2]
    assert len(longer) == 3
    assert all(entry[0].belief_weight != entry[1].belief_weight for entry in longer)
    two_cycles = [entry for entry in paired.values() if len(entry[0].cycle) == 2]
    assert len(two_cycles) == 8
    assert all(entry[0].belief_weight == entry[1].belief_weight for entry in two_cycles)


def test_reciprocity_preserves_the_flatness_of_the_model_channel() -> None:
    """Mutation caught: a convention change silently destroying the design.

    Every two-cycle is flat under the reciprocal convention by construction, since
    its holonomy is the forward element plus its own inverse, so admitting the
    two-cycles into the face set leaves every reciprocal result exactly where it was.
    Under the independent convention they are curved, which is the shortest-scale
    curvature the face set previously could not see.
    """
    reciprocal = bidi.build_bidirected_model("reciprocal")
    two_cycles = [
        face for face in bidi.oriented_faces(reciprocal) if len(face.cycle) == 2
    ]
    assert len(two_cycles) == 16
    assert all(
        face.belief_holonomy == 0 and face.model_holonomy == 0 for face in two_cycles
    )
    assert bidi.wilson_action(reciprocal, "model") == pytest.approx(0.0, abs=1e-15)
    assert bidi.wilson_action(reciprocal, "belief") > 0.0
    independent = bidi.build_bidirected_model("independent")
    curved = [
        face
        for face in bidi.oriented_faces(independent)
        if len(face.cycle) == 2 and (face.belief_holonomy or face.model_holonomy)
    ]
    assert curved
    assert bidi.wilson_action(independent, "model") > 0.0


def test_the_two_conventions_are_matched_controls() -> None:
    """Mutation caught: a shared rng stream confounding the convention comparison.

    The reverse elements draw from their own stream, so the forward elements and
    every attention row are bit-identical across conventions and the only declared
    difference between the two instances is the reverse transport itself.
    """
    reciprocal = bidi.build_bidirected_model("reciprocal")
    independent = bidi.build_bidirected_model("independent")
    edges = len(build_reference_model().graph.edges)
    assert reciprocal.graph.edges == independent.graph.edges
    assert reciprocal.graph.belief_elements[:edges] == (
        independent.graph.belief_elements[:edges]
    )
    assert reciprocal.graph.model_elements[:edges] == (
        independent.graph.model_elements[:edges]
    )
    assert reciprocal.graph.belief_elements[edges:] != (
        independent.graph.belief_elements[edges:]
    )
    left = reciprocal.attention_rows("peaked")
    right = independent.attention_rows("peaked")
    for channel in ("belief", "model"):
        assert np.array_equal(left[channel], right[channel])


def test_each_two_cell_is_charged_once_by_the_bidirected_action() -> None:
    """Mutation caught: summing the orientations and charging every face twice.

    Both traversals of a two-cell carry the same defect, so summing them charged the
    cell twice at a normalization no other module uses. The action is the mean of the
    two directed traversal probabilities times that defect, which puts one charge on
    one geometric two-cell and matches how `plaquette_action.wilson_action` counts a
    simple directed cycle.
    """
    model = bidi.build_bidirected_model("reciprocal")
    faces = bidi.oriented_faces(model)
    doubled = sum(
        face.weight("belief") * plaquettes.wilson_defect(model, face.holonomy("belief"), "belief")
        for face in faces
    )
    assert bidi.wilson_action(model, "belief") == pytest.approx(doubled / 2.0, abs=1e-15)
    assert bidi.wilson_action(model, "belief") == pytest.approx(0.0428236615, abs=1e-9)


def test_a_globally_frame_derived_connection_is_flat_on_every_face() -> None:
    """Mutation caught: conflating local reciprocity with a pure-gauge connection.

    Reversing an arc inverts its transport under either reading, but a connection
    that is globally a difference of per-agent frames telescopes around any closed
    loop and carries no curvature at all. Local reciprocity is the weaker condition
    and is what leaves curvature possible.
    """
    model = build_reference_model()
    generator = np.random.default_rng(5)
    for _ in range(4):
        frames = {
            vertex: int(value)
            for vertex, value in zip(
                model.graph.vertices, generator.integers(0, 3, len(model.graph.vertices))
            )
        }
        elements = tuple(
            (frames[edge.receiver] - frames[edge.source]) % model.graph.order
            for edge in model.graph.edges
        )
        graph = TwoChannelGraph(
            order=model.graph.order,
            vertices=model.graph.vertices,
            edges=model.graph.edges,
            belief_elements=elements,
            model_elements=elements,
        )
        pure_gauge = type(model)(**{**vars(model), "graph": graph})
        for cycle in plaquettes.simple_directed_cycles(pure_gauge):
            assert plaquettes.cycle_holonomy(pure_gauge, cycle, "belief") == 0


def test_the_declared_connection_is_reciprocal_without_being_pure_gauge() -> None:
    """Mutation caught: a curvature claim on a connection that is trivializable."""
    model = build_reference_model()
    holonomies = [
        plaquettes.cycle_holonomy(model, cycle, "belief")
        for cycle in plaquettes.simple_directed_cycles(model)
    ]
    assert any(value != 0 for value in holonomies)


def test_declared_rows_must_be_normalized_and_cover_both_channels() -> None:
    """Mutation caught: accepting declared rows that are not conditional laws."""
    model = bidi.build_bidirected_model("reciprocal")
    broken = tuple(
        (name, channel, tuple(tuple(0.5 for _ in row) for row in matrix))
        for name, channel, matrix in model.declared_rows
    )
    bad = type(model)(**{**vars(model), "declared_rows": broken})
    with pytest.raises(ValueError):
        bad.attention_rows("peaked")
    missing = tuple(entry for entry in model.declared_rows if entry[1] == "belief")
    partial = type(model)(**{**vars(model), "declared_rows": missing})
    with pytest.raises(ValueError):
        partial.attention_rows("peaked")


def test_the_declared_instance_still_uses_its_built_in_configurations() -> None:
    """Mutation caught: the new declared-row path capturing the original model."""
    model = build_reference_model()
    assert model.declared_rows is None
    for configuration in model.row_configurations:
        rows = model.attention_rows(configuration)
        assert set(rows) == {"belief", "model"}
        assert np.allclose(rows["belief"].sum(axis=1), 1.0, atol=1e-12)
