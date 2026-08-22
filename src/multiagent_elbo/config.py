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
    """Theory block of the two experiments that share an interaction decomposition.

    ``retained_interaction_order`` is the Hoeffding order the read-back keeps,
    with ``None`` meaning the full order. It gates the ``INT-01_retained_order_*``
    metrics of ``finite_exact``; ``gaussian_realization`` decomposes no
    interaction and reads it nowhere, so for that experiment it is declared,
    validated, and folded into the run identity while changing no number. Both
    facts are stated here rather than left to be discovered: until 2026-08-18
    the key reached no metric in either experiment, so a sweep over it produced
    thirteen distinct config hashes and one byte-identical ``metrics.json``
    (2026-08-18 lab-versus-theory audit, finding 6).
    """

    experiment: Literal["finite_exact", "gaussian_realization"]
    retained_interaction_order: int | None


@dataclass(frozen=True)
class AttentionTheoryConfig:
    experiment: Literal["attention_marked_event"]
    fixture: Literal["nested_nonuniform_v1"]


@dataclass(frozen=True)
class CategoricalDqmTheoryConfig:
    experiment: Literal["categorical_dqm"]
    fixture: Literal["three_category_softmax_v1"]
    theta: tuple[float, float]
    finite_difference_step: float
    dqm_step_sizes: tuple[float, ...]


NEW_EXPERIMENT_NAMES = (
    "multiagent_network",
    "theory_oracle",
    "finite_counterexample",
    "information_history",
    "gauge_holonomy",
    "scale_cocycle",
    "gaussian_fixed_ray",
    "renormalization_v2",
    "renormalization_v2_recursive",
)


@dataclass(frozen=True)
class MultiagentNetworkTheoryConfig:
    experiment: Literal["multiagent_network"]
    fixture: Literal["two_scale_application_v1"]
    scenario: Literal[
        "aligned", "frustrated", "asymmetric_evidence", "higher_order"
    ]
    arithmetic: Literal["exact_rational"]


@dataclass(frozen=True)
class TheoryOracleTheoryConfig:
    experiment: Literal["theory_oracle"]
    fixture: Literal["two_scale_application_v1"]
    oracle_set: Literal["core_identities"]
    arithmetic: Literal["exact_rational"]


@dataclass(frozen=True)
class FiniteCounterexampleTheoryConfig:
    experiment: Literal["finite_counterexample"]
    fixture: Literal["counterexample_catalog_v1"]
    max_states: int
    max_denominator: int
    arithmetic: Literal["exact_rational"]


@dataclass(frozen=True)
class InformationHistoryTheoryConfig:
    experiment: Literal["information_history"]
    fixture: Literal["two_scale_application_v1"]
    family: Literal["categorical_softmax"]
    history_steps: int
    step_size: float


@dataclass(frozen=True)
class GaugeHolonomyTheoryConfig:
    experiment: Literal["gauge_holonomy"]
    fixture: Literal["two_scale_application_v1"]
    scenario: Literal[
        "flat_tree",
        "flat_cycle",
        "nonflat_plaquette",
        "frustrated_transport",
        "staged_aggregation",
    ]
    group: Literal["GL+(2)"]


@dataclass(frozen=True)
class ScaleCocycleTheoryConfig:
    experiment: Literal["scale_cocycle"]
    fixture: Literal["two_scale_application_v1"]
    extension: Literal["three_level_composition_v1"]
    retained_interaction_order: int
    arithmetic: Literal["exact_rational"]


@dataclass(frozen=True)
class GaussianFixedRayTheoryConfig:
    experiment: Literal["gaussian_fixed_ray"]
    fixture: Literal["gaussian_fixed_ray_v1"]
    preregistration: Literal["2026-08-09-gaussian-fixed-ray-v1"]
    blocking_schemes: tuple[
        Literal["adjacent_pairs"], Literal["balanced_alternating"]
    ]
    matrix_dimension: int


@dataclass(frozen=True)
class RenormalizationV2TheoryConfig:
    experiment: Literal["renormalization_v2"]
    fixture: Literal[
        "lf3_product_v1",
        "lf3_correlated_v1",
        "lf3_dirac_boundary_v1",
    ]
    arithmetic: Literal["exact_rational"]


