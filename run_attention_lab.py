"""Click-to-run marked-event attention lab; edit the dictionaries, then run."""

from __future__ import annotations

from pathlib import Path
import sys


_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.finite.attention_experiment import (
    AttentionExperimentResult,
    run_attention_experiment,
)


RUN = {
    "name": "attention_marked_event",
    "seed": 20260809,
}

THEORY = {
    "experiment": "attention_marked_event",
    "fixture": "nested_nonuniform_v1",
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


def main() -> AttentionExperimentResult:
    """Resolve the editable dictionaries and run one attention experiment."""
    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT)
    result = run_attention_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(
        f"status={result.status}; metrics={len(result.metrics)}; "
        f"figures={result.figure_status}"
    )
    return result


if __name__ == "__main__":
    main()
