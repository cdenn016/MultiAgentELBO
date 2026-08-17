"""Click-to-run finite categorical falsification lab; edit dictionaries, then run."""

from __future__ import annotations

from pathlib import Path
import sys


_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.finite.categorical_falsification_experiment import (
    CategoricalFalsificationResult,
    run_categorical_falsification_experiment,
)


RUN = {
    "name": "categorical_falsification",
    "seed": 20260816,
}

THEORY = {
    "experiment": "categorical_falsification",
    "fixture": "two_channel_z3_v1",
    "admitted_family": "both",
    # Other settings: orbit excludes the uniform law so a nontrivial holonomy
    # empties the fixed sector; simplex admits it so the score stays finite.
    "null_control_seeds": 8,
    "descent_restarts": 200,
    "arithmetic": "exact_rational",
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


def main() -> CategoricalFalsificationResult:
    """Resolve the editable dictionaries and run one falsification sweep."""
    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT)
    result = run_categorical_falsification_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(f"admitted_family={result.admitted_family}")
    print(
        f"status={result.status}; metrics={len(result.metrics)}; "
        "figures=not_exposed"
    )
    for name in sorted(result.fired_falsifiers):
        print(f"falsifier_fired={name}")
    return result


if __name__ == "__main__":
    main()
