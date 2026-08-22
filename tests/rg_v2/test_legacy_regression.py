"""Frozen v1 regression and repository-local boundary gates."""

from __future__ import annotations

import ast
from collections.abc import Iterator
import json
import os
from pathlib import Path
import subprocess
import tempfile
import tomllib
from typing import Mapping

import pytest


_BASELINE = "244f4893b135decfb8e61627bc8f12c409da3e98"
_ROOT = Path(__file__).resolve().parents[2]
_MANIFEST = _ROOT / "rg_v2/data/legacy_rescaling_v1.json"
_PYTHON = Path(r"C:\Python314\python.exe")
_SEAMS = frozenset(
    {
        "src/multiagent_elbo/config.py",
        "src/multiagent_elbo/experiment_support.py",
    }
)
_LAUNCHERS = (
    "run_attention_lab.py",
    "run_categorical_dqm_lab.py",
    "run_categorical_falsification_lab.py",
    "run_finite_counterexample_lab.py",
    "run_finite_lab.py",
    "run_gauge_holonomy_lab.py",
    "run_gaussian_fixed_ray_lab.py",
    "run_gaussian_lab.py",
    "run_information_history_lab.py",
    "run_multiagent_network_lab.py",
    "run_scale_cocycle_lab.py",
    "run_theory_oracle_lab.py",
)

_BOOT = r'''
import contextlib, hashlib, json, site, subprocess, sys
from pathlib import Path
import runpy
root, out = (Path(x).resolve() for x in sys.argv[1:3])
if not (root / "src").is_dir(): raise RuntimeError("capture root lacks src/")
out.mkdir(parents=True, exist_ok=True); sys.path.insert(0, str(root / "src")); sys.path.insert(1, str(root))
if site.getusersitepackages() not in sys.path: sys.path.append(site.getusersitepackages())
from multiagent_elbo.config import ExperimentConfig, canonical_config_json, config_sha256
from multiagent_elbo.finite.scale_cocycle_experiment import run_scale_cocycle_experiment
L=("run_attention_lab.py","run_categorical_dqm_lab.py","run_categorical_falsification_lab.py","run_finite_counterexample_lab.py","run_finite_lab.py","run_gauge_holonomy_lab.py","run_gaussian_fixed_ray_lab.py","run_gaussian_lab.py","run_information_history_lab.py","run_multiagent_network_lab.py","run_scale_cocycle_lab.py","run_theory_oracle_lab.py")
S=("three_level_extension.json","composed_channels.json","coarse_actions.json","posterior_bridges.json","comparison_isomorphisms.json","derivative_cocycle.json","retained_projection_residual.json")
def c(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True)
def n(x):
 if isinstance(x,dict): return {k:n(v) for k,v in x.items() if k not in {"run_dir","run_path","publication_root"}}
 if isinstance(x,list): return [n(v) for v in x]
 return x
configs={}
with contextlib.redirect_stdout(sys.stderr):
 for launcher in L:
  z=runpy.run_path(str(root/launcher),run_name="rg_v2_legacy_capture"); q=ExperimentConfig.from_dicts(z["RUN"],z["THEORY"],z["NUMERICS"],z["OUTPUT"],z.get("COMPUTE")); x,h=canonical_config_json(q),config_sha256(q)
  if hashlib.sha256(x.encode()).hexdigest()!=h: raise AssertionError(launcher)
  configs[launcher]={"canonical_config_json":x,"sha256":h}
 z=runpy.run_path(str(root/"run_scale_cocycle_lab.py"),run_name="rg_v2_legacy_capture"); o=dict(z["OUTPUT"]); o["root"]=str(out); r=run_scale_cocycle_experiment(ExperimentConfig.from_dicts(z["RUN"],z["THEORY"],z["NUMERICS"],o,z.get("COMPUTE")))
sh={f:hashlib.sha256(c(n(json.loads((r.run_dir/f).read_text(encoding="utf-8")))).encode()).hexdigest() for f in S}; m=json.loads((r.run_dir/"metrics.json").read_text(encoding="utf-8"))
sys.stdout.write(c({"schema_version":"legacy-rescaling-v1-capture-v1","captured_commit":subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip(),"launchers":configs,"source_fixture_sha256":{"tests/fixtures/two_scale_application_v1.json":hashlib.sha256((root/"tests/fixtures/two_scale_application_v1.json").read_bytes()).hexdigest()},"scale_cocycle_semantic_artifact_sha256":sh,"scale_cocycle_metrics":{k:m[k] for k in sorted(m)}}))
'''


@pytest.fixture
def external_task_temp() -> Iterator[Path]:
    with tempfile.TemporaryDirectory(prefix="rg-v2-task8-") as raw_path:
        path = Path(raw_path).resolve()
        root = _ROOT.resolve()
        assert path != root
        assert root not in path.parents
        yield path


