"""Regression gates for the v1 laboratory frozen before rg_v2 shared seams."""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import subprocess
import tomllib

import pytest


_BASELINE_COMMIT = "c04a56e80abf3fd956941aa0021a3a93ea53eaae"
_ROOT = Path(__file__).resolve().parents[2]
_MANIFEST_PATH = _ROOT / "rg_v2" / "data" / "legacy_rescaling_v1.json"
_PYTHON = Path(r"C:\Python314\python.exe")
_BASELINE_LAUNCHERS = (
    "run_attention_lab.py", "run_categorical_dqm_lab.py",
    "run_categorical_falsification_lab.py", "run_finite_counterexample_lab.py",
    "run_finite_lab.py", "run_gauge_holonomy_lab.py",
    "run_gaussian_fixed_ray_lab.py", "run_gaussian_lab.py",
    "run_information_history_lab.py", "run_multiagent_network_lab.py",
    "run_scale_cocycle_lab.py", "run_theory_oracle_lab.py",
)
_SOURCE_FIXTURES = ("tests/fixtures/two_scale_application_v1.json",)
_SCALE_SEMANTIC_ARTIFACTS = (
    "three_level_extension.json", "composed_channels.json", "coarse_actions.json",
    "posterior_bridges.json", "comparison_isomorphisms.json",
    "derivative_cocycle.json", "retained_projection_residual.json",
)

_CAPTURE_BOOTSTRAP = r'''
import contextlib, hashlib, json, site, subprocess, sys
from pathlib import Path
import runpy

root, output_root = (Path(arg).resolve() for arg in sys.argv[1:3])
if not (root / "src").is_dir(): raise RuntimeError("capture root lacks src/")
output_root.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / "src")); sys.path.insert(1, str(root))
user_site = site.getusersitepackages()
if user_site not in sys.path: sys.path.append(user_site)
from multiagent_elbo.config import ExperimentConfig, canonical_config_json, config_sha256
from multiagent_elbo.finite.scale_cocycle_experiment import run_scale_cocycle_experiment

launchers = (
    "run_attention_lab.py", "run_categorical_dqm_lab.py",
    "run_categorical_falsification_lab.py", "run_finite_counterexample_lab.py",
    "run_finite_lab.py", "run_gauge_holonomy_lab.py",
    "run_gaussian_fixed_ray_lab.py", "run_gaussian_lab.py",
    "run_information_history_lab.py", "run_multiagent_network_lab.py",
    "run_scale_cocycle_lab.py", "run_theory_oracle_lab.py",
)
semantic_names = (
    "three_level_extension.json", "composed_channels.json", "coarse_actions.json",
    "posterior_bridges.json", "comparison_isomorphisms.json",
    "derivative_cocycle.json", "retained_projection_residual.json",
)
def canonical(value): return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
def normalize(value):
    if isinstance(value, dict): return {key: normalize(item) for key, item in value.items() if key not in {"run_dir", "run_path", "publication_root"}}
    if isinstance(value, list): return [normalize(item) for item in value]
    return value

configs = {}
with contextlib.redirect_stdout(sys.stderr):
    for launcher in launchers:
        namespace = runpy.run_path(str(root / launcher), run_name="rg_v2_legacy_capture")
        config = ExperimentConfig.from_dicts(namespace["RUN"], namespace["THEORY"], namespace["NUMERICS"], namespace["OUTPUT"], namespace.get("COMPUTE"))
        config_json, digest = canonical_config_json(config), config_sha256(config)
        if hashlib.sha256(config_json.encode("utf-8")).hexdigest() != digest: raise AssertionError(f"config digest mismatch for {launcher}")
        configs[launcher] = {"canonical_config_json": config_json, "sha256": digest}
    scale = runpy.run_path(str(root / "run_scale_cocycle_lab.py"), run_name="rg_v2_legacy_capture")
    output = dict(scale["OUTPUT"]); output["root"] = str(output_root)
    result = run_scale_cocycle_experiment(ExperimentConfig.from_dicts(scale["RUN"], scale["THEORY"], scale["NUMERICS"], output, scale.get("COMPUTE")))

semantic_hashes = {}
for name in semantic_names:
    payload = json.loads((result.run_dir / name).read_text(encoding="utf-8"))
    semantic_hashes[name] = hashlib.sha256(canonical(normalize(payload)).encode("utf-8")).hexdigest()
metrics = json.loads((result.run_dir / "metrics.json").read_text(encoding="utf-8"))
payload = {
    "schema_version": "legacy-rescaling-v1-capture-v1",
    "captured_commit": subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip(),
    "launchers": configs,
    "source_fixture_sha256": {"tests/fixtures/two_scale_application_v1.json": hashlib.sha256((root / "tests/fixtures/two_scale_application_v1.json").read_bytes()).hexdigest()},
    "scale_cocycle_semantic_artifact_sha256": semantic_hashes,
    "scale_cocycle_metrics": {name: metrics[name] for name in sorted(metrics)},
}
sys.stdout.write(canonical(payload))
'''


