from __future__ import annotations

import math
from pathlib import Path

import pytest

from multiagent_elbo.config import (
    AttentionTheoryConfig,
    CategoricalDqmTheoryConfig,
    ConfigError,
    ExperimentConfig,
    config_sha256,
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