@dataclass(frozen=True)
class RenormalizationV2RecursiveTheoryConfig:
    experiment: Literal["renormalization_v2_recursive"]
    fixture: Literal["lf4_two_parent_recursive_v1"]
    arithmetic: Literal["exact_rational"]


@dataclass(frozen=True)
class CategoricalFalsificationTheoryConfig:
    experiment: Literal["categorical_falsification"]
    fixture: Literal["two_channel_z3_v1"]
    admitted_family: Literal["orbit", "simplex", "both"]
    null_control_seeds: int
    descent_restarts: int
    arithmetic: Literal["exact_rational"]


ExperimentTheoryConfig = (
    TheoryConfig
    | AttentionTheoryConfig
    | CategoricalFalsificationTheoryConfig
    | CategoricalDqmTheoryConfig
    | MultiagentNetworkTheoryConfig
    | TheoryOracleTheoryConfig
    | FiniteCounterexampleTheoryConfig
    | InformationHistoryTheoryConfig
    | GaugeHolonomyTheoryConfig
    | ScaleCocycleTheoryConfig
    | GaussianFixedRayTheoryConfig
    | RenormalizationV2TheoryConfig
    | RenormalizationV2RecursiveTheoryConfig
)


@dataclass(frozen=True)
class NumericsConfig:
    dtype: Literal["float64"]
    atol: float
    rtol: float
    min_spd_rcond: float = 1e-12
    max_frame_condition: float = 1.0e6


@dataclass(frozen=True)
class OutputConfig:
    root: Path
    collect_diagnostics: bool
    render_figures: bool


@dataclass(frozen=True)
class ComputeConfig:
    backend: Literal["cpu", "cuda"]
    dtype: Literal["float64", "float32", "bfloat16"]
    device_index: int
    batch_size: int
    deterministic: bool
    allow_tf32: bool
    cpu_cuda_parity: bool
    cuda_worker_python: Path
    heavy_sweep_enabled: bool


def _default_compute_config() -> ComputeConfig:
    return ComputeConfig(
        backend="cpu",
        dtype="float64",
        device_index=0,
        batch_size=4096,
        deterministic=True,
        allow_tf32=False,
        cpu_cuda_parity=True,
        cuda_worker_python=Path(r"C:\anaconda\python.exe"),
        heavy_sweep_enabled=False,
    )


@dataclass(frozen=True)
class ExperimentConfig:
    run: RunConfig
    theory: ExperimentTheoryConfig
    numerics: NumericsConfig
    output: OutputConfig
    compute: ComputeConfig
    _compute_explicit: bool

    @property
    def compute_explicit(self) -> bool:
        """Whether the caller supplied the optional COMPUTE dictionary."""
        return self._compute_explicit

    @classmethod
    def from_dicts(
        cls,
        run: Mapping[str, object],
        theory: Mapping[str, object],
        numerics: Mapping[str, object],
        output: Mapping[str, object],
        compute: Mapping[str, object] | None = None,
    ) -> "ExperimentConfig":
        """Validate dictionaries before any RNG or filesystem operation."""
        _require_exact_keys(run, "run", {"name", "seed"})
        theory_config = _resolve_theory_config(theory)
        compute_config = (
            _default_compute_config()
            if compute is None
            else _resolve_compute_config(compute, theory_config)
        )
        _require_exact_keys(
            numerics,
            "numerics",
            {
                "dtype",
                "atol",
                "rtol",
                "min_spd_rcond",
                "max_frame_condition",
            },
        )
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

        dtype = _require_str(numerics["dtype"], "dtype")
        if dtype != "float64":
            raise ConfigError("dtype must be 'float64'")
        atol = _require_positive_float(numerics["atol"], "atol")
        rtol = _require_positive_float(numerics["rtol"], "rtol")
        min_spd_rcond = _require_bounded_float(
            numerics["min_spd_rcond"],
            "min_spd_rcond",
            minimum=0.0,
            maximum=1.0,
            minimum_inclusive=False,
        )
        max_frame_condition = _require_bounded_float(
            numerics["max_frame_condition"],
            "max_frame_condition",
            minimum=1.0,
            maximum=None,
            minimum_inclusive=True,
        )

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
            theory=theory_config,
            numerics=NumericsConfig(
                dtype=dtype,
                atol=atol,
                rtol=rtol,
                min_spd_rcond=min_spd_rcond,
                max_frame_condition=max_frame_condition,
            ),
            output=OutputConfig(
                root=root,
                collect_diagnostics=collect_diagnostics,
                render_figures=render_figures,
            ),
            compute=compute_config,
            _compute_explicit=compute is not None,
        )


