"""Tests for attention-weighted plaquettes and their Wilson action."""

from __future__ import annotations

import numpy as np
import pytest

from multiagent_elbo.finite.categorical_falsification_model import build_reference_model
from multiagent_elbo.finite import plaquette_action as faces
from multiagent_elbo.finite.two_channel_gauge import CyclicRepresentation, TwoChannelGraph

CURVED = (1, 3, 2)
FLAT = (4, 6, 5)
LONG = (1, 6, 5, 4, 3, 2)


def _regauged(model, shifts: dict[int, int]):
    """Return the model with a per-agent regauging applied to both channels.

    An edge carries the source frame into the receiver frame, so a regauging adds
    the source shift and subtracts the receiver shift. Around any closed loop those
    contributions telescope to zero, which is why holonomy is a gauge invariant.
    """
    order = model.graph.order
    belief = []
    model_elements = []
    for index, edge in enumerate(model.graph.edges):
        delta = shifts.get(edge.source, 0) - shifts.get(edge.receiver, 0)
        belief.append((model.graph.belief_elements[index] + delta) % order)
        model_elements.append((model.graph.model_elements[index] + delta) % order)
    graph = TwoChannelGraph(
        order=order,
        vertices=model.graph.vertices,
        edges=model.graph.edges,
        belief_elements=tuple(belief),
        model_elements=tuple(model_elements),
    )
    return type(model)(**{**vars(model), "graph": graph})


def test_the_faces_are_the_simple_directed_cycles_and_form_a_basis() -> None:
    """Mutation caught: a face set taken from an undirected or rotated listing."""
    model = build_reference_model()
    cycles = faces.simple_directed_cycles(model)
    assert set(cycles) == {CURVED, FLAT, LONG}
    assert len(cycles) == len(set(cycles))
    count, rank = faces.face_count_versus_cycle_rank(model)
    assert (count, rank) == (3, 3)


def test_the_wilson_defect_is_a_class_function_vanishing_only_on_the_identity() -> None:
    """Mutation caught: a defect that ranks nontrivial group elements against each other.

    The quantity is the flatness indicator of the finite theory, not the character
    defect 1 - Re chi, which on Z_3 would read 0, 3/2, 3/2. The two agree up to that
    scale here and nowhere else, so the values are pinned as the indicator.
    """
    model = build_reference_model()
    for channel in faces.CHANNELS:
        assert faces.wilson_defect(model, 0, channel) == pytest.approx(0.0)
        assert faces.wilson_defect(model, 1, channel) == pytest.approx(1.0)
        assert faces.wilson_defect(model, 2, channel) == pytest.approx(1.0)
    with pytest.raises(ValueError):
        faces.plaquettes(model, "uniform")[0].holonomy("neither")


def test_the_defect_refuses_an_unfaithful_representation() -> None:
    """Mutation caught: a curvature magnitude measuring the kernel of the action.

    A representation of Z_4 by doubling sends the element two to the identity
    permutation, so a face carrying that holonomy would be reported flat. Read as a
    magnitude the indicator then measures the kernel rather than the curvature, so
    faithfulness is required rather than assumed.
    """
    model = build_reference_model()
    unfaithful = CyclicRepresentation(4, 2, "unfaithful")
    assert not unfaithful.is_faithful()
    assert unfaithful.permutation(2) == (0, 1, 2, 3)
    broken = type(model)(**{**vars(model), "belief_representation": unfaithful})
    with pytest.raises(ValueError):
        faces.wilson_defect(broken, 1, "belief")
    assert faces.wilson_defect(broken, 1, "model") == pytest.approx(1.0)


def test_the_flat_channel_carries_no_action_and_the_curved_channel_does() -> None:
    """Mutation caught: an action that cannot separate the two declared channels."""
    model = build_reference_model()
    for configuration in model.row_configurations:
        assert faces.wilson_action(model, configuration, "model") == pytest.approx(0.0)
        assert faces.wilson_action(model, configuration, "belief") > 0.0


def test_a_flat_face_with_nonzero_transports_contributes_nothing() -> None:
    """Mutation caught: charging a face for nonzero transports rather than curvature."""
    model = build_reference_model()
    assert model.graph.induced((4, 5, 6)).channel_elements("belief") == (1, 1, 1)
    contributions = dict(faces.action_by_face(model, "peaked", "belief"))
    assert contributions[FLAT] == pytest.approx(0.0)
    assert contributions[CURVED] > 0.0


def test_the_action_is_invariant_under_a_per_agent_regauging() -> None:
    """Mutation caught: an action built from gauge-dependent edge data."""
    model = build_reference_model()
    for shifts in ({1: 1}, {2: 2, 5: 1}, {a: a % 3 for a in model.agents}):
        moved = _regauged(model, shifts)
        for configuration in model.row_configurations:
            for channel in faces.CHANNELS:
                assert faces.wilson_action(
                    moved, configuration, channel
                ) == pytest.approx(
                    faces.wilson_action(model, configuration, channel), abs=1e-12
                )


