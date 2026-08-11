"""Validation and deterministic replay of the frozen confirmatory extract.

The tracked extract is historical scientific evidence produced at one source
revision.  This module validates that source before replaying the same frozen
production iterator at a separately supplied live diagnostic revision.  Replay
is deliberately not described as an independent reconstruction.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from hashlib import sha256
import json
import math
from pathlib import Path
import re
from types import MappingProxyType

import numpy as np

from .confirmatory_analysis import analyze_holdout, analyze_primary
from .fixed_ray import (
    FixedRayTrajectory,
    blocking_scheme_dispersion,
    build_preregistered_system,
    generate_initial_coefficients,
    iterate_fixed_ray,
    job_seed,
    projective_ray_angle,
    scalarized_ray_construction_residual,
)


CPU_REPLAY_ATOL = 2.0e-14

_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
_REVISION_PATTERN = re.compile(r"[0-9a-f]{40}")
_SCHEMES = ("adjacent_pairs", "balanced_alternating")
_PRIMARY_JOB_IDS = tuple(f"C{index:03d}" for index in range(1, 31))
_HOLDOUT_JOB_IDS = tuple(f"H{index:03d}" for index in range(1, 11))
_JOB_IDS = _PRIMARY_JOB_IDS + _HOLDOUT_JOB_IDS
_PILOT_JOB_IDS = tuple(f"P{index:03d}" for index in range(1, 5))
_ALL_JOB_IDS = _PILOT_JOB_IDS + _JOB_IDS
_ORIGINAL_INVENTORY_NAMES = (
    "config.json",
    "confirmatory_arrays.npz",
    "confirmatory_endpoints.json",
    "confirmatory_execution.json",
    "confirmatory_job_table.json",
    "holdout_analysis.json",
    "manifest.json",
    "metrics.json",
    "primary_analysis.json",
    "primary_execution.json",
)
_TRACKED_SCIENTIFIC_SUBSET = (
    "config.json",
    "confirmatory_arrays.npz",
    "confirmatory_endpoints.json",
    "confirmatory_job_table.json",
    "holdout_analysis.json",
    "manifest.json",
    "metrics.json",
    "primary_analysis.json",
)
_OMITTED_EXECUTION_LOGS = (
    "confirmatory_execution.json",
    "primary_execution.json",
)
_CANONICAL_JOB_TABLE_FORMAT = (
    "json.dumps(_job_table(config), sort_keys=True, separators=(',', ':'), "
    "allow_nan=False).encode('utf-8')"
)
_REPLAY_FIELDS = (
    "coefficients",
    "projective_ray_angles",
    "normalized_coupling_distances",
    "scalarized_ray_construction_residuals",
    "retained_beta_residuals",
    "coefficient_conditioning",
)


def _canonical_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _require_sha256(value: object, label: str) -> str:
    if type(value) is not str or _SHA256_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{label} must be a lowercase SHA-256 digest")
    return value


def _require_revision(value: object, label: str) -> str:
    if type(value) is not str or _REVISION_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{label} must be a lowercase 40-hex Git revision")
    return value


def _freeze_json(value: object, *, label: str = "JSON value") -> object:
    if isinstance(value, Mapping):
        frozen: dict[str, object] = {}
        for key, nested in value.items():
            if type(key) is not str:
                raise ValueError(f"{label} keys must be strings")
            frozen[key] = _freeze_json(nested, label=f"{label}.{key}")
        return MappingProxyType(frozen)
    if isinstance(value, (list, tuple)):
        return tuple(
            _freeze_json(nested, label=f"{label}[{index}]")
            for index, nested in enumerate(value)
        )
    if value is None or type(value) in {str, bool, int}:
        return value
    if type(value) is float and math.isfinite(value):
        return value
    raise ValueError(f"{label} must contain only finite JSON values")


def _plain_json(value: object) -> object:
    if isinstance(value, Mapping):
        return {str(key): _plain_json(nested) for key, nested in value.items()}
    if isinstance(value, tuple):
        return [_plain_json(nested) for nested in value]
    return value


def _readonly(values: object, *, dtype: object | None = None) -> np.ndarray:
    array = np.array(values, dtype=dtype, copy=True, order="C")
    array.setflags(write=False)
    return array


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _sequence(value: object, label: str) -> Sequence[object]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{label} must be a sequence")
    return value


def _finite_array(
    value: object,
    *,
    shape: tuple[int, ...],
    label: str,
) -> np.ndarray:
    array = np.asarray(value, dtype=np.float64)
    if array.shape != shape or not np.all(np.isfinite(array)):
        raise ValueError(f"{label} must be a finite float64 array of shape {shape}")
    return array


def _compare_array(
    actual: object,
    expected: object,
    *,
    label: str,
    atol: float = CPU_REPLAY_ATOL,
) -> float:
    left = np.asarray(actual, dtype=np.float64)
    right = np.asarray(expected, dtype=np.float64)
    if left.shape != right.shape or not np.all(np.isfinite(left)):
        raise ValueError(f"{label} shape or finiteness drifted")
    difference = float(np.max(np.abs(left - right))) if left.size else 0.0
    if not np.allclose(left, right, rtol=0.0, atol=atol):
        raise ValueError(
            f"{label} drifted beyond the deterministic replay tolerance {atol}"
        )
    return difference


def _semantic_equal(
    actual: object,
    expected: object,
    *,
    label: str,
    skip_hash_fields: bool = False,
) -> None:
    if isinstance(actual, Mapping) and isinstance(expected, Mapping):
        _semantic_mapping_equal(
            actual,
            expected,
            label=label,
            skip_hash_fields=skip_hash_fields,
        )
        return
    if isinstance(actual, (list, tuple)) and isinstance(expected, (list, tuple)):
        _semantic_sequence_equal(
            actual,
            expected,
            label=label,
            skip_hash_fields=skip_hash_fields,
        )
        return
    if type(actual) is bool or type(expected) is bool:
        if actual is not expected:
            raise ValueError(f"{label} drifted")
        return
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        if not _finite_numbers_close(actual, expected):
            raise ValueError(f"{label} drifted")
        return
    if actual != expected:
        raise ValueError(f"{label} drifted")


def _semantic_mapping_equal(
    actual: Mapping[str, object],
    expected: Mapping[str, object],
    *,
    label: str,
    skip_hash_fields: bool,
) -> None:
    if set(actual) != set(expected):
        raise ValueError(f"{label} key inventory drifted")
    for key in actual:
        if skip_hash_fields and key.endswith("_sha256"):
            _require_sha256(actual[key], f"{label}.{key}")
            continue
        _semantic_equal(
            actual[key],
            expected[key],
            label=f"{label}.{key}",
            skip_hash_fields=skip_hash_fields,
        )


def _semantic_sequence_equal(
    actual: Sequence[object],
    expected: Sequence[object],
    *,
    label: str,
    skip_hash_fields: bool,
) -> None:
    if len(actual) != len(expected):
        raise ValueError(f"{label} length drifted")
    for index, (left, right) in enumerate(zip(actual, expected)):
        _semantic_equal(
            left,
            right,
            label=f"{label}[{index}]",
            skip_hash_fields=skip_hash_fields,
        )


def _finite_numbers_close(actual: int | float, expected: int | float) -> bool:
    return (
        math.isfinite(float(actual))
        and math.isfinite(float(expected))
        and math.isclose(
            float(actual),
            float(expected),
            rel_tol=0.0,
            abs_tol=CPU_REPLAY_ATOL,
        )
    )


@dataclass(frozen=True)
class ConfirmatorySourceBinding:
    """Typed historical-source and live-diagnostic revision binding."""

    schema_version: str
    scientific_revision: str
    diagnostic_revision: str
    coordinator_evidence_sha256: str
    complete_original_inventory: Mapping[str, Mapping[str, object]]
    scientific_payload_hashes: Mapping[str, object]
    tracked_scientific_subset: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "gaussian-confirmatory-source-binding-v1":
            raise ValueError("source-binding schema version drifted")
        _require_revision(self.scientific_revision, "scientific revision")
        _require_revision(self.diagnostic_revision, "diagnostic revision")
        _require_sha256(
            self.coordinator_evidence_sha256,
            "coordinator evidence SHA-256",
        )
        inventory = _mapping(
            self.complete_original_inventory,
            "complete original inventory",
        )
        if tuple(inventory) != _ORIGINAL_INVENTORY_NAMES:
            raise ValueError("complete original inventory must contain all ten files")
        frozen_inventory: dict[str, Mapping[str, object]] = {}
        for name in _ORIGINAL_INVENTORY_NAMES:
            record = _mapping(inventory[name], f"inventory record for {name}")
            if set(record) != {"sha256", "size_bytes"}:
                raise ValueError(f"inventory record for {name} drifted")
            digest = _require_sha256(record["sha256"], f"{name} SHA-256")
            size = record["size_bytes"]
            if type(size) is not int or size <= 0:
                raise ValueError(f"{name} size must be a positive integer")
            frozen_inventory[name] = MappingProxyType(
                {"sha256": digest, "size_bytes": size}
            )
        if tuple(self.tracked_scientific_subset) != _TRACKED_SCIENTIFIC_SUBSET:
            raise ValueError("tracked scientific subset inventory drifted")
        payload_hashes = _mapping(
            self.scientific_payload_hashes,
            "scientific payload hashes",
        )
        if set(payload_hashes) != {
            "job_table_canonical_json_sha256",
            "job_table_canonical_json_format",
            "published_job_table_reconstruction",
        }:
            raise ValueError("scientific payload hash contract drifted")
        _require_sha256(
            payload_hashes["job_table_canonical_json_sha256"],
            "canonical job-table SHA-256",
        )
        if payload_hashes["job_table_canonical_json_format"] != (
            _CANONICAL_JOB_TABLE_FORMAT
        ):
            raise ValueError("canonical job-table serialization format drifted")
        reconstruction = _mapping(
            payload_hashes["published_job_table_reconstruction"],
            "published job-table reconstruction",
        )
        if (
            tuple(reconstruction.get("remove_fields", ()))
            != (
                "executed_primary_job_ids",
                "executed_holdout_job_ids",
            )
            or reconstruction.get("set_confirmatory_executed") is not False
        ):
            raise ValueError("published job-table reconstruction rule drifted")
        object.__setattr__(
            self,
            "complete_original_inventory",
            MappingProxyType(frozen_inventory),
        )
        frozen_payload_hashes = _freeze_json(
            payload_hashes,
            label="scientific payload hashes",
        )
        assert isinstance(frozen_payload_hashes, Mapping)
        object.__setattr__(self, "scientific_payload_hashes", frozen_payload_hashes)
        object.__setattr__(
            self,
            "tracked_scientific_subset",
            tuple(self.tracked_scientific_subset),
        )

    @classmethod
    def from_mapping(
        cls,
        payload: Mapping[str, object],
        *,
        diagnostic_revision: str,
    ) -> "ConfirmatorySourceBinding":
        source = _mapping(payload, "source binding")
        expected_keys = {
            "schema_version",
            "scientific_revision",
            "coordinator_evidence_sha256",
            "complete_original_inventory",
            "scientific_payload_hashes",
            "tracked_scientific_subset",
        }
        if set(source) != expected_keys:
            raise ValueError("source-binding field inventory drifted")
        subset = _sequence(
            source["tracked_scientific_subset"],
            "tracked scientific subset",
        )
        if not all(type(name) is str for name in subset):
            raise ValueError("tracked scientific subset names must be strings")
        return cls(
            schema_version=str(source["schema_version"]),
            scientific_revision=str(source["scientific_revision"]),
            diagnostic_revision=diagnostic_revision,
            coordinator_evidence_sha256=str(source["coordinator_evidence_sha256"]),
            complete_original_inventory=_mapping(
                source["complete_original_inventory"],
                "complete original inventory",
            ),
            scientific_payload_hashes=_mapping(
                source["scientific_payload_hashes"],
                "scientific payload hashes",
            ),
            tracked_scientific_subset=tuple(str(name) for name in subset),
        )

    @classmethod
    def from_path(
        cls,
        path: Path,
        *,
        diagnostic_revision: str,
    ) -> "ConfirmatorySourceBinding":
        source_path = Path(path)
        try:
            payload = json.loads(source_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ValueError("source-binding JSON could not be loaded") from error
        return cls.from_mapping(payload, diagnostic_revision=diagnostic_revision)

    @property
    def canonical_source_binding_sha256(self) -> str:
        """Return the source-only binding digest, excluding live code identity."""
        payload = {
            "schema_version": self.schema_version,
            "scientific_revision": self.scientific_revision,
            "coordinator_evidence_sha256": self.coordinator_evidence_sha256,
            "complete_original_inventory": _plain_json(
                self.complete_original_inventory
            ),
            "scientific_payload_hashes": _plain_json(self.scientific_payload_hashes),
            "tracked_scientific_subset": list(self.tracked_scientific_subset),
        }
        return sha256(_canonical_bytes(payload)).hexdigest()


@dataclass(frozen=True)
class ValidatedConfirmatorySource:
    """Immutable, hash-validated confirmatory scientific source."""

    source_dir: Path
    binding: ConfirmatorySourceBinding
    scientific_revision: str
    diagnostic_revision: str
    job_ids: tuple[str, ...]
    schemes: tuple[str, ...]
    jobs: tuple[Mapping[str, object], ...]
    arrays: Mapping[str, np.ndarray]
    config: Mapping[str, object]
    job_table: Mapping[str, object]
    endpoint_records: tuple[Mapping[str, object], ...]
    primary_analysis: Mapping[str, object]
    holdout_analysis: Mapping[str, object]
    manifest: Mapping[str, object]
    metrics: Mapping[str, object]
    recorded_execution_metadata: Mapping[str, object]


@dataclass(frozen=True)
class ReplayResult:
    """Immutable output of the frozen production-path deterministic replay."""

    operation: str
    scientific_revision: str
    diagnostic_revision: str
    call_count: int
    cpu_replay_atol: float
    trajectories: Mapping[str, Mapping[str, FixedRayTrajectory]]
    max_absolute_errors: Mapping[str, float]
    recorded_execution_metadata: Mapping[str, object]


def _read_json(path: Path, label: str) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{label} could not be loaded as JSON") from error
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must contain one JSON object")
    _freeze_json(payload, label=label)
    return payload


def _expected_job_rows() -> tuple[tuple[str, int, str], ...]:
    rows: list[tuple[str, int, str]] = []
    specifications = (
        ("P", 4, 202608090001, "pilot"),
        ("C", 30, 202608090101, "confirmatory_primary"),
        ("H", 10, 202608090201, "confirmatory_holdout"),
    )
    for prefix, count, first_seed, role in specifications:
        rows.extend(
            (f"{prefix}{offset + 1:03d}", first_seed + offset, role)
            for offset in range(count)
        )
    return tuple(rows)


def _validate_job_table(
    job_table: Mapping[str, object],
    binding: ConfirmatorySourceBinding,
) -> tuple[Mapping[str, object], ...]:
    if job_table.get("schema_version") != "gaussian-fixed-ray-job-table-v1":
        raise ValueError("confirmatory job-table schema drifted")
    if (
        job_table.get("preregistration") != "2026-08-09-gaussian-fixed-ray-v1"
        or job_table.get("confirmatory_executed") is not True
        or job_table.get("heavy_sweep_enabled") is not True
        or job_table.get("primary_scale_window") != [4, 5, 6, 7, 8]
    ):
        raise ValueError("confirmatory job-table protocol drifted")
    rows = _sequence(job_table.get("jobs"), "confirmatory jobs")
    expected_rows = _expected_job_rows()
    if len(rows) != len(expected_rows):
        raise ValueError("confirmatory job-table inventory drifted")
    validated_rows: list[Mapping[str, object]] = []
    observed_ids: list[str] = []
    for raw_row, (expected_id, expected_seed, expected_role) in zip(
        rows,
        expected_rows,
    ):
        row = _mapping(raw_row, f"job {expected_id}")
        job_id = row.get("job_id")
        if type(job_id) is not str:
            raise ValueError("confirmatory job ID must be a string")
        observed_ids.append(job_id)
        if (
            job_id != expected_id
            or row.get("master_seed") != expected_seed
            or row.get("role") != expected_role
            or tuple(row.get("schemes", ())) != _SCHEMES
            or row.get("steps") != 8
            or row.get("substream_seed_u64") != job_seed(expected_seed, expected_id)
        ):
            raise ValueError(f"confirmatory job {expected_id} drifted")
        validated_rows.append(row)
    if len(set(observed_ids)) != len(observed_ids):
        raise ValueError("confirmatory job IDs must be unique")
    if observed_ids != list(_ALL_JOB_IDS):
        raise ValueError("confirmatory job order drifted")
    if job_table.get("executed_primary_job_ids") != list(_PRIMARY_JOB_IDS):
        raise ValueError("primary execution inventory drifted")
    if job_table.get("executed_holdout_job_ids") != list(_HOLDOUT_JOB_IDS):
        raise ValueError("holdout execution inventory drifted")
    pilot_rows = _sequence(job_table.get("executed_pilot_jobs"), "executed pilots")
    if len(pilot_rows) != 4:
        raise ValueError("pilot inventory drifted")
    for actual, expected in zip(pilot_rows, validated_rows[:4]):
        if actual != expected:
            raise ValueError("executed pilot record drifted")
    if job_table.get("sentinel_job_ids") != [
        "C001",
        "C015",
        "C030",
        "H001",
        "H010",
    ]:
        raise ValueError("sentinel inventory drifted")

    planned_table = dict(job_table)
    planned_table.pop("executed_primary_job_ids", None)
    planned_table.pop("executed_holdout_job_ids", None)
    planned_table["confirmatory_executed"] = False
    canonical_hash = sha256(_canonical_bytes(planned_table)).hexdigest()
    payload_hashes = binding.scientific_payload_hashes
    if canonical_hash != payload_hashes["job_table_canonical_json_sha256"]:
        raise ValueError(
            "canonical planned job-table payload SHA-256 drifted independently "
            "of the published raw-file SHA-256"
        )
    return tuple(validated_rows[4:])


def _expected_array_names() -> tuple[str, ...]:
    names: list[str] = []
    for job_id in _JOB_IDS:
        names.append(f"{job_id}_initial_coefficients")
        names.extend(f"{job_id}_{scheme}_coefficients" for scheme in _SCHEMES)
    return tuple(names)


def _load_arrays(path: Path) -> Mapping[str, np.ndarray]:
    expected_names = _expected_array_names()
    try:
        with np.load(path, allow_pickle=False) as archive:
            if tuple(archive.files) != expected_names:
                raise ValueError("confirmatory NPZ array inventory drifted")
            arrays: dict[str, np.ndarray] = {}
            for name in expected_names:
                try:
                    raw = archive[name]
                except ValueError as error:
                    raise ValueError(
                        "confirmatory NPZ must not contain object arrays"
                    ) from error
                if raw.dtype.hasobject or raw.dtype != np.dtype(np.float64):
                    raise ValueError(
                        "confirmatory NPZ arrays must be non-object float64 arrays"
                    )
                expected_shape = (
                    (6,) if name.endswith("_initial_coefficients") else (9, 6)
                )
                if raw.shape != expected_shape or not np.all(np.isfinite(raw)):
                    raise ValueError(
                        f"confirmatory NPZ array {name} shape or finiteness drifted"
                    )
                if np.any(raw <= 0.0):
                    raise ValueError(
                        f"confirmatory NPZ array {name} must stay positive"
                    )
                arrays[name] = _readonly(raw, dtype=np.float64)
    except (OSError, EOFError) as error:
        raise ValueError("confirmatory NPZ could not be loaded") from error
    return MappingProxyType(arrays)


def _stored_endpoint_from_coefficients(
    coefficients: np.ndarray,
    *,
    system: object,
) -> dict[str, object]:
    ray = system.perron_ray
    target = ray / np.linalg.norm(ray)
    angles = np.asarray(
        [projective_ray_angle(row, ray) for row in coefficients],
        dtype=np.float64,
    )
    distances = np.asarray(
        [np.linalg.norm(row / np.linalg.norm(row) - target) for row in coefficients],
        dtype=np.float64,
    )
    couplings = coefficients[:, :, None, None] * system.matrix_direction
    construction = np.asarray(
        [
            scalarized_ray_construction_residual(level, system.matrix_direction)
            for level in couplings
        ],
        dtype=np.float64,
    )
    projection = np.outer(ray, ray) / float(np.dot(ray, ray))
    retained_vectors = np.asarray(
        [
            (np.eye(coefficients.shape[1]) - projection)
            @ difference
            / system.log_block_scale
            for difference in coefficients[1:] - coefficients[:-1]
        ],
        dtype=np.float64,
    )
    return {
        "projective_ray_angles": angles,
        "normalized_coupling_distances": distances,
        "scalarized_ray_construction_residuals": construction,
        "retained_beta_residuals": np.linalg.norm(retained_vectors, axis=1),
        "coefficient_conditioning": (
            np.max(coefficients, axis=1) / np.min(coefficients, axis=1)
        ),
        "basin_exit": bool(
            np.any(
                (coefficients < system.basin_lower)
                | (coefficients > system.basin_upper)
            )
        ),
        "matrix_condition": float(np.linalg.cond(system.matrix_direction)),
    }


def _validate_endpoint_records(
    endpoints: Mapping[str, object],
    jobs: tuple[Mapping[str, object], ...],
    arrays: Mapping[str, np.ndarray],
    *,
    binding: ConfirmatorySourceBinding,
    config_hash: str,
) -> tuple[Mapping[str, object], ...]:
    if endpoints.get("schema_version") != (
        "gaussian-fixed-ray-confirmatory-endpoints-v1"
    ):
        raise ValueError("confirmatory endpoint schema drifted")
    records = _sequence(endpoints.get("records"), "confirmatory endpoint records")
    if len(records) != 40:
        raise ValueError("confirmatory endpoint inventory must contain 40 records")
    mapped_records = tuple(
        _mapping(record, "confirmatory endpoint record") for record in records
    )
    observed_ids = tuple(record.get("job_id") for record in mapped_records)
    if len(set(observed_ids)) != len(observed_ids):
        raise ValueError("confirmatory endpoint job IDs must be unique")
    if observed_ids != _JOB_IDS:
        raise ValueError("confirmatory endpoint job order drifted")

    system = build_preregistered_system()
    recorded_exchanges = 0
    recorded_retries = 0
    for job, record in zip(jobs, mapped_records):
        job_id = str(job["job_id"])
        expected_role = (
            "confirmatory_primary" if job_id.startswith("C") else "confirmatory_holdout"
        )
        if (
            record.get("job_id") != job_id
            or record.get("master_seed") != job["master_seed"]
            or record.get("role") != expected_role
            or record.get("source_revision") != binding.scientific_revision
            or record.get("config_sha256") != config_hash
            or record.get("schema_version") != "gaussian-fixed-ray-confirmatory-job-v1"
            or record.get("terminal_status") != "completed"
            or record.get("scientific_analysis_eligibility") is not True
        ):
            raise ValueError(f"confirmatory endpoint binding drifted for {job_id}")
        worker_exchanges = record.get("worker_exchange_count")
        outer_attempts = record.get("outer_attempt_count")
        retry_lineage = record.get("retry_lineage")
        if (
            type(worker_exchanges) is not int
            or worker_exchanges != 16
            or type(outer_attempts) is not int
            or outer_attempts != 1
            or retry_lineage != [{"outer_attempt": 1, "parent_attempt": None}]
        ):
            raise ValueError(f"recorded execution metadata drifted for {job_id}")
        recorded_exchanges += worker_exchanges
        recorded_retries += max(0, outer_attempts - 1)

        initial = _finite_array(
            record.get("initial_coefficients"),
            shape=(6,),
            label=f"{job_id} endpoint initial coefficients",
        )
        stored_initial = arrays[f"{job_id}_initial_coefficients"]
        if not np.array_equal(initial, stored_initial):
            raise ValueError(f"{job_id} endpoint and NPZ initials drifted")
        if (
            record.get("initial_coefficients_sha256")
            != sha256(stored_initial.tobytes(order="C")).hexdigest()
        ):
            raise ValueError(f"{job_id} initial-coefficient SHA-256 drifted")
        scheme_records = _mapping(record.get("schemes"), f"{job_id} schemes")
        if tuple(scheme_records) != _SCHEMES:
            raise ValueError(f"{job_id} scheme inventory drifted")
        coefficient_paths: dict[str, np.ndarray] = {}
        for scheme in _SCHEMES:
            coefficients = arrays[f"{job_id}_{scheme}_coefficients"]
            if not np.array_equal(coefficients[0], stored_initial):
                raise ValueError(f"{job_id} {scheme} trajectory initial drifted")
            coefficient_paths[scheme] = coefficients
            endpoint = _mapping(
                scheme_records[scheme],
                f"{job_id} {scheme} endpoint",
            )
            if (
                endpoint.get("rejected") is not False
                or endpoint.get("rejection_reason") is not None
                or type(endpoint.get("basin_exit")) is not bool
            ):
                raise ValueError(f"{job_id} {scheme} endpoint status drifted")
            reconstructed = _stored_endpoint_from_coefficients(
                coefficients,
                system=system,
            )
            for field, shape in {
                "projective_ray_angles": (9,),
                "normalized_coupling_distances": (9,),
                "scalarized_ray_construction_residuals": (9,),
                "retained_beta_residuals": (8,),
                "coefficient_conditioning": (9,),
            }.items():
                observed = _finite_array(
                    endpoint.get(field),
                    shape=shape,
                    label=f"{job_id} {scheme} {field}",
                )
                _compare_array(
                    observed,
                    reconstructed[field],
                    label=f"{job_id} {scheme} stored endpoint",
                )
            if endpoint["basin_exit"] is not reconstructed["basin_exit"]:
                raise ValueError(f"{job_id} {scheme} basin endpoint drifted")
            matrix_condition = endpoint.get("matrix_condition")
            if not isinstance(matrix_condition, (int, float)) or not math.isclose(
                float(matrix_condition),
                float(reconstructed["matrix_condition"]),
                rel_tol=0.0,
                abs_tol=CPU_REPLAY_ATOL,
            ):
                raise ValueError(f"{job_id} {scheme} matrix condition drifted")
        dispersion = _finite_array(
            record.get("blocking_scheme_dispersion"),
            shape=(9,),
            label=f"{job_id} blocking-scheme dispersion",
        )
        expected_dispersion = blocking_scheme_dispersion(
            coefficient_paths[_SCHEMES[0]],
            coefficient_paths[_SCHEMES[1]],
        )
        _compare_array(
            dispersion,
            expected_dispersion,
            label=f"{job_id} blocking-scheme dispersion",
        )
    if recorded_exchanges != 640 or recorded_retries != 0:
        raise ValueError("recorded execution metadata aggregate drifted")
    return mapped_records


def _validate_analysis_records(
    primary: Mapping[str, object],
    holdout: Mapping[str, object],
    records: tuple[Mapping[str, object], ...],
    *,
    binding: ConfirmatorySourceBinding,
    config_hash: str,
    primary_raw_sha256: str,
) -> None:
    job_table_hash = binding.scientific_payload_hashes[
        "job_table_canonical_json_sha256"
    ]
    primary_execution_hash = binding.complete_original_inventory[
        "primary_execution.json"
    ]["sha256"]
    if (
        primary.get("schema_version") != "gaussian-fixed-ray-primary-analysis-v1"
        or primary.get("primary_job_ids") != list(_PRIMARY_JOB_IDS)
        or primary.get("independent_job_count") != 30
        or primary.get("completed_job_count") != 30
        or primary.get("missing_job_ids") != []
        or primary.get("job_table_sha256") != job_table_hash
        or primary.get("primary_execution_sha256") != primary_execution_hash
        or primary.get("config_sha256") != config_hash
        or primary.get("source_revision") != binding.scientific_revision
        or primary.get("theorem_status") != "NUMERICAL"
        or primary.get("verification_state") != "CANDIDATE"
        or primary.get("mathematical_verification_state") != "INCONCLUSIVE"
        or primary.get("claim_origin") != "APPLICATION_SPECIFIC"
    ):
        raise ValueError("primary analysis binding drifted")
    if (
        holdout.get("schema_version") != "gaussian-fixed-ray-holdout-analysis-v1"
        or holdout.get("analysis_scope") != "descriptive_replication_only"
        or holdout.get("holdout_job_ids") != list(_HOLDOUT_JOB_IDS)
        or holdout.get("independent_job_count") != 10
        or holdout.get("job_table_sha256") != job_table_hash
        or holdout.get("primary_analysis_sha256") != primary_raw_sha256
        or holdout.get("theorem_status") != "NUMERICAL"
        or holdout.get("verification_state") != "CANDIDATE"
        or holdout.get("mathematical_verification_state") != "INCONCLUSIVE"
        or holdout.get("claim_origin") != "APPLICATION_SPECIFIC"
    ):
        raise ValueError("holdout analysis binding drifted")

    recomputed_primary = analyze_primary(
        records[:30],
        protocol_id=str(primary["protocol_id"]),
        job_table_sha256=str(job_table_hash),
        decision_stability=bool(primary["decision_stability"]),
        premises_passed=bool(primary["premises_passed"]),
        gpu_gate_complete=bool(primary["gpu_gate_complete"]),
        primary_execution_sha256=str(primary_execution_hash),
        config_sha256=config_hash,
        source_revision=binding.scientific_revision,
        accepted_gate_sha256=str(primary["accepted_gate_sha256"]),
    )
    _semantic_equal(
        primary,
        recomputed_primary,
        label="primary analysis",
        skip_hash_fields=True,
    )
    recomputed_holdout = analyze_holdout(
        records[30:],
        protocol_id=str(holdout["protocol_id"]),
        job_table_sha256=str(job_table_hash),
        primary_analysis_sha256=primary_raw_sha256,
    )
    _semantic_equal(
        holdout,
        recomputed_holdout,
        label="holdout analysis",
        skip_hash_fields=True,
    )


def _freeze_mapping(payload: Mapping[str, object], label: str) -> Mapping[str, object]:
    frozen = _freeze_json(payload, label=label)
    assert isinstance(frozen, Mapping)
    return frozen


def validate_scientific_extract(
    path: Path,
    binding: ConfirmatorySourceBinding,
) -> ValidatedConfirmatorySource:
    """Validate and defensively load the compact confirmatory source extract.

    The two omitted execution logs are checked only as hash-and-size inventory
    entries.  Their recorded 640-exchange and zero-retry facts are retained as
    source metadata; this function does not claim to revalidate those logs.
    """
    if not isinstance(binding, ConfirmatorySourceBinding):
        raise TypeError("binding must be a ConfirmatorySourceBinding")
    source_dir = Path(path).resolve()
    if not source_dir.is_dir():
        raise ValueError("scientific extract path must be a directory")
    for name in _OMITTED_EXECUTION_LOGS:
        if (source_dir / name).exists():
            raise ValueError(
                "hash-only execution logs must remain outside the compact extract"
            )

    raw_hashes: dict[str, str] = {}
    for name in binding.tracked_scientific_subset:
        owned_path = source_dir / name
        if owned_path.is_symlink() or not owned_path.is_file():
            raise ValueError(f"owned scientific source {name} is missing or linked")
        content = owned_path.read_bytes()
        expected = binding.complete_original_inventory[name]
        if (
            len(content) != expected["size_bytes"]
            or sha256(content).hexdigest() != expected["sha256"]
        ):
            raise ValueError(f"owned scientific source {name} hash or size drifted")
        raw_hashes[name] = sha256(content).hexdigest()

    config = _read_json(source_dir / "config.json", "config")
    job_table = _read_json(
        source_dir / "confirmatory_job_table.json",
        "confirmatory job table",
    )
    endpoints = _read_json(
        source_dir / "confirmatory_endpoints.json",
        "confirmatory endpoints",
    )
    primary = _read_json(source_dir / "primary_analysis.json", "primary analysis")
    holdout = _read_json(source_dir / "holdout_analysis.json", "holdout analysis")
    manifest = _read_json(source_dir / "manifest.json", "manifest")
    metrics = _read_json(source_dir / "metrics.json", "metrics")
    arrays = _load_arrays(source_dir / "confirmatory_arrays.npz")

    resolved_config = _mapping(config.get("resolved_config"), "resolved config")
    config_hash = sha256(_canonical_bytes(resolved_config)).hexdigest()
    theory = _mapping(resolved_config.get("theory"), "resolved theory config")
    if (
        config.get("config_hash") != config_hash
        or tuple(theory.get("blocking_schemes", ())) != _SCHEMES
        or theory.get("experiment") != "gaussian_fixed_ray"
        or theory.get("fixture") != "gaussian_fixed_ray_v1"
        or theory.get("matrix_dimension") != 2
        or theory.get("preregistration") != "2026-08-09-gaussian-fixed-ray-v1"
    ):
        raise ValueError("resolved confirmatory configuration drifted")

    jobs = _validate_job_table(job_table, binding)
    records = _validate_endpoint_records(
        endpoints,
        jobs,
        arrays,
        binding=binding,
        config_hash=config_hash,
    )
    _validate_analysis_records(
        primary,
        holdout,
        records,
        binding=binding,
        config_hash=config_hash,
        primary_raw_sha256=raw_hashes["primary_analysis.json"],
    )

    artifacts = _mapping(manifest.get("artifacts"), "manifest artifact inventory")
    provenance = _mapping(manifest.get("provenance"), "manifest provenance")
    input_hashes = _mapping(provenance.get("input_hashes"), "manifest input hashes")
    if (
        tuple(artifacts) != _ORIGINAL_INVENTORY_NAMES
        or any(artifacts[name] != "complete" for name in _ORIGINAL_INVENTORY_NAMES)
        or manifest.get("complete") is not True
        or manifest.get("config_hash") != config_hash
        or provenance.get("config_hash") != config_hash
        or provenance.get("git_commit") != binding.scientific_revision
        or provenance.get("git_dirty") is not False
        or provenance.get("confirmatory_executed") is not True
        or provenance.get("experiment_scope")
        != "gaussian_fixed_ray_confirmatory_40_job"
        or provenance.get("effective_dtype") != "float64"
        or input_hashes.get("job_table_sha256")
        != binding.scientific_payload_hashes["job_table_canonical_json_sha256"]
        or input_hashes.get("primary_analysis_sha256")
        != raw_hashes["primary_analysis.json"]
        or input_hashes.get("primary_execution_sha256")
        != binding.complete_original_inventory["primary_execution.json"]["sha256"]
        or input_hashes.get("resolved_config_sha256") != config_hash
    ):
        raise ValueError("manifest source binding drifted")
    classification = _mapping(
        metrics.get("confirmatory_primary_classification"),
        "confirmatory primary metric",
    )
    if (
        classification.get("status") != primary.get("classification")
        or classification.get("theorem_status") != "NUMERICAL"
        or classification.get("verification_state") != "CANDIDATE"
        or classification.get("claim_origin") != "APPLICATION_SPECIFIC"
        or classification.get("assessment_scope") != "implementation_check"
    ):
        raise ValueError("confirmatory primary metric drifted")

    recorded_metadata = MappingProxyType(
        {
            "recorded_worker_exchange_count": 640,
            "recorded_retried_job_count": 0,
            "omitted_execution_logs_revalidated": False,
            "omitted_execution_logs": _OMITTED_EXECUTION_LOGS,
        }
    )
    return ValidatedConfirmatorySource(
        source_dir=source_dir,
        binding=binding,
        scientific_revision=binding.scientific_revision,
        diagnostic_revision=binding.diagnostic_revision,
        job_ids=_JOB_IDS,
        schemes=_SCHEMES,
        jobs=tuple(_freeze_mapping(job, "confirmatory job") for job in jobs),
        arrays=arrays,
        config=_freeze_mapping(config, "config"),
        job_table=_freeze_mapping(job_table, "job table"),
        endpoint_records=tuple(
            _freeze_mapping(record, "confirmatory endpoint") for record in records
        ),
        primary_analysis=_freeze_mapping(primary, "primary analysis"),
        holdout_analysis=_freeze_mapping(holdout, "holdout analysis"),
        manifest=_freeze_mapping(manifest, "manifest"),
        metrics=_freeze_mapping(metrics, "metrics"),
        recorded_execution_metadata=recorded_metadata,
    )


def _copy_trajectory(trajectory: FixedRayTrajectory) -> FixedRayTrajectory:
    return FixedRayTrajectory(
        scheme=trajectory.scheme,
        coefficients=_readonly(trajectory.coefficients, dtype=np.float64),
        coupling_matrices=_readonly(trajectory.coupling_matrices, dtype=np.float64),
        projective_ray_angles=_readonly(
            trajectory.projective_ray_angles,
            dtype=np.float64,
        ),
        normalized_coupling_distances=_readonly(
            trajectory.normalized_coupling_distances,
            dtype=np.float64,
        ),
        scalarized_ray_construction_residuals=_readonly(
            trajectory.scalarized_ray_construction_residuals,
            dtype=np.float64,
        ),
        retained_beta_residual_vectors=_readonly(
            trajectory.retained_beta_residual_vectors,
            dtype=np.float64,
        ),
        retained_beta_residuals=_readonly(
            trajectory.retained_beta_residuals,
            dtype=np.float64,
        ),
        basin_exits=_readonly(trajectory.basin_exits, dtype=np.bool_),
        coefficient_conditioning=_readonly(
            trajectory.coefficient_conditioning,
            dtype=np.float64,
        ),
        matrix_condition=float(trajectory.matrix_condition),
    )


def _validate_replayed_trajectory(
    trajectory: FixedRayTrajectory,
    *,
    source: ValidatedConfirmatorySource,
    record: Mapping[str, object],
    job_id: str,
    scheme: str,
) -> dict[str, float]:
    if not isinstance(trajectory, FixedRayTrajectory) or trajectory.scheme != scheme:
        raise ValueError(
            f"deterministic replay returned an invalid {job_id} {scheme} result"
        )
    expected_shapes = {
        "coefficients": (9, 6),
        "coupling_matrices": (9, 6, 2, 2),
        "projective_ray_angles": (9,),
        "normalized_coupling_distances": (9,),
        "scalarized_ray_construction_residuals": (9,),
        "retained_beta_residual_vectors": (8, 6),
        "retained_beta_residuals": (8,),
        "basin_exits": (9,),
        "coefficient_conditioning": (9,),
    }
    for field, shape in expected_shapes.items():
        values = np.asarray(getattr(trajectory, field))
        if values.shape != shape:
            raise ValueError(
                f"deterministic replay {job_id} {scheme} {field} shape drifted"
            )
        if field != "basin_exits" and not np.all(np.isfinite(values)):
            raise ValueError(
                f"deterministic replay {job_id} {scheme} {field} became nonfinite"
            )
    scheme_record = _mapping(record["schemes"], f"{job_id} schemes")[scheme]
    scheme_endpoint = _mapping(scheme_record, f"{job_id} {scheme} endpoint")
    errors = {
        "coefficients": _compare_array(
            trajectory.coefficients,
            source.arrays[f"{job_id}_{scheme}_coefficients"],
            label=f"deterministic replay {job_id} {scheme} coefficients",
        ),
        "projective_ray_angles": _compare_array(
            trajectory.projective_ray_angles,
            scheme_endpoint["projective_ray_angles"],
            label=f"deterministic replay {job_id} {scheme} projective angles",
        ),
        "normalized_coupling_distances": _compare_array(
            trajectory.normalized_coupling_distances,
            scheme_endpoint["normalized_coupling_distances"],
            label=f"deterministic replay {job_id} {scheme} normalized distances",
        ),
        "scalarized_ray_construction_residuals": _compare_array(
            trajectory.scalarized_ray_construction_residuals,
            scheme_endpoint["scalarized_ray_construction_residuals"],
            label=f"deterministic replay {job_id} {scheme} construction residuals",
        ),
        "retained_beta_residuals": _compare_array(
            trajectory.retained_beta_residuals,
            scheme_endpoint["retained_beta_residuals"],
            label=f"deterministic replay {job_id} {scheme} retained beta residuals",
        ),
        "coefficient_conditioning": _compare_array(
            trajectory.coefficient_conditioning,
            scheme_endpoint["coefficient_conditioning"],
            label=f"deterministic replay {job_id} {scheme} coefficient conditioning",
        ),
    }
    if bool(np.any(trajectory.basin_exits)) is not scheme_endpoint["basin_exit"]:
        raise ValueError(f"deterministic replay {job_id} {scheme} basin status drifted")
    if not math.isclose(
        trajectory.matrix_condition,
        float(scheme_endpoint["matrix_condition"]),
        rel_tol=0.0,
        abs_tol=CPU_REPLAY_ATOL,
    ):
        raise ValueError(
            f"deterministic replay {job_id} {scheme} matrix condition drifted"
        )
    return errors


def replay_confirmatory_diagnostics(
    source: ValidatedConfirmatorySource,
    *,
    iterate_fn: Callable[..., FixedRayTrajectory] = iterate_fixed_ray,
) -> ReplayResult:
    """Deterministically replay all 40 jobs through both frozen schemes.

    Exactly 80 calls are made to ``iterate_fn``.  Initial coefficients are
    regenerated from each master-seed/job-ID pair rather than loaded as replay
    outputs.  Stored trajectories and endpoints are comparison targets only.
    """
    if not isinstance(source, ValidatedConfirmatorySource):
        raise TypeError("source must be a ValidatedConfirmatorySource")
    if not callable(iterate_fn):
        raise TypeError("iterate_fn must be callable")
    system = build_preregistered_system()
    call_count = 0
    maxima = {field: 0.0 for field in _REPLAY_FIELDS}
    maxima["blocking_scheme_dispersion"] = 0.0
    replayed: dict[str, Mapping[str, FixedRayTrajectory]] = {}
    for job, record, job_id in zip(
        source.jobs, source.endpoint_records, source.job_ids
    ):
        master_seed = job.get("master_seed")
        if type(master_seed) is not int or job.get("job_id") != job_id:
            raise ValueError(f"deterministic replay job binding drifted for {job_id}")
        regenerated = generate_initial_coefficients(master_seed, job_id)
        stored_initial = source.arrays[f"{job_id}_initial_coefficients"]
        if not np.array_equal(regenerated, stored_initial):
            raise ValueError(
                f"deterministic replay initial regeneration drifted for {job_id}"
            )
        per_scheme: dict[str, FixedRayTrajectory] = {}
        for scheme in source.schemes:
            iterator_initial = _readonly(regenerated, dtype=np.float64)
            trajectory = iterate_fn(
                system,
                iterator_initial,
                scheme=scheme,
                steps=8,
            )
            call_count += 1
            errors = _validate_replayed_trajectory(
                trajectory,
                source=source,
                record=record,
                job_id=job_id,
                scheme=scheme,
            )
            for field, error in errors.items():
                maxima[field] = max(maxima[field], error)
            per_scheme[scheme] = _copy_trajectory(trajectory)
        dispersion = blocking_scheme_dispersion(
            per_scheme[_SCHEMES[0]].coefficients,
            per_scheme[_SCHEMES[1]].coefficients,
        )
        dispersion_error = _compare_array(
            dispersion,
            record["blocking_scheme_dispersion"],
            label=f"deterministic replay {job_id} blocking-scheme dispersion",
        )
        maxima["blocking_scheme_dispersion"] = max(
            maxima["blocking_scheme_dispersion"],
            dispersion_error,
        )
        replayed[job_id] = MappingProxyType(per_scheme)
    if call_count != 80:
        raise ValueError(
            "deterministic replay must invoke the frozen iterator 80 times"
        )
    return ReplayResult(
        operation="deterministic_replay",
        scientific_revision=source.scientific_revision,
        diagnostic_revision=source.diagnostic_revision,
        call_count=call_count,
        cpu_replay_atol=CPU_REPLAY_ATOL,
        trajectories=MappingProxyType(replayed),
        max_absolute_errors=MappingProxyType(maxima),
        recorded_execution_metadata=source.recorded_execution_metadata,
    )


__all__ = [
    "CPU_REPLAY_ATOL",
    "ConfirmatorySourceBinding",
    "ReplayResult",
    "ValidatedConfirmatorySource",
    "replay_confirmatory_diagnostics",
    "validate_scientific_extract",
]
