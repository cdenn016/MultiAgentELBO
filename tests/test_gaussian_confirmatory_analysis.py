from __future__ import annotations

from math import isfinite

import numpy as np
import pytest

from multiagent_elbo.realizations.gaussian.confirmatory_analysis import (
    SECONDARY_ENDPOINT_IDS,
    analyze_holdout,
    analyze_primary,
    bootstrap_seed,
    exact_binomial_lower_tail,
    exact_sign_pvalue,
    holm_adjust,
    percentile_interval,
    summarize_paired_job,
)


def test_exact_sign_pvalue_is_conservative_at_ties():
    values = np.array([-1.0, -0.5, 0.0, 0.0], dtype=np.float64)

    assert exact_sign_pvalue(values, 0.0) == pytest.approx(11.0 / 16.0)


def test_exact_binomial_lower_tail_uses_composite_null_boundary():
    assert exact_binomial_lower_tail(0, 30, 0.05) == pytest.approx(0.95**30)


@pytest.mark.parametrize(
    ("values", "boundary"),
    [
        (np.array([], dtype=np.float64), 0.0),
        (np.array([np.nan], dtype=np.float64), 0.0),
        (np.array([0.0], dtype=np.float64), np.inf),
    ],
)
def test_exact_sign_pvalue_rejects_invalid_samples(values: np.ndarray, boundary: float):
    with pytest.raises(ValueError):
        exact_sign_pvalue(values, boundary)


@pytest.mark.parametrize(
    ("events", "trials", "probability"),
    [(-1, 30, 0.05), (31, 30, 0.05), (0, 0, 0.05), (0, 30, -0.1), (0, 30, 1.1)],
)
def test_exact_binomial_lower_tail_rejects_invalid_inputs(
    events: int, trials: int, probability: float
):
    with pytest.raises(ValueError):
        exact_binomial_lower_tail(events, trials, probability)


def test_holm_adjusts_one_frozen_six_endpoint_family():
    raw = dict(
        zip(
            SECONDARY_ENDPOINT_IDS,
            [0.01, 0.04, 0.03, 0.002, 0.5, 0.04],
            strict=True,
        )
    )

    result = holm_adjust(raw)

    assert [row["endpoint_id"] for row in result] == list(SECONDARY_ENDPOINT_IDS)
    by_id = {row["endpoint_id"]: row for row in result}
    assert by_id["scheme_dispersion"]["adjusted_p"] == pytest.approx(0.012)
    assert all(0.0 <= row["adjusted_p"] <= 1.0 for row in result)


def test_holm_breaks_raw_pvalue_ties_by_endpoint_id():
    raw = {endpoint_id: 0.04 for endpoint_id in reversed(SECONDARY_ENDPOINT_IDS)}

    result = holm_adjust(raw)

    ranked = sorted(result, key=lambda row: row["rank"])
    assert [row["endpoint_id"] for row in ranked] == sorted(SECONDARY_ENDPOINT_IDS)


def test_holm_rejects_a_partial_or_extra_family():
    with pytest.raises(ValueError, match="exactly six"):
        holm_adjust({SECONDARY_ENDPOINT_IDS[0]: 0.01})
    with pytest.raises(ValueError, match="exactly six"):
        holm_adjust({**{name: 0.01 for name in SECONDARY_ENDPOINT_IDS}, "extra": 0.2})


def _scheme_record(
    *,
    angle_tail: list[float],
    distance: float,
    beta_tail: list[float],
    construction: float,
    conditioning_tail: list[float],
    basin_exit: bool = False,
    rejected: bool = False,
) -> dict[str, object]:
    return {
        "projective_ray_angles": [1.0, 0.9, 0.8, 0.7, *angle_tail],
        "normalized_coupling_distances": [1.0] * 8 + [distance],
        "retained_beta_residuals": [1.0, 0.8, 0.6, *beta_tail],
        "scalarized_ray_construction_residuals": [construction] * 9,
        "coefficient_conditioning": [8.0, 7.0, 6.0, 5.0, *conditioning_tail],
        "basin_exit": basin_exit,
        "rejected": rejected,
        "rejection_reason": "frozen rejection" if rejected else None,
    }


def test_paired_summary_uses_least_favorable_scheme_without_pseudoreplication():
    record = {
        "job_id": "C001",
        "role": "confirmatory_primary",
        "scientific_analysis_eligibility": True,
        "schemes": {
            "adjacent_pairs": _scheme_record(
                angle_tail=[0.5, 0.4, 0.3, 0.2, 0.1],
                distance=0.01,
                beta_tail=[0.5, 0.4, 0.3, 0.2, 0.1],
                construction=2.0e-13,
                conditioning_tail=list(np.exp([2.0, 1.8, 1.6, 1.4, 1.2])),
            ),
            "balanced_alternating": _scheme_record(
                angle_tail=[0.5, 0.5, 0.5, 0.5, 0.5],
                distance=0.03,
                beta_tail=[0.2, 0.2, 0.2, 0.2, 0.2],
                construction=3.0e-13,
                conditioning_tail=list(np.exp([2.0, 2.0, 2.0, 2.0, 2.0])),
                basin_exit=True,
                rejected=True,
            ),
        },
        "blocking_scheme_dispersion": [0.1] * 8 + [0.015],
    }

    summary = summarize_paired_job(record)

    assert summary["job_id"] == "C001"
    assert summary["primary_angle_slope"] == pytest.approx(0.0)
    assert summary["scale_8_normalized_distance"] == pytest.approx(0.03)
    assert summary["construction_residual"] == pytest.approx(3.0e-13)
    assert summary["retained_beta_trend"] == pytest.approx(0.0)
    assert summary["basin_exit"] is True
    assert summary["scheme_dispersion"] == pytest.approx(0.015)
    assert summary["conditioning_trend"] == pytest.approx(0.0)
    assert summary["rejected"] is True
    assert summary["independent_observation_count"] == 1


