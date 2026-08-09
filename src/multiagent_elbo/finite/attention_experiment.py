"""Pre-registered state-conditioned marked-event attention laboratory."""

from __future__ import annotations

from dataclasses import asdict, dataclass
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
from multiagent_elbo.finite.attention import (
    StateConditionedAttentionLaw,
    compose_kernels,
)
from multiagent_elbo.finite.measures import MarkovKernel, ProbabilityMeasure
from multiagent_elbo.geometry.attention_gauge import (
    AttentionCovariantInputs,
    evaluate_attention,
    transform_attention_inputs,
)
from multiagent_elbo.rendering import (
    record_figure_failure_safely,
    validated_renderer_status,
)
from multiagent_elbo.runtime import RngStreams, collect_provenance


MetricStatus = Literal["pass", "fail", "inconclusive"]
FigureRunStatus = Literal["not_requested", "complete", "failed"]


@dataclass(frozen=True)
class AttentionExperimentResult:
    """Typed handle to one finalized attention-experiment run."""

    run_dir: Path
    config_hash: str
    status: MetricStatus
    metrics: Mapping[str, MetricRecord]
    arrays: Mapping[str, np.ndarray]
    figure_status: FigureRunStatus
    figure_dir: Path | None


def _max_abs(*values: np.ndarray) -> float:
    return max(float(np.max(np.abs(value))) for value in values)


def _active_beta_residual(
    first: np.ndarray, second: np.ndarray, active: np.ndarray
) -> float:
    if not np.any(active):
        return 0.0
    return float(np.max(np.abs(first[active] - second[active])))


def _normalization_residual(law: StateConditionedAttentionLaw) -> float:
    disintegration = law.disintegrate()
    state_residual = (
        law.eta_given_state[disintegration.positive_state_mask].sum(axis=(1, 2))
        - 1.0
    )
    alpha_residual = (
        disintegration.alpha_given_state[
            disintegration.positive_state_mask
        ].sum(axis=1)
        - 1.0
    )
    beta_residual = (
        disintegration.beta_given_state[
            disintegration.positive_receiver_mask
        ].sum(axis=1)
        - 1.0
    )
    return _max_abs(state_residual, alpha_residual, beta_residual)


def _wrong_beta_pushforward(
    beta: np.ndarray,
    receiver_partition: np.ndarray,
    source_partition: np.ndarray,
) -> np.ndarray:
    """Deliberately wrong equal-row aggregation used only as a control."""
    aggregated_sources = beta @ source_partition
    receiver_counts = receiver_partition.sum(axis=0)
    return (receiver_partition.T @ aggregated_sources) / receiver_counts[:, None]


def _freeze_arrays(values: Mapping[str, np.ndarray]) -> dict[str, np.ndarray]:
    frozen: dict[str, np.ndarray] = {}
    for name in sorted(values):
        dtype = np.bool_ if np.asarray(values[name]).dtype == np.bool_ else np.float64
        frozen[name] = readonly_array(values[name], dtype=dtype)
    return frozen


