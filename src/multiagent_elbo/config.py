"""Strict, side-effect-free resolution of experiment configuration."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Literal, Mapping


class ConfigError(ValueError):
    """Raised when an editable experiment configuration is invalid."""


@dataclass(frozen=True)
class RunConfig:
    name: str
    seed: int


@dataclass(frozen=True)
class TheoryConfig:
    experiment: Literal["finite_exact", "gaussian_realization"]
    retained_interaction_order: int | None


@dataclass(frozen=True)
class NumericsConfig:
    dtype: Literal["float64"]
    atol: float
    rtol: float


@dataclass(frozen=True)
class OutputConfig:
    root: Path
    collect_diagnostics: bool
    render_figures: bool


@dataclass(frozen=True)
class ExperimentConfig:
    run: RunConfig
    theory: TheoryConfig
    numerics: NumericsConfig
    output: OutputConfig

    @classmethod
    def from_dicts(
        cls,
        run: Mapping[str, object],
        theory: Mapping[str, object],
        numerics: Mapping[str, object],
        output: Mapping[str, object],
    ) -> "ExperimentConfig":
        """Validate dictionaries before any RNG or filesystem operation."""
        _require_exact_keys(run, "run", {"name", "seed"})
        _require_exact_keys(
            theory, "theory", {"experiment", "retained_interaction_order"}
        )
        _require_exact_keys(numerics, "numerics", {"dtype", "atol", "rtol"})
        _require_exact_keys(
            output,
            "output",
            {"root", "collect_diagnostics", "render_figures"},
        )

        name = _require_str(run["name"], "name")
        if not name or name in {".", ".."} or "/" in name or "\\" in name:
            raise ConfigError("name must not contain path traversal")
        seed = _require_int(run["seed"], "seed")
        if seed < 0:
            raise ConfigError("seed must be a nonnegative int")

        experiment = _require_str(theory["experiment"], "experiment")
        if experiment not in {"finite_exact", "gaussian_realization"}:
            raise ConfigError("experiment must be one of: finite_exact, gaussian_realization")
        retained_interaction_order = theory["retained_interaction_order"]
        if retained_interaction_order is not None:
            if type(retained_interaction_order) is bool:
                raise ConfigError(
                    "retained_interaction_order must be an int or None, not bool"
                )
            retained_interaction_order = _require_int(
                retained_interaction_order, "retained_interaction_order"
            )
            if retained_interaction_order < 1:
                raise ConfigError("retained_interaction_order must be at least 1")

        dtype = _require_str(numerics["dtype"], "dtype")
        if dtype != "float64":
            raise ConfigError("dtype must be 'float64'")
        atol = _require_positive_float(numerics["atol"], "atol")
        rtol = _require_positive_float(numerics["rtol"], "rtol")

        root_value = output["root"]
        if not isinstance(root_value, (str, Path)):
            raise ConfigError("root must be a str or Path")
        root = Path(root_value)
        collect_diagnostics = _require_bool(
            output["collect_diagnostics"], "collect_diagnostics"
        )
        render_figures = _require_bool(output["render_figures"], "render_figures")

        return cls(
            run=RunConfig(name=name, seed=seed),
            theory=TheoryConfig(
                experiment=experiment,
                retained_interaction_order=retained_interaction_order,
            ),
            numerics=NumericsConfig(dtype=dtype, atol=atol, rtol=rtol),
            output=OutputConfig(
                root=root,
                collect_diagnostics=collect_diagnostics,
                render_figures=render_figures,
            ),
        )


def canonical_config_json(config: ExperimentConfig) -> str:
    """Return an unambiguous serialization of a resolved configuration."""
    payload = asdict(config)
    payload["output"]["root"] = str(config.output.root)
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def config_sha256(config: ExperimentConfig) -> str:
    """Return the lowercase SHA-256 digest of the canonical configuration."""
    return hashlib.sha256(canonical_config_json(config).encode("utf-8")).hexdigest()


def _require_exact_keys(
    values: Mapping[str, object], section: str, expected: set[str]
) -> None:
    unknown = sorted(set(values) - expected)
    if unknown:
        raise ConfigError(f"unknown {section} key: {unknown[0]}")
    missing = sorted(expected - set(values))
    if missing:
        raise ConfigError(f"missing {section} key: {missing[0]}")


def _require_str(value: object, field: str) -> str:
    if type(value) is not str:
        raise ConfigError(f"{field} must be a str")
    return value


def _require_int(value: object, field: str) -> int:
    if type(value) is bool:
        raise ConfigError(f"{field} must be an int, not bool")
    if type(value) is not int:
        raise ConfigError(f"{field} must be an int")
    return value


def _require_positive_float(value: object, field: str) -> float:
    if type(value) is not float or not math.isfinite(value) or value <= 0.0:
        raise ConfigError(f"{field} must be a positive finite float")
    return value


def _require_bool(value: object, field: str) -> bool:
    if type(value) is not bool:
        raise ConfigError(f"{field} must be a bool")
    return value
