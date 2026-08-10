"""Artifact-backed finite information-history laboratory."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import tracemalloc
from types import MappingProxyType
from typing import Literal, Mapping

import numpy as np

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.experiment_support import MetricRecord, readonly_array, target_metric
from multiagent_elbo.runtime import RngStreams, collect_provenance

from .information_history import (
    InformationHistory,
    RequiredNegativeControls,
    build_information_history_model,
    required_negative_controls,
    simulate_information_history,
)


MetricStatus = Literal["pass", "fail", "inconclusive"]
_FIXTURE_APPLICATION_ID = (
    "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"
)


@dataclass(frozen=True)
class InformationHistoryExperimentResult:
    """Typed handle to one finalized Session 4 run."""

    run_dir: Path
    config_hash: str
    status: MetricStatus
    metrics: Mapping[str, MetricRecord]
    artifact_arrays: Mapping[str, Mapping[str, np.ndarray]]


def _load_fixture_payload(path: Path) -> Mapping[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("two-scale fixture must contain a JSON object")
    return payload


def _freeze_artifact(
    arrays: Mapping[str, object]
) -> Mapping[str, np.ndarray]:
    frozen = {
        name: readonly_array(arrays[name])
        for name in sorted(arrays)
    }
    return MappingProxyType(frozen)


def _artifact_arrays(
    history: InformationHistory, controls: RequiredNegativeControls
) -> Mapping[str, Mapping[str, np.ndarray]]:
    artifacts = {
        "history_parameters": _freeze_artifact(
            {
                "coarse_parameters": history.coarse_parameters,
                "fine_parameters": history.fine_parameters,
                "inference_orbit_parameter": history.inference_orbit_parameter,
                "rg_depth": history.rg_depth,
            }
        ),
        "scores": _freeze_artifact(
            {
                "coarse_analytic": history.coarse_score,
                "coarse_finite_difference": history.coarse_finite_difference_score,
                "fine_analytic": history.fine_score,
                "fine_finite_difference": history.fine_finite_difference_score,
                "pushed_analytic": history.pushed_score,
                "pushed_finite_difference": history.pushed_finite_difference_score,
                "parameter_dependent_actual_coarse_score": controls.parameter_dependent_actual_score,
                "parameter_dependent_channel_gap": controls.parameter_dependent_gap,
                "parameter_dependent_conditional_expected_score": controls.parameter_dependent_conditional_score,
            }
        ),
        "fisher_matrices": _freeze_artifact(
            {
                "coarse": history.coarse_fisher,
                "coarse_positive_spectrum_condition_number": history.coarse_positive_condition,
                "coarse_rank": history.coarse_rank,
                "defect": history.fisher_defect,
                "fine": history.fine_fisher,
                "fine_positive_spectrum_condition_number": history.fine_positive_condition,
                "fine_rank": history.fine_rank,
                "identity_residual": history.fisher_identity_residual,
                "pushed_coarse": history.pushed_fisher,
                "pushed_positive_spectrum_condition_number": history.pushed_positive_condition,
                "pushed_rank": history.pushed_rank,
                "rank_deficient_control_fisher": controls.rank_deficient_fisher,
                "rank_deficient_control_natural_gradient": controls.rank_deficient_natural_gradient,
                "rank_deficient_control_range_residual": controls.rank_deficient_range_residual,
                "rank_deficient_control_rank": controls.rank_deficient_rank,
                "rank_deficient_control_vfe_gradient": controls.rank_deficient_gradient,
            }
        ),
        "vfe_gradients": _freeze_artifact(
            {
                "coarse": history.coarse_vfe_gradient,
                "fine": history.fine_vfe_gradient,
            }
        ),
        "natural_gradient_fields": _freeze_artifact(
            {
                "coarse": history.coarse_natural_gradient,
                "coarse_range_residual": history.coarse_range_residual,
                "fine": history.fine_natural_gradient,
                "fine_range_residual": history.fine_range_residual,
            }
        ),
        "information_durations": _freeze_artifact(
            {
                "information_duration": history.information_duration,
                "raw_coordinate_cumulative": history.raw_coordinate_cumulative,
                "reparameterization_parameter": history.reparameterization_parameter,
                "reparameterized_information_duration": history.reparameterized_information_duration,
                "chart_information_duration_residual": controls.chart_information_duration_residual,
                "chart_raw_coordinate_length_ratio": controls.chart_raw_length_ratio,
                "same_endpoint_detour_duration": controls.detour_duration,
                "same_endpoint_detour_history": controls.detour_history,
                "same_endpoint_straight_duration": controls.straight_duration,
                "same_endpoint_straight_history": controls.straight_history,
            }
        ),
        "semiconjugacy_defects": _freeze_artifact(
            {
                "coarse_comparison_vector": history.coarse_comparison_vector,
                "defect": history.semiconjugacy_defects,
                "norm": history.semiconjugacy_defect_norms,
                "pushed_fine_vector": history.pushed_fine_vector,
                "literal_minus_sign_oracle": controls.semiconjugacy_minus_oracle,
                "plus_sign_mutation": controls.semiconjugacy_plus_mutation,
                "plus_sign_mutation_gap": controls.semiconjugacy_plus_mutation_gap,
            }
        ),
    }
    return MappingProxyType(artifacts)


def _max_abs(values: np.ndarray) -> float:
    return float(np.max(np.abs(values)))


def _metrics(
    history: InformationHistory, config: ExperimentConfig
) -> Mapping[str, MetricRecord]:
    numerics = config.numerics
    identity_tolerance = numerics.atol + numerics.rtol
    finite_difference_tolerance = max(1.0e-8, 100.0 * identity_tolerance)
    score_residual = max(
        _max_abs(history.fine_finite_difference_score - history.fine_score),
        _max_abs(history.pushed_finite_difference_score - history.pushed_score),
        _max_abs(history.coarse_finite_difference_score - history.coarse_score),
    )
    fisher_residual = _max_abs(history.fisher_identity_residual)
    range_residual = max(
        float(np.max(history.fine_range_residual)),
        float(np.max(history.coarse_range_residual)),
    )
    arc_residual = abs(
        float(history.information_duration[-1])
        - float(history.reparameterized_information_duration[-1])
    )
    defect_norm = float(np.max(history.semiconjugacy_defect_norms))
    semiconjugacy_detection_tolerance = max(1.0e-6, identity_tolerance)

    return MappingProxyType(
        {
            "score_finite_difference_residual": target_metric(
                score_residual,
                finite_difference_tolerance,
                target=0.0,
                interpretation=(
                    "Analytic fine, fixed-channel pushed, and independent coarse "
                    "scores agree with centered finite differences in their declared charts."
                ),
                theorem_status="ESTABLISHED",
                verification_state="EVIDENCE_VERIFIED",
                claim_origin="STANDARD",
            ),
            "fisher_defect_residual": target_metric(
                fisher_residual,
                identity_tolerance,
                target=0.0,
                interpretation=(
                    "For the fixed parameter-independent fixture channel, fine Fisher "
                    "equals pushed Fisher plus conditional score covariance."
                ),
                theorem_status="ESTABLISHED",
                verification_state="EVIDENCE_VERIFIED",
                claim_origin="STANDARD",
            ),
            "natural_gradient_range_residual": target_metric(
                range_residual,
                identity_tolerance,
                target=0.0,
                interpretation=(
                    "Each VFE covector lies in the Fisher range used by the declared "
                    "Moore--Penrose identifiable-tangent quotient rule."
                ),
                theorem_status="HYPOTHESIS",
                verification_state="EVIDENCE_VERIFIED",
                claim_origin="APPLICATION_SPECIFIC",
            ),
            "arc_length_reparameterization_residual": target_metric(
                arc_residual,
                identity_tolerance,
                target=0.0,
                interpretation=(
                    "The saved polygonal Fisher duration is independent of the separate "
                    "orientation-preserving history parameter labels."
                ),
                theorem_status="ESTABLISHED",
                verification_state="EVIDENCE_VERIFIED",
                claim_origin="STANDARD",
            ),
            "semiconjugacy_defect_norm": MetricRecord(
                value=defect_norm,
                tolerance=semiconjugacy_detection_tolerance,
                status=(
                    "pass"
                    if defect_norm > semiconjugacy_detection_tolerance
                    else "fail"
                ),
                interpretation=(
                    "Detectable norm of dC_theta(v_fine) - v_coarse(C(theta)); "
                    "the control witnesses nonintertwining and does not assume automatic "
                    "semiconjugacy."
                ),
                assessment_scope="implementation_check",
                theorem_status="OPEN",
                verification_state="INCONCLUSIVE",
                claim_origin="PROJECT_NOVEL",
            ),
        }
    )


def run_information_history_experiment(
    config: ExperimentConfig,
) -> InformationHistoryExperimentResult:
    """Validate, compute, then atomically publish one information-history run."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    if config.theory.experiment != "information_history":
        raise ValueError(
            "information history experiment requires theory.experiment='information_history'"
        )
    if config.output.render_figures:
        raise ValueError("information_history does not expose rendering")

    repo_root = Path(__file__).resolve().parents[3]
    fixture_path = repo_root / "tests" / "fixtures" / "two_scale_application_v1.json"
    fixture_bytes = fixture_path.read_bytes()
    fixture_payload = _load_fixture_payload(fixture_path)
    model = build_information_history_model(fixture_payload, config.numerics)
    if model.application_id != _FIXTURE_APPLICATION_ID:
        raise ValueError("fixture application_id does not match the frozen Session 4 ID")

    owned_tracemalloc = not tracemalloc.is_tracing()
    if owned_tracemalloc:
        tracemalloc.start()
    history = simulate_information_history(
        model,
        history_steps=config.theory.history_steps,
        step_size=config.theory.step_size,
    )
    controls = required_negative_controls(config.numerics)
    _, peak_memory = tracemalloc.get_traced_memory()
    if owned_tracemalloc:
        tracemalloc.stop()

    metrics = _metrics(history, config)
    artifacts = _artifact_arrays(history, controls)
    config_hash = config_sha256(config)

    # Configuration, fixture, and all numerical validation above intentionally
    # precede both RNG construction and artifact-directory creation.
    streams = RngStreams.from_seed(config.run.seed)
    provenance = collect_provenance(
        repo_root, repo_root / "Theory", config_hash, streams
    )
    provenance["source_revision"] = provenance["git_commit"]
    provenance["application_id"] = model.application_id
    provenance["fixture_sha256"] = hashlib.sha256(fixture_bytes).hexdigest()
    provenance["input_hashes"]["two_scale_fixture_sha256"] = provenance[
        "fixture_sha256"
    ]
    provenance["floating_point"] = {"backend": "cpu", "dtype": "float64"}
    provenance["performance_records"] = {
        "wall_time_seconds": history.wall_time_seconds,
        "peak_tracemalloc_bytes": int(peak_memory),
    }
    provenance["experiment_scope"] = model.family_scope
    provenance["channel_scope"] = "declared_fixed_parameter_independent"
    provenance["semiconjugacy_scope"] = (
        "typed_pointwise_defect_not_assumed_to_vanish"
    )

    store = RunStore.create(config, provenance)
    store.write_json(
        "metrics", {name: asdict(metrics[name]) for name in sorted(metrics)}
    )
    declared_artifacts = ["metrics.json"]
    for name in sorted(artifacts):
        store.write_npz(name, artifacts[name])
        declared_artifacts.append(f"{name}.npz")
    store.finalize(declared_artifacts)

    status: MetricStatus = (
        "pass"
        if all(metric.status == "pass" for metric in metrics.values())
        else "fail"
    )
    return InformationHistoryExperimentResult(
        run_dir=store.run_dir,
        config_hash=config_hash,
        status=status,
        metrics=metrics,
        artifact_arrays=artifacts,
    )


__all__ = [
    "InformationHistoryExperimentResult",
    "run_information_history_experiment",
]
