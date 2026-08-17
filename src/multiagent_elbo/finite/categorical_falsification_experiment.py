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
    upper_bounded_metric,
    readonly_array,
    target_metric,
)
from multiagent_elbo.runtime import RngStreams, collect_provenance

from .categorical_falsification_model import (
    build_reference_model,
    build_reduced_model,
)
from .closure_residual import coarse_closure_residual, model_closure_residual
from .coarse_composition import run_coarse_composition_measurement
from .downward_influence import influence_report
from .partition_dynamics import null_control_comparison, persistence_statistics
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

COARSE_RATIO_THRESHOLD = 0.10
EXIT_SEED_MINIMUM = 32
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
    model = build_reference_model()
    coarse = coarse_closure_residual(model, REFERENCE_RECORD)
    against = model_closure_residual(model, REFERENCE_RECORD)
    metrics = {
        "CFL-06_coarse_three_body_ratio": upper_bounded_metric(
            coarse.three_to_two_ratio,
            tolerance,
            upper_bound=COARSE_RATIO_THRESHOLD,
            interpretation=(
                "blocking generates a three-body coarse coupling, measured against "
                "the pairwise one; this is the direction a renormalization step runs, "
                "and a small ratio means a pairwise coarse theory is a truncation "
                "with a small residual rather than a misdescription; the threshold "
                "was fixed after the first measurement and is not pre-registered, so "
                "this metric records rather than corroborates"
            ),
            theorem_status="NUMERICAL",
            verification_state="CANDIDATE",
            claim_origin="PROJECT_NOVEL",
        ),
        "CFL-07_pairwise_closure_residual_ratio": lower_bounded_metric(
            float(coarse.flow_weighted_residual),
            tolerance,
            lower_bound=0.0,
            interpretation=(
                "omitted many-body mass of the coarse theory measured against the "
                "retained flow the model itself assigns, not against a sup norm"
            ),
            theorem_status="NUMERICAL",
            verification_state="CANDIDATE",
            claim_origin="PROJECT_NOVEL",
        ),
    }
    detail = {
        "observation": list(REFERENCE_RECORD),
        "coarse_partition": [list(block) for block in coarse.partition],
        "coarse_order_magnitudes": {
            str(order): float(value) for order, value in coarse.order_magnitudes
        },
        "coarse_three_body_coefficient": float(coarse.largest_three_body_coefficient),
        "coarse_two_body_coefficient": float(coarse.largest_two_body_coefficient),
        "coarse_three_to_two_ratio": float(coarse.three_to_two_ratio),
        "flow_weighted_residual": float(coarse.flow_weighted_residual),
        "pairwise_closure_holds": bool(coarse.pairwise_closure_holds),
        "against_direction_three_body_coefficient": float(
            against.largest_three_body_coefficient
        ),
        "against_direction_note": (
            "eliminating a block parent and keeping its children runs against the "
            "coarse-graining direction and is not a renormalization step; it is "
            "recorded only as the generic common-cause mechanism"
        ),
    }
    arrays = {
        "coarse_order_magnitudes": np.asarray(
            [value for _, value in coarse.order_magnitudes], dtype=np.float64
        ),
        "block_three_body_coefficients": np.asarray(
            [float(block.largest_three_body_coefficient) for block in against.blocks],
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


def _open_instance_metric(
    value: float,
    tolerance: float,
    *,
    interpretation: str,
) -> MetricRecord:
    """Record a measurement bearing on an open hypothesis at one finite instance.

    These quantities are measured soundly, but a single finite instance neither
    establishes nor refutes the general hypothesis they bear on, so the metric is
    inconclusive by construction rather than by outcome. Marking such a metric as
    passing would claim support the run does not have, and marking it as failing
    would read as a software fault. The sharp instance-level statement is carried
    by the pre-registered falsifier verdicts published beside the metrics.
    """
    return MetricRecord(
        value=float(value),
        tolerance=float(tolerance),
        status="inconclusive",
        interpretation=interpretation,
        assessment_scope="implementation_check",
        theorem_status="OPEN",
        verification_state="INCONCLUSIVE",
        claim_origin="PROJECT_NOVEL",
    )


def _dynamics_metrics(
    tolerance: float,
    seed: int,
    restarts: int,
    null_seeds: int,
) -> tuple[dict[str, MetricRecord], dict[str, object], dict[str, np.ndarray]]:
    """Measure partition persistence, downward influence, and the null control."""
    model = build_reference_model()
    steps = max(60, min(300, restarts * 2))
    exit_seeds = tuple(range(max(8, restarts // 4)))
    exit_sweep_is_powered = len(exit_seeds) >= EXIT_SEED_MINIMUM
    persistence = persistence_statistics(
        model,
        seed=seed,
        noise=1.0,
        steps=steps,
        initializations=restarts,
        exit_seeds=exit_seeds,
        exit_noise_values=(0.3, 0.5, 0.8, 1.0, 1.5, 2.0),
    )
    null = null_control_comparison(
        tuple(range(1, null_seeds + 1)),
        noise=1.0,
        steps=max(40, steps // 2),
        initializations=max(8, restarts // 2),
    )
    influence = influence_report(model)

    influences = [row.influence for row in influence]
    controls = [row.control for row in influence]
    metrics = {
        "CFL-12_partition_residence_ratio": _open_instance_metric(
            persistence.residence_ratio,
            tolerance,
            interpretation=(
                "residence time of the most persistent partition against the belief "
                "relaxation time, pre-registered support threshold ten; one finite "
                "instance cannot close an open hypothesis either way, and the "
                "instance-level verdict is carried by the falsifier record"
            ),
        ),
        "CFL-13_exit_time_fit_r_squared": _open_instance_metric(
            persistence.exit_fit.r_squared,
            tolerance,
            interpretation=(
                "linearity of log exit time in inverse noise, pre-registered support "
                "threshold 0.90; the fit is seed-count sensitive, so the verdict is "
                "published only when the sweep carries at least the declared minimum "
                "number of exit seeds"
            ),
        ),
        "CFL-14_downward_influence_supremum": lower_bounded_metric(
            min(influences),
            tolerance,
            lower_bound=1.0e-6,
            interpretation=(
                "the declared downward kernel moves the child optimum across parent "
                "states, so the meta-agent is not decorative"
            ),
            theorem_status="NUMERICAL",
            verification_state="CANDIDATE",
            claim_origin="PROJECT_NOVEL",
        ),
        "CFL-15_deterministic_control_collapse": _open_instance_metric(
            min(controls),
            tolerance,
            interpretation=(
                "the deterministic fiber disintegration measured on the same "
                "statistic as the declared influence; it does not collapse on the "
                "small blocks, which is reported rather than tuned away"
            ),
        ),
        "CFL-16_null_control_separation": _open_instance_metric(
            abs(
                persistence.residence_ratio
                - float(np.median(null.null_residence_ratio))
            ),
            tolerance,
            interpretation=(
                "distance between the reference residence ratio and the median of "
                "its null distribution under randomized transports and beliefs; the "
                "reference lying inside the null range means the pipeline is "
                "reporting its own blocking algorithm"
            ),
        ),
    }
    null_ratios = [float(value) for value in null.null_residence_ratio]
    inside_null = bool(
        min(null_ratios) <= persistence.residence_ratio <= max(null_ratios)
    )
    part = {
        "modal_partition": [list(block) for block in persistence.modal_partition],
        "modal_occupancy": float(persistence.modal_occupancy),
        "maximum_residence_time": float(persistence.maximum_residence_time),
        "belief_relaxation_time": float(persistence.relaxation_time),
        "residence_ratio": float(persistence.residence_ratio),
        "timescale_falsifier_fired": bool(persistence.timescale_falsifier_fired),
        "exit_slope": float(persistence.exit_fit.slope),
        "exit_r_squared": float(persistence.exit_fit.r_squared),
        "exit_linearity_falsifier_fired": bool(
            persistence.exit_fit.linearity_falsifier_fired
        ),
        "exit_seed_count": len(exit_seeds),
        "exit_censored_fraction": max(
            float(value) for value in persistence.exit_fit.censored_fraction
        ),
        "exit_sweep_is_powered": exit_sweep_is_powered,
        "largest_off_diagonal_co_membership": float(
            persistence.largest_off_diagonal_co_membership
        ),
        "null_residence_ratios": null_ratios,
        "reference_ratio_inside_null_range": inside_null,
        "downward_influence": [
            {
                "block": list(row.block),
                "agent": row.agent,
                "influence": float(row.influence),
                "control": float(row.control),
                "generative_reference_control": float(
                    row.generative_reference_control
                ),
                "control_collapsed": bool(row.control_collapsed),
            }
            for row in influence
        ],
        "min_downward_influence": min(influences),
        "any_control_collapsed": any(row.control_collapsed for row in influence),
    }
    arrays = {
        "null_residence_ratios": np.asarray(null_ratios, dtype=np.float64),
        "downward_influences": np.asarray(influences, dtype=np.float64),
        "deterministic_controls": np.asarray(controls, dtype=np.float64),
        "exit_mean_times": np.asarray(
            persistence.exit_fit.mean_exit_times, dtype=np.float64
        ),
        "exit_noise_values": np.asarray(
            persistence.exit_fit.noise_values, dtype=np.float64
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
    pre-registered refutation describes. The two can disagree, because a metric
    can be an implementation check on a quantity whose value carries a separate
    refutation criterion.
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
    if "coarse_three_to_two_ratio" in detail:
        verdicts["M3_coarse_residual_not_small"] = bool(
            float(detail["coarse_three_to_two_ratio"]) > COARSE_RATIO_THRESHOLD
        )
    if "timescale_falsifier_fired" in detail:
        verdicts["M5_no_timescale_separation"] = bool(
            detail["timescale_falsifier_fired"]
        )
        if detail["exit_sweep_is_powered"]:
            verdicts["M5_exit_times_not_arrhenius"] = bool(
                detail["exit_linearity_falsifier_fired"]
            )
        verdicts["NULL_pipeline_detects_its_own_blocking"] = bool(
            detail["reference_ratio_inside_null_range"]
        )
    if "min_downward_influence" in detail:
        verdicts["M6_meta_agent_is_decorative"] = bool(
            float(detail["min_downward_influence"]) <= 1.0e-12
        )
        verdicts["M6_deterministic_control_did_not_collapse"] = not bool(
            detail["any_control_collapsed"]
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
        rule = (
            "target"
            if name in _TARGET_RULES
            else "lower_bound"
            if name in _LOWER_BOUND_RULES
            else "upper_bound"
            if name in _UPPER_BOUND_RULES
            else "not_applicable"
        )
        decisions[name] = {
            "rule": rule,
            "observed_value": metric.value,
            "reference_value": _TARGET_RULES.get(
                name, _LOWER_BOUND_RULES.get(name, _UPPER_BOUND_RULES.get(name))
            ),
            "tolerance": metric.tolerance,
            "status": metric.status,
        }
    declared = set(_TARGET_RULES) | set(_LOWER_BOUND_RULES) | set(_UPPER_BOUND_RULES)
    orphaned = sorted(declared - set(metrics))
    if orphaned:
        raise ValueError(
            "declared decision rules name no measured metric: " + ", ".join(orphaned)
        )
    return decisions


_TARGET_RULES: dict[str, float] = {
    "CFL-01_tower_accounting_residual": 0.0,
    "CFL-03_coarse_composition_residual": 0.0,
    "CFL-04_row_average_discrepancy": 0.4,
    "CFL-09_model_holonomy_distortion": 0.0,
    "CFL-10_dressed_transport_mass": 0.0,
}

_UPPER_BOUND_RULES: dict[str, float] = {
    "CFL-06_coarse_three_body_ratio": COARSE_RATIO_THRESHOLD,
}

_LOWER_BOUND_RULES: dict[str, float] = {
    "CFL-02_naive_local_overcount": 1.0e-6,
    "CFL-05_product_form_substitution_gap": 1.0e-6,
    "CFL-07_pairwise_closure_residual_ratio": 0.0,
    "CFL-08_belief_holonomy_distortion": 1.0e-6,
    "CFL-11_restricted_dressed_mass_defect": 1.0e-6,

    "CFL-13_exit_time_fit_r_squared": 0.90,
    "CFL-14_downward_influence_supremum": 1.0e-6,


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

    dynamics = _dynamics_metrics(
        tolerance,
        config.run.seed,
        config.theory.descent_restarts,
        config.theory.null_control_seeds,
    )
    metrics.update(dynamics[0])
    detail.update(dynamics[1])
    arrays.update(dynamics[2])

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
