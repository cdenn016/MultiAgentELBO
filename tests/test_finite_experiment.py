from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig, NumericsConfig
from multiagent_elbo.finite.measures import (
    FiniteMeasure,
    MarkovKernel,
    MeasurePair,
    ProbabilityMeasure,
)
from multiagent_elbo.finite.experiment import (
    FiniteExperimentResult,
    run_finite_experiment,
)
from multiagent_elbo.finite.vfe import kl_divergence
from multiagent_elbo.geometry.finite_gauge import (
    FinitePermutation,
    apply_site_relabeling,
)


LABELS = ("00", "01", "10", "11")
NUMERICS = NumericsConfig(
    dtype="float64",
    atol=1e-12,
    rtol=1e-10,
    min_spd_rcond=1e-12,
    max_frame_condition=1.0e6,
)


def gauge_fixture():
    pair = MeasurePair(
        ProbabilityMeasure(LABELS, (0.25, 0.25, 0.25, 0.25), NUMERICS),
        FiniteMeasure(LABELS, (0.2, 0.4, 0.6, 0.8), NUMERICS),
    )
    q = ProbabilityMeasure(LABELS, (0.2, 0.3, 0.1, 0.4), NUMERICS)
    channel = MarkovKernel(
        LABELS,
        ("A", "B"),
        ((1.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, 1.0)),
        NUMERICS,
    )
    first_flip = FinitePermutation(
        ((0, 0, 1, 0), (0, 0, 0, 1), (1, 0, 0, 0), (0, 1, 0, 0))
    )
    target_swap = FinitePermutation(((0, 1), (1, 0)))
    bit_flip = FinitePermutation(((0, 1), (1, 0)))
    identity = FinitePermutation(((1, 0), (0, 1)))
    values = np.array([[-1.0, 1.0], [2.0, -2.0]])
    references = (np.array([0.7, 0.3]), np.array([0.4, 0.6]))
    return (
        q,
        pair,
        channel,
        values,
        references,
        first_flip,
        target_swap,
        (bit_flip, identity),
    )


def test_componentwise_finite_relabeling_preserves_typed_observables_and_intertwines_projection():
    (
        q,
        pair,
        channel,
        values,
        references,
        source_permutation,
        target_permutation,
        axis_permutations,
    ) = gauge_fixture()

    result = apply_site_relabeling(
        q=q,
        pair=pair,
        channel=channel,
        values=values,
        axis_references=references,
        source_permutation=source_permutation,
        target_permutation=target_permutation,
        axis_permutations=axis_permutations,
        retained_interaction_order=1,
    )

    np.testing.assert_allclose(result.recognition.masses, [0.1, 0.4, 0.2, 0.3])
    np.testing.assert_allclose(
        result.recognition.masses @ result.channel.matrix,
        (q.masses @ channel.matrix) @ target_permutation.matrix,
    )
    np.testing.assert_allclose(result.axis_references[0], [0.3, 0.7])
    np.testing.assert_allclose(result.axis_references[1], [0.4, 0.6])
    np.testing.assert_allclose(result.values, [[2.0, -2.0], [-1.0, 1.0]])
    assert result.residuals.evidence == pytest.approx(0.0, abs=1e-12)
    assert result.residuals.kl == pytest.approx(0.0, abs=1e-12)
    assert result.residuals.vfe == pytest.approx(0.0, abs=1e-12)
    assert result.residuals.conditional_kl == pytest.approx(0.0, abs=1e-12)
    assert result.residuals.interaction_reconstruction == pytest.approx(
        0.0, abs=1e-12
    )
    assert result.residuals.retained_projection_intertwining < 1e-12
    assert result.residuals.channel_intertwining < 1e-12
    assert result.scope == "componentwise_finite_borel_relabeling"


def test_relabeling_only_recognition_is_a_detectable_mismatch_control():
    q, pair, *_ = gauge_fixture()
    posterior = pair.posterior()
    mismatched_q = ProbabilityMeasure(LABELS, (0.1, 0.4, 0.2, 0.3), NUMERICS)

    delta = kl_divergence(mismatched_q, posterior) - kl_divergence(q, posterior)

    assert delta == pytest.approx((math.log(2.0) - math.log(3.0)) / 10.0)
    assert delta == pytest.approx(-0.04054651081081644)


