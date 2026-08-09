from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

from multiagent_elbo.finite.experiment import FiniteExperimentResult


REPO_ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = REPO_ROOT / "run_finite_lab.py"


def load_launcher(module_name: str):
    specification = importlib.util.spec_from_file_location(module_name, LAUNCHER)
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