def _resolve_theory_config(theory: Mapping[str, object]) -> ExperimentTheoryConfig:
    if "experiment" not in theory:
        raise ConfigError("missing theory key: experiment")
    experiment = _require_str(theory["experiment"], "experiment")

    if experiment in {"finite_exact", "gaussian_realization"}:
        _require_exact_keys(
            theory, "theory", {"experiment", "retained_interaction_order"}
        )
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
        return TheoryConfig(
            experiment=experiment,
            retained_interaction_order=retained_interaction_order,
        )

    if experiment == "attention_marked_event":
        _require_exact_keys(theory, "theory", {"experiment", "fixture"})
        fixture = _require_str(theory["fixture"], "fixture")
        if fixture != "nested_nonuniform_v1":
            raise ConfigError("fixture must be 'nested_nonuniform_v1'")
        return AttentionTheoryConfig(experiment=experiment, fixture=fixture)

    if experiment == "categorical_dqm":
        _require_exact_keys(
            theory,
            "theory",
            {
                "experiment",
                "fixture",
                "theta",
                "finite_difference_step",
                "dqm_step_sizes",
            },
        )
        fixture = _require_str(theory["fixture"], "fixture")
        if fixture != "three_category_softmax_v1":
            raise ConfigError("fixture must be 'three_category_softmax_v1'")
        theta = _require_float_tuple(theory["theta"], "theta")
        if len(theta) != 2:
            raise ConfigError("theta must contain exactly 2 values")
        dqm_step_sizes = _require_positive_float_tuple(
            theory["dqm_step_sizes"], "dqm_step_sizes"
        )
        if len(set(dqm_step_sizes)) != len(dqm_step_sizes):
            raise ConfigError("dqm_step_sizes must contain unique values")
        if any(
            current <= following
            for current, following in zip(dqm_step_sizes, dqm_step_sizes[1:])
        ):
            raise ConfigError("dqm_step_sizes must be strictly decreasing")
        return CategoricalDqmTheoryConfig(
            experiment=experiment,
            fixture=fixture,
            theta=(theta[0], theta[1]),
            finite_difference_step=_require_positive_float(
                theory["finite_difference_step"], "finite_difference_step"
            ),
            dqm_step_sizes=dqm_step_sizes,
        )

    if experiment == "multiagent_network":
        _require_exact_keys(
            theory,
            "theory",
            {"experiment", "fixture", "scenario", "arithmetic"},
        )
        fixture = _require_literal(
            theory["fixture"], "fixture", ("two_scale_application_v1",)
        )
        scenario = _require_literal(
            theory["scenario"],
            "scenario",
            ("aligned", "frustrated", "asymmetric_evidence", "higher_order"),
        )
        arithmetic = _require_literal(
            theory["arithmetic"], "arithmetic", ("exact_rational",)
        )
        return MultiagentNetworkTheoryConfig(
            experiment=experiment,
            fixture=fixture,
            scenario=scenario,
            arithmetic=arithmetic,
        )

    if experiment == "theory_oracle":
        _require_exact_keys(
            theory,
            "theory",
            {"experiment", "fixture", "oracle_set", "arithmetic"},
        )
        return TheoryOracleTheoryConfig(
            experiment=experiment,
            fixture=_require_literal(
                theory["fixture"], "fixture", ("two_scale_application_v1",)
            ),
            oracle_set=_require_literal(
                theory["oracle_set"], "oracle_set", ("core_identities",)
            ),
            arithmetic=_require_literal(
                theory["arithmetic"], "arithmetic", ("exact_rational",)
            ),
        )

    if experiment == "finite_counterexample":
        _require_exact_keys(
            theory,
            "theory",
            {
                "experiment",
                "fixture",
                "max_states",
                "max_denominator",
                "arithmetic",
            },
        )
        return FiniteCounterexampleTheoryConfig(
            experiment=experiment,
            fixture=_require_literal(
                theory["fixture"], "fixture", ("counterexample_catalog_v1",)
            ),
            max_states=_require_positive_int(theory["max_states"], "max_states"),
            max_denominator=_require_positive_int(
                theory["max_denominator"], "max_denominator"
            ),
            arithmetic=_require_literal(
                theory["arithmetic"], "arithmetic", ("exact_rational",)
            ),
        )

    if experiment == "information_history":
        _require_exact_keys(
            theory,
            "theory",
            {"experiment", "fixture", "family", "history_steps", "step_size"},
        )
        return InformationHistoryTheoryConfig(
            experiment=experiment,
            fixture=_require_literal(
                theory["fixture"], "fixture", ("two_scale_application_v1",)
            ),
            family=_require_literal(
                theory["family"], "family", ("categorical_softmax",)
            ),
            history_steps=_require_positive_int(
                theory["history_steps"], "history_steps"
            ),
            step_size=_require_positive_float(theory["step_size"], "step_size"),
        )

    if experiment == "gauge_holonomy":
        _require_exact_keys(
            theory,
            "theory",
            {"experiment", "fixture", "scenario", "group"},
        )
        return GaugeHolonomyTheoryConfig(
            experiment=experiment,
            fixture=_require_literal(
                theory["fixture"], "fixture", ("two_scale_application_v1",)
            ),
            scenario=_require_literal(
                theory["scenario"],
                "scenario",
                (
                    "flat_tree",
                    "flat_cycle",
                    "nonflat_plaquette",
                    "frustrated_transport",
                    "staged_aggregation",
                ),
            ),
            group=_require_literal(theory["group"], "group", ("GL+(2)",)),
        )

    if experiment == "scale_cocycle":
        _require_exact_keys(
            theory,
            "theory",
            {
                "experiment",
                "fixture",
                "extension",
                "retained_interaction_order",
                "arithmetic",
            },
        )
        return ScaleCocycleTheoryConfig(
            experiment=experiment,
            fixture=_require_literal(
                theory["fixture"], "fixture", ("two_scale_application_v1",)
            ),
            extension=_require_literal(
                theory["extension"], "extension", ("three_level_composition_v1",)
            ),
            retained_interaction_order=_require_positive_int(
                theory["retained_interaction_order"], "retained_interaction_order"
            ),
            arithmetic=_require_literal(
                theory["arithmetic"], "arithmetic", ("exact_rational",)
            ),
        )

    if experiment == "gaussian_fixed_ray":
        _require_exact_keys(
            theory,
            "theory",
            {
                "experiment",
                "fixture",
                "preregistration",
                "blocking_schemes",
                "matrix_dimension",
            },
        )
        blocking_schemes = _require_str_tuple(
            theory["blocking_schemes"], "blocking_schemes"
        )
        if blocking_schemes != ("adjacent_pairs", "balanced_alternating"):
            raise ConfigError(
                "blocking_schemes must contain exactly adjacent_pairs then "
                "balanced_alternating"
            )
        return GaussianFixedRayTheoryConfig(
            experiment=experiment,
            fixture=_require_literal(
                theory["fixture"], "fixture", ("gaussian_fixed_ray_v1",)
            ),
            preregistration=_require_literal(
                theory["preregistration"],
                "preregistration",
                ("2026-08-09-gaussian-fixed-ray-v1",),
            ),
            blocking_schemes=(blocking_schemes[0], blocking_schemes[1]),
            matrix_dimension=_require_positive_int(
                theory["matrix_dimension"], "matrix_dimension"
            ),
        )

    if experiment == "renormalization_v2":
        _require_exact_keys(
            theory,
            "theory",
            {"experiment", "fixture", "arithmetic"},
        )
        return RenormalizationV2TheoryConfig(
            experiment=experiment,
            fixture=_require_literal(
                theory["fixture"],
                "fixture",
                (
                    "lf3_product_v1",
                    "lf3_correlated_v1",
                    "lf3_dirac_boundary_v1",
                ),
            ),
            arithmetic=_require_literal(
                theory["arithmetic"],
                "arithmetic",
                ("exact_rational",),
            ),
        )

    if experiment == "renormalization_v2_recursive":
        _require_exact_keys(
            theory,
            "theory",
            {"experiment", "fixture", "arithmetic"},
        )
        return RenormalizationV2RecursiveTheoryConfig(
            experiment=experiment,
            fixture=_require_literal(
                theory["fixture"],
                "fixture",
                ("lf4_two_parent_recursive_v1",),
            ),
            arithmetic=_require_literal(
                theory["arithmetic"],
                "arithmetic",
                ("exact_rational",),
            ),
        )

    if experiment == "categorical_falsification":
        _require_exact_keys(
            theory,
            "theory",
            {
                "experiment",
                "fixture",
                "admitted_family",
                "null_control_seeds",
                "descent_restarts",
                "arithmetic",
            },
        )
        return CategoricalFalsificationTheoryConfig(
            experiment=experiment,
            fixture=_require_literal(
                theory["fixture"], "fixture", ("two_channel_z3_v1",)
            ),
            admitted_family=_require_literal(
                theory["admitted_family"],
                "admitted_family",
                ("orbit", "simplex", "both"),
            ),
            null_control_seeds=_require_positive_int(
                theory["null_control_seeds"], "null_control_seeds"
            ),
            descent_restarts=_require_positive_int(
                theory["descent_restarts"], "descent_restarts"
            ),
            arithmetic=_require_literal(
                theory["arithmetic"], "arithmetic", ("exact_rational",)
            ),
        )

    raise ConfigError(
        "experiment must be one of: finite_exact, gaussian_realization, "
        "attention_marked_event, categorical_dqm, categorical_falsification, "
        + ", ".join(NEW_EXPERIMENT_NAMES)
    )


