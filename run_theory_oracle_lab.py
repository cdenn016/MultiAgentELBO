"""Click-to-run exact theory-oracle lab; edit the dictionaries, then run."""

from __future__ import annotations

from pathlib import Path
import sys


_REPO_ROOT = Path(__file__).resolve().parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.finite.theory_oracle_experiment import (
    TheoryOracleExperimentResult,
    run_theory_oracle_experiment,
)


RUN = {
    "name": "theory_oracle",
    "seed": 20260809,
}

THEORY = {
    "experiment": "theory_oracle",
    "fixture": "two_scale_application_v1",
    "oracle_set": "core_identities",
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


def main(*, output_root: str | Path | None = None) -> TheoryOracleExperimentResult:
    """Resolve editable dictionaries and finalize one exact-oracle run."""
    output = dict(OUTPUT)
    if output_root is not None:
        output["root"] = output_root
    config = ExperimentConfig.from_dicts(
        RUN, THEORY, NUMERICS, output, COMPUTE
    )
    result = run_theory_oracle_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(
        f"status={result.status}; metrics={len(result.metrics)}; "
        f"figures={result.figure_status}"
    )
    return result


if __name__ == "__main__":
    main()
