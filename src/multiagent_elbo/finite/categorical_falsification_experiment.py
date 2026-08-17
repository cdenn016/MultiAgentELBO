"""Run the finite categorical two-channel falsification laboratory.

The design is frozen in
`docs/experiments/2026-08-16-finite-categorical-falsification/spec.md` and its
metric contracts are pre-registered in `docs/hypotheses.md`. Six agents sit on two
directed three-cycles at one contextual point, the structure group is Z_3 carrying
two distinct representations, and every state is a pair of laws from finite
orbit-closed families. Nothing is Gaussian, deliberately: Gaussian closure
properties are special and would confound a failure of the mechanism with a failure
of the ansatz.

This laboratory can refute a proposed mechanism. It cannot certify a theorem,
exhibit a rescaling map, or establish persistence, a continuum limit, or physical
time. A fired falsifier is a result and is reported as one.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

import numpy as np

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.experiment_support import (
    MetricRecord,
    MetricStatus,
    lower_bounded_metric,
    readonly_array,
    target_metric,
)
from multiagent_elbo.runtime import RngStreams, collect_provenance

from .categorical_falsification_model import (
    build_reference_model,
    build_reduced_model,
)
from .closure_residual import model_closure_residual
from .coarse_composition import run_coarse_composition_measurement
from .holonomy_retention import (
    barycenter_is_group_element,
    convolution_converse_witness,
    declared_endpoint_kernel,
    dressed_barycenter,
    dressed_transport_law,
    exact_dressed_transport_law,
    logical_chain_report,
    prediction_report,
    restricted_dressed_mass,
    retention_report,
    theory_falsifier_verdict,
)
from .tower_vfe import (
    decomposed_tower_free_energy,
    naive_local_potential_sum,
    seeded_tower_recognition,
    tower_accounting_residual,
    tower_observation_records,
)

ACCOUNTING_TOLERANCE = 1.0e-12
REFERENCE_RECORD = (1, 0, 1, 0, 1, 0)
RECOGNITION_SEEDS = (11, 4243)

_SCIENTIFIC_ARTIFACTS: tuple[str, ...] = (
    "metric_decisions.json",
    "measurements.json",
    "arrays.npz",
)


@dataclass(frozen=True)
class CategoricalFalsificationResult:
    """The published outcome of one falsification sweep."""

    run_dir: Path
    config_hash: str
    status: MetricStatus
    admitted_family: str
    fired_falsifiers: tuple[str, ...]
    metrics: Mapping[str, MetricRecord]
    arrays: Mapping[str, np.ndarray]


def _check_config(config: ExperimentConfig) -> None:
    """Reject any configuration this laboratory is not declared to run."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    theory = config.theory
    if getattr(theory, "experiment", None) != "categorical_falsification":
        raise ValueError(
            "categorical falsification requires theory.experiment="
            "'categorical_falsification'"
        )
    if theory.fixture != "two_channel_z3_v1":
        raise ValueError("fixture must be 'two_channel_z3_v1'")
    if theory.admitted_family not in ("orbit", "simplex", "both"):
        raise ValueError("admitted_family must be orbit, simplex, or both")
    if theory.arithmetic != "exact_rational":
        raise ValueError("arithmetic must be 'exact_rational'")
    if config.output.render_figures:
        raise ValueError("the categorical falsification laboratory exposes no renderer")