def test_permutation_is_exactly_typed_and_read_only():
    permutation = FinitePermutation(((0, 1), (1, 0)))

    assert permutation.size == 2
    assert permutation.old_to_new == (1, 0)
    assert not permutation.matrix.flags.writeable
    with pytest.raises(ValueError):
        permutation.matrix[0, 0] = 1.0


@pytest.mark.parametrize(
    ("matrix", "message"),
    [
        (((1, 0, 0), (0, 1, 0)), "square"),
        (((1, 0), (1, 0)), "one unit entry"),
        (((0.5, 0.5), (0.5, 0.5)), "zero-one"),
        (((1, math.nan), (0, 1)), "finite"),
    ],
)
def test_finite_permutation_rejects_nonpermutations(matrix, message):
    with pytest.raises(ValueError, match=message):
        FinitePermutation(matrix)


def test_apply_site_relabeling_rejects_untyped_or_mismatched_permutations():
    q, pair, channel, values, references, source, target, axes = gauge_fixture()

    with pytest.raises(TypeError, match="FinitePermutation"):
        apply_site_relabeling(
            q=q,
            pair=pair,
            channel=channel,
            values=values,
            axis_references=references,
            source_permutation=np.eye(4),  # type: ignore[arg-type]
            target_permutation=target,
            axis_permutations=axes,
            retained_interaction_order=1,
        )
    with pytest.raises(ValueError, match="source permutation size"):
        apply_site_relabeling(
            q=q,
            pair=pair,
            channel=channel,
            values=values,
            axis_references=references,
            source_permutation=FinitePermutation(((1, 0), (0, 1))),
            target_permutation=target,
            axis_permutations=axes,
            retained_interaction_order=1,
        )
    with pytest.raises(ValueError, match="one axis permutation"):
        apply_site_relabeling(
            q=q,
            pair=pair,
            channel=channel,
            values=values,
            axis_references=references,
            source_permutation=source,
            target_permutation=target,
            axis_permutations=axes[:1],
            retained_interaction_order=1,
        )


def experiment_config(
    root: Path,
    *,
    seed: int = 20260808,
    retained_interaction_order: int | None = 2,
    collect_diagnostics: bool = True,
    render_figures: bool = False,
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "finite exact", "seed": seed},
        {
            "experiment": "finite_exact",
            "retained_interaction_order": retained_interaction_order,
        },
        {
            "dtype": "float64",
            "atol": 1e-10,
            "rtol": 1e-9,
            "min_spd_rcond": 1e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(root),
            "collect_diagnostics": collect_diagnostics,
            "render_figures": render_figures,
        },
    )


def test_finite_experiment_writes_one_complete_exact_run_bundle(tmp_path: Path):
    result = run_finite_experiment(experiment_config(tmp_path))

    assert isinstance(result, FiniteExperimentResult)
    assert result.run_dir.is_dir()
    assert result.status == "pass"
    assert set(path.name for path in result.run_dir.iterdir()) == {
        "arrays.npz",
        "config.json",
        "diagnostics.npz",
        "manifest.json",
        "metrics.json",
    }
    manifest = json.loads((result.run_dir / "manifest.json").read_text("utf-8"))
    assert manifest["complete"] is True
    assert manifest["artifacts"] == {
        "arrays.npz": "complete",
        "config.json": "complete",
        "diagnostics.npz": "complete",
        "manifest.json": "complete",
        "metrics.json": "complete",
    }