def _primary_record(index: int) -> dict[str, object]:
    angle_shift = index * 1.0e-5
    return {
        "job_id": f"C{index + 1:03d}",
        "role": "confirmatory_primary",
        "scientific_analysis_eligibility": True,
        "schemes": {
            "adjacent_pairs": _scheme_record(
                angle_tail=list(np.array([0.20, 0.17, 0.14, 0.11, 0.08]) + angle_shift),
                distance=0.03,
                beta_tail=[0.20, 0.16, 0.12, 0.08, 0.04],
                construction=2.0e-13,
                conditioning_tail=list(np.exp([2.0, 1.8, 1.6, 1.4, 1.2])),
            ),
            "balanced_alternating": _scheme_record(
                angle_tail=list(np.array([0.21, 0.18, 0.15, 0.12, 0.09]) + angle_shift),
                distance=0.04,
                beta_tail=[0.21, 0.17, 0.13, 0.09, 0.05],
                construction=3.0e-13,
                conditioning_tail=list(np.exp([2.1, 1.9, 1.7, 1.5, 1.3])),
            ),
        },
        "blocking_scheme_dispersion": [0.03] * 8 + [0.01],
        "distinct_projective_rays": False,
    }


def test_bootstrap_identity_is_deterministic_and_endpoint_bound():
    first = bootstrap_seed("2026-08-09-gaussian-fixed-ray-v1a", "a" * 64, "primary")
    second = bootstrap_seed("2026-08-09-gaussian-fixed-ray-v1a", "a" * 64, "primary")

    assert first == second
    assert first != bootstrap_seed(
        "2026-08-09-gaussian-fixed-ray-v1a", "a" * 64, "supporting_distance"
    )
    assert first != bootstrap_seed(
        "2026-08-09-gaussian-fixed-ray-v1a", "b" * 64, "primary"
    )


def test_percentile_interval_uses_exactly_ten_thousand_whole_job_resamples():
    values = np.arange(30, dtype=np.float64)

    first = percentile_interval(values, seed=1234)
    second = percentile_interval(values, seed=1234)

    assert first == second
    assert first["resamples"] == 10_000
    assert first["trials"] == 30
    assert len(first["resample_indices_sha256"]) == 64
    assert len(first["bootstrap_statistics_sha256"]) == 64


def test_primary_analysis_uses_thirty_unique_c_jobs_and_one_six_test_holm_family():
    records = [_primary_record(index) for index in range(30)]

    result = analyze_primary(
        records,
        protocol_id="2026-08-09-gaussian-fixed-ray-v1a",
        job_table_sha256="a" * 64,
        decision_stability=True,
        premises_passed=True,
        gpu_gate_complete=True,
    )

    assert result["primary_job_ids"] == [f"C{index:03d}" for index in range(1, 31)]
    assert result["independent_job_count"] == 30
    assert len(result["secondary_tests"]) == 6
    assert {row["endpoint_id"] for row in result["secondary_tests"]} == set(
        SECONDARY_ENDPOINT_IDS
    )
    assert result["classification"] == "support"


@pytest.mark.parametrize(
    "record",
    [
        {**_primary_record(0), "job_id": "P001", "role": "pilot"},
        {**_primary_record(0), "job_id": "H001", "role": "confirmatory_holdout"},
        {**_primary_record(0), "scientific_analysis_eligibility": False},
    ],
)
def test_primary_analysis_rejects_pilot_holdout_and_sentinel_records(
    record: dict[str, object],
):
    records = [_primary_record(index) for index in range(30)]
    records[0] = record

    with pytest.raises(ValueError, match="primary"):
        analyze_primary(
            records,
            protocol_id="2026-08-09-gaussian-fixed-ray-v1a",
            job_table_sha256="a" * 64,
            decision_stability=True,
            premises_passed=True,
            gpu_gate_complete=True,
        )