def _guard_output(root: Path, output: Path) -> tuple[Path, Path]:
    root, output = root.resolve(), output.resolve()
    for protected in (root, _ROOT.resolve()):
        if output == protected or protected in output.parents:
            raise ValueError("capture output must be external to every revision root")
    return root, output


def _capture_legacy_snapshot(root: Path, output: Path) -> dict[str, object]:
    root, output = _guard_output(root, output)
    environment = os.environ.copy()
    environment.update(
        CUDA_VISIBLE_DEVICES="-1",
        PYTHONHASHSEED="0",
        PYTHONPATH="",
    )
    completed = subprocess.run(
        [
            _PYTHON,
            "-I",
            "-B",
            "-c",
            _BOOT,
            str(root),
            str(output),
        ],
        cwd=root,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    assert isinstance(payload, dict)
    return payload


def _payload(
    captured: Mapping[str, object],
    *,
    expected_commit: str,
) -> dict[str, object]:
    assert captured["schema_version"] == "legacy-rescaling-v1-capture-v1"
    assert captured["captured_commit"] == expected_commit
    assert tuple(captured["launchers"]) == _LAUNCHERS
    return {
        "baseline_commit": _BASELINE,
        "launchers": captured["launchers"],
        "scale_cocycle_metrics": captured["scale_cocycle_metrics"],
        "scale_cocycle_semantic_artifact_sha256": captured[
            "scale_cocycle_semantic_artifact_sha256"
        ],
        "schema_version": captured["schema_version"],
        "source_fixture_sha256": captured["source_fixture_sha256"],
    }


def _write_manifest(
    manifest_path: Path,
    payload: Mapping[str, object],
) -> None:
    temporary = manifest_path.with_name(f".{manifest_path.name}.refresh.tmp")
    try:
        temporary.write_text(
            json.dumps(
                payload,
                ensure_ascii=True,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, manifest_path)
    finally:
        temporary.unlink(missing_ok=True)


def _capture_detached_baseline(task_temp: Path) -> dict[str, object]:
    _, task_temp = _guard_output(_ROOT, task_temp)
    baseline_root = (task_temp / "detached-legacy-baseline").resolve()
    output_root = (task_temp / "detached-legacy-output").resolve()
    baseline_root, output_root = _guard_output(baseline_root, output_root)
    assert _ROOT.resolve() not in baseline_root.parents
    assert not baseline_root.exists()
    made = False
    try:
        subprocess.run(
            [
                "git",
                "-C",
                str(_ROOT),
                "worktree",
                "add",
                "--detach",
                str(baseline_root),
                _BASELINE,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        made = True
        assert (
            subprocess.check_output(
                ["git", "-C", str(baseline_root), "rev-parse", "HEAD"],
                text=True,
            ).strip()
            == _BASELINE
        )
        assert (
            subprocess.run(
                ["git", "-C", str(baseline_root), "symbolic-ref", "-q", "HEAD"],
                capture_output=True,
            ).returncode
            == 1
        )
        return _capture_legacy_snapshot(baseline_root, output_root)
    finally:
        if made:
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(_ROOT),
                    "worktree",
                    "remove",
                    str(baseline_root),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            assert not baseline_root.exists()


def _refresh(
    task_temp: Path,
    *,
    manifest_path: Path = _MANIFEST,
) -> dict[str, object]:
    if os.environ.get("RG_V2_REFRESH_LEGACY_BASELINE") != "1":
        raise RuntimeError("explicit refresh only")
    payload = _payload(
        _capture_detached_baseline(task_temp),
        expected_commit=_BASELINE,
    )
    _write_manifest(manifest_path, payload)
    return payload


def _blob(root: Path, spec: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", spec],
        text=True,
    ).strip()


def _work(root: Path, path: str) -> str:
    return subprocess.check_output(
        [
            "git",
            "-C",
            str(root),
            "hash-object",
            f"--path={path}",
            "--",
            str(root / path),
        ],
        text=True,
    ).strip()


def _baseline_map() -> dict[str, str]:
    rows = subprocess.check_output(
        [
            "git",
            "-C",
            str(_ROOT),
            "ls-tree",
            "-r",
            _BASELINE,
            "--",
            "src/multiagent_elbo",
        ],
        text=True,
    ).splitlines()
    return {
        path: metadata.split()[2]
        for row in rows
        for metadata, path in [row.split("\t", 1)]
        if path.endswith(".py") and path not in _SEAMS
    }


def _current_map() -> dict[str, str]:
    return {
        path.relative_to(_ROOT).as_posix(): _work(
            _ROOT,
            path.relative_to(_ROOT).as_posix(),
        )
        for path in (_ROOT / "src/multiagent_elbo").rglob("*.py")
        if path.relative_to(_ROOT).as_posix() not in _SEAMS
    }


def _same(expected: Mapping[str, str], actual: Mapping[str, str]) -> None:
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    changed = sorted(
        path
        for path in set(expected) & set(actual)
        if expected[path] != actual[path]
    )
    assert not missing, f"missing {missing}"
    assert not extra, f"extra {extra}"
    assert not changed, f"changed {changed}"


def test_output_guard_rejects_in_worktree_before_subprocess(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: pytest.fail("subprocess launched"),
    )
    with pytest.raises(ValueError, match="external"):
        _capture_legacy_snapshot(
            _ROOT,
            _ROOT / "rg_v2" / "forbidden-output",
        )


def test_refresh_rejects_in_worktree_candidate_before_git_or_path_effect(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    candidate = _ROOT / "rg_v2" / ".refresh-preflight-guard"
    assert not candidate.exists()
    monkeypatch.setenv("RG_V2_REFRESH_LEGACY_BASELINE", "1")
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: pytest.fail("subprocess launched"),
    )
    monkeypatch.setattr(
        subprocess,
        "check_output",
        lambda *args, **kwargs: pytest.fail("git launched"),
    )
    with pytest.raises(ValueError, match="external"):
        _refresh(candidate)
    assert not candidate.exists()


def test_blob_seam_rejects_all_drift() -> None:
    expected = {"src/multiagent_elbo/a.py": "x"}
    cases = (
        ({}, "missing"),
        ({**expected, "src/multiagent_elbo/b.py": "x"}, "extra"),
        ({"src/multiagent_elbo/a.py": "y"}, "changed"),
    )
    for actual, word in cases:
        with pytest.raises(AssertionError, match=word):
            _same(expected, actual)


def test_legacy_manifest_matches_fresh_baseline_and_current_captures(
    external_task_temp: Path,
) -> None:
    manifest = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    baseline = _capture_detached_baseline(external_task_temp)
    assert _payload(baseline, expected_commit=_BASELINE) == manifest
    assert not (external_task_temp / "detached-legacy-baseline").exists()

    current = _capture_legacy_snapshot(
        _ROOT,
        external_task_temp / "current-legacy-output",
    )
    current_commit = subprocess.check_output(
        ["git", "-C", str(_ROOT), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    assert _payload(current, expected_commit=current_commit) == manifest


def test_boundary() -> None:
    assert _work(_ROOT, "pyproject.toml") == _blob(
        _ROOT,
        f"{_BASELINE}:pyproject.toml",
    )
    metadata = tomllib.loads(
        (_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    assert metadata["tool"]["setuptools"]["packages"]["find"]["where"] == ["src"]
    assert not (_ROOT / "src/multiagent_elbo/rg_v2").exists()
    _same(_baseline_map(), _current_map())
    for source in (_ROOT / "src/multiagent_elbo").rglob("*.py"):
        for node in ast.walk(
            ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        ):
            if isinstance(node, ast.Import):
                assert all(
                    alias.name != "rg_v2"
                    and not alias.name.startswith("rg_v2.")
                    for alias in node.names
                )
            if isinstance(node, ast.ImportFrom):
                assert node.module is None or (
                    node.module != "rg_v2"
                    and not node.module.startswith("rg_v2.")
                )
    for path in (*_LAUNCHERS, "tests/fixtures/two_scale_application_v1.json"):
        assert _work(_ROOT, path) == _blob(_ROOT, f"{_BASELINE}:{path}")


def test_refresh_writes_absent_destination_from_detached_capture(
    monkeypatch: pytest.MonkeyPatch,
    external_task_temp: Path,
) -> None:
    destination = external_task_temp / "legacy_rescaling_v1.json"
    assert not destination.exists()
    monkeypatch.setenv("RG_V2_REFRESH_LEGACY_BASELINE", "1")
    payload = _refresh(external_task_temp, manifest_path=destination)
    assert json.loads(destination.read_text(encoding="utf-8")) == payload
    assert destination.read_text(encoding="utf-8") == (
        json.dumps(
            payload,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    assert not (external_task_temp / "detached-legacy-baseline").exists()


@pytest.mark.skipif(
    os.environ.get("RG_V2_REFRESH_LEGACY_BASELINE") != "1",
    reason="explicit refresh only",
)
def test_refresh(external_task_temp: Path) -> None:
    assert _refresh(external_task_temp) == json.loads(
        _MANIFEST.read_text(encoding="utf-8")
    )
    assert not (external_task_temp / "detached-legacy-baseline").exists()
