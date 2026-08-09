from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.finite.attention_experiment import (
    AttentionExperimentResult,
    run_attention_experiment,
)


METRIC_KEYS = {
    "ATT-01_factorization_residual",
    "ATT-01_normalization_residual",
    "ATT-02_direct_staged_eta_residual",
    "ATT-02_direct_staged_alpha_residual",
    "ATT-02_direct_staged_active_beta_residual",
    "ATT-02_literal_eta_residual",
    "ATT-02_literal_alpha_residual",
    "ATT-02_literal_active_beta_residual",
    "ATT-02_reverse_bridge_residual",
    "ATT-03_gauge_logits_residual",
    "ATT-03_gauge_alpha_residual",
    "ATT-03_gauge_beta_residual",
    "ATT-03_gauge_eta_residual",
    "ATT-03_broken_link_gap_control",
    "ATT-04_relabeling_naturality_residual",
    "ATT-04_incoherent_relabeling_gap_control",
    "ATT-NEG-01_beta_only_associativity_gap",
    "ATT-NEG-01_beta_only_correct_gap",
}

IDENTITY_KEYS = {
    "ATT-01_factorization_residual",
    "ATT-01_normalization_residual",
    "ATT-02_direct_staged_eta_residual",
    "ATT-02_direct_staged_alpha_residual",
    "ATT-02_direct_staged_active_beta_residual",
    "ATT-02_literal_eta_residual",
    "ATT-02_literal_alpha_residual",
    "ATT-02_literal_active_beta_residual",
    "ATT-02_reverse_bridge_residual",
    "ATT-03_gauge_logits_residual",
    "ATT-03_gauge_alpha_residual",
    "ATT-03_gauge_beta_residual",
    "ATT-03_gauge_eta_residual",
    "ATT-04_relabeling_naturality_residual",
}

CORE_ARRAY_KEYS = {
    "beta_only_correct_beta",
    "beta_only_direct_beta",
    "beta_only_staged_beta",
    "direct_coarse_active_receiver_mask",
    "direct_coarse_alpha",
    "direct_coarse_beta",
    "direct_coarse_eta",
    "direct_coarse_state_probability",
    "fine_active_receiver_mask",
    "fine_alpha",
    "fine_beta",
    "fine_eta",
    "fine_state_probability",
    "middle_active_receiver_mask",
    "middle_alpha",
    "middle_beta",
    "middle_eta",
    "middle_state_probability",
    "staged_coarse_active_receiver_mask",
    "staged_coarse_alpha",
    "staged_coarse_beta",
    "staged_coarse_eta",
    "staged_coarse_state_probability",
}

DIAGNOSTIC_KEYS = {
    "gauge_broken_eta",
    "gauge_frames",
    "gauge_links",
    "gauge_receiver_covectors",
    "gauge_receiver_vectors",
    "gauge_source_vectors",
    "gauge_transformed_links",
    "gauge_transformed_receiver_covectors",
    "gauge_transformed_receiver_vectors",
    "gauge_transformed_source_vectors",
    "incoherent_coarse_eta",
    "relabeling_eta",
    "relabeling_permutation",
    "relabeling_receiver_partition",
    "relabeling_source_partition",
    "receiver_partition_direct",
    "receiver_partition_fine_to_middle",
    "receiver_partition_middle_to_coarse",
    "reverse_bridge_direct",
    "reverse_bridge_expected",
    "reverse_bridge_staged",
    "source_partition_direct",
    "source_partition_fine_to_middle",
    "source_partition_middle_to_coarse",
    "state_channel_direct",
    "state_channel_fine_to_middle",
    "state_channel_middle_to_coarse",
}


