"""Executable contract for the exact typed-intervention witness.

Every expected value is hand-derived from the approved design. This file is
committed before the production witness so the first focused run records a
genuine RED at the missing-witness boundary.
"""

from __future__ import annotations

import hashlib
import inspect
import importlib.util
import io
import itertools
import json
import re
import subprocess
import sys
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path
from types import ModuleType

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "docs/derivations/2026-08-14-typed-intervention-nonidentifiability"
WITNESS = RUN / "evidence/exact_typed_intervention_witness.py"
SNAPSHOT = RUN / "evidence/test_typed_intervention_semantics_witness.snapshot.py"
RED_MESSAGE = (
    "expected RED: exact_typed_intervention_witness.py has not been implemented"
)
REQUIRED_API = {
    "bsc",
    "compose_bsc",
    "compose_context",
    "direct_retained_law",
    "split_joint_law",
    "split_retained_law",
    "null_extended_joint_law",
    "null_extended_retained_law",
    "intervention_response",
    "shared_boundary_intervention_law",
    "mediator_response",
    "binary_total_variation",
    "contextual_response_signature",
    "response_image",
    "same_signature_counterexample",
    "raw_presentation_invariants",
    "main",
}

CONTROL_A = Fraction(1, 10)
CONTROL_B = Fraction(1, 8)
CONTROL_DELTA = Fraction(1, 5)
CONTROL_ETA = Fraction(2, 5)
LEFT_A = Fraction(1, 4)
LEFT_B = Fraction(1, 3)
RIGHT_A = Fraction(1, 3)
RIGHT_B = Fraction(1, 4)
PASSIVE_COUNTEREXAMPLE_LAW = (
    Fraction(7, 24),
    Fraction(5, 24),
    Fraction(5, 24),
    Fraction(7, 24),
)

