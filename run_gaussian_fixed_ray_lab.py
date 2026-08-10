"""Click Run for the CPU pilot or an explicitly gated CUDA parity sentinel."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from multiagent_elbo.config import ExperimentConfig  # noqa: E402
from multiagent_elbo.realizations.gaussian.fixed_ray_experiment import (  # noqa: E402
    GaussianFixedRayExperimentResult,
    build_confirmatory_gate_record,
    build_cuda_gate_record,
    publish_confirmatory_experiment,
    publish_cuda_sentinel,
    run_gaussian_fixed_ray_experiment,
)


OPERATOR_CONTROL_PATH = ROOT / ".verification" / "gaussian-fixed-ray-operator-control.json"
CUDA_GATE_PATH = ROOT / ".verification" / "gaussian-fixed-ray-cuda-gate.json"
SENTINEL_STAGING_ROOT = ROOT / ".verification" / "gaussian-fixed-ray-sentinel-staging"
CONFIRMATORY_CONTROL_PATH = (
    ROOT / ".verification" / "gaussian-fixed-ray-confirmatory-control.json"
)
CONFIRMATORY_GATE_PATH = (
    ROOT / ".verification" / "gaussian-fixed-ray-confirmatory-gate.json"
)
CONFIRMATORY_STAGING_ROOT = (
    ROOT / ".verification" / "gaussian-fixed-ray-confirmatory-staging"
)
RUN = {"name": "gaussian-fixed-ray-pilot", "seed": 20260809}
THEORY = {
    "experiment": "gaussian_fixed_ray",
    "fixture": "gaussian_fixed_ray_v1",
    "preregistration": "2026-08-09-gaussian-fixed-ray-v1",
    "blocking_schemes": ["adjacent_pairs", "balanced_alternating"],
    "matrix_dimension": 2,
}
NUMERICS = {
    "dtype": "float64",
    "atol": 1e-12,
    "rtol": 1e-10,
    "min_spd_rcond": 1e-12,
    "max_frame_condition": 1.0e6,
}
OUTPUT = {
    "root": "artifacts",
    "collect_diagnostics": True,
    "render_figures": False,
}
COMPUTE = {
    "backend": "cpu",
    "dtype": "float64",
    "device_index": 0,
    "batch_size": 4096,
    "deterministic": True,
    "allow_tf32": False,
    "cpu_cuda_parity": True,
    "cuda_worker_python": r"C:\anaconda\python.exe",
    "heavy_sweep_enabled": False,
}


def _current_git_revision() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    revision = completed.stdout.strip()
    if completed.returncode != 0 or len(revision) != 40:
        raise RuntimeError("sentinel launcher requires a resolved Git revision")
    return revision


def _sentinel_run(revision: str) -> dict[str, object]:
    if not isinstance(revision, str) or len(revision) != 40:
        raise ValueError("sentinel run requires a full source revision")
    run = dict(RUN)
    run["name"] = f"gaussian-fixed-ray-sentinel-{revision[:12]}"
    return run


def _print_result(result: GaussianFixedRayExperimentResult) -> None:
    print(f"run_dir={result.run_dir}")
    print(f"status={result.status}")
    for name, metric in sorted(result.metrics.items()):
        print(
            f"{name}: value={metric.value:.12g} tolerance={metric.tolerance:.3g} "
            f"status={metric.status} theorem_status={metric.theorem_status} "
            f"verification_state={metric.verification_state} claim_origin={metric.claim_origin}"
        )


def _operator_control() -> dict[str, object]:
    if not OPERATOR_CONTROL_PATH.is_file():
        return {
            "mode": "pilot",
            "operator_opt_in": False,
            "accepted_gate_sha256": "",
        }
    control = json.loads(OPERATOR_CONTROL_PATH.read_text(encoding="utf-8"))
    if set(control) != {"mode", "operator_opt_in", "accepted_gate_sha256"}:
        raise ValueError("operator control sidecar does not match the frozen schema")
    return control


def _confirmatory_control() -> dict[str, object]:
    if not CONFIRMATORY_CONTROL_PATH.is_file():
        return {
            "mode": "pilot",
            "operator_opt_in": False,
            "accepted_gate_sha256": "",
            "accepted_sentinel_manifest_sha256": "",
        }
    control = json.loads(CONFIRMATORY_CONTROL_PATH.read_text(encoding="utf-8"))
    if set(control) != {
        "mode",
        "operator_opt_in",
        "accepted_gate_sha256",
        "accepted_sentinel_manifest_sha256",
    }:
        raise ValueError("confirmatory operator control does not match the frozen schema")
    if type(control["operator_opt_in"]) is not bool:
        raise ValueError("confirmatory operator opt-in must be a JSON Boolean")
    if control["mode"] in {"confirmatory_gate", "confirmatory_run"} and (
        control["operator_opt_in"] is not True
    ):
        raise ValueError("confirmatory execution requires literal operator_opt_in=true")
    return control


def _find_accepted_sentinel_run(
    manifest_sha256: str, source_revision: str
) -> Path:
    if not isinstance(manifest_sha256, str) or len(manifest_sha256) != 64:
        raise ValueError("confirmatory run requires a sentinel manifest SHA-256")
    if (
        not isinstance(source_revision, str)
        or len(source_revision) != 40
        or any(
            character not in "0123456789abcdef"
            for character in source_revision.lower()
        )
    ):
        raise ValueError("confirmatory gate requires a full Git source revision")
    root = (
        ROOT
        / str(OUTPUT["root"])
        / str(_sentinel_run(source_revision)["name"])
    )
    matches: list[Path] = []
    if root.is_dir():
        for manifest in root.glob("*/manifest.json"):
            if hashlib.sha256(manifest.read_bytes()).hexdigest() == manifest_sha256:
                matches.append(manifest.parent)
    if len(matches) != 1:
        raise ValueError("accepted sentinel manifest must resolve to exactly one run")
    return matches[0]


def main() -> GaussianFixedRayExperimentResult | dict[str, object]:
    confirmatory = _confirmatory_control()
    confirmatory_mode = confirmatory["mode"]
    if confirmatory_mode in {"confirmatory_gate", "confirmatory_run"}:
        compute = dict(COMPUTE)
        compute["backend"] = "cuda"
        compute["heavy_sweep_enabled"] = True
        run = dict(RUN)
        run["name"] = "gaussian-fixed-ray-confirmatory"
        config = ExperimentConfig.from_dicts(run, THEORY, NUMERICS, OUTPUT, compute)
        operator_opt_in = confirmatory["operator_opt_in"]
        accepted_gate_sha256 = confirmatory["accepted_gate_sha256"]
        accepted_sentinel_manifest_sha256 = confirmatory[
            "accepted_sentinel_manifest_sha256"
        ]
        if confirmatory_mode == "confirmatory_gate":
            gate = build_confirmatory_gate_record(
                config, operator_opt_in=operator_opt_in
            )
            CONFIRMATORY_GATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            payload = json.dumps(
                gate, sort_keys=True, separators=(",", ":"), allow_nan=False
            )
            temporary = CONFIRMATORY_GATE_PATH.with_suffix(
                CONFIRMATORY_GATE_PATH.suffix + ".tmp"
            )
            temporary.write_text(payload, encoding="utf-8")
            temporary.replace(CONFIRMATORY_GATE_PATH)
            digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            print(f"confirmatory_gate_path={CONFIRMATORY_GATE_PATH}")
            print(f"confirmatory_gate_sha256={digest}")
            print(f"processes_present={gate['processes_present']}")
            print("acceptance_required=set accepted_gate_sha256 to this exact digest")
            return gate

        if not accepted_gate_sha256 or not accepted_sentinel_manifest_sha256:
            raise ValueError(
                "confirmatory_run requires accepted gate and sentinel manifest digests"
            )
        gate = json.loads(CONFIRMATORY_GATE_PATH.read_text(encoding="utf-8"))
        payload = json.dumps(gate, sort_keys=True, separators=(",", ":"))
        if hashlib.sha256(payload.encode("utf-8")).hexdigest() != accepted_gate_sha256:
            raise ValueError("confirmatory accepted gate SHA-256 does not match the gate")
        source_identity = gate.get("source_identity")
        if not isinstance(source_identity, dict):
            raise ValueError("confirmatory gate is missing its source identity")
        source_revision = source_identity.get("git_revision")
        if not isinstance(source_revision, str):
            raise ValueError("confirmatory gate is missing its Git source revision")
        sentinel_run_dir = _find_accepted_sentinel_run(
            str(accepted_sentinel_manifest_sha256), source_revision
        )
        result = publish_confirmatory_experiment(
            config,
            operator_opt_in=operator_opt_in,
            operator_gate=gate,
            accepted_gate_sha256=str(accepted_gate_sha256),
            sentinel_run_dir=sentinel_run_dir,
            accepted_sentinel_manifest_sha256=str(
                accepted_sentinel_manifest_sha256
            ),
            staging_root=CONFIRMATORY_STAGING_ROOT / str(accepted_gate_sha256),
        )
        _print_result(result)
        return result
    if confirmatory_mode != "pilot":
        raise ValueError(
            "confirmatory MODE must be pilot, confirmatory_gate, or confirmatory_run"
        )

    control = _operator_control()
    mode = control["mode"]
    operator_opt_in = control["operator_opt_in"]
    accepted_gate_sha256 = control["accepted_gate_sha256"]
    if mode == "cuda_gate":
        compute = dict(COMPUTE)
        compute["backend"] = "cuda"
        compute["heavy_sweep_enabled"] = False
        config = ExperimentConfig.from_dicts(
            _sentinel_run(_current_git_revision()),
            THEORY,
            NUMERICS,
            OUTPUT,
            compute,
        )
        gate = build_cuda_gate_record(config, operator_opt_in=operator_opt_in)
        CUDA_GATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            gate, sort_keys=True, separators=(",", ":"), allow_nan=False
        )
        temporary = CUDA_GATE_PATH.with_suffix(CUDA_GATE_PATH.suffix + ".tmp")
        temporary.write_text(payload, encoding="utf-8")
        temporary.replace(CUDA_GATE_PATH)
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        print(f"cuda_gate_path={CUDA_GATE_PATH}")
        print(f"cuda_gate_sha256={digest}")
        print(f"processes_present={gate['processes_present']}")
        print("acceptance_required=set ACCEPTED_GATE_SHA256 to this exact digest")
        return gate

    compute = dict(COMPUTE)
    if mode == "cuda_sentinel":
        compute["backend"] = "cuda"
        compute["heavy_sweep_enabled"] = False
        if not accepted_gate_sha256:
            raise ValueError("cuda_sentinel requires an accepted gate SHA-256")
        gate = json.loads(CUDA_GATE_PATH.read_text(encoding="utf-8"))
        source_identity = gate.get("source_identity")
        if not isinstance(source_identity, dict):
            raise ValueError("cuda_sentinel gate is missing its source identity")
        config = ExperimentConfig.from_dicts(
            _sentinel_run(str(source_identity.get("git_revision"))),
            THEORY,
            NUMERICS,
            OUTPUT,
            compute,
        )
        result = publish_cuda_sentinel(
            config,
            operator_opt_in=operator_opt_in,
            operator_gate=gate,
            accepted_gate_sha256=accepted_gate_sha256,
            staging_root=SENTINEL_STAGING_ROOT / accepted_gate_sha256,
        )
        _print_result(result)
        return result
    if mode != "pilot":
        raise ValueError("MODE must be pilot, cuda_gate, or cuda_sentinel")

    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT, compute)
    result = run_gaussian_fixed_ray_experiment(config)
    _print_result(result)
    return result


if __name__ == "__main__":
    main()
