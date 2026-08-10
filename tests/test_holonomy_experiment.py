from __future__ import annotations

import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from dataclasses import replace

import numpy as np
from numpy.testing import assert_array_equal
import pytest

from multiagent_elbo.config import ExperimentConfig


ARTIFACT_STEMS = {
    "interaction_complex",
    "oriented_links",
    "vertex_frames",
    "cycle_holonomies",
    "operational_record_laws",
    "aggregation_stages",
}

METRIC_KEYS = {
    "passive_covariance_residual",
    "cycle_conjugacy_invariant_residual",
    "trivialization_residual",
    "operational_observable_residual",
    "broken_link_negative_control",
}

RUN_FILES = {
    "aggregation_stages.npz",
    "config.json",
    "cycle_holonomies.npz",
    "interaction_complex.json",
    "manifest.json",
    "metrics.json",
    "operational_record_laws.npz",
    "oriented_links.npz",
    "vertex_frames.npz",
}


def holonomy_config(
    root: Path,
    *,
    scenario: str = "nonflat_plaquette",
    seed: int = 20260809,
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "gauge_holonomy", "seed": seed},
        {
            "experiment": "gauge_holonomy",
            "fixture": "two_scale_application_v1",
            "scenario": scenario,
            "group": "GL+(2)",
        },
        {
            "dtype": "float64",
            "atol": 1.0e-12,
            "rtol": 1.0e-10,
            "min_spd_rcond": 1.0e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(root),
            "collect_diagnostics": False,
            "render_figures": False,
        },
    )


def test_default_nonflat_run_publishes_frozen_contract_and_literal_oracle(
    tmp_path: Path,
):
    """Mutation caught: omitting a frozen artifact/metric or reversing the cycle."""
    experiment = importlib.import_module(
        "multiagent_elbo.geometry.holonomy_experiment"
    )

    result = experiment.run_holonomy_experiment(holonomy_config(tmp_path))

    assert isinstance(result, experiment.HolonomyExperimentResult)
    assert result.status == "pass"
    assert result.scenario == "nonflat_plaquette"
    assert result.theorem_status == "NUMERICAL"
    assert result.verification_state == "CANDIDATE"
    assert result.claim_origin == "APPLICATION_SPECIFIC"
    assert set(result.metrics) == METRIC_KEYS
    assert all(metric.status == "pass" for metric in result.metrics.values())
    assert {
        path.stem for path in result.run_dir.iterdir() if path.stem in ARTIFACT_STEMS
    } == ARTIFACT_STEMS
    assert all(
        metric.verification_state == "CANDIDATE"
        for metric in result.metrics.values()
    )
    assert_array_equal(
        result.arrays["cycle_holonomies.original"],
        np.array([[[2.0, 2.0], [0.0, 1.0]]]),
    )
    assert_array_equal(
        result.arrays["cycle_holonomies.transformed"],
        np.array([[[2.0, 1.0], [0.0, 1.0]]]),
    )
    assert result.metrics["trivialization_residual"].value == 0.0
    assert result.metrics["broken_link_negative_control"].value > 1.0e-3


@pytest.mark.parametrize(
    ("scenario", "trivializable", "raw_trivialization"),
    [
        ("flat_tree", True, 0.0),
        ("flat_cycle", True, 0.0),
        ("nonflat_plaquette", False, 1.0),
        ("frustrated_transport", False, 1.0),
        ("staged_aggregation", False, 1.0),
    ],
)
def test_all_frozen_scenarios_publish_their_declared_finite_records(
    tmp_path: Path,
    scenario: str,
    trivializable: bool,
    raw_trivialization: float,
):
    """Mutation caught: routing a declared scenario through the wrong graph fixture."""
    experiment = importlib.import_module(
        "multiagent_elbo.geometry.holonomy_experiment"
    )

    result = experiment.run_holonomy_experiment(
        holonomy_config(tmp_path, scenario=scenario)
    )

    assert result.status == "pass"
    assert result.scenario == scenario
    assert {path.name for path in result.run_dir.iterdir()} == RUN_FILES
    record = json.loads(
        (result.run_dir / "interaction_complex.json").read_text("utf-8")
    )
    assert record["scenario"] == scenario
    assert record["application_id"] == (
        "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"
    )
    assert record["scope"] == {
        "base_connection_identification": False,
        "continuum_claim": False,
        "dynamical_symmetry_claim": False,
        "object": "finite_declared_graph_links",
        "physical_time_claim": False,
        "universality_claim": False,
    }
    assert bool(
        result.arrays["cycle_holonomies.is_trivializable"][0]
    ) is trivializable
    assert result.arrays[
        "cycle_holonomies.trivialization_max_edge_residual"
    ][0] == pytest.approx(raw_trivialization)


def test_frustrated_transport_has_a_normalized_path_dependent_observable(
    tmp_path: Path,
):
    """Mutation caught: calling link holonomy operational without normalized laws."""
    experiment = importlib.import_module(
        "multiagent_elbo.geometry.holonomy_experiment"
    )
    result = experiment.run_holonomy_experiment(
        holonomy_config(tmp_path, scenario="frustrated_transport")
    )

    short = result.arrays["operational_record_laws.frustrated_short_probabilities"]
    long = result.arrays["operational_record_laws.frustrated_long_probabilities"]
    assert short.sum() == pytest.approx(1.0)
    assert long.sum() == pytest.approx(1.0)
    assert_array_equal(short, [0.5, 0.5])
    assert_array_equal(
        result.arrays["operational_record_laws.frustrated_short_logits"],
        [0.0, 0.0],
    )
    assert_array_equal(
        result.arrays["operational_record_laws.frustrated_long_logits"],
        [0.0, 2.0],
    )
    assert long[1] - short[1] == pytest.approx(
        0.3807970779778823, abs=1.0e-15
    )