CONTROL_CONTEXTS = (
    (),
    (("R", 0),),
    (("R", 1),),
    (("O", 0),),
    (("O", 1),),
    (("R", 0), ("O", 0)),
    (("R", 0), ("O", 1)),
    (("R", 1), ("O", 0)),
    (("R", 1), ("O", 1)),
)
CONTROL_RETAINED_LAWS = (
    (Fraction(2, 5), Fraction(1, 10), Fraction(1, 10), Fraction(2, 5)),
    (Fraction(4, 5), Fraction(1, 5), Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(0), Fraction(1, 5), Fraction(4, 5)),
    (Fraction(1, 2), Fraction(0), Fraction(1, 2), Fraction(0)),
    (Fraction(0), Fraction(1, 2), Fraction(0), Fraction(1, 2)),
    (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
    (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
)
REDUCED_REPRESENTATIVES = (
    (),
    (("O", 0),),
    (("O", 1),),
    (("E", 0),),
    (("E", 1),),
    (("R", 0),),
    (("R", 0), ("O", 0)),
    (("R", 0), ("O", 1)),
    (("R", 0), ("E", 0)),
    (("R", 0), ("E", 1)),
    (("R", 1),),
    (("R", 1), ("O", 0)),
    (("R", 1), ("O", 1)),
    (("R", 1), ("E", 0)),
    (("R", 1), ("E", 1)),
)
LEFT_REDUCED_RESPONSES = (
    PASSIVE_COUNTEREXAMPLE_LAW,
    (Fraction(1, 2), Fraction(0), Fraction(1, 2), Fraction(0)),
    (Fraction(0), Fraction(1, 2), Fraction(0), Fraction(1, 2)),
    (Fraction(1, 3), Fraction(1, 6), Fraction(1, 3), Fraction(1, 6)),
    (Fraction(1, 6), Fraction(1, 3), Fraction(1, 6), Fraction(1, 3)),
    (Fraction(7, 12), Fraction(5, 12), Fraction(0), Fraction(0)),
    (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
    (Fraction(2, 3), Fraction(1, 3), Fraction(0), Fraction(0)),
    (Fraction(1, 3), Fraction(2, 3), Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(0), Fraction(5, 12), Fraction(7, 12)),
    (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
    (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
    (Fraction(0), Fraction(0), Fraction(2, 3), Fraction(1, 3)),
    (Fraction(0), Fraction(0), Fraction(1, 3), Fraction(2, 3)),
)
RIGHT_REDUCED_RESPONSES = (
    PASSIVE_COUNTEREXAMPLE_LAW,
    (Fraction(1, 2), Fraction(0), Fraction(1, 2), Fraction(0)),
    (Fraction(0), Fraction(1, 2), Fraction(0), Fraction(1, 2)),
    (Fraction(3, 8), Fraction(1, 8), Fraction(3, 8), Fraction(1, 8)),
    (Fraction(1, 8), Fraction(3, 8), Fraction(1, 8), Fraction(3, 8)),
    (Fraction(7, 12), Fraction(5, 12), Fraction(0), Fraction(0)),
    (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
    (Fraction(3, 4), Fraction(1, 4), Fraction(0), Fraction(0)),
    (Fraction(1, 4), Fraction(3, 4), Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(0), Fraction(5, 12), Fraction(7, 12)),
    (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
    (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
    (Fraction(0), Fraction(0), Fraction(3, 4), Fraction(1, 4)),
    (Fraction(0), Fraction(0), Fraction(1, 4), Fraction(3, 4)),
)
CLASS_SIZES = (1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1)
COUNTEREXAMPLE_KEYS = {
    "passive_equal",
    "passive_law",
    "left_experiment",
    "right_experiment",
    "left_unmatched_response",
    "boundary_match_exists",
    "diagnostic_tv",
    "raw_invariants_equal",
}
RAW_PRESENTATION_INVARIANTS = {
    "direct": {
        "roles": ("retained-state", "record"),
        "cardinalities": (2, 2),
        "edges": (("R", "O"),),
        "auxiliary_target": (),
    },
    "split": {
        "roles": ("retained-state", "mediator", "record"),
        "cardinalities": (2, 2, 2),
        "edges": (("R", "E"), ("E", "O")),
        "auxiliary_target": ("E",),
    },
    "null": {
        "roles": ("retained-state", "mediator", "null", "record"),
        "cardinalities": (2, 2, 2, 2),
        "edges": (("R", "E"), ("E", "O")),
        "auxiliary_target": ("E", "N"),
    },
}
NUMERIC_RE = re.compile(r"^-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?$")
NUMERIC_LIKE_RE = re.compile(
    r"^[+-]?(?:[0-9]+(?:[./][0-9]*)?|[.][0-9]+)(?:[eE][+-]?[0-9]+)?$"
)


def _load_witness() -> ModuleType:
    assert WITNESS.is_file(), RED_MESSAGE
    spec = importlib.util.spec_from_file_location(
        "exact_typed_intervention_witness", WITNESS
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    missing = sorted(name for name in REQUIRED_API if not callable(getattr(module, name, None)))
    assert not missing, f"expected RED: witness API is missing {missing}"
    return module


def _all_contexts(nodes):
    return tuple(
        tuple((node, value) for node, value in zip(nodes, values) if value is not None)
        for values in itertools.product((None, 0, 1), repeat=len(nodes))
    )


def _direct_oracle_experiment():
    contexts = _all_contexts(("R", "O"))
    literal_responses = dict(zip(CONTROL_CONTEXTS, CONTROL_RETAINED_LAWS))

    def right_override(left, right):
        assignments = dict(left)
        assignments.update(right)
        return tuple(
            (node, assignments[node])
            for node in ("R", "O")
            if node in assignments
        )

    signatures = {
        context: tuple(
            literal_responses[right_override(right_override(left, context), right)]
            for left in contexts
            for right in contexts
        )
        for context in contexts
    }
    signature_classes = {}
    for context in contexts:
        signature_classes.setdefault(signatures[context], []).append(context)
    classes = tuple(tuple(members) for members in signature_classes.values())
    context_to_class = {
        context: class_index
        for class_index, behavioral_class in enumerate(classes)
        for context in behavioral_class
    }
    multiplication = tuple(
        tuple(
            context_to_class[right_override(left_class[0], right_class[0])]
            for right_class in classes
        )
        for left_class in classes
    )
    responses = tuple(literal_responses[members[0]] for members in classes)
    return contexts, signatures, (classes, multiplication, responses)


def _relabel_retained(law, flip_r, flip_o):
    return tuple(
        law[(r ^ flip_r) * 2 + (o ^ flip_o)]
        for r, o in itertools.product((0, 1), repeat=2)
    )


def _relabel_joint(law, flips):
    relabeled = []
    for new_bits in itertools.product((0, 1), repeat=len(flips)):
        old_bits = tuple(bit ^ flip for bit, flip in zip(new_bits, flips))
        old_index = sum(bit << (len(flips) - index - 1) for index, bit in enumerate(old_bits))
        relabeled.append(law[old_index])
    return tuple(relabeled)


def _context_json(context):
    return [[node, bit] for node, bit in context]


def _canonical_experiment_bytes(experiment, node_order):
    classes, multiplication, responses = experiment
    document = {
        "boundary_order": ["R", "O"],
        "identity": 0,
        "multiplication": multiplication,
        "node_order": list(node_order),
        "records": [
            {
                "members": [_context_json(context) for context in behavioral_class],
                "representative": _context_json(behavioral_class[0]),
                "response": [str(atom) for atom in response],
            }
            for behavioral_class, response in zip(classes, responses)
        ],
    }
    return json.dumps(
        document, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def _json_ready(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_json_ready(item) for item in value]
    return value


def _validate_json_tree(value):
    if isinstance(value, dict):
        for key, item in value.items():
            assert isinstance(key, str)
            _validate_json_tree(item)
        return
    if isinstance(value, list):
        for item in value:
            _validate_json_tree(item)
        return
    if isinstance(value, bool):
        return
    assert isinstance(value, str)
    if NUMERIC_LIKE_RE.fullmatch(value):
        assert NUMERIC_RE.fullmatch(value)
        assert str(Fraction(value)) == value


def _capture_main(witness):
    stream = io.StringIO()
    with redirect_stdout(stream):
        status = witness.main()
    output = stream.getvalue()
    assert status == 0
    return output.encode("ascii"), json.loads(output)


def _call_signature(function):
    signature = inspect.signature(function)
    return tuple(
        (parameter.name, parameter.kind, parameter.default)
        for parameter in signature.parameters.values()
    )


def _assert_context_schema(context, node_order):
    assert type(context) is tuple
    ranks = {node: index for index, node in enumerate(node_order)}
    previous_rank = -1
    seen = set()
    for assignment in context:
        assert type(assignment) is tuple
        assert len(assignment) == 2
        node, bit = assignment
        assert type(node) is str
        assert node in ranks
        assert node not in seen
        assert ranks[node] > previous_rank
        assert type(bit) is int
        assert bit in (0, 1)
        seen.add(node)
        previous_rank = ranks[node]


def _assert_retained_law_schema(law):
    assert type(law) is tuple
    assert len(law) == 4
    assert all(type(atom) is Fraction and atom >= 0 for atom in law)
    assert sum(law, Fraction(0)) == Fraction(1)


def _assert_contextual_signature_schema(signature, node_order):
    context_count = 3 ** len(node_order)
    assert type(signature) is tuple
    assert len(signature) == context_count * context_count
    for law in signature:
        _assert_retained_law_schema(law)


def _assert_reduced_experiment_schema(experiment, node_order):
    assert type(experiment) is tuple
    assert len(experiment) == 3
    classes, multiplication, responses = experiment
    assert type(classes) is tuple
    assert classes
    flattened_contexts = []
    representatives = []
    canonical_contexts = _all_contexts(node_order)
    context_ranks = {
        context: index for index, context in enumerate(canonical_contexts)
    }
    for behavioral_class in classes:
        assert type(behavioral_class) is tuple
        assert behavioral_class
        for context in behavioral_class:
            _assert_context_schema(context, node_order)
            flattened_contexts.append(context)
        assert behavioral_class == tuple(
            sorted(behavioral_class, key=context_ranks.__getitem__)
        )
        representatives.append(behavioral_class[0])
    assert len(flattened_contexts) == len(canonical_contexts)
    assert set(flattened_contexts) == set(canonical_contexts)
    assert tuple(representatives) == tuple(
        sorted(representatives, key=context_ranks.__getitem__)
    )

    class_count = len(classes)
    assert type(multiplication) is tuple
    assert len(multiplication) == class_count
    for row in multiplication:
        assert type(row) is tuple
        assert len(row) == class_count
        assert all(
            type(class_index) is int and 0 <= class_index < class_count
            for class_index in row
        )
    assert multiplication[0] == tuple(range(class_count))
    assert tuple(row[0] for row in multiplication) == tuple(range(class_count))

    assert type(responses) is tuple
    assert len(responses) == class_count
    for law in responses:
        _assert_retained_law_schema(law)


def test_public_api_call_signatures_are_exact():
    witness = _load_witness()
    positional = inspect.Parameter.POSITIONAL_OR_KEYWORD
    keyword_only = inspect.Parameter.KEYWORD_ONLY
    required = inspect.Parameter.empty
    expected = {
        "bsc": (
            ("epsilon", positional, required),
            ("output_bit", positional, required),
            ("input_bit", positional, required),
        ),
        "compose_bsc": (
            ("a", positional, required), ("b", positional, required)
        ),
        "compose_context": (
            ("left", positional, required), ("right", positional, required)
        ),
        "direct_retained_law": (
            ("delta", positional, required), ("context", positional, ())
        ),
        "split_joint_law": (
            ("a", positional, required), ("b", positional, required),
            ("context", positional, ()),
        ),
        "split_retained_law": (
            ("a", positional, required), ("b", positional, required),
            ("context", positional, ()),
        ),
        "null_extended_joint_law": (
            ("a", positional, required), ("b", positional, required),
            ("eta", positional, required), ("context", positional, ()),
        ),
        "null_extended_retained_law": (
            ("a", positional, required), ("b", positional, required),
            ("eta", positional, required), ("context", positional, ()),
        ),
        "intervention_response": (
            ("model", positional, required), ("a", keyword_only, required),
            ("b", keyword_only, required), ("eta", keyword_only, None),
            ("context", keyword_only, ()),
        ),
        "shared_boundary_intervention_law": (
            ("model", positional, required), ("context", positional, ())
        ),
        "mediator_response": (
            ("b", positional, required),
            ("mediator_bit", positional, required),
        ),
        "binary_total_variation": (
            ("left", positional, required), ("right", positional, required)
        ),
        "contextual_response_signature": (
            ("model", positional, required), ("a", keyword_only, required),
            ("b", keyword_only, required), ("eta", keyword_only, None),
            ("context", keyword_only, ()),
        ),
        "response_image": (
            ("model", positional, required), ("a", keyword_only, required),
            ("b", keyword_only, required), ("eta", keyword_only, None),
        ),
        "same_signature_counterexample": (),
        "raw_presentation_invariants": (("model", positional, required),),
        "main": (),
    }

    assert set(expected) == REQUIRED_API
    for name, parameters in expected.items():
        assert _call_signature(getattr(witness, name)) == parameters


@pytest.mark.parametrize(
    ("selector", "node_order", "eta"),
    (
        pytest.param("direct", ("R", "O"), None, id="direct"),
        pytest.param("split", ("R", "E", "O"), None, id="split"),
        pytest.param(
            "null", ("R", "E", "N", "O"), CONTROL_ETA, id="null"
        ),
    ),
)
def test_every_selector_returns_declared_signature_and_experiment_schemas(
    selector, node_order, eta
):
    witness = _load_witness()
    arguments = {"a": CONTROL_A, "b": CONTROL_B}
    if eta is not None:
        arguments["eta"] = eta

    signature = witness.contextual_response_signature(
        selector, **arguments, context=()
    )
    experiment = witness.response_image(selector, **arguments)
    _assert_contextual_signature_schema(signature, node_order)
    _assert_reduced_experiment_schema(experiment, node_order)


def test_direct_selector_matches_independent_literal_response_oracle():
    witness = _load_witness()
    contexts, signatures, expected_experiment = _direct_oracle_experiment()

    for context in contexts:
        actual = witness.contextual_response_signature(
            "direct", a=CONTROL_A, b=CONTROL_B, context=context
        )
        assert actual == signatures[context]
    actual_experiment = witness.response_image(
        "direct", a=CONTROL_A, b=CONTROL_B
    )
    assert actual_experiment == expected_experiment

    classes, multiplication, _ = actual_experiment
    lookup = {
        context: class_index
        for class_index, behavioral_class in enumerate(classes)
        for context in behavioral_class
    }
    for left_index, left_class in enumerate(classes):
        for right_index, right_class in enumerate(classes):
            products = {
                lookup[witness.compose_context(left, right)]
                for left in left_class
                for right in right_class
            }
            assert products == {multiplication[left_index][right_index]}


def test_bsc_context_composition_and_validation_are_exact():
    witness = _load_witness()

    assert witness.bsc(Fraction(1, 4), 0, 0) == Fraction(3, 4)
    assert witness.bsc(Fraction(1, 4), 1, 0) == Fraction(1, 4)
    assert witness.bsc(Fraction(1, 4), 0, 1) == Fraction(1, 4)
    assert witness.bsc(Fraction(1, 4), 1, 1) == Fraction(3, 4)
    assert witness.compose_bsc(CONTROL_A, CONTROL_B) == CONTROL_DELTA
    assert witness.compose_bsc(LEFT_A, LEFT_B) == Fraction(5, 12)
    assert witness.compose_bsc(RIGHT_A, RIGHT_B) == Fraction(5, 12)

    assert witness.compose_context(
        (("O", 1), ("R", 0)), (("E", 1),)
    ) == (("R", 0), ("E", 1), ("O", 1))
    assert witness.compose_context(
        (("R", 0), ("E", 0)), (("R", 1), ("O", 1))
    ) == (("R", 1), ("E", 0), ("O", 1))
    assert witness.compose_context(
        (("O", 1), ("N", 0)), (("E", 1), ("R", 0))
    ) == (("R", 0), ("E", 1), ("N", 0), ("O", 1))
    assert witness.compose_context((), ()) == ()

    for invalid in (Fraction(-1, 10), Fraction(11, 10)):
        with pytest.raises(ValueError):
            witness.bsc(invalid, 0, 0)
        with pytest.raises(ValueError):
            witness.compose_bsc(invalid, CONTROL_B)
        with pytest.raises(ValueError):
            witness.compose_bsc(CONTROL_A, invalid)
        with pytest.raises(ValueError):
            witness.direct_retained_law(invalid)
        with pytest.raises(ValueError):
            witness.split_joint_law(invalid, CONTROL_B)
        with pytest.raises(ValueError):
            witness.split_joint_law(CONTROL_A, invalid)
        with pytest.raises(ValueError):
            witness.null_extended_joint_law(CONTROL_A, CONTROL_B, invalid)

    for bad_context in (
        (("R", 0), ("R", 1)),
        (("X", 0),),
        (("R", 2),),
    ):
        with pytest.raises(ValueError):
            witness.compose_context(bad_context, ())
    with pytest.raises(ValueError):
        witness.bsc(CONTROL_A, 2, 0)
    with pytest.raises(ValueError):
        witness.bsc(CONTROL_A, 0, -1)

    invalid_context_calls = (
        lambda: witness.direct_retained_law(
            CONTROL_DELTA, (("E", 0),)
        ),
        lambda: witness.split_joint_law(
            CONTROL_A, CONTROL_B, (("N", 0),)
        ),
        lambda: witness.split_retained_law(
            CONTROL_A, CONTROL_B, (("N", 0),)
        ),
        lambda: witness.null_extended_joint_law(
            CONTROL_A, CONTROL_B, CONTROL_ETA, (("X", 0),)
        ),
        lambda: witness.null_extended_retained_law(
            CONTROL_A, CONTROL_B, CONTROL_ETA, (("X", 0),)
        ),
        lambda: witness.shared_boundary_intervention_law(
            "direct", (("E", 0),)
        ),
        lambda: witness.shared_boundary_intervention_law(
            "split", (("N", 0),)
        ),
        lambda: witness.contextual_response_signature(
            "direct", a=CONTROL_A, b=CONTROL_B, context=(("E", 0),)
        ),
        lambda: witness.contextual_response_signature(
            "split", a=CONTROL_A, b=CONTROL_B, context=(("N", 0),)
        ),
        lambda: witness.contextual_response_signature(
            "null", a=CONTROL_A, b=CONTROL_B, eta=CONTROL_ETA,
            context=(("X", 0),)
        ),
    )
    for invalid_context_call in invalid_context_calls:
        with pytest.raises(ValueError):
            invalid_context_call()
    with pytest.raises(ValueError):
        witness.intervention_response(
            "unknown", a=CONTROL_A, b=CONTROL_B, context=()
        )
    with pytest.raises(ValueError):
        witness.intervention_response(
            "direct", a=CONTROL_A, b=CONTROL_B, context=(("E", 0),)
        )
    with pytest.raises(ValueError):
        witness.intervention_response(
            "split", a=CONTROL_A, b=CONTROL_B, context=(("N", 0),)
        )
    with pytest.raises(ValueError):
        witness.intervention_response(
            "null", a=CONTROL_A, b=CONTROL_B, context=()
        )


def test_joint_and_retained_laws_use_frozen_lexicographic_order():
    witness = _load_witness()
    expected_split = (
        Fraction(63, 160), Fraction(9, 160), Fraction(1, 160), Fraction(7, 160),
        Fraction(7, 160), Fraction(1, 160), Fraction(9, 160), Fraction(63, 160),
    )
    expected_null = (
        Fraction(189, 800), Fraction(27, 800), Fraction(63, 400), Fraction(9, 400),
        Fraction(3, 800), Fraction(21, 800), Fraction(1, 400), Fraction(7, 400),
        Fraction(21, 800), Fraction(3, 800), Fraction(7, 400), Fraction(1, 400),
        Fraction(27, 800), Fraction(189, 800), Fraction(9, 400), Fraction(63, 400),
    )

    split_joint = witness.split_joint_law(CONTROL_A, CONTROL_B)
    null_joint = witness.null_extended_joint_law(
        CONTROL_A, CONTROL_B, CONTROL_ETA
    )
    assert isinstance(split_joint, tuple)
    assert isinstance(null_joint, tuple)
    assert split_joint == expected_split
    assert null_joint == expected_null
    assert all(isinstance(atom, Fraction) for atom in split_joint + null_joint)
    assert sum(split_joint, Fraction(0)) == Fraction(1)
    assert sum(null_joint, Fraction(0)) == Fraction(1)
    assert witness.direct_retained_law(CONTROL_DELTA) == CONTROL_RETAINED_LAWS[0]
    assert witness.split_retained_law(CONTROL_A, CONTROL_B) == CONTROL_RETAINED_LAWS[0]
    assert witness.null_extended_retained_law(
        CONTROL_A, CONTROL_B, CONTROL_ETA
    ) == CONTROL_RETAINED_LAWS[0]


def test_all_nine_shared_boundary_intervention_tables_are_literal():
    witness = _load_witness()

    for context, expected in zip(CONTROL_CONTEXTS, CONTROL_RETAINED_LAWS):
        assert witness.direct_retained_law(CONTROL_DELTA, context) == expected
        assert witness.split_retained_law(CONTROL_A, CONTROL_B, context) == expected
        assert witness.null_extended_retained_law(
            CONTROL_A, CONTROL_B, CONTROL_ETA, context
        ) == expected
        for model in ("direct", "split", "null"):
            assert witness.shared_boundary_intervention_law(model, context) == expected
            assert witness.intervention_response(
                model,
                a=CONTROL_A,
                b=CONTROL_B,
                eta=CONTROL_ETA,
                context=context,
            ) == expected


def test_control_mediator_responses_have_exact_total_variation():
    witness = _load_witness()
    left = (Fraction(7, 8), Fraction(1, 8))
    right = (Fraction(1, 8), Fraction(7, 8))

    assert witness.mediator_response(CONTROL_B, 0) == left
    assert witness.mediator_response(CONTROL_B, 1) == right
    assert witness.binary_total_variation(left, right) == Fraction(3, 4)
    with pytest.raises(ValueError):
        witness.mediator_response(CONTROL_B, 2)
    with pytest.raises(ValueError):
        witness.binary_total_variation(left, (Fraction(1),))


def test_null_assignments_are_exhaustively_inert_in_all_27_contexts():
    witness = _load_witness()

    for null_bit in (0, 1):
        for context in _all_contexts(("R", "E", "O")):
            extended = witness.compose_context((("N", null_bit),), context)
            expected = witness.split_retained_law(CONTROL_A, CONTROL_B, context)
            assert witness.null_extended_retained_law(
                CONTROL_A, CONTROL_B, CONTROL_ETA, extended
            ) == expected
            assert witness.intervention_response(
                "null",
                a=CONTROL_A,
                b=CONTROL_B,
                eta=CONTROL_ETA,
                context=extended,
            ) == expected


def test_null_two_sided_signatures_and_reduced_quotient_are_identical():
    witness = _load_witness()
    noop = witness.contextual_response_signature(
        "null", a=CONTROL_A, b=CONTROL_B, eta=CONTROL_ETA, context=()
    )
    do_n0 = witness.contextual_response_signature(
        "null",
        a=CONTROL_A,
        b=CONTROL_B,
        eta=CONTROL_ETA,
        context=(("N", 0),),
    )
    do_n1 = witness.contextual_response_signature(
        "null",
        a=CONTROL_A,
        b=CONTROL_B,
        eta=CONTROL_ETA,
        context=(("N", 1),),
    )
    _assert_contextual_signature_schema(noop, ("R", "E", "N", "O"))
    _assert_contextual_signature_schema(do_n0, ("R", "E", "N", "O"))
    _assert_contextual_signature_schema(do_n1, ("R", "E", "N", "O"))
    assert noop == do_n0 == do_n1
    assert len(noop) == 81 * 81
    serialized = json.dumps(
        [[str(atom) for atom in law] for law in noop],
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    assert hashlib.sha256(serialized).hexdigest() == (
        "19a12f8ac81046c57b6ff3d2c6039d69fab34639e47e9af074f431638ac3ce33"
    )

    split = witness.response_image("split", a=CONTROL_A, b=CONTROL_B)
    null = witness.response_image(
        "null", a=CONTROL_A, b=CONTROL_B, eta=CONTROL_ETA
    )
    _assert_reduced_experiment_schema(split, ("R", "E", "O"))
    _assert_reduced_experiment_schema(null, ("R", "E", "N", "O"))
    split_classes, split_multiplication, split_responses = split
    null_classes, null_multiplication, null_responses = null
    split_lookup = {
        context: class_index
        for class_index, behavioral_class in enumerate(split_classes)
        for context in behavioral_class
    }

    def forget_n(context):
        return tuple((node, bit) for node, bit in context if node != "N")

    class_map = []
    for behavioral_class in null_classes:
        image = {split_lookup[forget_n(context)] for context in behavioral_class}
        assert len(image) == 1
        class_map.append(image.pop())
    assert tuple(class_map) == tuple(range(15))
    assert null_responses == split_responses
    for left_index, row in enumerate(null_multiplication):
        for right_index, product_index in enumerate(row):
            assert class_map[product_index] == split_multiplication[
                class_map[left_index]
            ][class_map[right_index]]

    def containing(classes, context):
        return next(index for index, members in enumerate(classes) if context in members)

    assert containing(null_classes, ()) == containing(null_classes, (("N", 0),))
    assert containing(null_classes, ()) == containing(null_classes, (("N", 1),))


def test_same_signature_pair_has_frozen_passive_and_mediator_responses():
    witness = _load_witness()
    left_e0 = (Fraction(1, 3), Fraction(1, 6), Fraction(1, 3), Fraction(1, 6))
    left_e1 = (Fraction(1, 6), Fraction(1, 3), Fraction(1, 6), Fraction(1, 3))
    right_e0 = (Fraction(3, 8), Fraction(1, 8), Fraction(3, 8), Fraction(1, 8))
    right_e1 = (Fraction(1, 8), Fraction(3, 8), Fraction(1, 8), Fraction(3, 8))

    assert witness.compose_bsc(LEFT_A, LEFT_B) == Fraction(5, 12)
    assert witness.compose_bsc(RIGHT_A, RIGHT_B) == Fraction(5, 12)
    assert witness.split_retained_law(LEFT_A, LEFT_B) == PASSIVE_COUNTEREXAMPLE_LAW
    assert witness.split_retained_law(RIGHT_A, RIGHT_B) == PASSIVE_COUNTEREXAMPLE_LAW
    assert witness.split_retained_law(
        LEFT_A, LEFT_B, (("E", 0),)
    ) == left_e0
    assert witness.split_retained_law(
        LEFT_A, LEFT_B, (("E", 1),)
    ) == left_e1
    assert witness.split_retained_law(
        RIGHT_A, RIGHT_B, (("E", 0),)
    ) == right_e0
    assert witness.split_retained_law(
        RIGHT_A, RIGHT_B, (("E", 1),)
    ) == right_e1
    assert witness.mediator_response(LEFT_B, 0) == (
        Fraction(2, 3), Fraction(1, 3)
    )
    assert witness.mediator_response(LEFT_B, 1) == (
        Fraction(1, 3), Fraction(2, 3)
    )
    assert witness.mediator_response(RIGHT_B, 0) == (
        Fraction(3, 4), Fraction(1, 4)
    )
    assert witness.mediator_response(RIGHT_B, 1) == (
        Fraction(1, 4), Fraction(3, 4)
    )
    assert witness.binary_total_variation(
        witness.mediator_response(LEFT_B, 0),
        witness.mediator_response(LEFT_B, 1),
    ) == Fraction(1, 3)
    assert witness.binary_total_variation(
        witness.mediator_response(RIGHT_B, 0),
        witness.mediator_response(RIGHT_B, 1),
    ) == Fraction(1, 2)


def test_reduced_experiments_match_all_frozen_classes_tables_and_hashes():
    witness = _load_witness()
    left = witness.response_image("split", a=LEFT_A, b=LEFT_B)
    right = witness.response_image("split", a=RIGHT_A, b=RIGHT_B)
    left_classes, left_multiplication, left_responses = left
    right_classes, right_multiplication, right_responses = right

    for experiment in (left, right):
        _assert_reduced_experiment_schema(experiment, ("R", "E", "O"))
    assert tuple(behavioral_class[0] for behavioral_class in left_classes) == (
        REDUCED_REPRESENTATIVES
    )
    assert tuple(behavioral_class[0] for behavioral_class in right_classes) == (
        REDUCED_REPRESENTATIVES
    )
    assert tuple(len(behavioral_class) for behavioral_class in left_classes) == CLASS_SIZES
    assert tuple(len(behavioral_class) for behavioral_class in right_classes) == CLASS_SIZES
    assert left_responses == LEFT_REDUCED_RESPONSES
    assert right_responses == RIGHT_REDUCED_RESPONSES
    assert left_multiplication == right_multiplication
    multiplication_bytes = json.dumps(
        left_multiplication, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    assert hashlib.sha256(multiplication_bytes).hexdigest() == (
        "c65706798f15a0a7fe8ee6d2be77525dc9afabf4266443f182d151ede619ea2d"
    )

    left_bytes = _canonical_experiment_bytes(left, ("R", "E", "O"))
    right_bytes = _canonical_experiment_bytes(right, ("R", "E", "O"))
    assert len(left_bytes) == 2337
    assert len(right_bytes) == 2337
    assert hashlib.sha256(left_bytes).hexdigest() == (
        "7a9b8ef13488caca86f061633c092873b8f64a949c7e134f1ae7eb27cae65283"
    )
    assert hashlib.sha256(right_bytes).hexdigest() == (
        "a83aa65a81eeda2817cc584c284b999453ec3633187881737ea159df41219dd0"
    )


def test_full_response_images_do_not_match_under_any_boundary_relabeling():
    witness = _load_witness()
    left = witness.response_image("split", a=LEFT_A, b=LEFT_B)
    right = witness.response_image("split", a=RIGHT_A, b=RIGHT_B)
    left_responses = set(left[2])
    unmatched = LEFT_REDUCED_RESPONSES[3]

    assert unmatched in left_responses
    for flip_r, flip_o in itertools.product((0, 1), repeat=2):
        transformed_right = {
            _relabel_retained(response, flip_r, flip_o) for response in right[2]
        }
        assert unmatched not in transformed_right
        assert left_responses != transformed_right


def test_raw_signature_and_all_binary_state_relabelings_are_controlled():
    witness = _load_witness()
    actual = {
        model: witness.raw_presentation_invariants(model)
        for model in ("direct", "split", "null")
    }
    assert actual == RAW_PRESENTATION_INVARIANTS
    assert actual["direct"] != actual["split"]
    assert actual["direct"] != actual["null"]
    assert actual["split"] != actual["null"]
    with pytest.raises(ValueError):
        witness.raw_presentation_invariants("unknown")

    left_joint = witness.split_joint_law(LEFT_A, LEFT_B)
    right_joint = witness.split_joint_law(RIGHT_A, RIGHT_B)
    assert all(
        _relabel_joint(right_joint, flips) != left_joint
        for flips in itertools.product((0, 1), repeat=3)
    )


def test_counterexample_record_is_transparent_and_independently_recomputed():
    witness = _load_witness()
    left = witness.response_image("split", a=LEFT_A, b=LEFT_B)
    right = witness.response_image("split", a=RIGHT_A, b=RIGHT_B)
    record = witness.same_signature_counterexample()

    assert set(record) == COUNTEREXAMPLE_KEYS
    assert record["passive_equal"] is True
    assert record["passive_law"] == PASSIVE_COUNTEREXAMPLE_LAW
    assert record["left_experiment"] == left
    assert record["right_experiment"] == right
    assert record["left_unmatched_response"] == LEFT_REDUCED_RESPONSES[3]
    assert record["boundary_match_exists"] is False
    assert record["diagnostic_tv"] == (Fraction(1, 3), Fraction(1, 2))
    assert record["raw_invariants_equal"] is True


def test_main_json_is_recursive_exact_sorted_compact_and_stable():
    witness = _load_witness()
    first_bytes, first_payload = _capture_main(witness)
    second_bytes, second_payload = _capture_main(witness)

    assert first_bytes == second_bytes
    assert first_payload == second_payload
    assert first_bytes.endswith(b"\n")
    assert first_bytes.count(b"\n") == 1
    assert b"\r" not in first_bytes
    assert list(first_payload) == [
        "control",
        "counterexample",
        "null_control",
        "raw_invariants",
    ]

    direct_passive = witness.direct_retained_law(CONTROL_DELTA)
    split_passive = witness.split_retained_law(CONTROL_A, CONTROL_B)
    null_passive = witness.null_extended_retained_law(
        CONTROL_A, CONTROL_B, CONTROL_ETA
    )
    mediator_responses = (
        witness.mediator_response(CONTROL_B, 0),
        witness.mediator_response(CONTROL_B, 1),
    )
    expected_control = {
        "direct_passive": direct_passive,
        "mediator_responses": mediator_responses,
        "mediator_total_variation": witness.binary_total_variation(
            *mediator_responses
        ),
        "null_passive": null_passive,
        "shared_boundary_laws": tuple(
            witness.shared_boundary_intervention_law("direct", context)
            for context in CONTROL_CONTEXTS
        ),
        "split_passive": split_passive,
    }

    noop_signature = witness.contextual_response_signature(
        "null", a=CONTROL_A, b=CONTROL_B, eta=CONTROL_ETA, context=()
    )
    do_n0_signature = witness.contextual_response_signature(
        "null", a=CONTROL_A, b=CONTROL_B, eta=CONTROL_ETA,
        context=(("N", 0),)
    )
    do_n1_signature = witness.contextual_response_signature(
        "null", a=CONTROL_A, b=CONTROL_B, eta=CONTROL_ETA,
        context=(("N", 1),)
    )
    split_experiment = witness.response_image(
        "split", a=CONTROL_A, b=CONTROL_B
    )
    null_experiment = witness.response_image(
        "null", a=CONTROL_A, b=CONTROL_B, eta=CONTROL_ETA
    )
    split_classes, split_multiplication, split_responses = split_experiment
    null_classes, null_multiplication, null_responses = null_experiment
    split_lookup = {
        context: class_index
        for class_index, behavioral_class in enumerate(split_classes)
        for context in behavioral_class
    }
    class_images = tuple(
        tuple(sorted({
            split_lookup[tuple(
                (node, bit) for node, bit in context if node != "N"
            )]
            for context in behavioral_class
        }))
        for behavioral_class in null_classes
    )
    assert all(len(image) == 1 for image in class_images)
    class_map = tuple(image[0] for image in class_images)
    assert class_map == tuple(range(15))
    multiplication_preserved = all(
        class_map[null_multiplication[left_index][right_index]]
        == split_multiplication[class_map[left_index]][class_map[right_index]]
        for left_index in range(len(null_classes))
        for right_index in range(len(null_classes))
    )
    assert multiplication_preserved
    assert null_responses == split_responses
    expected_null_control = {
        "do_n0_signature": do_n0_signature,
        "do_n1_signature": do_n1_signature,
        "forget_n_isomorphism": {
            "class_map": class_map,
            "identity_preserved": class_map[0] == 0,
            "multiplication_preserved": multiplication_preserved,
            "responses_preserved": null_responses == split_responses,
        },
        "noop_signature": noop_signature,
        "null_experiment": null_experiment,
        "split_experiment": split_experiment,
    }
    canonical = (
        json.dumps(
            first_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        )
        + "\n"
    ).encode("ascii")
    assert first_bytes == canonical
    _validate_json_tree(first_payload)
    assert first_payload["control"] == _json_ready(expected_control)
    assert first_payload["null_control"] == _json_ready(
        expected_null_control
    )
    assert first_payload["counterexample"] == _json_ready(
        witness.same_signature_counterexample()
    )
    assert first_payload["raw_invariants"] == _json_ready(
        RAW_PRESENTATION_INVARIANTS
    )


def test_fresh_process_json_and_lf_test_snapshot_are_byte_identical():
    witness = _load_witness()
    in_process, _ = _capture_main(witness)
    completed = subprocess.run(
        [sys.executable, str(WITNESS)],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert completed.returncode == 0
    assert completed.stderr == b""
    assert completed.stdout == in_process
    live_test = Path(__file__).read_bytes()
    snapshot = SNAPSHOT.read_bytes()
    assert live_test == snapshot
    assert b"\r" not in live_test
    assert live_test.endswith(b"\n")
