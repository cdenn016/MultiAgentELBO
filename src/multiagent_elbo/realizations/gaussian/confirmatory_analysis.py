"""Pure statistics for the preregistered Gaussian fixed-ray confirmation."""

from __future__ import annotations

import hashlib
import re
from math import comb, isfinite
from typing import Mapping

import numpy as np


SECONDARY_ENDPOINT_IDS = (
    "construction_residual",
    "retained_beta_trend",
    "basin_exit_rate",
    "scheme_dispersion",
    "conditioning_trend",
    "rejection_rate",
)
_SCHEME_IDS = ("adjacent_pairs", "balanced_alternating")
_SCALES_4_8 = np.arange(4.0, 9.0, dtype=np.float64)
_SHA256_HEX = re.compile(r"[0-9a-f]{64}")
_CENSORED_VALUES = {
    "primary_angle_slope": float(np.pi),
    "scale_8_normalized_distance": 2.0,
    "construction_residual": 1.0,
    "retained_beta_trend": 1.0,
    "scheme_dispersion": 2.0,
    "conditioning_trend": float(np.log(1.0e12)),
}


def _finite_vector(values: object, *, length: int, label: str) -> np.ndarray:
    vector = np.asarray(values, dtype=np.float64)
    if vector.shape != (length,) or not np.all(np.isfinite(vector)):
        raise ValueError(f"{label} must be a finite vector of length {length}")
    return vector


def _ols_slope(values: np.ndarray) -> float:
    centered = _SCALES_4_8 - float(np.mean(_SCALES_4_8))
    return float(np.dot(centered, values) / np.dot(centered, centered))


def exact_sign_pvalue(values: object, boundary: float) -> float:
    """Return the conservative lower-sided exact sign-test p-value."""
    sample = np.asarray(values, dtype=np.float64)
    if sample.ndim != 1 or sample.size == 0 or not np.all(np.isfinite(sample)):
        raise ValueError("sign-test values must be a nonempty finite vector")
    if not isfinite(float(boundary)):
        raise ValueError("sign-test boundary must be finite")
    favorable = int(np.count_nonzero(sample < float(boundary)))
    trials = int(sample.size)
    return float(sum(comb(trials, count) for count in range(favorable, trials + 1)) / (2**trials))


def exact_binomial_lower_tail(
    events: int, trials: int, boundary_probability: float
) -> float:
    """Return P(X <= events) at the composite-null binomial boundary."""
    if type(events) is not int or type(trials) is not int:
        raise ValueError("binomial counts must be integers")
    if trials <= 0 or events < 0 or events > trials:
        raise ValueError("binomial counts are outside the admitted range")
    probability = float(boundary_probability)
    if not isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError("binomial boundary probability must lie in [0, 1]")
    return float(
        sum(
            comb(trials, count)
            * probability**count
            * (1.0 - probability) ** (trials - count)
            for count in range(events + 1)
        )
    )


def holm_adjust(
    pvalues: Mapping[str, float], *, alpha: float = 0.05
) -> list[dict[str, object]]:
    """Adjust the frozen six-endpoint family using Holm's step-down method."""
    if set(pvalues) != set(SECONDARY_ENDPOINT_IDS):
        raise ValueError("Holm input must contain exactly six frozen endpoints")
    if not isfinite(float(alpha)) or not 0.0 < float(alpha) < 1.0:
        raise ValueError("Holm alpha must lie strictly between zero and one")
    raw: dict[str, float] = {}
    for endpoint_id in SECONDARY_ENDPOINT_IDS:
        value = float(pvalues[endpoint_id])
        if not isfinite(value) or not 0.0 <= value <= 1.0:
            raise ValueError("Holm p-values must be finite and lie in [0, 1]")
        raw[endpoint_id] = value

    ordered = sorted(raw.items(), key=lambda item: (item[1], item[0]))
    adjusted_by_id: dict[str, float] = {}
    rank_by_id: dict[str, int] = {}
    running = 0.0
    family_size = len(ordered)
    for index, (endpoint_id, value) in enumerate(ordered):
        running = max(running, (family_size - index) * value)
        adjusted_by_id[endpoint_id] = min(1.0, running)
        rank_by_id[endpoint_id] = index + 1

    return [
        {
            "endpoint_id": endpoint_id,
            "unadjusted_p": raw[endpoint_id],
            "adjusted_p": adjusted_by_id[endpoint_id],
            "rank": rank_by_id[endpoint_id],
            "rejected": adjusted_by_id[endpoint_id] <= float(alpha),
        }
        for endpoint_id in SECONDARY_ENDPOINT_IDS
    ]


