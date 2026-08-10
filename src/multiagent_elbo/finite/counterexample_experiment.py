"""Artifact-backed exact finite counterexample laboratory for Session 3."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import json
import math
from pathlib import Path
from types import MappingProxyType
from typing import Literal, Mapping, Sequence

import numpy as np

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.experiment_support import MetricRecord, readonly_array, target_metric
from multiagent_elbo.finite.counterexamples import (
    CandidateRecord,
    EnumerationBounds,
    ExactAction,
    ExactChannel,
    ExactLaw,
    canonical_candidates_json,
    coarsen_marked_event,
    compose_channels,
    diagonal_spd_conditioning,
    enumerate_rational_actions,
    enumerate_rational_channels,
    enumerate_rational_laws,
    fixed_channel_score_gap,
    hoeffding_decompose_action,
    kl_divergence,
    minimize_candidates,
    parameter_dependent_channel_witness,
    project_action,
    relabel_law,
    retained_projection_invariant,
    scale_tolerance,
    validate_full_rank_spd,
)
from multiagent_elbo.runtime import RngStreams, collect_provenance


MetricStatus = Literal["pass", "fail", "inconclusive"]
FigureRunStatus = Literal["not_requested"]
_EFFECTIVE_BOUNDS = EnumerationBounds(max_states=2, max_denominator=4)
_ACTION_CARDINALITIES = (2, 2, 2)
_ACTION_MAX_DENOMINATOR = 1
_ACTION_VALUE_BOUND = 1


@dataclass(frozen=True)
class FiniteCounterexampleExperimentResult:
    run_dir: Path
    config_hash: str
    status: MetricStatus
    metrics: Mapping[str, MetricRecord]
    arrays: Mapping[str, np.ndarray]
    figure_status: FigureRunStatus


def _float(value: Fraction) -> float:
    return float(value)


def _readonly_arrays(values: Mapping[str, object]) -> dict[str, np.ndarray]:
    return {name: readonly_array(value) for name, value in sorted(values.items())}


def _metric(
    value: float,
    target: float,
    interpretation: str,
    claim_origin: Literal["STANDARD", "PROJECT_NOVEL"],
) -> MetricRecord:
    return target_metric(
        value,
        1.0e-12,
        target=target,
        interpretation=interpretation,
        theorem_status="ESTABLISHED",
        verification_state="EVIDENCE_VERIFIED",
        claim_origin=claim_origin,
    )


def _record(
    claim_id: str,
    witness: Mapping[str, object],
    observed_residual: str,
    *,
    inside: bool,
    assumptions: bool,
    origin: str,
    exact_or_numeric: Literal["exact", "numeric_log"],
    classification: Literal["catalog", "assumption_boundary"],
) -> CandidateRecord:
    return CandidateRecord(
        claim_id,
        inside,
        assumptions,
        witness,
        exact_or_numeric,
        observed_residual,
        classification,
        "ESTABLISHED",
        "EVIDENCE_VERIFIED",
        origin,
    )


def _fraction_arrays(prefix: str, values: Sequence[Fraction]) -> dict[str, np.ndarray]:
    return {
        f"{prefix}_num": np.asarray([value.numerator for value in values], dtype=np.int64),
        f"{prefix}_den": np.asarray([value.denominator for value in values], dtype=np.int64),
    }


def _full_candidate_payload(records: Sequence[CandidateRecord]) -> list[dict[str, object]]:
    """Reuse the core canonical record serializer without applying global minimization."""
    payload = [json.loads(canonical_candidates_json((record,)))[0] for record in records]
    return sorted(payload, key=lambda record: json.dumps(record, sort_keys=True, separators=(",", ":")))


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def _channel_text(channel: ExactChannel) -> list[list[str]]:
    return [[_fraction_text(value) for value in row] for row in channel.rows]


def _enumerate_candidates(
    laws: tuple[ExactLaw, ...], channels: tuple[ExactChannel, ...]
) -> tuple[CandidateRecord, ...]:
    records: list[CandidateRecord] = []
    for q in laws:
        for p in laws:
            support = kl_divergence(q, p)
            if support.is_infinite:
                records.append(
                    _record(
                        "support_boundary",
                        {"states": 2, "q": q.masses, "p": p.masses},
                        str(len(support.support_violations)),
                        inside=True,
                        assumptions=True,
                        origin="PROJECT_NOVEL",
                        exact_or_numeric="exact",
                        classification="catalog",
                    )
                )
    for theta in sorted({law.masses[0] for law in laws if law.masses[0] > 0}):
        records.append(parameter_dependent_channel_witness(theta))
    swap = (1, 0)
    for law in laws:
        if all(value > 0 for value in law.masses):
            result = kl_divergence(relabel_law(law, swap), law)
            if result.value and result.value > 0.0:
                residual = (
                    "ln(3)/2"
                    if law.masses == (Fraction(3, 4), Fraction(1, 4))
                    else "numeric_log"
                )
                records.append(
                    _record(
                        "single_law_relabeling",
                        {"states": 2, "p": law.masses, "permutation": swap},
                        residual,
                        inside=False,
                        assumptions=False,
                        origin="STANDARD",
                        exact_or_numeric="numeric_log",
                        classification="assumption_boundary",
                    )
                )
    for source in laws:
        for first_beta in laws:
            for second_beta in laws:
                for channel in channels:
                    joint, beta_only = coarsen_marked_event(source, (first_beta.masses, second_beta.masses), channel)
                    gap = max(abs(left - right) for left_row, right_row in zip(joint, beta_only) for left, right in zip(left_row, right_row))
                    if gap > 0:
                        records.append(
                            _record(
                                "marked_event_source_mass",
                                {
                                    "states": 2,
                                    "source": source.masses,
                                    "beta": (first_beta.masses, second_beta.masses),
                                    "channel": channel.rows,
                                },
                                str(gap),
                                inside=True,
                                assumptions=True,
                                origin="PROJECT_NOVEL",
                                exact_or_numeric="exact",
                                classification="catalog",
                            )
                        )
    for action in enumerate_rational_actions(
        _ACTION_CARDINALITIES,
        _ACTION_MAX_DENOMINATOR,
        value_bound=_ACTION_VALUE_BOUND,
    ):
        residual = project_action(hoeffding_decompose_action(action), 2).residual
        if residual > 0:
            records.append(
                _record(
                    "pairwise_truncation",
                    {
                        "states": 2,
                        "action_arity": 3,
                        "retained_order": 2,
                        "values": action.values,
                    },
                    str(residual),
                    inside=True,
                    assumptions=True,
                    origin="PROJECT_NOVEL",
                    exact_or_numeric="exact",
                    classification="catalog",
                )
            )
    return tuple(records)


def _catalog(config: ExperimentConfig) -> tuple[dict[str, MetricRecord], dict[str, np.ndarray], tuple[CandidateRecord, ...], dict[str, object], dict[str, object]]:
    requested = EnumerationBounds(config.theory.max_states, config.theory.max_denominator)
    laws = tuple(enumerate_rational_laws(_EFFECTIVE_BOUNDS.max_states, _EFFECTIVE_BOUNDS.max_denominator))
    channels = tuple(enumerate_rational_channels(2, 2, _EFFECTIVE_BOUNDS.max_denominator))
    candidates = _enumerate_candidates(laws, channels)
    minimal = minimize_candidates(candidates)
    support_q = ExactLaw((Fraction(1), Fraction(0)))
    support_p = ExactLaw((Fraction(0), Fraction(1)))
    theta = Fraction(1, 4)
    relabel_p = ExactLaw((Fraction(3, 4), Fraction(1, 4)))
    permutation = (1, 0)
    relabel_result = kl_divergence(relabel_law(relabel_p, permutation), relabel_p)
    source = ExactLaw((Fraction(1), Fraction(0)))
    beta = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    channel = ExactChannel(((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))))
    joint, beta_only = coarsen_marked_event(source, beta, channel)
    marked_gap = max(abs(left - right) for first, second in zip(joint, beta_only) for left, right in zip(first, second))
    action = ExactAction(
        _ACTION_CARDINALITIES,
        (
            Fraction(1), Fraction(-1), Fraction(-1), Fraction(1),
            Fraction(-1), Fraction(1), Fraction(1), Fraction(-1),
        ),
    )
    retained_order = 2
    pairwise = project_action(hoeffding_decompose_action(action), retained_order)
    support_count = len(kl_divergence(support_q, support_p).support_violations)
    metrics = {
        "support_violation_count": _metric(float(support_count), 1.0, "Structured extended-real support failures are counted without infinity arithmetic.", "PROJECT_NOVEL"),
        "parameter_dependent_channel_gap": _metric(_float(fixed_channel_score_gap(theta)), 0.125, "Parameter-dependent-channel control is outside the fixed-channel assumptions.", "STANDARD"),
        "single_law_relabeling_gap": _metric(float(relabel_result.value), math.log(3.0) / 2.0, "Relabeling q alone produces the pinned finite KL gap.", "STANDARD"),
        "marked_event_source_mass_gap": _metric(_float(marked_gap), 0.5, "Dropping source-law weights changes the marked-event pushforward.", "PROJECT_NOVEL"),
        "pairwise_truncation_residual": _metric(_float(pairwise.residual), 1.0, "A three-axis order-three action leaves an omitted residual after order-two retention.", "PROJECT_NOVEL"),
    }
    arrays: dict[str, np.ndarray] = {
        "relabel_permutation": np.asarray(permutation, dtype=np.int64),
        "marked_channel_shape": np.asarray((2, 2), dtype=np.int64),
        "marked_beta_shape": np.asarray((2, 2), dtype=np.int64),
        "action_axis_sizes": np.asarray(action.cardinalities, dtype=np.int64),
        "retained_order": np.asarray((retained_order,), dtype=np.int64),
    }
    arrays.update(_fraction_arrays("support_q", support_q.masses))
    arrays.update(_fraction_arrays("support_p", support_p.masses))
    arrays.update(_fraction_arrays("theta", (theta,)))
    arrays.update(_fraction_arrays("relabel_p", relabel_p.masses))
    arrays.update(_fraction_arrays("marked_source", source.masses))
    arrays.update(_fraction_arrays("marked_channel", tuple(value for row in channel.rows for value in row)))
    arrays.update(_fraction_arrays("marked_beta", tuple(value for row in beta for value in row)))
    arrays.update(_fraction_arrays("action", action.values))
    composition_a = ExactChannel(
        ((Fraction(1), Fraction(0)), (Fraction(1, 2), Fraction(1, 2)))
    )
    composition_b = ExactChannel(
        ((Fraction(1, 2), Fraction(1, 2)), (Fraction(0), Fraction(1)))
    )
    composition_c = ExactChannel(
        ((Fraction(3, 4), Fraction(1, 4)), (Fraction(1, 4), Fraction(3, 4)))
    )
    composed_direct = compose_channels(compose_channels(composition_a, composition_b), composition_c)
    composed_staged = compose_channels(composition_a, compose_channels(composition_b, composition_c))
    composition_residual = max(
        abs(left - right)
        for direct_row, staged_row in zip(composed_direct.rows, composed_staged.rows)
        for left, right in zip(direct_row, staged_row)
    )
    relabeled_action = action.relabel(((1, 0), (1, 0), (1, 0)))
    stress = {
        "deep_composition": {
            "channels": {
                "a": _channel_text(composition_a),
                "b": _channel_text(composition_b),
                "c": _channel_text(composition_c),
            },
            "direct_rows": _channel_text(composed_direct),
            "staged_rows": _channel_text(composed_staged),
            "residual": _fraction_text(composition_residual),
            "direct_equals_staged": composed_direct == composed_staged,
        },
        "relabeling": {"coherent": retained_projection_invariant(action, relabeled_action, ((1, 0), (1, 0), (1, 0)), retained_order), "residual": "0"},
        "retained_space": {"pass_residual": str(pairwise.residual), "fails_full_reconstruction": pairwise.residual > 0},
        "tolerance_scaling": {"base": "1/100", "states": 2, "scaled": str(scale_tolerance(Fraction(1, 100), 2))},
        "conditioning": {"accepted_dimension": validate_full_rank_spd(((Fraction(1), Fraction(0)), (Fraction(0), Fraction(4)))), "accepted_condition": str(diagonal_spd_conditioning((Fraction(1), Fraction(4)))), "rejected_near_singular": _rejected_near_singular()},
    }
    bounds = {
        "requested": {
            "max_states": requested.max_states,
            "max_denominator": requested.max_denominator,
        },
        "effective": {
            "laws_channels": {
                "max_states": _EFFECTIVE_BOUNDS.max_states,
                "max_denominator": _EFFECTIVE_BOUNDS.max_denominator,
            },
            "actions": {
                "axis_cardinalities": list(_ACTION_CARDINALITIES),
                "max_denominator": _ACTION_MAX_DENOMINATOR,
                "value_bound": _ACTION_VALUE_BOUND,
            },
        },
        "enumerated_counts": {
            "laws": len(laws),
            "channels": len(channels),
            "actions": 3 ** 8,
            "candidates": len(candidates),
            "minimal_candidates": len(minimal),
        },
    }
    return metrics, arrays, candidates, bounds, stress


def _rejected_near_singular() -> bool:
    try:
        validate_full_rank_spd(((Fraction(1), Fraction(0)), (Fraction(0), Fraction(0))))
    except ValueError:
        return True
    return False


def run_finite_counterexample_experiment(config: ExperimentConfig) -> FiniteCounterexampleExperimentResult:
    """Validate, exhaust the explicit effective catalog, and publish the bundle."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    if config.theory.experiment != "finite_counterexample":
        raise ValueError("finite counterexample experiment requires theory.experiment='finite_counterexample'")
    if config.compute.backend != "cpu":
        raise ValueError("exact-rational finite counterexample execution is CPU-only")
    if config.output.render_figures:
        raise ValueError("finite counterexample laboratory exposes no figures")
    metrics, raw_arrays, candidates, bounds, stress = _catalog(config)
    arrays = _readonly_arrays(raw_arrays)
    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    repo_root = Path(__file__).resolve().parents[3]
    provenance = collect_provenance(repo_root, repo_root / "Theory", config_hash, streams)
    provenance.update({"arithmetic": "exact_rational", "effective_backend": "cpu", "effective_dtype": "float64"})
    store = RunStore.create(config, provenance)
    minimal = minimize_candidates(candidates)
    store.write_json("metrics", {name: asdict(metrics[name]) for name in sorted(metrics)})
    store.write_json("enumeration_bounds", bounds)
    store.write_json("candidate_records", _full_candidate_payload(candidates))
    store.write_json("minimal_witnesses", json.loads(canonical_candidates_json(minimal)))
    store.write_json("stress_matrix", stress)
    store.write_npz("arrays", arrays)
    artifacts = ["metrics.json", "enumeration_bounds.json", "candidate_records.json", "minimal_witnesses.json", "stress_matrix.json", "arrays.npz"]
    if config.output.collect_diagnostics:
        store.write_npz("diagnostics", _readonly_arrays({"candidate_count": np.asarray((len(candidates),), dtype=np.int64)}))
        artifacts.append("diagnostics.npz")
    store.finalize(artifacts)
    status: MetricStatus = "pass" if all(metric.status == "pass" for metric in metrics.values()) else "fail"
    return FiniteCounterexampleExperimentResult(store.run_dir, store.config_hash, status, MappingProxyType(dict(metrics)), MappingProxyType(arrays), "not_requested")


__all__ = ["FiniteCounterexampleExperimentResult", "run_finite_counterexample_experiment"]
