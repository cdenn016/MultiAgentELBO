from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from multiagent_elbo.config import ExperimentConfig  # noqa: E402
from rg_v2.experiment import run_renormalization_v2_experiment  # noqa: E402


RUN = {"name": "renormalization-v2", "seed": 20260821}
THEORY = {
    "experiment": "renormalization_v2",
    "fixture": "lf3_product_v1",
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
    "root": "artifacts",
    "collect_diagnostics": True,
    "render_figures": False,
}


def main() -> object:
    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT)
    result = run_renormalization_v2_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(f"status={result.status}")
    return result


if __name__ == "__main__":
    main()
