from __future__ import annotations

from dataclasses import replace
import math
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.finite.categorical_dqm_experiment import (
    CategoricalDqmExperimentResult,
    run_categorical_dqm_experiment,
)
from multiagent_elbo.finite.categorical_dqm import DqmRemainderLadder


GENERIC_METRIC_KEYS = {
    "DQM-01_normalization_residual",
    "DQM-01_score_centering_residual",
    "DQM-01_finite_difference_score_residual",
    "DQM-01_two_sided_remainder_final",
    "INF-02_conditional_score_fd_residual",
    "INF-02_fisher_identity_residual",
    "INF-02_fisher_defect_min_eigenvalue",
    "INF-02_positive_loss_trace_control",
}

DEFAULT_ONLY_METRIC_KEYS = {
    "DQM-01_literal_probability_residual",
    "DQM-01_literal_score_residual",
    "DQM-01_positive_remainder_ladder_monotonicity",
    "DQM-01_negative_remainder_ladder_monotonicity",
    "INF-02_literal_coarse_probability_residual",
    "INF-02_literal_conditional_score_residual",
    "INF-02_literal_fine_fisher_residual",
    "INF-02_literal_coarse_fisher_residual",
    "INF-02_literal_fisher_defect_residual",
}

PINNED_DEFAULT_METRIC_KEYS = {"INF-NEG-01_wrong_weight_gap"}
CUSTOM_DIAGNOSTIC_METRIC_KEYS = {"INF-NEG-01_wrong_weight_gap_diagnostic"}

CORE_ARRAY_KEYS = {
    "analytic_coarse_score",
    "analytic_fine_score",
    "channel",
    "coarse_fisher",
    "coarse_probability",
    "direction",
    "dqm_remainder_negative",
    "dqm_remainder_positive",
    "dqm_step_sizes",
    "fine_fisher",
    "fine_probability",
    "finite_difference_coarse_score",
    "finite_difference_fine_score",
    "fisher_defect",
    "fisher_identity_residual",
    "theta",
    "wrong_weight_gap",
}

DIAGNOSTIC_ARRAY_KEYS = {
    "conditional_covariance_contributions",
    "joint_mass",
    "wrong_score",
    "wrong_score_error",
}


def categorical_dqm_config(
    root: Path,
    *,
    theta: tuple[float, float] = (math.log(2.0), math.log(3.0)),
    finite_difference_step: float = 1.0e-5,
    dqm_step_sizes: tuple[float, ...] = (0.1, 0.05, 0.025, 0.0125),
    seed: int = 20260809,
    collect_diagnostics: bool = False,
    render_figures: bool = False,
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "categorical_dqm", "seed": seed},
        {
            "experiment": "categorical_dqm",
            "fixture": "three_category_softmax_v1",
            "theta": theta,
            "finite_difference_step": finite_difference_step,
            "dqm_step_sizes": dqm_step_sizes,
        },
        {
            "dtype": "float64",
            "atol": 1.0e-12,
            "rtol": 1.0e-10,
            "min_spd_rcond": 1.0e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(root),
            "collect_diagnostics": collect_diagnostics,
            "render_figures": render_figures,
        },
    )


