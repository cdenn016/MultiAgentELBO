from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json
import math
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
        result.metrics[name].verification_state == "CANDIDATE"
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


def test_retained_projection_artifact_independently_reconstructs_beta_outputs(
    tmp_path: Path,
):
    result = run_scale_cocycle_experiment(scale_config(tmp_path))
    artifact = json.loads(
        (result.run_dir / "retained_projection_residual.json").read_text(
            encoding="utf-8"
        )
    )

    def vector(values: list[str]) -> tuple[Fraction, ...]:
        return tuple(Fraction(value) for value in values)

    def matrix(values: list[list[str]]) -> tuple[tuple[Fraction, ...], ...]:
        return tuple(vector(row) for row in values)

    def matvec(
        values: tuple[tuple[Fraction, ...], ...],
        operand: tuple[Fraction, ...],
    ) -> tuple[Fraction, ...]:
        return tuple(
            sum((entry * value for entry, value in zip(row, operand)), Fraction(0))
            for row in values
        )

    def matmul(
        left: tuple[tuple[Fraction, ...], ...],
        right: tuple[tuple[Fraction, ...], ...],
    ) -> tuple[tuple[Fraction, ...], ...]:
        columns = tuple(zip(*right))
        return tuple(
            tuple(
                sum((entry * value for entry, value in zip(row, column)), Fraction(0))
                for column in columns
            )
            for row in left
        )

    source_identification = matrix(artifact["source_identification"]["matrix"])
    source_inverse = matrix(artifact["source_identification"]["inverse"])
    target_identification = matrix(artifact["target_identification"]["matrix"])
    target_inverse = matrix(artifact["target_identification"]["inverse"])
    source_projection = matrix(artifact["source_projection"])
    target_projection = matrix(artifact["target_projection"])
    exact_step = matrix(artifact["exact_step"])
    reference_input = vector(artifact["reference_input"])
    delta_log_scale = Fraction(artifact["delta_log_scale"])

    assert artifact["schema_version"] == "scale-retained-projection-residual-v2"
    assert artifact["source_identification"]["native_type"] == "interaction-native"
    assert artifact["target_identification"]["reference_type"] == (
        "interaction-reference"
    )
    source_reference_projection = matmul(
        source_identification, matmul(source_projection, source_inverse)
    )
    assert matvec(source_reference_projection, reference_input) == reference_input
    native_input = matvec(source_inverse, reference_input)
    native_output = matvec(exact_step, native_input)
    exact_output = matvec(target_identification, native_output)
    target_reference_projection = matmul(
        target_identification, matmul(target_projection, target_inverse)
    )
    retained_output = matvec(target_reference_projection, exact_output)
    exact_beta = tuple(
        (output - reference) / delta_log_scale
        for output, reference in zip(exact_output, reference_input)
    )
    retained_beta = tuple(
        (output - reference) / delta_log_scale
        for output, reference in zip(retained_output, reference_input)
    )
    signed_residual = tuple(
        exact - retained for exact, retained in zip(exact_beta, retained_beta)
    )
    dimension = len(reference_input)
    identity = tuple(
        tuple(Fraction(int(row == column)) for column in range(dimension))
        for row in range(dimension)
    )
    omitted_reference = tuple(
        tuple(base - projected for base, projected in zip(base_row, projected_row))
        for base_row, projected_row in zip(identity, target_reference_projection)
    )
    signed_residual_identified = tuple(
        value / delta_log_scale
        for value in matvec(omitted_reference, exact_output)
    )
    omitted_native = tuple(
        tuple(base - projected for base, projected in zip(base_row, projected_row))
        for base_row, projected_row in zip(identity, target_projection)
    )
    signed_residual_native = tuple(
        value / delta_log_scale
        for value in matvec(
            target_identification, matvec(omitted_native, native_output)
        )
    )

    assert exact_beta == vector(artifact["exact_beta"])
    assert retained_beta == vector(artifact["retained_beta"])
    assert signed_residual == vector(artifact["signed_residual_difference"])
    assert signed_residual_identified == vector(
        artifact["signed_residual_identified"]
    )
    assert signed_residual_native == vector(artifact["signed_residual_native"])
    assert max(abs(value) for value in exact_beta) == Fraction(
        artifact["exact_beta_linf_norm"]
    )
    assert max(abs(value) for value in retained_beta) == Fraction(
        artifact["retained_beta_linf_norm"]
    )
    assert max(abs(value) for value in signed_residual) == Fraction(
        artifact["signed_residual_linf_norm"]
    )


def test_coarse_action_artifact_independently_reconstructs_all_mobius_components(
    tmp_path: Path,
):
    result = run_scale_cocycle_experiment(scale_config(tmp_path))
    artifact = json.loads(
        (result.run_dir / "coarse_actions.json").read_text(encoding="utf-8")
    )
    states = tuple(tuple(int(bit) for bit in label) for label in artifact["fine_state_labels"])
    state_index = {state: index for index, state in enumerate(states)}
    reference = tuple(Fraction(value) for value in artifact["fine_reference"])
    likelihood = tuple(Fraction(value) for value in artifact["fine_likelihood"])
    evidence = tuple(base * density for base, density in zip(reference, likelihood))
    channel = tuple(
        tuple(Fraction(value) for value in row)
        for row in artifact["coarse_channel_rows"]
    )
    coarse_reference = tuple(
        sum((reference[row] * channel[row][column] for row in range(len(states))), Fraction(0))
        for column in range(len(states))
    )
    coarse_evidence = tuple(
        sum((evidence[row] * channel[row][column] for row in range(len(states))), Fraction(0))
        for column in range(len(states))
    )
    coarse_action = tuple(
        -math.log(float(numerator / denominator))
        for numerator, denominator in zip(coarse_evidence, coarse_reference)
    )

    anchor = (0, 0, 0)
    anchor_value = coarse_action[state_index[anchor]]
    components: dict[tuple[int, ...], dict[tuple[int, ...], float]] = {}
    for size in range(1, 4):
        for subset in combinations(range(3), size):
            table: dict[tuple[int, ...], float] = {}
            for assignment in (
                tuple((mask >> position) & 1 for position in range(size))
                for mask in range(2**size)
            ):
                value = 0.0
                for active_size in range(size + 1):
                    for active_positions in combinations(range(size), active_size):
                        state = list(anchor)
                        for position in active_positions:
                            state[subset[position]] = assignment[position]
                        value += (-1) ** (size - active_size) * coarse_action[
                            state_index[tuple(state)]
                        ]
                table[assignment] = value
            components[subset] = table

    emitted = {
        tuple(record["subset"]): {
            tuple(entry["state"]): entry["value"] for entry in record["table"]
        }
        for record in artifact["coarse_mobius_nonempty_components"]
    }
    assert set(emitted) == set(components)
    assert artifact["coarse_mobius_anchor_component"] == pytest.approx(anchor_value)
    for subset, table in components.items():
        assert emitted[subset] == pytest.approx(table, abs=2.0e-15)

    reconstruction = tuple(
        anchor_value
        + sum(
            table[tuple(state[index] for index in subset)]
            for subset, table in components.items()
        )
        for state in states
    )
    np.testing.assert_allclose(
        reconstruction,
        artifact["full_reconstruction"],
        rtol=0.0,
        atol=2.0e-15,
    )
    np.testing.assert_allclose(
        reconstruction,
        coarse_action,
        rtol=0.0,
        atol=2.0e-15,
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