def _resolve_compute_config(
    compute: Mapping[str, object], theory: ExperimentTheoryConfig
) -> ComputeConfig:
    _require_exact_keys(
        compute,
        "compute",
        {
            "backend",
            "dtype",
            "device_index",
            "batch_size",
            "deterministic",
            "allow_tf32",
            "cpu_cuda_parity",
            "cuda_worker_python",
            "heavy_sweep_enabled",
        },
    )
    backend = _require_literal(compute["backend"], "backend", ("cpu", "cuda"))
    dtype = _require_literal(
        compute["dtype"], "dtype", ("float64", "float32", "bfloat16")
    )
    device_index = _require_int(compute["device_index"], "device_index")
    if device_index < 0:
        raise ConfigError("device_index must be a nonnegative int")
    batch_size = _require_positive_int(compute["batch_size"], "batch_size")
    deterministic = _require_bool(compute["deterministic"], "deterministic")
    allow_tf32 = _require_bool(compute["allow_tf32"], "allow_tf32")
    cpu_cuda_parity = _require_bool(
        compute["cpu_cuda_parity"], "cpu_cuda_parity"
    )
    cuda_worker_value = _require_str(
        compute["cuda_worker_python"], "cuda_worker_python"
    )
    cuda_worker_python = Path(cuda_worker_value)
    if not cuda_worker_python.is_absolute():
        raise ConfigError("cuda_worker_python must be an absolute path")
    heavy_sweep_enabled = _require_bool(
        compute["heavy_sweep_enabled"], "heavy_sweep_enabled"
    )

    exact_rational = getattr(theory, "arithmetic", None) == "exact_rational"
    if exact_rational and backend != "cpu":
        raise ConfigError("exact-rational experiments are CPU-only")
    if dtype in {"float32", "bfloat16"} and backend != "cuda":
        raise ConfigError("float32 and bfloat16 require CUDA")
    if dtype in {"float32", "bfloat16"} and not heavy_sweep_enabled:
        raise ConfigError("reduced precision requires heavy_sweep_enabled")
    if backend == "cuda" and not isinstance(theory, GaussianFixedRayTheoryConfig):
        raise ConfigError("CUDA is reserved for gaussian_fixed_ray in this freeze")
    if backend == "cuda" and not cpu_cuda_parity:
        raise ConfigError("CUDA requires cpu_cuda_parity")
    if backend == "cpu" and device_index != 0:
        raise ConfigError("CPU device_index must be 0")
    if allow_tf32 and not (
        backend == "cuda"
        and dtype == "float32"
        and heavy_sweep_enabled
        and not deterministic
    ):
        raise ConfigError("allow_tf32 requires CUDA float32 screening")

    return ComputeConfig(
        backend=backend,
        dtype=dtype,
        device_index=device_index,
        batch_size=batch_size,
        deterministic=deterministic,
        allow_tf32=allow_tf32,
        cpu_cuda_parity=cpu_cuda_parity,
        cuda_worker_python=cuda_worker_python,
        heavy_sweep_enabled=heavy_sweep_enabled,
    )


