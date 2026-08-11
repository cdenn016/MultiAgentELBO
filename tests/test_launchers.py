from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.figures import FigureManifest
from multiagent_elbo.finite.experiment import FiniteExperimentResult
from multiagent_elbo.finite.experiment import run_finite_experiment


REPO_ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = REPO_ROOT / "run_finite_lab.py"
FIGURE_LAUNCHER = REPO_ROOT / "make_figures.py"
ATTENTION_LAUNCHER = REPO_ROOT / "run_attention_lab.py"
CATEGORICAL_DQM_LAUNCHER = REPO_ROOT / "run_categorical_dqm_lab.py"
MULTIAGENT_NETWORK_LAUNCHER = REPO_ROOT / "run_multiagent_network_lab.py"
THEORY_ORACLE_LAUNCHER = REPO_ROOT / "run_theory_oracle_lab.py"
FINITE_COUNTEREXAMPLE_LAUNCHER = REPO_ROOT / "run_finite_counterexample_lab.py"
INFORMATION_HISTORY_LAUNCHER = REPO_ROOT / "run_information_history_lab.py"
GAUGE_HOLONOMY_LAUNCHER = REPO_ROOT / "run_gauge_holonomy_lab.py"
SCALE_COCYCLE_LAUNCHER = REPO_ROOT / "run_scale_cocycle_lab.py"
GAUSSIAN_FIXED_RAY_LAUNCHER = REPO_ROOT / "run_gaussian_fixed_ray_lab.py"
GAUSSIAN_FIXED_RAY_DIAGNOSTIC_LAUNCHER = (
    REPO_ROOT / "run_gaussian_fixed_ray_diagnostic.py"
)
GAUSSIAN_CONFIRMATORY_SOURCE = (
    REPO_ROOT
    / "docs"
    / "verification"
    / "evidence"
    / "2026-08-10-gaussian-confirmatory-fcb2c49"
)
NEW_LAUNCHERS = (
    ("attention", ATTENTION_LAUNCHER, "pass"),
    ("categorical_dqm", CATEGORICAL_DQM_LAUNCHER, "pass"),
    ("multiagent_network", MULTIAGENT_NETWORK_LAUNCHER, "pass"),
    ("theory_oracle", THEORY_ORACLE_LAUNCHER, "pass"),
    ("finite_counterexample", FINITE_COUNTEREXAMPLE_LAUNCHER, "inconclusive"),
    ("information_history", INFORMATION_HISTORY_LAUNCHER, "pass"),
    ("gauge_holonomy", GAUGE_HOLONOMY_LAUNCHER, "pass"),
    ("scale_cocycle", SCALE_COCYCLE_LAUNCHER, "pass"),
    ("gaussian_fixed_ray", GAUSSIAN_FIXED_RAY_LAUNCHER, "inconclusive"),
)


