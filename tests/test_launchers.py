from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.figures import FigureManifest
from multiagent_elbo.finite.experiment import FiniteExperimentResult
from multiagent_elbo.finite.experiment import run_finite_experiment


REPO_ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = REPO_ROOT / "run_finite_lab.py"
FIGURE_LAUNCHER = REPO_ROOT / "make_figures.py"


def load_launcher(module_name: str, path: Path = LAUNCHER):
    specification = importlib.util.spec_from_file_location(module_name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


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
