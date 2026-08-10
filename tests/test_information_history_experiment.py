from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from multiagent_elbo.config import ExperimentConfig


APPLICATION_ID = "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"
ARTIFACT_NAMES = {
    "history_parameters",
    "scores",
    "fisher_matrices",
    "vfe_gradients",
    "natural_gradient_fields",
    "information_durations",
    "semiconjugacy_defects",
}
METRIC_NAMES = {
    "score_finite_difference_residual",
    "fisher_defect_residual",
    "natural_gradient_range_residual",
    "arc_length_reparameterization_residual",
    "semiconjugacy_defect_norm",
}


def _sut():
    try:
        import multiagent_elbo.finite.information_history_experiment as module
    except ModuleNotFoundError:
        pytest.fail("information-history experiment implementation is missing", pytrace=False)
    return module


def information_history_config(
    root: Path, *, render_figures: bool = False
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "information_history", "seed": 20260809},
        {
            "experiment": "information_history",
            "fixture": "two_scale_application_v1",
            "family": "categorical_softmax",
            "history_steps": 16,
            "step_size": 0.05,
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
            "collect_diagnostics": True,
            "render_figures": render_figures,
        },
    )


def _npz_payloads(run_dir: Path) -> dict[str, bytes]:
    return {
        name: (run_dir / f"{name}.npz").read_bytes()
        for name in sorted(ARTIFACT_NAMES)
    }


def test_experiment_rejects_the_wrong_discriminator_before_publication(tmp_path: Path):
    module = _sut()
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
        {"root": str(tmp_path), "collect_diagnostics": False, "render_figures": False},
    )

    with pytest.raises(ValueError, match="information_history"):
        module.run_information_history_experiment(wrong)

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_fixture_validation_precedes_rng_and_artifact_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    module = _sut()
    fixture_path = Path(__file__).parent / "fixtures" / "two_scale_application_v1.json"
    malformed = json.loads(fixture_path.read_text(encoding="utf-8"))
    malformed["application_id"] = "0" * 64

    def forbidden(*_args, **_kwargs):
        raise AssertionError("runtime seam executed before fixture validation")

    monkeypatch.setattr(module, "_load_fixture_payload", lambda _path: malformed)
    monkeypatch.setattr(module.RngStreams, "from_seed", forbidden)
    monkeypatch.setattr(module.RunStore, "create", forbidden)

    with pytest.raises(ValueError, match="application_id"):
        module.run_information_history_experiment(information_history_config(tmp_path))

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_unexposed_rendering_is_rejected_before_artifact_creation(tmp_path: Path):
    module = _sut()

    with pytest.raises(ValueError, match="does not expose rendering"):
        module.run_information_history_experiment(
            information_history_config(tmp_path, render_figures=True)
        )

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_default_run_publishes_exact_registered_artifacts_and_typed_metrics(tmp_path: Path):
    module = _sut()

    result = module.run_information_history_experiment(information_history_config(tmp_path))

    assert result.status == "pass"
    assert set(result.metrics) == METRIC_NAMES
    assert set(result.artifact_arrays) == ARTIFACT_NAMES
    assert {path.name for path in result.run_dir.iterdir()} == {
        "config.json",
        "manifest.json",
        "metrics.json",
        *(f"{name}.npz" for name in ARTIFACT_NAMES),
    }
    for metric in result.metrics.values():
        assert metric.status in {"pass", "fail", "inconclusive"}
        assert metric.theorem_status in {"ESTABLISHED", "HYPOTHESIS", "CONJECTURE", "NUMERICAL", "OPEN"}
        assert metric.verification_state in {"CANDIDATE", "LLM_SUPPORTED", "EVIDENCE_VERIFIED", "REFUTED", "INCONCLUSIVE"}
        assert metric.claim_origin in {"STANDARD", "PROJECT_NOVEL", "APPLICATION_SPECIFIC"}
    assert result.metrics["semiconjugacy_defect_norm"].status == "pass"
    assert result.metrics["semiconjugacy_defect_norm"].theorem_status == "OPEN"
    assert result.metrics["semiconjugacy_defect_norm"].verification_state == "INCONCLUSIVE"