@pytest.mark.parametrize("collect_diagnostics", [False, True])
@pytest.mark.parametrize("render_figures", [False, True])
def test_finite_output_toggles_cover_the_reachable_two_by_two_matrix(
    tmp_path: Path, collect_diagnostics: bool, render_figures: bool
):
    result = run_finite_experiment(
        experiment_config(
            tmp_path,
            collect_diagnostics=collect_diagnostics,
            render_figures=render_figures,
        )
    )

    assert (result.run_dir / "metrics.json").is_file()
    assert (result.run_dir / "arrays.npz").is_file()
    assert (result.run_dir / "diagnostics.npz").is_file() is collect_diagnostics
    expected_figure_dir = result.run_dir.parent / "figures" / result.run_dir.name
    assert result.figure_dir == (expected_figure_dir if render_figures else None)
    assert result.figure_status == ("complete" if render_figures else "not_requested")
    assert expected_figure_dir.exists() is render_figures
    if render_figures:
        figure_manifest = json.loads(
            (expected_figure_dir / "figure-manifest.json").read_text("utf-8")
        )
        assert figure_manifest["status"] == "complete"
        assert figure_manifest["requested"] == ["finite_identity"]


def test_collect_diagnostics_alone_adds_declared_finite_intermediate_tensors(
    tmp_path: Path,
):
    result = run_finite_experiment(
        experiment_config(
            tmp_path, collect_diagnostics=True, render_figures=False
        )
    )

    with np.load(result.run_dir / "diagnostics.npz", allow_pickle=False) as archive:
        assert set(archive.files) == {
            "fisher_coarse_probability",
            "fisher_coarse_score",
            "fisher_conditional_covariance",
            "fisher_fine",
            "fisher_joint_mass",
            "gauge_relabelled_channel",
            "gauge_relabelled_q",
            "gauge_relabelled_values",
            "stochastic_fisher_coarse_score",
        }
        assert archive["fisher_joint_mass"].shape == (4, 2)
        assert archive["gauge_relabelled_channel"].shape == (4, 2)


def test_renderer_failure_leaves_numerical_status_and_semantic_bytes_unchanged(
    tmp_path: Path,
):
    baseline = run_finite_experiment(
        experiment_config(
            tmp_path / "baseline",
            collect_diagnostics=False,
            render_figures=False,
        )
    )

    def fail_renderer(run_dir, output_dir, requested):
        raise RuntimeError("injected renderer failure")

    failed_render = run_finite_experiment(
        experiment_config(
            tmp_path / "failed",
            collect_diagnostics=False,
            render_figures=True,
        ),
        renderer=fail_renderer,
    )

    assert baseline.status == failed_render.status == "pass"
    assert (baseline.run_dir / "metrics.json").read_bytes() == (
        failed_render.run_dir / "metrics.json"
    ).read_bytes()
    assert (baseline.run_dir / "arrays.npz").read_bytes() == (
        failed_render.run_dir / "arrays.npz"
    ).read_bytes()
    assert failed_render.figure_status == "failed"
    assert failed_render.figure_dir is not None
    failure = json.loads(
        (failed_render.figure_dir / "figure-manifest.json").read_text("utf-8")
    )
    assert failure["status"] == "failed"
    assert failure["message"] == "injected renderer failure"


def test_secondary_failure_manifest_error_cannot_invalidate_finalized_numerics(
    tmp_path: Path,
):
    def fail_renderer_and_block_failure_manifest(run_dir, output_dir, requested):
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        output_dir.write_text("not a directory", "utf-8")
        raise RuntimeError("injected renderer failure")

    result = run_finite_experiment(
        experiment_config(
            tmp_path,
            collect_diagnostics=False,
            render_figures=True,
        ),
        renderer=fail_renderer_and_block_failure_manifest,
    )

    assert result.status == "pass"
    assert result.figure_status == "failed"
    assert (result.run_dir / "manifest.json").is_file()
    assert json.loads((result.run_dir / "manifest.json").read_text("utf-8"))[
        "complete"
    ] is True
    assert (result.run_dir / "metrics.json").is_file()
    assert (result.run_dir / "arrays.npz").is_file()


