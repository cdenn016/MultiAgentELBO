"""Shared immutable metric records for experiment laboratories."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import re
from types import MappingProxyType
from typing import Literal, Mapping

import numpy as np

from .config import NEW_EXPERIMENT_NAMES


MetricStatus = Literal["pass", "fail", "inconclusive"]
LegacyTheoremStatus = Literal[
    "established_conditional_identity",
    "finite_metamorphic_identity",
    "negative_control",
]
CanonicalTheoremStatus = Literal[
    "ESTABLISHED", "HYPOTHESIS", "CONJECTURE", "NUMERICAL", "OPEN"
]
TheoremStatus = LegacyTheoremStatus | CanonicalTheoremStatus
VerificationState = Literal[
    "CANDIDATE",
    "LLM_SUPPORTED",
    "EVIDENCE_VERIFIED",
    "REFUTED",
    "INCONCLUSIVE",
]
ClaimOrigin = Literal["STANDARD", "PROJECT_NOVEL", "APPLICATION_SPECIFIC"]

_CANONICAL_THEOREM_STATUSES = frozenset(
    {"ESTABLISHED", "HYPOTHESIS", "CONJECTURE", "NUMERICAL", "OPEN"}
)
_LEGACY_THEOREM_STATUSES = frozenset(
    {
        "established_conditional_identity",
        "finite_metamorphic_identity",
        "negative_control",
    }
)
_VERIFICATION_STATES = frozenset(
    {
        "CANDIDATE",
        "LLM_SUPPORTED",
        "EVIDENCE_VERIFIED",
        "REFUTED",
        "INCONCLUSIVE",
    }
)
_CLAIM_ORIGINS = frozenset(
    {"STANDARD", "PROJECT_NOVEL", "APPLICATION_SPECIFIC"}
)


@dataclass(frozen=True)
class MetricRecord:
    """One implementation check, separate from its theorem status."""

    value: float
    tolerance: float
    status: MetricStatus
    interpretation: str
    assessment_scope: Literal["implementation_check"]
    theorem_status: TheoremStatus
    verification_state: VerificationState = "CANDIDATE"
    claim_origin: ClaimOrigin = "PROJECT_NOVEL"

    def __post_init__(self) -> None:
        if self.theorem_status not in (
            _CANONICAL_THEOREM_STATUSES | _LEGACY_THEOREM_STATUSES
        ):
            raise ValueError("invalid theorem_status")
        if self.verification_state not in _VERIFICATION_STATES:
            raise ValueError("invalid verification_state")
        if self.claim_origin not in _CLAIM_ORIGINS:
            raise ValueError("invalid claim_origin")


def target_metric(
    value: float,
    tolerance: float,
    *,
    target: float,
    interpretation: str,
    theorem_status: TheoremStatus,
    verification_state: VerificationState | None = None,
    claim_origin: ClaimOrigin | None = None,
) -> MetricRecord:
    """Create a metric which passes within tolerance of its target."""
    verification_state, claim_origin = _resolve_metric_metadata(
        theorem_status, verification_state, claim_origin
    )
    return MetricRecord(
        value=float(value),
        tolerance=float(tolerance),
        status="pass" if abs(value - target) <= tolerance else "fail",
        interpretation=interpretation,
        assessment_scope="implementation_check",
        theorem_status=theorem_status,
        verification_state=verification_state,
        claim_origin=claim_origin,
    )


def lower_bounded_metric(
    value: float,
    tolerance: float,
    *,
    lower_bound: float,
    interpretation: str,
    theorem_status: TheoremStatus,
    verification_state: VerificationState | None = None,
    claim_origin: ClaimOrigin | None = None,
) -> MetricRecord:
    """Create a metric which passes when it reaches its lower bound."""
    verification_state, claim_origin = _resolve_metric_metadata(
        theorem_status, verification_state, claim_origin
    )
    return MetricRecord(
        value=float(value),
        tolerance=float(tolerance),
        status="pass" if value >= lower_bound - tolerance else "fail",
        interpretation=interpretation,
        assessment_scope="implementation_check",
        theorem_status=theorem_status,
        verification_state=verification_state,
        claim_origin=claim_origin,
    )


def upper_bounded_metric(
    value: float,
    tolerance: float,
    *,
    upper_bound: float,
    interpretation: str,
    theorem_status: TheoremStatus,
    verification_state: VerificationState | None = None,
    claim_origin: ClaimOrigin | None = None,
) -> MetricRecord:
    """Create a metric which passes when it stays under its upper bound."""
    verification_state, claim_origin = _resolve_metric_metadata(
        theorem_status, verification_state, claim_origin
    )
    return MetricRecord(
        value=float(value),
        tolerance=float(tolerance),
        status="pass" if value <= upper_bound + tolerance else "fail",
        interpretation=interpretation,
        assessment_scope="implementation_check",
        theorem_status=theorem_status,
        verification_state=verification_state,
        claim_origin=claim_origin,
    )


def _resolve_metric_metadata(
    theorem_status: TheoremStatus,
    verification_state: VerificationState | None,
    claim_origin: ClaimOrigin | None,
) -> tuple[VerificationState, ClaimOrigin]:
    if theorem_status in _CANONICAL_THEOREM_STATUSES and (
        verification_state is None or claim_origin is None
    ):
        raise ValueError(
            "canonical metrics require explicit verification_state and claim_origin"
        )
    resolved_verification = (
        "CANDIDATE" if verification_state is None else verification_state
    )
    resolved_origin = "PROJECT_NOVEL" if claim_origin is None else claim_origin
    if resolved_verification not in _VERIFICATION_STATES:
        raise ValueError("invalid verification_state")
    if resolved_origin not in _CLAIM_ORIGINS:
        raise ValueError("invalid claim_origin")
    return resolved_verification, resolved_origin


@dataclass(frozen=True)
class ExperimentContract:
    """Frozen shared interface owned by one future implementation lane."""

    experiment: str
    lane_owner: str
    launcher: str
    config_keys: tuple[str, ...]
    artifact_inventory: tuple[str, ...]
    metric_inventory: tuple[str, ...]


_EXPERIMENT_CONTRACTS = {
    "multiagent_network": ExperimentContract(
        experiment="multiagent_network",
        lane_owner="session_1",
        launcher="run_multiagent_network_lab.py",
        config_keys=("experiment", "fixture", "scenario", "arithmetic"),
        artifact_inventory=(
            "fine_law",
            "coarse_law",
            "fine_to_coarse_channel",
            "hoeffding_interactions",
            "local_collective_differences",
            "configuration_scale_map",
        ),
        metric_inventory=(
            "evidence_residual",
            "elbo_gap_residual",
            "local_collective_residual",
            "hoeffding_reconstruction_residual",
            "recognition_lift_residual",
            "pairwise_retained_residual",
        ),
    ),
    "theory_oracle": ExperimentContract(
        experiment="theory_oracle",
        lane_owner="session_2",
        launcher="run_theory_oracle_lab.py",
        config_keys=("experiment", "fixture", "oracle_set", "arithmetic"),
        artifact_inventory=(
            "exact_numerators",
            "exact_denominators",
            "theorem_assumption_matrix",
            "literal_commuting_diagrams",
        ),
        metric_inventory=(
            "elbo_oracle_residual",
            "fisher_defect_oracle_residual",
            "marked_event_associativity_residual",
            "hoeffding_oracle_residual",
            "gaussian_linear_algebra_oracle_residual",
        ),
    ),
    "finite_counterexample": ExperimentContract(
        experiment="finite_counterexample",
        lane_owner="session_3",
        launcher="run_finite_counterexample_lab.py",
        config_keys=(
            "experiment",
            "fixture",
            "max_states",
            "max_denominator",
            "arithmetic",
        ),
        artifact_inventory=(
            "enumeration_bounds",
            "candidate_records",
            "minimal_witnesses",
            "stress_matrix",
        ),
        metric_inventory=(
            "support_violation_count",
            "parameter_dependent_channel_gap",
            "single_law_relabeling_gap",
            "marked_event_source_mass_gap",
            "pairwise_truncation_residual",
        ),
    ),
    "information_history": ExperimentContract(
        experiment="information_history",
        lane_owner="session_4",
        launcher="run_information_history_lab.py",
        config_keys=(
            "experiment",
            "fixture",
            "family",
            "history_steps",
            "step_size",
        ),
        artifact_inventory=(
            "history_parameters",
            "scores",
            "fisher_matrices",
            "vfe_gradients",
            "natural_gradient_fields",
            "information_durations",
            "semiconjugacy_defects",
        ),
        metric_inventory=(
            "score_finite_difference_residual",
            "fisher_defect_residual",
            "natural_gradient_range_residual",
            "arc_length_reparameterization_residual",
            "semiconjugacy_defect_norm",
        ),
    ),
    "gauge_holonomy": ExperimentContract(
        experiment="gauge_holonomy",
        lane_owner="session_5",
        launcher="run_gauge_holonomy_lab.py",
        config_keys=("experiment", "fixture", "scenario", "group"),
        artifact_inventory=(
            "interaction_complex",
            "oriented_links",
            "vertex_frames",
            "cycle_holonomies",
            "operational_record_laws",
            "aggregation_stages",
        ),
        metric_inventory=(
            "passive_covariance_residual",
            "cycle_conjugacy_invariant_residual",
            "trivialization_residual",
            "operational_observable_residual",
            "broken_link_negative_control",
        ),
    ),
    "scale_cocycle": ExperimentContract(
        experiment="scale_cocycle",
        lane_owner="session_6",
        launcher="run_scale_cocycle_lab.py",
        config_keys=(
            "experiment",
            "fixture",
            "extension",
            "retained_interaction_order",
            "arithmetic",
        ),
        artifact_inventory=(
            "three_level_extension",
            "composed_channels",
            "coarse_actions",
            "posterior_bridges",
            "comparison_isomorphisms",
            "derivative_cocycle",
            "retained_projection_residual",
        ),
        metric_inventory=(
            "direct_staged_pushforward_residual",
            "cocycle_composition_residual",
            "retained_beta_residual",
            "full_interaction_reconstruction_residual",
            "wrong_order_negative_control",
        ),
    ),
    "gaussian_fixed_ray": ExperimentContract(
        experiment="gaussian_fixed_ray",
        lane_owner="session_6",
        launcher="run_gaussian_fixed_ray_lab.py",
        config_keys=(
            "experiment",
            "fixture",
            "preregistration",
            "blocking_schemes",
            "matrix_dimension",
        ),
        artifact_inventory=(
            "preregistered_job_table",
            "initial_conditions",
            "per_seed_endpoints",
            "backend_provenance",
            "parity_matrix",
            "performance_records",
        ),
        metric_inventory=(
            "projective_ray_angle",
            "normalized_coupling_distance",
            "scalarized_ray_construction_residual",
            "retained_beta_residual",
            "basin_exit_rate",
            "blocking_scheme_dispersion",
            "cpu_cuda_parity_residual",
        ),
    ),
    "renormalization_v2": ExperimentContract(
        experiment="renormalization_v2",
        lane_owner="rg_v2_release_1",
        launcher="run_renormalization_v2_lab.py",
        config_keys=("experiment", "fixture", "arithmetic"),
        artifact_inventory=(
            "fixture_snapshot",
            "population_joint",
            "population_inference",
            "aggregate_datum",
            "metrics",
            "arrays",
        ),
        metric_inventory=(
            "agent_kernel_normalization_residual",
            "evaluator_compatibility_residual",
            "record_kernel_normalization_residual",
            "record_ownership_violation_count",
            "population_normalization_residual",
            "independent_population_residual",
            "recognition_marginal_residual",
            "model_marginal_non_dirac_count",
            "posterior_derivation_residual",
            "common_channel_identity_violation_count",
            "coarse_evidence_residual",
            "conditional_kl_defect",
            "kl_chain_residual",
        ),
    ),
}

if tuple(_EXPERIMENT_CONTRACTS) != NEW_EXPERIMENT_NAMES:
    raise RuntimeError("experiment registry order drifted from config discriminators")

EXPERIMENT_REGISTRY: Mapping[str, ExperimentContract] = MappingProxyType(
    _EXPERIMENT_CONTRACTS
)


CUDA_WORKER_PROTOCOL_VERSION = "cuda-worker-protocol-v1"
_TWO_SCALE_APPLICATION_ID = (
    "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"
)
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
_JOB_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_WORKER_DTYPES = frozenset({"float64", "float32", "bfloat16", "int64", "bool"})


@dataclass(frozen=True)
class WorkerArrayDescriptor:
    name: str
    shape: tuple[int, ...]
    dtype: str
    sha256: str


@dataclass(frozen=True)
class WorkerProtocolManifest:
    schema_version: str
    message_type: Literal["request", "response"]
    job_id: str
    requested_backend: Literal["cpu", "cuda"]
    requested_dtype: Literal["float64", "float32", "bfloat16"]
    effective_backend: Literal["cpu", "cuda"] | None
    effective_dtype: Literal["float64", "float32", "bfloat16"] | None
    environment_sha256: str
    npz_sha256: str
    arrays: tuple[WorkerArrayDescriptor, ...]
    output_identity: str | None


def worker_output_identity(
    manifest: Mapping[str, object],
    *,
    request_manifest: Mapping[str, object],
) -> str:
    """Hash the canonical request/response pair with response self-hash null."""
    request_payload = dict(request_manifest)
    request_payload["output_identity"] = None
    response_payload = dict(manifest)
    response_payload["output_identity"] = None
    payload = {"request": request_payload, "response": response_payload}
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_worker_protocol_manifest(
    manifest: Mapping[str, object],
    *,
    expected_message_type: str,
    request_manifest: Mapping[str, object] | None = None,
) -> WorkerProtocolManifest:
    """Validate the frozen JSON/NPZ controller-worker envelope without I/O."""
    _require_mapping_keys(
        manifest,
        "worker manifest",
        {
            "schema_version",
            "message_type",
            "job_id",
            "requested_backend",
            "requested_dtype",
            "effective_backend",
            "effective_dtype",
            "environment_sha256",
            "npz_sha256",
            "arrays",
            "output_identity",
        },
    )
    if manifest["schema_version"] != CUDA_WORKER_PROTOCOL_VERSION:
        raise ValueError("invalid schema_version")
    message_type = manifest["message_type"]
    if message_type not in {"request", "response"}:
        raise ValueError("message_type must be request or response")
    if message_type != expected_message_type:
        raise ValueError("unexpected message_type")
    job_id = manifest["job_id"]
    if type(job_id) is not str or _JOB_ID_PATTERN.fullmatch(job_id) is None:
        raise ValueError("invalid job_id")
    requested_backend = manifest["requested_backend"]
    if requested_backend not in {"cpu", "cuda"}:
        raise ValueError("invalid requested_backend")
    requested_dtype = manifest["requested_dtype"]
    if requested_dtype not in {"float64", "float32", "bfloat16"}:
        raise ValueError("invalid requested_dtype")
    environment_sha256 = _require_sha256(
        manifest["environment_sha256"], "environment_sha256"
    )
    npz_sha256 = _require_sha256(manifest["npz_sha256"], "npz_sha256")

    raw_arrays = manifest["arrays"]
    if type(raw_arrays) is not list or not raw_arrays:
        raise ValueError("arrays must not be empty")
    arrays: list[WorkerArrayDescriptor] = []
    names: set[str] = set()
    for index, raw_array in enumerate(raw_arrays):
        if not isinstance(raw_array, Mapping):
            raise ValueError(f"arrays[{index}] must be an object")
        _require_mapping_keys(
            raw_array, f"arrays[{index}]", {"name", "shape", "dtype", "sha256"}
        )
        name = raw_array["name"]
        if type(name) is not str or _JOB_ID_PATTERN.fullmatch(name) is None:
            raise ValueError(f"arrays[{index}].name is invalid")
        if name in names:
            raise ValueError("array names must be unique")
        names.add(name)
        raw_shape = raw_array["shape"]
        if type(raw_shape) is not list or any(
            type(size) is not int or size < 0 for size in raw_shape
        ):
            raise ValueError(f"arrays[{index}].shape is invalid")
        dtype = raw_array["dtype"]
        if dtype not in _WORKER_DTYPES:
            raise ValueError(f"arrays[{index}].dtype is invalid")
        arrays.append(
            WorkerArrayDescriptor(
                name=name,
                shape=tuple(raw_shape),
                dtype=dtype,
                sha256=_require_sha256(
                    raw_array["sha256"], f"arrays[{index}].sha256"
                ),
            )
        )

    effective_backend = manifest["effective_backend"]
    effective_dtype = manifest["effective_dtype"]
    output_identity = manifest["output_identity"]
    if message_type == "request":
        if effective_backend is not None or effective_dtype is not None:
            raise ValueError("request effective backend and dtype must be null")
        if output_identity is not None:
            raise ValueError("request output_identity must be null")
    else:
        if request_manifest is None:
            raise ValueError("response validation requires the original request")
        validated_request = validate_worker_protocol_manifest(
            request_manifest, expected_message_type="request"
        )
        for field, response_value, request_value in (
            ("job_id", job_id, validated_request.job_id),
            (
                "requested_backend",
                requested_backend,
                validated_request.requested_backend,
            ),
            (
                "requested_dtype",
                requested_dtype,
                validated_request.requested_dtype,
            ),
            (
                "environment_sha256",
                environment_sha256,
                validated_request.environment_sha256,
            ),
        ):
            if response_value != request_value:
                raise ValueError(f"response {field} does not match original request")
        if effective_backend != validated_request.requested_backend:
            raise ValueError("effective backend must equal requested backend")
        if effective_dtype != validated_request.requested_dtype:
            raise ValueError("effective dtype must equal requested dtype")
        _require_sha256(output_identity, "output_identity")
        if output_identity != worker_output_identity(
            manifest, request_manifest=request_manifest
        ):
            raise ValueError("output_identity does not match canonical response")

    return WorkerProtocolManifest(
        schema_version=CUDA_WORKER_PROTOCOL_VERSION,
        message_type=message_type,
        job_id=job_id,
        requested_backend=requested_backend,
        requested_dtype=requested_dtype,
        effective_backend=effective_backend,
        effective_dtype=effective_dtype,
        environment_sha256=environment_sha256,
        npz_sha256=npz_sha256,
        arrays=tuple(arrays),
        output_identity=output_identity,
    )


def fixture_application_id(payload: Mapping[str, object]) -> str:
    """Return the self-hash-free canonical application identifier."""
    canonical_payload = {key: value for key, value in payload.items() if key != "application_id"}
    canonical = json.dumps(
        canonical_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_two_scale_application_fixture(payload: Mapping[str, object]) -> str:
    """Validate the immutable literal application tuple and return its ID."""
    _require_mapping_keys(
        payload,
        "fixture",
        {
            "schema_version",
            "application_id",
            "hash_rule",
            "epistemic_boundary",
            "agents",
            "organization",
            "state_spaces",
            "interaction_complex",
            "channel",
            "reference_laws",
            "generative_structure",
            "recognition",
            "configuration",
            "local_blocks",
            "claims",
        },
    )
    if payload["schema_version"] != "two-scale-application-v1":
        raise ValueError("invalid fixture schema_version")
    application_id = _require_sha256(payload["application_id"], "application_id")
    if application_id != fixture_application_id(payload):
        raise ValueError("application_id does not match canonical fixture")

    agents = payload["agents"]
    expected_agents = [
        {"agent_id": str(index), "state_labels": ["0", "1"]}
        for index in range(4)
    ]
    if agents != expected_agents:
        raise ValueError("agents must be the exact four binary agents")
    organization = _require_mapping(payload["organization"], "organization")
    if organization.get("blocks") != [
        {"block_id": "B01", "agents": ["0", "1"]},
        {"block_id": "B23", "agents": ["2", "3"]},
    ]:
        raise ValueError("organization must be the frozen two-block partition")

    state_spaces = _require_mapping(payload["state_spaces"], "state_spaces")
    fine_space = _require_mapping(state_spaces.get("fine"), "state_spaces.fine")
    coarse_space = _require_mapping(
        state_spaces.get("coarse"), "state_spaces.coarse"
    )
    fine_labels = [f"{value:04b}" for value in range(16)]
    coarse_labels = ["00", "01", "10", "11"]
    if fine_space.get("labels") != fine_labels:
        raise ValueError("invalid fine state labels")
    if coarse_space.get("labels") != coarse_labels:
        raise ValueError("invalid coarse state labels")

    interaction = _require_mapping(
        payload["interaction_complex"], "interaction_complex"
    )
    if interaction.get("vertices") != ["0", "1", "2", "3"]:
        raise ValueError("interaction vertices do not match agents")
    hyperedges = interaction.get("hyperedges")
    if type(hyperedges) is not list or not any(
        isinstance(edge, Mapping) and len(edge.get("members", ())) > 2
        for edge in hyperedges
    ):
        raise ValueError("one higher-order hyperedge is required")

    channel = _require_mapping(payload["channel"], "channel")
    arrows = channel.get("arrows")
    if type(arrows) is not list or len(arrows) != 1:
        raise ValueError("fixture must declare exactly one channel arrow")
    arrow = _require_mapping(arrows[0], "channel.arrows[0]")
    if arrow.get("recognition_independent") is not True:
        raise ValueError("channel must be recognition-independent")
    if arrow.get("source_labels") != fine_labels or arrow.get("target_labels") != coarse_labels:
        raise ValueError("channel labels do not match state spaces")
    rows = arrow.get("rows")
    if type(rows) is not list or len(rows) != len(fine_labels):
        raise ValueError("channel rows do not match fine states")
    for index, row in enumerate(rows):
        values = _require_fraction_vector(
            row, 4, f"channel.arrows[0].rows[{index}]"
        )
        if sum(values) != 1:
            raise ValueError(f"channel row {index} is not normalized")

    references = _require_mapping(payload["reference_laws"], "reference_laws")
    fine_reference = _require_mapping(references.get("fine"), "reference_laws.fine")
    coarse_reference = _require_mapping(
        references.get("coarse"), "reference_laws.coarse"
    )
    fine_reference_values = _require_fraction_vector(
        fine_reference.get("values"), 16, "reference_laws.fine.values"
    )
    coarse_reference_values = _require_fraction_vector(
        coarse_reference.get("values"), 4, "reference_laws.coarse.values"
    )
    if sum(fine_reference_values) != 1 or sum(coarse_reference_values) != 1:
        raise ValueError("reference laws must be normalized")
    if fine_reference.get("reference_type") != "product_reference":
        raise ValueError("fine reference must be product_reference")
    if coarse_reference.get("reference_type") != "block_product_reference":
        raise ValueError("coarse reference must be block_product_reference")

    generative = _require_mapping(
        payload["generative_structure"], "generative_structure"
    )
    baseline = _require_fraction_vector(
        generative.get("correlated_baseline"), 16, "correlated_baseline"
    )
    if sum(baseline) != 1 or baseline == fine_reference_values:
        raise ValueError("baseline must be normalized and correlated")
    observation_kernel = generative.get("observation_record_kernel")
    if type(observation_kernel) is not list or len(observation_kernel) != 16:
        raise ValueError("observation record kernel has the wrong shape")
    for index, row in enumerate(observation_kernel):
        if sum(_require_fraction_vector(row, 2, f"observation row {index}")) != 1:
            raise ValueError("observation record kernel must be normalized")
    evidence = _require_fraction_vector(
        generative.get("evidence_submeasure"), 16, "evidence_submeasure"
    )
    evidence_mass = _require_fraction(
        generative.get("evidence_mass"), "evidence_mass"
    )
    if sum(evidence) != evidence_mass:
        raise ValueError("evidence submeasure does not match evidence mass")
    if sum(
        _require_fraction_vector(generative.get("posterior"), 16, "posterior")
    ) != 1:
        raise ValueError("posterior must be normalized")

    recognition = _require_mapping(payload["recognition"], "recognition")
    if sum(
        _require_fraction_vector(recognition.get("fine_law"), 16, "recognition.fine_law")
    ) != 1:
        raise ValueError("fine recognition law must be normalized")
    if sum(
        _require_fraction_vector(recognition.get("coarse_law"), 4, "recognition.coarse_law")
    ) != 1:
        raise ValueError("coarse recognition law must be normalized")
    right_inverse = _require_mapping(
        recognition.get("right_inverse"), "recognition.right_inverse"
    )
    if right_inverse.get("check_state") != "NOT_CHECKED":
        raise ValueError("right-inverse application check must remain NOT_CHECKED")

    configuration = _require_mapping(payload["configuration"], "configuration")
    _require_fraction_matrix(
        configuration.get("coarse_map_matrix"), 2, 4, "coarse_map_matrix"
    )
    comparisons = _require_mapping(
        configuration.get("comparison_isomorphisms"),
        "configuration.comparison_isomorphisms",
    )
    _require_fraction_matrix(comparisons.get("fine"), 4, 4, "fine comparison")
    _require_fraction_matrix(comparisons.get("coarse"), 2, 2, "coarse comparison")

    claims = _require_mapping(payload["claims"], "claims")
    for section in ("assumptions", "witness_data", "checked_conclusions"):
        records = claims.get(section)
        if type(records) is not list or not records:
            raise ValueError(f"claims.{section} must not be empty")
        for record in records:
            metadata = _require_mapping(record, f"claims.{section} record")
            if metadata.get("theorem_status") not in _CANONICAL_THEOREM_STATUSES:
                raise ValueError("claim theorem_status is invalid")
            if metadata.get("verification_state") not in _VERIFICATION_STATES:
                raise ValueError("claim verification_state is invalid")
            if metadata.get("claim_origin") not in _CLAIM_ORIGINS:
                raise ValueError("claim claim_origin is invalid")
    if application_id != _TWO_SCALE_APPLICATION_ID:
        raise ValueError("fixture does not match frozen application_id")
    return application_id


def _require_mapping(value: object, field: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return value


def _require_mapping_keys(
    value: Mapping[str, object], section: str, expected: set[str]
) -> None:
    unknown = sorted(set(value) - expected)
    missing = sorted(expected - set(value))
    if unknown:
        raise ValueError(f"unknown {section} key: {unknown[0]}")
    if missing:
        raise ValueError(f"missing {section} key: {missing[0]}")


def _require_sha256(value: object, field: str) -> str:
    if type(value) is not str or _SHA256_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{field} must be a lowercase SHA-256")
    return value


def _require_fraction(value: object, field: str) -> Fraction:
    if type(value) is not str:
        raise ValueError(f"{field} must be a rational string")
    try:
        fraction = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(f"{field} must be a rational string") from error
    if str(fraction) != value:
        raise ValueError(f"{field} must be a reduced rational string")
    return fraction


def _require_fraction_vector(
    value: object, size: int, field: str
) -> list[Fraction]:
    if type(value) is not list or len(value) != size:
        raise ValueError(f"{field} must contain {size} rational strings")
    return [
        _require_fraction(item, f"{field}[{index}]")
        for index, item in enumerate(value)
    ]


def _require_fraction_matrix(
    value: object, rows: int, columns: int, field: str
) -> None:
    if type(value) is not list or len(value) != rows:
        raise ValueError(f"{field} has the wrong row count")
    for index, row in enumerate(value):
        _require_fraction_vector(row, columns, f"{field}[{index}]")


def readonly_array(values: object, dtype: object = np.float64) -> np.ndarray:
    """Copy values into an immutable C-contiguous numerical array."""
    array = np.array(values, dtype=dtype, copy=True, order="C")
    array.setflags(write=False)
    return array


__all__ = [
    "CUDA_WORKER_PROTOCOL_VERSION",
    "CanonicalTheoremStatus",
    "ClaimOrigin",
    "EXPERIMENT_REGISTRY",
    "ExperimentContract",
    "MetricRecord",
    "MetricStatus",
    "TheoremStatus",
    "VerificationState",
    "WorkerArrayDescriptor",
    "WorkerProtocolManifest",
    "fixture_application_id",
    "lower_bounded_metric",
    "readonly_array",
    "target_metric",
    "upper_bounded_metric",
    "validate_two_scale_application_fixture",
    "validate_worker_protocol_manifest",
    "worker_output_identity",
]