def _accounting_metrics(
    tolerance: float,
) -> tuple[dict[str, MetricRecord], dict[str, object], dict[str, np.ndarray]]:
    """Measure the tower accounting identity and the local-potential overcount."""
    model = build_reduced_model()
    records = tower_observation_records(model)
    residuals: list[float] = []
    overcounts: list[float] = []
    naive_sums: list[float] = []
    for record in (records[0], records[3], records[6]):
        for seed in RECOGNITION_SEEDS:
            recognition = seeded_tower_recognition(model, record, seed)
            residuals.append(
                abs(tower_accounting_residual(model, record, recognition))
            )
            naive, overcount = naive_local_potential_sum(model, record, recognition)
            naive_sums.append(naive)
            overcounts.append(overcount)
    groups = decomposed_tower_free_energy(
        model, records[3], seeded_tower_recognition(model, records[3], RECOGNITION_SEEDS[0])
    )
    metrics = {
        "CFL-01_tower_accounting_residual": target_metric(
            max(residuals),
            ACCOUNTING_TOLERANCE,
            target=0.0,
            interpretation=(
                "flat enumeration of the tower joint agrees with the sum of its "
                "conditional-KL groups"
            ),
            theorem_status="established_conditional_identity",
        ),
        "CFL-02_naive_local_overcount": lower_bounded_metric(
            min(overcounts),
            tolerance,
            lower_bound=1.0e-6,
            interpretation=(
                "summing singleton local row potentials double counts every shared "
                "interaction factor; the naive sum is not an evidence bound"
            ),
            theorem_status="negative_control",
        ),
    }
    detail = {
        "records_measured": [list(records[index]) for index in (0, 3, 6)],
        "recognition_seeds": list(RECOGNITION_SEEDS),
        "max_accounting_residual": max(residuals),
        "min_overcount": min(overcounts),
        "max_overcount": max(overcounts),
        "decomposition_groups": {
            name: float(value) for name, value in asdict(groups).items()
        },
    }
    arrays = {
        "accounting_residuals": np.asarray(residuals, dtype=np.float64),
        "local_overcounts": np.asarray(overcounts, dtype=np.float64),
        "naive_local_sums": np.asarray(naive_sums, dtype=np.float64),
    }
    return metrics, detail, arrays


def _composition_metrics(
    tolerance: float,
) -> tuple[dict[str, MetricRecord], dict[str, object], dict[str, np.ndarray]]:
    """Measure coarse-edge composition and the two aggregation controls."""
    measurement = run_coarse_composition_measurement()
    witness = measurement.three_node_witness
    metrics = {
        "CFL-03_coarse_composition_residual": target_metric(
            measurement.max_composition_residual,
            tolerance,
            target=0.0,
            interpretation=(
                "nested pushforwards of the directed edge-event law compose through "
                "a general correlated endpoint kernel"
            ),
            theorem_status="established_conditional_identity",
        ),
        "CFL-04_row_average_discrepancy": target_metric(
            witness.discrepancy,
            tolerance,
            target=0.4,
            interpretation=(
                "uniform row averaging is not the event-law pushforward; the literal "
                "three-node witness separates them by four tenths"
            ),
            theorem_status="negative_control",
        ),
        "CFL-05_product_form_substitution_gap": lower_bounded_metric(
            measurement.min_product_form_discrepancy,
            tolerance,
            lower_bound=1.0e-6,
            interpretation=(
                "assuming a product endpoint kernel while the endpoint assignments "
                "are correlated moves the coarse event law"
            ),
            theorem_status="negative_control",
        ),
    }
    detail = {
        "three_node_beta_coarse": float(witness.beta_coarse),
        "three_node_beta_naive": float(witness.beta_naive),
        "three_node_discrepancy": float(witness.discrepancy),
        "correlated_is_product_form": bool(measurement.correlated_is_product_form),
        "substituted_is_product_form": bool(measurement.substituted_is_product_form),
        "max_composition_residual": float(measurement.max_composition_residual),
        "max_mass_residual": float(measurement.max_mass_residual),
        "max_row_average_discrepancy": float(measurement.max_row_average_discrepancy),
        "cases": [
            {
                "channel": case.channel,
                "configuration": case.configuration,
                "composition_residual": float(case.composition_residual),
                "product_form_discrepancy": float(case.product_form_discrepancy),
                "row_average_discrepancy": float(case.row_average_discrepancy),
            }
            for case in measurement.cases
        ],
    }
    arrays = {
        "composition_residuals": np.asarray(
            [case.composition_residual for case in measurement.cases], dtype=np.float64
        ),
        "row_average_discrepancies": np.asarray(
            [case.row_average_discrepancy for case in measurement.cases],
            dtype=np.float64,
        ),
    }
    return metrics, detail, arrays


