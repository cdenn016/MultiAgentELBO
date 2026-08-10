from __future__ import annotations

import math
from pathlib import Path
import tomllib

import pytest

import multiagent_elbo.config as config_module

from multiagent_elbo.config import (
    AttentionTheoryConfig,
    CategoricalDqmTheoryConfig,
    ConfigError,
    ExperimentConfig,
    config_sha256,
    canonical_config_json,
)


def valid_dicts(root: Path | None = None) -> tuple[dict, dict, dict, dict]:
    return (
        {"name": "finite_exact_smoke", "seed": 20260808},
        {"experiment": "finite_exact", "retained_interaction_order": 2},
        {
            "dtype": "float64",
            "atol": 1e-10,
            "rtol": 1e-9,
            "min_spd_rcond": 1e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(root or Path("artifacts")),
            "collect_diagnostics": True,
            "render_figures": False,
        },
    )


def attention_theory() -> dict[str, object]:
    return {
        "experiment": "attention_marked_event",
        "fixture": "nested_nonuniform_v1",
    }


def dqm_theory() -> dict[str, object]:
    return {
        "experiment": "categorical_dqm",
        "fixture": "three_category_softmax_v1",
        "theta": [math.log(2.0), math.log(3.0)],
        "finite_difference_step": 1.0e-5,
        "dqm_step_sizes": [0.1, 0.05, 0.025, 0.0125],
    }


def test_attention_and_dqm_theory_configs_resolve_to_frozen_variants(
    tmp_path: Path,
):
    run, _, numerics, output = valid_dicts(tmp_path)

    attention = ExperimentConfig.from_dicts(run, attention_theory(), numerics, output)
    dqm = ExperimentConfig.from_dicts(run, dqm_theory(), numerics, output)

    assert isinstance(attention.theory, AttentionTheoryConfig)
    assert isinstance(dqm.theory, CategoricalDqmTheoryConfig)
    assert dqm.theory.theta == (math.log(2.0), math.log(3.0))
    assert dqm.theory.dqm_step_sizes == (0.1, 0.05, 0.025, 0.0125)


@pytest.mark.parametrize(
    ("theory", "message"),
    [
        (
            {"experiment": "attention_marked_event"},
            "missing theory key: fixture",
        ),
        (
            {
                "experiment": "attention_marked_event",
                "fixture": "nested_nonuniform_v1",
                "unexpected": True,
            },
            "unknown theory key: unexpected",
        ),
        (
            {"experiment": "attention_marked_event", "fixture": "other"},
            "fixture must be 'nested_nonuniform_v1'",
        ),
        (
            {
                **dqm_theory(),
                "fixture": "other",
            },
            "fixture must be 'three_category_softmax_v1'",
        ),
        ({**dqm_theory(), "theta": [True, math.log(3.0)]}, r"theta\[0\] must be a finite float"),
        ({**dqm_theory(), "theta": [1, math.log(3.0)]}, r"theta\[0\] must be a finite float"),
        ({**dqm_theory(), "theta": ["bad", math.log(3.0)]}, r"theta\[0\] must be a finite float"),
        ({**dqm_theory(), "theta": [math.log(2.0)]}, "theta must contain exactly 2 values"),
        ({**dqm_theory(), "theta": [math.log(2.0), math.log(3.0), 0.0]}, "theta must contain exactly 2 values"),
        ({**dqm_theory(), "theta": "not-a-sequence"}, "theta must be a list or tuple"),
        ({**dqm_theory(), "finite_difference_step": 0.0}, "finite_difference_step must be a positive finite float"),
        ({**dqm_theory(), "finite_difference_step": -1.0e-5}, "finite_difference_step must be a positive finite float"),
        ({**dqm_theory(), "finite_difference_step": float("inf")}, "finite_difference_step must be a positive finite float"),
        ({**dqm_theory(), "finite_difference_step": float("nan")}, "finite_difference_step must be a positive finite float"),
        ({**dqm_theory(), "dqm_step_sizes": []}, "dqm_step_sizes must not be empty"),
        ({**dqm_theory(), "dqm_step_sizes": [0.1, 0.05, 0.05]}, "dqm_step_sizes must contain unique values"),
        ({**dqm_theory(), "dqm_step_sizes": [0.1, 0.05, 0.075]}, "dqm_step_sizes must be strictly decreasing"),
        ({**dqm_theory(), "dqm_step_sizes": [0.1, 0.0]}, r"dqm_step_sizes\[1\] must be a positive finite float"),
    ],
)
def test_invalid_discriminated_theory_configs_are_rejected(
    theory: dict[str, object], message: str
):
    run, _, numerics, output = valid_dicts()

    with pytest.raises(ConfigError, match=message):
        ExperimentConfig.from_dicts(run, theory, numerics, output)