def canonical_config_json(config: ExperimentConfig) -> str:
    """Return an unambiguous serialization of a resolved configuration."""
    payload = asdict(config)
    payload["output"]["root"] = str(config.output.root)
    payload["compute"]["cuda_worker_python"] = str(
        config.compute.cuda_worker_python
    )
    payload.pop("_compute_explicit")
    if not config.compute_explicit:
        payload.pop("compute")
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


def _require_positive_int(value: object, field: str) -> int:
    value = _require_int(value, field)
    if value <= 0:
        raise ConfigError(f"{field} must be a positive int")
    return value


def _require_literal(
    value: object, field: str, allowed: tuple[str, ...]
) -> str:
    value = _require_str(value, field)
    if value not in allowed:
        if len(allowed) == 2:
            raise ConfigError(f"{field} must be '{allowed[0]}' or '{allowed[1]}'")
        raise ConfigError(f"{field} must be one of: {', '.join(allowed)}")
    return value


def _require_str_tuple(value: object, field: str) -> tuple[str, ...]:
    if type(value) not in {list, tuple}:
        raise ConfigError(f"{field} must be a list or tuple")
    values = tuple(value)
    for index, item in enumerate(values):
        if type(item) is not str:
            raise ConfigError(f"{field}[{index}] must be a str")
    return values