def test_staged_aggregation_records_finite_stages_and_matches_direct_total(
    tmp_path: Path,
):
    """Mutation caught: publishing only the final aggregate and losing its stages."""
    experiment = importlib.import_module(
        "multiagent_elbo.geometry.holonomy_experiment"
    )
    result = experiment.run_holonomy_experiment(
        holonomy_config(tmp_path, scenario="staged_aggregation")
    )

    assert_array_equal(
        result.arrays["aggregation_stages.agent_contributions"],
        [[1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [2.0, 0.0]],
    )
    assert_array_equal(
        result.arrays["aggregation_stages.block_contributions"],
        [[2.0, 1.0], [2.0, 1.0]],
    )
    assert_array_equal(
        result.arrays["aggregation_stages.direct_total"], [[4.0, 2.0]]
    )
    assert_array_equal(
        result.arrays["aggregation_stages.staged_total"], [[4.0, 2.0]]
    )


def test_runner_rejects_invalid_data_before_rng_provenance_or_run_store(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Mutation caught: creating runtime state before validating frozen inputs."""
    experiment = importlib.import_module(
        "multiagent_elbo.geometry.holonomy_experiment"
    )

    def forbidden(*_args, **_kwargs):
        raise AssertionError("runtime seam executed before validation")

    monkeypatch.setattr(experiment.RngStreams, "from_seed", forbidden)
    monkeypatch.setattr(experiment, "collect_provenance", forbidden)
    monkeypatch.setattr(experiment.RunStore, "create", forbidden)

    with pytest.raises(TypeError, match="ExperimentConfig"):
        experiment.run_holonomy_experiment({})

    wrong = ExperimentConfig.from_dicts(
        {"name": "wrong", "seed": 1},
        {"experiment": "finite_exact", "retained_interaction_order": 2},
        {
            "dtype": "float64",
            "atol": 1.0e-12,
            "rtol": 1.0e-10,
            "min_spd_rcond": 1.0e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(tmp_path),
            "collect_diagnostics": False,
            "render_figures": False,
        },
    )
    with pytest.raises(ValueError, match="gauge_holonomy"):
        experiment.run_holonomy_experiment(wrong)

    valid = holonomy_config(tmp_path)
    for field, value, message in (
        ("scenario", "invented", "scenario"),
        ("group", "GL(2)", "GL\\+"),
        ("fixture", "replacement", "frozen two-scale fixture"),
    ):
        forged = replace(valid, theory=replace(valid.theory, **{field: value}))
        with pytest.raises(ValueError, match=message):
            experiment.run_holonomy_experiment(forged)

    render_requested = replace(
        valid, output=replace(valid.output, render_figures=True)
    )
    with pytest.raises(ValueError, match="no figure renderer"):
        experiment.run_holonomy_experiment(render_requested)

    monkeypatch.setattr(
        experiment,
        "validate_two_scale_application_fixture",
        lambda _payload: (_ for _ in ()).throw(ValueError("invalid fixture math")),
    )
    with pytest.raises(ValueError, match="invalid fixture math"):
        experiment.run_holonomy_experiment(valid)
    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_same_seed_semantic_artifacts_replay_byte_identically_and_are_immutable(
    tmp_path: Path,
):
    """Mutation caught: using output-root state or mutable arrays in computation."""
    experiment = importlib.import_module(
        "multiagent_elbo.geometry.holonomy_experiment"
    )
    first = experiment.run_holonomy_experiment(
        holonomy_config(tmp_path / "first", scenario="staged_aggregation")
    )
    second = experiment.run_holonomy_experiment(
        holonomy_config(tmp_path / "second", scenario="staged_aggregation")
    )

    for filename in sorted(RUN_FILES - {"config.json", "manifest.json"}):
        assert (first.run_dir / filename).read_bytes() == (
            second.run_dir / filename
        ).read_bytes()
    assert set(first.arrays) == set(second.arrays)
    for name in first.arrays:
        assert_array_equal(first.arrays[name], second.arrays[name])
        assert not first.arrays[name].flags.writeable
    with pytest.raises(TypeError):
        first.arrays["new"] = np.zeros(1)
    with pytest.raises(ValueError):
        first.arrays["oriented_links.e01"][0, 0] = 2.0


def test_launcher_runs_without_arguments_pythonpath_or_editable_install(
    tmp_path: Path,
):
    """Mutation caught: relying on the caller's environment to import src layout."""
    launcher = Path(__file__).resolve().parents[1] / "run_gauge_holonomy_lab.py"
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in {"PYTHONPATH", "PYTHONHOME"} and not key.startswith("PYTEST_")
    }

    completed = subprocess.run(
        [sys.executable, str(launcher)],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )

    assert completed.returncode == 0, completed.stderr
    assert "scenario=nonflat_plaquette" in completed.stdout
    assert "status=pass; metrics=5; figures=not_exposed" in completed.stdout
    manifests = list((tmp_path / "artifacts").rglob("manifest.json"))
    assert len(manifests) == 1
    assert json.loads(manifests[0].read_text("utf-8"))["complete"] is True
