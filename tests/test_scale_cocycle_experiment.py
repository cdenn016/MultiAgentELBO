from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import numpy as np
import pytest

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.finite.scale_cocycle_experiment import (
    ScaleCocycleExperimentResult,
    run_scale_cocycle_experiment,
)


def scale_config(root: Path, *, name: str = "scale cocycle") -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": name, "seed": 20260809},
        {
            "experiment": "scale_cocycle",
            "fixture": "two_scale_application_v1",
            "extension": "three_level_composition_v1",
            "retained_interaction_order": 2,
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
            "root": str(root),
            "collect_diagnostics": True,
            "render_figures": False,
        },
    )


def test_scale_experiment_publishes_recomputable_exact_extension_and_canonical_metrics(
    tmp_path: Path,
):
    result = run_scale_cocycle_experiment(scale_config(tmp_path))

    assert isinstance(result, ScaleCocycleExperimentResult)
    assert result.status == "pass"
    required_artifacts = {
        "three_level_extension.json",
        "composed_channels.json",
        "coarse_actions.json",
        "posterior_bridges.json",
        "comparison_isomorphisms.json",
        "derivative_cocycle.json",
        "retained_projection_residual.json",
        "metrics.json",
        "arrays.npz",
    }
    assert required_artifacts <= {path.name for path in result.run_dir.iterdir()}
    extension = json.loads(
        (result.run_dir / "three_level_extension.json").read_text(encoding="utf-8")
    )
    assert extension["schema_version"] == "three-level-composition-v1"
    assert extension["base_application_id"] == (
        "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"
    )
    assert extension["fine_to_macro_rows"][0] == ["59/96", "37/96"]
    assert extension["fixture_mutated"] is False

    required_metrics = {
        "direct_staged_pushforward_residual",
        "cocycle_composition_residual",
        "retained_beta_residual",
        "full_interaction_reconstruction_residual",
        "wrong_order_negative_control",
        "projection_nonintertwining_control",
        "pairwise_truncation_control",
    }
    assert required_metrics <= set(result.metrics)
    assert all(result.metrics[name].status == "pass" for name in required_metrics)
    assert all(result.metrics[name].theorem_status.isupper() for name in result.metrics)
    assert all(
        result.metrics[name].verification_state == "EVIDENCE_VERIFIED"
        for name in result.metrics
    )
    assert all(result.metrics[name].claim_origin in {"PROJECT_NOVEL", "APPLICATION_SPECIFIC"} for name in result.metrics)
    assert result.metrics["retained_beta_residual"].value == pytest.approx(2.0)
    assert "magnitude" in result.metrics["retained_beta_residual"].interpretation
    assert result.metrics["retained_beta_residual_signed_min"].value == pytest.approx(0.0)
    assert result.metrics["retained_beta_residual_signed_max"].value == pytest.approx(2.0)
    assert result.metrics["wrong_order_negative_control"].value == pytest.approx(1.0)
    assert result.metrics["projection_nonintertwining_control"].value == pytest.approx(1.0)
    assert result.metrics["generated_higher_order_coefficient"].value == pytest.approx(
        -0.32394711573301693
    )
    assert result.metrics["pairwise_truncation_control"].value == pytest.approx(
        0.32394711573301693
    )

    assert set(result.arrays) >= {
        "channel_fine_to_middle",
        "channel_middle_to_macro",
        "channel_fine_to_macro",
        "reference_direct",
        "reference_staged",
        "evidence_direct",
        "evidence_staged",
        "posterior_direct",
        "posterior_staged",
        "recognition_direct",
        "recognition_staged",
        "action_direct",
        "action_staged",
        "reverse_bridge_direct",
        "reverse_bridge_staged",
        "identified_step",
        "derivative_cocycle",
        "fine_pairwise_action",
        "coarse_generated_action",
        "coarse_generated_likelihood",
        "coarse_mobius_triple_component",
        "retained_beta_exact",
        "retained_beta_retained",
        "retained_beta_residual_difference",
        "retained_beta_residual_identified",
        "retained_beta_residual_native",
        "full_action",
        "full_action_reconstruction",
        "pairwise_action_reconstruction",
    }
    np.testing.assert_allclose(
        result.arrays["retained_beta_residual_difference"],
        result.arrays["retained_beta_residual_identified"],
    )
    np.testing.assert_allclose(
        result.arrays["retained_beta_residual_difference"],
        result.arrays["retained_beta_residual_native"],
    )
    derivative = json.loads(
        (result.run_dir / "derivative_cocycle.json").read_text(encoding="utf-8")
    )
    assert derivative["ordered_nonautonomous"] is True
    assert derivative["factors"][0]["source_level"] == "level-0"
    assert derivative["factors"][1]["target_level"] == "level-2"
    assert derivative["composite"]["source_type"] == "interaction-tangent-0"
    assert derivative["composite"]["target_type"] == "interaction-tangent-2"

    coarse = json.loads(
        (result.run_dir / "coarse_actions.json").read_text(encoding="utf-8")
    )
    assert coarse["fine_action_maximum_order"] == 2
    assert coarse["coarse_triple_log_ratio"] == "103823/143543"
    assert coarse["generated_triple_component"] == pytest.approx(
        -0.32394711573301693
    )


def test_scale_experiment_is_same_seed_deterministic_across_output_roots(tmp_path: Path):
    first = run_scale_cocycle_experiment(scale_config(tmp_path / "a", name="same"))
    second = run_scale_cocycle_experiment(scale_config(tmp_path / "b", name="same"))

    assert first.metrics == second.metrics
    assert first.arrays.keys() == second.arrays.keys()
    for name in first.arrays:
        np.testing.assert_array_equal(first.arrays[name], second.arrays[name])


def test_fixture_validation_precedes_rng_and_artifact_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    invalid_fixture = tmp_path / "invalid.json"
    invalid_fixture.write_text("{}", encoding="utf-8")
    output_root = tmp_path / "output"

    def forbidden_rng(*_: object, **__: object) -> object:
        raise AssertionError("RNG constructed before fixture validation")

    monkeypatch.setattr(
        "multiagent_elbo.finite.scale_cocycle_experiment.RngStreams.from_seed",
        forbidden_rng,
    )
    with pytest.raises(ValueError, match="fixture"):
        run_scale_cocycle_experiment(
            scale_config(output_root), fixture_path=invalid_fixture
        )
    assert not output_root.exists()


def test_scale_launcher_is_click_to_run_from_a_fresh_uninstalled_checkout(
    tmp_path: Path,
):
    repository = Path(__file__).resolve().parents[1]
    checkout = tmp_path / "fresh-checkout"
    checkout.mkdir()
    shutil.copy2(repository / "run_scale_cocycle_lab.py", checkout / "run_scale_cocycle_lab.py")
    shutil.copytree(repository / "src", checkout / "src")
    shutil.copytree(repository / "Theory", checkout / "Theory")
    (checkout / "tests" / "fixtures").mkdir(parents=True)
    shutil.copy2(
        repository / "tests" / "fixtures" / "two_scale_application_v1.json",
        checkout / "tests" / "fixtures" / "two_scale_application_v1.json",
    )
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in {"PYTHONPATH", "PYTHONHOME"} and not key.startswith("PYTEST_")
    }

    completed = subprocess.run(
        [sys.executable, "run_scale_cocycle_lab.py"],
        cwd=checkout,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "run_dir=" in completed.stdout
    assert "status=pass" in completed.stdout
    source = (checkout / "run_scale_cocycle_lab.py").read_text(encoding="utf-8")
    assert "import argparse" not in source
    assert "from click" not in source.lower()
    assert "import typer" not in source.lower()
