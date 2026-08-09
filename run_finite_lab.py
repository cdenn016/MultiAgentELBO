"""Click-to-run exact finite laboratory; edit the dictionaries, then run this file."""

from __future__ import annotations

from pathlib import Path
import sys


_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.finite.experiment import FiniteExperimentResult, run_finite_experiment


RUN = {
    "name": "finite exact",
    "seed": 20260808,
}

THEORY = {
    "experiment": "finite_exact",
    "retained_interaction_order": 2,
}

NUMERICS = {
    "dtype": "float64",
    "atol": 1e-10,
    "rtol": 1e-9,
    "min_spd_rcond": 1e-12,
    "max_frame_condition": 1.0e6,
}

OUTPUT = {
    "root": "artifacts",
    "collect_diagnostics": True,
    "render_figures": False,
}


def main() -> FiniteExperimentResult:
    """Resolve the editable dictionaries and run one owned finite experiment."""
    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT)
    result = run_finite_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(f"status={result.status}; metrics={len(result.metrics)}")
    return result


if __name__ == "__main__":
    main()