def _closure_metrics(
    tolerance: float,
) -> tuple[dict[str, MetricRecord], dict[str, object], dict[str, np.ndarray]]:
    """Measure the generated three-body term and the pairwise closure residual."""
    report = model_closure_residual(build_reference_model(), REFERENCE_RECORD)
    coefficient = abs(float(report.largest_three_body_coefficient))
    metrics = {
        "CFL-06_largest_three_body_coefficient": lower_bounded_metric(
            coefficient,
            tolerance,
            lower_bound=1.0e-6,
            interpretation=(
                "exact elimination of the block parent generates a three-body term, "
                "so a pairwise coarse theory is a truncation carrying a residual"
            ),
            theorem_status="established_conditional_identity",
        ),
        "CFL-07_pairwise_closure_residual_ratio": lower_bounded_metric(
            float(report.flow_weighted_residual),
            tolerance,
            lower_bound=0.0,
            interpretation=(
                "omitted many-body mass measured against the retained flow the model "
                "itself assigns, not against an unweighted sup norm"
            ),
            theorem_status="NUMERICAL",
            verification_state="CANDIDATE",
            claim_origin="PROJECT_NOVEL",
        ),
    }
    detail = {
        "observation": list(REFERENCE_RECORD),
        "largest_three_body_block": list(report.largest_three_body_block),
        "largest_three_body_subset": sorted(report.largest_three_body_subset),
        "largest_three_body_coefficient": float(
            report.largest_three_body_coefficient
        ),
        "flow_weighted_residual": float(report.flow_weighted_residual),
        "pairwise_closure_holds": bool(report.pairwise_closure_holds),
    }
    arrays = {
        "block_three_body_coefficients": np.asarray(
            [float(block.largest_three_body_coefficient) for block in report.blocks],
            dtype=np.float64,
        ),
        "block_flow_weighted_residuals": np.asarray(
            [float(block.flow_weighted_residual) for block in report.blocks],
            dtype=np.float64,
        ),
    }
    return metrics, detail, arrays


def _holonomy_metrics(
    tolerance: float,
) -> tuple[dict[str, MetricRecord], dict[str, object], dict[str, np.ndarray]]:
    """Measure holonomy retention, its distortion scores, and the dressed law."""
    model = build_reference_model()
    prediction = prediction_report(model)
    verdict = theory_falsifier_verdict(model)
    chain = logical_chain_report(model)
    witness = convolution_converse_witness()

    kernel = declared_endpoint_kernel(model)
    pairs = ((kernel.labels[0], kernel.labels[0]), (kernel.labels[0], kernel.labels[1]))
    mass_errors: list[float] = []
    restricted_defects: list[float] = []
    barycenter_flags: list[bool] = []
    dressed: list[dict[str, object]] = []
    for channel in ("belief", "model"):
        for pair in pairs:
            exact = exact_dressed_transport_law(model, channel, kernel, pair)
            mass_errors.append(abs(float(sum(exact.values())) - 1.0))
            restricted = float(restricted_dressed_mass(model, channel, kernel, pair))
            restricted_defects.append(abs(restricted - 1.0))
            law = dressed_transport_law(model, channel, kernel, pair)
            representation = (
                model.belief_representation
                if channel == "belief"
                else model.model_representation
            )
            barycenter = dressed_barycenter(law, representation)
            in_group = barycenter_is_group_element(barycenter, representation)
            barycenter_flags.append(in_group)
            dressed.append(
                {
                    "channel": channel,
                    "coarse_pair": list(pair),
                    "atoms": {str(g): float(w) for g, w in law.items() if w > 0.0},
                    "exact_mass": float(sum(exact.values())),
                    "restricted_mass": restricted,
                    "barycenter_is_group_element": bool(in_group),
                }
            )

    metrics = {
        "CFL-08_belief_holonomy_distortion": lower_bounded_metric(
            prediction.belief_cyclic_simplex,
            tolerance,
            lower_bound=1.0e-6,
            interpretation=(
                "the block carrying nontrivial belief holonomy admits no "
                "zero-distortion belief parent; the orbit family empties the fixed "
                "sector entirely and the score is infinite there"
            ),
            theorem_status="established_conditional_identity",
        ),
        "CFL-09_model_holonomy_distortion": target_metric(
            prediction.model_cyclic_zero_distortion,
            tolerance,
            target=0.0,
            interpretation=(
                "the same block admits an exactly parallel parent in the flat model "
                "channel, so the asymmetry between channels is observable"
            ),
            theorem_status="established_conditional_identity",
        ),
        "CFL-10_dressed_transport_mass": target_metric(
            max(mass_errors),
            tolerance,
            target=0.0,
            interpretation=(
                "the dressed-transport law normalizes exactly when the endpoint "
                "factor is carried over all ordered pairs in the numerator"
            ),
            theorem_status="established_conditional_identity",
        ),
        "CFL-11_restricted_dressed_mass_defect": lower_bounded_metric(
            min(restricted_defects),
            tolerance,
            lower_bound=1.0e-6,
            interpretation=(
                "dropping the endpoint factor and restricting the sum to members of "
                "the two blocks does not give a probability measure under soft "
                "memberships"
            ),
            theorem_status="negative_control",
        ),
    }
    part = {
        "holonomy_predictions": {
            name: (list(value) if isinstance(value, tuple) else value)
            if not isinstance(value, dict)
            else {str(k): v for k, v in value.items()}
            for name, value in vars(prediction).items()
        },
        "holonomy_theory_falsifier_fired": bool(verdict.fired),
        "zero_distortion_block_count": len(verdict.zero_distortion_blocks),
        "logical_chain": {
            "flatness_implies_stabilization": bool(chain.flatness_implies_stabilization),
            "flatness_implies_agreement": bool(chain.flatness_implies_agreement),
            "stabilization_without_flatness_in_orbit_family": bool(
                chain.stabilization_without_flatness_in_orbit_family
            ),
            "stabilization_without_flatness_on_uniform": bool(
                chain.stabilization_without_flatness_on_uniform
            ),
            "disagreement_distortion_under_flat_transport": float(
                chain.disagreement_distortion
            ),
        },
        "convolution_converse": {
            "composite_matches_convolution": bool(witness.composite_matches_convolution),
            "joint_is_a_product": bool(witness.joint_is_a_product),
        },
        "dressed_transports": dressed,
        "max_dressed_mass_error": max(mass_errors),
        "min_restricted_mass_defect": min(restricted_defects),
        "any_barycenter_outside_the_group": not all(barycenter_flags),
    }
    arrays = {
        "dressed_mass_errors": np.asarray(mass_errors, dtype=np.float64),
        "restricted_mass_defects": np.asarray(restricted_defects, dtype=np.float64),
        "block_distortions": np.asarray(
            [row.distortion for row in retention_report(model)], dtype=np.float64
        ),
    }
    return metrics, part, arrays


