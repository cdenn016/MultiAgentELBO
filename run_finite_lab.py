"""Click-to-run exact finite laboratory; edit the dictionaries, then run this file."""

from __future__ import annotations

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