def _require_positive_float(value: object, field: str) -> float:
    if type(value) is not float or not math.isfinite(value) or value <= 0.0:
        raise ConfigError(f"{field} must be a positive finite float")
    return value


def _require_float_tuple(value: object, field: str) -> tuple[float, ...]:
    if type(value) not in {list, tuple}:
        raise ConfigError(f"{field} must be a list or tuple")
    values = tuple(value)
    for index, item in enumerate(values):
        if type(item) is not float or not math.isfinite(item):
            raise ConfigError(f"{field}[{index}] must be a finite float")
    return values


def _require_positive_float_tuple(value: object, field: str) -> tuple[float, ...]:
    if type(value) not in {list, tuple}:
        raise ConfigError(f"{field} must be a list or tuple")
    values = tuple(value)
    if not values:
        raise ConfigError(f"{field} must not be empty")
    for index, item in enumerate(values):
        if type(item) is not float or not math.isfinite(item) or item <= 0.0:
            raise ConfigError(f"{field}[{index}] must be a positive finite float")
    return values


def _require_bounded_float(
    value: object,
    field: str,
    *,
    minimum: float,
    maximum: float | None,
    minimum_inclusive: bool,
) -> float:
    valid_type_and_finite = type(value) is float and math.isfinite(value)
    valid_minimum = valid_type_and_finite and (
        value >= minimum if minimum_inclusive else value > minimum
    )
    valid_maximum = valid_type_and_finite and (
        maximum is None or value <= maximum
    )
    if not valid_minimum or not valid_maximum:
        if maximum is not None:
            raise ConfigError(f"{field} must be a finite float in (0, 1]")
        raise ConfigError(f"{field} must be a finite float at least 1")
    return value


def _require_bool(value: object, field: str) -> bool:
    if type(value) is not bool:
        raise ConfigError(f"{field} must be a bool")
    return value