def test_legacy_launcher_config_hashes_remain_unchanged():
    finite = ExperimentConfig.from_dicts(
        {"name": "finite exact", "seed": 20260808},
        {"experiment": "finite_exact", "retained_interaction_order": 2},
        {
            "dtype": "float64",
            "atol": 1e-10,
            "rtol": 1e-9,
            "min_spd_rcond": 1e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": "artifacts",
            "collect_diagnostics": True,
            "render_figures": False,
        },
    )
    gaussian = ExperimentConfig.from_dicts(
        {"name": "gaussian realization", "seed": 20260808},
        {"experiment": "gaussian_realization", "retained_interaction_order": None},
        {
            "dtype": "float64",
            "atol": 1e-12,
            "rtol": 1e-10,
            "min_spd_rcond": 1e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": "artifacts",
            "collect_diagnostics": True,
            "render_figures": False,
        },
    )

    assert config_sha256(finite) == (
        "ad296bae54057c87330a964e99c1ce6657bcfc2f769fd3d7211c5d6a6380e4f9"
    )
    assert config_sha256(gaussian) == (
        "30e8e0dd923c24a63d9ffc91e4b1d9740d15f576bb393f3106783fdd1b78085c"
    )


def test_unknown_config_key_is_rejected():
    run, theory, numerics, output = valid_dicts()
    run["mystery"] = 1

    with pytest.raises(ConfigError, match="unknown run key: mystery"):
        ExperimentConfig.from_dicts(run, theory, numerics, output)


def test_bool_is_not_accepted_as_integer_seed():
    run, theory, numerics, output = valid_dicts()
    run["seed"] = True

    with pytest.raises(ConfigError, match="seed must be an int, not bool"):
        ExperimentConfig.from_dicts(run, theory, numerics, output)


def test_invalid_config_has_no_filesystem_side_effect(tmp_path: Path):
    run, theory, numerics, output = valid_dicts(tmp_path)
    theory["retained_interaction_order"] = 0

    with pytest.raises(ConfigError):
        ExperimentConfig.from_dicts(run, theory, numerics, output)

    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    ("section", "key", "value", "message"),
    [
        ("run", "name", "../escape", "name must not contain path traversal"),
        ("run", "seed", -1, "seed must be a nonnegative int"),
        ("theory", "experiment", "other", "experiment must be one of"),
        (
            "theory",
            "retained_interaction_order",
            True,
            "retained_interaction_order must be an int or None, not bool",
        ),
        ("numerics", "dtype", "float32", "dtype must be 'float64'"),
        ("numerics", "atol", 0.0, "atol must be a positive finite float"),
        (
            "numerics",
            "min_spd_rcond",
            0.0,
            r"min_spd_rcond must be a finite float in \(0, 1\]",
        ),
        (
            "numerics",
            "min_spd_rcond",
            2.0,
            r"min_spd_rcond must be a finite float in \(0, 1\]",
        ),
        (
            "numerics",
            "min_spd_rcond",
            "1e-12",
            r"min_spd_rcond must be a finite float in \(0, 1\]",
        ),
        (
            "numerics",
            "max_frame_condition",
            1,
            "max_frame_condition must be a finite float at least 1",
        ),
        (
            "numerics",
            "max_frame_condition",
            None,
            "max_frame_condition must be a finite float at least 1",
        ),
        (
            "numerics",
            "max_frame_condition",
            float("inf"),
            "max_frame_condition must be a finite float at least 1",
        ),
        (
            "output",
            "collect_diagnostics",
            1,
            "collect_diagnostics must be a bool",
        ),
    ],
)
def test_invalid_typed_config_is_rejected_before_resolution(
    section: str, key: str, value: object, message: str
):
    run, theory, numerics, output = valid_dicts()
    {"run": run, "theory": theory, "numerics": numerics, "output": output}[section][key] = value

    with pytest.raises(ConfigError, match=message):
        ExperimentConfig.from_dicts(run, theory, numerics, output)


