"""Click-to-run Gaussian laboratory; edit the dictionaries, then run this file."""

from __future__ import annotations

from pathlib import Path
import sys


_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.realizations.gaussian.experiment import (
    GaussianExperimentResult,
    run_gaussian_experiment,
)


RUN = {
    "name": "gaussian realization",
    "seed": 20260808,
}

THEORY = {
    "experiment": "gaussian_realization",
    "retained_interaction_order": None,
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


def main() -> GaussianExperimentResult:
    """Resolve the editable dictionaries and run one Gaussian experiment."""
    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT)
    result = run_gaussian_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(
        f"status={result.status}; metrics={len(result.metrics)}; "
        f"figures={result.figure_status}"
    )
    return result


if __name__ == "__main__":
    main()
