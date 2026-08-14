"""Exact finite typed-intervention witness over binary state spaces.

This module implements the executable controls frozen by the approved design.
It uses only exact rational arithmetic.  The computations corroborate the
finite constructions; the direct derivations, not this program, carry the
mathematical proof.
"""

from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction
from functools import lru_cache


Context = tuple[tuple[str, int], ...]
BinaryLaw = tuple[Fraction, Fraction]
RetainedLaw = tuple[Fraction, Fraction, Fraction, Fraction]
ReducedExperiment = tuple[tuple[tuple[Context, ...], ...], tuple[tuple[int, ...], ...], tuple[RetainedLaw, ...]]

_NODE_ORDER = ("R", "E", "N", "O")
_NODE_RANK = {node: index for index, node in enumerate(_NODE_ORDER)}
_MODEL_NODES = {
    "direct": ("R", "O"),
    "split": ("R", "E", "O"),
    "null": ("R", "E", "N", "O"),
}
_CONTROL_A = Fraction(1, 10)
_CONTROL_B = Fraction(1, 8)
_CONTROL_ETA = Fraction(2, 5)
_LEFT_A = Fraction(1, 4)
_LEFT_B = Fraction(1, 3)
_RIGHT_A = Fraction(1, 3)
_RIGHT_B = Fraction(1, 4)
_CONTROL_CONTEXTS = (
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


def _probability(value: object, name: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise ValueError(f"{name} must be an exact rational probability")
    result = Fraction(value)
    if result < 0 or result > 1:
        raise ValueError(f"{name} must lie in [0,1]")
    return result


def _bit(value: object, name: str) -> int:
    if isinstance(value, bool) or type(value) is not int or value not in (0, 1):
        raise ValueError(f"{name} must be the integer 0 or 1")
    return value


def _model_nodes(model: object) -> tuple[str, ...]:
    if type(model) is not str or model not in _MODEL_NODES:
        raise ValueError("model must be 'direct', 'split', or 'null'")
    return _MODEL_NODES[model]


def _normalize_context(raw: object, allowed_nodes: tuple[str, ...] = _NODE_ORDER) -> Context:
    if isinstance(raw, (str, bytes)):
        raise ValueError("context must be a finite sequence of assignments")
    try:
        assignments = tuple(raw)  # type: ignore[arg-type]
    except TypeError as error:
        raise ValueError("context must be a finite sequence of assignments") from error

    allowed = set(allowed_nodes)
    normalized: list[tuple[str, int]] = []
    seen: set[str] = set()
    for assignment in assignments:
        if not isinstance(assignment, (tuple, list)) or len(assignment) != 2:
            raise ValueError("every context assignment must be a node-bit pair")
        node, value = assignment
        if type(node) is not str or node not in _NODE_RANK:
            raise ValueError("context contains an unknown node")
        if node not in allowed:
            raise ValueError("context names a node absent from the presentation")
        if node in seen:
            raise ValueError("context contains a duplicate node assignment")
        normalized.append((node, _bit(value, f"assignment for {node}")))
        seen.add(node)
    return tuple(sorted(normalized, key=lambda item: _NODE_RANK[item[0]]))


def _compose_canonical(left: Context, right: Context) -> Context:
    assignments = dict(left)
    assignments.update(right)
    return tuple(
        (node, assignments[node])
        for node in _NODE_ORDER
        if node in assignments
    )


def _all_contexts(nodes: tuple[str, ...]) -> tuple[Context, ...]:
    return tuple(
        tuple(
            (node, value)
            for node, value in zip(nodes, values)
            if value is not None
        )
        for values in itertools.product((None, 0, 1), repeat=len(nodes))
    )


def _point_probability(observed: int, assigned: int) -> Fraction:
    return Fraction(int(observed == assigned))


def bsc(epsilon, output_bit, input_bit) -> Fraction:
    epsilon_value = _probability(epsilon, "epsilon")
    output = _bit(output_bit, "output_bit")
    input_value = _bit(input_bit, "input_bit")
    return Fraction(1) - epsilon_value if output == input_value else epsilon_value


def compose_bsc(a, b) -> Fraction:
    a_value = _probability(a, "a")
    b_value = _probability(b, "b")
    return a_value + b_value - 2 * a_value * b_value


def compose_context(left, right) -> Context:
    left_context = _normalize_context(left)
    right_context = _normalize_context(right)
    return _compose_canonical(left_context, right_context)


@lru_cache(maxsize=None)
def _direct_retained_law_cached(delta: Fraction, context: Context) -> RetainedLaw:
    assignments = dict(context)
    atoms: list[Fraction] = []
    for retained, output in itertools.product((0, 1), repeat=2):
        retained_factor = (
            _point_probability(retained, assignments["R"])
            if "R" in assignments
            else Fraction(1, 2)
        )
        output_factor = (
            _point_probability(output, assignments["O"])
            if "O" in assignments
            else bsc(delta, output, retained)
        )
        atoms.append(retained_factor * output_factor)
    return tuple(atoms)  # type: ignore[return-value]


def direct_retained_law(delta, context=()) -> RetainedLaw:
    delta_value = _probability(delta, "delta")
    canonical = _normalize_context(context, _MODEL_NODES["direct"])
    return _direct_retained_law_cached(delta_value, canonical)


@lru_cache(maxsize=None)
def _split_joint_law_cached(a: Fraction, b: Fraction, context: Context) -> tuple[Fraction, ...]:
    assignments = dict(context)
    atoms: list[Fraction] = []
    for retained, mediator, output in itertools.product((0, 1), repeat=3):
        retained_factor = (
            _point_probability(retained, assignments["R"])
            if "R" in assignments
            else Fraction(1, 2)
        )
        mediator_factor = (
            _point_probability(mediator, assignments["E"])
            if "E" in assignments
            else bsc(a, mediator, retained)
        )
        output_factor = (
            _point_probability(output, assignments["O"])
            if "O" in assignments
            else bsc(b, output, mediator)
        )
        atoms.append(retained_factor * mediator_factor * output_factor)
    return tuple(atoms)


def split_joint_law(a, b, context=()) -> tuple[Fraction, ...]:
    a_value = _probability(a, "a")
    b_value = _probability(b, "b")
    canonical = _normalize_context(context, _MODEL_NODES["split"])
    return _split_joint_law_cached(a_value, b_value, canonical)


@lru_cache(maxsize=None)
def _split_retained_law_cached(a: Fraction, b: Fraction, context: Context) -> RetainedLaw:
    joint = _split_joint_law_cached(a, b, context)
    atoms = []
    for retained, output in itertools.product((0, 1), repeat=2):
        atoms.append(
            sum(
                (
                    joint[retained * 4 + mediator * 2 + output]
                    for mediator in (0, 1)
                ),
                Fraction(0),
            )
        )
    return tuple(atoms)  # type: ignore[return-value]


def split_retained_law(a, b, context=()) -> RetainedLaw:
    a_value = _probability(a, "a")
    b_value = _probability(b, "b")
    canonical = _normalize_context(context, _MODEL_NODES["split"])
    return _split_retained_law_cached(a_value, b_value, canonical)


@lru_cache(maxsize=None)
def _null_extended_joint_law_cached(
    a: Fraction, b: Fraction, eta: Fraction, context: Context
) -> tuple[Fraction, ...]:
    assignments = dict(context)
    atoms: list[Fraction] = []
    for retained, mediator, null, output in itertools.product((0, 1), repeat=4):
        retained_factor = (
            _point_probability(retained, assignments["R"])
            if "R" in assignments
            else Fraction(1, 2)
        )
        mediator_factor = (
            _point_probability(mediator, assignments["E"])
            if "E" in assignments
            else bsc(a, mediator, retained)
        )
        null_factor = (
            _point_probability(null, assignments["N"])
            if "N" in assignments
            else (eta if null else Fraction(1) - eta)
        )
        output_factor = (
            _point_probability(output, assignments["O"])
            if "O" in assignments
            else bsc(b, output, mediator)
        )
        atoms.append(
            retained_factor * mediator_factor * null_factor * output_factor
        )
    return tuple(atoms)


def null_extended_joint_law(a, b, eta, context=()) -> tuple[Fraction, ...]:
    a_value = _probability(a, "a")
    b_value = _probability(b, "b")
    eta_value = _probability(eta, "eta")
    canonical = _normalize_context(context, _MODEL_NODES["null"])
    return _null_extended_joint_law_cached(a_value, b_value, eta_value, canonical)


@lru_cache(maxsize=None)
def _null_extended_retained_law_cached(
    a: Fraction, b: Fraction, eta: Fraction, context: Context
) -> RetainedLaw:
    joint = _null_extended_joint_law_cached(a, b, eta, context)
    atoms = []
    for retained, output in itertools.product((0, 1), repeat=2):
        atoms.append(
            sum(
                (
                    joint[retained * 8 + mediator * 4 + null * 2 + output]
                    for mediator, null in itertools.product((0, 1), repeat=2)
                ),
                Fraction(0),
            )
        )
    return tuple(atoms)  # type: ignore[return-value]


def null_extended_retained_law(a, b, eta, context=()) -> RetainedLaw:
    a_value = _probability(a, "a")
    b_value = _probability(b, "b")
    eta_value = _probability(eta, "eta")
    canonical = _normalize_context(context, _MODEL_NODES["null"])
    return _null_extended_retained_law_cached(a_value, b_value, eta_value, canonical)


def _prepared_parameters(model: str, a: object, b: object, eta: object) -> tuple[Fraction, Fraction, Fraction | None]:
    _model_nodes(model)
    a_value = _probability(a, "a")
    b_value = _probability(b, "b")
    if model == "null":
        if eta is None:
            raise ValueError("eta is required for the null presentation")
        eta_value: Fraction | None = _probability(eta, "eta")
    else:
        if eta is not None:
            _probability(eta, "eta")
        eta_value = None
    return a_value, b_value, eta_value


@lru_cache(maxsize=None)
def _intervention_response_cached(
    model: str,
    a: Fraction,
    b: Fraction,
    eta: Fraction | None,
    context: Context,
) -> RetainedLaw:
    if model == "direct":
        return _direct_retained_law_cached(compose_bsc(a, b), context)
    if model == "split":
        return _split_retained_law_cached(a, b, context)
    assert eta is not None
    return _null_extended_retained_law_cached(a, b, eta, context)


def intervention_response(model, *, a, b, eta=None, context=()) -> RetainedLaw:
    nodes = _model_nodes(model)
    a_value, b_value, eta_value = _prepared_parameters(model, a, b, eta)
    canonical = _normalize_context(context, nodes)
    return _intervention_response_cached(
        model, a_value, b_value, eta_value, canonical
    )


def shared_boundary_intervention_law(model, context=()) -> RetainedLaw:
    nodes = _model_nodes(model)
    canonical = _normalize_context(context, nodes)
    return _intervention_response_cached(
        model,
        _CONTROL_A,
        _CONTROL_B,
        _CONTROL_ETA if model == "null" else None,
        canonical,
    )


def mediator_response(b, mediator_bit) -> BinaryLaw:
    b_value = _probability(b, "b")
    bit = _bit(mediator_bit, "mediator_bit")
    return (bsc(b_value, 0, bit), bsc(b_value, 1, bit))


def binary_total_variation(left, right) -> Fraction:
    if type(left) is not tuple or type(right) is not tuple:
        raise ValueError("binary laws must be tuples")
    if len(left) != 2 or len(right) != 2:
        raise ValueError("binary laws must contain exactly two atoms")
    left_law = tuple(_probability(atom, "left atom") for atom in left)
    right_law = tuple(_probability(atom, "right atom") for atom in right)
    if sum(left_law, Fraction(0)) != 1 or sum(right_law, Fraction(0)) != 1:
        raise ValueError("binary laws must be normalized")
    return sum(
        (abs(left_atom - right_atom) for left_atom, right_atom in zip(left_law, right_law)),
        Fraction(0),
    ) / 2


@lru_cache(maxsize=None)
def _contextual_response_signature_cached(
    model: str,
    a: Fraction,
    b: Fraction,
    eta: Fraction | None,
    context: Context,
) -> tuple[RetainedLaw, ...]:
    contexts = _all_contexts(_MODEL_NODES[model])
    responses: list[RetainedLaw] = []
    for left in contexts:
        for right in contexts:
            composed = _compose_canonical(
                _compose_canonical(left, context), right
            )
            responses.append(
                _intervention_response_cached(model, a, b, eta, composed)
            )
    return tuple(responses)


def contextual_response_signature(model, *, a, b, eta=None, context=()) -> tuple:
    nodes = _model_nodes(model)
    a_value, b_value, eta_value = _prepared_parameters(model, a, b, eta)
    canonical = _normalize_context(context, nodes)
    return _contextual_response_signature_cached(
        model, a_value, b_value, eta_value, canonical
    )


@lru_cache(maxsize=None)
def _response_image_cached(
    model: str, a: Fraction, b: Fraction, eta: Fraction | None
) -> ReducedExperiment:
    contexts = _all_contexts(_MODEL_NODES[model])
    signature_to_class: dict[tuple[RetainedLaw, ...], list[Context]] = {}
    for context in contexts:
        signature = _contextual_response_signature_cached(
            model, a, b, eta, context
        )
        signature_to_class.setdefault(signature, []).append(context)

    classes = tuple(
        tuple(members) for members in signature_to_class.values()
    )
    context_to_class = {
        context: class_index
        for class_index, behavioral_class in enumerate(classes)
        for context in behavioral_class
    }

    def quotient_product(
        left_class: tuple[Context, ...], right_class: tuple[Context, ...]
    ) -> int:
        product_classes = {
            context_to_class[_compose_canonical(left, right)]
            for left in left_class
            for right in right_class
        }
        if len(product_classes) != 1:
            raise RuntimeError("behavioral classes do not define a quotient monoid")
        return product_classes.pop()

    multiplication = tuple(
        tuple(
            quotient_product(left_class, right_class)
            for right_class in classes
        )
        for left_class in classes
    )
    representatives = tuple(
        behavioral_class[0] for behavioral_class in classes
    )
    responses = tuple(
        _intervention_response_cached(model, a, b, eta, representative)
        for representative in representatives
    )
    return classes, multiplication, responses


def response_image(model, *, a, b, eta=None) -> ReducedExperiment:
    _model_nodes(model)
    a_value, b_value, eta_value = _prepared_parameters(model, a, b, eta)
    return _response_image_cached(model, a_value, b_value, eta_value)


def _relabel_retained(
    law: RetainedLaw, flip_retained: int, flip_output: int
) -> RetainedLaw:
    return tuple(
        law[(retained ^ flip_retained) * 2 + (output ^ flip_output)]
        for retained, output in itertools.product((0, 1), repeat=2)
    )  # type: ignore[return-value]


def same_signature_counterexample() -> dict:
    left_experiment = response_image("split", a=_LEFT_A, b=_LEFT_B)
    right_experiment = response_image("split", a=_RIGHT_A, b=_RIGHT_B)
    left_passive = split_retained_law(_LEFT_A, _LEFT_B)
    right_passive = split_retained_law(_RIGHT_A, _RIGHT_B)
    left_responses = set(left_experiment[2])
    right_responses = right_experiment[2]
    transformed_right_images = tuple(
        {
            _relabel_retained(response, flip_retained, flip_output)
            for response in right_responses
        }
        for flip_retained, flip_output in itertools.product((0, 1), repeat=2)
    )
    boundary_match_exists = any(
        left_responses == transformed for transformed in transformed_right_images
    )
    unmatched_indices = tuple(
        index
        for index, response in enumerate(left_experiment[2])
        if all(response not in transformed for transformed in transformed_right_images)
    )
    certificate_indices = tuple(
        index
        for index in unmatched_indices
        if (("E", 0),) in left_experiment[0][index]
    )
    if len(certificate_indices) != 1:
        raise RuntimeError("do(E=0) does not select one unmatched response class")
    left_unmatched_response = left_experiment[2][certificate_indices[0]]
    return {
        "passive_equal": left_passive == right_passive,
        "passive_law": left_passive,
        "left_experiment": left_experiment,
        "right_experiment": right_experiment,
        "left_unmatched_response": left_unmatched_response,
        "boundary_match_exists": boundary_match_exists,
        "diagnostic_tv": (
            binary_total_variation(
                mediator_response(_LEFT_B, 0), mediator_response(_LEFT_B, 1)
            ),
            binary_total_variation(
                mediator_response(_RIGHT_B, 0), mediator_response(_RIGHT_B, 1)
            ),
        ),
        "raw_invariants_equal": (
            raw_presentation_invariants("split")
            == raw_presentation_invariants("split")
        ),
    }


def raw_presentation_invariants(model) -> dict:
    _model_nodes(model)
    if model == "direct":
        return {
            "roles": ("retained-state", "record"),
            "cardinalities": (2, 2),
            "edges": (("R", "O"),),
            "auxiliary_target": (),
        }
    if model == "split":
        return {
            "roles": ("retained-state", "mediator", "record"),
            "cardinalities": (2, 2, 2),
            "edges": (("R", "E"), ("E", "O")),
            "auxiliary_target": ("E",),
        }
    return {
        "roles": ("retained-state", "mediator", "null", "record"),
        "cardinalities": (2, 2, 2, 2),
        "edges": (("R", "E"), ("E", "O")),
        "auxiliary_target": ("E", "N"),
    }


def _json_ready(value: object) -> object:
    if isinstance(value, bool):
        return value
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, dict):
        return {
            key: _json_ready(item)
            for key, item in sorted(value.items())
        }
    if isinstance(value, (tuple, list)):
        return [_json_ready(item) for item in value]
    return value


def main() -> int:
    direct_passive = direct_retained_law(compose_bsc(_CONTROL_A, _CONTROL_B))
    split_passive = split_retained_law(_CONTROL_A, _CONTROL_B)
    null_passive = null_extended_retained_law(
        _CONTROL_A, _CONTROL_B, _CONTROL_ETA
    )
    mediator_responses = (
        mediator_response(_CONTROL_B, 0),
        mediator_response(_CONTROL_B, 1),
    )
    control = {
        "direct_passive": direct_passive,
        "mediator_responses": mediator_responses,
        "mediator_total_variation": binary_total_variation(*mediator_responses),
        "null_passive": null_passive,
        "shared_boundary_laws": tuple(
            shared_boundary_intervention_law("direct", context)
            for context in _CONTROL_CONTEXTS
        ),
        "split_passive": split_passive,
    }

    noop_signature = contextual_response_signature(
        "null", a=_CONTROL_A, b=_CONTROL_B, eta=_CONTROL_ETA, context=()
    )
    do_n0_signature = contextual_response_signature(
        "null",
        a=_CONTROL_A,
        b=_CONTROL_B,
        eta=_CONTROL_ETA,
        context=(("N", 0),),
    )
    do_n1_signature = contextual_response_signature(
        "null",
        a=_CONTROL_A,
        b=_CONTROL_B,
        eta=_CONTROL_ETA,
        context=(("N", 1),),
    )
    split_experiment = response_image("split", a=_CONTROL_A, b=_CONTROL_B)
    null_experiment = response_image(
        "null", a=_CONTROL_A, b=_CONTROL_B, eta=_CONTROL_ETA
    )
    split_classes, split_multiplication, split_responses = split_experiment
    null_classes, null_multiplication, null_responses = null_experiment
    split_lookup = {
        context: class_index
        for class_index, behavioral_class in enumerate(split_classes)
        for context in behavioral_class
    }
    class_images = tuple(
        tuple(
            sorted(
                {
                    split_lookup[
                        tuple(
                            (node, bit)
                            for node, bit in context
                            if node != "N"
                        )
                    ]
                    for context in behavioral_class
                }
            )
        )
        for behavioral_class in null_classes
    )
    if any(len(image) != 1 for image in class_images):
        raise RuntimeError("forgetting N is not well-defined on reduced classes")
    class_map = tuple(image[0] for image in class_images)
    multiplication_preserved = all(
        class_map[null_multiplication[left_index][right_index]]
        == split_multiplication[class_map[left_index]][class_map[right_index]]
        for left_index in range(len(null_classes))
        for right_index in range(len(null_classes))
    )
    null_control = {
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
    payload = _json_ready(
        {
            "control": control,
            "counterexample": same_signature_counterexample(),
            "null_control": null_control,
            "raw_invariants": {
                "direct": raw_presentation_invariants("direct"),
                "null": raw_presentation_invariants("null"),
                "split": raw_presentation_invariants("split"),
            },
        }
    )
    output = (
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    )
    binary_stdout = getattr(sys.stdout, "buffer", None)
    if binary_stdout is None:
        sys.stdout.write(output)
    else:
        binary_stdout.write(output.encode("ascii"))
        binary_stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
