"""Click Run to execute the preregistered non-heavy Gaussian fixed-ray pilot."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from multiagent_elbo.config import ExperimentConfig  # noqa: E402
from multiagent_elbo.realizations.gaussian.fixed_ray_experiment import (  # noqa: E402
    GaussianFixedRayExperimentResult,
    run_gaussian_fixed_ray_experiment,
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


def main() -> GaussianFixedRayExperimentResult:
    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT, COMPUTE)
    result = run_gaussian_fixed_ray_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(f"status={result.status}")
    for name, metric in sorted(result.metrics.items()):
        print(
            f"{name}: value={metric.value:.12g} tolerance={metric.tolerance:.3g} "
            f"status={metric.status} theorem_status={metric.theorem_status} "
            f"verification_state={metric.verification_state} claim_origin={metric.claim_origin}"
        )
    return result


if __name__ == "__main__":
    main()