def test_resolved_config_is_frozen_and_normalizes_output_path(tmp_path: Path):
    run, theory, numerics, output = valid_dicts(tmp_path / "out")

    config = ExperimentConfig.from_dicts(run, theory, numerics, output)

    assert config.output.root == tmp_path / "out"
    assert config.numerics.min_spd_rcond == 1e-12
    assert config.numerics.max_frame_condition == 1.0e6
    with pytest.raises(AttributeError):
        config.run.seed = 1  # type: ignore[misc]


def valid_compute(**updates: object) -> dict[str, object]:
    compute: dict[str, object] = {
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
    compute.update(updates)
    return compute


def new_lab_theories() -> list[tuple[dict[str, object], str]]:
    return [
        (
            {
                "experiment": "multiagent_network",
                "fixture": "two_scale_application_v1",
                "scenario": "aligned",
                "arithmetic": "exact_rational",
            },
            "MultiagentNetworkTheoryConfig",
        ),
        (
            {
                "experiment": "theory_oracle",
                "fixture": "two_scale_application_v1",
                "oracle_set": "core_identities",
                "arithmetic": "exact_rational",
            },
            "TheoryOracleTheoryConfig",
        ),
        (
            {
                "experiment": "finite_counterexample",
                "fixture": "counterexample_catalog_v1",
                "max_states": 4,
                "max_denominator": 8,
                "arithmetic": "exact_rational",
            },
            "FiniteCounterexampleTheoryConfig",
        ),
        (
            {
                "experiment": "information_history",
                "fixture": "two_scale_application_v1",
                "family": "categorical_softmax",
                "history_steps": 16,
                "step_size": 0.05,
            },
            "InformationHistoryTheoryConfig",
        ),
        (
            {
                "experiment": "gauge_holonomy",
                "fixture": "two_scale_application_v1",
                "scenario": "nonflat_plaquette",
                "group": "GL+(2)",
            },
            "GaugeHolonomyTheoryConfig",
        ),
        (
            {
                "experiment": "scale_cocycle",
                "fixture": "two_scale_application_v1",
                "extension": "three_level_composition_v1",
                "retained_interaction_order": 2,
                "arithmetic": "exact_rational",
            },
            "ScaleCocycleTheoryConfig",
        ),
        (
            {
                "experiment": "gaussian_fixed_ray",
                "fixture": "gaussian_fixed_ray_v1",
                "preregistration": "2026-08-09-gaussian-fixed-ray-v1",
                "blocking_schemes": ["adjacent_pairs", "balanced_alternating"],
                "matrix_dimension": 2,
            },
            "GaussianFixedRayTheoryConfig",
        ),
    ]


def test_legacy_four_dictionary_json_and_hash_are_byte_compatible():
    run, theory, numerics, output = valid_dicts()

    config = ExperimentConfig.from_dicts(run, theory, numerics, output)

    assert canonical_config_json(config) == (
        '{"numerics":{"atol":1e-10,"dtype":"float64",'
        '"max_frame_condition":1000000.0,"min_spd_rcond":1e-12,'
        '"rtol":1e-09},"output":{"collect_diagnostics":true,'
        '"render_figures":false,"root":"artifacts"},"run":'
        '{"name":"finite_exact_smoke","seed":20260808},"theory":'
        '{"experiment":"finite_exact","retained_interaction_order":2}}'
    )
    assert config_sha256(config) == (
        "5d515fcc0ca990f793e0fc2e790f83ec335445fcb26f4da9f17f4de11defb458"
    )
    assert config.compute.backend == "cpu"
    assert config.compute.dtype == "float64"
    assert config.compute_explicit is False


@pytest.mark.parametrize(("theory", "type_name"), new_lab_theories())
def test_all_seven_new_lab_schemas_resolve_strict_literal_smoke_configs(
    theory: dict[str, object], type_name: str
):
    run, _, numerics, output = valid_dicts()

    config = ExperimentConfig.from_dicts(
        run, theory, numerics, output, valid_compute()
    )

    assert type(config.theory).__name__ == type_name
    assert config.compute_explicit is True
    assert config.compute.backend == "cpu"


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        ({"unknown": True}, "unknown compute key: unknown"),
        ({"batch_size": True}, "batch_size must be an int, not bool"),
        ({"batch_size": 0}, "batch_size must be a positive int"),
        ({"device_index": -1}, "device_index must be a nonnegative int"),
        ({"backend": "gpu"}, "backend must be 'cpu' or 'cuda'"),
        ({"dtype": "float16"}, "dtype must be one of"),
        ({"deterministic": 1}, "deterministic must be a bool"),
        ({"cuda_worker_python": "python"}, "cuda_worker_python must be an absolute path"),
    ],
)
def test_compute_schema_rejects_wrong_keys_and_types(
    mutate: dict[str, object], message: str
):
    run, theory, numerics, output = valid_dicts()
    compute = valid_compute(**mutate)

    with pytest.raises(ConfigError, match=message):
        ExperimentConfig.from_dicts(run, theory, numerics, output, compute)