def test_artifact_fields_recompute_every_registered_metric(tmp_path: Path):
    module = _sut()
    result = module.run_information_history_experiment(information_history_config(tmp_path))
    tolerance = result.metrics["score_finite_difference_residual"].tolerance

    scores = result.artifact_arrays["scores"]
    fisher = result.artifact_arrays["fisher_matrices"]
    natural = result.artifact_arrays["natural_gradient_fields"]
    durations = result.artifact_arrays["information_durations"]
    defects = result.artifact_arrays["semiconjugacy_defects"]
    score_residual = max(
        float(np.max(np.abs(scores["fine_finite_difference"] - scores["fine_analytic"]))),
        float(np.max(np.abs(scores["pushed_finite_difference"] - scores["pushed_analytic"]))),
        float(np.max(np.abs(scores["coarse_finite_difference"] - scores["coarse_analytic"]))),
    )

    assert result.metrics["score_finite_difference_residual"].value == pytest.approx(score_residual)
    assert result.metrics["fisher_defect_residual"].value == pytest.approx(
        float(np.max(np.abs(fisher["identity_residual"])))
    )
    assert result.metrics["natural_gradient_range_residual"].value == pytest.approx(
        max(float(np.max(natural["fine_range_residual"])), float(np.max(natural["coarse_range_residual"])))
    )
    assert result.metrics["arc_length_reparameterization_residual"].value == pytest.approx(
        abs(float(durations["information_duration"][-1]) - float(durations["reparameterized_information_duration"][-1]))
    )
    original_delta = np.diff(durations["fine_parameters"], axis=0)
    transformed_delta = np.diff(durations["reparameterized_fine_parameters"], axis=0)
    original_oracle = np.concatenate(
        ([0.0], np.cumsum(np.sqrt(np.einsum(
            "si,sij,sj->s", original_delta, durations["fine_segment_fisher"], original_delta
        ))))
    )
    transformed_oracle = np.concatenate(
        ([0.0], np.cumsum(np.sqrt(np.einsum(
            "si,sij,sj->s",
            transformed_delta,
            durations["reparameterized_segment_fisher"],
            transformed_delta,
        ))))
    )
    mutation_oracle = np.concatenate(
        ([0.0], np.cumsum(np.sqrt(np.einsum(
            "si,sij,sj->s",
            transformed_delta,
            durations["fine_segment_fisher"],
            transformed_delta,
        ))))
    )
    np.testing.assert_allclose(durations["information_duration"], original_oracle, atol=1.0e-15)
    np.testing.assert_allclose(
        durations["reparameterized_information_duration"], transformed_oracle, atol=1.0e-15
    )
    np.testing.assert_allclose(
        durations["reparameterization_jacobian"], 2.0 * np.eye(4), atol=0.0
    )
    np.testing.assert_allclose(
        durations["reparameterized_segment_fisher"],
        durations["fine_segment_fisher"] / 4.0,
        atol=1.0e-15,
    )
    np.testing.assert_allclose(
        durations["metric_pullback_mutation_duration"], mutation_oracle, atol=1.0e-15
    )
    assert mutation_oracle[-1] > transformed_oracle[-1] + 0.1
    assert result.metrics["semiconjugacy_defect_norm"].value == pytest.approx(
        float(np.max(defects["norm"]))
    )
    np.testing.assert_allclose(
        defects["defect"],
        np.einsum(
            "sij,sj->si", defects["coarse_map_jacobian"], natural["fine"]
        )
        - natural["coarse"],
        atol=1.0e-15,
    )
    assert score_residual <= tolerance


