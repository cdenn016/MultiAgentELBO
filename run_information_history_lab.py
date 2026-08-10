"""Click-to-run information-history lab; edit the dictionaries, then run."""

from __future__ import annotations

from pathlib import Path
import sys


_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.finite.information_history_experiment import (
    InformationHistoryExperimentResult,
    run_information_history_experiment,
)


RUN = {
    "name": "information_history",
    "seed": 20260809,
}

THEORY = {
    "experiment": "information_history",
    "fixture": "two_scale_application_v1",
    "family": "categorical_softmax",
    "history_steps": 16,
    "step_size": 0.05,
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
    "render_figures": False,
}


def main() -> InformationHistoryExperimentResult:
    """Resolve the editable dictionaries and run one information-history experiment."""
    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT)
    result = run_information_history_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(f"status={result.status}; metrics={len(result.metrics)}")
    return result


if __name__ == "__main__":
    main()
