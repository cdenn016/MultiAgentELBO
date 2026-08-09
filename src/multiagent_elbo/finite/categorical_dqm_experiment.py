"""Pre-registered finite categorical DQM and Fisher laboratory."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from pathlib import Path
from types import MappingProxyType
from typing import Callable, Literal, Mapping

import numpy as np

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.experiment_support import (
    MetricRecord,
    lower_bounded_metric,
    readonly_array,
    target_metric,
)
from multiagent_elbo.finite.categorical import CategoricalExponentialFamily
from multiagent_elbo.finite.categorical_dqm import analyze_categorical_dqm
from multiagent_elbo.finite.measures import MarkovKernel
from multiagent_elbo.rendering import (
    record_figure_failure_safely,
    validated_renderer_status,
)
from multiagent_elbo.runtime import RngStreams, collect_provenance


MetricStatus = Literal["pass", "fail", "inconclusive"]
FigureRunStatus = Literal["not_requested", "complete", "failed"]
ChannelScope = Literal["declared_fixed_parameter_independent"]

_DEFAULT_THETA = (math.log(2.0), math.log(3.0))
_DEFAULT_DQM_STEPS = (0.1, 0.05, 0.025, 0.0125)
_DIRECTION = (3.0 / 5.0, -4.0 / 5.0)


@dataclass(frozen=True)
class CategoricalDqmExperimentResult:
    """Typed handle to one finalized categorical-DQM experiment run."""

    run_dir: Path
    config_hash: str
    status: MetricStatus
    metrics: Mapping[str, MetricRecord]
    arrays: Mapping[str, np.ndarray]
    channel_scope: ChannelScope
    figure_status: FigureRunStatus
    figure_dir: Path | None


def _max_abs(values: np.ndarray) -> float:
    return float(np.max(np.abs(values)))


def _freeze_arrays(values: Mapping[str, np.ndarray]) -> dict[str, np.ndarray]:
    return {
        name: readonly_array(values[name])
        for name in sorted(values)
    }


def _identity_metric(
    value: float, tolerance: float, interpretation: str
) -> MetricRecord:
    return target_metric(
        value,
        tolerance,
        target=0.0,
        interpretation=interpretation,
        theorem_status="established_conditional_identity",
    )


def _strictly_decreasing_metric(
    values: np.ndarray, interpretation: str
) -> MetricRecord:
    adjacent_differences = np.diff(values)
    maximum_adjacent_difference = float(np.max(adjacent_differences))
    return MetricRecord(
        value=maximum_adjacent_difference,
        tolerance=0.0,
        status="pass" if np.all(adjacent_differences < 0.0) else "fail",
        interpretation=interpretation,
        assessment_scope="implementation_check",
        theorem_status="established_conditional_identity",
    )


def _categorical_dqm_fixture(
    config: ExperimentConfig,
) -> tuple[dict[str, MetricRecord], dict[str, np.ndarray], dict[str, np.ndarray]]:
    theory = config.theory
    numerics = config.numerics
    tolerance = numerics.atol + numerics.rtol
    family = CategoricalExponentialFamily(
        ("x0", "x1", "x2"),
        (0.0, 0.0, 0.0),
        ((1.0, 0.0), (0.0, 1.0), (0.0, 0.0)),
        numerics,
    )
    channel = MarkovKernel(
        family.labels,
        ("z0", "z1"),
        ((1.0, 0.0), (0.0, 1.0), (0.5, 0.5)),
        numerics,
    )
    theta = theory.theta
    analysis = analyze_categorical_dqm(
        family,
        theta,
        channel,
        theory.finite_difference_step,
        _DIRECTION,
        theory.dqm_step_sizes,
    )
    fisher = analysis.fisher_channel_result
    probability = analysis.base_probability
    analytic_score = analysis.analytic_fine_score
    coarse_probability = fisher.coarse_probability
    coarse_score = fisher.coarse_score
    defect = fisher.conditional_covariance
    ladder = analysis.remainder_ladder
    wrong_score = (
        channel.matrix.T @ analytic_score
    ) / channel.matrix.sum(axis=0)[:, None]
    wrong_score_error = wrong_score - coarse_score
    wrong_weight_gap = _max_abs(wrong_score_error)
    is_default = (
        tuple(theta) == _DEFAULT_THETA
        and tuple(theory.dqm_step_sizes) == _DEFAULT_DQM_STEPS
    )

    final_remainder = max(float(ladder.positive[-1]), float(ladder.negative[-1]))
    metrics = {
        "DQM-01_normalization_residual": _identity_metric(
            max(abs(float(probability.sum()) - 1.0), abs(float(coarse_probability.sum()) - 1.0)),
            tolerance,
            "Fine and pushed categorical probabilities normalize.",
        ),
        "DQM-01_score_centering_residual": _identity_metric(
            _max_abs(probability @ analytic_score),
            tolerance,
            "The analytic categorical score is centered under the fine law.",
        ),
        "DQM-01_finite_difference_score_residual": _identity_metric(
            _max_abs(analysis.finite_difference_fine_score - analytic_score),
            tolerance,
            "Centered finite differences reproduce the analytic fine score.",
        ),
        "DQM-01_two_sided_remainder_final": target_metric(
            final_remainder,
            max(float(ladder.step_sizes[-1]), tolerance),
            target=0.0,
            interpretation=(
                "Final two-sided normalized square-root likelihood remainder; "
                "the finite ladder is an implementation check, not the DQM proof."
            ),
            theorem_status="established_conditional_identity",
        ),
        "INF-02_conditional_score_fd_residual": _identity_metric(
            _max_abs(analysis.finite_difference_pushed_score - coarse_score),
            tolerance,
            "Fixed-channel conditional score agrees with an independent pushed FD score.",
        ),
        "INF-02_fisher_identity_residual": _identity_metric(
            _max_abs(fisher.residual),
            tolerance,
            "Fine Fisher equals coarse Fisher plus expected conditional covariance.",
        ),
        "INF-02_fisher_defect_min_eigenvalue": lower_bounded_metric(
            fisher.minimum_defect_eigenvalue,
            fisher.defect_psd_tolerance,
            lower_bound=0.0,
            interpretation="The fixed-channel Fisher information-loss tensor is PSD.",
            theorem_status="established_conditional_identity",
        ),
        "INF-02_positive_loss_trace_control": MetricRecord(
            value=float(np.trace(defect)),
            tolerance=tolerance,
            status=(
                "pass" if float(np.trace(defect)) > tolerance else "fail"
            ),
            interpretation="The registered lossy channel removes detectable Fisher information.",
            assessment_scope="implementation_check",
            theorem_status="established_conditional_identity",
        ),
    }

    if is_default:
        expected_probability = np.array((1.0 / 3.0, 1.0 / 2.0, 1.0 / 6.0))
        expected_score = np.array(
            ((2.0 / 3.0, -1.0 / 2.0), (-1.0 / 3.0, 1.0 / 2.0), (-1.0 / 3.0, -1.0 / 2.0))
        )
        expected_coarse_probability = np.array((5.0 / 12.0, 7.0 / 12.0))
        expected_coarse_score = np.array(
            ((7.0 / 15.0, -1.0 / 2.0), (-1.0 / 3.0, 5.0 / 14.0))
        )
        expected_fine_fisher = np.array(
            ((2.0 / 9.0, -1.0 / 6.0), (-1.0 / 6.0, 1.0 / 4.0))
        )
        expected_coarse_fisher = np.array(
            ((7.0 / 45.0, -1.0 / 6.0), (-1.0 / 6.0, 5.0 / 28.0))
        )
        expected_defect = np.array(((1.0 / 15.0, 0.0), (0.0, 1.0 / 14.0)))
        literal_values = {
            "DQM-01_literal_probability_residual": _max_abs(
                probability - expected_probability
            ),
            "DQM-01_literal_score_residual": _max_abs(
                analytic_score - expected_score
            ),
            "INF-02_literal_coarse_probability_residual": _max_abs(
                coarse_probability - expected_coarse_probability
            ),
            "INF-02_literal_conditional_score_residual": _max_abs(
                coarse_score - expected_coarse_score
            ),
            "INF-02_literal_fine_fisher_residual": _max_abs(
                fisher.fine_fisher - expected_fine_fisher
            ),
            "INF-02_literal_coarse_fisher_residual": _max_abs(
                fisher.coarse_fisher - expected_coarse_fisher
            ),
            "INF-02_literal_fisher_defect_residual": _max_abs(
                defect - expected_defect
            ),
        }
        metrics.update(
            {
                key: _identity_metric(
                    value,
                    tolerance,
                    "The registered default fixture agrees with its independent rational oracle.",
                )
                for key, value in literal_values.items()
            }
        )
        metrics["DQM-01_positive_remainder_ladder_monotonicity"] = (
            _strictly_decreasing_metric(
                ladder.positive,
                "The registered positive DQM remainder ladder strictly decreases.",
            )
        )
        metrics["DQM-01_negative_remainder_ladder_monotonicity"] = (
            _strictly_decreasing_metric(
                ladder.negative,
                "The registered negative DQM remainder ladder strictly decreases.",
            )
        )
        metrics["INF-NEG-01_wrong_weight_gap"] = target_metric(
            wrong_weight_gap,
            tolerance,
            target=4.0 / 21.0,
            interpretation=(
                "The column-normalized unweighted score has the pinned default gap "
                "from the conditional score."
            ),
            theorem_status="negative_control",
        )
    else:
        metrics["INF-NEG-01_wrong_weight_gap_diagnostic"] = MetricRecord(
            value=wrong_weight_gap,
            tolerance=0.0,
            status="inconclusive",
            interpretation=(
                "Diagnostic unweighted-score gap at an edited theta; no default "
                "rational threshold is assessed."
            ),
            assessment_scope="implementation_check",
            theorem_status="negative_control",
        )

    covariance_contributions = np.empty(
        (len(channel.target_labels), family.parameter_count, family.parameter_count),
        dtype=np.float64,
    )
    for target_index in range(len(channel.target_labels)):
        deviations = analytic_score - coarse_score[target_index]
        covariance_contributions[target_index] = np.einsum(
            "x,xi,xj->ij", fisher.joint_mass[:, target_index], deviations, deviations
        )

    core_arrays = {
        "analytic_coarse_score": coarse_score,
        "analytic_fine_score": analytic_score,
        "channel": channel.matrix,
        "coarse_fisher": fisher.coarse_fisher,
        "coarse_probability": coarse_probability,
        "direction": np.asarray(_DIRECTION),
        "dqm_remainder_negative": ladder.negative,
        "dqm_remainder_positive": ladder.positive,
        "dqm_step_sizes": ladder.step_sizes,
        "fine_fisher": fisher.fine_fisher,
        "fine_probability": probability,
        "finite_difference_coarse_score": analysis.finite_difference_pushed_score,
        "finite_difference_fine_score": analysis.finite_difference_fine_score,
        "fisher_defect": defect,
        "fisher_identity_residual": fisher.residual,
        "theta": np.asarray(theta),
        "wrong_weight_gap": np.asarray(wrong_weight_gap),
    }
    diagnostics = {
        "conditional_covariance_contributions": covariance_contributions,
        "joint_mass": fisher.joint_mass,
        "wrong_score": wrong_score,
        "wrong_score_error": wrong_score_error,
    }
    return metrics, core_arrays, diagnostics


def run_categorical_dqm_experiment(
    config: ExperimentConfig,
    *,
    renderer: Callable[..., object] | None = None,
) -> CategoricalDqmExperimentResult:
    """Run and finalize the registered categorical-DQM fixture."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    if config.theory.experiment != "categorical_dqm":
        raise ValueError(
            "categorical DQM experiment requires theory.experiment='categorical_dqm'"
        )

    metrics, raw_arrays, raw_diagnostics = _categorical_dqm_fixture(config)
    arrays = _freeze_arrays(raw_arrays)
    diagnostics = _freeze_arrays(raw_diagnostics)
    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    repo_root = Path(__file__).resolve().parents[3]
    provenance = collect_provenance(repo_root, repo_root / "Theory", config_hash, streams)
    provenance["experiment_scope"] = "finite_positive_smooth_exponential_family"
    provenance["channel_scope"] = "declared_fixed_parameter_independent"
    store = RunStore.create(config, provenance)
    store.write_json(
        "metrics", {name: asdict(metrics[name]) for name in sorted(metrics)}
    )
    store.write_npz("arrays", arrays)
    artifacts = ["metrics.json", "arrays.npz"]
    if config.output.collect_diagnostics:
        store.write_npz("diagnostics", diagnostics)
        artifacts.append("diagnostics.npz")
    store.finalize(artifacts)

    status_bearing_metrics = (
        metric
        for name, metric in metrics.items()
        if name != "INF-NEG-01_wrong_weight_gap_diagnostic"
    )
    numerical_status: MetricStatus = (
        "pass"
        if all(metric.status == "pass" for metric in status_bearing_metrics)
        else "fail"
    )

    figure_status: FigureRunStatus = "not_requested"
    figure_dir: Path | None = None
    if config.output.render_figures:
        figure_dir = store.run_dir.parent / "figures" / store.run_dir.name
        requested = ("categorical_dqm",)
        if renderer is None:
            from multiagent_elbo.figures import render_run

            renderer = render_run
        try:
            figure_manifest = renderer(
                store.run_dir,
                figure_dir,
                requested=requested,
            )
            figure_status = validated_renderer_status(
                figure_manifest, store.run_dir, figure_dir, requested
            )
        except Exception as error:
            figure_status = "failed"
            record_figure_failure_safely(store.run_dir, figure_dir, str(error))
    return CategoricalDqmExperimentResult(
        run_dir=store.run_dir,
        config_hash=store.config_hash,
        status=numerical_status,
        metrics=MappingProxyType(dict(metrics)),
        arrays=MappingProxyType(arrays),
        channel_scope="declared_fixed_parameter_independent",
        figure_status=figure_status,
        figure_dir=figure_dir,
    )


__all__ = ["CategoricalDqmExperimentResult", "run_categorical_dqm_experiment"]