def test_rejected_job_is_retained_as_a_censored_worst_case_observation():
    rejected = _primary_record(0)
    rejected["schemes"] = {
        "adjacent_pairs": _scheme_record(
            angle_tail=[0.2, 0.17, 0.14, 0.11, 0.08],
            distance=0.03,
            beta_tail=[0.2, 0.16, 0.12, 0.08, 0.04],
            construction=2.0e-13,
            conditioning_tail=list(np.exp([2.0, 1.8, 1.6, 1.4, 1.2])),
        ),
        "balanced_alternating": {
            "projective_ray_angles": None,
            "normalized_coupling_distances": None,
            "retained_beta_residuals": None,
            "scalarized_ray_construction_residuals": None,
            "coefficient_conditioning": None,
            "basin_exit": False,
            "rejected": True,
            "rejection_reason": "nonfinite worker output",
        },
    }

    summary = summarize_paired_job(rejected)

    assert summary["rejected"] is True
    assert summary["continuous_endpoint_censored_worst_case"] is True
    assert summary["primary_angle_slope"] is None

    records = [_primary_record(index) for index in range(30)]
    records[0] = rejected
    result = analyze_primary(
        records,
        protocol_id="2026-08-09-gaussian-fixed-ray-v1a",
        job_table_sha256="a" * 64,
        decision_stability=True,
        premises_passed=True,
        gpu_gate_complete=True,
    )
    assert result["rejection_events"] == 1
    assert result["censored_worst_case_count"] == 1


def test_missing_primary_job_forces_inconclusive_without_replacement():
    result = analyze_primary(
        [_primary_record(index) for index in range(29)],
        protocol_id="2026-08-09-gaussian-fixed-ray-v1a",
        job_table_sha256="a" * 64,
        decision_stability=True,
        premises_passed=True,
        gpu_gate_complete=True,
    )

    assert result["missing_job_ids"] == ["C030"]
    assert result["classification"] == "inconclusive"
    basin = next(
        row for row in result["secondary_tests"] if row["endpoint_id"] == "basin_exit_rate"
    )
    assert basin["unadjusted_p"] == pytest.approx(0.95**29)
    assert basin["available_trials"] == 29


def test_terminal_missing_record_is_not_analyzed_as_a_favorable_event():
    records = [_primary_record(index) for index in range(29)]
    records.append(
        {
            "schema_version": "gaussian-fixed-ray-confirmatory-job-v1",
            "job_id": "C030",
            "role": "confirmatory_primary",
            "terminal_status": "missing",
            "scientific_analysis_eligibility": False,
            "failure_reason": "infrastructure retry exhausted",
        }
    )

    result = analyze_primary(
        records,
        protocol_id="2026-08-09-gaussian-fixed-ray-v1a",
        job_table_sha256="a" * 64,
        decision_stability=True,
        premises_passed=True,
        gpu_gate_complete=True,
    )

    assert result["missing_job_ids"] == ["C030"]
    assert result["completed_job_count"] == 29
    assert result["classification"] == "inconclusive"


def test_many_rejected_jobs_use_finite_frozen_censor_values():
    records = [_primary_record(index) for index in range(30)]
    for index in range(16):
        records[index]["schemes"] = {
            scheme_id: {
                "projective_ray_angles": None,
                "normalized_coupling_distances": None,
                "retained_beta_residuals": None,
                "scalarized_ray_construction_residuals": None,
                "coefficient_conditioning": None,
                "basin_exit": False,
                "rejected": True,
                "rejection_reason": "frozen rejection",
            }
            for scheme_id in ("adjacent_pairs", "balanced_alternating")
        }

    result = analyze_primary(
        records,
        protocol_id="2026-08-09-gaussian-fixed-ray-v1a",
        job_table_sha256="a" * 64,
        decision_stability=True,
        premises_passed=True,
        gpu_gate_complete=True,
    )

    for interval_name in (
        "primary_endpoint",
        "supporting_distance",
        "scheme_dispersion_interval",
    ):
        interval = result[interval_name]
        assert all(isfinite(float(interval[key])) for key in ("estimate", "lower", "upper"))


def test_distinct_projective_rays_is_the_frozen_dispersion_counterevidence_alias():
    records = [_primary_record(index) for index in range(30)]
    for record in records:
        record["blocking_scheme_dispersion"] = [0.1] * 9
        record["distinct_projective_rays"] = False

    result = analyze_primary(
        records,
        protocol_id="2026-08-09-gaussian-fixed-ray-v1a",
        job_table_sha256="a" * 64,
        decision_stability=True,
        premises_passed=True,
        gpu_gate_complete=True,
    )

    assert result["scheme_dispersion_interval"]["lower"] > 0.05
    assert result["distinct_projective_rays"] is True
    assert result["classification"] == "counterevidence"


def test_holdout_analysis_is_descriptive_and_bound_to_primary_digest():
    records = []
    for index in range(10):
        record = _primary_record(index)
        record["job_id"] = f"H{index + 1:03d}"
        record["role"] = "confirmatory_holdout"
        records.append(record)

    result = analyze_holdout(
        records,
        protocol_id="2026-08-09-gaussian-fixed-ray-v1a",
        job_table_sha256="a" * 64,
        primary_analysis_sha256="b" * 64,
    )

    assert result["holdout_job_ids"] == [f"H{index:03d}" for index in range(1, 11)]
    assert result["primary_analysis_sha256"] == "b" * 64
    assert result["analysis_scope"] == "descriptive_replication_only"
    assert "secondary_tests" not in result
    assert "classification" not in result
    assert "two_sided_p" not in result["primary_endpoint"]
