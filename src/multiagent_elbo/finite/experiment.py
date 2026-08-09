"""Pre-registered exact finite experiment and immutable artifact publication."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from pathlib import Path
from types import MappingProxyType
from typing import Literal, Mapping

import numpy as np

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.geometry.finite_gauge import (
    FinitePermutation,
    apply_site_relabeling,
)
from multiagent_elbo.runtime import RngStreams, collect_provenance

from .fisher import fisher_channel_decomposition
from .interactions import hoeffding_decompose, retain_interaction_order
from .measures import FiniteMeasure, MarkovKernel, MeasurePair, ProbabilityMeasure
from .vfe import block_update_decomposition, kl_divergence, vfe_channel_decomposition


MetricStatus = Literal["pass", "fail", "inconclusive"]
TheoremStatus = Literal[
    "established_conditional_identity",
    "finite_metamorphic_identity",
    "negative_control",
]


@dataclass(frozen=True)
class MetricRecord:
    """One implementation check, kept distinct from its theorem status."""

    value: float
    tolerance: float
    status: MetricStatus
    interpretation: str
    assessment_scope: Literal["implementation_check"]
    theorem_status: TheoremStatus


@dataclass(frozen=True)
class FiniteExperimentResult:
    """Typed handle to one finalized finite-experiment run."""

    run_dir: Path
    config_hash: str
    status: MetricStatus
    metrics: Mapping[str, MetricRecord]
    arrays: Mapping[str, np.ndarray]


def _readonly(values: object) -> np.ndarray:
    result = np.array(values, dtype=np.float64, copy=True, order="C")
    result.setflags(write=False)
    return result


def _metric(
    value: float,
    tolerance: float,
    *,
    target: float,
    interpretation: str,
    theorem_status: TheoremStatus,
) -> MetricRecord:
    return MetricRecord(
        value=float(value),
        tolerance=float(tolerance),
        status="pass" if abs(value - target) <= tolerance else "fail",
        interpretation=interpretation,
        assessment_scope="implementation_check",
        theorem_status=theorem_status,
    )


def _lower_bounded_metric(
    value: float,
    tolerance: float,
    *,
    lower_bound: float,
    interpretation: str,
    theorem_status: TheoremStatus,
) -> MetricRecord:
    return MetricRecord(
        value=float(value),
        tolerance=float(tolerance),
        status="pass" if value >= lower_bound - tolerance else "fail",
        interpretation=interpretation,
        assessment_scope="implementation_check",
        theorem_status=theorem_status,
    )


def _finite_fixtures(config: ExperimentConfig):
    numerics = config.numerics
    tolerance = numerics.atol + numerics.rtol
    labels = ("00", "01", "10", "11")
    pair = MeasurePair(
        ProbabilityMeasure(labels, (0.25,) * 4, numerics),
        FiniteMeasure(labels, (0.2, 0.4, 0.6, 0.8), numerics),
    )
    recognition = ProbabilityMeasure(labels, (0.2, 0.3, 0.1, 0.4), numerics)
    channel = MarkovKernel(
        labels,
        ("A", "B"),
        ((1.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, 1.0)),
        numerics,
    )

    pushed_pair = pair.pushforward(channel)
    vfe = vfe_channel_decomposition(recognition, pair, channel)
    block = block_update_decomposition(
        np.array([[0.10, 0.20], [0.30, 0.40]]),
        np.array([[0.21, 0.13], [0.14, 0.52]]),
        np.array([[0.14, 0.325], [0.21, 0.325]]),
        block_axes=(0,),
    )
    fisher = fisher_channel_decomposition(
        pair.reference, (-1.5, -0.5, 0.5, 1.5), channel
    )
    stochastic_probability = ProbabilityMeasure(
        ("x0", "x1", "x2"), (0.5, 1.0 / 3.0, 1.0 / 6.0), numerics
    )
    stochastic_channel = MarkovKernel(
        stochastic_probability.labels,
        ("z0", "z1"),
        ((1.0, 0.0), (0.5, 0.5), (0.0, 1.0)),
        numerics,
    )
    stochastic_fisher = fisher_channel_decomposition(
        stochastic_probability, (-1.0, 1.0, 1.0), stochastic_channel
    )
    singular_fisher = fisher_channel_decomposition(
        pair.reference,
        np.array([[-1.5, -1.0], [-0.5, 1.0], [0.5, -1.0], [1.5, 1.0]]),
        channel,
    )

    spins = np.array([-1.0, 1.0])
    x1, x2, x3, x4 = np.meshgrid(spins, spins, spins, spins, indexing="ij")
    interaction_values = 0.3 * x1 * x2 * x3 + 0.4 * x1 * x2 * x4
    interaction = hoeffding_decompose(
        interaction_values, (np.array([0.5, 0.5]),) * 4
    )
    retained_order = config.theory.retained_interaction_order
    if retained_order is None:
        retained_order = interaction_values.ndim
    interaction_projection = retain_interaction_order(interaction, retained_order)
    pairwise_control = retain_interaction_order(interaction, 2)

    first_flip = FinitePermutation(
        ((0, 0, 1, 0), (0, 0, 0, 1), (1, 0, 0, 0), (0, 1, 0, 0))
    )
    target_swap = FinitePermutation(((0, 1), (1, 0)))
    bit_flip = FinitePermutation(((0, 1), (1, 0)))
    identity = FinitePermutation(((1, 0), (0, 1)))
    gauge = apply_site_relabeling(
        q=recognition,
        pair=pair,
        channel=channel,
        values=np.array([[-1.0, 1.0], [2.0, -2.0]]),
        axis_references=(np.array([0.7, 0.3]), np.array([0.4, 0.6])),
        source_permutation=first_flip,
        target_permutation=target_swap,
        axis_permutations=(bit_flip, identity),
        retained_interaction_order=1,
    )
    mismatch = ProbabilityMeasure(labels, (0.1, 0.4, 0.2, 0.3), numerics)
    mismatch_delta = kl_divergence(mismatch, pair.posterior()) - kl_divergence(
        recognition, pair.posterior()
    )
    gauge_residual = max(
        abs(value) for value in asdict(gauge.residuals).values()
    )

    metrics = {
        "FIN-01_evidence_residual": _metric(
            pushed_pair.evidence - pair.evidence,
            tolerance,
            target=0.0,
            interpretation="Implementation check of common-channel evidence preservation.",
            theorem_status="established_conditional_identity",
        ),
        "FIN-02_vfe_chain_residual": _metric(
            float(vfe.residual),
            tolerance,
            target=0.0,
            interpretation="Implementation check of the finite VFE chain rule on its finite branch.",
            theorem_status="established_conditional_identity",
        ),
        "FIN-03_block_update_residual": _metric(
            float(block.residual),
            tolerance,
            target=0.0,
            interpretation="Implementation check of the fixed-outside local/collective VFE identity.",
            theorem_status="established_conditional_identity",
        ),
        "INF-01_fisher_identity_residual": _metric(
            float(np.max(np.abs(fisher.residual))),
            tolerance,
            target=0.0,
            interpretation="Finite centered-score implementation check; it does not establish DQM.",
            theorem_status="established_conditional_identity",
        ),
        "INF-01_fisher_defect_min_eigenvalue": _lower_bounded_metric(
            singular_fisher.minimum_defect_eigenvalue,
            singular_fisher.defect_psd_tolerance,
            lower_bound=0.0,
            interpretation="Raw singular-PSD defect diagnostic without clipping, jitter, or PD assumptions.",
            theorem_status="established_conditional_identity",
        ),
        "INF-01_stochastic_weighting_control": _metric(
            float(np.max(np.abs(stochastic_fisher.coarse_score[:, 0] - [-0.5, 1.0]))),
            tolerance,
            target=0.0,
            interpretation="Nonuniform stochastic-channel control for joint-mass weighting.",
            theorem_status="negative_control",
        ),
        "INT-01_reconstruction_residual": _metric(
            interaction.reconstruction_residual_sup,
            tolerance,
            target=0.0,
            interpretation="Implementation check of complete product-reference interaction reconstruction.",
            theorem_status="established_conditional_identity",
        ),
        "INT-01_theorem_coordinate_g_norm_control": _metric(
            pairwise_control.theorem_coordinate_g_norm,
            tolerance,
            target=0.7,
            interpretation="Retained-pairwise omission in theorem-coordinate G norm.",
            theorem_status="negative_control",
        ),
        "INT-01_quotient_sup_norm_control": _metric(
            pairwise_control.quotient_sup_norm,
            tolerance,
            target=0.7,
            interpretation="Action residual modulo constants in quotient sup norm; not the G norm.",
            theorem_status="negative_control",
        ),
        "INT-01_weighted_l2_diagnostic_control": _metric(
            pairwise_control.weighted_l2_diagnostic,
            tolerance,
            target=0.5,
            interpretation="Product-reference weighted L2 diagnostic; not a theorem-coordinate norm.",
            theorem_status="negative_control",
        ),
        "GAUGE_finite_relabeling_residual": _metric(
            gauge_residual,
            tolerance,
            target=0.0,
            interpretation="Coherent componentwise finite Borel relabeling metamorphic; no holonomy claim.",
            theorem_status="finite_metamorphic_identity",
        ),
        "GAUGE_mismatch_kl_delta_control": _metric(
            mismatch_delta,
            tolerance,
            target=(math.log(2.0) - math.log(3.0)) / 10.0,
            interpretation="Pinned mismatch from relabeling recognition alone.",
            theorem_status="negative_control",
        ),
    }
    arrays = {
        "fisher_coarse_probability": fisher.coarse_probability,
        "fisher_coarse_score": fisher.coarse_score,
        "fisher_conditional_covariance": fisher.conditional_covariance,
        "fisher_fine": fisher.fine_fisher,
        "fisher_joint_mass": fisher.joint_mass,
        "fisher_residual": fisher.residual,
        "gauge_relabelled_channel": gauge.channel.matrix,
        "gauge_relabelled_q": gauge.recognition.masses,
        "gauge_relabelled_values": gauge.values,
        "interaction_omitted_values": interaction_projection.omitted_values,
        "interaction_reconstruction": interaction.reconstruction,
        "interaction_values": interaction.values,
        "singular_fisher_defect": singular_fisher.conditional_covariance,
        "stochastic_fisher_coarse_score": stochastic_fisher.coarse_score,
    }
    return metrics, arrays


def run_finite_experiment(config: ExperimentConfig) -> FiniteExperimentResult:
    """Run the fixed finite laboratory and atomically finalize its exact inventory."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    if config.theory.experiment != "finite_exact":
        raise ValueError("finite experiment requires theory.experiment='finite_exact'")

    metrics, raw_arrays = _finite_fixtures(config)
    arrays = {
        name: _readonly(raw_arrays[name]) for name in sorted(raw_arrays)
    }
    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    repo_root = Path(__file__).resolve().parents[3]
    provenance = collect_provenance(
        repo_root, repo_root / "Theory", config_hash, streams
    )
    provenance["experiment_scope"] = "pre_registered_exact_finite_fixtures"
    store = RunStore.create(config, provenance)
    store.write_json(
        "metrics",
        {name: asdict(metrics[name]) for name in sorted(metrics)},
    )
    store.write_npz("arrays", arrays)
    store.finalize(("metrics.json", "arrays.npz"))
    status: MetricStatus = (
        "pass" if all(metric.status == "pass" for metric in metrics.values()) else "fail"
    )
    return FiniteExperimentResult(
        run_dir=store.run_dir,
        config_hash=store.config_hash,
        status=status,
        metrics=MappingProxyType(dict(metrics)),
        arrays=MappingProxyType(arrays),
    )
