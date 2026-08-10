from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from multiagent_elbo.config import ExperimentConfig


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "two_scale_application_v1.json"
LAUNCHER_PATH = REPO_ROOT / "run_multiagent_network_lab.py"


def network_config(
    root: Path, *, scenario: str = "aligned", render_figures: bool = False
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": f"multiagent {scenario}", "seed": 20260809},
        {
            "experiment": "multiagent_network",
            "fixture": "two_scale_application_v1",
            "scenario": scenario,
            "arithmetic": "exact_rational",
        },
        {
            "dtype": "float64",
            "atol": 1e-12,
            "rtol": 1e-10,
            "min_spd_rcond": 1e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": root,
            "collect_diagnostics": True,
            "render_figures": render_figures,
        },
    )


def test_run_publishes_frozen_inventory_with_orthogonal_claim_fields(
    tmp_path: Path,
) -> None:
    """Catches missing contract artifacts or metric metadata collapsed into status."""
    from multiagent_elbo.finite.agent_network_experiment import (
        run_agent_network_experiment,
    )

    result = run_agent_network_experiment(
        network_config(tmp_path), fixture_path=FIXTURE_PATH
    )

    assert result.status == "pass"
    assert tuple(result.metrics) == (
        "elbo_gap_residual",
        "evidence_residual",
        "hoeffding_reconstruction_residual",
        "local_collective_residual",
        "pairwise_retained_residual",
        "recognition_lift_residual",
    )
    assert all(metric.status == "pass" for metric in result.metrics.values())
    assert all(
        metric.verification_state == "CANDIDATE"
        for metric in result.metrics.values()
    )
    assert result.metrics["recognition_lift_residual"].theorem_status == "HYPOTHESIS"
    assert result.metrics["recognition_lift_residual"].claim_origin == (
        "APPLICATION_SPECIFIC"
    )
    assert result.metrics["evidence_residual"].theorem_status == "ESTABLISHED"

    required_arrays = {
        "fine_law",
        "coarse_law",
        "fine_to_coarse_channel",
        "hoeffding_interactions",
        "local_collective_differences",
        "configuration_scale_map",
    }
    assert required_arrays <= result.arrays.keys()
    assert np.array_equal(result.arrays["fine_law_numerators"][:4], [12, 1, 1, 3])
    assert np.array_equal(result.arrays["fine_law_denominators"][:4], [91] * 4)
    assert np.max(np.abs(result.arrays["local_collective_differences"][:, 2])) < 1e-15
    assert result.arrays["hoeffding_interactions"].shape == (16, 16)
    assert all(not array.flags.writeable for array in result.arrays.values())

    manifest = json.loads((result.run_dir / "manifest.json").read_text("utf-8"))
    claims = json.loads((result.run_dir / "claims.json").read_text("utf-8"))
    assert manifest["complete"] is True
    assert manifest["provenance"]["application_id"] == (
        "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"
    )
    assert manifest["provenance"]["arithmetic"] == "exact_rational_inputs"
    assert manifest["provenance"]["performance_record"]["scope"] == (
        "validated_scientific_evaluation"
    )
    assert manifest["provenance"]["performance_record"]["runtime_seconds"] > 0.0
    assert manifest["provenance"]["performance_record"]["tracemalloc_peak_bytes"] > 0
    assert claims["fixed_channel_premise"]["verification_state"] == "CANDIDATE"


@pytest.mark.parametrize(
    ("scenario", "expected_pairwise_residual"),
    (
        ("aligned", 0.0),
        ("frustrated", 0.0),
        ("asymmetric_evidence", 0.0),
        ("higher_order", 1.0),
    ),
)
def test_all_declared_scenarios_pass_the_same_frozen_contract(
    tmp_path: Path, scenario: str, expected_pairwise_residual: float
) -> None:
    """Catches scenario-specific schema drift or loss of the higher-order control."""
    from multiagent_elbo.finite.agent_network_experiment import (
        run_agent_network_experiment,
    )

    result = run_agent_network_experiment(
        network_config(tmp_path / scenario, scenario=scenario),
        fixture_path=FIXTURE_PATH,
    )

    assert result.status == "pass"
    assert result.metrics["pairwise_retained_residual"].value == (
        expected_pairwise_residual
    )