def test_artifacts_pin_every_required_assumption_boundary_and_geometry_control(
    tmp_path: Path,
):
    module = _sut()
    result = module.run_information_history_experiment(information_history_config(tmp_path))
    scores = result.artifact_arrays["scores"]
    fisher = result.artifact_arrays["fisher_matrices"]
    durations = result.artifact_arrays["information_durations"]
    semiconjugacy = result.artifact_arrays["semiconjugacy_defects"]

    np.testing.assert_allclose(
        scores["parameter_dependent_conditional_expected_score"],
        [[0.0], [0.0]],
        atol=1.0e-15,
    )
    np.testing.assert_allclose(
        scores["parameter_dependent_actual_coarse_score"],
        [[0.5], [-0.5]],
        atol=1.0e-8,
    )
    assert float(scores["parameter_dependent_channel_gap"]) == pytest.approx(0.5, abs=1.0e-8)
    assert int(fisher["rank_deficient_control_rank"]) == 1
    assert float(fisher["rank_deficient_control_range_residual"]) < 1.0e-12
    np.testing.assert_allclose(
        fisher["rank_deficient_control_fisher"] @ fisher["rank_deficient_control_natural_gradient"],
        -fisher["rank_deficient_control_vfe_gradient"],
        atol=1.0e-12,
    )
    np.testing.assert_array_equal(
        durations["same_endpoint_straight_history"][[0, -1]],
        durations["same_endpoint_detour_history"][[0, -1]],
    )
    assert durations["same_endpoint_detour_duration"][-1] > durations["same_endpoint_straight_duration"][-1] + 0.05
    assert float(durations["chart_raw_coordinate_length_ratio"]) == pytest.approx(2.0)
    assert float(durations["chart_information_duration_residual"]) < 1.0e-14
    assert float(semiconjugacy["plus_sign_mutation_gap"]) > 0.1


def test_same_seed_semantic_metric_and_npz_bundles_are_root_independent(tmp_path: Path):
    module = _sut()
    first = module.run_information_history_experiment(information_history_config(tmp_path / "first"))
    second = module.run_information_history_experiment(information_history_config(tmp_path / "second"))

    assert first.config_hash != second.config_hash
    assert (first.run_dir / "metrics.json").read_bytes() == (second.run_dir / "metrics.json").read_bytes()
    assert _npz_payloads(first.run_dir) == _npz_payloads(second.run_dir)
    assert all(
        not array.flags.writeable
        for artifact in first.artifact_arrays.values()
        for array in artifact.values()
    )


def test_manifest_binds_fixture_source_theory_rng_float_and_performance_provenance(tmp_path: Path):
    module = _sut()
    result = module.run_information_history_experiment(information_history_config(tmp_path))

    manifest = json.loads((result.run_dir / "manifest.json").read_text(encoding="utf-8"))
    provenance = manifest["provenance"]

    assert manifest["complete"] is True
    assert provenance["application_id"] == APPLICATION_ID
    assert provenance["fixture_sha256"] == hashlib.sha256(
        (Path(__file__).parent / "fixtures" / "two_scale_application_v1.json").read_bytes()
    ).hexdigest()
    assert provenance["config_hash"] == result.config_hash
    assert provenance["theory_sha256"]
    assert provenance["source_revision"]
    assert provenance["dirty_tree_sha256"]
    assert provenance["rng"]["seed"] == 20260809
    assert set(provenance["rng"]["named_streams"]) == {"problem", "recognition", "controls", "figures"}
    assert provenance["floating_point"] == {"backend": "cpu", "dtype": "float64"}
    assert provenance["performance_records"]["wall_time_seconds"] >= 0.0
    assert provenance["performance_records"]["peak_tracemalloc_bytes"] >= 0


def test_launcher_is_import_safe_and_preserves_exact_click_to_run_defaults(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    _sut()
    launcher_path = Path(__file__).resolve().parents[1] / "run_information_history_lab.py"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["run_information_history_lab.py", "--invalid"])
    spec = importlib.util.spec_from_file_location("information_history_launcher_under_test", launcher_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    assert list(tmp_path.iterdir()) == []
    assert not hasattr(module, "parser")
    assert module.THEORY == {
        "experiment": "information_history",
        "fixture": "two_scale_application_v1",
        "family": "categorical_softmax",
        "history_steps": 16,
        "step_size": 0.05,
    }
    module.OUTPUT["root"] = str(tmp_path / "owned-artifacts")
    result = module.main()

    assert result.status == "pass"
    output = capsys.readouterr().out
    assert f"run_dir={result.run_dir}" in output
    assert "status=pass; metrics=5" in output


def test_launcher_runs_from_sanitized_uninstalled_temporary_cwd(tmp_path: Path):
    _sut()
    launcher_path = Path(__file__).resolve().parents[1] / "run_information_history_lab.py"
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)

    completed = subprocess.run(
        [r"C:\Python314\python.exe", str(launcher_path)],
        cwd=tmp_path,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
    )

    assert completed.returncode == 0, completed.stderr
    assert "status=pass; metrics=5" in completed.stdout
    assert (tmp_path / "artifacts" / "information_history").is_dir()