def summarize_paired_job(record: Mapping[str, object]) -> dict[str, object]:
    """Reduce one two-scheme job to one conservative independent summary."""
    if record.get("scientific_analysis_eligibility") is not True:
        raise ValueError("job is not eligible for scientific analysis")
    job_id = record.get("job_id")
    role = record.get("role")
    if not isinstance(job_id, str) or role not in {
        "confirmatory_primary",
        "confirmatory_holdout",
    }:
        raise ValueError("job identity or role is invalid")
    schemes = record.get("schemes")
    if not isinstance(schemes, Mapping) or set(schemes) != set(_SCHEME_IDS):
        raise ValueError("job must contain exactly the two frozen schemes")

    angle_slopes: list[float] = []
    distances: list[float] = []
    construction: list[float] = []
    beta_slopes: list[float] = []
    conditioning_slopes: list[float] = []
    basin_events: list[bool] = []
    rejection_events: list[bool] = []
    censored = False
    for scheme_id in _SCHEME_IDS:
        scheme = schemes[scheme_id]
        if not isinstance(scheme, Mapping):
            raise ValueError("scheme record must be a mapping")
        basin_exit = scheme.get("basin_exit")
        rejected = scheme.get("rejected")
        if type(basin_exit) is not bool or type(rejected) is not bool:
            raise ValueError("basin and rejection events must be Boolean")
        basin_events.append(basin_exit)
        rejection_events.append(rejected)
        continuous_fields = (
            "projective_ray_angles",
            "normalized_coupling_distances",
            "retained_beta_residuals",
            "scalarized_ray_construction_residuals",
            "coefficient_conditioning",
        )
        continuous_available = all(scheme.get(field) is not None for field in continuous_fields)
        if rejected and not continuous_available:
            censored = True
            continue
        if not continuous_available:
            raise ValueError("nonrejected scheme is missing a continuous endpoint")
        angles = _finite_vector(
            scheme.get("projective_ray_angles"),
            length=9,
            label="projective ray angles",
        )
        normalized = _finite_vector(
            scheme.get("normalized_coupling_distances"),
            length=9,
            label="normalized coupling distances",
        )
        beta = _finite_vector(
            scheme.get("retained_beta_residuals"),
            length=8,
            label="retained beta residuals",
        )
        conditioning = _finite_vector(
            scheme.get("coefficient_conditioning"),
            length=9,
            label="coefficient conditioning",
        )
        if np.any(conditioning <= 0.0):
            raise ValueError("coefficient conditioning must be strictly positive")
        residuals = np.asarray(
            scheme.get("scalarized_ray_construction_residuals"),
            dtype=np.float64,
        )
        if residuals.size == 0 or not np.all(np.isfinite(residuals)):
            raise ValueError("construction residuals must be finite and nonempty")
        angle_slopes.append(_ols_slope(angles[4:9]))
        distances.append(float(normalized[8]))
        construction.append(float(np.max(residuals)))
        beta_slopes.append(_ols_slope(beta[3:8]))
        conditioning_slopes.append(_ols_slope(np.log(conditioning[4:9])))
    dispersion_value: float | None
    if censored:
        dispersion_value = None
    else:
        dispersion = _finite_vector(
            record.get("blocking_scheme_dispersion"),
            length=9,
            label="blocking scheme dispersion",
        )
        dispersion_value = float(dispersion[8])
    return {
        "job_id": job_id,
        "role": role,
        "primary_angle_slope": None if censored else max(angle_slopes),
        "scale_8_normalized_distance": None if censored else max(distances),
        "construction_residual": None if censored else max(construction),
        "retained_beta_trend": None if censored else max(beta_slopes),
        "basin_exit": any(basin_events),
        "scheme_dispersion": dispersion_value,
        "conditioning_trend": None if censored else max(conditioning_slopes),
        "rejected": any(rejection_events),
        "continuous_endpoint_censored_worst_case": censored,
        "independent_observation_count": 1,
    }


