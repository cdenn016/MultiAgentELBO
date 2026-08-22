from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from multiagent_elbo.config import ExperimentConfig  # noqa: E402
from rg_v2.recursive_experiment import (  # noqa: E402
    run_renormalization_v2_recursive_experiment,
)


RUN = {"name": "renormalization-v2-recursive", "seed": 20260821}
THEORY = {
    "experiment": "renormalization_v2_recursive",
    "fixture": "lf4_two_parent_recursive_v1",
    "arithmetic": "exact_rational",
}
NUMERICS = {
    "dtype": "float64",
    "atol": 1.0e-12,
    "rtol": 1.0e-12,
    "min_spd_rcond": 1.0e-12,
    "max_frame_condition": 1.0e12,
}
OUTPUT = {
    "root": "artifacts/renormalization-v2-recursive",
    "collect_diagnostics": True,
    "render_figures": False,
}


def main() -> object:
    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT)
    result = run_renormalization_v2_recursive_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(f"status={result.status}")
    return result


if __name__ == "__main__":
    main()
