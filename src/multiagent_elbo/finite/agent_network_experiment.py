"""Exact four-agent application laboratory and immutable artifact publication."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import math
import os
from pathlib import Path
import subprocess
import time
import tracemalloc
from types import MappingProxyType
from typing import Literal, Mapping, Protocol, Sequence

import numpy as np

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.experiment_support import MetricRecord, readonly_array, target_metric
from multiagent_elbo.runtime import RngStreams, collect_provenance

from .agent_network import (
    ApplicationFixture,
    ExactInteractionDecomposition,
    ScenarioApplication,
    assess_fixed_channel_premise,
    build_scenario_application,
    exact_hoeffding_decompose,
    global_vfe_gap,
    load_application_fixture,
    local_collective_difference,
    overlapping_local_objective_gap,
    product_bernoulli_law,
    recognition_lift_residual,
    retained_interaction_residual,
    scenario_recognition_target,
)


MetricStatus = Literal["pass", "fail", "inconclusive"]


class _Digest(Protocol):
    def update(self, data: bytes, /) -> None: ...


@dataclass(frozen=True)
class AgentNetworkExperimentResult:
    """Typed handle to one finalized multi-agent network run."""

    run_dir: Path
    config_hash: str
    status: MetricStatus
    metrics: Mapping[str, MetricRecord]
    arrays: Mapping[str, np.ndarray]


def _fraction_values(values: Sequence[Fraction]) -> np.ndarray:
    return np.asarray([float(value) for value in values], dtype=np.float64)


def _fraction_numerators(values: Sequence[Fraction]) -> np.ndarray:
    return np.asarray([value.numerator for value in values], dtype=np.int64)


def _fraction_denominators(values: Sequence[Fraction]) -> np.ndarray:
    return np.asarray([value.denominator for value in values], dtype=np.int64)


def _fraction_matrix_values(values: Sequence[Sequence[Fraction]]) -> np.ndarray:
    return np.asarray([[float(value) for value in row] for row in values], dtype=np.float64)


def _fraction_matrix_numerators(values: Sequence[Sequence[Fraction]]) -> np.ndarray:
    return np.asarray(
        [[value.numerator for value in row] for row in values], dtype=np.int64
    )


def _fraction_matrix_denominators(values: Sequence[Sequence[Fraction]]) -> np.ndarray:
    return np.asarray(
        [[value.denominator for value in row] for row in values], dtype=np.int64
    )


def _freeze_arrays(values: Mapping[str, np.ndarray]) -> dict[str, np.ndarray]:
    return {
        name: readonly_array(values[name], dtype=values[name].dtype)
        for name in sorted(values)
    }


def _metric(
    value: float,
    target: float,
    tolerance: float,
    *,
    interpretation: str,
    theorem_status: Literal["ESTABLISHED", "HYPOTHESIS"],
    claim_origin: Literal["STANDARD", "PROJECT_NOVEL", "APPLICATION_SPECIFIC"],
) -> MetricRecord:
    verified = math.isfinite(value) and abs(value - target) <= tolerance
    return target_metric(
        value,
        tolerance,
        target=target,
        interpretation=interpretation,
        theorem_status=theorem_status,
        verification_state="EVIDENCE_VERIFIED" if verified else "INCONCLUSIVE",
        claim_origin=claim_origin,
    )


def _subset_mask(subset: tuple[int, ...]) -> int:
    return sum(1 << axis for axis in subset)


def _interaction_matrix(
    decomposition: ExactInteractionDecomposition,
) -> tuple[tuple[Fraction, ...], ...]:
    ordered = sorted(decomposition.components, key=_subset_mask)
    return tuple(decomposition.components[subset] for subset in ordered)


def _local_checks(
    fixture: ApplicationFixture, application: ScenarioApplication
) -> tuple[np.ndarray, tuple[tuple[Fraction, ...], ...]]:
    before_parameters = (Fraction(1, 2),) * 4
    before = product_bernoulli_law(before_parameters)
    target = scenario_recognition_target(application.scenario)
    differences: list[tuple[float, float, float]] = []
    outside_marginals: list[tuple[Fraction, ...]] = []
    for block_id in ("local_B01", "local_B23"):
        block_axes, _outside_axes = fixture.local_blocks[block_id]
        after_parameters = list(before_parameters)
        for axis in block_axes:
            after_parameters[axis] = target[axis]
        check = local_collective_difference(
            application.posterior,
            before,
            product_bernoulli_law(after_parameters),
            block_axes=block_axes,
        )
        differences.append(
            (check.local_difference, check.collective_difference, check.residual)
        )
        outside_marginals.append(check.outside_marginal)
    return np.asarray(differences, dtype=np.float64), tuple(outside_marginals)


def _evaluate(
    config: ExperimentConfig, fixture_path: Path
) -> tuple[
    ApplicationFixture,
    ScenarioApplication,
    Mapping[str, MetricRecord],
    Mapping[str, np.ndarray],
    Mapping[str, np.ndarray],
    Mapping[str, object],
]:
    fixture = load_application_fixture(fixture_path)
    application = build_scenario_application(fixture, config.theory.scenario)
    before = product_bernoulli_law((Fraction(1, 2),) * 4)
    target_parameters = scenario_recognition_target(application.scenario)
    target_law = product_bernoulli_law(target_parameters)
    gap = global_vfe_gap(before, application.evidence_measure)
    decomposition = exact_hoeffding_decompose(
        application.interaction_action_log2, fixture.fine_axis_references
    )
    pairwise_residual = retained_interaction_residual(
        decomposition, maximum_order=2
    )
    expected_pairwise = Fraction(1) if application.scenario == "higher_order" else Fraction()
    lift_residual = recognition_lift_residual(target_parameters)
    local_differences, outside_marginals = _local_checks(fixture, application)
    evidence_residual = abs(
        application.evidence - sum(application.coarse_evidence_measure, Fraction())
    )
    tolerance = config.numerics.atol + config.numerics.rtol

    metrics = {
        "evidence_residual": _metric(
            float(evidence_residual),
            0.0,
            tolerance,
            interpretation="common normalized one-arrow pushforward preserves evidence mass",
            theorem_status="ESTABLISHED",
            claim_origin="STANDARD",
        ),
        "elbo_gap_residual": _metric(
            gap.residual,
            0.0,
            tolerance,
            interpretation="joint VFE equals posterior KL minus log evidence",
            theorem_status="ESTABLISHED",
            claim_origin="STANDARD",
        ),
        "local_collective_residual": _metric(
            float(np.max(np.abs(local_differences[:, 2]))),
            0.0,
            tolerance,
            interpretation="both fixed-outside block changes equal their collective KL changes",
            theorem_status="ESTABLISHED",
            claim_origin="PROJECT_NOVEL",
        ),
        "hoeffding_reconstruction_residual": _metric(
            float(decomposition.reconstruction_residual),
            0.0,
            0.0,
            interpretation="complete Fraction-based Hoeffding components reconstruct the action",
            theorem_status="ESTABLISHED",
            claim_origin="STANDARD",
        ),
        "recognition_lift_residual": _metric(
            float(lift_residual),
            0.0,
            0.0,
            interpretation="extraction after the declared product recognition lift is identity",
            theorem_status="HYPOTHESIS",
            claim_origin="APPLICATION_SPECIFIC",
        ),
        "pairwise_retained_residual": _metric(
            float(pairwise_residual),
            float(expected_pairwise),
            0.0,
            interpretation="pairwise truncation matches the scenario-specific literal residual",
            theorem_status="HYPOTHESIS",
            claim_origin="APPLICATION_SPECIFIC",
        ),
    }
    ordered_metrics = MappingProxyType({name: metrics[name] for name in sorted(metrics)})

    interaction_matrix = _interaction_matrix(decomposition)
    record_names = tuple(application.interaction_record_kernels)
    record_success = tuple(
        tuple(row[0] for row in application.interaction_record_kernels[name])
        for name in record_names
    )
    coarse_action = np.asarray(
        [-math.log(float(value)) for value in application.coarse_effective_likelihood],
        dtype=np.float64,
    )
    arrays = _freeze_arrays(
        {
            "coarse_action": coarse_action,
            "coarse_evidence_measure": _fraction_values(
                application.coarse_evidence_measure
            ),
            "coarse_law": _fraction_values(application.coarse_posterior),
            "coarse_law_denominators": _fraction_denominators(
                application.coarse_posterior
            ),
            "coarse_law_numerators": _fraction_numerators(
                application.coarse_posterior
            ),
            "configuration_scale_map": _fraction_matrix_values(
                fixture.configuration_scale_map
            ),
            "configuration_scale_map_denominators": _fraction_matrix_denominators(
                fixture.configuration_scale_map
            ),
            "configuration_scale_map_numerators": _fraction_matrix_numerators(
                fixture.configuration_scale_map
            ),
            "fine_evidence_measure": _fraction_values(application.evidence_measure),
            "fine_law": _fraction_values(application.posterior),
            "fine_law_denominators": _fraction_denominators(application.posterior),
            "fine_law_numerators": _fraction_numerators(application.posterior),
            "fine_to_coarse_channel": _fraction_matrix_values(fixture.channel),
            "fine_to_coarse_channel_denominators": _fraction_matrix_denominators(
                fixture.channel
            ),
            "fine_to_coarse_channel_numerators": _fraction_matrix_numerators(
                fixture.channel
            ),
            "hoeffding_interactions": _fraction_matrix_values(interaction_matrix),
            "hoeffding_interactions_denominators": _fraction_matrix_denominators(
                interaction_matrix
            ),
            "hoeffding_interactions_numerators": _fraction_matrix_numerators(
                interaction_matrix
            ),
            "interaction_action_log2": _fraction_values(
                application.interaction_action_log2
            ),
            "local_collective_differences": local_differences,
            "recognition_before": _fraction_values(before),
            "recognition_target": _fraction_values(target_law),
            "record_success_likelihoods": _fraction_matrix_values(record_success),
        }
    )
    wrong_lift = (Fraction(1, 16),) * 16
    parameter_dependent = assess_fixed_channel_premise(
        recognition_independent=False
    )
    diagnostics = _freeze_arrays(
        {
            "outside_marginals": _fraction_matrix_values(outside_marginals),
            "overlapping_local_objective_gap": np.asarray(
                [
                    overlapping_local_objective_gap(
                        application.posterior,
                        before,
                        tuple(block[0] for block in fixture.local_blocks.values()),
                    )
                ],
                dtype=np.float64,
            ),
            "parameter_dependent_channel_applicable": np.asarray(
                [parameter_dependent.satisfied], dtype=np.bool_
            ),
            "recognition_lift_negative_control": np.asarray(
                [recognition_lift_residual(target_parameters, wrong_lift)],
                dtype=np.float64,
            ),
        }
    )
    claims: Mapping[str, object] = MappingProxyType(
        {
            "application_id": fixture.application_id,
            "fixed_channel_premise": asdict(
                assess_fixed_channel_premise(recognition_independent=True)
            ),
            "parameter_dependent_control": asdict(parameter_dependent),
            "record_names": list(record_names),
            "scenario": application.scenario,
            "scope_exclusions": [
                "physical time",
                "universality",
                "continuum limit",
                "learned-agent behavior",
            ],
        }
    )
    return fixture, application, ordered_metrics, arrays, diagnostics, claims


def _git_bytes(repo_root: Path, *args: str) -> bytes | None:
    safe = repo_root.as_posix()
    completed = subprocess.run(
        ["git", "-c", f"safe.directory={safe}", "-C", str(repo_root), *args],
        capture_output=True,
        check=False,
    )
    return completed.stdout if completed.returncode == 0 else None


def _update_framed(digest: _Digest, label: bytes, payload: bytes) -> None:
    digest.update(len(label).to_bytes(8, "big"))
    digest.update(label)
    digest.update(len(payload).to_bytes(8, "big"))
    digest.update(payload)


def _bind_git_provenance(provenance: dict[str, object], repo_root: Path) -> None:
    revision = _git_bytes(repo_root, "rev-parse", "HEAD")
    status = _git_bytes(
        repo_root, "status", "--porcelain=v1", "-z", "--untracked-files=all"
    )
    tracked = _git_bytes(repo_root, "diff", "--binary", "--no-ext-diff", "HEAD", "--")
    untracked = _git_bytes(
        repo_root, "ls-files", "--others", "--exclude-standard", "-z"
    )
    if revision is not None:
        provenance["git_commit"] = revision.decode("ascii").strip()
    if status is not None:
        provenance["git_dirty"] = bool(status)
        provenance["git_status_sha256"] = hashlib.sha256(status).hexdigest()
    if tracked is None or untracked is None:
        return
    digest = hashlib.sha256()
    _update_framed(digest, b"tracked-diff", tracked)
    for raw_path in sorted(path for path in untracked.split(b"\0") if path):
        relative = Path(os.fsdecode(raw_path))
        if relative.is_absolute() or ".." in relative.parts:
            return
        _update_framed(digest, b"untracked-path", raw_path)
        _update_framed(
            digest,
            b"untracked-content-sha256",
            hashlib.sha256((repo_root / relative).read_bytes()).digest(),
        )
    provenance["dirty_tree_sha256"] = digest.hexdigest()


def run_agent_network_experiment(
    config: ExperimentConfig, *, fixture_path: Path | str | None = None
) -> AgentNetworkExperimentResult:
    """Validate, evaluate, provenance-bind, and finalize one Session-1 run."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    if config.theory.experiment != "multiagent_network":
        raise ValueError(
            "agent-network experiment requires theory.experiment='multiagent_network'"
        )
    if config.output.render_figures:
        raise ValueError("multiagent_network figures are deferred to serial integration")

    repo_root = Path(__file__).resolve().parents[3]
    active_fixture = (
        repo_root / "tests" / "fixtures" / "two_scale_application_v1.json"
        if fixture_path is None
        else Path(fixture_path)
    )
    owns_tracer = not tracemalloc.is_tracing()
    if owns_tracer:
        tracemalloc.start()
    evaluation_start = time.perf_counter()
    try:
        fixture, application, metrics, arrays, diagnostics, claims = _evaluate(
            config, active_fixture
        )
    finally:
        evaluation_runtime = time.perf_counter() - evaluation_start
        _current_bytes, evaluation_peak_bytes = tracemalloc.get_traced_memory()
        if owns_tracer:
            tracemalloc.stop()

    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    provenance = collect_provenance(
        repo_root, repo_root / "Theory", config_hash, streams
    )
    _bind_git_provenance(provenance, repo_root)
    provenance.update(
        {
            "application_id": fixture.application_id,
            "arithmetic": "exact_rational_inputs",
            "experiment_scope": "explicit_four_agent_two_scale_application",
            "fixture_file_sha256": hashlib.sha256(active_fixture.read_bytes()).hexdigest(),
            "floating_evaluations": ["log", "KL", "VFE", "coarse_action"],
            "performance_record": {
                "scope": "validated_scientific_evaluation",
                "runtime_seconds": evaluation_runtime,
                "tracemalloc_peak_bytes": evaluation_peak_bytes,
                "tracer_owned_by_run": owns_tracer,
            },
            "scenario": application.scenario,
        }
    )
    store = RunStore.create(config, provenance)
    store.write_json(
        "metrics", {name: asdict(metrics[name]) for name in sorted(metrics)}
    )
    store.write_json("claims", dict(claims))
    store.write_npz("arrays", arrays)
    artifacts = ["metrics.json", "claims.json", "arrays.npz"]
    if config.output.collect_diagnostics:
        store.write_npz("diagnostics", diagnostics)
        artifacts.append("diagnostics.npz")
    store.finalize(artifacts)
    status: MetricStatus = (
        "pass" if all(metric.status == "pass" for metric in metrics.values()) else "fail"
    )
    return AgentNetworkExperimentResult(
        run_dir=store.run_dir,
        config_hash=store.config_hash,
        status=status,
        metrics=metrics,
        arrays=MappingProxyType(dict(arrays)),
    )


__all__ = ["AgentNetworkExperimentResult", "run_agent_network_experiment"]
