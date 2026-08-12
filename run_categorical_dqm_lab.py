"""Click-to-run categorical-DQM lab; edit the dictionaries, then run."""

from __future__ import annotations

import math
from pathlib import Path
import sys


_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.finite.categorical_dqm_experiment import (
    CategoricalDqmExperimentResult,
    run_categorical_dqm_experiment,
)


RUN = {
    "name": "categorical_dqm",
    "seed": 20260809,
}

THEORY = {
    "experiment": "categorical_dqm",
    "fixture": "three_category_softmax_v1",
    "theta": [math.log(2.0), math.log(3.0)],
    "finite_difference_step": 1.0e-5,
    "dqm_step_sizes": [0.1, 0.05, 0.025, 0.0125],
}

NUMERICS = {
    "dtype": "float64",
    "atol": 1.0e-12,
    "rtol": 1.0e-10,
    "min_spd_rcond": 1.0e-12,
    "max_frame_condition": 1.0e6,
}

OUTPUT = {
    "root": "artifacts",
    "collect_diagnostics": True,
    "render_figures": True,
}


def main() -> CategoricalDqmExperimentResult:
    """Resolve the editable dictionaries and run one categorical-DQM experiment."""
    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT)
    result = run_categorical_dqm_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(
        f"status={result.status}; metrics={len(result.metrics)}; "
        f"figures={result.figure_status}"
    )
    return result


if __name__ == "__main__":
    main()
