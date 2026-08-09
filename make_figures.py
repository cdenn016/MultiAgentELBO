"""Click-to-run pure figure replay; edit REPLAY, then run this file."""

from __future__ import annotations

from pathlib import Path
import sys


_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from multiagent_elbo.figures import FigureManifest, render_run


REPLAY = {
    "run_dir": "artifacts/finite-exact/example-run",
    "output_dir": "artifacts/finite-exact/figures/example-run",
    "requested": ("finite_identity",),
}


def main() -> FigureManifest:
    """Render the editable request from finalized saved artifacts only."""
    result = render_run(
        Path(REPLAY["run_dir"]),
        Path(REPLAY["output_dir"]),
        requested=REPLAY["requested"],
    )
    print(f"figure_dir={result.output_dir}")
    print(f"status={result.status}; figures={len(result.figures)}")
    return result


if __name__ == "__main__":
    main()