@pytest.mark.parametrize(
    ("theory", "compute", "message"),
    [
        (
            new_lab_theories()[0][0],
            valid_compute(backend="cuda"),
            "exact-rational experiments are CPU-only",
        ),
        (
            new_lab_theories()[-1][0],
            valid_compute(dtype="float32"),
            "float32 and bfloat16 require CUDA",
        ),
        (
            new_lab_theories()[-1][0],
            valid_compute(
                backend="cuda", dtype="float32", heavy_sweep_enabled=False
            ),
            "reduced precision requires heavy_sweep_enabled",
        ),
        (
            new_lab_theories()[-1][0],
            valid_compute(
                backend="cuda", dtype="float64", cpu_cuda_parity=False
            ),
            "CUDA requires cpu_cuda_parity",
        ),
        (
            new_lab_theories()[-1][0],
            valid_compute(
                backend="cuda",
                dtype="float64",
                allow_tf32=True,
            ),
            "allow_tf32 requires CUDA float32 screening",
        ),
    ],
)
def test_compute_cross_field_failures_are_rejected_before_resolution(
    theory: dict[str, object], compute: dict[str, object], message: str
):
    run, _, numerics, output = valid_dicts()

    with pytest.raises(ConfigError, match=message):
        ExperimentConfig.from_dicts(run, theory, numerics, output, compute)


def test_explicit_compute_participates_in_new_configuration_identity():
    run, _, numerics, output = valid_dicts()
    theory = new_lab_theories()[-1][0]

    config = ExperimentConfig.from_dicts(
        run, theory, numerics, output, valid_compute()
    )
    payload = canonical_config_json(config)

    assert '"compute":{"allow_tf32":false,"backend":"cpu"' in payload
    assert '"compute_explicit"' not in payload


@pytest.mark.parametrize(
    ("theory", "message"),
    [
        (
            {**new_lab_theories()[0][0], "scenario": "other"},
            "scenario must be one of",
        ),
        (
            {**new_lab_theories()[2][0], "max_states": True},
            "max_states must be an int, not bool",
        ),
        (
            {**new_lab_theories()[3][0], "history_steps": 0},
            "history_steps must be a positive int",
        ),
        (
            {**new_lab_theories()[5][0], "retained_interaction_order": 0},
            "retained_interaction_order must be a positive int",
        ),
        (
            {**new_lab_theories()[6][0], "blocking_schemes": ["adjacent_pairs"]},
            "blocking_schemes must contain exactly",
        ),
    ],
)
def test_new_lab_schema_mutations_are_rejected(
    theory: dict[str, object], message: str
):
    run, _, numerics, output = valid_dicts()

    with pytest.raises(ConfigError, match=message):
        ExperimentConfig.from_dicts(
            run, theory, numerics, output, valid_compute()
        )


def test_reserved_experiment_names_are_complete_and_immutable():
    names = config_module.NEW_EXPERIMENT_NAMES

    assert names == (
        "multiagent_network",
        "theory_oracle",
        "finite_counterexample",
        "information_history",
        "gauge_holonomy",
        "scale_cocycle",
        "gaussian_fixed_ray",
    )
    with pytest.raises(TypeError):
        names[0] = "changed"  # type: ignore[index]


def test_development_coverage_contract_is_machine_readable_and_enforced():
    project = tomllib.loads(
        (Path(__file__).parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    )

    assert "pytest-cov>=7.0" in project["project"]["optional-dependencies"]["test"]
    assert project["tool"]["coverage"]["run"] == {
        "branch": True,
        "source": ["src/multiagent_elbo"],
    }
    assert project["tool"]["coverage"]["report"]["fail_under"] >= 80
    assert project["tool"]["coverage"]["report"]["show_missing"] is True