def attention_config(
    root: Path,
    *,
    seed: int = 20260809,
    collect_diagnostics: bool = False,
    render_figures: bool = False,
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "attention_marked_event", "seed": seed},
        {
            "experiment": "attention_marked_event",
            "fixture": "nested_nonuniform_v1",
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


def test_attention_runner_rejects_invalid_inputs_before_runtime_seams(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.finite.attention_experiment as experiment

    def forbidden(*_args, **_kwargs):
        raise AssertionError("runtime seam executed before config validation")

    monkeypatch.setattr(experiment.RngStreams, "from_seed", forbidden)
    monkeypatch.setattr(experiment, "collect_provenance", forbidden)
    monkeypatch.setattr(experiment.RunStore, "create", forbidden)

    with pytest.raises(TypeError, match="ExperimentConfig"):
        run_attention_experiment({})  # type: ignore[arg-type]

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
    with pytest.raises(ValueError, match="attention_marked_event"):
        run_attention_experiment(wrong)

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_default_attention_run_emits_the_registered_exact_metrics(tmp_path: Path):
    config = attention_config(tmp_path)

    result = run_attention_experiment(config)

    assert isinstance(result, AttentionExperimentResult)
    assert result.status == "pass"
    assert set(result.metrics) == METRIC_KEYS
    tolerance = config.numerics.atol + config.numerics.rtol
    for name in IDENTITY_KEYS:
        metric = result.metrics[name]
        assert metric.status == "pass"
        assert metric.tolerance == tolerance
        assert abs(metric.value) <= tolerance
        assert metric.assessment_scope == "implementation_check"
    assert result.metrics[
        "ATT-NEG-01_beta_only_associativity_gap"
    ].value == pytest.approx(1.0 / 10.0, abs=tolerance)
    assert result.metrics[
        "ATT-NEG-01_beta_only_correct_gap"
    ].value == pytest.approx(1.0 / 20.0, abs=tolerance)
    assert result.metrics["ATT-03_broken_link_gap_control"].value > tolerance
    assert result.metrics[
        "ATT-04_incoherent_relabeling_gap_control"
    ].value > tolerance
    assert all(metric.status == "pass" for metric in result.metrics.values())


def _write_attention_figure_manifest(
    run_dir: Path, output_dir: Path, requested: tuple[str, ...]
) -> SimpleNamespace:
    output_dir.mkdir(parents=True, exist_ok=True)
    png = output_dir / "attention-composition.png"
    pdf = output_dir / "attention-composition.pdf"
    png.write_bytes(b"\x89PNG\r\n\x1a\nattention fixture")
    pdf.write_bytes(b"%PDF-1.7\nattention fixture")
    manifest_path = output_dir / "figure-manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "figures": [
                    {
                        "name": "attention_composition",
                        "png": png.name,
                        "png_sha256": hashlib.sha256(png.read_bytes()).hexdigest(),
                        "pdf": pdf.name,
                        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
                    }
                ],
                "message": None,
                "requested": list(requested),
                "run_dir": str(run_dir.resolve()),
                "status": "complete",
            }
        ),
        encoding="utf-8",
    )
    return SimpleNamespace(
        status="complete",
        run_dir=run_dir,
        output_dir=output_dir,
        requested=requested,
        manifest_path=manifest_path,
    )


