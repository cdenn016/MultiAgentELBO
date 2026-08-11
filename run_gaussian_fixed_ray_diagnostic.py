"""Click Run to publish the deterministic CPU fixed-ray diagnosis."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from multiagent_elbo.config import ExperimentConfig  # noqa: E402
from multiagent_elbo.realizations.gaussian.fixed_ray_diagnostic_experiment import (  # noqa: E402
    ConfirmatorySourceBinding,
    GaussianFixedRayDiagnosticResult,
    run_fixed_model_diagnostic,
)


RUN = {"name": "gaussian-fixed-ray-diagnostic", "seed": 20260809}
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
    "cpu_cuda_parity": False,
    "cuda_worker_python": r"C:\anaconda\python.exe",
    "heavy_sweep_enabled": False,
}
SOURCE = {"root": "docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49"}


def _current_git_revision() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    revision = completed.stdout.strip()
    if (
        completed.returncode != 0
        or len(revision) != 40
        or any(character not in "0123456789abcdef" for character in revision)
    ):
        raise RuntimeError("diagnostic launcher requires a full Git revision")
    return revision


def _source_directory() -> Path:
    if set(SOURCE) != {"root"}:
        raise ValueError("SOURCE must contain exactly the root entry")
    configured = SOURCE["root"]
    if not isinstance(configured, str) or not configured:
        raise ValueError("SOURCE root must be a nonempty path string")
    source_dir = Path(configured)
    if not source_dir.is_absolute():
        source_dir = ROOT / source_dir
    source_dir = source_dir.resolve()
    if not source_dir.is_dir():
        raise FileNotFoundError("fixed-model diagnostic source directory is missing")
    binding_path = source_dir / "source_binding.json"
    if not binding_path.is_file():
        raise FileNotFoundError("fixed-model diagnostic source binding is missing")
    return source_dir


def _require_cpu_only() -> None:
    if COMPUTE.get("backend") != "cpu":
        raise ValueError("fixed-model diagnostic launcher requires the CPU backend")
    if COMPUTE.get("heavy_sweep_enabled") is not False:
        raise ValueError("fixed-model diagnostic launcher prohibits heavy sweeps")


def main() -> GaussianFixedRayDiagnosticResult:
    _require_cpu_only()
    source_dir = _source_directory()
    revision = _current_git_revision()
    source_binding = ConfirmatorySourceBinding.from_path(
        source_dir / "source_binding.json",
        diagnostic_revision=revision,
    )
    config = ExperimentConfig.from_dicts(
        RUN,
        THEORY,
        NUMERICS,
        OUTPUT,
        COMPUTE,
    )
    result = run_fixed_model_diagnostic(config, source_binding, source_dir)
    print(f"run_dir={result.run_dir}")
    print(f"status={result.status}")
    print(f"source_binding_sha256={result.source_binding_sha256}")
    return result


if __name__ == "__main__":
    main()
