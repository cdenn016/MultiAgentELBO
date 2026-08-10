"""Artifact-backed exact scale-cocycle laboratory."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from types import MappingProxyType
from typing import Literal, Mapping

import numpy as np

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.experiment_support import (
    MetricRecord,
    readonly_array,
    target_metric,
    validate_two_scale_application_fixture,
)
from multiagent_elbo.runtime import RngStreams, collect_provenance

from .scale_cocycle import (
    ExactLinearIsomorphism,
    ExactMarkovChannel,
    anchored_mobius_decompose,
    base_fisher_cocycle_residual_forms,
    conditional_log_laplace_action,
    identified_linear_step,
    ordered_derivative_cocycle,
    posterior_bridge,
    projection_intertwining_residual,
    retained_beta_diagnostics,
)


F = Fraction
MetricStatus = Literal["pass", "fail", "inconclusive"]


@dataclass(frozen=True)
class ScaleCocycleExperimentResult:
    run_dir: Path
    config_hash: str
    status: MetricStatus
    metrics: Mapping[str, MetricRecord]
    arrays: Mapping[str, np.ndarray]


def _fraction(value: str) -> Fraction:
    return Fraction(value)


def _fraction_rows(rows: object) -> tuple[tuple[Fraction, ...], ...]:
    if not isinstance(rows, list):
        raise ValueError("fixture channel rows are invalid")
    return tuple(tuple(_fraction(value) for value in row) for row in rows)


def _fraction_vector(values: object) -> tuple[Fraction, ...]:
    if not isinstance(values, list):
        raise ValueError("fixture law is invalid")
    return tuple(_fraction(value) for value in values)


def _float_array(values: object) -> np.ndarray:
    array = np.asarray(values, dtype=object)
    converted = np.empty(array.shape, dtype=np.float64)
    for index in np.ndindex(array.shape):
        converted[index] = float(array[index])
    return readonly_array(converted)


def _fraction_strings(values: tuple[tuple[Fraction, ...], ...]) -> list[list[str]]:
    return [[str(value) for value in row] for row in values]


def _matmul(
    left: tuple[tuple[Fraction, ...], ...],
    right: tuple[tuple[Fraction, ...], ...],
) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(
            sum(
                (left[row][inner] * right[inner][column] for inner in range(len(right))),
                F(0),
            )
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def _maximum_gap(left: object, right: object) -> Fraction:
    left_array = np.asarray(left, dtype=object)
    right_array = np.asarray(right, dtype=object)
    if left_array.shape != right_array.shape:
        raise ValueError("exact diagnostic shapes do not match")
    return max(
        (abs(F(left_array[index]) - F(right_array[index])) for index in np.ndindex(left_array.shape)),
        default=F(0),
    )


def _build_extension(payload: Mapping[str, object]) -> tuple[dict[str, object], ExactMarkovChannel, ExactMarkovChannel, ExactMarkovChannel]:
    state_spaces = payload["state_spaces"]
    channel_payload = payload["channel"]
    if not isinstance(state_spaces, Mapping) or not isinstance(channel_payload, Mapping):
        raise ValueError("validated fixture structures are unavailable")
    fine = state_spaces["fine"]
    coarse = state_spaces["coarse"]
    arrows = channel_payload["arrows"]
    if not isinstance(fine, Mapping) or not isinstance(coarse, Mapping) or not isinstance(arrows, list):
        raise ValueError("validated fixture structures are unavailable")
    arrow = arrows[0]
    if not isinstance(arrow, Mapping):
        raise ValueError("validated fixture arrow is unavailable")
    fine_to_middle = ExactMarkovChannel(
        tuple(fine["labels"]),
        tuple(coarse["labels"]),
        _fraction_rows(arrow["rows"]),
    )
    middle_to_macro = ExactMarkovChannel(
        fine_to_middle.target_labels,
        ("macro-0", "macro-1"),
        (
            (F(3, 4), F(1, 4)),
            (F(1, 4), F(3, 4)),
            (F(2, 3), F(1, 3)),
            (F(1, 3), F(2, 3)),
        ),
    )
    fine_to_macro = fine_to_middle.compose(middle_to_macro)
    extension_without_id = {
        "schema_version": "three-level-composition-v1",
        "base_application_id": payload["application_id"],
        "fixture_mutated": False,
        "right_acting_composition": "fine_to_macro=fine_to_middle middle_to_macro",
        "fine_labels": list(fine_to_middle.source_labels),
        "middle_labels": list(fine_to_middle.target_labels),
        "macro_labels": list(middle_to_macro.target_labels),
        "fine_to_middle_rows": _fraction_strings(fine_to_middle.matrix),
        "middle_to_macro_rows": _fraction_strings(middle_to_macro.matrix),
        "fine_to_macro_rows": _fraction_strings(fine_to_macro.matrix),
    }
    canonical = json.dumps(
        extension_without_id,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    extension = dict(extension_without_id)
    extension["extension_id"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return extension, fine_to_middle, middle_to_macro, fine_to_macro


def _exact_fixtures(
    config: ExperimentConfig, payload: Mapping[str, object]
) -> tuple[dict[str, object], dict[str, MetricRecord], dict[str, np.ndarray]]:
    extension, first, second, direct_channel = _build_extension(payload)
    references = payload["reference_laws"]
    generative = payload["generative_structure"]
    recognition_payload = payload["recognition"]
    if not all(isinstance(value, Mapping) for value in (references, generative, recognition_payload)):
        raise ValueError("validated fixture law structures are unavailable")
    fine_reference = _fraction_vector(references["fine"]["values"])  # type: ignore[index]
    fine_evidence = _fraction_vector(generative["evidence_submeasure"])  # type: ignore[index]
    fine_posterior = _fraction_vector(generative["posterior"])  # type: ignore[index]
    fine_recognition = _fraction_vector(recognition_payload["fine_law"])  # type: ignore[index]

    typed_fine_laws = {
        "reference": fine_reference,
        "evidence": fine_evidence,
        "posterior": fine_posterior,
        "recognition": fine_recognition,
    }
    typed_direct = {name: direct_channel.pushforward(law) for name, law in typed_fine_laws.items()}
    typed_staged = {
        name: second.pushforward(first.pushforward(law))
        for name, law in typed_fine_laws.items()
    }
    direct_action = conditional_log_laplace_action(fine_reference, fine_evidence, direct_channel)
    middle_action = conditional_log_laplace_action(fine_reference, fine_evidence, first)
    staged_action = conditional_log_laplace_action(
        middle_action.coarse_reference,
        middle_action.coarse_evidence,
        second,
    )
    direct_bridge = posterior_bridge(fine_posterior, direct_channel)
    first_bridge = posterior_bridge(fine_posterior, first)
    second_bridge = posterior_bridge(first_bridge.coarse_posterior, second)
    staged_reverse = _matmul(second_bridge.reverse, first_bridge.reverse)

    source_identification = ExactLinearIsomorphism(
        "native-0", "reference", ((F(2), F(0)), (F(0), F(3)))
    )
    target_identification = ExactLinearIsomorphism(
        "native-1", "reference", ((F(5), F(0)), (F(0), F(7)))
    )
    native_step = ((F(1), F(2)), (F(3), F(4)))
    identified_step = identified_linear_step(
        source_identification, native_step, target_identification
    )
    derivative_first = ((F(1), F(1)), (F(0), F(1)))
    derivative_second = ((F(1), F(0)), (F(1), F(1)))
    derivative_direct = ordered_derivative_cocycle((derivative_first, derivative_second))
    derivative_wrong = ordered_derivative_cocycle((derivative_second, derivative_first))

    identity = ExactLinearIsomorphism(
        "interaction-native", "interaction-reference", ((F(1), F(0)), (F(0), F(1)))
    )
    retained_projection = ((F(1), F(0)), (F(0), F(0)))
    beta = retained_beta_diagnostics(
        exact_step=((F(1), F(0)), (F(1), F(0))),
        reference_input=(F(2), F(0)),
        source_identification=identity,
        target_identification=identity,
        source_projection=retained_projection,
        target_projection=retained_projection,
        delta_log_scale=F(1),
    )
    nonintertwining = projection_intertwining_residual(
        ExactLinearIsomorphism(
            "projection-native", "projection-reference", ((F(1), F(1)), (F(0), F(1)))
        ),
        retained_projection,
        retained_projection,
    )
    fisher_forms = base_fisher_cocycle_residual_forms(
        fisher_defect=((F(2), F(1)), (F(1), F(3))),
        pushed_fine_jet=(F(1), F(2)),
        horizontal_anomaly=(F(2), F(-1)),
    )

    states = tuple(
        (a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)
    )
    full_action = {
        state: F(state[0] + 2 * state[1] + 3 * state[2] + 5 * np.prod(state))
        for state in states
    }
    interactions = anchored_mobius_decompose(full_action, anchor=(0, 0, 0))
    full_reconstruction = tuple(interactions.reconstruct(state) for state in states)
    pairwise_reconstruction = tuple(
        interactions.reconstruct(state, maximum_order=2) for state in states
    )

    typed_gap = max(
        _maximum_gap(typed_direct[name], typed_staged[name])
        for name in typed_direct
    )
    channel_cocycle_gap = _maximum_gap(
        direct_channel.matrix, _matmul(first.matrix, second.matrix)
    )
    action_gap = max(
        _maximum_gap(direct_action.likelihood, staged_action.likelihood),
        F(0),
    )
    bridge_gap = _maximum_gap(direct_bridge.reverse, staged_reverse)
    beta_form_gap = max(
        _maximum_gap(beta.residual_from_difference, beta.residual_from_identified_projection),
        _maximum_gap(beta.residual_from_difference, beta.residual_from_native_transport),
    )
    fisher_form_gap = max(
        abs(fisher_forms.from_norm_difference - fisher_forms.from_coarse_jet_cross_terms),
        abs(fisher_forms.from_norm_difference - fisher_forms.from_pushed_jet_cross_terms),
    )
    full_residual = interactions.maximum_residual(maximum_order=3)
    pairwise_residual = interactions.maximum_residual(maximum_order=2)
    wrong_order_gap = _maximum_gap(derivative_direct, derivative_wrong)
    tolerance = config.numerics.atol + config.numerics.rtol

    def exact_metric(
        value: Fraction,
        target: Fraction,
        interpretation: str,
        *,
        theorem_status: str = "ESTABLISHED",
        origin: str = "PROJECT_NOVEL",
    ) -> MetricRecord:
        return target_metric(
            float(value),
            tolerance,
            target=float(target),
            interpretation=interpretation,
            theorem_status=theorem_status,  # type: ignore[arg-type]
            verification_state="EVIDENCE_VERIFIED",
            claim_origin=origin,  # type: ignore[arg-type]
        )

    metrics = {
        "direct_staged_pushforward_residual": exact_metric(
            typed_gap,
            F(0),
            "Every declared fixture law has identical direct and staged exact pushforwards.",
            origin="APPLICATION_SPECIFIC",
        ),
        "cocycle_composition_residual": exact_metric(
            channel_cocycle_gap,
            F(0),
            "The right-acting exact channel composite equals the staged matrix product.",
        ),
        "conditional_action_composition_residual": exact_metric(
            action_gap,
            F(0),
            "Direct and staged conditional log-Laplace likelihoods agree exactly.",
        ),
        "posterior_bridge_composition_residual": exact_metric(
            bridge_gap,
            F(0),
            "The direct posterior reverse bridge equals the ordered staged reverse bridge.",
        ),
        "retained_beta_residual": exact_metric(
            max(abs(value) for value in beta.residual_from_difference),
            F(2),
            "The exact signed omitted beta component matches the independent two-coordinate oracle.",
        ),
        "retained_beta_equivalent_forms_residual": exact_metric(
            beta_form_gap,
            F(0),
            "Difference, identified projection, and native transported beta residuals coincide exactly.",
        ),
        "base_fisher_cocycle_forms_residual": exact_metric(
            fisher_form_gap,
            F(0),
            "All three sign-sensitive base Fisher cocycle residual forms coincide exactly.",
        ),
        "full_interaction_reconstruction_residual": exact_metric(
            full_residual,
            F(0),
            "The complete nonempty-subset hierarchy plus the anchor term reconstructs the action.",
        ),
        "wrong_order_negative_control": exact_metric(
            wrong_order_gap,
            F(1),
            "Reversing the noncommuting derivative order gives the pinned exact gap.",
            theorem_status="NUMERICAL",
        ),
        "projection_nonintertwining_control": exact_metric(
            nonintertwining,
            F(1),
            "Holding a retained projection fixed across a nontrivial comparison breaks intertwining.",
            theorem_status="NUMERICAL",
        ),
        "pairwise_truncation_control": exact_metric(
            pairwise_residual,
            F(5),
            "Pairwise truncation omits the pinned three-body interaction generated by exact closure.",
            theorem_status="NUMERICAL",
        ),
    }

    arrays = {
        "channel_fine_to_middle": _float_array(first.matrix),
        "channel_middle_to_macro": _float_array(second.matrix),
        "channel_fine_to_macro": _float_array(direct_channel.matrix),
        "reference_direct": _float_array(typed_direct["reference"]),
        "reference_staged": _float_array(typed_staged["reference"]),
        "evidence_direct": _float_array(typed_direct["evidence"]),
        "evidence_staged": _float_array(typed_staged["evidence"]),
        "posterior_direct": _float_array(typed_direct["posterior"]),
        "posterior_staged": _float_array(typed_staged["posterior"]),
        "recognition_direct": _float_array(typed_direct["recognition"]),
        "recognition_staged": _float_array(typed_staged["recognition"]),
        "action_likelihood_direct": _float_array(direct_action.likelihood),
        "action_likelihood_staged": _float_array(staged_action.likelihood),
        "action_direct": readonly_array(direct_action.action),
        "action_staged": readonly_array(staged_action.action),
        "reverse_bridge_direct": _float_array(direct_bridge.reverse),
        "reverse_bridge_staged": _float_array(staged_reverse),
        "identified_step": _float_array(identified_step),
        "derivative_first": _float_array(derivative_first),
        "derivative_second": _float_array(derivative_second),
        "derivative_cocycle": _float_array(derivative_direct),
        "derivative_wrong_order": _float_array(derivative_wrong),
        "retained_beta_exact": _float_array(beta.exact_beta),
        "retained_beta_retained": _float_array(beta.retained_beta),
        "retained_beta_residual_difference": _float_array(beta.residual_from_difference),
        "retained_beta_residual_identified": _float_array(beta.residual_from_identified_projection),
        "retained_beta_residual_native": _float_array(beta.residual_from_native_transport),
        "base_fisher_residual_forms": _float_array(
            (
                fisher_forms.from_norm_difference,
                fisher_forms.from_coarse_jet_cross_terms,
                fisher_forms.from_pushed_jet_cross_terms,
            )
        ),
        "full_action": _float_array(tuple(full_action[state] for state in states)),
        "full_action_reconstruction": _float_array(full_reconstruction),
        "pairwise_action_reconstruction": _float_array(pairwise_reconstruction),
    }
    return extension, metrics, arrays


def run_scale_cocycle_experiment(
    config: ExperimentConfig,
    *,
    fixture_path: Path | None = None,
) -> ScaleCocycleExperimentResult:
    """Validate, execute, and atomically publish the exact scale laboratory."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    if config.theory.experiment != "scale_cocycle":
        raise ValueError("scale cocycle requires theory.experiment='scale_cocycle'")
    if config.compute.backend != "cpu" or config.compute.dtype != "float64":
        raise ValueError("exact rational scale cocycle requires CPU float64 publication")
    if config.output.render_figures:
        raise ValueError("scale cocycle laboratory exposes no figure renderer")

    repo_root = Path(__file__).resolve().parents[3]
    resolved_fixture = (
        repo_root / "tests" / "fixtures" / "two_scale_application_v1.json"
        if fixture_path is None
        else Path(fixture_path)
    )
    payload = json.loads(resolved_fixture.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("fixture must be a JSON object")
    application_id = validate_two_scale_application_fixture(payload)
    extension, metrics, arrays = _exact_fixtures(config, payload)

    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    provenance = collect_provenance(
        repo_root, repo_root / "Theory", config_hash, streams
    )
    provenance["experiment_scope"] = "exact_finite_three_level_scale_extension"
    provenance["application_id"] = application_id
    provenance["extension_id"] = extension["extension_id"]
    provenance["input_hashes"]["two_scale_fixture_file_sha256"] = hashlib.sha256(  # type: ignore[index]
        resolved_fixture.read_bytes()
    ).hexdigest()
    provenance["exact_arithmetic"] = "fractions.Fraction before NPZ rendering"
    provenance["effective_backend"] = "cpu"
    provenance["effective_dtype"] = "exact_rational_with_float64_rendering"

    store = RunStore.create(config, provenance)
    store.write_json("three_level_extension", extension)
    store.write_json(
        "metrics", {name: asdict(metrics[name]) for name in sorted(metrics)}
    )
    store.write_npz("arrays", arrays)
    store.finalize(
        ("three_level_extension.json", "metrics.json", "arrays.npz")
    )
    status: MetricStatus = (
        "pass" if all(metric.status == "pass" for metric in metrics.values()) else "fail"
    )
    return ScaleCocycleExperimentResult(
        run_dir=store.run_dir,
        config_hash=store.config_hash,
        status=status,
        metrics=MappingProxyType(dict(metrics)),
        arrays=MappingProxyType(dict(arrays)),
    )


__all__ = ["ScaleCocycleExperimentResult", "run_scale_cocycle_experiment"]
