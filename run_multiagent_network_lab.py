"""Click-to-run four-agent network laboratory; edit the dictionaries, then run."""

from __future__ import annotations

from pathlib import Path
import sys


_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.finite.agent_network_experiment import (
    AgentNetworkExperimentResult,
    run_agent_network_experiment,
)


RUN = {
    "name": "multiagent network aligned",
    "seed": 20260809,
}

THEORY = {
    "experiment": "multiagent_network",
    "fixture": "two_scale_application_v1",
    "scenario": "aligned",  # aligned, frustrated, asymmetric_evidence, higher_order
    "arithmetic": "exact_rational",
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

COMPUTE = {
    "backend": "cpu",
    "dtype": "float64",
    "device_index": 0,
    "batch_size": 4096,
    "deterministic": True,
    "allow_tf32": False,
    "cpu_cuda_parity": True,
    "cuda_worker_python": r"C:\anaconda\python.exe",
    "heavy_sweep_enabled": False,
}


def main() -> AgentNetworkExperimentResult:
    """Resolve the editable dictionaries and run one exact application scenario."""
    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT, COMPUTE)
    result = run_agent_network_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(f"status={result.status}; metrics={len(result.metrics)}")
    return result


if __name__ == "__main__":
    main()
