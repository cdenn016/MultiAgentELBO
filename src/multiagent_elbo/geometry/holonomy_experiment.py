"""Artifact-backed finite graph-link holonomy laboratory.

The laboratory studies declared links on a finite interaction complex.  It does
not identify those links with a base-manifold connection, and coherent passive
frame covariance is not a dynamical symmetry.  Its floating-point checks are
implementation evidence, not mathematical proofs.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from types import MappingProxyType
from typing import Literal, Mapping

import numpy as np

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.experiment_support import (
    ClaimOrigin,
    MetricRecord,
    VerificationState,
    lower_bounded_metric,
    readonly_array,
    target_metric,
    validate_two_scale_application_fixture,
)
from multiagent_elbo.geometry import discrete_holonomy as hol
from multiagent_elbo.runtime import RngStreams, collect_provenance


MetricStatus = Literal["pass", "fail", "inconclusive"]
CanonicalStatus = Literal["ESTABLISHED", "HYPOTHESIS", "CONJECTURE", "NUMERICAL", "OPEN"]

_FIXTURE_NAME = "two_scale_application_v1"
_FIXTURE_APPLICATION_ID = (
    "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"
)
_SCENARIOS = frozenset(
    {
        "flat_tree",
        "flat_cycle",
        "nonflat_plaquette",
        "frustrated_transport",
        "staged_aggregation",
    }
)
_SCIENTIFIC_ARTIFACTS = (
    "interaction_complex.json",
    "oriented_links.npz",
    "vertex_frames.npz",
    "cycle_holonomies.npz",
    "operational_record_laws.npz",
    "aggregation_stages.npz",
)


@dataclass(frozen=True)
class HolonomyExperimentResult:
    """Typed handle to one finalized graph-link laboratory run."""

    run_dir: Path
    config_hash: str
    status: MetricStatus
    scenario: str
    theorem_status: CanonicalStatus
    verification_state: VerificationState
    claim_origin: ClaimOrigin
    metrics: Mapping[str, MetricRecord]
    arrays: Mapping[str, np.ndarray]
    artifacts: Mapping[str, Path]


def _load_fixture(repo_root: Path) -> tuple[dict[str, object], str, str]:
    fixture_path = repo_root / "tests" / "fixtures" / f"{_FIXTURE_NAME}.json"
    fixture_bytes = fixture_path.read_bytes()
    payload = json.loads(fixture_bytes.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("two-scale fixture must be a JSON object")
    application_id = validate_two_scale_application_fixture(payload)
    if application_id != _FIXTURE_APPLICATION_ID:
        raise ValueError("fixture application identity is not the frozen identity")
    return payload, application_id, hashlib.sha256(fixture_bytes).hexdigest()


def _edge_pair(
    label: str, source: str, target: str
) -> tuple[hol.OrientedEdge, hol.OrientedEdge]:
    inverse = f"e{target}{source}"
    return (
        hol.OrientedEdge(label, source, target, inverse),
        hol.OrientedEdge(inverse, target, source, label),
    )


def _scenario_fixture(
    payload: Mapping[str, object], scenario: str,
) -> tuple[hol.InteractionComplex, hol.OrientedLinks]:
    interaction = payload["interaction_complex"]
    if not isinstance(interaction, Mapping):
        raise ValueError("fixture interaction_complex must be an object")
    forward_edges = interaction["oriented_edges"]
    cells = interaction["two_cells"]
    if not isinstance(forward_edges, list) or not isinstance(cells, list):
        raise ValueError("fixture interaction data must use literal arrays")
    selected_edges = forward_edges[:-1] if scenario == "flat_tree" else forward_edges
    edges: list[hol.OrientedEdge] = []
    for record in selected_edges:
        if not isinstance(record, Mapping):
            raise ValueError("fixture oriented edge must be an object")
        edges.extend(
            _edge_pair(
                str(record["edge_id"]),
                str(record["source"]),
                str(record["target"]),
            )
        )
    two_cells = (
        ()
        if scenario == "flat_tree"
        else tuple(
            hol.OrientedTwoCell(str(cell["cell_id"]), tuple(cell["boundary"]))
            for cell in cells
            if isinstance(cell, Mapping)
        )
    )
    complex_ = hol.InteractionComplex(
        tuple(interaction["vertices"]), tuple(edges), two_cells
    )
    forward: dict[str, np.ndarray] = {
        "e01": np.eye(2),
        "e12": np.array([[1.0, 1.0], [0.0, 1.0]]),
        "e23": np.eye(2),
    }
    if scenario == "flat_cycle":
        forward["e30"] = np.array([[1.0, -1.0], [0.0, 1.0]])
    elif scenario != "flat_tree":
        forward["e30"] = np.array([[2.0, 0.0], [0.0, 1.0]])
    matrices: dict[str, np.ndarray] = {}
    for label, matrix in forward.items():
        edge = next(edge for edge in complex_.edges if edge.label == label)
        matrices[label] = matrix
        matrices[edge.inverse] = hol.invert_link(matrix)
    return complex_, hol.OrientedLinks(complex_, matrices)


def _frozen_arrays(values: Mapping[str, object]) -> dict[str, np.ndarray]:
    return {
        name: readonly_array(value, dtype=np.asarray(value).dtype)
        for name, value in sorted(values.items())
    }


def _record_law_arrays(
    baseline: hol.OperationalRecordLaw,
    coherent: hol.OperationalRecordLaw,
    broken: hol.OperationalRecordLaw,
) -> dict[str, np.ndarray]:
    return _frozen_arrays(
        {
            "baseline_logits": baseline.logits,
            "baseline_probabilities": baseline.probabilities,
            "baseline_transported_state": baseline.transported_state,
            "broken_logits": broken.logits,
            "broken_probabilities": broken.probabilities,
            "broken_transported_state": broken.transported_state,
            "coherent_logits": coherent.logits,
            "coherent_probabilities": coherent.probabilities,
            "coherent_transported_state": coherent.transported_state,
            "mark_values": [0.0, 1.0],
        }
    )


def _scenario_arrays(
    complex_: hol.InteractionComplex,
    links: hol.OrientedLinks,
    scenario: str,
    tolerance: float,
) -> tuple[
    dict[str, dict[str, np.ndarray]],
    dict[str, MetricRecord],
    dict[str, object],
]:
    frames = {
        "0": np.array([[2.0, 0.0], [0.0, 1.0]]),
        "1": np.eye(2),
        "2": np.eye(2),
        "3": np.eye(2),
    }
    transformed_links = hol.passive_transform_links(complex_, links, frames)
    broken_link_labels = ("e01", "e10")
    broken_link_matrices = dict(transformed_links.matrices)
    for label in broken_link_labels:
        broken_link_matrices[label] = links.matrices[label]
    broken_links = hol.OrientedLinks(complex_, broken_link_matrices)
    if complex_.two_cells:
        boundary = complex_.two_cells[0].boundary
        cycle = hol.cycle_holonomy(complex_, links, boundary)
        transformed_cycle = hol.cycle_holonomy(
            complex_, transformed_links, boundary
        )
        invariants = hol.conjugacy_invariants(cycle)
        transformed_invariants = hol.conjugacy_invariants(transformed_cycle)
        cycle_matrices = cycle.matrix[None, ...]
        transformed_cycle_matrices = transformed_cycle.matrix[None, ...]
        invariant_vectors = np.array(
            [[invariants.trace, invariants.determinant, invariants.discriminant]]
        )
        transformed_invariant_vectors = np.array(
            [
                [
                    transformed_invariants.trace,
                    transformed_invariants.determinant,
                    transformed_invariants.discriminant,
                ]
            ]
        )
        passive_residual = float(
            np.max(
                np.abs(
                    transformed_cycle.matrix
                    - np.linalg.inv(frames[cycle.base_vertex])
                    @ cycle.matrix
                    @ frames[cycle.base_vertex]
                )
            )
        )
        invariant_residual = float(
            np.max(np.abs(invariant_vectors - transformed_invariant_vectors))
        )
    else:
        cycle_matrices = np.empty((0, 2, 2))
        transformed_cycle_matrices = np.empty((0, 2, 2))
        invariant_vectors = np.empty((0, 3))
        transformed_invariant_vectors = np.empty((0, 3))
        passive_residual = max(
            float(
                np.max(
                    np.abs(
                        transformed_links.matrices[edge.label]
                        - np.linalg.inv(frames[edge.target])
                        @ links.matrices[edge.label]
                        @ frames[edge.source]
                    )
                )
            )
            for edge in complex_.edges
        )
        invariant_residual = 0.0

    states = {
        "0": np.array([1.0, 0.0]),
        "1": np.array([1.0, 1.0]),
        "2": np.zeros(2),
        "3": np.zeros(2),
    }
    paths = {
        "0": (),
        "1": ("e10",),
        "2": ("e21", "e10"),
        "3": ("e32", "e21", "e10"),
    }
    marks = ("quiet", "signal")
    covectors = np.array([[0.0, 0.0], [1.0, 0.0]])
    baseline = hol.operational_record_law(
        complex_, links, states, "0", paths, marks, covectors
    )
    transformed_states = hol.passive_transform_states(complex_, states, frames)
    transformed_covectors = hol.passive_transform_covectors(
        complex_, covectors, "0", frames
    )
    coherent = hol.operational_record_law(
        complex_,
        transformed_links,
        transformed_states,
        "0",
        paths,
        marks,
        transformed_covectors,
    )
    broken = hol.operational_record_law(
        complex_,
        broken_links,
        transformed_states,
        "0",
        paths,
        marks,
        transformed_covectors,
    )
    mark_values = {"quiet": 0.0, "signal": 1.0}
    baseline_observable = hol.operational_observable(baseline, mark_values)
    coherent_observable = hol.operational_observable(coherent, mark_values)
    broken_observable = hol.operational_observable(broken, mark_values)
    trivialization = hol.trivialization_via_spanning_tree(complex_, links)
    expected_trivialization = (
        0.0 if scenario in {"flat_tree", "flat_cycle"} else 1.0
    )

    operational_arrays = _record_law_arrays(baseline, coherent, broken)
    operational_arrays.update(
        _frozen_arrays(
            {
                "baseline_states": np.stack(
                    [states[vertex] for vertex in complex_.vertices]
                ),
                "mark_covectors": covectors,
                "transformed_mark_covectors": transformed_covectors,
                "transformed_states": np.stack(
                    [transformed_states[vertex] for vertex in complex_.vertices]
                ),
            }
        )
    )
    operational_residual = abs(baseline_observable - coherent_observable)
    expected_frustration_gap: float | None = None
    frustration_gap: float | None = None

    if scenario == "frustrated_transport":
        frustrated_state = {"2": np.array([1.0, 1.0])}
        short = hol.operational_record_law(
            complex_,
            links,
            frustrated_state,
            "0",
            {"2": ("e21", "e10")},
            marks,
            covectors,
        )
        long = hol.operational_record_law(
            complex_,
            links,
            frustrated_state,
            "0",
            {"2": ("e23", "e30")},
            marks,
            covectors,
        )
        frustration_gap = hol.operational_observable(
            long, mark_values
        ) - hol.operational_observable(short, mark_values)
        expected_frustration_gap = 0.3807970779778823
        operational_residual = max(
            operational_residual,
            abs(frustration_gap - expected_frustration_gap),
        )
        operational_arrays.update(
            _frozen_arrays(
                {
                    "frustrated_long_logits": long.logits,
                    "frustrated_long_probabilities": long.probabilities,
                    "frustrated_long_transported_state": long.transported_state,
                    "frustrated_observable_gap": [frustration_gap],
                    "frustrated_short_logits": short.logits,
                    "frustrated_short_probabilities": short.probabilities,
                    "frustrated_short_transported_state": short.transported_state,
                }
            )
        )

    aggregation_arrays = _frozen_arrays(
        {
            "agent_contributions": np.empty((0, 2)),
            "block_contributions": np.empty((0, 2)),
            "direct_total": np.empty((0, 2)),
            "staged_total": np.empty((0, 2)),
        }
    )
    if scenario == "staged_aggregation":
        stage_states = {
            "0": np.array([1.0, 0.0]),
            "1": np.array([1.0, 1.0]),
            "2": np.array([1.0, 1.0]),
            "3": np.array([1.0, 0.0]),
        }
        stage_paths = {**paths, "3": ("e30",)}
        contributions = []
        for vertex in complex_.vertices:
            path = stage_paths[vertex]
            contribution = stage_states[vertex]
            if path:
                contribution = (
                    hol.open_path_transport(complex_, links, path).matrix
                    @ contribution
                )
            contributions.append(contribution)
        agent_contributions = np.stack(contributions)
        block_contributions = np.stack(
            [agent_contributions[:2].sum(axis=0), agent_contributions[2:].sum(axis=0)]
        )
        direct_total = agent_contributions.sum(axis=0)
        staged_total = block_contributions.sum(axis=0)
        direct_law = hol.operational_record_law(
            complex_, links, stage_states, "0", stage_paths, marks, covectors
        )
        staged_law = hol.operational_record_law(
            complex_,
            links,
            {"0": staged_total},
            "0",
            {"0": ()},
            marks,
            covectors,
        )
        operational_residual = max(
            operational_residual,
            abs(
                hol.operational_observable(direct_law, mark_values)
                - hol.operational_observable(staged_law, mark_values)
            ),
            float(np.max(np.abs(direct_total - staged_total))),
        )
        aggregation_arrays = _frozen_arrays(
            {
                "agent_contributions": agent_contributions,
                "block_contributions": block_contributions,
                "direct_probabilities": direct_law.probabilities,
                "direct_total": direct_total[None, :],
                "staged_probabilities": staged_law.probabilities,
                "staged_total": staged_total[None, :],
            }
        )

    cycle_comparison_applicable = bool(complex_.two_cells)
    cycle_metric = (
        target_metric(
            invariant_residual,
            tolerance,
            target=0.0,
            interpretation=(
                "Trace, determinant, and discriminant agree under represented "
                "cycle conjugation."
            ),
            theorem_status="ESTABLISHED",
            verification_state="CANDIDATE",
            claim_origin="STANDARD",
        )
        if cycle_comparison_applicable
        else MetricRecord(
            value=0.0,
            tolerance=tolerance,
            status="inconclusive",
            interpretation=(
                "Cycle conjugacy comparison is not applicable because the flat-tree "
                "scenario declares no cycle."
            ),
            assessment_scope="implementation_check",
            theorem_status="ESTABLISHED",
            verification_state="CANDIDATE",
            claim_origin="STANDARD",
        )
    )
    metrics = {
        "passive_covariance_residual": target_metric(
            passive_residual,
            tolerance,
            target=0.0,
            interpretation=(
                "The declared graph-link cycle obeys the coherent passive frame law; "
                "this is not a dynamical symmetry claim."
            ),
            theorem_status="ESTABLISHED",
            verification_state="CANDIDATE",
            claim_origin="STANDARD",
        ),
        "cycle_conjugacy_invariant_residual": cycle_metric,
        "trivialization_residual": target_metric(
            abs(trivialization.max_edge_residual - expected_trivialization),
            tolerance,
            target=0.0,
            interpretation=(
                "The finite graph matches its declared flat/nonflat coboundary "
                "criterion; the check makes no base-connection claim."
            ),
            theorem_status="ESTABLISHED",
            verification_state="CANDIDATE",
            claim_origin="PROJECT_NOVEL",
        ),
        "operational_observable_residual": target_metric(
            operational_residual,
            tolerance,
            target=0.0,
            interpretation=(
                "The scalar expectation of the normalized marked law is preserved "
                "when states, links, and covectors transform coherently."
            ),
            theorem_status="ESTABLISHED",
            verification_state="CANDIDATE",
            claim_origin="PROJECT_NOVEL",
        ),
        "broken_link_negative_control": lower_bounded_metric(
            abs(broken_observable - baseline_observable),
            tolerance,
            lower_bound=1.0e-3,
            interpretation=(
                "Replacing exactly one coherently transformed undirected link pair "
                "with its original pair produces a detectable operational mismatch."
            ),
            theorem_status="NUMERICAL",
            verification_state="CANDIDATE",
            claim_origin="APPLICATION_SPECIFIC",
        ),
    }
    bundles = {
        "oriented_links": _frozen_arrays(
            {
                **links.matrices,
                **{
                    f"coherent_{label}": matrix
                    for label, matrix in transformed_links.matrices.items()
                },
                **{
                    f"broken_{label}": matrix
                    for label, matrix in broken_links.matrices.items()
                },
            }
        ),
        "vertex_frames": _frozen_arrays(
            {f"frame_{vertex}": frame for vertex, frame in frames.items()}
        ),
        "cycle_holonomies": _frozen_arrays(
            {
                "is_trivializable": [trivialization.is_trivializable],
                "original": cycle_matrices,
                "original_invariants": invariant_vectors,
                "comparison_applicable": [cycle_comparison_applicable],
                "transformed": transformed_cycle_matrices,
                "transformed_invariants": transformed_invariant_vectors,
                "trivialization_max_edge_residual": [
                    trivialization.max_edge_residual
                ],
            }
        ),
        "operational_record_laws": operational_arrays,
        "aggregation_stages": aggregation_arrays,
    }
    interaction_record = {
        "scenario": scenario,
        "group": "GL+(2)",
        "vertices": list(complex_.vertices),
        "oriented_edges": [asdict(edge) for edge in complex_.edges],
        "two_cells": [
            {"label": cell.label, "boundary": list(cell.boundary)}
            for cell in complex_.two_cells
        ],
        "scope": {
            "object": "finite_declared_graph_links",
            "base_connection_identification": False,
            "dynamical_symmetry_claim": False,
            "continuum_claim": False,
            "universality_claim": False,
            "physical_time_claim": False,
        },
        "claim_metadata": {
            "theorem_status": "NUMERICAL",
            "verification_state": "CANDIDATE",
            "claim_origin": "APPLICATION_SPECIFIC",
        },
        "negative_control_mutation": {
            "undirected_link_pair": list(broken_link_labels),
            "mutated_oriented_edges": list(broken_link_labels),
            "replacement": "original_declared_link_pair",
        },
        "metric_decisions": {
            "passive_covariance_residual": {
                "rule": "target",
                "observed_value": passive_residual,
                "reference_value": 0.0,
                "tolerance": tolerance,
            },
            "cycle_conjugacy_invariant_residual": {
                "rule": "target" if cycle_comparison_applicable else "not_applicable",
                "observed_value": invariant_residual,
                "reference_value": 0.0 if cycle_comparison_applicable else None,
                "tolerance": tolerance,
                "comparison_applicable": cycle_comparison_applicable,
            },
            "trivialization_residual": {
                "rule": "target",
                "observed_value": abs(
                    trivialization.max_edge_residual - expected_trivialization
                ),
                "reference_value": 0.0,
                "tolerance": tolerance,
                "actual_max_edge_residual": trivialization.max_edge_residual,
                "expected_max_edge_residual": expected_trivialization,
            },
            "operational_observable_residual": {
                "rule": "target",
                "observed_value": operational_residual,
                "reference_value": 0.0,
                "tolerance": tolerance,
                "baseline_observable": baseline_observable,
                "coherent_observable": coherent_observable,
                "frustration_gap": frustration_gap,
                "expected_frustration_gap": expected_frustration_gap,
            },
            "broken_link_negative_control": {
                "rule": "lower_bound",
                "observed_value": abs(broken_observable - baseline_observable),
                "reference_value": 1.0e-3,
                "tolerance": tolerance,
                "baseline_observable": baseline_observable,
                "broken_observable": broken_observable,
            },
        },
    }
    return bundles, metrics, interaction_record


def _flatten_bundles(
    bundles: Mapping[str, Mapping[str, np.ndarray]],
) -> dict[str, np.ndarray]:
    return {
        f"{bundle_name}.{array_name}": array
        for bundle_name, arrays in bundles.items()
        for array_name, array in arrays.items()
    }


def run_holonomy_experiment(config: ExperimentConfig) -> HolonomyExperimentResult:
    """Validate, compute, and atomically publish one finite holonomy scenario."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    theory = config.theory
    if theory.experiment != "gauge_holonomy":
        raise ValueError("holonomy experiment requires theory.experiment='gauge_holonomy'")
    if theory.fixture != _FIXTURE_NAME:
        raise ValueError("holonomy experiment requires the frozen two-scale fixture")
    if theory.group != "GL+(2)":
        raise ValueError("holonomy experiment requires group='GL+(2)'")
    if theory.scenario not in _SCENARIOS:
        raise ValueError("holonomy experiment scenario is not declared")
    if config.output.render_figures:
        raise ValueError("the holonomy laboratory exposes no figure renderer")

    repo_root = Path(__file__).resolve().parents[3]
    fixture, application_id, fixture_sha256 = _load_fixture(repo_root)
    complex_, links = _scenario_fixture(fixture, theory.scenario)
    bundles, metrics, interaction_record = _scenario_arrays(
        complex_,
        links,
        theory.scenario,
        config.numerics.atol + config.numerics.rtol,
    )
    interaction_record["application_id"] = application_id
    interaction_record["fixture_file_sha256"] = fixture_sha256

    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    provenance = collect_provenance(
        repo_root, repo_root / "Theory", config_hash, streams
    )
    input_hashes = dict(provenance["input_hashes"])
    input_hashes.update(
        {
            "fixture_application_id": application_id,
            "fixture_file_sha256": fixture_sha256,
        }
    )
    provenance.update(
        {
            "input_hashes": input_hashes,
            "experiment_scope": "finite_declared_graph_link_holonomy",
            "effective_backend": config.compute.backend,
            "effective_dtype": config.compute.dtype,
            "arithmetic_provenance": "floating_point_float64",
            "graph_to_base_identification": False,
            "experiment_module_path": str(Path(__file__).resolve()),
        }
    )
    store = RunStore.create(config, provenance)
    store.write_json(
        "metrics", {name: asdict(metrics[name]) for name in sorted(metrics)}
    )
    store.write_json("interaction_complex", interaction_record)
    for name, arrays in bundles.items():
        store.write_npz(name, arrays)
    store.finalize(("metrics.json", *_SCIENTIFIC_ARTIFACTS))

    artifacts = {
        Path(filename).stem: store.run_dir / filename
        for filename in _SCIENTIFIC_ARTIFACTS
    }
    metric_statuses = {metric.status for metric in metrics.values()}
    status: MetricStatus = (
        "fail"
        if "fail" in metric_statuses
        else "inconclusive"
        if "inconclusive" in metric_statuses
        else "pass"
    )
    return HolonomyExperimentResult(
        run_dir=store.run_dir,
        config_hash=store.config_hash,
        status=status,
        scenario=theory.scenario,
        theorem_status="NUMERICAL",
        verification_state="CANDIDATE",
        claim_origin="APPLICATION_SPECIFIC",
        metrics=MappingProxyType(dict(metrics)),
        arrays=MappingProxyType(_flatten_bundles(bundles)),
        artifacts=MappingProxyType(artifacts),
    )


__all__ = ["HolonomyExperimentResult", "run_holonomy_experiment"]
