from __future__ import annotations

from pathlib import Path

import pytest

from multiagent_elbo.config import ConfigError, ExperimentConfig


def valid_dicts(root: Path | None = None) -> tuple[dict, dict, dict, dict]:
    return (
        {"name": "finite_exact_smoke", "seed": 20260808},
        {"experiment": "finite_exact", "retained_interaction_order": 2},
        {"dtype": "float64", "atol": 1e-10, "rtol": 1e-9},
        {
            "root": str(root or Path("artifacts")),
            "collect_diagnostics": True,
            "render_figures": False,
        },
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
    with pytest.raises(AttributeError):
        config.run.seed = 1  # type: ignore[misc]