def test_same_seed_semantic_artifacts_are_deterministic_across_output_roots(
    tmp_path: Path,
) -> None:
    """Catches hidden ambient randomness or output-root-dependent scientific data."""
    from multiagent_elbo.finite.agent_network_experiment import (
        run_agent_network_experiment,
    )

    first = run_agent_network_experiment(
        network_config(tmp_path / "first"), fixture_path=FIXTURE_PATH
    )
    second = run_agent_network_experiment(
        network_config(tmp_path / "second"), fixture_path=FIXTURE_PATH
    )

    assert (first.run_dir / "metrics.json").read_bytes() == (
        second.run_dir / "metrics.json"
    ).read_bytes()
    assert (first.run_dir / "claims.json").read_bytes() == (
        second.run_dir / "claims.json"
    ).read_bytes()
    assert (first.run_dir / "arrays.npz").read_bytes() == (
        second.run_dir / "arrays.npz"
    ).read_bytes()


def test_fixture_and_figure_validation_precede_rng_and_artifact_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Catches partial publication or RNG use before input validation finishes."""
    from multiagent_elbo.experiment_support import fixture_application_id
    import multiagent_elbo.finite.agent_network_experiment as experiment

    def forbidden(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("RNG or artifact creation occurred before validation")

    monkeypatch.setattr(experiment.RngStreams, "from_seed", forbidden)
    monkeypatch.setattr(experiment.RunStore, "create", forbidden)

    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    payload["channel"]["arrows"][0]["rows"][0][0] = "1/2"
    payload["application_id"] = fixture_application_id(payload)
    invalid_fixture = tmp_path / "invalid.json"
    invalid_fixture.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="channel row 0 is not normalized"):
        experiment.run_agent_network_experiment(
            network_config(tmp_path / "invalid"), fixture_path=invalid_fixture
        )
    with pytest.raises(ValueError, match="deferred to serial integration"):
        experiment.run_agent_network_experiment(
            network_config(tmp_path / "figures", render_figures=True),
            fixture_path=FIXTURE_PATH,
        )
    assert not (tmp_path / "invalid").exists()
    assert not (tmp_path / "figures").exists()


def test_click_to_run_launcher_needs_no_arguments_install_or_pythonpath(
    tmp_path: Path,
) -> None:
    """Catches CLI coupling or reliance on an editable package installation."""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = ""

    completed = subprocess.run(
        [sys.executable, str(LAUNCHER_PATH)],
        cwd=tmp_path,
        env=environment,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "status=pass" in completed.stdout
    manifests = list((tmp_path / "artifacts").rglob("manifest.json"))
    assert len(manifests) == 1
    assert json.loads(manifests[0].read_text("utf-8"))["complete"] is True


def test_provenance_dirty_digest_uses_the_declared_length_framing(tmp_path: Path) -> None:
    """Catches a digest whose bytes disagree with its recorded format identifier."""
    from multiagent_elbo.finite.agent_network_experiment import (
        run_agent_network_experiment,
    )

    result = run_agent_network_experiment(
        network_config(tmp_path), fixture_path=FIXTURE_PATH
    )
    provenance = json.loads((result.run_dir / "manifest.json").read_text("utf-8"))[
        "provenance"
    ]

    def git_bytes(*args: str) -> bytes:
        completed = subprocess.run(
            [
                "git",
                "-c",
                f"safe.directory={REPO_ROOT.as_posix()}",
                "-C",
                str(REPO_ROOT),
                *args,
            ],
            capture_output=True,
            check=True,
        )
        return completed.stdout

    def frame(digest: object, label: bytes, payload: bytes) -> None:
        digest.update(len(label).to_bytes(8, "big"))
        digest.update(label)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)

    digest = hashlib.sha256()
    frame(digest, b"tracked-diff", git_bytes("diff", "--binary", "--no-ext-diff", "HEAD", "--"))
    untracked = git_bytes("ls-files", "--others", "--exclude-standard", "-z")
    for raw_path in sorted(path for path in untracked.split(b"\0") if path):
        relative = Path(os.fsdecode(raw_path))
        frame(digest, b"untracked-path", raw_path)
        frame(
            digest,
            b"untracked-content-sha256",
            hashlib.sha256((REPO_ROOT / relative).read_bytes()).digest(),
        )

    assert provenance["dirty_tree_format"] == (
        "git-diff-binary-head-plus-sorted-untracked-path-content-v1"
    )
    assert provenance["dirty_tree_sha256"] == digest.hexdigest()