def test_finite_metrics_keep_implementation_checks_distinct_from_theorem_status(
    tmp_path: Path,
):
    result = run_finite_experiment(experiment_config(tmp_path))
    metrics = json.loads((result.run_dir / "metrics.json").read_text("utf-8"))

    assert {
        "FIN-01_evidence_residual",
        "FIN-02_vfe_chain_residual",
        "FIN-03_block_update_residual",
        "INF-01_fisher_identity_residual",
        "INF-01_fisher_defect_min_eigenvalue",
        "INT-01_reconstruction_residual",
        "INT-01_theorem_coordinate_g_norm_control",
        "INT-01_quotient_sup_norm_control",
        "INT-01_weighted_l2_diagnostic_control",
        "GAUGE_finite_relabeling_residual",
        "GAUGE_mismatch_kl_delta_control",
    }.issubset(metrics)
    for metric in metrics.values():
        assert {"value", "tolerance", "status", "interpretation"}.issubset(metric)
        assert metric["assessment_scope"] == "implementation_check"
        assert metric["theorem_status"] in {
            "established_conditional_identity",
            "finite_metamorphic_identity",
            "negative_control",
        }
    assert metrics["INT-01_theorem_coordinate_g_norm_control"]["value"] == pytest.approx(
        0.7
    )
    assert metrics["INT-01_quotient_sup_norm_control"]["value"] == pytest.approx(0.7)
    assert metrics["INT-01_weighted_l2_diagnostic_control"]["value"] == pytest.approx(
        0.5
    )
    assert metrics["GAUGE_mismatch_kl_delta_control"]["value"] == pytest.approx(
        -0.04054651081081644
    )


def test_same_seed_semantic_artifacts_are_byte_identical_across_roots(tmp_path: Path):
    first = run_finite_experiment(experiment_config(tmp_path / "first"))
    second = run_finite_experiment(experiment_config(tmp_path / "second"))

    assert (first.run_dir / "metrics.json").read_bytes() == (
        second.run_dir / "metrics.json"
    ).read_bytes()
    assert (first.run_dir / "arrays.npz").read_bytes() == (
        second.run_dir / "arrays.npz"
    ).read_bytes()


def test_finite_experiment_rejects_the_wrong_experiment_before_writing(tmp_path: Path):
    config = ExperimentConfig.from_dicts(
        {"name": "wrong", "seed": 1},
        {"experiment": "gaussian_realization", "retained_interaction_order": 2},
        {
            "dtype": "float64",
            "atol": 1e-10,
            "rtol": 1e-9,
            "min_spd_rcond": 1e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(tmp_path),
            "collect_diagnostics": True,
            "render_figures": False,
        },
    )

    with pytest.raises(ValueError, match="finite_exact"):
        run_finite_experiment(config)
    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_none_retained_order_keeps_full_model_and_still_runs_pairwise_control(
    tmp_path: Path,
):
    result = run_finite_experiment(
        experiment_config(tmp_path, retained_interaction_order=None)
    )

    assert result.status == "pass"
    np.testing.assert_allclose(result.arrays["interaction_omitted_values"], 0.0)
    assert result.metrics[
        "INT-01_theorem_coordinate_g_norm_control"
    ].value == pytest.approx(0.7)
    assert result.metrics["INT-01_quotient_sup_norm_control"].value == pytest.approx(
        0.7
    )
    assert result.metrics[
        "INT-01_weighted_l2_diagnostic_control"
    ].value == pytest.approx(0.5)


def test_retained_order_above_fixture_rank_is_rejected_before_writing(tmp_path: Path):
    config = experiment_config(tmp_path, retained_interaction_order=5)

    with pytest.raises(ValueError, match="maximum_order"):
        run_finite_experiment(config)

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_finalize_failure_leaves_an_incomplete_owned_nonoverwritable_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    config = experiment_config(tmp_path)

    def fail_finalize(self: RunStore, declared_artifacts) -> Path:
        raise OSError("injected finalize failure")

    monkeypatch.setattr(RunStore, "finalize", fail_finalize)
    with pytest.raises(OSError, match="injected finalize failure"):
        run_finite_experiment(config)

    manifests = list(tmp_path.rglob("manifest.json"))
    assert len(manifests) == 1
    run_dir = manifests[0].parent
    manifest = json.loads(manifests[0].read_text("utf-8"))
    assert manifest["complete"] is False
    assert (run_dir / "metrics.json").is_file()
    assert (run_dir / "arrays.npz").is_file()
    with pytest.raises(FileExistsError, match="run path already exists"):
        run_finite_experiment(config)