def load_launcher(module_name: str, path: Path = LAUNCHER):
    specification = importlib.util.spec_from_file_location(module_name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def test_fixed_ray_diagnostic_launcher_import_is_side_effect_free(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        [GAUSSIAN_FIXED_RAY_DIAGNOSTIC_LAUNCHER.name, "--invalid-argument"],
    )

    module = load_launcher(
        "fixed_ray_diagnostic_launcher_import_only",
        GAUSSIAN_FIXED_RAY_DIAGNOSTIC_LAUNCHER,
    )

    assert hasattr(module, "main")
    assert not hasattr(module, "parser")
    assert list(tmp_path.iterdir()) == []


def test_fixed_ray_diagnostic_launcher_exposes_only_six_editable_dictionaries() -> None:
    module = load_launcher(
        "fixed_ray_diagnostic_launcher_dictionary_contract",
        GAUSSIAN_FIXED_RAY_DIAGNOSTIC_LAUNCHER,
    )

    editable = {
        name
        for name, value in vars(module).items()
        if name.isupper() and isinstance(value, dict)
    }
    assert editable == {"RUN", "THEORY", "NUMERICS", "OUTPUT", "COMPUTE", "SOURCE"}
    assert module.COMPUTE["backend"] == "cpu"
    assert module.COMPUTE["heavy_sweep_enabled"] is False


def test_fixed_ray_diagnostic_launcher_runs_with_temporary_source_and_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = load_launcher(
        "fixed_ray_diagnostic_launcher_success",
        GAUSSIAN_FIXED_RAY_DIAGNOSTIC_LAUNCHER,
    )
    source_root = tmp_path / "source"
    output_root = tmp_path / "output"
    shutil.copytree(GAUSSIAN_CONFIRMATORY_SOURCE, source_root)
    module.SOURCE = {**module.SOURCE, "root": str(source_root)}
    module.OUTPUT = {**module.OUTPUT, "root": str(output_root)}

    diagnostic_module = sys.modules[module.run_fixed_model_diagnostic.__module__]

    def clean_provenance(
        repository_root: Path,
        theory_root: Path,
        config_hash: str,
        rng_streams: object,
    ) -> dict[str, object]:
        del repository_root, theory_root, rng_streams
        return {
            "config_hash": config_hash,
            "git_commit": module._current_git_revision(),
            "git_dirty": False,
            "theory_sha256": "f" * 64,
        }

    monkeypatch.setattr(diagnostic_module, "collect_provenance", clean_provenance)

    result = module.main()

    assert result.status == "complete"
    assert result.run_dir.is_relative_to(output_root)
    assert (
        json.loads((result.run_dir / "manifest.json").read_text("utf-8"))["complete"]
        is True
    )


def test_fixed_ray_diagnostic_launcher_missing_default_source_writes_nothing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = load_launcher(
        "fixed_ray_diagnostic_launcher_missing_source",
        GAUSSIAN_FIXED_RAY_DIAGNOSTIC_LAUNCHER,
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(module, "ROOT", tmp_path)

    with pytest.raises(FileNotFoundError, match="source directory"):
        module.main()

    assert list(tmp_path.iterdir()) == []


def test_new_stable_primitives_results_and_runs_are_public_package_exports():
    from multiagent_elbo.finite import (
        AttentionDisintegration,
        AttentionExperimentResult,
        AgentNetworkExperimentResult,
        CategoricalDqmAnalysis,
        CategoricalDqmExperimentResult,
        CategoricalExponentialFamily,
        DqmRemainderLadder,
        FiniteCounterexampleExperimentResult,
        InformationHistoryExperimentResult,
        ScaleCocycleExperimentResult,
        StateConditionedAttentionLaw,
        TheoryOracleExperimentResult,
        analyze_categorical_dqm,
        centered_log_probability_finite_difference,
        centered_pushed_log_probability_finite_difference,
        compose_kernels,
        normalized_dqm_remainder_ladder,
        run_agent_network_experiment,
        run_attention_experiment,
        run_categorical_dqm_experiment,
        run_finite_counterexample_experiment,
        run_information_history_experiment,
        run_scale_cocycle_experiment,
        run_theory_oracle_experiment,
    )
    from multiagent_elbo.geometry import (
        AttentionCovariantInputs,
        AttentionGaugeEvaluation,
        HolonomyExperimentResult,
        evaluate_attention,
        run_holonomy_experiment,
        transform_attention_inputs,
    )
    from multiagent_elbo.realizations.gaussian import (
        GaussianFixedRayExperimentResult,
        run_gaussian_fixed_ray_experiment,
    )

    assert all(
        value is not None
        for value in (
            AttentionDisintegration,
            AttentionExperimentResult,
            AgentNetworkExperimentResult,
            CategoricalDqmAnalysis,
            CategoricalDqmExperimentResult,
            CategoricalExponentialFamily,
            DqmRemainderLadder,
            FiniteCounterexampleExperimentResult,
            InformationHistoryExperimentResult,
            ScaleCocycleExperimentResult,
            StateConditionedAttentionLaw,
            TheoryOracleExperimentResult,
            analyze_categorical_dqm,
            centered_log_probability_finite_difference,
            centered_pushed_log_probability_finite_difference,
            compose_kernels,
            normalized_dqm_remainder_ladder,
            run_agent_network_experiment,
            run_attention_experiment,
            run_categorical_dqm_experiment,
            run_finite_counterexample_experiment,
            run_information_history_experiment,
            run_scale_cocycle_experiment,
            run_theory_oracle_experiment,
            AttentionCovariantInputs,
            AttentionGaugeEvaluation,
            HolonomyExperimentResult,
            evaluate_attention,
            run_holonomy_experiment,
            transform_attention_inputs,
            GaussianFixedRayExperimentResult,
            run_gaussian_fixed_ray_experiment,
        )
    )


@pytest.mark.parametrize(("label", "launcher", "expected_status"), NEW_LAUNCHERS)
def test_new_launcher_import_ignores_invalid_argv_and_has_no_side_effects(
    tmp_path: Path,
    monkeypatch,
    label: str,
    launcher: Path,
    expected_status: str,
):
    del expected_status
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", [launcher.name, "--invalid-argument"])

    module = load_launcher(f"{label}_launcher_import_only", launcher)

    assert hasattr(module, "main")
    assert not hasattr(module, "parser")
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(("label", "launcher", "expected_status"), NEW_LAUNCHERS)
def test_new_launcher_main_needs_only_an_overridden_output_root(
    tmp_path: Path, label: str, launcher: Path, expected_status: str
):
    module = load_launcher(f"{label}_launcher_main", launcher)
    module.OUTPUT = {**module.OUTPUT, "root": str(tmp_path)}

    result = module.main()

    assert result.status == expected_status
    assert not hasattr(module, "parser")
    manifests = list(tmp_path.rglob("manifest.json"))
    assert manifests == [result.run_dir / "manifest.json"]
    assert json.loads(manifests[0].read_text("utf-8"))["complete"] is True


@pytest.mark.parametrize(("label", "launcher", "expected_status"), NEW_LAUNCHERS)
def test_new_launcher_runs_with_no_arguments_from_a_sanitized_temp_cwd(
    tmp_path: Path, label: str, launcher: Path, expected_status: str
):
    environment = os.environ.copy()
    environment["PYTHONPATH"] = ""

    completed = subprocess.run(
        [sys.executable, str(launcher)],
        cwd=tmp_path,
        env=environment,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert f"status={expected_status}" in completed.stdout
    manifests = list((tmp_path / "artifacts").rglob("manifest.json"))
    assert len(manifests) == 1
    assert json.loads(manifests[0].read_text("utf-8"))["complete"] is True


def test_import_does_not_read_process_arguments_or_write_files(
    tmp_path: Path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["run_finite_lab.py", "--invalid-argument"])

    module = load_launcher("run_finite_lab_import_only")

    assert hasattr(module, "main")
    assert not hasattr(module, "parser")
    assert list(tmp_path.iterdir()) == []


def test_launcher_runs_from_editable_dictionaries_after_only_output_root_changes(
    tmp_path: Path,
):
    module = load_launcher("run_finite_lab_smoke")
    module.OUTPUT = {**module.OUTPUT, "root": str(tmp_path)}

    result = module.main()

    assert isinstance(result, FiniteExperimentResult)
    manifests = list(tmp_path.rglob("manifest.json"))
    assert manifests == [result.run_dir / "manifest.json"]
    assert '"complete":true' in manifests[0].read_text("utf-8")


def test_finite_launcher_runs_from_a_temp_cwd_without_pythonpath_or_editable_install(
    tmp_path: Path,
):
    environment = os.environ.copy()
    environment["PYTHONPATH"] = ""

    completed = subprocess.run(
        [sys.executable, str(LAUNCHER)],
        cwd=tmp_path,
        env=environment,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "status=pass" in completed.stdout
    manifests = list((tmp_path / "artifacts").rglob("manifest.json"))
    assert len(manifests) == 1
    assert json.loads(manifests[0].read_text("utf-8"))["complete"] is True


def test_make_figures_is_dictionary_driven_and_replays_a_saved_run(tmp_path: Path):
    config = ExperimentConfig.from_dicts(
        {"name": "launcher replay", "seed": 7},
        {"experiment": "finite_exact", "retained_interaction_order": 2},
        {
            "dtype": "float64",
            "atol": 1e-10,
            "rtol": 1e-9,
            "min_spd_rcond": 1e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(tmp_path / "runs"),
            "collect_diagnostics": False,
            "render_figures": False,
        },
    )
    run = run_finite_experiment(config)
    module = load_launcher("make_figures_smoke", FIGURE_LAUNCHER)
    module.REPLAY = {
        "run_dir": str(run.run_dir),
        "output_dir": str(tmp_path / "replay"),
        "requested": ("finite_identity",),
    }

    result = module.main()

    assert isinstance(result, FigureManifest)
    assert result.status == "complete"
    assert not hasattr(module, "parser")


def test_make_figures_bootstraps_src_in_a_sanitized_temp_cwd(tmp_path: Path):
    environment = os.environ.copy()
    environment["PYTHONPATH"] = ""

    completed = subprocess.run(
        [sys.executable, str(FIGURE_LAUNCHER)],
        cwd=tmp_path,
        env=environment,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "status=failed" in completed.stdout
    failure_manifests = list(tmp_path.rglob("figure-manifest.json"))
    assert len(failure_manifests) == 1
    assert json.loads(failure_manifests[0].read_text("utf-8"))["status"] == "failed"