@pytest.mark.parametrize("collect_diagnostics", [False, True])
@pytest.mark.parametrize("render_figures", [False, True])
def test_attention_output_toggles_have_exact_finalized_inventories(
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
        assert requested == ("attention_composition",)
        return _write_attention_figure_manifest(run_dir, output_dir, requested)

    result = run_attention_experiment(
        attention_config(
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
    assert manifest["provenance"]["experiment_scope"] == (
        "pre_registered_state_conditioned_marked_event_fixture"
    )
    assert manifest["provenance"]["metamorphic_scope"] == (
        "scalar_gauge_plus_finite_relabeling"
    )
    with np.load(result.run_dir / "arrays.npz", allow_pickle=False) as archive:
        assert archive.files == sorted(CORE_ARRAY_KEYS)
        assert set(archive.files) == CORE_ARRAY_KEYS
    diagnostics_path = result.run_dir / "diagnostics.npz"
    assert diagnostics_path.is_file() is collect_diagnostics
    if collect_diagnostics:
        with np.load(diagnostics_path, allow_pickle=False) as archive:
            assert archive.files == sorted(DIAGNOSTIC_KEYS)
            assert set(archive.files) == DIAGNOSTIC_KEYS
    expected_figure_dir = result.run_dir.parent / "figures" / result.run_dir.name
    assert renderer_calls == int(render_figures)
    assert result.figure_status == (
        "complete" if render_figures else "not_requested"
    )
    assert result.figure_dir == (expected_figure_dir if render_figures else None)
    assert expected_figure_dir.exists() is render_figures


def test_attention_semantic_artifacts_are_deterministic_and_results_immutable(
    tmp_path: Path,
):
    first = run_attention_experiment(attention_config(tmp_path / "first"))
    second = run_attention_experiment(attention_config(tmp_path / "second"))

    assert (first.run_dir / "metrics.json").read_bytes() == (
        second.run_dir / "metrics.json"
    ).read_bytes()
    assert (first.run_dir / "arrays.npz").read_bytes() == (
        second.run_dir / "arrays.npz"
    ).read_bytes()
    with pytest.raises(TypeError):
        first.metrics["new"] = first.metrics["ATT-01_factorization_residual"]  # type: ignore[index]
    with pytest.raises(TypeError):
        first.arrays["new"] = np.zeros(1)  # type: ignore[index]
    assert all(not array.flags.writeable for array in first.arrays.values())
    with pytest.raises(ValueError):
        first.arrays["fine_eta"][0, 0, 0] = 1.0


def test_renderer_failure_cannot_change_finalized_attention_numerics(tmp_path: Path):
    baseline = run_attention_experiment(attention_config(tmp_path / "baseline"))

    def fail_after_finalization(
        run_dir: Path, output_dir: Path, *, requested: tuple[str, ...]
    ) -> object:
        assert json.loads((run_dir / "manifest.json").read_text("utf-8"))[
            "complete"
        ] is True
        assert (run_dir / "metrics.json").is_file()
        assert (run_dir / "arrays.npz").is_file()
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        output_dir.write_text("blocks secondary failure evidence", encoding="utf-8")
        raise RuntimeError("injected attention renderer failure")

    failed = run_attention_experiment(
        attention_config(tmp_path / "failed", render_figures=True),
        renderer=fail_after_finalization,
    )

    assert failed.status == baseline.status == "pass"
    assert failed.figure_status == "failed"
    assert failed.figure_dir is not None
    assert (baseline.run_dir / "metrics.json").read_bytes() == (
        failed.run_dir / "metrics.json"
    ).read_bytes()
    assert (baseline.run_dir / "arrays.npz").read_bytes() == (
        failed.run_dir / "arrays.npz"
    ).read_bytes()


def test_unbacked_attention_renderer_success_is_recorded_as_failure(tmp_path: Path):
    result = run_attention_experiment(
        attention_config(tmp_path, render_figures=True),
        renderer=lambda *_args, **_kwargs: SimpleNamespace(status="complete"),
    )

    assert result.status == "pass"
    assert result.figure_status == "failed"
    assert result.figure_dir is not None
    failure = json.loads((result.figure_dir / "figure-manifest.json").read_text("utf-8"))
    assert failure["status"] == "failed"
    assert "unbacked" in failure["message"]


def test_attention_launcher_import_is_side_effect_free_and_main_is_click_to_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    launcher_path = Path(__file__).resolve().parents[1] / "run_attention_lab.py"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        "sys.argv", ["run_attention_lab.py", "--invalid"]
    )
    spec = importlib.util.spec_from_file_location(
        "attention_launcher_under_test", launcher_path
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    assert list(tmp_path.iterdir()) == []
    assert not hasattr(module, "parser")
    assert set(module.OUTPUT) == {
        "root",
        "collect_diagnostics",
        "render_figures",
    }
    module.OUTPUT["root"] = str(tmp_path / "owned-artifacts")
    result = module.main()

    assert isinstance(result, AttentionExperimentResult)
    assert result.status == "pass"
    assert result.figure_status == "not_requested"
    output = capsys.readouterr().out
    assert f"run_dir={result.run_dir}" in output
    assert f"status=pass; metrics={len(METRIC_KEYS)}" in output
    assert "figures=not_requested" in output
