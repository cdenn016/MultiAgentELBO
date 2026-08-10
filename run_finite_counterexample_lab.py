"""Click-to-run finite counterexample lab; edit the dictionaries, then run."""
from __future__ import annotations
from pathlib import Path
import sys

_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.finite.counterexample_experiment import FiniteCounterexampleExperimentResult, run_finite_counterexample_experiment

RUN = {"name": "finite_counterexample", "seed": 20260809}
THEORY = {"experiment": "finite_counterexample", "fixture": "counterexample_catalog_v1", "max_states": 4, "max_denominator": 8, "arithmetic": "exact_rational"}
NUMERICS = {"dtype": "float64", "atol": 1.0e-12, "rtol": 1.0e-10, "min_spd_rcond": 1.0e-12, "max_frame_condition": 1.0e6}
OUTPUT = {"root": "artifacts", "collect_diagnostics": True, "render_figures": False}

def main() -> FiniteCounterexampleExperimentResult:
    result = run_finite_counterexample_experiment(ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT))
    print(f"run_dir={result.run_dir}")
    print(f"status={result.status}; metrics={len(result.metrics)}; figures={result.figure_status}")
    return result

if __name__ == "__main__":
    main()