def _attention_fixture(
    config: ExperimentConfig,
) -> tuple[
    dict[str, MetricRecord], dict[str, np.ndarray], dict[str, np.ndarray]
]:
    numerics = config.numerics
    tolerance = numerics.atol + numerics.rtol

    fine_probability = ProbabilityMeasure(
        ("y0", "y1", "y2"), (1.0 / 2.0, 1.0 / 3.0, 1.0 / 6.0), numerics
    )
    node_labels = ("n0", "n1", "n2", "n3")
    alpha0 = np.array((1.0 / 20.0, 1.0 / 4.0, 1.0 / 10.0, 3.0 / 5.0))
    beta0 = np.array(
        (
            (1.0 / 2.0, 1.0 / 4.0, 1.0 / 5.0, 1.0 / 20.0),
            (1.0 / 4.0, 1.0 / 5.0, 1.0 / 10.0, 9.0 / 20.0),
            (1.0 / 20.0, 1.0 / 20.0, 1.0 / 20.0, 17.0 / 20.0),
            (1.0 / 5.0, 3.0 / 10.0, 1.0 / 10.0, 2.0 / 5.0),
        )
    )
    eta0 = alpha0[:, None] * beta0
    fine_eta = np.stack((eta0, np.roll(eta0, (1, 1), axis=(0, 1)), eta0.T))
    fine_law = StateConditionedAttentionLaw(
        fine_probability, node_labels, node_labels, fine_eta
    )

    state_01 = MarkovKernel(
        fine_probability.labels,
        ("z0", "z1"),
        ((1.0, 0.0), (1.0, 0.0), (0.0, 1.0)),
        numerics,
    )
    state_12 = MarkovKernel(
        state_01.target_labels,
        ("w0", "w1"),
        ((3.0 / 4.0, 1.0 / 4.0), (1.0 / 4.0, 3.0 / 4.0)),
        numerics,
    )
    state_02 = compose_kernels(state_01, state_12)
    node_01 = MarkovKernel(
        node_labels,
        ("A", "B", "C"),
        ((1.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        numerics,
    )
    node_12 = MarkovKernel(
        node_01.target_labels,
        ("U", "V"),
        ((1.0, 0.0), (1.0, 0.0), (0.0, 1.0)),
        numerics,
    )
    node_02 = compose_kernels(node_01, node_12)

    middle_law = fine_law.pushforward(state_01, node_01, node_01)
    staged_law = middle_law.pushforward(state_12, node_12, node_12)
    direct_law = fine_law.pushforward(state_02, node_02, node_02)
    fine_parts = fine_law.disintegrate()
    middle_parts = middle_law.disintegrate()
    direct_parts = direct_law.disintegrate()
    staged_parts = staged_law.disintegrate()

    expected_eta = np.array(
        (
            ((683.0 / 1600.0, 273.0 / 1600.0), (401.0 / 1600.0, 243.0 / 1600.0)),
            ((281.0 / 800.0, 187.0 / 800.0), (187.0 / 800.0, 145.0 / 800.0)),
        )
    )
    expected_alpha = np.array(
        ((239.0 / 400.0, 161.0 / 400.0), (117.0 / 200.0, 83.0 / 200.0))
    )
    expected_beta = np.array(
        (
            ((683.0 / 956.0, 273.0 / 956.0), (401.0 / 644.0, 243.0 / 644.0)),
            ((281.0 / 468.0, 187.0 / 468.0), (187.0 / 332.0, 145.0 / 332.0)),
        )
    )

    direct_joint = fine_probability.masses[:, None] * state_02.matrix
    reverse_direct = (
        direct_joint.T / direct_law.state_probability.masses[:, None]
    )
    middle_joint = fine_probability.masses[:, None] * state_01.matrix
    reverse_01 = (
        middle_joint.T / middle_law.state_probability.masses[:, None]
    )
    final_joint = middle_law.state_probability.masses[:, None] * state_12.matrix
    reverse_12 = final_joint.T / direct_law.state_probability.masses[:, None]
    reverse_staged = reverse_12 @ reverse_01
    expected_reverse = np.array(
        ((9.0 / 16.0, 3.0 / 8.0, 1.0 / 16.0), (3.0 / 8.0, 1.0 / 4.0, 3.0 / 8.0))
    )

    one_state = ProbabilityMeasure(("base",), (1.0,), numerics)
    identity_state = MarkovKernel(("base",), ("base",), ((1.0,),), numerics)
    base_law = StateConditionedAttentionLaw(
        one_state, node_labels, node_labels, eta0[None, ...]
    )
    correct_base = base_law.pushforward(
        identity_state, node_02, node_02
    ).disintegrate()
    wrong_direct = _wrong_beta_pushforward(beta0, node_02.matrix, node_02.matrix)
    wrong_middle = _wrong_beta_pushforward(beta0, node_01.matrix, node_01.matrix)
    wrong_staged = _wrong_beta_pushforward(
        wrong_middle, node_12.matrix, node_12.matrix
    )

    gauge_inputs = AttentionCovariantInputs(
        ((1.0, 2.0), (-1.0, 1.0)),
        ((2.0, -1.0 / 2.0), (1.0 / 3.0, 2.0)),
        ((1.0, -1.0), (2.0, 1.0 / 2.0)),
        (
            (((1.0, 0.0), (0.0, 1.0)), ((1.0, 1.0 / 2.0), (0.0, 1.0))),
            (((2.0, 0.0), (1.0 / 3.0, 1.0)), ((1.0, 0.0), (-1.0 / 4.0, 3.0 / 2.0))),
        ),
        numerics,
    )
    frames = np.array((((2.0, 1.0 / 2.0), (0.0, 1.0)), ((1.0, 0.0), (1.0 / 3.0, 3.0 / 2.0))))
    gauge_original = evaluate_attention(gauge_inputs)
    transformed_inputs = transform_attention_inputs(gauge_inputs, frames)
    gauge_transformed = evaluate_attention(transformed_inputs)
    expected_occupancy_logits = np.array((1.0, 5.0 / 3.0))
    expected_source_logits = np.array(((5.0 / 2.0, 17.0 / 4.0), (-2.0 / 3.0, 7.0 / 6.0)))
    broken_inputs = AttentionCovariantInputs(
        transformed_inputs.receiver_vectors,
        transformed_inputs.receiver_covectors,
        transformed_inputs.source_vectors,
        gauge_inputs.links,
        numerics,
    )
    gauge_broken = evaluate_attention(broken_inputs)

    permutation = np.roll(np.eye(4), 1, axis=1)
    relabeled_eta = np.stack(
        [permutation.T @ state_eta @ permutation for state_eta in fine_eta]
    )
    relabeled_law = StateConditionedAttentionLaw(
        fine_probability, node_labels, node_labels, relabeled_eta
    )
    relabeled_node_matrix = permutation.T @ node_02.matrix
    relabeled_node = MarkovKernel(
        node_labels, node_02.target_labels, relabeled_node_matrix, numerics
    )
    relabeled_coarse = relabeled_law.pushforward(
        state_02, relabeled_node, relabeled_node
    )
    incoherent_coarse = relabeled_law.pushforward(state_02, node_02, node_02)

    factorization_residual = max(
        _max_abs(
            law.eta_given_state
            - parts.alpha_given_state[..., None] * parts.beta_given_state
        )
        for law, parts in (
            (fine_law, fine_parts),
            (middle_law, middle_parts),
            (direct_law, direct_parts),
            (staged_law, staged_parts),
        )
    )
    normalization_residual = max(
        _normalization_residual(law)
        for law in (fine_law, middle_law, direct_law, staged_law)
    )
    gauge_logits_residual = _max_abs(
        gauge_original.occupancy_logits - gauge_transformed.occupancy_logits,
        gauge_original.source_logits - gauge_transformed.source_logits,
        gauge_original.occupancy_logits - expected_occupancy_logits,
        gauge_original.source_logits - expected_source_logits,
    )

    def identity(value: float, interpretation: str, *, metamorphic: bool = False) -> MetricRecord:
        return target_metric(
            value,
            tolerance,
            target=0.0,
            interpretation=interpretation,
            theorem_status=(
                "finite_metamorphic_identity"
                if metamorphic
                else "established_conditional_identity"
            ),
        )

    def negative_target(value: float, target: float, interpretation: str) -> MetricRecord:
        return target_metric(
            value,
            tolerance,
            target=target,
            interpretation=interpretation,
            theorem_status="negative_control",
        )

    def nonzero_control(value: float, interpretation: str) -> MetricRecord:
        return lower_bounded_metric(
            value,
            tolerance,
            lower_bound=1.0e-3,
            interpretation=interpretation,
            theorem_status="negative_control",
        )

    metrics = {
        "ATT-01_factorization_residual": identity(
            factorization_residual,
            "Marked-event factorization eta=alpha*beta on every active row.",
        ),
        "ATT-01_normalization_residual": identity(
            normalization_residual,
            "State-conditioned marked-event and active conditional laws normalize.",
        ),
        "ATT-02_direct_staged_eta_residual": identity(
            _max_abs(direct_law.eta_given_state - staged_law.eta_given_state),
            "Direct and staged joint marked-event pushforwards agree.",
        ),
        "ATT-02_direct_staged_alpha_residual": identity(
            _max_abs(direct_parts.alpha_given_state - staged_parts.alpha_given_state),
            "Direct and staged receiver occupancies agree.",
        ),
        "ATT-02_direct_staged_active_beta_residual": identity(
            _active_beta_residual(
                direct_parts.beta_given_state,
                staged_parts.beta_given_state,
                direct_parts.positive_receiver_mask,
            ),
            "Direct and staged source conditionals agree only on active receiver rows.",
        ),
        "ATT-02_literal_eta_residual": identity(
            _max_abs(direct_law.eta_given_state - expected_eta),
            "Direct coarse marked-event law agrees with the independent rational oracle.",
        ),
        "ATT-02_literal_alpha_residual": identity(
            _max_abs(direct_parts.alpha_given_state - expected_alpha),
            "Direct coarse receiver occupancy agrees with the rational oracle.",
        ),
        "ATT-02_literal_active_beta_residual": identity(
            _active_beta_residual(
                direct_parts.beta_given_state,
                expected_beta,
                direct_parts.positive_receiver_mask,
            ),
            "Direct coarse active source rows agree with the rational oracle.",
        ),
        "ATT-02_reverse_bridge_residual": identity(
            _max_abs(
                reverse_direct - expected_reverse,
                reverse_staged - expected_reverse,
                reverse_direct - reverse_staged,
            ),
            "Direct and staged posterior state bridges agree with independent joint-mass weights.",
        ),
        "ATT-03_gauge_logits_residual": identity(
            gauge_logits_residual,
            "Occupancy and source contractions are invariant under coherent local GL+(2) frames.",
        ),
        "ATT-03_gauge_alpha_residual": identity(
            _max_abs(gauge_original.alpha - gauge_transformed.alpha),
            "Receiver occupancy is invariant after gauge-covariant recomputation.",
        ),
        "ATT-03_gauge_beta_residual": identity(
            _max_abs(gauge_original.beta - gauge_transformed.beta),
            "Conditional source attention is invariant after gauge-covariant recomputation.",
        ),
        "ATT-03_gauge_eta_residual": identity(
            _max_abs(gauge_original.eta - gauge_transformed.eta),
            "The scalar marked-event law is invariant after gauge-covariant recomputation.",
        ),
        "ATT-03_broken_link_gap_control": nonzero_control(
            _max_abs(gauge_original.eta - gauge_broken.eta),
            "Leaving transport links untransformed detectably breaks the gauge metamorphic.",
        ),
        "ATT-04_relabeling_naturality_residual": identity(
            _max_abs(
                direct_law.eta_given_state - relabeled_coarse.eta_given_state
            ),
            "Coherent cyclic node relabeling intertwines the finite pushforward.",
            metamorphic=True,
        ),
        "ATT-04_incoherent_relabeling_gap_control": nonzero_control(
            _max_abs(direct_law.eta_given_state - incoherent_coarse.eta_given_state),
            "Relabeling eta without its node partitions produces a detectable mismatch.",
        ),
        "ATT-NEG-01_beta_only_associativity_gap": negative_target(
            _max_abs(wrong_direct - wrong_staged),
            1.0 / 10.0,
            "Equal-row beta-only aggregation has the pinned nonassociative gap.",
        ),
        "ATT-NEG-01_beta_only_correct_gap": negative_target(
            _max_abs(wrong_direct - correct_base.beta_given_state[0]),
            1.0 / 20.0,
            "The beta-only direct rule differs from the correct joint-law conditional.",
        ),
    }

    core_arrays = {
        "beta_only_correct_beta": correct_base.beta_given_state[0],
        "beta_only_direct_beta": wrong_direct,
        "beta_only_staged_beta": wrong_staged,
        "direct_coarse_active_receiver_mask": direct_parts.positive_receiver_mask,
        "direct_coarse_alpha": direct_parts.alpha_given_state,
        "direct_coarse_beta": direct_parts.beta_given_state,
        "direct_coarse_eta": direct_law.eta_given_state,
        "direct_coarse_state_probability": direct_law.state_probability.masses,
        "fine_active_receiver_mask": fine_parts.positive_receiver_mask,
        "fine_alpha": fine_parts.alpha_given_state,
        "fine_beta": fine_parts.beta_given_state,
        "fine_eta": fine_law.eta_given_state,
        "fine_state_probability": fine_probability.masses,
        "middle_active_receiver_mask": middle_parts.positive_receiver_mask,
        "middle_alpha": middle_parts.alpha_given_state,
        "middle_beta": middle_parts.beta_given_state,
        "middle_eta": middle_law.eta_given_state,
        "middle_state_probability": middle_law.state_probability.masses,
        "staged_coarse_active_receiver_mask": staged_parts.positive_receiver_mask,
        "staged_coarse_alpha": staged_parts.alpha_given_state,
        "staged_coarse_beta": staged_parts.beta_given_state,
        "staged_coarse_eta": staged_law.eta_given_state,
        "staged_coarse_state_probability": staged_law.state_probability.masses,
    }
    diagnostics = {
        "gauge_broken_eta": gauge_broken.eta,
        "gauge_frames": frames,
        "gauge_links": gauge_inputs.links,
        "gauge_receiver_covectors": gauge_inputs.receiver_covectors,
        "gauge_receiver_vectors": gauge_inputs.receiver_vectors,
        "gauge_source_vectors": gauge_inputs.source_vectors,
        "gauge_transformed_links": transformed_inputs.links,
        "gauge_transformed_receiver_covectors": transformed_inputs.receiver_covectors,
        "gauge_transformed_receiver_vectors": transformed_inputs.receiver_vectors,
        "gauge_transformed_source_vectors": transformed_inputs.source_vectors,
        "incoherent_coarse_eta": incoherent_coarse.eta_given_state,
        "relabeling_eta": relabeled_eta,
        "relabeling_permutation": permutation,
        "relabeling_receiver_partition": relabeled_node.matrix,
        "relabeling_source_partition": relabeled_node.matrix,
        "receiver_partition_direct": node_02.matrix,
        "receiver_partition_fine_to_middle": node_01.matrix,
        "receiver_partition_middle_to_coarse": node_12.matrix,
        "reverse_bridge_direct": reverse_direct,
        "reverse_bridge_expected": expected_reverse,
        "reverse_bridge_staged": reverse_staged,
        "source_partition_direct": node_02.matrix,
        "source_partition_fine_to_middle": node_01.matrix,
        "source_partition_middle_to_coarse": node_12.matrix,
        "state_channel_direct": state_02.matrix,
        "state_channel_fine_to_middle": state_01.matrix,
        "state_channel_middle_to_coarse": state_12.matrix,
    }
    return metrics, core_arrays, diagnostics


def run_attention_experiment(
    config: ExperimentConfig,
    *,
    renderer: Callable[..., object] | None = None,
) -> AttentionExperimentResult:
    """Run and finalize the preregistered marked-event attention fixture."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    if config.theory.experiment != "attention_marked_event":
        raise ValueError(
            "attention experiment requires theory.experiment='attention_marked_event'"
        )

    metrics, raw_arrays, raw_diagnostics = _attention_fixture(config)
    arrays = _freeze_arrays(raw_arrays)
    diagnostics = _freeze_arrays(raw_diagnostics)
    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    repo_root = Path(__file__).resolve().parents[3]
    provenance = collect_provenance(
        repo_root, repo_root / "Theory", config_hash, streams
    )
    provenance["experiment_scope"] = (
        "pre_registered_state_conditioned_marked_event_fixture"
    )
    provenance["metamorphic_scope"] = "scalar_gauge_plus_finite_relabeling"
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
    numerical_status: MetricStatus = (
        "pass" if all(metric.status == "pass" for metric in metrics.values()) else "fail"
    )

    figure_status: FigureRunStatus = "not_requested"
    figure_dir: Path | None = None
    if config.output.render_figures:
        figure_dir = store.run_dir.parent / "figures" / store.run_dir.name
        requested = ("attention_composition",)
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
    return AttentionExperimentResult(
        run_dir=store.run_dir,
        config_hash=store.config_hash,
        status=numerical_status,
        metrics=MappingProxyType(dict(metrics)),
        arrays=MappingProxyType(arrays),
        figure_status=figure_status,
        figure_dir=figure_dir,
    )


__all__ = ["AttentionExperimentResult", "run_attention_experiment"]
