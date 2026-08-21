"""Frozen v1 regression and repository-local boundary gates."""
from __future__ import annotations
import ast, json, os, subprocess, tomllib
from pathlib import Path
from typing import Mapping
import pytest

_BASELINE = "c04a56e80abf3fd956941aa0021a3a93ea53eaae"
_ROOT = Path(__file__).resolve().parents[2]
_MANIFEST = _ROOT / "rg_v2/data/legacy_rescaling_v1.json"
_PYTHON = Path(r"C:\Python314\python.exe")
_SEAMS = frozenset({"src/multiagent_elbo/config.py", "src/multiagent_elbo/experiment_support.py"})
_LAUNCHERS = ("run_attention_lab.py", "run_categorical_dqm_lab.py", "run_categorical_falsification_lab.py", "run_finite_counterexample_lab.py", "run_finite_lab.py", "run_gauge_holonomy_lab.py", "run_gaussian_fixed_ray_lab.py", "run_gaussian_lab.py", "run_information_history_lab.py", "run_multiagent_network_lab.py", "run_scale_cocycle_lab.py", "run_theory_oracle_lab.py")

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

def _guard_output(root: Path, output: Path) -> tuple[Path, Path]:
    root, output = root.resolve(), output.resolve()
    for protected in (root, _ROOT.resolve()):
        if output == protected or protected in output.parents:
            raise ValueError("capture output must be external to every revision root")
    return root, output

def _capture_legacy_snapshot(root: Path, output: Path) -> dict[str, object]:
    root, output = _guard_output(root, output)
    env = os.environ.copy(); env.update(CUDA_VISIBLE_DEVICES="-1", PYTHONHASHSEED="0", PYTHONPATH="")
    done = subprocess.run([_PYTHON,"-I","-B","-c",_BOOT,str(root),str(output)],cwd=root,env=env,check=True,capture_output=True,text=True)
    return json.loads(done.stdout)

def _payload(captured: Mapping[str, object]) -> dict[str, object]:
    assert captured["schema_version"] == "legacy-rescaling-v1-capture-v1" and captured["captured_commit"] == _BASELINE
    assert tuple(captured["launchers"]) == _LAUNCHERS
    return {"baseline_commit":_BASELINE,"launchers":captured["launchers"],"scale_cocycle_metrics":captured["scale_cocycle_metrics"],"scale_cocycle_semantic_artifact_sha256":captured["scale_cocycle_semantic_artifact_sha256"],"schema_version":captured["schema_version"],"source_fixture_sha256":captured["source_fixture_sha256"]}

def _refresh(tmp: Path) -> dict[str, object]:
    if os.environ.get("RG_V2_REFRESH_LEGACY_BASELINE") != "1": raise RuntimeError("explicit refresh only")
    base, out = (tmp/"detached-legacy-baseline").resolve(), (tmp/"detached-legacy-output").resolve(); assert _ROOT not in base.parents and not base.exists(); made=False
    try:
        subprocess.run(["git","-C",str(_ROOT),"worktree","add","--detach",str(base),_BASELINE],check=True,capture_output=True,text=True); made=True
        assert subprocess.check_output(["git","-C",str(base),"rev-parse","HEAD"],text=True).strip()==_BASELINE
        assert subprocess.run(["git","-C",str(base),"symbolic-ref","-q","HEAD"],capture_output=True).returncode==1
        p=_payload(_capture_legacy_snapshot(base,out)); old=_MANIFEST.read_bytes(); assert json.loads(old)==p
        t=_MANIFEST.with_name(".legacy_rescaling_v1.refresh.tmp")
        try: t.write_bytes(old); os.replace(t,_MANIFEST)
        finally: t.unlink(missing_ok=True)
        return p
    finally:
        if made: subprocess.run(["git","-C",str(_ROOT),"worktree","remove",str(base)],check=True,capture_output=True,text=True); assert not base.exists()

def _blob(root: Path, spec: str) -> str: return subprocess.check_output(["git","-C",str(root),"rev-parse",spec],text=True).strip()
def _work(root: Path, path: str) -> str: return subprocess.check_output(["git","-C",str(root),"hash-object",f"--path={path}","--",str(root/path)],text=True).strip()
def _baseline_map() -> dict[str,str]:
    rows=subprocess.check_output(["git","-C",str(_ROOT),"ls-tree","-r",_BASELINE,"--","src/multiagent_elbo"],text=True).splitlines(); return {p:m.split()[2] for row in rows for m,p in [row.split("\t",1)] if p.endswith(".py") and p not in _SEAMS}
def _current_map() -> dict[str,str]: return {p.relative_to(_ROOT).as_posix():_work(_ROOT,p.relative_to(_ROOT).as_posix()) for p in (_ROOT/"src/multiagent_elbo").rglob("*.py") if p.relative_to(_ROOT).as_posix() not in _SEAMS}
def _same(expected: Mapping[str,str], actual: Mapping[str,str]) -> None:
    missing=sorted(set(expected)-set(actual)); extra=sorted(set(actual)-set(expected)); changed=sorted(p for p in set(expected)&set(actual) if expected[p]!=actual[p]); assert not missing,f"missing {missing}"; assert not extra,f"extra {extra}"; assert not changed,f"changed {changed}"

def test_output_guard_rejects_in_worktree_before_subprocess(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(subprocess,"run",lambda *a,**k: pytest.fail("subprocess launched"))
    with pytest.raises(ValueError,match="external"):_capture_legacy_snapshot(_ROOT,_ROOT/"rg_v2"/"forbidden-output")

def test_blob_seam_rejects_all_drift() -> None:
    e={"src/multiagent_elbo/a.py":"x"}
    for a,word in (({},"missing"),({**e,"src/multiagent_elbo/b.py":"x"},"extra"),({"src/multiagent_elbo/a.py":"y"},"changed")):
        with pytest.raises(AssertionError,match=word):_same(e,a)

def test_legacy_manifest_current(tmp_path: Path) -> None:
    c=_capture_legacy_snapshot(_ROOT,tmp_path/"external-output"); assert json.loads(_MANIFEST.read_text(encoding="utf-8"))==_payload({**c,"captured_commit":_BASELINE})

def test_boundary() -> None:
    assert _work(_ROOT,"pyproject.toml")==_blob(_ROOT,f"{_BASELINE}:pyproject.toml"); assert tomllib.loads((_ROOT/"pyproject.toml").read_text())["tool"]["setuptools"]["packages"]["find"]["where"]==["src"]; assert not (_ROOT/"src/multiagent_elbo/rg_v2").exists(); _same(_baseline_map(),_current_map())
    for s in (_ROOT/"src/multiagent_elbo").rglob("*.py"):
        for n in ast.walk(ast.parse(s.read_text())):
            if isinstance(n,ast.Import): assert all(a.name!="rg_v2" and not a.name.startswith("rg_v2.") for a in n.names)
            if isinstance(n,ast.ImportFrom): assert n.module is None or (n.module!="rg_v2" and not n.module.startswith("rg_v2."))
    for p in (*_LAUNCHERS,"tests/fixtures/two_scale_application_v1.json"): assert _work(_ROOT,p)==_blob(_ROOT,f"{_BASELINE}:{p}")

@pytest.mark.skipif(os.environ.get("RG_V2_REFRESH_LEGACY_BASELINE")!="1",reason="explicit refresh only")
def test_refresh(tmp_path: Path) -> None:
    before=_MANIFEST.read_bytes(); assert _refresh(tmp_path)==json.loads(before); assert _MANIFEST.read_bytes()==before; assert not (tmp_path/"detached-legacy-baseline").exists()
