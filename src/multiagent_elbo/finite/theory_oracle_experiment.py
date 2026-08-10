"""Session-2 exact-theory oracle experiment adapter."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from types import MappingProxyType
from typing import Literal, Mapping

import numpy as np

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import (
    ExperimentConfig,
    TheoryOracleTheoryConfig,
    config_sha256,
)
from multiagent_elbo.experiment_support import (
    MetricRecord,
    MetricStatus,
    readonly_array,
    target_metric,
)
from multiagent_elbo.finite.attention import (
    StateConditionedAttentionLaw,
    compose_kernels,
)
from multiagent_elbo.finite.fisher import fisher_channel_decomposition
from multiagent_elbo.finite.interactions import (
    hoeffding_decompose,
    retain_interaction_order,
)
from multiagent_elbo.finite.measures import (
    FiniteMeasure,
    MarkovKernel,
    MeasurePair,
    ProbabilityMeasure,
)
from multiagent_elbo.finite.theory_oracles import (
    LANE_PRIVATE_AUXILIARY_PACKETS,
    LANE_PRIVATE_NONIDENTITY_COMMUTING_SQUARE,
    THEOREM_ASSUMPTION_MATRIX,
    TWO_SCALE_APPLICATION_ID,
    FormalLogSum,
    FractionMatrix,
    FractionTensor,
    FractionVector,
    compose_markov_kernels,
    evaluate_commuting_square,
    exact_evidence_elbo,
    exact_fisher_defect,
    exact_hoeffding_decomposition,
    galerkin_restriction,
    inverse_congruence,
    load_two_scale_application,
    parse_fraction_literal,
    push_marked_event_law,
    schur_complement,
    transform_prolongator as exact_transform_prolongator,
)
from multiagent_elbo.finite.vfe import free_energy, kl_divergence
from multiagent_elbo.realizations.gaussian.gauge import apply_frame_change
from multiagent_elbo.realizations.gaussian.interactions import (
    GaussianInteraction,
    galerkin_aggregate_precision,
    schur_complement_precision,
)
from multiagent_elbo.runtime import RngStreams, collect_provenance


FigureStatus = Literal["not_exposed"]

_METRIC_ARRAY_PAIRS = {
    "elbo_oracle_residual": ("elbo_oracle_values", "elbo_production_values"),
    "fisher_defect_oracle_residual": (
        "fisher_defect_oracle_values",
        "fisher_defect_production_values",
    ),
    "marked_event_associativity_residual": (
        "marked_event_oracle_values",
        "marked_event_production_values",
    ),
    "hoeffding_oracle_residual": (
        "hoeffding_oracle_values",
        "hoeffding_production_values",
    ),
    "gaussian_linear_algebra_oracle_residual": (
        "gaussian_linear_algebra_oracle_values",
        "gaussian_linear_algebra_production_values",
    ),
}

_METRIC_EXACT_LAYOUT = {
    "elbo_oracle_residual": [
        {"kind": "formal_log", "name": "elbo.evidence_log"},
        {"kind": "formal_log", "name": "elbo.elbo"},
        {"kind": "formal_log", "name": "elbo.kl"},
        {"kind": "formal_log", "name": "elbo.structural_residual"},
    ],
    "fisher_defect_oracle_residual": [
        {"kind": "rational_array", "name": f"fisher.{name}"}
        for name in (
            "joint_weights",
            "coarse_mass",
            "coarse_scores",
            "fine_fisher",
            "coarse_fisher",
            "defect",
            "conditional_covariance",
        )
    ],
    "marked_event_associativity_residual": [
        {"kind": "rational_array", "name": f"marked.{stage}.{name}"}
        for stage in ("direct", "staged")
        for name in ("joint", "coarse_state_mass", "conditional_events")
    ],
    "hoeffding_oracle_residual": [
        {"kind": "rational_array", "name": f"hoeffding.component.{subset}"}
        for subset in (
            "empty",
            "0",
            "1",
            "2",
            "0_1",
            "0_2",
            "1_2",
            "0_1_2",
        )
    ]
    + [
        {"kind": "rational_array", "name": f"hoeffding.{name}"}
        for name in (
            "reconstruction",
            "reconstruction_residual",
            "retained_values",
            "retained_residual",
        )
    ],
    "gaussian_linear_algebra_oracle_residual": [
        {"kind": "rational_array", "name": f"gaussian.{name}"}
        for name in (
            "inverse_congruence",
            "transformed_prolongator",
            "galerkin",
            "schur",
        )
    ],
}


@dataclass(frozen=True)
class TheoryOracleExperimentResult:
    """Finalized immutable result of the exact-theory comparison laboratory."""

    run_dir: Path
    config_hash: str
    status: MetricStatus
    metrics: Mapping[str, MetricRecord]
    arrays: Mapping[str, np.ndarray]
    diagnostics: Mapping[str, np.ndarray]
    figure_status: FigureStatus


@dataclass(frozen=True)
class _OracleBundle:
    arrays: dict[str, np.ndarray]
    diagnostics: dict[str, np.ndarray]
    rational_arrays: dict[str, tuple[tuple[int, ...], tuple[Fraction, ...]]]
    formal_logs: dict[str, FormalLogSum]
    application_id: str
    fixture_sha256: str
    theorem_assumptions: dict[str, object]
    commuting_diagrams: dict[str, object]


def _validate_config(config: ExperimentConfig) -> None:
    if config.theory.experiment != "theory_oracle":
        raise ValueError(
            "theory oracle experiment requires theory.experiment='theory_oracle'"
        )
    expected_theory = TheoryOracleTheoryConfig(
        experiment="theory_oracle",
        fixture="two_scale_application_v1",
        oracle_set="core_identities",
        arithmetic="exact_rational",
    )
    if config.theory != expected_theory:
        raise ValueError("theory oracle experiment requires the frozen theory config")
    if config.compute.backend != "cpu":
        raise ValueError("theory oracle experiment is CPU-only")
    if config.compute.dtype != "float64":
        raise ValueError("compute dtype must be 'float64'")
    if config.numerics.dtype != "float64":
        raise ValueError("numerics dtype must be 'float64'")
    if config.compute.device_index != 0:
        raise ValueError("theory oracle CPU device_index must be 0")
    if config.compute.allow_tf32:
        raise ValueError("theory oracle experiment does not allow TF32")
    if config.output.render_figures:
        raise ValueError("figures are not exposed for theory_oracle")


def _fraction_vector(values: object) -> FractionVector:
    if not isinstance(values, list):
        raise TypeError("fixture vector must be a JSON array")
    return FractionVector(tuple(parse_fraction_literal(value) for value in values))


def _packet(packet_id: str) -> dict[str, tuple[Fraction, ...]]:
    packet = next(
        (item for item in LANE_PRIVATE_AUXILIARY_PACKETS if item.packet_id == packet_id),
        None,
    )
    if packet is None or not packet.lane_private or packet.replacement_application_fixture:
        raise ValueError(f"invalid lane-private oracle packet: {packet_id}")
    return {
        name: tuple(parse_fraction_literal(value) for value in values)
        for name, values in packet.literals
    }


def _matrix(values: tuple[Fraction, ...], rows: int, columns: int) -> FractionMatrix:
    if len(values) != rows * columns:
        raise ValueError("matrix packet length does not match its declared shape")
    return FractionMatrix(
        tuple(
            tuple(values[row * columns + column] for column in range(columns))
            for row in range(rows)
        )
    )


def _float(values: tuple[Fraction, ...]) -> np.ndarray:
    return np.asarray([float(value) for value in values], dtype=np.float64)


def _matrix_values(matrix: FractionMatrix) -> tuple[Fraction, ...]:
    return tuple(value for row in matrix.rows for value in row)


def _rational_entry(
    value: FractionVector | FractionMatrix | FractionTensor,
) -> tuple[tuple[int, ...], tuple[Fraction, ...]]:
    if isinstance(value, FractionVector):
        return (len(value),), value.values
    if isinstance(value, FractionMatrix):
        return value.shape, _matrix_values(value)
    return value.shape, value.values


def _add_rational(
    target: dict[str, tuple[tuple[int, ...], tuple[Fraction, ...]]],
    name: str,
    value: FractionVector | FractionMatrix | FractionTensor,
) -> None:
    target[name] = _rational_entry(value)


def _oracle_elbo(
    payload: dict[str, object], config: ExperimentConfig
) -> tuple[np.ndarray, np.ndarray, dict[str, FormalLogSum], dict[str, object]]:
    generative = payload["generative_structure"]
    recognition = payload["recognition"]
    if not isinstance(generative, dict) or not isinstance(recognition, dict):
        raise TypeError("fixture generative and recognition sections must be objects")
    evidence = _fraction_vector(generative["evidence_submeasure"])
    evidence_mass = parse_fraction_literal(generative["evidence_mass"])
    posterior = _fraction_vector(generative["posterior"])
    q = _fraction_vector(recognition["fine_law"])
    exact = exact_evidence_elbo(evidence, evidence_mass, posterior, q)
    if (
        exact.branch != "finite"
        or not isinstance(exact.elbo, FormalLogSum)
        or not isinstance(exact.kl, FormalLogSum)
        or exact.residual is None
        or not exact.residual.is_zero
    ):
        raise ValueError("frozen ELBO oracle did not remain on its finite exact branch")

    labels = tuple(f"x{index}" for index in range(len(q)))
    q_float = ProbabilityMeasure(labels, _float(q.values), config.numerics)
    posterior_float = ProbabilityMeasure(
        labels, _float(posterior.values), config.numerics
    )
    reference = ProbabilityMeasure(
        labels, np.full(len(labels), 1.0 / len(labels)), config.numerics
    )
    evidence_float = FiniteMeasure(labels, _float(evidence.values), config.numerics)
    pair = MeasurePair(reference, evidence_float)
    production_kl = kl_divergence(q_float, posterior_float)
    production_elbo = -free_energy(q_float, pair)
    production_evidence_log = math.log(pair.evidence)
    production_residual = (
        production_evidence_log - production_elbo - production_kl
    )
    oracle_values = np.asarray(
        (
            exact.evidence_log.evaluate_float(),
            exact.elbo.evaluate_float(),
            exact.kl.evaluate_float(),
            exact.residual.evaluate_float(),
        ),
        dtype=np.float64,
    )
    production_values = np.asarray(
        (
            production_evidence_log,
            production_elbo,
            production_kl,
            production_residual,
        ),
        dtype=np.float64,
    )
    formal_logs = {
        "elbo.evidence_log": exact.evidence_log,
        "elbo.elbo": exact.elbo,
        "elbo.kl": exact.kl,
        "elbo.structural_residual": exact.residual,
    }
    details = {
        "evidence": evidence,
        "posterior": posterior,
        "recognition": q,
    }
    return oracle_values, production_values, formal_logs, details


def _oracle_fisher(
    config: ExperimentConfig,
) -> tuple[np.ndarray, np.ndarray, object, dict[str, np.ndarray]]:
    literals = _packet("oracle_aux_fisher_v1")
    probability = FractionVector(literals["probability"])
    channel = _matrix(literals["channel"], 2, 2)
    score = _matrix(literals["score"], 2, 1)
    exact = exact_fisher_defect(probability, channel, score)
    production = fisher_channel_decomposition(
        ProbabilityMeasure(("x0", "x1"), _float(probability.values), config.numerics),
        _float(_matrix_values(score)).reshape(score.shape),
        MarkovKernel(
            ("x0", "x1"),
            ("z0", "z1"),
            _float(_matrix_values(channel)).reshape(channel.shape),
            config.numerics,
        ),
    )
    exact_parts = (
        exact.joint_weights,
        exact.coarse_mass,
        exact.coarse_scores,
        exact.fine_fisher,
        exact.coarse_fisher,
        exact.defect,
        exact.conditional_covariance,
    )
    oracle_values = np.concatenate(
        [_float(_rational_entry(part)[1]) for part in exact_parts]
    )
    production_values = np.concatenate(
        [
            production.joint_mass.ravel(),
            production.coarse_probability.ravel(),
            production.coarse_score.ravel(),
            production.fine_fisher.ravel(),
            production.coarse_fisher.ravel(),
            (production.fine_fisher - production.coarse_fisher).ravel(),
            production.conditional_covariance.ravel(),
        ]
    )
    diagnostics = {
        "fisher_identity_residual": production.residual,
        "fisher_score": _float(_matrix_values(score)).reshape(score.shape),
    }
    return oracle_values, production_values, exact, diagnostics


def _exact_marked_eta(pushforward: object) -> FractionTensor:
    events = pushforward.conditional_events
    if any(event is None for event in events):
        raise ValueError("marked-event auxiliary packet produced a zero-mass state")
    first = events[0]
    if first is None:
        raise ValueError("marked-event auxiliary packet is missing a state")
    return FractionTensor(
        (len(events), *first.shape),
        tuple(
            value
            for event in events
            if event is not None
            for value in event.values
        ),
    )


def _marked_values(pushforward: object) -> tuple[Fraction, ...]:
    eta = _exact_marked_eta(pushforward)
    return (
        *pushforward.joint.values,
        *pushforward.coarse_state_mass.values,
        *eta.values,
    )


def _oracle_marked_event(
    config: ExperimentConfig,
) -> tuple[np.ndarray, np.ndarray, dict[str, object], dict[str, np.ndarray]]:
    literals = _packet("oracle_aux_marked_event_v1")
    state_mass = FractionVector(literals["state_mass"])
    events = FractionTensor((2, 2, 2), literals["conditional_events"])
    state_1 = _matrix(literals["state_kernel_stage_1"], 2, 2)
    state_2 = _matrix(literals["state_kernel_stage_2"], 2, 2)
    receiver_1 = _matrix(literals["receiver_kernel_stage_1"], 2, 2)
    receiver_2 = _matrix(literals["receiver_kernel_stage_2"], 2, 2)
    source_1 = _matrix(literals["source_kernel_stage_1"], 2, 2)
    source_2 = _matrix(literals["source_kernel_stage_2"], 2, 2)
    exact_middle = push_marked_event_law(
        state_mass, events, state_1, receiver_1, source_1
    )
    exact_staged = push_marked_event_law(
        exact_middle.coarse_state_mass,
        _exact_marked_eta(exact_middle),
        state_2,
        receiver_2,
        source_2,
    )
    exact_direct = push_marked_event_law(
        state_mass,
        events,
        compose_markov_kernels(state_1, state_2),
        compose_markov_kernels(receiver_1, receiver_2),
        compose_markov_kernels(source_1, source_2),
    )
    if exact_direct.joint != exact_staged.joint:
        raise ValueError("exact marked-event direct and staged laws disagree")

    state_labels = ("y0", "y1")
    node_labels = ("n0", "n1")
    fine_law = StateConditionedAttentionLaw(
        ProbabilityMeasure(state_labels, _float(state_mass.values), config.numerics),
        node_labels,
        node_labels,
        _float(events.values).reshape(events.shape),
    )

    def kernel(
        source: tuple[str, ...],
        target: tuple[str, ...],
        exact_kernel: FractionMatrix,
    ) -> MarkovKernel:
        return MarkovKernel(
            source,
            target,
            _float(_matrix_values(exact_kernel)).reshape(exact_kernel.shape),
            config.numerics,
        )

    state_k1 = kernel(state_labels, ("u0", "u1"), state_1)
    state_k2 = kernel(("u0", "u1"), ("z0", "z1"), state_2)
    receiver_k1 = kernel(node_labels, ("r0", "r1"), receiver_1)
    receiver_k2 = kernel(("r0", "r1"), ("R0", "R1"), receiver_2)
    source_k1 = kernel(node_labels, ("s0", "s1"), source_1)
    source_k2 = kernel(("s0", "s1"), ("S0", "S1"), source_2)
    middle = fine_law.pushforward(state_k1, receiver_k1, source_k1)
    staged = middle.pushforward(state_k2, receiver_k2, source_k2)
    direct = fine_law.pushforward(
        compose_kernels(state_k1, state_k2),
        compose_kernels(receiver_k1, receiver_k2),
        compose_kernels(source_k1, source_k2),
    )

    def production_values(law: StateConditionedAttentionLaw) -> np.ndarray:
        joint = law.state_probability.masses[:, None, None] * law.eta_given_state
        return np.concatenate(
            (
                joint.ravel(),
                law.state_probability.masses.ravel(),
                law.eta_given_state.ravel(),
            )
        )

    oracle_values = np.concatenate(
        (_float(_marked_values(exact_direct)), _float(_marked_values(exact_staged)))
    )
    production = np.concatenate((production_values(direct), production_values(staged)))
    details = {
        "direct": exact_direct,
        "staged": exact_staged,
        "middle": exact_middle,
    }
    diagnostics = {
        "marked_direct_minus_staged": (
            direct.eta_given_state - staged.eta_given_state
        ),
        "marked_stage_1_state_kernel": state_k1.matrix,
        "marked_stage_2_state_kernel": state_k2.matrix,
    }
    return oracle_values, production, details, diagnostics


def _broadcast_component(
    component: np.ndarray,
    subset: tuple[int, ...],
    shape: tuple[int, ...],
) -> np.ndarray:
    component_shape = tuple(shape[axis] if axis in subset else 1 for axis in range(len(shape)))
    return np.broadcast_to(component.reshape(component_shape), shape)


def _oracle_hoeffding() -> tuple[np.ndarray, np.ndarray, object, dict[str, np.ndarray]]:
    literals = _packet("oracle_aux_hoeffding_v1")
    values = FractionTensor((2, 2, 2), literals["action"])
    references = tuple(
        FractionVector(literals[f"axis_{axis}_reference"]) for axis in range(3)
    )
    retained_order_values = literals["retained_order"]
    if len(retained_order_values) != 1 or retained_order_values[0].denominator != 1:
        raise ValueError("retained-order packet must contain one integer")
    retained_order = retained_order_values[0].numerator
    exact = exact_hoeffding_decomposition(values, references, retained_order)
    action = _float(values.values).reshape(values.shape)
    production = hoeffding_decompose(
        action, tuple(_float(reference.values) for reference in references)
    )
    projection = retain_interaction_order(production, retained_order)
    exact_parts = [component.values.values for component in exact.components]
    exact_parts.extend(
        (
            exact.reconstruction.values,
            exact.reconstruction_residual.values,
            exact.retained_values.values,
            exact.retained_residual.values,
        )
    )
    production_parts = [
        _broadcast_component(
            production.components[component.subset], component.subset, action.shape
        ).ravel()
        for component in exact.components
    ]
    production_parts.extend(
        (
            production.reconstruction.ravel(),
            (action - production.reconstruction).ravel(),
            projection.retained_values.ravel(),
            projection.omitted_values.ravel(),
        )
    )
    diagnostics = {
        "hoeffding_omitted_values": projection.omitted_values,
        "hoeffding_reconstruction_residual": action - production.reconstruction,
    }
    return (
        np.concatenate([_float(part) for part in exact_parts]),
        np.concatenate(production_parts),
        exact,
        diagnostics,
    )


def _oracle_gaussian(
    config: ExperimentConfig,
) -> tuple[np.ndarray, np.ndarray, dict[str, object], dict[str, np.ndarray]]:
    literals = _packet("oracle_aux_gaussian_v1")
    precision = _matrix(literals["fine_precision"], 4, 4)
    prolongator = _matrix(literals["prolongator"], 4, 2)
    fine_frame = _matrix(literals["fine_frame"], 4, 4)
    coarse_frame = _matrix(literals["coarse_frame"], 2, 2)
    schur_precision = _matrix(literals["schur_precision"], 3, 3)
    retained, eliminated = _validated_schur_indices(
        literals["schur_retained"],
        literals["schur_eliminated"],
        size=schur_precision.shape[0],
    )
    exact_congruence = inverse_congruence(precision, fine_frame)
    exact_prolongator = exact_transform_prolongator(
        prolongator, fine_frame, coarse_frame
    )
    exact_galerkin = galerkin_restriction(precision, prolongator)
    exact_schur = schur_complement(
        schur_precision, retained=retained, eliminated=eliminated
    )

    precision_float = _float(_matrix_values(precision)).reshape(precision.shape)
    prolongator_float = _float(_matrix_values(prolongator)).reshape(prolongator.shape)
    fine_frame_float = _float(_matrix_values(fine_frame)).reshape(fine_frame.shape)
    coarse_frame_float = _float(_matrix_values(coarse_frame)).reshape(
        coarse_frame.shape
    )
    fine_frames = np.diag(fine_frame_float).reshape(4, 1, 1)
    coarse_frames = np.diag(coarse_frame_float).reshape(2, 1, 1)
    gauge = apply_frame_change(
        precision_float,
        np.zeros_like(precision_float),
        fine_frames,
        config.numerics,
        prolongator=prolongator_float,
        coarse_frames=coarse_frames,
    )
    interaction = GaussianInteraction.from_self_and_edges(
        np.diag(precision_float), {}, config.numerics
    )
    aggregation = galerkin_aggregate_precision(
        interaction, ((0, 2), (1, 3))
    )
    production_schur = schur_complement_precision(
        _float(_matrix_values(schur_precision)).reshape(schur_precision.shape),
        retained_vertices=retained,
        block_size=1,
        numerics=config.numerics,
    )
    if gauge.transformed_prolongator is None:
        raise ValueError("Gaussian production path did not transform the prolongator")
    oracle_values = np.concatenate(
        (
            _float(_matrix_values(exact_congruence)),
            _float(_matrix_values(exact_prolongator)),
            _float(_matrix_values(exact_galerkin)),
            _float(_matrix_values(exact_schur)),
        )
    )
    production_values = np.concatenate(
        (
            gauge.transformed_precision.ravel(),
            gauge.transformed_prolongator.ravel(),
            aggregation.precision.ravel(),
            production_schur.ravel(),
        )
    )
    details = {
        "inverse_congruence": exact_congruence,
        "transformed_prolongator": exact_prolongator,
        "galerkin": exact_galerkin,
        "schur": exact_schur,
    }
    diagnostics = {
        "gaussian_fine_frames": fine_frames,
        "gaussian_coarse_frames": coarse_frames,
        "gaussian_prolongator": prolongator_float,
    }
    return oracle_values, production_values, details, diagnostics


def _validated_schur_indices(
    retained_values: tuple[Fraction, ...],
    eliminated_values: tuple[Fraction, ...],
    *,
    size: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if not retained_values or not eliminated_values:
        raise ValueError("Schur indices require nonempty retained and eliminated sets")
    if any(
        value.denominator != 1 for value in retained_values + eliminated_values
    ):
        raise ValueError("Schur packet indices must be integer indices")
    retained = tuple(int(value) for value in retained_values)
    eliminated = tuple(int(value) for value in eliminated_values)
    if len(set(retained)) != len(retained) or len(set(eliminated)) != len(
        eliminated
    ):
        raise ValueError("Schur retained and eliminated indices must be unique")
    if set(retained).intersection(eliminated):
        raise ValueError("Schur retained and eliminated indices must be disjoint")
    if any(index < 0 or index >= size for index in retained + eliminated):
        raise ValueError("Schur retained and eliminated indices must be in range")
    if set(retained).union(eliminated) != set(range(size)):
        raise ValueError("Schur indices must form the required full partition")
    return retained, eliminated


def _matrix_literals(matrix: FractionMatrix) -> list[list[str]]:
    return [[str(value) for value in row] for row in matrix.rows]


def _diagram_payload(application: object) -> tuple[dict[str, object], dict[str, object]]:
    positive_witness = LANE_PRIVATE_NONIDENTITY_COMMUTING_SQUARE
    positive = evaluate_commuting_square(
        positive_witness.coarse_map,
        positive_witness.fine_comparison,
        positive_witness.coarse_comparison,
    )
    negative_coarse_comparison = FractionMatrix(
        ((Fraction(2), Fraction(0)), (Fraction(0), Fraction(2)))
    )
    negative = evaluate_commuting_square(
        positive_witness.coarse_map,
        positive_witness.fine_comparison,
        negative_coarse_comparison,
    )
    if not application.commutes or not positive.commutes or negative.commutes:
        raise ValueError("literal commuting-diagram controls lost their polarity")

    def record(
        packet_id: str,
        left: FractionMatrix,
        right: FractionMatrix,
        commutes: bool,
        *,
        auxiliary: bool,
        control: str,
    ) -> dict[str, object]:
        return {
            "packet_id": packet_id,
            "left": _matrix_literals(left),
            "right": _matrix_literals(right),
            "commutes": commutes,
            "auxiliary": auxiliary,
            "control": control,
            "lane_private": auxiliary,
            "replacement_application_fixture": False,
        }

    payload = {
        "schema_version": "literal-commuting-diagrams-v1",
        "application_identity_map_square": {
            **record(
                "two_scale_application_v1",
                application.left_square,
                application.right_square,
                application.commutes,
                auxiliary=False,
                control="frozen_application_witness",
            ),
            "application_id": application.application_id,
            "recognition_right_inverse_state": application.recognition_right_inverse_state,
            "application_theorem_status": application.application_theorem_status,
            "application_verification_state": application.application_verification_state,
            "application_claim_origin": application.application_claim_origin,
        },
        "auxiliary_nonidentity_positive_control": record(
            positive_witness.packet_id,
            positive.left,
            positive.right,
            positive.commutes,
            auxiliary=True,
            control="positive",
        ),
        "auxiliary_nonidentity_negative_control": record(
            "oracle_aux_nonidentity_noncommuting_square_v1",
            negative.left,
            negative.right,
            negative.commutes,
            auxiliary=True,
            control="negative",
        ),
    }
    exact = {
        "application_square_left": application.left_square,
        "application_square_right": application.right_square,
        "aux_positive_square_left": positive.left,
        "aux_positive_square_right": positive.right,
        "aux_negative_square_left": negative.left,
        "aux_negative_square_right": negative.right,
    }
    return payload, exact


def _assumption_payload() -> dict[str, object]:
    records = [asdict(record) for record in THEOREM_ASSUMPTION_MATRIX]
    if len({record["identity_id"] for record in records}) != len(records):
        raise ValueError("theorem-assumption identities must be unique")
    application_records = [
        record
        for record in records
        if record["identity_id"] == "two_scale_literal_commuting_square"
    ]
    if application_records != [
        {
            **application_records[0],
            "theorem_status": "HYPOTHESIS",
            "verification_state": "CANDIDATE",
            "claim_origin": "APPLICATION_SPECIFIC",
        }
    ]:
        raise ValueError("application assumption metadata crossed its frozen boundary")
    return {
        "schema_version": "theorem-assumption-matrix-v1",
        "records": records,
    }


def _build_bundle(config: ExperimentConfig) -> _OracleBundle:
    repo_root = Path(__file__).resolve().parents[3]
    fixture_path = repo_root / "tests" / "fixtures" / "two_scale_application_v1.json"
    fixture_bytes = fixture_path.read_bytes()
    payload = json.loads(fixture_bytes.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("two-scale application fixture must be a JSON object")
    application = load_two_scale_application(fixture_path)
    if application.application_id != TWO_SCALE_APPLICATION_ID:
        raise ValueError("unexpected two-scale application ID")

    elbo_oracle, elbo_production, formal_logs, elbo_details = _oracle_elbo(
        payload, config
    )
    fisher_oracle, fisher_production, fisher, fisher_diagnostics = _oracle_fisher(
        config
    )
    marked_oracle, marked_production, marked, marked_diagnostics = (
        _oracle_marked_event(config)
    )
    hoeffding_oracle, hoeffding_production, hoeffding, hoeffding_diagnostics = (
        _oracle_hoeffding()
    )
    gaussian_oracle, gaussian_production, gaussian, gaussian_diagnostics = (
        _oracle_gaussian(config)
    )
    diagrams, diagram_exact = _diagram_payload(application)
    assumptions = _assumption_payload()

    arrays = {
        "elbo_oracle_values": elbo_oracle,
        "elbo_production_values": elbo_production,
        "fisher_defect_oracle_values": fisher_oracle,
        "fisher_defect_production_values": fisher_production,
        "marked_event_oracle_values": marked_oracle,
        "marked_event_production_values": marked_production,
        "hoeffding_oracle_values": hoeffding_oracle,
        "hoeffding_production_values": hoeffding_production,
        "gaussian_linear_algebra_oracle_values": gaussian_oracle,
        "gaussian_linear_algebra_production_values": gaussian_production,
    }
    diagnostics = {
        **fisher_diagnostics,
        **marked_diagnostics,
        **hoeffding_diagnostics,
        **gaussian_diagnostics,
    }
    rational_arrays: dict[
        str, tuple[tuple[int, ...], tuple[Fraction, ...]]
    ] = {}
    for name, value in elbo_details.items():
        _add_rational(rational_arrays, f"elbo.{name}", value)
    for name in (
        "joint_weights",
        "coarse_mass",
        "coarse_scores",
        "fine_fisher",
        "coarse_fisher",
        "defect",
        "conditional_covariance",
    ):
        _add_rational(rational_arrays, f"fisher.{name}", getattr(fisher, name))
    for stage_name, stage in marked.items():
        _add_rational(rational_arrays, f"marked.{stage_name}.joint", stage.joint)
        _add_rational(
            rational_arrays,
            f"marked.{stage_name}.coarse_state_mass",
            stage.coarse_state_mass,
        )
        _add_rational(
            rational_arrays,
            f"marked.{stage_name}.conditional_events",
            _exact_marked_eta(stage),
        )
    for component in hoeffding.components:
        subset = "empty" if not component.subset else "_".join(map(str, component.subset))
        _add_rational(
            rational_arrays, f"hoeffding.component.{subset}", component.values
        )
    for name in (
        "reconstruction",
        "reconstruction_residual",
        "retained_values",
        "retained_residual",
    ):
        _add_rational(rational_arrays, f"hoeffding.{name}", getattr(hoeffding, name))
    for name, value in gaussian.items():
        _add_rational(rational_arrays, f"gaussian.{name}", value)
    for name, value in diagram_exact.items():
        _add_rational(rational_arrays, f"diagram.{name}", value)

    bundle = _OracleBundle(
        arrays=arrays,
        diagnostics=diagnostics,
        rational_arrays=rational_arrays,
        formal_logs=formal_logs,
        application_id=application.application_id,
        fixture_sha256=hashlib.sha256(fixture_bytes).hexdigest(),
        theorem_assumptions=assumptions,
        commuting_diagrams=diagrams,
    )
    for metric_name, (oracle_name, _) in _METRIC_ARRAY_PAIRS.items():
        reconstructed = _exact_layout_values(bundle, metric_name)
        if not np.array_equal(reconstructed, bundle.arrays[oracle_name]):
            raise ValueError(
                f"exact JSON layout does not reproduce {metric_name} oracle values"
            )
    return bundle


def _exact_layout_values(bundle: _OracleBundle, metric_name: str) -> np.ndarray:
    pieces: list[np.ndarray] = []
    for component in _METRIC_EXACT_LAYOUT[metric_name]:
        name = component["name"]
        if component["kind"] == "rational_array":
            _, values = bundle.rational_arrays[name]
            pieces.append(np.asarray([float(value) for value in values]))
        else:
            pieces.append(np.asarray([bundle.formal_logs[name].evaluate_float()]))
    return np.concatenate(pieces)


def _split_exact_artifact(
    bundle: _OracleBundle, *, numerator: bool
) -> dict[str, object]:
    attribute = "numerator" if numerator else "denominator"
    return {
        "schema_version": "exact-rational-components-v1",
        "component": attribute,
        "metric_oracle_layout": _METRIC_EXACT_LAYOUT,
        "rational_arrays": {
            name: {
                "shape": list(shape),
                "values": [getattr(value, attribute) for value in values],
            }
            for name, (shape, values) in sorted(bundle.rational_arrays.items())
        },
        "formal_log_sums": {
            name: {
                "atoms": [getattr(term.atom, attribute) for term in value.terms],
                "coefficients": [
                    getattr(term.coefficient, attribute) for term in value.terms
                ],
            }
            for name, value in sorted(bundle.formal_logs.items())
        },
    }


def _freeze(values: Mapping[str, np.ndarray]) -> dict[str, np.ndarray]:
    return {
        name: readonly_array(values[name], dtype=np.float64)
        for name in sorted(values)
    }


def run_theory_oracle_experiment(
    config: ExperimentConfig,
) -> TheoryOracleExperimentResult:
    """Validate, compare independent exact/float paths, and finalize one run."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    _validate_config(config)

    # All fixture and oracle validation occurs before RNG, provenance, or publication.
    bundle = _build_bundle(config)
    arrays = _freeze(bundle.arrays)
    diagnostics = _freeze(bundle.diagnostics)
    tolerance = config.numerics.atol + config.numerics.rtol
    metrics = {
        name: target_metric(
            float(np.max(np.abs(arrays[production] - arrays[oracle]))),
            tolerance,
            target=0.0,
            interpretation=(
                "Independent float implementation agrees with the exact conditional "
                f"oracle for {name}; numerical agreement is not mathematical proof."
            ),
            theorem_status="ESTABLISHED",
            verification_state="CANDIDATE",
            claim_origin="PROJECT_NOVEL",
        )
        for name, (oracle, production) in _METRIC_ARRAY_PAIRS.items()
    }

    resolved_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    repo_root = Path(__file__).resolve().parents[3]
    provenance = collect_provenance(
        repo_root, repo_root / "Theory", resolved_hash, streams
    )
    provenance["experiment_scope"] = "finite_conditional_exact_oracle_comparison"
    provenance["application_id"] = bundle.application_id
    input_hashes = provenance["input_hashes"]
    if not isinstance(input_hashes, dict):
        raise TypeError("provenance input_hashes must be a dictionary")
    input_hashes["two_scale_application_id"] = bundle.application_id
    input_hashes["two_scale_application_file_sha256"] = bundle.fixture_sha256

    store = RunStore.create(config, provenance)
    store.write_json(
        "metrics", {name: asdict(metrics[name]) for name in sorted(metrics)}
    )
    store.write_npz("arrays", arrays)
    store.write_json("exact_numerators", _split_exact_artifact(bundle, numerator=True))
    store.write_json(
        "exact_denominators", _split_exact_artifact(bundle, numerator=False)
    )
    store.write_json("theorem_assumption_matrix", bundle.theorem_assumptions)
    store.write_json("literal_commuting_diagrams", bundle.commuting_diagrams)
    declared = [
        "metrics.json",
        "arrays.npz",
        "exact_numerators.json",
        "exact_denominators.json",
        "theorem_assumption_matrix.json",
        "literal_commuting_diagrams.json",
    ]
    if config.output.collect_diagnostics:
        store.write_npz("diagnostics", diagnostics)
        declared.append("diagnostics.npz")
    store.finalize(declared)
    status: MetricStatus = (
        "pass" if all(metric.status == "pass" for metric in metrics.values()) else "fail"
    )
    return TheoryOracleExperimentResult(
        run_dir=store.run_dir,
        config_hash=store.config_hash,
        status=status,
        metrics=MappingProxyType(dict(metrics)),
        arrays=MappingProxyType(arrays),
        diagnostics=MappingProxyType(
            diagnostics if config.output.collect_diagnostics else {}
        ),
        figure_status="not_exposed",
    )


__all__ = ["TheoryOracleExperimentResult", "run_theory_oracle_experiment"]