def test_categorical_dqm_runner_rejects_wrong_experiment_before_runtime_seams(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.finite.categorical_dqm_experiment as experiment

    def forbidden(*_args, **_kwargs):
        raise AssertionError("runtime seam executed before experiment validation")

    monkeypatch.setattr(experiment.RngStreams, "from_seed", forbidden)
    monkeypatch.setattr(experiment, "collect_provenance", forbidden)
    monkeypatch.setattr(experiment.RunStore, "create", forbidden)
    wrong = ExperimentConfig.from_dicts(
        {"name": "wrong", "seed": 1},
        {"experiment": "finite_exact", "retained_interaction_order": 2},
        {
            "dtype": "float64",
            "atol": 1.0e-12,
            "rtol": 1.0e-10,
            "min_spd_rcond": 1.0e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(tmp_path),
            "collect_diagnostics": False,
            "render_figures": False,
        },
    )

    with pytest.raises(ValueError, match="categorical_dqm"):
        run_categorical_dqm_experiment(wrong)

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_default_categorical_dqm_run_emits_generic_and_literal_oracle_metrics(
    tmp_path: Path,
):
    config = categorical_dqm_config(tmp_path)

    result = run_categorical_dqm_experiment(config)

    assert isinstance(result, CategoricalDqmExperimentResult)
    assert result.status == "pass"
    assert set(result.metrics) == (
        GENERIC_METRIC_KEYS
        | DEFAULT_ONLY_METRIC_KEYS
        | PINNED_DEFAULT_METRIC_KEYS
    )
    assert result.channel_scope == "declared_fixed_parameter_independent"
    tolerance = config.numerics.atol + config.numerics.rtol
    literal_residual_keys = {
        key for key in DEFAULT_ONLY_METRIC_KEYS if key.endswith("_residual")
    }
    for key in literal_residual_keys:
        metric = result.metrics[key]
        assert metric.status == "pass"
        assert abs(metric.value) <= tolerance
        assert metric.assessment_scope == "implementation_check"
    for key in GENERIC_METRIC_KEYS - {
        "DQM-01_two_sided_remainder_final",
        "INF-02_fisher_defect_min_eigenvalue",
        "INF-02_positive_loss_trace_control",
    }:
        assert result.metrics[key].status == "pass"
        assert abs(result.metrics[key].value) <= tolerance
    assert result.metrics[
        "INF-NEG-01_wrong_weight_gap"
    ].value == pytest.approx(4.0 / 21.0, abs=tolerance)
    assert all(metric.status == "pass" for metric in result.metrics.values())


def test_default_arrays_match_independent_rational_probability_score_and_fisher_oracles(
    tmp_path: Path,
):
    result = run_categorical_dqm_experiment(categorical_dqm_config(tmp_path))

    expected_fine_probability = np.array([1.0 / 3.0, 1.0 / 2.0, 1.0 / 6.0])
    expected_fine_score = np.array(
        [
            [2.0 / 3.0, -1.0 / 2.0],
            [-1.0 / 3.0, 1.0 / 2.0],
            [-1.0 / 3.0, -1.0 / 2.0],
        ]
    )
    expected_coarse_probability = np.array([5.0 / 12.0, 7.0 / 12.0])
    expected_coarse_score = np.array(
        [[7.0 / 15.0, -1.0 / 2.0], [-1.0 / 3.0, 5.0 / 14.0]]
    )
    expected_fine_fisher = np.array(
        [[2.0 / 9.0, -1.0 / 6.0], [-1.0 / 6.0, 1.0 / 4.0]]
    )
    expected_coarse_fisher = np.array(
        [[7.0 / 45.0, -1.0 / 6.0], [-1.0 / 6.0, 5.0 / 28.0]]
    )
    expected_defect = np.array([[1.0 / 15.0, 0.0], [0.0, 1.0 / 14.0]])

    np.testing.assert_allclose(
        result.arrays["fine_probability"],
        expected_fine_probability,
        rtol=0.0,
        atol=1.0e-15,
    )
    np.testing.assert_allclose(
        result.arrays["analytic_fine_score"],
        expected_fine_score,
        rtol=0.0,
        atol=1.0e-15,
    )
    np.testing.assert_allclose(
        result.arrays["finite_difference_fine_score"],
        expected_fine_score,
        rtol=0.0,
        atol=1.0e-8,
    )
    np.testing.assert_allclose(
        result.arrays["coarse_probability"],
        expected_coarse_probability,
        rtol=0.0,
        atol=1.0e-15,
    )
    np.testing.assert_allclose(
        result.arrays["analytic_coarse_score"],
        expected_coarse_score,
        rtol=0.0,
        atol=1.0e-15,
    )
    np.testing.assert_allclose(
        result.arrays["finite_difference_coarse_score"],
        expected_coarse_score,
        rtol=0.0,
        atol=1.0e-8,
    )
    np.testing.assert_allclose(
        result.arrays["fine_fisher"],
        expected_fine_fisher,
        rtol=0.0,
        atol=1.0e-15,
    )
    np.testing.assert_allclose(
        result.arrays["coarse_fisher"],
        expected_coarse_fisher,
        rtol=0.0,
        atol=1.0e-15,
    )
    np.testing.assert_allclose(
        result.arrays["fisher_defect"],
        expected_defect,
        rtol=0.0,
        atol=1.0e-15,
    )


def test_default_theta_with_edited_ladder_has_no_default_only_or_pinned_metrics(
    tmp_path: Path,
):
    result = run_categorical_dqm_experiment(
        categorical_dqm_config(
            tmp_path,
            dqm_step_sizes=(0.08, 0.04, 0.02, 0.01),
        )
    )

    assert result.status == "pass"
    assert set(result.metrics) == GENERIC_METRIC_KEYS | CUSTOM_DIAGNOSTIC_METRIC_KEYS
    assert DEFAULT_ONLY_METRIC_KEYS.isdisjoint(result.metrics)
    assert PINNED_DEFAULT_METRIC_KEYS.isdisjoint(result.metrics)
    assert result.metrics["INF-NEG-01_wrong_weight_gap_diagnostic"].value == (
        pytest.approx(4.0 / 21.0)
    )


def test_custom_theta_keeps_generic_checks_without_default_literal_or_pinned_metrics(
    tmp_path: Path,
):
    result = run_categorical_dqm_experiment(
        categorical_dqm_config(tmp_path, theta=(-0.75, 1.25))
    )

    assert result.status == "pass"
    assert set(result.metrics) == GENERIC_METRIC_KEYS | CUSTOM_DIAGNOSTIC_METRIC_KEYS
    assert DEFAULT_ONLY_METRIC_KEYS.isdisjoint(result.metrics)
    assert PINNED_DEFAULT_METRIC_KEYS.isdisjoint(result.metrics)
    diagnostic = result.metrics["INF-NEG-01_wrong_weight_gap_diagnostic"]
    assert diagnostic.status == "inconclusive"
    assert diagnostic.value == pytest.approx(float(result.arrays["wrong_weight_gap"]))
    assert np.isfinite(diagnostic.value)
    np.testing.assert_allclose(result.arrays["theta"], [-0.75, 1.25])
    assert result.arrays["dqm_step_sizes"].shape == (4,)
    assert result.arrays["dqm_remainder_positive"].shape == (4,)
    assert result.arrays["dqm_remainder_negative"].shape == (4,)


def _analysis_with(
    analysis: object,
    *,
    fisher_channel_result: object | None = None,
    remainder_ladder: object | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        base_probability=analysis.base_probability,
        analytic_fine_score=analysis.analytic_fine_score,
        finite_difference_fine_score=analysis.finite_difference_fine_score,
        finite_difference_pushed_score=analysis.finite_difference_pushed_score,
        fisher_channel_result=(
            analysis.fisher_channel_result
            if fisher_channel_result is None
            else fisher_channel_result
        ),
        remainder_ladder=(
            analysis.remainder_ladder
            if remainder_ladder is None
            else remainder_ladder
        ),
        family_scope=analysis.family_scope,
        channel_scope=analysis.channel_scope,
    )


def test_zero_fisher_loss_trace_fails_the_control_and_aggregate_status(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.finite.categorical_dqm_experiment as experiment

    real_analyze = experiment.analyze_categorical_dqm

    def zero_loss_analysis(*args, **kwargs):
        analysis = real_analyze(*args, **kwargs)
        fisher = analysis.fisher_channel_result
        zeros = np.zeros_like(fisher.conditional_covariance)
        zero_loss_fisher = replace(
            fisher,
            fine_fisher=fisher.coarse_fisher,
            conditional_covariance=zeros,
            residual=zeros,
            minimum_defect_eigenvalue=0.0,
            defect_is_psd=True,
        )
        return _analysis_with(analysis, fisher_channel_result=zero_loss_fisher)

    monkeypatch.setattr(experiment, "analyze_categorical_dqm", zero_loss_analysis)

    result = run_categorical_dqm_experiment(
        categorical_dqm_config(tmp_path, theta=(-0.75, 1.25))
    )

    control = result.metrics["INF-02_positive_loss_trace_control"]
    assert control.value == 0.0
    assert control.status == "fail"
    assert result.status == "fail"


def test_flat_remainder_ladders_fail_both_strict_monotonicity_controls(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.finite.categorical_dqm_experiment as experiment

    real_analyze = experiment.analyze_categorical_dqm

    def flat_ladder_analysis(*args, **kwargs):
        analysis = real_analyze(*args, **kwargs)
        steps = analysis.remainder_ladder.step_sizes
        flat = DqmRemainderLadder(
            steps,
            np.full_like(steps, 1.0e-3),
            np.full_like(steps, 1.0e-3),
        )
        return _analysis_with(analysis, remainder_ladder=flat)

    monkeypatch.setattr(experiment, "analyze_categorical_dqm", flat_ladder_analysis)

    result = run_categorical_dqm_experiment(categorical_dqm_config(tmp_path))

    positive = result.metrics["DQM-01_positive_remainder_ladder_monotonicity"]
    negative = result.metrics["DQM-01_negative_remainder_ladder_monotonicity"]
    assert positive.status == "fail"
    assert negative.status == "fail"
    assert result.status == "fail"


def _write_figure_manifest(
    run_dir: Path,
    output_dir: Path,
    requested: tuple[str, ...],
    *,
    status: str = "complete",
) -> SimpleNamespace:
    output_dir.mkdir(parents=True, exist_ok=True)
    figures: list[dict[str, str]] = []
    message: str | None = None
    manifest_name = "figure-manifest.json"
    if status == "complete":
        png = output_dir / "categorical-dqm.png"
        pdf = output_dir / "categorical-dqm.pdf"
        png.write_bytes(b"\x89PNG\r\n\x1a\ncategorical dqm")
        pdf.write_bytes(b"%PDF-1.7\ncategorical dqm")
        figures.append(
            {
                "name": "categorical_dqm",
                "png": png.name,
                "png_sha256": hashlib.sha256(png.read_bytes()).hexdigest(),
                "pdf": pdf.name,
                "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            }
        )
    else:
        message = "backed renderer failure"
        manifest_name = "figure-failure.json"
    manifest_path = output_dir / manifest_name
    manifest_path.write_text(
        json.dumps(
            {
                "figures": figures,
                "message": message,
                "requested": list(requested),
                "run_dir": str(run_dir.resolve()),
                "status": status,
            }
        ),
        encoding="utf-8",
    )
    return SimpleNamespace(
        status=status,
        run_dir=run_dir,
        output_dir=output_dir,
        requested=requested,
        manifest_path=manifest_path,
    )


@pytest.mark.parametrize("collect_diagnostics", [False, True])
@pytest.mark.parametrize("render_figures", [False, True])
def test_output_toggles_preserve_exact_finalized_numerical_inventories(
    tmp_path: Path, collect_diagnostics: bool, render_figures: bool
):
    renderer_calls = 0

    def renderer(
        run_dir: Path, output_dir: Path, *, requested: tuple[str, ...]
    ) -> object:
        nonlocal renderer_calls
        renderer_calls += 1
        manifest = json.loads((run_dir / "manifest.json").read_text("utf-8"))
        assert manifest["complete"] is True
        assert requested == ("categorical_dqm",)
        return _write_figure_manifest(run_dir, output_dir, requested)

    result = run_categorical_dqm_experiment(
        categorical_dqm_config(
            tmp_path,
            collect_diagnostics=collect_diagnostics,
            render_figures=render_figures,
        ),
        renderer=renderer,
    )

    expected_run_files = {
        "arrays.npz",
        "config.json",
        "manifest.json",
        "metrics.json",
    }
    if collect_diagnostics:
        expected_run_files.add("diagnostics.npz")
    assert {path.name for path in result.run_dir.iterdir()} == expected_run_files
    manifest = json.loads((result.run_dir / "manifest.json").read_text("utf-8"))
    assert manifest["complete"] is True
    assert manifest["artifacts"] == {
        name: "complete" for name in sorted(expected_run_files)
    }
    assert manifest["provenance"]["channel_scope"] == (
        "declared_fixed_parameter_independent"
    )
    assert result.channel_scope == "declared_fixed_parameter_independent"
    with np.load(result.run_dir / "arrays.npz", allow_pickle=False) as archive:
        assert archive.files == sorted(CORE_ARRAY_KEYS)
        assert set(archive.files) == CORE_ARRAY_KEYS
        assert "channel_scope" not in archive.files
        assert all(np.issubdtype(archive[name].dtype, np.number) for name in archive.files)
    diagnostics_path = result.run_dir / "diagnostics.npz"
    assert diagnostics_path.is_file() is collect_diagnostics
    if collect_diagnostics:
        with np.load(diagnostics_path, allow_pickle=False) as archive:
            assert archive.files == sorted(DIAGNOSTIC_ARRAY_KEYS)
            assert set(archive.files) == DIAGNOSTIC_ARRAY_KEYS
    assert DIAGNOSTIC_ARRAY_KEYS.isdisjoint(result.arrays)
    expected_figure_dir = result.run_dir.parent / "figures" / result.run_dir.name
    assert renderer_calls == int(render_figures)
    assert result.figure_status == (
        "complete" if render_figures else "not_requested"
    )
    assert result.figure_dir == (expected_figure_dir if render_figures else None)


def test_semantic_artifacts_are_root_independent_and_result_arrays_are_immutable(
    tmp_path: Path,
):
    first = run_categorical_dqm_experiment(
        categorical_dqm_config(tmp_path / "first")
    )
    second = run_categorical_dqm_experiment(
        categorical_dqm_config(tmp_path / "second")
    )

    assert first.config_hash != second.config_hash
    assert (first.run_dir / "metrics.json").read_bytes() == (
        second.run_dir / "metrics.json"
    ).read_bytes()
    assert (first.run_dir / "arrays.npz").read_bytes() == (
        second.run_dir / "arrays.npz"
    ).read_bytes()
    with pytest.raises(TypeError):
        first.metrics["new"] = first.metrics["DQM-01_normalization_residual"]  # type: ignore[index]
    with pytest.raises(TypeError):
        first.arrays["new"] = np.zeros(1)  # type: ignore[index]
    assert all(not array.flags.writeable for array in first.arrays.values())
    with pytest.raises(ValueError):
        first.arrays["theta"][0] = 0.0


def test_invalid_perturbation_fails_before_rng_or_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.finite.categorical_dqm_experiment as experiment

    def forbidden(*_args, **_kwargs):
        raise AssertionError("runtime seam executed before perturbation validation")

    monkeypatch.setattr(experiment.RngStreams, "from_seed", forbidden)
    monkeypatch.setattr(experiment, "collect_provenance", forbidden)
    monkeypatch.setattr(experiment.RunStore, "create", forbidden)

    with pytest.raises(ValueError, match="rounds back"):
        run_categorical_dqm_experiment(
            categorical_dqm_config(tmp_path, finite_difference_step=1.0e-320)
        )

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_renderer_exception_cannot_change_finalized_numerical_bytes(tmp_path: Path):
    baseline = run_categorical_dqm_experiment(
        categorical_dqm_config(tmp_path / "baseline")
    )

    def fail_renderer(
        run_dir: Path, output_dir: Path, *, requested: tuple[str, ...]
    ) -> object:
        assert json.loads((run_dir / "manifest.json").read_text("utf-8"))[
            "complete"
        ] is True
        assert requested == ("categorical_dqm",)
        raise RuntimeError("injected categorical DQM renderer failure")

    failed = run_categorical_dqm_experiment(
        categorical_dqm_config(tmp_path / "failed", render_figures=True),
        renderer=fail_renderer,
    )

    assert failed.status == baseline.status == "pass"
    assert failed.figure_status == "failed"
    assert (baseline.run_dir / "metrics.json").read_bytes() == (
        failed.run_dir / "metrics.json"
    ).read_bytes()
    assert (baseline.run_dir / "arrays.npz").read_bytes() == (
        failed.run_dir / "arrays.npz"
    ).read_bytes()


@pytest.mark.parametrize("forged_status", ["complete", "failed"])
def test_unbacked_renderer_statuses_are_recorded_as_failures(
    tmp_path: Path, forged_status: str
):
    result = run_categorical_dqm_experiment(
        categorical_dqm_config(tmp_path, render_figures=True),
        renderer=lambda *_args, **_kwargs: SimpleNamespace(status=forged_status),
    )

    assert result.status == "pass"
    assert result.figure_status == "failed"
    assert result.figure_dir is not None
    failure = json.loads((result.figure_dir / "figure-manifest.json").read_text("utf-8"))
    assert failure["status"] == "failed"
    assert "unbacked" in failure["message"]


def test_secondary_failure_record_error_cannot_invalidate_finalized_numerics(
    tmp_path: Path,
):
    def fail_and_block_failure_record(
        run_dir: Path, output_dir: Path, *, requested: tuple[str, ...]
    ) -> object:
        assert json.loads((run_dir / "manifest.json").read_text("utf-8"))[
            "complete"
        ] is True
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        output_dir.write_text("blocks failure record", encoding="utf-8")
        raise RuntimeError("primary renderer failure")

    result = run_categorical_dqm_experiment(
        categorical_dqm_config(tmp_path, render_figures=True),
        renderer=fail_and_block_failure_record,
    )

    assert result.status == "pass"
    assert result.figure_status == "failed"
    assert result.figure_dir is not None and result.figure_dir.is_file()
    assert json.loads((result.run_dir / "manifest.json").read_text("utf-8"))[
        "complete"
    ] is True


def test_categorical_dqm_launcher_is_import_safe_and_main_honors_output_override(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    launcher_path = Path(__file__).resolve().parents[1] / "run_categorical_dqm_lab.py"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["run_categorical_dqm_lab.py", "--invalid"])
    spec = importlib.util.spec_from_file_location(
        "categorical_dqm_launcher_under_test", launcher_path
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    assert list(tmp_path.iterdir()) == []
    assert not hasattr(module, "parser")
    assert module.THEORY == {
        "experiment": "categorical_dqm",
        "fixture": "three_category_softmax_v1",
        "theta": [math.log(2.0), math.log(3.0)],
        "finite_difference_step": 1.0e-5,
        "dqm_step_sizes": [0.1, 0.05, 0.025, 0.0125],
    }
    assert set(module.OUTPUT) == {
        "root",
        "collect_diagnostics",
        "render_figures",
    }
    assert module.OUTPUT["render_figures"] is True
    module.OUTPUT["root"] = str(tmp_path / "owned-artifacts")
    result = module.main()

    assert isinstance(result, CategoricalDqmExperimentResult)
    assert result.status == "pass"
    assert result.figure_status == "complete"
    assert result.figure_dir is not None
    assert result.figure_dir.is_dir()
    figure_manifest_path = result.figure_dir / "figure-manifest.json"
    assert figure_manifest_path.is_file()
    figure_manifest = json.loads(figure_manifest_path.read_text("utf-8"))
    assert figure_manifest["status"] == "complete"
    assert figure_manifest["requested"] == ["categorical_dqm"]
    assert figure_manifest["figures"] == [
        {
            "name": "categorical_dqm",
            "pdf": "categorical-dqm-diagnostic.pdf",
            "pdf_sha256": hashlib.sha256(
                (result.figure_dir / "categorical-dqm-diagnostic.pdf").read_bytes()
            ).hexdigest(),
            "png": "categorical-dqm-diagnostic.png",
            "png_dpi": 300,
            "png_sha256": hashlib.sha256(
                (result.figure_dir / "categorical-dqm-diagnostic.png").read_bytes()
            ).hexdigest(),
        }
    ]
    assert (result.figure_dir / "categorical-dqm-diagnostic.pdf").is_file()
    assert (result.figure_dir / "categorical-dqm-diagnostic.png").is_file()
    np.testing.assert_array_equal(
        result.arrays["theta"], [math.log(2.0), math.log(3.0)]
    )
    np.testing.assert_array_equal(
        result.arrays["dqm_step_sizes"], [0.1, 0.05, 0.025, 0.0125]
    )
    output = capsys.readouterr().out
    assert f"run_dir={result.run_dir}" in output
    assert f"status=pass; metrics={len(result.metrics)}" in output
    assert "figures=complete" in output