def _json_safe(value: object) -> object:
    """Rewrite non-finite floats as explicit sentinels so the record stays JSON.

    An infinite distortion score is a scientific result here, not a numerical
    accident: it is what an empty fixed sector produces under the convention that
    the infimum over the empty set is positive infinity. The artifact contract
    forbids non-finite JSON, so the value is carried as the string "+infinity"
    rather than dropped or silently clamped to a finite surrogate.
    """
    if isinstance(value, float):
        if value == float("inf"):
            return "+infinity"
        if value == float("-inf"):
            return "-infinity"
        if value != value:
            return "nan"
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value


def _falsifier_verdicts(detail: Mapping[str, object]) -> dict[str, bool]:
    """Evaluate each pre-registered falsifier from the measured quantities.

    A falsifier verdict is not a metric status. A metric fails when the
    implementation check fails; a falsifier fires when the system behaves as the
    pre-registered refutation describes. The two can and do disagree: the
    three-body measurement passes as an implementation check precisely because it
    correctly detects the nonzero coefficient that fires the pairwise-closure
    falsifier.
    """
    verdicts: dict[str, bool] = {}
    if "max_accounting_residual" in detail:
        verdicts["M1_accounting_mismatch"] = bool(
            float(detail["max_accounting_residual"]) > ACCOUNTING_TOLERANCE
        )
        verdicts["M1_overcount_not_exercised"] = bool(
            float(detail["min_overcount"]) <= 0.0
        )
    if "max_composition_residual" in detail:
        verdicts["M2_composition_failure"] = bool(
            float(detail["max_composition_residual"]) > 1.0e-10
        )
        verdicts["M2_correlated_kernel_not_exercised"] = bool(
            detail["correlated_is_product_form"]
        )
    if "pairwise_closure_holds" in detail:
        verdicts["M3_pairwise_closure_false"] = not bool(
            detail["pairwise_closure_holds"]
        )
    if "holonomy_theory_falsifier_fired" in detail:
        verdicts["M4_no_zero_distortion_belief_parent_anywhere"] = bool(
            detail["holonomy_theory_falsifier_fired"]
        )
        verdicts["M4_dressed_law_unnormalized"] = bool(
            float(detail["max_dressed_mass_error"]) > 1.0e-12
        )
        verdicts["M4_restricted_form_not_exercised"] = bool(
            float(detail["min_restricted_mass_defect"]) <= 0.0
        )
    return verdicts


