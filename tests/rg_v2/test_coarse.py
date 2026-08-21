from __future__ import annotations

from dataclasses import fields, replace
from fractions import Fraction
import hashlib
import inspect
import json
import math

import pytest

from multiagent_elbo.config import NumericsConfig
from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
from rg_v2 import coarse
from rg_v2.contracts import (
    AggregateDatum,
    CoarseChannelSpec,
    ExactProbabilityLaw,
    PopulationInference,
)
from rg_v2.fixtures import LocalFirstFixture, load_fixture
from rg_v2.population import construct_population_joint, derive_population_inference


NUMERICS = NumericsConfig(
    dtype="float64",
    atol=1.0e-12,
    rtol=1.0e-10,
    min_spd_rcond=1.0e-12,
    max_frame_condition=1.0e6,
)

PARITY_CHANNEL_SHA256 = "d34d5791ab365a22e3259729d935ea9e38be493f35e30d365dc9633948b8322e"
DIRAC_CHANNEL_SHA256 = "ad297ca272b5b7437276cadd8df32ce711fdca0600f40b5b39e868d6cbbc45e2"
PARITY_AGGREGATE_ID = "aggregate-8baf93a0c184059724fda2f9a0448634f3594b97e5e0000f8388a0d6e8a803c4"
DIRAC_AGGREGATE_ID = "aggregate-626f6923d5cc1dfa2750de7097ab5a0795ed6dc9c084db587492c58c9090416b"

PARITY_COARSE_JOINT = (
    (
        Fraction(9593, 80000),
        Fraction(4427, 80000),
        Fraction(173, 3200),
        Fraction(883, 16000),
        Fraction(191, 3200),
        Fraction(649, 16000),
        Fraction(4907, 80000),
        Fraction(4313, 80000),
    ),
    (
        Fraction(4313, 80000),
        Fraction(4907, 80000),
        Fraction(649, 16000),
        Fraction(191, 3200),
        Fraction(883, 16000),
        Fraction(173, 3200),
        Fraction(4427, 80000),
        Fraction(9593, 80000),
    ),
)


def _fixture_inference(fixture_id: str = "lf3_product_v1") -> tuple[LocalFirstFixture, PopulationInference]:
    fixture = load_fixture(fixture_id)  # type: ignore[arg-type]
    population = construct_population_joint(fixture.agents, fixture.records, fixture.context_id)
    inference = derive_population_inference(
        population,
        fixture.observation,
        fixture.recognitions,
        fixture.selector,
    )
    return fixture, inference


def _copy_channel(channel: ExactMarkovChannel) -> ExactMarkovChannel:
    return ExactMarkovChannel(
        channel.source_labels,
        channel.target_labels,
        channel.matrix,
        recognition_independent=channel.recognition_independent,
    )


def _copy_channel_spec(spec: CoarseChannelSpec) -> CoarseChannelSpec:
    return CoarseChannelSpec(
        channel_id=spec.channel_id,
        source_agent_ids=spec.source_agent_ids,
        structural_input_ids=spec.structural_input_ids,
        channel=_copy_channel(spec.channel),
    )


