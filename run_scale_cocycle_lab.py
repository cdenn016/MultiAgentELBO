"""Click Run to execute the exact finite scale-cocycle laboratory."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from multiagent_elbo.config import ExperimentConfig  # noqa: E402
from multiagent_elbo.finite.scale_cocycle_experiment import (  # noqa: E402
    run_scale_cocycle_experiment,
)


RUN = {"name": "scale-cocycle", "seed": 20260809}
THEORY = {
    "experiment": "scale_cocycle",
    "fixture": "two_scale_application_v1",
    "extension": "three_level_composition_v1",
    "retained_interaction_order": 2,
    "arithmetic": "exact_rational",
}
NUMERICS = {
    "dtype": "float64",
    "atol": 1e-12,
    "rtol": 1e-10,
    "min_spd_rcond": 1e-12,
    "max_frame_condition": 1.0e6,
}
OUTPUT = {
    "root": str(ROOT / "artifacts" / "scale-cocycle"),
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


def main() -> None:
    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT, COMPUTE)
    result = run_scale_cocycle_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(f"status={result.status}")
    for name, metric in sorted(result.metrics.items()):
        print(
            f"{name}: value={metric.value:.12g} tolerance={metric.tolerance:.3g} "
            f"status={metric.status} theorem_status={metric.theorem_status} "
            f"verification_state={metric.verification_state} claim_origin={metric.claim_origin}"
        )


if __name__ == "__main__":
    main()
