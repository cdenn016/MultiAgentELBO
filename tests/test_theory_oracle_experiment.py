from __future__ import annotations

from dataclasses import replace
from dataclasses import FrozenInstanceError
from dataclasses import asdict
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess

import pytest
import numpy as np

from multiagent_elbo.config import ExperimentConfig


RUN = {"name": "theory oracle test", "seed": 20260809}
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


def _config(
    root: Path,
    *,
    diagnostics: bool = True,
    figures: bool = False,
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        RUN,
        THEORY,
        NUMERICS,
        {
            "root": root,
            "collect_diagnostics": diagnostics,
            "render_figures": figures,
        },
        COMPUTE,
    )


def test_runner_rejects_wrong_object_before_publication(tmp_path: Path):
    """Mutation caught: removing the public runner's config type guard."""
    from multiagent_elbo.finite.theory_oracle_experiment import (
        run_theory_oracle_experiment,
    )

    with pytest.raises(TypeError, match="config must be an ExperimentConfig"):
        run_theory_oracle_experiment({"output": {"root": tmp_path}})  # type: ignore[arg-type]

    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        ("discriminator", "requires theory.experiment='theory_oracle'"),
        ("backend", "CPU-only"),
        ("compute_dtype", "compute dtype must be 'float64'"),
        ("numerics_dtype", "numerics dtype must be 'float64'"),
        ("figures", "figures are not exposed"),
    ),
)
def test_runner_rejects_policy_mutations_before_publication(
    tmp_path: Path,
    mutation: str,
    message: str,
    monkeypatch: pytest.MonkeyPatch,
):
    """Mutation caught: moving policy checks after run-directory creation."""
    import multiagent_elbo.finite.theory_oracle_experiment as experiment_module

    def unreachable(*args: object, **kwargs: object) -> object:
        raise AssertionError("validation reached a forbidden runtime seam")

    monkeypatch.setattr(experiment_module.RngStreams, "from_seed", unreachable)
    monkeypatch.setattr(experiment_module, "collect_provenance", unreachable)
    monkeypatch.setattr(experiment_module.RunStore, "create", unreachable)

    config = _config(tmp_path / "runs")
    if mutation == "discriminator":
        config = ExperimentConfig.from_dicts(
            RUN,
            {"experiment": "finite_exact", "retained_interaction_order": 2},
            NUMERICS,
            {
                "root": tmp_path / "runs",
                "collect_diagnostics": True,
                "render_figures": False,
            },
        )
    elif mutation == "backend":
        config = replace(config, compute=replace(config.compute, backend="cuda"))
    elif mutation == "compute_dtype":
        config = replace(config, compute=replace(config.compute, dtype="float32"))
    elif mutation == "numerics_dtype":
        config = replace(config, numerics=replace(config.numerics, dtype="float32"))
    elif mutation == "figures":
        config = replace(config, output=replace(config.output, render_figures=True))

    with pytest.raises(ValueError, match=message):
        experiment_module.run_theory_oracle_experiment(config)

    assert not (tmp_path / "runs").exists()


METRIC_KEYS = {
    "elbo_oracle_residual",
    "fisher_defect_oracle_residual",
    "marked_event_associativity_residual",
    "hoeffding_oracle_residual",
    "gaussian_linear_algebra_oracle_residual",
}