def _canonical_channel_sha256(channel: ExactMarkovChannel) -> str:
    body = {
        "source_labels": list(channel.source_labels),
        "target_labels": list(channel.target_labels),
        "matrix": [
            [
                {"numerator": value.numerator, "denominator": value.denominator}
                for value in row
            ]
            for row in channel.matrix
        ],
        "recognition_independent": channel.recognition_independent,
    }
    canonical = json.dumps(
        body,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _mutate_frozen(value: object, field: str, replacement: object) -> object:
    clone = replace(value)  # type: ignore[call-overload]
    object.__setattr__(clone, field, replacement)
    return clone


def test_public_signatures_and_aggregate_field_order_are_exact() -> None:
    assert tuple(inspect.signature(coarse.aggregate_population).parameters) == (
        "inference",
        "channel",
        "numerics",
    )
    assert tuple(inspect.signature(coarse.validate_aggregate_datum).parameters) == (
        "datum",
        "inference",
        "channel",
        "numerics",
    )
    assert tuple(field.name for field in fields(AggregateDatum)) == (
        "aggregate_id",
        "source_agent_ids",
        "observed_record",
        "channel_id",
        "channel_sha256",
        "observation_labels",
        "target_labels",
        "generative_joint",
        "recognition",
        "posterior",
        "evidence",
        "conditional_kl_defect",
        "kl_chain_residual",
    )


@pytest.mark.parametrize(
    ("fixture_id", "expected_defect", "expected_residual"),
    [
        ("lf3_product_v1", 1.596404090511296, 2.220446049250313e-16),
        ("lf3_correlated_v1", 2.2895512710712413, 0.0),
    ],
)
def test_parity_aggregate_matches_full_exact_and_float_oracles(
    fixture_id: str,
    expected_defect: float,
    expected_residual: float,
) -> None:
    fixture, inference = _fixture_inference(fixture_id)

    datum = coarse.aggregate_population(inference, fixture.coarse_channel, NUMERICS)

    assert datum.aggregate_id == PARITY_AGGREGATE_ID
    assert datum.source_agent_ids == ("a", "b", "c")
    assert datum.observed_record == '[["r_a","1"],["r_b","1"],["r_c","1"]]'
    assert datum.channel_id == "lf3-belief-parity-channel-v1"
    assert datum.channel_sha256 == PARITY_CHANNEL_SHA256
    assert datum.observation_labels == inference.population.observation_labels
    assert datum.target_labels == ("even", "odd")
    assert datum.generative_joint == PARITY_COARSE_JOINT
    assert sum((sum(row, Fraction(0)) for row in datum.generative_joint), Fraction(0)) == 1
    assert datum.recognition == ExactProbabilityLaw(("even", "odd"), (Fraction(1, 2), Fraction(1, 2)))
    assert datum.posterior == ExactProbabilityLaw(
        ("even", "odd"),
        (Fraction(4313, 13906), Fraction(9593, 13906)),
    )
    observed_index = datum.observation_labels.index(datum.observed_record)
    assert tuple(row[observed_index] for row in datum.generative_joint) == (
        Fraction(4313, 80000),
        Fraction(9593, 80000),
    )
    assert datum.evidence == inference.evidence == Fraction(6953, 40000)
    assert datum.conditional_kl_defect == expected_defect
    assert datum.kl_chain_residual == expected_residual
    assert datum.conditional_kl_defect >= -min(NUMERICS.atol, 1.0e-12)
    assert datum.kl_chain_residual <= min(NUMERICS.atol, 1.0e-12)
    coarse.validate_aggregate_datum(datum, inference, fixture.coarse_channel, NUMERICS)


def test_dirac_boundary_is_exactly_normalized_with_zero_diagnostics() -> None:
    fixture, inference = _fixture_inference("lf3_dirac_boundary_v1")

    datum = coarse.aggregate_population(inference, fixture.coarse_channel, NUMERICS)

    assert datum.aggregate_id == DIRAC_AGGREGATE_ID
    assert datum.channel_sha256 == DIRAC_CHANNEL_SHA256
    assert datum.generative_joint == ((Fraction(1),),)
    assert datum.recognition == ExactProbabilityLaw(("singleton",), (Fraction(1),))
    assert datum.posterior == ExactProbabilityLaw(("singleton",), (Fraction(1),))
    assert datum.evidence == 1
    assert datum.conditional_kl_defect == 0.0
    assert datum.kl_chain_residual == 0.0


def test_one_exact_channel_reference_reaches_all_three_execution_pushes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture, inference = _fixture_inference()
    captured: list[tuple[str, int]] = []

    for seam_name in ("_push_full_joint", "_push_recognition", "_push_posterior"):
        original = getattr(coarse, seam_name)

        def spy(*args: object, _name: str = seam_name, _original: object = original) -> object:
            channel = args[-1]
            captured.append((_name, id(channel)))
            return _original(*args)  # type: ignore[operator]

        monkeypatch.setattr(coarse, seam_name, spy)

    coarse.aggregate_population(inference, fixture.coarse_channel, NUMERICS)

    assert captured == [
        ("_push_full_joint", id(fixture.coarse_channel.channel)),
        ("_push_recognition", id(fixture.coarse_channel.channel)),
        ("_push_posterior", id(fixture.coarse_channel.channel)),
    ]


def test_equal_but_distinct_channel_on_one_execution_route_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture, inference = _fixture_inference()
    original = coarse._push_posterior
    split_channel = _copy_channel(fixture.coarse_channel.channel)
    assert split_channel == fixture.coarse_channel.channel
    assert split_channel is not fixture.coarse_channel.channel

    def split_route(source: PopulationInference, _: ExactMarkovChannel) -> object:
        return original(source, split_channel)

    monkeypatch.setattr(coarse, "_push_posterior", split_route)

    with pytest.raises(ValueError, match="same exact channel object"):
        coarse.aggregate_population(inference, fixture.coarse_channel, NUMERICS)


def test_replay_validation_accepts_equal_structural_channel_without_process_identity() -> None:
    fixture, inference = _fixture_inference()
    datum = coarse.aggregate_population(inference, fixture.coarse_channel, NUMERICS)
    reconstructed = _copy_channel_spec(fixture.coarse_channel)

    assert reconstructed.channel == fixture.coarse_channel.channel
    assert reconstructed.channel is not fixture.coarse_channel.channel
    coarse.validate_aggregate_datum(datum, inference, reconstructed, NUMERICS)


def test_channel_hash_is_canonical_and_excludes_declaration_metadata() -> None:
    fixture, inference = _fixture_inference()
    channel = fixture.coarse_channel
    alternate_metadata = CoarseChannelSpec(
        channel_id="alternate-channel-id",
        source_agent_ids=channel.source_agent_ids,
        structural_input_ids=("alternate-structural-input",),
        channel=_copy_channel(channel.channel),
    )

    assert coarse._channel_sha256(channel.channel) == _canonical_channel_sha256(channel.channel)
    assert coarse._channel_sha256(channel.channel) == PARITY_CHANNEL_SHA256
    assert coarse._channel_sha256(alternate_metadata.channel) == PARITY_CHANNEL_SHA256
    assert coarse._aggregate_id(inference, channel, PARITY_CHANNEL_SHA256) == PARITY_AGGREGATE_ID
    assert coarse._aggregate_id(inference, alternate_metadata, PARITY_CHANNEL_SHA256) != PARITY_AGGREGATE_ID


def test_aggregate_route_identity_excludes_selector_values_and_structural_metadata() -> None:
    product_fixture, product_inference = _fixture_inference("lf3_product_v1")
    correlated_fixture, correlated_inference = _fixture_inference("lf3_correlated_v1")
    structural_variant = replace(
        product_fixture.coarse_channel,
        structural_input_ids=("different-valid-structural-declaration",),
    )

    assert product_inference.recognition != correlated_inference.recognition
    assert coarse._aggregate_id(
        product_inference,
        product_fixture.coarse_channel,
        PARITY_CHANNEL_SHA256,
    ) == coarse._aggregate_id(
        correlated_inference,
        correlated_fixture.coarse_channel,
        PARITY_CHANNEL_SHA256,
    )
    assert coarse._aggregate_id(
        product_inference,
        structural_variant,
        PARITY_CHANNEL_SHA256,
    ) == PARITY_AGGREGATE_ID


@pytest.mark.parametrize(
    "mutation",
    [
        "channel_id",
        "source_agent_order",
        "channel_source_support",
        "channel_target_support",
        "channel_matrix_type",
        "channel_matrix_normalization",
        "empty_structural_id",
        "duplicate_structural_id",
        "observed_record_leak",
        "recognition_independence",
        "population_agent_order",
        "population_joint",
        "recognitions",
        "selected_recognition",
        "evidence_measure",
        "evidence",
        "posterior",
        "observed_record",
        "selector",
    ],
)
def test_mutated_inputs_are_rejected_before_any_push(
    mutation: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture, inference = _fixture_inference()
    channel = _copy_channel_spec(fixture.coarse_channel)
    bad_inference = replace(inference)
    bad_channel = channel
    bad_numerics = NUMERICS

    if mutation == "channel_id":
        object.__setattr__(bad_channel, "channel_id", "")
    elif mutation == "source_agent_order":
        object.__setattr__(bad_channel, "source_agent_ids", ("b", "a", "c"))
    elif mutation == "channel_source_support":
        object.__setattr__(bad_channel.channel, "source_labels", tuple(reversed(bad_channel.channel.source_labels)))
    elif mutation == "channel_target_support":
        object.__setattr__(bad_channel.channel, "target_labels", ("even", ""))
    elif mutation == "channel_matrix_type":
        object.__setattr__(
            bad_channel.channel,
            "matrix",
            tuple(tuple(value.numerator for value in row) for row in bad_channel.channel.matrix),
        )
    elif mutation == "channel_matrix_normalization":
        rows = list(bad_channel.channel.matrix)
        rows[0] = (Fraction(1), Fraction(1))
        object.__setattr__(bad_channel.channel, "matrix", tuple(rows))
    elif mutation == "empty_structural_id":
        object.__setattr__(bad_channel, "structural_input_ids", ("",))
    elif mutation == "duplicate_structural_id":
        object.__setattr__(bad_channel, "structural_input_ids", ("same", "same"))
    elif mutation == "observed_record_leak":
        object.__setattr__(bad_channel, "structural_input_ids", (inference.observed_record,))
    elif mutation == "recognition_independence":
        object.__setattr__(bad_channel.channel, "recognition_independent", False)
    elif mutation == "population_agent_order":
        population = _mutate_frozen(
            inference.population,
            "agent_order",
            tuple(reversed(inference.population.agent_order)),
        )
        object.__setattr__(bad_inference, "population", population)
    elif mutation == "population_joint":
        population = _mutate_frozen(
            inference.population,
            "joint_masses",
            inference.population.joint_masses[:-1],
        )
        object.__setattr__(bad_inference, "population", population)
    elif mutation == "recognitions":
        object.__setattr__(bad_inference, "recognitions", ("not-a-recognition",))
    elif mutation == "selected_recognition":
        object.__setattr__(
            bad_inference,
            "recognition",
            ExactProbabilityLaw(
                inference.recognition.labels,
                (Fraction(1),) + (Fraction(0),) * (len(inference.recognition.labels) - 1),
            ),
        )
    elif mutation == "evidence_measure":
        evidence_measure = _mutate_frozen(
            inference.evidence_measure,
            "masses",
            tuple(reversed(inference.evidence_measure.masses)),
        )
        object.__setattr__(bad_inference, "evidence_measure", evidence_measure)
    elif mutation == "evidence":
        object.__setattr__(bad_inference, "evidence", inference.evidence + Fraction(1, 1000))
    elif mutation == "posterior":
        object.__setattr__(
            bad_inference,
            "posterior",
            ExactProbabilityLaw(
                inference.posterior.labels,
                tuple(reversed(inference.posterior.masses)),
            ),
        )
    elif mutation == "observed_record":
        object.__setattr__(bad_inference, "observed_record", inference.population.observation_labels[0])
    elif mutation == "selector":
        selector = _mutate_frozen(inference.selector, "selector_id", "")
        object.__setattr__(bad_inference, "selector", selector)
    else:  # pragma: no cover - the parameter list is closed above
        raise AssertionError(mutation)

    reached: list[str] = []

    def fail_if_reached(*_: object) -> object:
        reached.append("push")
        raise AssertionError("a push was reached before input validation")

    monkeypatch.setattr(coarse, "_push_full_joint", fail_if_reached)
    monkeypatch.setattr(coarse, "_push_recognition", fail_if_reached)
    monkeypatch.setattr(coarse, "_push_posterior", fail_if_reached)

    with pytest.raises((TypeError, ValueError)):
        coarse.aggregate_population(bad_inference, bad_channel, bad_numerics)
    assert reached == []


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("dtype", "float32"),
        ("atol", 1.0e-9),
        ("atol", 0.0),
        ("atol", 1),
        ("rtol", 0.0),
        ("rtol", float("nan")),
        ("min_spd_rcond", 0.0),
        ("min_spd_rcond", 2.0),
        ("max_frame_condition", 0.5),
        ("max_frame_condition", float("inf")),
    ],
)
def test_invalid_numerics_are_rejected_before_any_push(
    field: str,
    replacement: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture, inference = _fixture_inference()
    numerics = _mutate_frozen(NUMERICS, field, replacement)
    reached: list[str] = []

    def fail_if_reached(*_: object) -> object:
        reached.append("push")
        raise AssertionError("a push was reached before numerics validation")

    monkeypatch.setattr(coarse, "_push_full_joint", fail_if_reached)
    monkeypatch.setattr(coarse, "_push_recognition", fail_if_reached)
    monkeypatch.setattr(coarse, "_push_posterior", fail_if_reached)

    with pytest.raises((TypeError, ValueError)):
        coarse.aggregate_population(inference, fixture.coarse_channel, numerics)  # type: ignore[arg-type]
    assert reached == []


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("aggregate_id", "aggregate-wrong"),
        ("source_agent_ids", ("c", "b", "a")),
        ("observed_record", '[["r_a","0"],["r_b","0"],["r_c","0"]]'),
        ("channel_id", "wrong-channel"),
        ("channel_sha256", "0" * 64),
        ("observation_labels", None),
        ("target_labels", ("odd", "even")),
        ("generative_joint", tuple(reversed(PARITY_COARSE_JOINT))),
        ("recognition", ExactProbabilityLaw(("even", "odd"), (Fraction(3, 4), Fraction(1, 4)))),
        ("posterior", ExactProbabilityLaw(("even", "odd"), (Fraction(1, 2), Fraction(1, 2)))),
        ("evidence", Fraction(1, 2)),
        ("conditional_kl_defect", 1.0),
        ("conditional_kl_defect", float("inf")),
        ("kl_chain_residual", 1.0e-6),
        ("kl_chain_residual", -1.0e-6),
    ],
)
def test_replay_validator_rejects_mutated_aggregate_fields(
    field: str,
    replacement: object,
) -> None:
    fixture, inference = _fixture_inference()
    datum = coarse.aggregate_population(inference, fixture.coarse_channel, NUMERICS)
    if field == "observation_labels":
        replacement = tuple(reversed(datum.observation_labels))
    mutated = _mutate_frozen(datum, field, replacement)

    with pytest.raises((TypeError, ValueError)):
        coarse.validate_aggregate_datum(
            mutated,  # type: ignore[arg-type]
            inference,
            fixture.coarse_channel,
            NUMERICS,
        )


def test_validator_recomputes_hash_route_and_vfe_diagnostics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture, inference = _fixture_inference()
    datum = coarse.aggregate_population(inference, fixture.coarse_channel, NUMERICS)
    calls: list[tuple[int, int]] = []
    original = coarse._vfe_diagnostics

    def spy(
        source: PopulationInference,
        channel: ExactMarkovChannel,
        numerics: NumericsConfig,
    ) -> tuple[float, float]:
        calls.append((id(channel), id(numerics)))
        return original(source, channel, numerics)

    monkeypatch.setattr(coarse, "_vfe_diagnostics", spy)

    coarse.validate_aggregate_datum(datum, inference, fixture.coarse_channel, NUMERICS)

    assert calls == [(id(fixture.coarse_channel.channel), id(NUMERICS))]
    assert math.isfinite(datum.conditional_kl_defect)
    assert math.isfinite(datum.kl_chain_residual)