def bootstrap_seed(protocol_id: str, job_table_sha256: str, endpoint_id: str) -> int:
    """Derive an endpoint-bound unsigned 64-bit bootstrap seed."""
    if not isinstance(protocol_id, str) or not protocol_id:
        raise ValueError("bootstrap protocol ID must be nonempty")
    if _SHA256_HEX.fullmatch(job_table_sha256) is None:
        raise ValueError("bootstrap job-table SHA-256 is invalid")
    if not isinstance(endpoint_id, str) or not endpoint_id:
        raise ValueError("bootstrap endpoint ID must be nonempty")
    payload = "\0".join(
        (
            protocol_id,
            job_table_sha256,
            "confirmatory-analysis-bootstrap-v1",
            endpoint_id,
        )
    ).encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big", signed=False)


def _bootstrap_statistics(
    values: object, *, seed: int, resamples: int
) -> tuple[np.ndarray, dict[str, object]]:
    sample = np.asarray(values, dtype=np.float64)
    if sample.ndim != 1 or sample.size == 0 or not np.all(np.isfinite(sample)):
        raise ValueError("bootstrap values must be a nonempty finite vector")
    if type(seed) is not int or not 0 <= seed < 2**64:
        raise ValueError("bootstrap seed must be an unsigned 64-bit integer")
    if type(resamples) is not int or resamples <= 0:
        raise ValueError("bootstrap resample count must be positive")
    generator = np.random.Generator(np.random.PCG64(seed))
    indices = generator.integers(
        0,
        sample.size,
        size=(resamples, sample.size),
        dtype=np.int64,
    )
    resampled = np.sort(sample[indices], axis=1)
    midpoint = resampled.shape[1] // 2
    if resampled.shape[1] % 2:
        statistics = resampled[:, midpoint]
    else:
        lower = resampled[:, midpoint - 1]
        upper = resampled[:, midpoint]
        statistics = lower + (upper - lower) / 2.0
    statistics = statistics.astype(np.float64, copy=False)
    return statistics, {
        "seed_u64": seed,
        "resamples": resamples,
        "trials": int(sample.size),
        "input_sha256": hashlib.sha256(sample.tobytes(order="C")).hexdigest(),
        "resample_indices_sha256": hashlib.sha256(
            indices.tobytes(order="C")
        ).hexdigest(),
        "bootstrap_statistics_sha256": hashlib.sha256(
            statistics.tobytes(order="C")
        ).hexdigest(),
    }


def percentile_interval(
    values: object, *, seed: int, resamples: int = 10_000
) -> dict[str, object]:
    """Return a deterministic whole-job percentile interval for a median."""
    sample = np.asarray(values, dtype=np.float64)
    statistics, identity = _bootstrap_statistics(
        sample, seed=seed, resamples=resamples
    )
    return {
        "estimate": float(_safe_median(sample)),
        "lower": float(np.percentile(statistics, 2.5)),
        "upper": float(np.percentile(statistics, 97.5)),
        **identity,
    }


def _safe_median(values: np.ndarray) -> float:
    ordered = np.sort(np.asarray(values, dtype=np.float64))
    midpoint = ordered.size // 2
    if ordered.size % 2:
        return float(ordered[midpoint])
    lower = float(ordered[midpoint - 1])
    upper = float(ordered[midpoint])
    return lower + (upper - lower) / 2.0


