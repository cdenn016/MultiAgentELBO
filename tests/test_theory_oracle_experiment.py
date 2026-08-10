from __future__ import annotations

from dataclasses import replace
from dataclasses import FrozenInstanceError
from dataclasses import asdict
from copy import deepcopy
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
        assert metric.verification_state == "CANDIDATE"
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
    with pytest.raises(TypeError):
        result.diagnostics["extra"] = next(iter(result.diagnostics.values()))  # type: ignore[index]
    with pytest.raises(ValueError):
        next(iter(result.arrays.values())).flat[0] = 123.0
    with pytest.raises(ValueError):
        next(iter(result.diagnostics.values())).flat[0] = 123.0
    with pytest.raises(FrozenInstanceError):
        result.status = "fail"  # type: ignore[misc]


def _reconstruct_json_oracle_vectors(
    numerators: dict[str, object], denominators: dict[str, object]
) -> tuple[
    dict[str, np.ndarray],
    dict[str, tuple[tuple[int, ...], tuple[Fraction, ...]]],
]:
    assert numerators["metric_oracle_layout"] == denominators[
        "metric_oracle_layout"
    ]
    numerator_arrays = numerators["rational_arrays"]
    denominator_arrays = denominators["rational_arrays"]
    assert isinstance(numerator_arrays, dict)
    assert isinstance(denominator_arrays, dict)
    rational_arrays: dict[
        str, tuple[tuple[int, ...], tuple[Fraction, ...]]
    ] = {}
    for name, numerator_record in numerator_arrays.items():
        denominator_record = denominator_arrays[name]
        assert isinstance(numerator_record, dict)
        assert isinstance(denominator_record, dict)
        shape = tuple(numerator_record["shape"])
        assert list(shape) == denominator_record["shape"]
        values = tuple(
            Fraction(numerator, denominator)
            for numerator, denominator in zip(
                numerator_record["values"],
                denominator_record["values"],
                strict=True,
            )
        )
        assert len(values) == math.prod(shape)
        rational_arrays[name] = shape, values

    numerator_logs = numerators["formal_log_sums"]
    denominator_logs = denominators["formal_log_sums"]
    assert isinstance(numerator_logs, dict)
    assert isinstance(denominator_logs, dict)
    formal_logs: dict[str, float] = {}
    for name, numerator_record in numerator_logs.items():
        denominator_record = denominator_logs[name]
        assert isinstance(numerator_record, dict)
        assert isinstance(denominator_record, dict)
        atoms = tuple(
            Fraction(numerator, denominator)
            for numerator, denominator in zip(
                numerator_record["atoms"],
                denominator_record["atoms"],
                strict=True,
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
        formal_logs[name] = sum(
            float(coefficient) * math.log(float(atom))
            for atom, coefficient in zip(atoms, coefficients, strict=True)
        )

    layout = numerators["metric_oracle_layout"]
    assert isinstance(layout, dict)
    vectors: dict[str, np.ndarray] = {}
    for metric_name, components in layout.items():
        pieces: list[np.ndarray] = []
        for component in components:
            if component["kind"] == "rational_array":
                _, values = rational_arrays[component["name"]]
                pieces.append(np.asarray([float(value) for value in values]))
            elif component["kind"] == "formal_log":
                pieces.append(np.asarray([formal_logs[component["name"]]]))
            else:
                raise AssertionError(f"unknown exact component kind: {component}")
        vectors[metric_name] = np.concatenate(pieces)
    return vectors, rational_arrays


def test_exact_artifacts_round_trip_and_recompute_every_metric(tmp_path: Path):
    """Mutation caught: corrupt JSON exact values hidden by arrays-only recomputation."""
    from multiagent_elbo.finite.theory_oracle_experiment import (
        run_theory_oracle_experiment,
    )
    from multiagent_elbo.finite.theory_oracles import THEOREM_ASSUMPTION_MATRIX

    result = run_theory_oracle_experiment(_config(tmp_path / "runs"))
    numerators = json.loads((result.run_dir / "exact_numerators.json").read_text())
    denominators = json.loads((result.run_dir / "exact_denominators.json").read_text())
    assert numerators["component"] == "numerator"
    assert denominators["component"] == "denominator"
    expected_layout = {
        "elbo_oracle_residual": [
            {"kind": "formal_log", "name": "elbo.evidence_log"},
            {"kind": "formal_log", "name": "elbo.elbo"},
            {"kind": "formal_log", "name": "elbo.kl"},
            {"kind": "formal_log", "name": "elbo.structural_residual"},
        ],
        "fisher_defect_oracle_residual": [
            {"kind": "rational_array", "name": f"fisher.{name}"}
            for name in (
                "joint_weights",
                "coarse_mass",
                "coarse_scores",
                "fine_fisher",
                "coarse_fisher",
                "defect",
                "conditional_covariance",
            )
        ],
        "marked_event_associativity_residual": [
            {"kind": "rational_array", "name": f"marked.{stage}.{name}"}
            for stage in ("direct", "staged")
            for name in ("joint", "coarse_state_mass", "conditional_events")
        ],
        "hoeffding_oracle_residual": [
            {"kind": "rational_array", "name": f"hoeffding.component.{subset}"}
            for subset in (
                "empty",
                "0",
                "1",
                "2",
                "0_1",
                "0_2",
                "1_2",
                "0_1_2",
            )
        ]
        + [
            {"kind": "rational_array", "name": f"hoeffding.{name}"}
            for name in (
                "reconstruction",
                "reconstruction_residual",
                "retained_values",
                "retained_residual",
            )
        ],
        "gaussian_linear_algebra_oracle_residual": [
            {"kind": "rational_array", "name": f"gaussian.{name}"}
            for name in (
                "inverse_congruence",
                "transformed_prolongator",
                "galerkin",
                "schur",
            )
        ],
    }
    assert numerators["metric_oracle_layout"] == expected_layout
    assert denominators["metric_oracle_layout"] == expected_layout
    reconstructed, rational_arrays = _reconstruct_json_oracle_vectors(
        numerators, denominators
    )
    assert {name: vector.shape for name, vector in reconstructed.items()} == {
        "elbo_oracle_residual": (4,),
        "fisher_defect_oracle_residual": (12,),
        "marked_event_associativity_residual": (36,),
        "hoeffding_oracle_residual": (96,),
        "gaussian_linear_algebra_oracle_residual": (32,),
    }
    assert rational_arrays["fisher.coarse_mass"] == (
        (2,),
        (Fraction(1, 2), Fraction(1, 2)),
    )
    assert rational_arrays["marked.direct.coarse_state_mass"] == (
        (2,),
        (Fraction(101, 315), Fraction(214, 315)),
    )
    assert rational_arrays["gaussian.schur"] == (
        (2, 2),
        (Fraction(11, 3), Fraction(-1, 3), Fraction(-1, 3), Fraction(5, 3)),
    )
    assert reconstructed["elbo_oracle_residual"][0] == -math.log(2.0)
    assert reconstructed["elbo_oracle_residual"][-1] == 0.0

    production_names = {
        "elbo_oracle_residual": "elbo_production_values",
        "fisher_defect_oracle_residual": "fisher_defect_production_values",
        "marked_event_associativity_residual": "marked_event_production_values",
        "hoeffding_oracle_residual": "hoeffding_production_values",
        "gaussian_linear_algebra_oracle_residual": (
            "gaussian_linear_algebra_production_values"
        ),
    }
    with np.load(result.run_dir / "arrays.npz", allow_pickle=False) as arrays:
        for metric_name, production_name in production_names.items():
            recomputed = float(
                np.max(np.abs(arrays[production_name] - reconstructed[metric_name]))
            )
            assert recomputed == result.metrics[metric_name].value
        corrupted_numerators = deepcopy(numerators)
        corrupted_numerators["rational_arrays"]["gaussian.schur"]["values"][0] += 1
        corrupted, _ = _reconstruct_json_oracle_vectors(
            corrupted_numerators, denominators
        )
        corrupted_residual = float(
            np.max(
                np.abs(
                    arrays["gaussian_linear_algebra_production_values"]
                    - corrupted["gaussian_linear_algebra_oracle_residual"]
                )
            )
        )
        assert corrupted_residual > result.metrics[
            "gaussian_linear_algebra_oracle_residual"
        ].tolerance

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


@pytest.mark.parametrize(
    ("retained", "eliminated", "message"),
    (
        (("0", "3/2"), ("1",), "integer indices"),
        (("0", "0"), ("1", "2"), "unique"),
        (("0", "1"), ("1",), "disjoint"),
        (("0", "3"), ("1",), "in range"),
        (("0",), ("1",), "full partition"),
    ),
)
def test_gaussian_schur_packet_indices_fail_before_runtime_seams(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    retained: tuple[str, ...],
    eliminated: tuple[str, ...],
    message: str,
):
    """Mutation caught: silently truncating malformed Fraction indices."""
    import multiagent_elbo.finite.theory_oracle_experiment as experiment_module

    packets = list(experiment_module.LANE_PRIVATE_AUXILIARY_PACKETS)
    target_index = next(
        index
        for index, packet in enumerate(packets)
        if packet.packet_id == "oracle_aux_gaussian_v1"
    )
    packet = packets[target_index]
    literals = dict(packet.literals)
    literals["schur_retained"] = retained
    literals["schur_eliminated"] = eliminated
    packets[target_index] = replace(packet, literals=tuple(literals.items()))
    monkeypatch.setattr(
        experiment_module, "LANE_PRIVATE_AUXILIARY_PACKETS", tuple(packets)
    )

    def unreachable(*args: object, **kwargs: object) -> object:
        raise AssertionError("malformed Schur indices reached a runtime seam")

    monkeypatch.setattr(experiment_module.RngStreams, "from_seed", unreachable)
    monkeypatch.setattr(experiment_module, "collect_provenance", unreachable)
    monkeypatch.setattr(experiment_module.RunStore, "create", unreachable)

    with pytest.raises(ValueError, match=message):
        experiment_module.run_theory_oracle_experiment(_config(tmp_path / "runs"))
    assert not (tmp_path / "runs").exists()


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
    with pytest.raises(TypeError):
        first.diagnostics["extra"] = np.asarray([1.0])  # type: ignore[index]
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