def test_run_publishes_exact_contract_and_returns_immutable_result(tmp_path: Path):
    """Mutation caught: dropping an oracle, artifact, claim field, or immutability guard."""
    from multiagent_elbo.finite.theory_oracle_experiment import (
        TheoryOracleExperimentResult,
        run_theory_oracle_experiment,
    )

    result = run_theory_oracle_experiment(_config(tmp_path / "runs"))

    assert isinstance(result, TheoryOracleExperimentResult)
    assert result.status == "pass"
    assert result.figure_status == "not_exposed"
    assert set(result.metrics) == METRIC_KEYS
    for metric in result.metrics.values():
        assert metric.status == "pass"
        assert metric.assessment_scope == "implementation_check"
        assert metric.theorem_status == "ESTABLISHED"
        assert metric.verification_state == "EVIDENCE_VERIFIED"
        assert metric.claim_origin == "PROJECT_NOVEL"

    expected_artifacts = {
        "config.json",
        "manifest.json",
        "metrics.json",
        "arrays.npz",
        "diagnostics.npz",
        "exact_numerators.json",
        "exact_denominators.json",
        "theorem_assumption_matrix.json",
        "literal_commuting_diagrams.json",
    }
    assert {path.name for path in result.run_dir.iterdir()} == expected_artifacts
    manifest = json.loads((result.run_dir / "manifest.json").read_text("utf-8"))
    assert manifest["complete"] is True
    assert set(manifest["artifacts"]) == expected_artifacts

    fixture_path = Path(__file__).parent / "fixtures" / "two_scale_application_v1.json"
    fixture_sha256 = hashlib.sha256(fixture_path.read_bytes()).hexdigest()
    provenance = manifest["provenance"]
    assert provenance["application_id"] == (
        "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"
    )
    assert provenance["input_hashes"]["two_scale_application_id"] == provenance[
        "application_id"
    ]
    assert (
        provenance["input_hashes"]["two_scale_application_file_sha256"]
        == fixture_sha256
    )

    with pytest.raises(TypeError):
        result.metrics["extra"] = next(iter(result.metrics.values()))  # type: ignore[index]
    with pytest.raises(TypeError):
        result.arrays["extra"] = next(iter(result.arrays.values()))  # type: ignore[index]
    with pytest.raises(ValueError):
        next(iter(result.arrays.values())).flat[0] = 123.0
    with pytest.raises(FrozenInstanceError):
        result.status = "fail"  # type: ignore[misc]


def test_exact_artifacts_round_trip_and_recompute_every_metric(tmp_path: Path):
    """Mutation caught: lossy rational serialization or a metric not backed by arrays."""
    from multiagent_elbo.finite.theory_oracle_experiment import (
        run_theory_oracle_experiment,
    )
    from multiagent_elbo.finite.theory_oracles import THEOREM_ASSUMPTION_MATRIX

    result = run_theory_oracle_experiment(_config(tmp_path / "runs"))
    numerators = json.loads((result.run_dir / "exact_numerators.json").read_text())
    denominators = json.loads((result.run_dir / "exact_denominators.json").read_text())
    assert numerators["component"] == "numerator"
    assert denominators["component"] == "denominator"
    assert numerators["rational_arrays"].keys() == denominators[
        "rational_arrays"
    ].keys()
    for name, numerator_record in numerators["rational_arrays"].items():
        denominator_record = denominators["rational_arrays"][name]
        assert numerator_record["shape"] == denominator_record["shape"]
        values = [
            Fraction(numerator, denominator)
            for numerator, denominator in zip(
                numerator_record["values"],
                denominator_record["values"],
                strict=True,
            )
        ]
        assert len(values) == math.prod(numerator_record["shape"])
    assert numerators["formal_log_sums"].keys() == denominators[
        "formal_log_sums"
    ].keys()
    for name, numerator_record in numerators["formal_log_sums"].items():
        denominator_record = denominators["formal_log_sums"][name]
        atoms = tuple(
            Fraction(numerator, denominator)
            for numerator, denominator in zip(
                numerator_record["atoms"], denominator_record["atoms"], strict=True
            )
        )
        coefficients = tuple(
            Fraction(numerator, denominator)
            for numerator, denominator in zip(
                numerator_record["coefficients"],
                denominator_record["coefficients"],
                strict=True,
            )
        )
        assert len(atoms) == len(coefficients)

    pairs = {
        "elbo_oracle_residual": ("elbo_oracle_values", "elbo_production_values"),
        "fisher_defect_oracle_residual": (
            "fisher_defect_oracle_values",
            "fisher_defect_production_values",
        ),
        "marked_event_associativity_residual": (
            "marked_event_oracle_values",
            "marked_event_production_values",
        ),
        "hoeffding_oracle_residual": (
            "hoeffding_oracle_values",
            "hoeffding_production_values",
        ),
        "gaussian_linear_algebra_oracle_residual": (
            "gaussian_linear_algebra_oracle_values",
            "gaussian_linear_algebra_production_values",
        ),
    }
    with np.load(result.run_dir / "arrays.npz", allow_pickle=False) as arrays:
        for metric_name, (oracle_name, production_name) in pairs.items():
            recomputed = float(
                np.max(np.abs(arrays[production_name] - arrays[oracle_name]))
            )
            assert recomputed == result.metrics[metric_name].value

    assumptions = json.loads(
        (result.run_dir / "theorem_assumption_matrix.json").read_text()
    )
    expected_records = json.loads(
        json.dumps([asdict(record) for record in THEOREM_ASSUMPTION_MATRIX])
    )
    assert assumptions["records"] == expected_records
    application = next(
        record
        for record in assumptions["records"]
        if record["identity_id"] == "two_scale_literal_commuting_square"
    )
    assert application["verification_state"] == "CANDIDATE"
    assert application["claim_origin"] == "APPLICATION_SPECIFIC"
    diagrams = json.loads(
        (result.run_dir / "literal_commuting_diagrams.json").read_text()
    )
    assert diagrams["application_identity_map_square"]["commutes"] is True
    assert (
        diagrams["application_identity_map_square"][
            "recognition_right_inverse_state"
        ]
        == "NOT_CHECKED"
    )
    assert diagrams["auxiliary_nonidentity_positive_control"]["commutes"] is True
    assert diagrams["auxiliary_nonidentity_negative_control"]["commutes"] is False
    assert diagrams["auxiliary_nonidentity_positive_control"]["auxiliary"] is True
    assert diagrams["auxiliary_nonidentity_negative_control"]["auxiliary"] is True