def _metric_decisions(metrics: Mapping[str, MetricRecord]) -> dict[str, object]:
    """Record every metric decision so a reader can recompute it from artifacts."""
    decisions: dict[str, object] = {}
    for name, metric in metrics.items():
        if metric.interpretation.startswith("__"):
            continue
        rule = "target" if name in _TARGET_RULES else "lower_bound"
        decisions[name] = {
            "rule": rule,
            "observed_value": metric.value,
            "reference_value": _TARGET_RULES.get(name, _LOWER_BOUND_RULES.get(name)),
            "tolerance": metric.tolerance,
            "status": metric.status,
        }
    return decisions


_TARGET_RULES: dict[str, float] = {
    "CFL-01_tower_accounting_residual": 0.0,
    "CFL-03_coarse_composition_residual": 0.0,
    "CFL-04_row_average_discrepancy": 0.4,
    "CFL-09_model_holonomy_distortion": 0.0,
    "CFL-10_dressed_transport_mass": 0.0,
}

_LOWER_BOUND_RULES: dict[str, float] = {
    "CFL-02_naive_local_overcount": 1.0e-6,
    "CFL-05_product_form_substitution_gap": 1.0e-6,
    "CFL-06_largest_three_body_coefficient": 1.0e-6,
    "CFL-07_pairwise_closure_residual_ratio": 0.0,
    "CFL-08_belief_holonomy_distortion": 1.0e-6,
    "CFL-11_restricted_dressed_mass_defect": 1.0e-6,
}


def run_categorical_falsification_experiment(
    config: ExperimentConfig,
) -> CategoricalFalsificationResult:
    """Validate, measure, and atomically publish one falsification sweep."""
    _check_config(config)
    tolerance = config.numerics.atol + config.numerics.rtol

    metrics: dict[str, MetricRecord] = {}
    detail: dict[str, object] = {}
    arrays: dict[str, np.ndarray] = {}
    for measure in (
        _accounting_metrics,
        _composition_metrics,
        _closure_metrics,
        _holonomy_metrics,
    ):
        part_metrics, part_detail, part_arrays = measure(tolerance)
        metrics.update(part_metrics)
        detail.update(part_detail)
        arrays.update(part_arrays)

    verdicts = _falsifier_verdicts(detail)
    detail["falsifier_verdicts"] = dict(verdicts)
    fired = tuple(sorted(name for name, hit in verdicts.items() if hit))
    statuses = {metric.status for metric in metrics.values()}
    status: MetricStatus = (
        "fail"
        if "fail" in statuses
        else "inconclusive"
        if "inconclusive" in statuses
        else "pass"
    )

    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    repo_root = Path(__file__).resolve().parents[3]
    provenance = collect_provenance(
        repo_root, repo_root / "Theory", config_hash, streams
    )
    provenance.update(
        {
            "experiment_scope": (
                "finite categorical two-channel falsification; refutes mechanisms, "
                "certifies no theorem"
            ),
            "effective_backend": "cpu",
            "effective_dtype": config.numerics.dtype,
            "arithmetic_provenance": "exact_rational_with_float_logarithms",
            "experiment_module_path": "multiagent_elbo/finite/"
            "categorical_falsification_experiment.py",
            "admitted_family": config.theory.admitted_family,
        }
    )

    store = RunStore.create(config, provenance)
    store.write_json("metrics", {name: asdict(metrics[name]) for name in sorted(metrics)})
    store.write_json("metric_decisions", _metric_decisions(metrics))
    store.write_json("measurements", _json_safe(detail))
    store.write_npz("arrays", arrays)
    store.finalize(("metrics.json", *_SCIENTIFIC_ARTIFACTS))

    return CategoricalFalsificationResult(
        run_dir=store.run_dir,
        config_hash=config_hash,
        status=status,
        admitted_family=config.theory.admitted_family,
        fired_falsifiers=fired,
        metrics=MappingProxyType(dict(metrics)),
        arrays=MappingProxyType(
            {name: readonly_array(value) for name, value in arrays.items()}
        ),
    )


__all__ = [
    "CategoricalFalsificationResult",
    "run_categorical_falsification_experiment",
]
