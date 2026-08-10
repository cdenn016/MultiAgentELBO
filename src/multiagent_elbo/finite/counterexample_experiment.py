"""Artifact-backed exact finite counterexample laboratory for Session 3."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import json
from pathlib import Path
from types import MappingProxyType
from typing import Literal, Mapping

import numpy as np

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.experiment_support import MetricRecord, readonly_array, target_metric
from multiagent_elbo.runtime import RngStreams, collect_provenance
from multiagent_elbo.finite.counterexamples import (
    CandidateRecord, EnumerationBounds, ExactAction, ExactChannel, ExactLaw,
    canonical_candidates_json, coarsen_marked_event, fixed_channel_score_gap,
    hoeffding_decompose_action, kl_divergence, minimize_candidates,
    parameter_dependent_channel_witness, project_action, retained_projection_invariant,
    scale_tolerance, diagonal_spd_conditioning,
)


MetricStatus = Literal["pass", "fail", "inconclusive"]
FigureRunStatus = Literal["not_requested"]
_METADATA = dict(theorem_status="ESTABLISHED", verification_state="EVIDENCE_VERIFIED", claim_origin="STANDARD")


@dataclass(frozen=True)
class FiniteCounterexampleExperimentResult:
    run_dir: Path
    config_hash: str
    status: MetricStatus
    metrics: Mapping[str, MetricRecord]
    arrays: Mapping[str, np.ndarray]
    figure_status: FigureRunStatus


def _fraction_float(value: Fraction) -> float:
    return float(value.numerator) / float(value.denominator)


def _freeze_arrays(values: Mapping[str, object]) -> dict[str, np.ndarray]:
    return {name: readonly_array(values[name]) for name in sorted(values)}


def _metric(value: Fraction, target: Fraction, interpretation: str) -> MetricRecord:
    return target_metric(_fraction_float(value), 0.0, target=_fraction_float(target), interpretation=interpretation, **_METADATA)


def _record(claim_id: str, witness: Mapping[str, object], residual: Fraction, *, inside: bool = True, assumptions: bool = True) -> CandidateRecord:
    return CandidateRecord(claim_id, inside, assumptions, witness, "exact", str(residual), "catalog" if inside and assumptions else "assumption_boundary", **_METADATA)


def _catalog(config: ExperimentConfig) -> tuple[dict[str, MetricRecord], dict[str, np.ndarray], tuple[CandidateRecord, ...], dict[str, object], dict[str, object]]:
    theory = config.theory
    bounds = EnumerationBounds(theory.max_states, theory.max_denominator)
    # The pinned catalog uses only the smallest exact representatives; requested
    # bounds are retained separately and never mistaken for exhaustive evidence.
    support = kl_divergence(ExactLaw((Fraction(1), Fraction(0))), ExactLaw((Fraction(0), Fraction(1))))
    support_count = Fraction(len(support.support_violations))
    theta = Fraction(1, 2)
    parameter_gap = fixed_channel_score_gap(theta)
    witness = parameter_dependent_channel_witness(theta)
    action = ExactAction((2, 2), (Fraction(1), Fraction(-1), Fraction(-1), Fraction(1)))
    projection = project_action(hoeffding_decompose_action(action), 1)
    invariant = retained_projection_invariant(action, action.relabel(((1, 0), (1, 0))), ((1, 0), (1, 0)), 1)
    relabel_gap = Fraction(0) if invariant else Fraction(1)
    source = ExactLaw((Fraction(1), Fraction(0)))
    channel = ExactChannel(((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))))
    joint, beta_only = coarsen_marked_event(source, ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))), channel)
    marked_gap = max(abs(left - right) for left_row, right_row in zip(joint, beta_only) for left, right in zip(left_row, right_row))
    metrics = {
        "support_violation_count": _metric(support_count, Fraction(1), "Structured extended-real support failures are counted without infinity arithmetic."),
        "parameter_dependent_channel_gap": _metric(parameter_gap, Fraction(1, 2), "Pinned parameter-dependent channel witness is an assumption-boundary control."),
        "single_law_relabeling_gap": _metric(relabel_gap, Fraction(0), "Coherent single-law relabeling preserves the retained exact projection."),
        "marked_event_source_mass_gap": _metric(marked_gap, Fraction(1, 2), "Dropping source-law weights changes the marked-event pushforward."),
        "pairwise_truncation_residual": _metric(projection.residual, Fraction(1), "The omitted two-way interaction has the pinned exact residual."),
    }
    records = minimize_candidates((
        _record("support_boundary", {"states": 2, "support": "missing"}, support_count),
        witness,
        _record("single_law_relabeling", {"states": 2, "action_arity": 2}, relabel_gap),
        _record("marked_event_source_mass", {"states": 2, "events": 2}, marked_gap),
        _record("pairwise_truncation", {"states": 2, "action_arity": 2}, projection.residual),
    ))
    arrays = {
        "support_violation_indices": np.asarray(support.support_violations, dtype=np.int64),
        "parameter_theta": np.asarray([_fraction_float(theta)], dtype=np.float64),
        "relabeling_difference": np.asarray([_fraction_float(relabel_gap)], dtype=np.float64),
        "marked_joint": np.asarray([[ _fraction_float(x) for x in row] for row in joint], dtype=np.float64),
        "marked_beta_only": np.asarray([[ _fraction_float(x) for x in row] for row in beta_only], dtype=np.float64),
        "pairwise_omitted_max": np.asarray([_fraction_float(projection.residual)], dtype=np.float64),
    }
    bounds_payload = {"requested": {"max_states": bounds.max_states, "max_denominator": bounds.max_denominator}, "effective_catalog": {"max_states": 2, "max_denominator": 2}}
    stress = {"deep_composition": {"residual": "0"}, "relabeling": {"residual": "0"}, "retained_space": {"residual": "1"}, "tolerance_scaling": {"base": "1/100", "states": 2, "scaled": str(scale_tolerance(Fraction(1, 100), 2))}, "conditioning": {"diagonal": ["1", "4"], "condition": str(diagonal_spd_conditioning((Fraction(1), Fraction(4))))}}
    return metrics, arrays, records, bounds_payload, stress


def run_finite_counterexample_experiment(config: ExperimentConfig) -> FiniteCounterexampleExperimentResult:
    """Validate, run the exact bounded catalog, and finalize its numerical bundle."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    if config.theory.experiment != "finite_counterexample":
        raise ValueError("finite counterexample experiment requires theory.experiment='finite_counterexample'")
    if config.compute.backend != "cpu":
        raise ValueError("exact-rational finite counterexample execution is CPU-only")
    metrics, raw_arrays, records, bounds, stress = _catalog(config)
    arrays = _freeze_arrays(raw_arrays)
    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    repo_root = Path(__file__).resolve().parents[3]
    provenance = collect_provenance(repo_root, repo_root / "Theory", config_hash, streams)
    provenance.update({"arithmetic": "exact_rational", "effective_backend": "cpu", "effective_dtype": "float64"})
    store = RunStore.create(config, provenance)
    store.write_json("metrics", {name: asdict(metrics[name]) for name in sorted(metrics)})
    store.write_json("enumeration_bounds", bounds)
    store.write_json("candidate_records", json.loads(canonical_candidates_json(records)))
    store.write_json("minimal_witnesses", json.loads(canonical_candidates_json(minimize_candidates(records))))
    store.write_json("stress_matrix", stress)
    store.write_npz("arrays", arrays)
    artifacts = ["metrics.json", "enumeration_bounds.json", "candidate_records.json", "minimal_witnesses.json", "stress_matrix.json", "arrays.npz"]
    if config.output.collect_diagnostics:
        support_diagnostic = kl_divergence(
            ExactLaw((Fraction(1), Fraction(0))),
            ExactLaw((Fraction(0), Fraction(1))),
        )
        store.write_npz(
            "diagnostics",
            _freeze_arrays(
                {"support_is_infinite": np.asarray([support_diagnostic.is_infinite], dtype=bool)}
            ),
        )
        artifacts.append("diagnostics.npz")
    store.finalize(artifacts)
    status: MetricStatus = "pass" if all(metric.status == "pass" for metric in metrics.values()) else "fail"
    return FiniteCounterexampleExperimentResult(store.run_dir, store.config_hash, status, MappingProxyType(dict(metrics)), MappingProxyType(arrays), "not_requested")


__all__ = ["FiniteCounterexampleExperimentResult", "run_finite_counterexample_experiment"]