def test_semantic_artifacts_are_byte_stable_and_complete_runs_do_not_overwrite(
    tmp_path: Path,
):
    """Mutation caught: embedding output roots or timestamps in semantic artifacts."""
    from multiagent_elbo.finite.theory_oracle_experiment import (
        run_theory_oracle_experiment,
    )

    first_config = _config(tmp_path / "first", diagnostics=False)
    second_config = _config(tmp_path / "second", diagnostics=False)
    first = run_theory_oracle_experiment(first_config)
    second = run_theory_oracle_experiment(second_config)
    expected_without_diagnostics = {
        "config.json",
        "manifest.json",
        "metrics.json",
        "arrays.npz",
        "exact_numerators.json",
        "exact_denominators.json",
        "theorem_assumption_matrix.json",
        "literal_commuting_diagrams.json",
    }
    assert {path.name for path in first.run_dir.iterdir()} == expected_without_diagnostics
    assert dict(first.diagnostics) == {}
    for filename in (
        "metrics.json",
        "arrays.npz",
        "exact_numerators.json",
        "exact_denominators.json",
        "theorem_assumption_matrix.json",
        "literal_commuting_diagrams.json",
    ):
        assert (first.run_dir / filename).read_bytes() == (
            second.run_dir / filename
        ).read_bytes()

    with pytest.raises(FileExistsError, match="complete run exists"):
        run_theory_oracle_experiment(first_config)


def _load_launcher():
    launcher = Path(__file__).parents[1] / "run_theory_oracle_lab.py"
    spec = importlib.util.spec_from_file_location("task2_theory_oracle_launcher", launcher)
    if spec is None or spec.loader is None:
        raise AssertionError("launcher import spec was unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return launcher, module


def test_launcher_is_import_safe_and_main_accepts_temporary_output_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Mutation caught: import-time execution or forcing callers to edit OUTPUT."""
    monkeypatch.chdir(tmp_path)
    launcher, module = _load_launcher()
    assert launcher.is_file()
    assert list(tmp_path.iterdir()) == []

    result = module.main(output_root=tmp_path / "override")

    assert result.status == "pass"
    assert result.run_dir.is_relative_to(tmp_path / "override")
    assert json.loads((result.run_dir / "manifest.json").read_text())["complete"] is True


def test_launcher_runs_without_arguments_from_sanitized_temporary_cwd(tmp_path: Path):
    """Mutation caught: relying on CWD, PYTHONPATH, editable install, or CLI parsing."""
    launcher = Path(__file__).parents[1] / "run_theory_oracle_lab.py"
    environment = os.environ.copy()
    environment["PYTHONPATH"] = ""
    completed = subprocess.run(
        [r"C:\Python314\python.exe", str(launcher)],
        cwd=tmp_path,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "status=pass" in completed.stdout
    manifests = list((tmp_path / "artifacts").rglob("manifest.json"))
    assert len(manifests) == 1
    assert json.loads(manifests[0].read_text())["complete"] is True
