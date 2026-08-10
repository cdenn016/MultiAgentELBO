"""Click-to-run finite graph-link holonomy lab; edit dictionaries, then run."""

from __future__ import annotations

from pathlib import Path
import sys


_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.geometry.holonomy_experiment import (
    HolonomyExperimentResult,
    run_holonomy_experiment,
)


RUN = {
    "name": "gauge_holonomy",
    "seed": 20260809,
}

THEORY = {
    "experiment": "gauge_holonomy",
    "fixture": "two_scale_application_v1",
    "scenario": "nonflat_plaquette",
    # Other controls: flat_tree, flat_cycle, frustrated_transport,
    # staged_aggregation.
    "group": "GL+(2)",
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
    "collect_diagnostics": False,
    "render_figures": False,
}


def main() -> HolonomyExperimentResult:
    """Resolve the editable dictionaries and run one finite holonomy scenario."""
    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT)
    result = run_holonomy_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(f"scenario={result.scenario}")
    print(
        f"status={result.status}; metrics={len(result.metrics)}; "
        "figures=not_exposed"
    )
    return result


if __name__ == "__main__":
    main()
