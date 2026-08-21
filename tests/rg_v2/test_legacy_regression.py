"""Regression gates for the v1 laboratory frozen before rg_v2 shared seams."""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import subprocess
import tomllib
from typing import Mapping

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
_ADDITIVE_SOURCE_SEAMS = frozenset({
    "src/multiagent_elbo/config.py",
    "src/multiagent_elbo/experiment_support.py",
})

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
    "run_attention_lab.py", "run_categorical_dqm_lab.py", "run_categorical_falsification_lab.py",
    "run_finite_counterexample_lab.py", "run_finite_lab.py", "run_gauge_holonomy_lab.py",
    "run_gaussian_fixed_ray_lab.py", "run_gaussian_lab.py", "run_information_history_lab.py",
    "run_multiagent_network_lab.py", "run_scale_cocycle_lab.py", "run_theory_oracle_lab.py",
)
semantic_names = (
    "three_level_extension.json", "composed_channels.json", "coarse_actions.json",
    "posterior_bridges.json", "comparison_isomorphisms.json", "derivative_cocycle.json",
    "retained_projection_residual.json",
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
    """Capture v1 with a fresh ``-I -B`` interpreter rooted at ``root``."""
    environment = os.environ.copy()
    environment.update(CUDA_VISIBLE_DEVICES="-1", PYTHONHASHSEED="0", PYTHONPATH="")
    completed = subprocess.run(
        [_PYTHON, "-I", "-B", "-c", _CAPTURE_BOOTSTRAP, str(root), str(output_root)],
        cwd=root, env=environment, check=True, capture_output=True, text=True,
    )
    return json.loads(completed.stdout)


def _manifest_payload(captured: Mapping[str, object]) -> dict[str, object]:
    """Validate the one-object capture protocol and bind it to the declared commit."""
    assert captured["schema_version"] == "legacy-rescaling-v1-capture-v1"
    assert captured["captured_commit"] == _BASELINE_COMMIT
    assert tuple(captured["launchers"]) == _BASELINE_LAUNCHERS
    return {
        "baseline_commit": _BASELINE_COMMIT,
        "launchers": captured["launchers"],
        "scale_cocycle_metrics": captured["scale_cocycle_metrics"],
        "scale_cocycle_semantic_artifact_sha256": captured["scale_cocycle_semantic_artifact_sha256"],
        "schema_version": captured["schema_version"],
        "source_fixture_sha256": captured["source_fixture_sha256"],
    }


def _refresh_legacy_manifest(task_temp: Path) -> dict[str, object]:
    """Refresh the manifest only through a verified detached baseline worktree."""
    if os.environ.get("RG_V2_REFRESH_LEGACY_BASELINE") != "1":
        raise RuntimeError("legacy refresh requires RG_V2_REFRESH_LEGACY_BASELINE=1")
    task_temp = task_temp.resolve()
    baseline_root = (task_temp / "detached-legacy-baseline").resolve()
    output_root = (task_temp / "detached-legacy-output").resolve()
    assert _ROOT not in baseline_root.parents
    assert not baseline_root.exists()
    created = False
    try:
        subprocess.run(
            ["git", "-C", str(_ROOT), "worktree", "add", "--detach", str(baseline_root), _BASELINE_COMMIT],
            check=True, capture_output=True, text=True,
        )
        created = True
        assert subprocess.check_output(
            ["git", "-C", str(baseline_root), "rev-parse", "HEAD"], text=True,
        ).strip() == _BASELINE_COMMIT
        assert subprocess.run(
            ["git", "-C", str(baseline_root), "symbolic-ref", "-q", "HEAD"], capture_output=True,
        ).returncode == 1
        payload = _manifest_payload(_capture_legacy_snapshot(baseline_root, output_root))
        existing_bytes = _MANIFEST_PATH.read_bytes() if _MANIFEST_PATH.exists() else None
        if existing_bytes is not None:
            assert json.loads(existing_bytes) == payload
            replacement = existing_bytes
        else:
            replacement = (json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        temporary = _MANIFEST_PATH.with_name(".legacy_rescaling_v1.refresh.tmp")
        try:
            temporary.write_bytes(replacement)
            os.replace(temporary, _MANIFEST_PATH)
        finally:
            temporary.unlink(missing_ok=True)
        return payload
    finally:
        if created:
            assert baseline_root.exists()
            subprocess.run(
                ["git", "-C", str(_ROOT), "worktree", "remove", str(baseline_root)],
                check=True, capture_output=True, text=True,
            )
            assert not baseline_root.exists()


def _git_blob_id(root: Path, revision: str, relative_path: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", f"{revision}:{relative_path}"], text=True,
    ).strip()


def _worktree_blob_id(root: Path, relative_path: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "hash-object", f"--path={relative_path}", "--", str(root / relative_path)], text=True,
    ).strip()


def _baseline_protected_source_blobs() -> dict[str, str]:
    """Return every baseline installed-package Python blob except approved seams."""
    listing = subprocess.check_output(
        ["git", "-C", str(_ROOT), "ls-tree", "-r", _BASELINE_COMMIT, "--", "src/multiagent_elbo"], text=True,
    )
    blobs: dict[str, str] = {}
    for line in listing.splitlines():
        metadata, relative_path = line.split("\t", maxsplit=1)
        _mode, kind, blob = metadata.split()
        if kind == "blob" and relative_path.endswith(".py") and relative_path not in _ADDITIVE_SOURCE_SEAMS:
            blobs[relative_path] = blob
    return blobs


def _current_protected_source_blobs() -> dict[str, str]:
    source_root = _ROOT / "src" / "multiagent_elbo"
    return {
        path.relative_to(_ROOT).as_posix(): _worktree_blob_id(_ROOT, path.relative_to(_ROOT).as_posix())
        for path in source_root.rglob("*.py")
        if path.relative_to(_ROOT).as_posix() not in _ADDITIVE_SOURCE_SEAMS
    }


def _assert_same_protected_blobs(expected: Mapping[str, str], actual: Mapping[str, str]) -> None:
    """Fail distinctly for removed, added, or modified protected source paths."""
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    changed = sorted(path for path in set(expected) & set(actual) if expected[path] != actual[path])
    assert not missing, f"missing protected source paths: {missing}"
    assert not extra, f"extra protected source paths: {extra}"
    assert not changed, f"changed protected source blobs: {changed}"


def test_protected_blob_comparison_seam_rejects_missing_extra_and_changed() -> None:
    expected = {"src/multiagent_elbo/a.py": "baseline"}
    with pytest.raises(AssertionError, match="missing"):
        _assert_same_protected_blobs(expected, {})
    with pytest.raises(AssertionError, match="extra"):
        _assert_same_protected_blobs(expected, {**expected, "src/multiagent_elbo/b.py": "extra"})
    with pytest.raises(AssertionError, match="changed"):
        _assert_same_protected_blobs(expected, {"src/multiagent_elbo/a.py": "changed"})


def test_legacy_manifest_matches_current_v1_capture(tmp_path: Path) -> None:
    manifest = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
    current = _capture_legacy_snapshot(_ROOT, tmp_path / "current-scale-cocycle")
    assert manifest == _manifest_payload({**current, "captured_commit": _BASELINE_COMMIT})


def test_root_local_boundary_preserves_v1_packaging_and_sources() -> None:
    assert _worktree_blob_id(_ROOT, "pyproject.toml") == _git_blob_id(_ROOT, _BASELINE_COMMIT, "pyproject.toml")
    pyproject = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["tool"]["setuptools"]["packages"]["find"]["where"] == ["src"]
    assert not (_ROOT / "src" / "multiagent_elbo" / "rg_v2").exists()
    _assert_same_protected_blobs(_baseline_protected_source_blobs(), _current_protected_source_blobs())
    for source in (_ROOT / "src" / "multiagent_elbo").rglob("*.py"):
        for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"), filename=str(source))):
            if isinstance(node, ast.Import): assert all(alias.name != "rg_v2" and not alias.name.startswith("rg_v2.") for alias in node.names), source
            if isinstance(node, ast.ImportFrom): assert node.module is None or (node.module != "rg_v2" and not node.module.startswith("rg_v2.")), source
    for path in (*_BASELINE_LAUNCHERS, *_SOURCE_FIXTURES): assert _worktree_blob_id(_ROOT, path) == _git_blob_id(_ROOT, _BASELINE_COMMIT, path)


@pytest.mark.skipif(os.environ.get("RG_V2_REFRESH_LEGACY_BASELINE") != "1", reason="explicit refresh only")
def test_refresh_controller_creates_and_removes_detached_baseline(tmp_path: Path) -> None:
    """The real explicit refresh path reproduces manifest bytes and cleans up."""
    before = _MANIFEST_PATH.read_bytes()
    assert _refresh_legacy_manifest(tmp_path) == json.loads(before)
    assert _MANIFEST_PATH.read_bytes() == before
    assert not (tmp_path / "detached-legacy-baseline").exists()