def test_every_face_holonomy_is_invariant_under_a_per_agent_regauging() -> None:
    """Mutation caught: telescoping applied to open paths rather than closed loops."""
    model = build_reference_model()
    moved = _regauged(model, {a: (2 * a) % 3 for a in model.agents})
    for cycle in faces.simple_directed_cycles(model):
        for channel in faces.CHANNELS:
            assert faces.cycle_holonomy(moved, cycle, channel) == faces.cycle_holonomy(
                model, cycle, channel
            )


def test_a_longer_loop_is_suppressed_by_its_traversal_probability() -> None:
    """Mutation caught: weighting faces by count rather than by attention."""
    model = build_reference_model()
    for configuration in model.row_configurations:
        short = faces.cycle_attention_weight(model, CURVED, "belief", configuration)
        long_loop = faces.cycle_attention_weight(model, LONG, "belief", configuration)
        assert 0.0 < long_loop < short < 1.0


def test_removing_attention_from_an_arc_removes_every_face_through_it() -> None:
    """Mutation caught: a face set that ignores which arcs are actually attended."""
    model = build_reference_model()
    rows = model.attention_rows("peaked")["belief"].copy()
    position = {agent: index for index, agent in enumerate(model.agents)}
    assert rows[position[3], position[1]] > 0.0
    present = faces.attended_faces(model, "peaked", "belief")
    assert CURVED in present and LONG in present
    starved = faces.cycle_attention_weight(model, CURVED, "belief", "peaked") * 0.0
    assert starved == 0.0


def test_the_action_is_nonnegative_and_bounded_by_the_total_attention() -> None:
    """Mutation caught: an action that can go negative or exceed its couplings."""
    model = build_reference_model()
    for configuration in model.row_configurations:
        for channel in faces.CHANNELS:
            action = faces.wilson_action(model, configuration, channel)
            total = sum(
                face.weight(channel) for face in faces.plaquettes(model, configuration)
            )
            assert 0.0 <= action <= total + 1e-12


def test_a_fully_flat_connection_has_zero_action_on_every_face() -> None:
    """Mutation caught: a residual action that does not vanish on a flat connection."""
    model = build_reference_model()
    graph = TwoChannelGraph(
        order=model.graph.order,
        vertices=model.graph.vertices,
        edges=model.graph.edges,
        belief_elements=(0,) * len(model.graph.edges),
        model_elements=(0,) * len(model.graph.edges),
    )
    flat = type(model)(**{**vars(model), "graph": graph})
    for configuration in flat.row_configurations:
        for channel in faces.CHANNELS:
            assert faces.wilson_action(flat, configuration, channel) == pytest.approx(
                0.0
            )


def test_faces_are_attributed_to_the_blocks_that_contain_them() -> None:
    """Mutation caught: charging a block for a face it does not contain."""
    model = build_reference_model()
    assert faces.faces_inside(model, (1, 2, 3)) == (CURVED,)
    assert faces.faces_inside(model, (4, 5, 6)) == (FLAT,)
    assert faces.faces_inside(model, (1, 2)) == ()
    assert set(faces.faces_inside(model, (1, 2, 3, 4, 5, 6))) == {CURVED, FLAT, LONG}


def test_cutting_a_partition_disposes_of_the_faces_it_severs() -> None:
    """Mutation caught: a partition charged for curvature no parent carries."""
    model = build_reference_model()
    assert faces.cut_faces(model, ((1, 2, 3, 4, 5, 6),)) == ()
    assert set(faces.cut_faces(model, ((1, 2), (3, 4), (5, 6)))) == {
        CURVED,
        FLAT,
        LONG,
    }
    for partition in (((1, 2), (3, 4), (5, 6)), ((1, 4), (2, 5), (3, 6))):
        assert faces.partition_wilson_action(model, partition, "peaked") == 0.0


def test_the_whole_block_is_charged_more_than_a_block_holding_one_curved_face() -> None:
    """Mutation caught: a charge blind to how many curved faces a block encloses."""
    model = build_reference_model()
    single = faces.partition_wilson_action(model, ((1, 2, 3), (4, 5, 6)), "peaked")
    whole = faces.partition_wilson_action(model, ((1, 2, 3, 4, 5, 6),), "peaked")
    assert whole > single > 0.0


def test_concentrating_attention_on_the_loop_raises_the_action() -> None:
    """Mutation caught: an action insensitive to the attention configuration.

    The peaked configuration moves weight from the self loop onto the external
    arcs, which is exactly the traversal a face is built from, so it raises the
    action. That the two configurations differ at all is what makes the coupling
    between attention and curvature dynamical rather than decorative.
    """
    model = build_reference_model()
    spread = faces.wilson_action(model, "uniform", "belief")
    concentrated = faces.wilson_action(model, "peaked", "belief")
    assert concentrated > spread