def _capture_legacy_snapshot(root: Path, output_root: Path) -> dict[str, object]:
    """Use a fresh ``-I -B`` interpreter with an empty inherited PYTHONPATH."""
    environment = os.environ.copy()
    environment.update(CUDA_VISIBLE_DEVICES="-1", PYTHONHASHSEED="0", PYTHONPATH="")
    completed = subprocess.run(
        [_PYTHON, "-I", "-B", "-c", _CAPTURE_BOOTSTRAP, str(root), str(output_root)],
        cwd=root, env=environment, check=True, capture_output=True, text=True,
    )
    return json.loads(completed.stdout)


def _git_blob_id(root: Path, revision: str, relative_path: str) -> None:
    """Compare filtered working-tree content to an exact baseline Git blob."""
    expected = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", f"{revision}:{relative_path}"], text=True,
    ).strip()
    actual = subprocess.check_output(
        ["git", "-C", str(root), "hash-object", f"--path={relative_path}", "--", str(root / relative_path)], text=True,
    ).strip()
    assert actual == expected, relative_path


def test_legacy_manifest_matches_current_v1_capture(tmp_path: Path) -> None:
    """A changed v1 config, fixture, semantic result, or metric must fail."""
    assert _MANIFEST_PATH.is_file(), "Task 1 must generate the detached-baseline manifest."
    manifest = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
    current = _capture_legacy_snapshot(_ROOT, tmp_path / "current-scale-cocycle")
    assert manifest["schema_version"] == "legacy-rescaling-v1-capture-v1"
    assert manifest["baseline_commit"] == _BASELINE_COMMIT
    for key in ("launchers", "source_fixture_sha256", "scale_cocycle_semantic_artifact_sha256", "scale_cocycle_metrics"):
        assert manifest[key] == current[key]


def test_root_local_boundary_preserves_v1_packaging_and_sources() -> None:
    """A reverse import, non-src package discovery, or protected v1 edit must fail."""
    _git_blob_id(_ROOT, _BASELINE_COMMIT, "pyproject.toml")
    pyproject = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["tool"]["setuptools"]["packages"]["find"]["where"] == ["src"]
    assert not (_ROOT / "src" / "multiagent_elbo" / "rg_v2").exists()
    for source in (_ROOT / "src" / "multiagent_elbo").rglob("*.py"):
        for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"), filename=str(source))):
            if isinstance(node, ast.Import):
                assert all(alias.name != "rg_v2" and not alias.name.startswith("rg_v2.") for alias in node.names), source
            if isinstance(node, ast.ImportFrom):
                assert node.module is None or (node.module != "rg_v2" and not node.module.startswith("rg_v2.")), source
    for path in (*_BASELINE_LAUNCHERS, *_SOURCE_FIXTURES): _git_blob_id(_ROOT, _BASELINE_COMMIT, path)


@pytest.mark.skipif(os.environ.get("RG_V2_REFRESH_LEGACY_BASELINE") != "1", reason="explicit baseline refresh only")
def test_refresh_capture_is_detached_baseline_only(tmp_path: Path) -> None:
    """The maintenance controller captures only a verified detached baseline root."""
    baseline_root = Path(os.environ["RG_V2_BASELINE_ROOT"]).resolve()
    assert baseline_root != _ROOT
    assert subprocess.check_output(["git", "-C", str(baseline_root), "rev-parse", "HEAD"], text=True).strip() == _BASELINE_COMMIT
    assert _capture_legacy_snapshot(baseline_root, tmp_path / "baseline-scale-cocycle")["captured_commit"] == _BASELINE_COMMIT