def analyze_primary(
    job_records: object,
    *,
    protocol_id: str,
    job_table_sha256: str,
    decision_stability: bool,
    premises_passed: bool,
    gpu_gate_complete: bool,
    primary_execution_sha256: str | None = None,
    config_sha256: str | None = None,
    source_revision: str | None = None,
    accepted_gate_sha256: str | None = None,
) -> dict[str, object]:
    """Analyze exactly the 30 frozen primary jobs without pseudo-replication."""
    if type(decision_stability) is not bool or type(premises_passed) is not bool:
        raise ValueError("primary analysis decision flags must be Boolean")
    if type(gpu_gate_complete) is not bool:
        raise ValueError("primary analysis GPU gate flag must be Boolean")
    if (
        not isinstance(job_records, (list, tuple))
        or len(job_records) == 0
        or len(job_records) > 30
    ):
        raise ValueError("primary analysis requires between one and 30 job records")
    records_by_id: dict[str, Mapping[str, object]] = {}
    terminal_missing_ids: set[str] = set()
    for record in job_records:
        if not isinstance(record, Mapping):
            raise ValueError("primary job record must be a mapping")
        job_id = record.get("job_id")
        terminal_status = record.get("terminal_status", "completed")
        is_missing = terminal_status == "missing"
        if (
            not isinstance(job_id, str)
            or record.get("role") != "confirmatory_primary"
            or terminal_status not in {"completed", "rejected", "missing"}
            or (
                record.get("scientific_analysis_eligibility")
                is not (False if is_missing else True)
            )
        ):
            raise ValueError("primary analysis received a non-primary record")
        if job_id in records_by_id:
            raise ValueError("primary analysis job IDs must be unique")
        records_by_id[job_id] = record
        if is_missing:
            terminal_missing_ids.add(job_id)
    expected_ids = [f"C{index:03d}" for index in range(1, 31)]
    if not set(records_by_id).issubset(set(expected_ids)):
        raise ValueError("primary analysis job table is drifted")
    missing_job_ids = [
        job_id
        for job_id in expected_ids
        if job_id not in records_by_id or job_id in terminal_missing_ids
    ]
    ordered_records = [
        records_by_id[job_id]
        for job_id in expected_ids
        if job_id in records_by_id and job_id not in terminal_missing_ids
    ]
    summaries = [summarize_paired_job(record) for record in ordered_records]
    censored_count = int(
        sum(
            bool(summary["continuous_endpoint_censored_worst_case"])
            for summary in summaries
        )
    )
    if not summaries:
        secondary_tests = holm_adjust(
            {endpoint_id: 1.0 for endpoint_id in SECONDARY_ENDPOINT_IDS}
        )
        for row in secondary_tests:
            row["available_trials"] = 0
            row["test_available"] = False
        result: dict[str, object] = {
            "schema_version": "gaussian-fixed-ray-primary-analysis-v1",
            "protocol_id": protocol_id,
            "job_table_sha256": job_table_sha256,
            "primary_job_ids": expected_ids,
            "independent_job_count": 30,
            "completed_job_count": 0,
            "missing_job_ids": missing_job_ids,
            "censored_worst_case_count": 0,
            "paired_reduction": "least_favorable_across_two_frozen_schemes",
            "primary_endpoint": None,
            "supporting_distance": None,
            "scheme_dispersion_interval": None,
            "secondary_tests": secondary_tests,
            "basin_exit_events": 0,
            "basin_exit_rate": None,
            "rejection_events": 0,
            "rejection_rate": None,
            "decision_stability": decision_stability,
            "premises_passed": premises_passed,
            "gpu_gate_complete": gpu_gate_complete,
            "distinct_projective_rays": False,
            "primary_interval_half_width": None,
            "classification": "inconclusive",
            "theorem_status": "NUMERICAL",
            "verification_state": "CANDIDATE",
            "mathematical_verification_state": "INCONCLUSIVE",
            "claim_origin": "APPLICATION_SPECIFIC",
            "job_summaries": [],
        }
        for name, value in {
            "primary_execution_sha256": primary_execution_sha256,
            "config_sha256": config_sha256,
            "source_revision": source_revision,
            "accepted_gate_sha256": accepted_gate_sha256,
        }.items():
            if value is not None:
                result[name] = value
        return result
    def values(name: str) -> np.ndarray:
        observed = [
            _CENSORED_VALUES[name] if summary[name] is None else summary[name]
            for summary in summaries
        ]
        return np.asarray(observed, dtype=np.float64)

    primary_values = values("primary_angle_slope")
    distance_values = values("scale_8_normalized_distance")
    dispersion_values = values("scheme_dispersion")
    primary_seed = bootstrap_seed(protocol_id, job_table_sha256, "primary_angle_slope")
    primary_statistics, primary_identity = _bootstrap_statistics(
        primary_values, seed=primary_seed, resamples=10_000
    )
    primary_estimate = _safe_median(primary_values)
    primary_interval = {
        "estimate": primary_estimate,
        "lower": float(np.percentile(primary_statistics, 2.5)),
        "upper": float(np.percentile(primary_statistics, 97.5)),
        **primary_identity,
    }
    primary_boundary = -0.02
    null_statistics = primary_statistics - primary_estimate + primary_boundary
    lower_count = int(np.count_nonzero(null_statistics <= primary_estimate))
    upper_count = int(np.count_nonzero(null_statistics >= primary_estimate))
    primary_pvalue = min(
        1.0,
        2.0 * (min(lower_count, upper_count) + 1.0) / (len(null_statistics) + 1.0),
    )
    distance_interval = percentile_interval(
        distance_values,
        seed=bootstrap_seed(protocol_id, job_table_sha256, "supporting_distance"),
    )
    dispersion_interval = percentile_interval(
        dispersion_values,
        seed=bootstrap_seed(protocol_id, job_table_sha256, "scheme_dispersion"),
    )

    basin_events = int(sum(bool(summary["basin_exit"]) for summary in summaries))
    rejection_events = int(sum(bool(summary["rejected"]) for summary in summaries))
    available_trials = len(summaries)
    raw_secondary = {
        "construction_residual": exact_sign_pvalue(
            values("construction_residual"), 1.0e-12
        ),
        "retained_beta_trend": exact_sign_pvalue(
            values("retained_beta_trend"), 0.0
        ),
        "basin_exit_rate": exact_binomial_lower_tail(
            basin_events, available_trials, 0.05
        ),
        "scheme_dispersion": exact_sign_pvalue(dispersion_values, 0.02),
        "conditioning_trend": exact_sign_pvalue(
            values("conditioning_trend"), 0.0
        ),
        "rejection_rate": exact_binomial_lower_tail(
            rejection_events, available_trials, 0.05
        ),
    }
    secondary_tests = holm_adjust(raw_secondary)
    for row in secondary_tests:
        row["available_trials"] = available_trials
        row["test_available"] = True
    basin_rate = basin_events / available_trials
    rejection_rate = rejection_events / available_trials
    distinct_rays = float(dispersion_interval["lower"]) > 0.05
    interval_half_width = (
        float(primary_interval["upper"]) - float(primary_interval["lower"])
    ) / 2.0
    support = (
        float(primary_interval["upper"]) <= -0.02
        and float(distance_interval["estimate"]) <= 0.05
        and float(dispersion_interval["upper"]) <= 0.02
        and basin_rate <= 0.05
        and rejection_rate <= 0.05
        and decision_stability
        and premises_passed
        and gpu_gate_complete
    )
    counterevidence = (
        float(primary_interval["lower"]) >= 0.0
        or distinct_rays
        or basin_rate > 0.20
        or rejection_rate > 0.20
        or distinct_rays
    )
    forced_inconclusive = (
        interval_half_width > 0.02
        or bool(missing_job_ids)
        or not decision_stability
        or not premises_passed
        or not gpu_gate_complete
    )
    if support and not counterevidence and not forced_inconclusive:
        classification = "support"
    elif counterevidence and not forced_inconclusive:
        classification = "counterevidence"
    else:
        classification = "inconclusive"

    result: dict[str, object] = {
        "schema_version": "gaussian-fixed-ray-primary-analysis-v1",
        "protocol_id": protocol_id,
        "job_table_sha256": job_table_sha256,
        "primary_job_ids": expected_ids,
        "independent_job_count": 30,
        "completed_job_count": len(summaries),
        "missing_job_ids": missing_job_ids,
        "censored_worst_case_count": censored_count,
        "paired_reduction": "least_favorable_across_two_frozen_schemes",
        "primary_endpoint": {
            **primary_interval,
            "null_boundary": primary_boundary,
            "two_sided_p": primary_pvalue,
        },
        "supporting_distance": distance_interval,
        "scheme_dispersion_interval": dispersion_interval,
        "secondary_tests": secondary_tests,
        "basin_exit_events": basin_events,
        "basin_exit_rate": basin_rate,
        "rejection_events": rejection_events,
        "rejection_rate": rejection_rate,
        "decision_stability": decision_stability,
        "premises_passed": premises_passed,
        "gpu_gate_complete": gpu_gate_complete,
        "distinct_projective_rays": distinct_rays,
        "primary_interval_half_width": interval_half_width,
        "classification": classification,
        "theorem_status": "NUMERICAL",
        "verification_state": "CANDIDATE",
        "mathematical_verification_state": "INCONCLUSIVE",
        "claim_origin": "APPLICATION_SPECIFIC",
        "job_summaries": summaries,
    }
    bound_fields = {
        "primary_execution_sha256": primary_execution_sha256,
        "config_sha256": config_sha256,
        "source_revision": source_revision,
        "accepted_gate_sha256": accepted_gate_sha256,
    }
    for name, value in bound_fields.items():
        if value is not None:
            result[name] = value
    return result


