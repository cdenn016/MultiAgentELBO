"""Exact common-channel aggregation for the local-first v2 laboratory."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import math

from multiagent_elbo.config import NumericsConfig
from multiagent_elbo.finite.measures import (
    FiniteMeasure,
    MarkovKernel,
    MeasurePair,
    ProbabilityMeasure,
)
from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
from multiagent_elbo.finite.vfe import vfe_channel_decomposition
from rg_v2.contracts import (
    AggregateDatum,
    CoarseChannelSpec,
    ExactProbabilityLaw,
    ExactSubmeasure,
    PopulationInference,
    PopulationJoint,
)
from rg_v2.population import _select_recognition


def _require_identifier(value: str, *, field: str) -> None:
    if type(value) is not str or not value or value.strip() != value:
        raise ValueError(f"{field} must be a nonempty string without surrounding whitespace")


def _require_identifier_tuple(
    values: tuple[str, ...],
    *,
    field: str,
) -> None:
    if type(values) is not tuple or not values:
        raise ValueError(f"{field} must be a nonempty tuple")
    for value in values:
        _require_identifier(value, field=field)
    if len(set(values)) != len(values):
        raise ValueError(f"{field} must not contain duplicates")


def _validate_numerics(numerics: NumericsConfig) -> None:
    if not isinstance(numerics, NumericsConfig):
        raise TypeError("numerics must be a NumericsConfig")
    if numerics.dtype != "float64":
        raise ValueError("coarse aggregation requires float64 numerics")
    for field, value in (("atol", numerics.atol), ("rtol", numerics.rtol)):
        if type(value) is not float or not math.isfinite(value) or value <= 0.0:
            raise ValueError(f"numerics.{field} must be a positive finite built-in float")
    if numerics.atol > 1.0e-12:
        raise ValueError("numerics.atol must be at most 1e-12")
    if (
        type(numerics.min_spd_rcond) is not float
        or not math.isfinite(numerics.min_spd_rcond)
        or not 0.0 < numerics.min_spd_rcond <= 1.0
    ):
        raise ValueError("numerics.min_spd_rcond must be a finite built-in float in (0, 1]")
    if (
        type(numerics.max_frame_condition) is not float
        or not math.isfinite(numerics.max_frame_condition)
        or numerics.max_frame_condition < 1.0
    ):
        raise ValueError("numerics.max_frame_condition must be a finite built-in float at least 1")


def _validate_probability_law(
    law: ExactProbabilityLaw,
    labels: tuple[str, ...],
    *,
    field: str,
) -> None:
    if not isinstance(law, ExactProbabilityLaw):
        raise TypeError(f"{field} must be an ExactProbabilityLaw")
    rebuilt = ExactProbabilityLaw(law.labels, law.masses)
    if rebuilt.labels != labels:
        raise ValueError(f"{field} labels must equal the fine latent support")


def _validate_submeasure(
    measure: ExactSubmeasure,
    labels: tuple[str, ...],
) -> None:
    if not isinstance(measure, ExactSubmeasure):
        raise TypeError("evidence measure must be an ExactSubmeasure")
    rebuilt = ExactSubmeasure(measure.labels, measure.masses)
    if rebuilt.labels != labels:
        raise ValueError("evidence measure labels must equal the fine latent support")


def _validate_population(population: PopulationJoint) -> None:
    if not isinstance(population, PopulationJoint):
        raise TypeError("inference.population must be a PopulationJoint")
    PopulationJoint(
        context_id=population.context_id,
        agent_order=population.agent_order,
        record_order=population.record_order,
        latent_labels=population.latent_labels,
        observation_labels=population.observation_labels,
        joint_masses=population.joint_masses,
        construction_trace=population.construction_trace,
    )


def _validate_inference(inference: PopulationInference) -> None:
    """Recompute every stored fine inference field before any coarse push."""
    if not isinstance(inference, PopulationInference):
        raise TypeError("inference must be a PopulationInference")
    population = inference.population
    _validate_population(population)
    if type(inference.recognitions) is not tuple:
        raise TypeError("inference recognitions must be a tuple")
    try:
        selected = _select_recognition(inference.recognitions, inference.selector)
    except KeyError as error:
        raise ValueError("inference recognition metadata is inconsistent") from error
    if tuple(item.agent_id for item in inference.recognitions) != population.agent_order:
        raise ValueError("inference recognition order must equal the population agent order")
    _validate_probability_law(inference.recognition, population.latent_labels, field="selected recognition")
    if inference.recognition != selected:
        raise ValueError("stored recognition must equal selection from retained local data")
    if type(inference.observed_record) is not str or inference.observed_record not in population.observation_labels:
        raise ValueError("observed record must belong to the population observation support")

    observed_index = population.observation_labels.index(inference.observed_record)
    expected_evidence_measure = ExactSubmeasure(
        population.latent_labels,
        tuple(row[observed_index] for row in population.joint_masses),
    )
    _validate_submeasure(inference.evidence_measure, population.latent_labels)
    if inference.evidence_measure != expected_evidence_measure:
        raise ValueError("stored evidence measure must equal the observed population slice")
    if type(inference.evidence) is not Fraction or inference.evidence <= 0:
        raise ValueError("inference evidence must be a positive exact Fraction")
    if inference.evidence != sum(expected_evidence_measure.masses, Fraction(0)):
        raise ValueError("stored evidence must equal the exact observed-slice total")

    expected_posterior = ExactProbabilityLaw(
        population.latent_labels,
        tuple(value / inference.evidence for value in expected_evidence_measure.masses),
    )
    _validate_probability_law(inference.posterior, population.latent_labels, field="posterior")
    if inference.posterior != expected_posterior:
        raise ValueError("stored posterior must be derived from the observed population slice")


def _has_observation_leak(identifier: str, inference: PopulationInference) -> bool:
    """Detect explicit observation provenance without interpreting opaque IDs."""
    lowered = identifier.casefold()
    return (
        identifier in inference.population.observation_labels
        or inference.observed_record in identifier
        or "observed_record" in lowered
        or "observed-record" in lowered
        or lowered.startswith("observation:")
        or lowered.startswith("observation=")
    )


def _validate_channel_spec(
    channel: CoarseChannelSpec,
    inference: PopulationInference,
) -> None:
    if not isinstance(channel, CoarseChannelSpec):
        raise TypeError("channel must be a CoarseChannelSpec")
    _require_identifier(channel.channel_id, field="channel ID")
    _require_identifier_tuple(channel.source_agent_ids, field="source agent IDs")
    _require_identifier_tuple(channel.structural_input_ids, field="structural input IDs")
    if channel.source_agent_ids != inference.population.agent_order:
        raise ValueError("coarse source-agent order must equal the population agent order")
    if any(_has_observation_leak(identifier, inference) for identifier in channel.structural_input_ids):
        raise ValueError("coarse structural inputs must not declare the realized observation")

    exact_channel = channel.channel
    if not isinstance(exact_channel, ExactMarkovChannel):
        raise TypeError("coarse channel must wrap an ExactMarkovChannel")
    if type(exact_channel.source_labels) is not tuple:
        raise ValueError("coarse channel source labels must be a tuple")
    _require_identifier_tuple(exact_channel.target_labels, field="coarse channel target labels")
    if type(exact_channel.matrix) is not tuple or len(exact_channel.matrix) != len(exact_channel.source_labels):
        raise ValueError("coarse channel rows must align with its source labels")
    for row in exact_channel.matrix:
        if type(row) is not tuple or len(row) != len(exact_channel.target_labels):
            raise ValueError("coarse channel columns must align with its target labels")
        if any(not isinstance(value, Fraction) for value in row):
            raise TypeError("coarse channel entries must be exact Fraction values")
        if any(value < 0 for value in row) or sum(row, Fraction(0)) != 1:
            raise ValueError("coarse channel rows must be nonnegative and normalized exactly")
    if exact_channel.recognition_independent is not True:
        raise ValueError("coarse channel must be recognition-independent")
    rebuilt = ExactMarkovChannel(
        exact_channel.source_labels,
        exact_channel.target_labels,
        exact_channel.matrix,
        recognition_independent=exact_channel.recognition_independent,
    )
    if (
        exact_channel.source_labels != rebuilt.source_labels
        or exact_channel.target_labels != rebuilt.target_labels
        or exact_channel.matrix != rebuilt.matrix
    ):
        raise ValueError("coarse channel fields must retain exact immutable representations")
    if rebuilt.source_labels != inference.population.latent_labels:
        raise ValueError("coarse channel source support must equal the population latent support")


def _validate_inputs(
    inference: PopulationInference,
    channel: CoarseChannelSpec,
    numerics: NumericsConfig,
) -> None:
    _validate_numerics(numerics)
    _validate_inference(inference)
    _validate_channel_spec(channel, inference)


def _channel_sha256(channel: ExactMarkovChannel) -> str:
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


def _aggregate_id(
    inference: PopulationInference,
    channel: CoarseChannelSpec,
    channel_sha256: str,
) -> str:
    """Return the prescribed route identity, which is not a content hash."""
    identity = {
        "context_id": inference.population.context_id,
        "source_agent_ids": list(channel.source_agent_ids),
        "observed_record": inference.observed_record,
        "channel_id": channel.channel_id,
        "channel_sha256": channel_sha256,
    }
    canonical = json.dumps(
        identity,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return "aggregate-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _push_joint_values(
    inference: PopulationInference,
    channel: ExactMarkovChannel,
) -> tuple[tuple[Fraction, ...], ...]:
    r"""Compute ``P_A(z,o) = sum_y P_V(y,o) C_A(y,z)`` exactly."""
    population = inference.population
    return tuple(
        tuple(
            sum(
                (
                    population.joint_masses[source_index][observation_index]
                    * channel.matrix[source_index][target_index]
                    for source_index in range(len(channel.source_labels))
                ),
                Fraction(0),
            )
            for observation_index in range(len(population.observation_labels))
        )
        for target_index in range(len(channel.target_labels))
    )


def _push_law_values(
    law: ExactProbabilityLaw,
    channel: ExactMarkovChannel,
) -> ExactProbabilityLaw:
    r"""Compute ``(mu C_A)(z) = sum_y mu(y) C_A(y,z)`` exactly."""
    return ExactProbabilityLaw(channel.target_labels, channel.pushforward(law.masses))


def _push_full_joint(
    inference: PopulationInference,
    channel: ExactMarkovChannel,
) -> tuple[tuple[tuple[Fraction, ...], ...], ExactMarkovChannel]:
    """Push the complete joint and retain the actual execution channel."""
    return _push_joint_values(inference, channel), channel


def _push_recognition(
    inference: PopulationInference,
    channel: ExactMarkovChannel,
) -> tuple[ExactProbabilityLaw, ExactMarkovChannel]:
    """Push the selected recognition and retain the actual channel."""
    return _push_law_values(inference.recognition, channel), channel


def _push_posterior(
    inference: PopulationInference,
    channel: ExactMarkovChannel,
) -> tuple[ExactProbabilityLaw, ExactMarkovChannel]:
    """Push the evidence-derived posterior and retain the actual channel."""
    return _push_law_values(inference.posterior, channel), channel


def _vfe_diagnostics(
    inference: PopulationInference,
    channel: ExactMarkovChannel,
    numerics: NumericsConfig,
) -> tuple[float, float]:
    fine_p_v = ProbabilityMeasure(
        inference.population.latent_labels,
        [float(sum(row, Fraction(0))) for row in inference.population.joint_masses],
        numerics,
    )
    fine_evidence = FiniteMeasure(
        inference.evidence_measure.labels,
        [float(value) for value in inference.evidence_measure.masses],
        numerics,
    )
    fine_q = ProbabilityMeasure(
        inference.recognition.labels,
        [float(value) for value in inference.recognition.masses],
        numerics,
    )
    float_channel = MarkovKernel(
        channel.source_labels,
        channel.target_labels,
        [[float(value) for value in row] for row in channel.matrix],
        numerics,
    )
    result = vfe_channel_decomposition(
        fine_q,
        MeasurePair(reference=fine_p_v, evidence_measure=fine_evidence),
        float_channel,
    )
    if result.residual is None or result.offending_state is not None:
        raise ValueError("finite VFE decomposition is undefined on this fixture")
    return result.conditional_kl, abs(result.residual)


def aggregate_population(
    inference: PopulationInference,
    channel: CoarseChannelSpec,
    numerics: NumericsConfig,
) -> AggregateDatum:
    """Push fine ``P``, ``Q``, and posterior through one common channel."""
    _validate_inputs(inference, channel, numerics)
    exact_channel = channel.channel

    generative_joint, generative_route_channel = _push_full_joint(inference, exact_channel)
    recognition, recognition_route_channel = _push_recognition(inference, exact_channel)
    posterior, posterior_route_channel = _push_posterior(inference, exact_channel)
    route_channels = (
        generative_route_channel,
        recognition_route_channel,
        posterior_route_channel,
    )
    route_ids = tuple(id(route_channel) for route_channel in route_channels)
    if (
        any(route_channel is not exact_channel for route_channel in route_channels)
        or len(set(route_ids)) != 1
    ):
        raise ValueError("all coarse pushes must use the same exact channel object")

    observed_index = inference.population.observation_labels.index(inference.observed_record)
    evidence = sum(
        (row[observed_index] for row in generative_joint),
        Fraction(0),
    )
    channel_sha256 = _channel_sha256(exact_channel)
    conditional_kl_defect, kl_chain_residual = _vfe_diagnostics(
        inference,
        exact_channel,
        numerics,
    )
    datum = AggregateDatum(
        aggregate_id=_aggregate_id(inference, channel, channel_sha256),
        source_agent_ids=channel.source_agent_ids,
        observed_record=inference.observed_record,
        channel_id=channel.channel_id,
        channel_sha256=channel_sha256,
        observation_labels=inference.population.observation_labels,
        target_labels=exact_channel.target_labels,
        generative_joint=generative_joint,
        recognition=recognition,
        posterior=posterior,
        evidence=evidence,
        conditional_kl_defect=conditional_kl_defect,
        kl_chain_residual=kl_chain_residual,
    )
    validate_aggregate_datum(datum, inference, channel, numerics)
    return datum


def validate_aggregate_datum(
    datum: AggregateDatum,
    inference: PopulationInference,
    channel: CoarseChannelSpec,
    numerics: NumericsConfig,
) -> None:
    """Replay the declared channel hash and every persisted mathematical arrow."""
    _validate_inputs(inference, channel, numerics)
    if not isinstance(datum, AggregateDatum):
        raise TypeError("datum must be an AggregateDatum")
    AggregateDatum(
        aggregate_id=datum.aggregate_id,
        source_agent_ids=datum.source_agent_ids,
        observed_record=datum.observed_record,
        channel_id=datum.channel_id,
        channel_sha256=datum.channel_sha256,
        observation_labels=datum.observation_labels,
        target_labels=datum.target_labels,
        generative_joint=datum.generative_joint,
        recognition=datum.recognition,
        posterior=datum.posterior,
        evidence=datum.evidence,
        conditional_kl_defect=datum.conditional_kl_defect,
        kl_chain_residual=datum.kl_chain_residual,
    )

    exact_channel = channel.channel
    expected_hash = _channel_sha256(exact_channel)
    if datum.channel_sha256 != expected_hash:
        raise ValueError("aggregate channel hash does not match the canonical declaration")
    if datum.aggregate_id != _aggregate_id(inference, channel, expected_hash):
        raise ValueError("aggregate ID does not match the prescribed deterministic route")
    if datum.source_agent_ids != channel.source_agent_ids:
        raise ValueError("aggregate source-agent IDs do not match the channel declaration")
    if datum.observed_record != inference.observed_record:
        raise ValueError("aggregate observed record does not match fine inference")
    if datum.channel_id != channel.channel_id:
        raise ValueError("aggregate channel ID does not match the channel declaration")
    if datum.observation_labels != inference.population.observation_labels:
        raise ValueError("aggregate observation support does not match the fine population")
    if datum.target_labels != exact_channel.target_labels:
        raise ValueError("aggregate target support does not match the channel declaration")

    expected_joint = _push_joint_values(inference, exact_channel)
    expected_recognition = _push_law_values(inference.recognition, exact_channel)
    expected_posterior = _push_law_values(inference.posterior, exact_channel)
    if datum.generative_joint != expected_joint:
        raise ValueError("aggregate generative joint does not equal the exact channel push")
    if datum.recognition != expected_recognition:
        raise ValueError("aggregate recognition does not equal the exact channel push")
    if datum.posterior != expected_posterior:
        raise ValueError("aggregate posterior does not equal the exact channel push")

    if sum((sum(row, Fraction(0)) for row in expected_joint), Fraction(0)) != 1:
        raise ValueError("aggregate generative joint must remain normalized exactly")
    observed_index = datum.observation_labels.index(datum.observed_record)
    expected_evidence = sum(
        (row[observed_index] for row in expected_joint),
        Fraction(0),
    )
    if expected_evidence != inference.evidence or datum.evidence != expected_evidence:
        raise ValueError("coarse evidence must equal fine evidence exactly")

    expected_defect, expected_residual = _vfe_diagnostics(
        inference,
        exact_channel,
        numerics,
    )
    if datum.conditional_kl_defect != expected_defect:
        raise ValueError("conditional KL defect does not match recomputation")
    if datum.kl_chain_residual != expected_residual:
        raise ValueError("KL chain residual does not match recomputation")
    tolerance = min(numerics.atol, 1.0e-12)
    if not math.isfinite(datum.conditional_kl_defect) or datum.conditional_kl_defect < -tolerance:
        raise ValueError("conditional KL defect violates its finite lower bound")
    if (
        not math.isfinite(datum.kl_chain_residual)
        or datum.kl_chain_residual < 0.0
        or datum.kl_chain_residual > tolerance
    ):
        raise ValueError("KL chain residual violates its finite upper bound")


__all__ = ["aggregate_population", "validate_aggregate_datum"]