def analyze_holdout(
    job_records: object,
    *,
    protocol_id: str,
    job_table_sha256: str,
    primary_analysis_sha256: str,
) -> dict[str, object]:
    """Apply the frozen estimators once as descriptive holdout replication."""
    if _SHA256_HEX.fullmatch(primary_analysis_sha256) is None:
        raise ValueError("holdout primary-analysis SHA-256 is invalid")
    if not isinstance(job_records, (list, tuple)) or len(job_records) != 10:
        raise ValueError("holdout analysis requires exactly ten job records")
    records_by_id: dict[str, Mapping[str, object]] = {}
    for record in job_records:
        if not isinstance(record, Mapping):
            raise ValueError("holdout job record must be a mapping")
        job_id = record.get("job_id")
        if (
            not isinstance(job_id, str)
            or record.get("role") != "confirmatory_holdout"
            or record.get("scientific_analysis_eligibility") is not True
            or job_id in records_by_id
        ):
            raise ValueError("holdout analysis received an ineligible record")
        records_by_id[job_id] = record
    expected_ids = [f"H{index:03d}" for index in range(1, 11)]
    if set(records_by_id) != set(expected_ids):
        raise ValueError("holdout analysis job table is incomplete or drifted")
    summaries = [
        summarize_paired_job(records_by_id[job_id]) for job_id in expected_ids
    ]
    worst_case = np.finfo(np.float64).max

    def endpoint_interval(name: str, endpoint_id: str) -> dict[str, object]:
        sample = np.asarray(
            [
                worst_case if summary[name] is None else summary[name]
                for summary in summaries
            ],
            dtype=np.float64,
        )
        return percentile_interval(
            sample,
            seed=bootstrap_seed(protocol_id, job_table_sha256, endpoint_id),
        )

    primary_endpoint = endpoint_interval(
        "primary_angle_slope", "holdout_primary_angle_slope"
    )
    supporting_distance = endpoint_interval(
        "scale_8_normalized_distance", "holdout_supporting_distance"
    )
    dispersion = endpoint_interval(
        "scheme_dispersion", "holdout_scheme_dispersion"
    )
    continuous_endpoints = {
        "construction_residual": endpoint_interval(
            "construction_residual", "holdout_construction_residual"
        ),
        "retained_beta_trend": endpoint_interval(
            "retained_beta_trend", "holdout_retained_beta_trend"
        ),
        "conditioning_trend": endpoint_interval(
            "conditioning_trend", "holdout_conditioning_trend"
        ),
    }
    basin_events = int(sum(bool(summary["basin_exit"]) for summary in summaries))
    rejection_events = int(sum(bool(summary["rejected"]) for summary in summaries))
    return {
        "schema_version": "gaussian-fixed-ray-holdout-analysis-v1",
        "analysis_scope": "descriptive_replication_only",
        "protocol_id": protocol_id,
        "job_table_sha256": job_table_sha256,
        "primary_analysis_sha256": primary_analysis_sha256,
        "holdout_job_ids": expected_ids,
        "independent_job_count": 10,
        "paired_reduction": "least_favorable_across_two_frozen_schemes",
        "primary_endpoint": primary_endpoint,
        "supporting_distance": supporting_distance,
        "scheme_dispersion_interval": dispersion,
        "continuous_endpoints": continuous_endpoints,
        "basin_exit_events": basin_events,
        "basin_exit_rate": basin_events / 10.0,
        "rejection_events": rejection_events,
        "rejection_rate": rejection_events / 10.0,
        "threshold_replication": {
            "primary_upper_at_most_minus_0_02": float(primary_endpoint["upper"])
            <= -0.02,
            "distance_median_at_most_0_05": float(supporting_distance["estimate"])
            <= 0.05,
            "dispersion_upper_at_most_0_02": float(dispersion["upper"]) <= 0.02,
            "basin_exit_rate_at_most_0_05": basin_events / 10.0 <= 0.05,
            "rejection_rate_at_most_0_05": rejection_events / 10.0 <= 0.05,
        },
        "theorem_status": "NUMERICAL",
        "verification_state": "CANDIDATE",
        "claim_origin": "APPLICATION_SPECIFIC",
        "job_summaries": summaries,
    }


__all__ = [
    "SECONDARY_ENDPOINT_IDS",
    "analyze_holdout",
    "analyze_primary",
    "bootstrap_seed",
    "exact_binomial_lower_tail",
    "exact_sign_pvalue",
    "holm_adjust",
    "percentile_interval",
    "summarize_paired_job",
]
