from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.experiment_support import EXPERIMENT_REGISTRY
import rg_v2.experiment as experiment_module
from rg_v2.experiment import run_renormalization_v2_experiment
from rg_v2.fixtures import LocalFirstFixture


_FIXTURE_IDS = (
    "lf3_product_v1",
    "lf3_correlated_v1",
    "lf3_dirac_boundary_v1",
)
_JSON_ARTIFACTS = (
    "fixture_snapshot",
    "population_joint",
    "population_inference",
    "aggregate_datum",
    "metrics",
)
_ARTIFACT_FILES = tuple(f"{name}.json" for name in _JSON_ARTIFACTS) + (
    "arrays.npz",
)
_CORE_FILES = ("config.json", "manifest.json")
_NPZ_PROVENANCE = (
    "schema_version",
    "fixture_id",
    "producer_commit",
    "config_hash",
    "direct_input_names",
    "direct_input_sha256",
)


def _config(
    root: Path,
    fixture_id: str,
    *,
    collect_diagnostics: bool = True,
    render_figures: bool = False,
    atol: float = 1.0e-12,
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": f"renormalization-v2-{fixture_id}", "seed": 20260821},
        {
            "experiment": "renormalization_v2",
            "fixture": fixture_id,
            "arithmetic": "exact_rational",
        },
        {
            "dtype": "float64",
            "atol": atol,
            "rtol": 1.0e-10,
            "min_spd_rcond": 1.0e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": root,
            "collect_diagnostics": collect_diagnostics,
            "render_figures": render_figures,
        },
    )


def _read_json(run_dir: Path, stem: str) -> dict[str, object]:
    payload = json.loads((run_dir / f"{stem}.json").read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _canonical_sha256(payload: object) -> str:
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _direct_inputs(envelope: dict[str, object]) -> tuple[tuple[str, str], ...]:
    records = envelope["direct_inputs"]
    assert isinstance(records, list)
    return tuple((record["name"], record["sha256"]) for record in records)


def _metric_records(envelope: dict[str, object]) -> dict[str, dict[str, object]]:
    payload = envelope["payload"]
    assert isinstance(payload, dict)
    records = payload["records"]
    assert isinstance(records, list)
    return {record["name"]: record["record"] for record in records}


@pytest.mark.parametrize("fixture_id", _FIXTURE_IDS)
def test_every_fixture_publishes_the_complete_release_contract(
    fixture_id: str,
    tmp_path: Path,
) -> None:
    result = run_renormalization_v2_experiment(_config(tmp_path, fixture_id))

    contract = EXPERIMENT_REGISTRY["renormalization_v2"]
    assert contract.artifact_inventory == (
        "fixture_snapshot",
        "population_joint",
        "population_inference",
        "aggregate_datum",
        "metrics",
        "arrays",
    )
    assert tuple(result.metrics) == contract.metric_inventory
    assert result.status == "pass"
    assert tuple(sorted(path.name for path in result.run_dir.iterdir())) == tuple(
        sorted(_CORE_FILES + _ARTIFACT_FILES)
    )

    manifest = _read_json(result.run_dir, "manifest")
    assert manifest["complete"] is True
    assert manifest["config_hash"] == result.config_hash
    assert manifest["artifacts"] == {
        filename: "complete" for filename in sorted(_CORE_FILES + _ARTIFACT_FILES)
    }

    envelopes = {name: _read_json(result.run_dir, name) for name in _JSON_ARTIFACTS}
    for envelope in envelopes.values():
        assert envelope["schema_version"] == "rg-v2-release-1-artifact-v1"
        assert envelope["fixture_id"] == fixture_id
        assert envelope["producer_commit"] == manifest["provenance"]["git_commit"]
        assert envelope["config_hash"] == result.config_hash
        assert isinstance(envelope["direct_inputs"], list)
        assert isinstance(envelope["payload"], dict)

    hashes = {name: _canonical_sha256(envelope) for name, envelope in envelopes.items()}
    fixture_payload = envelopes["fixture_snapshot"]["payload"]
    assert fixture_payload["fixture_sha256"]
    assert fixture_payload["agents"]
    assert fixture_payload["recognitions"]
    assert fixture_payload["records"]
    assert fixture_payload["selector"]
    assert fixture_payload["coarse_channel"]
    assert "fixture_path" not in json.dumps(fixture_payload)

    fixture_sources = tuple(
        (record["name"], record["sha256"])
        for record in fixture_payload["source_inputs"]
    )
    assert _direct_inputs(envelopes["fixture_snapshot"]) == fixture_sources
    assert _direct_inputs(envelopes["population_joint"]) == (
        ("fixture_snapshot", hashes["fixture_snapshot"]),
    )
    assert _direct_inputs(envelopes["population_inference"]) == (
        ("fixture_snapshot", hashes["fixture_snapshot"]),
        ("population_joint", hashes["population_joint"]),
    )
    channel_hash = fixture_payload["coarse_channel"]["channel_sha256"]
    assert _direct_inputs(envelopes["aggregate_datum"]) == (
        ("fixture_snapshot", hashes["fixture_snapshot"]),
        ("population_inference", hashes["population_inference"]),
        ("coarse_channel", channel_hash),
    )
    assert _direct_inputs(envelopes["metrics"]) == tuple(
        (name, hashes[name])
        for name in (
            "fixture_snapshot",
            "population_joint",
            "population_inference",
            "aggregate_datum",
        )
    )

    population_payload = envelopes["population_joint"]["payload"]
    assert population_payload["population"] == population_payload["independent_population"]
    assert population_payload["independent_population_residual"] == {
        "numerator": 0,
        "denominator": 1,
    }
    metric_records = _metric_records(envelopes["metrics"])
    assert tuple(metric_records) == contract.metric_inventory
    assert metric_records["independent_population_residual"]["value"] == 0.0
    assert all(
        record["assessment_scope"] == "implementation_check"
        for record in metric_records.values()
    )
    assert all(record["verification_state"] == "CANDIDATE" for record in metric_records.values())
    assert all(record["theorem_status"] for record in metric_records.values())
    assert all(record["claim_origin"] for record in metric_records.values())

    with np.load(result.run_dir / "arrays.npz", allow_pickle=False) as archive:
        assert set(_NPZ_PROVENANCE) <= set(archive.files)
        assert all(archive[name].dtype.kind == "U" for name in _NPZ_PROVENANCE)
        assert all(archive[name].dtype != object for name in archive.files)
        assert str(archive["schema_version"].item()) == "rg-v2-release-1-artifact-v1"
        assert str(archive["fixture_id"].item()) == fixture_id
        assert str(archive["producer_commit"].item()) == envelopes["metrics"]["producer_commit"]
        assert str(archive["config_hash"].item()) == result.config_hash
        expected_array_inputs = tuple(
            (name, hashes[name])
            for name in (
                "fixture_snapshot",
                "population_joint",
                "population_inference",
                "aggregate_datum",
                "metrics",
            )
        )
        assert tuple(archive["direct_input_names"].tolist()) == tuple(
            name for name, _ in expected_array_inputs
        )
        assert tuple(archive["direct_input_sha256"].tolist()) == tuple(
            sha256 for _, sha256 in expected_array_inputs
        )
        assert archive["population_joint"].dtype == np.float64
        assert archive["independent_population_joint"].dtype == np.float64
        np.testing.assert_array_equal(
            archive["population_joint"], archive["independent_population_joint"]
        )


@pytest.mark.parametrize(
    ("collect_diagnostics", "render_figures", "message"),
    [
        (False, False, "collect_diagnostics=True"),
        (True, True, "render_figures=False"),
    ],
)
def test_output_modes_are_rejected_before_fixture_rng_or_publication(
    collect_diagnostics: bool,
    render_figures: bool,
    message: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _config(
        tmp_path,
        "lf3_product_v1",
        collect_diagnostics=collect_diagnostics,
        render_figures=render_figures,
    )
    monkeypatch.setattr(
        experiment_module,
        "load_fixture",
        lambda _: pytest.fail("fixture loaded before output validation"),
    )
    monkeypatch.setattr(
        experiment_module.RngStreams,
        "from_seed",
        lambda _: pytest.fail("RNG created before output validation"),
    )
    monkeypatch.setattr(
        experiment_module.RunStore,
        "create",
        lambda *_: pytest.fail("RunStore created before output validation"),
    )

    with pytest.raises(ValueError, match=message):
        run_renormalization_v2_experiment(config)

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_loose_atol_is_rejected_before_fixture_rng_or_publication(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _config(tmp_path, "lf3_product_v1", atol=1.0e-11)
    monkeypatch.setattr(
        experiment_module,
        "load_fixture",
        lambda _: pytest.fail("fixture loaded before tolerance validation"),
    )
    monkeypatch.setattr(
        experiment_module.RngStreams,
        "from_seed",
        lambda _: pytest.fail("RNG created before tolerance validation"),
    )
    monkeypatch.setattr(
        experiment_module.RunStore,
        "create",
        lambda *_: pytest.fail("RunStore created before tolerance validation"),
    )

    with pytest.raises(ValueError, match="at most 1e-12"):
        run_renormalization_v2_experiment(config)

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_cpu_float64_deterministic_contract_is_enforced_before_fixture_load(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _config(tmp_path, "lf3_product_v1")
    invalid_compute = replace(config.compute, deterministic=False)
    invalid_config = replace(config, compute=invalid_compute)
    monkeypatch.setattr(
        experiment_module,
        "load_fixture",
        lambda _: pytest.fail("fixture loaded before compute validation"),
    )

    with pytest.raises(ValueError, match="deterministic CPU float64"):
        run_renormalization_v2_experiment(invalid_config)


def test_scientific_failure_precedes_rng_provenance_and_filesystem_effects(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _config(tmp_path, "lf3_product_v1")
    monkeypatch.setattr(
        experiment_module,
        "enumerate_population_joint_independently",
        lambda *_: (_ for _ in ()).throw(ArithmeticError("independent failure")),
    )
    monkeypatch.setattr(
        experiment_module.RngStreams,
        "from_seed",
        lambda _: pytest.fail("RNG created after failed science"),
    )
    monkeypatch.setattr(
        experiment_module,
        "collect_provenance",
        lambda *_: pytest.fail("provenance collected after failed science"),
    )
    monkeypatch.setattr(
        experiment_module.RunStore,
        "create",
        lambda *_: pytest.fail("RunStore created after failed science"),
    )

    with pytest.raises(ArithmeticError, match="independent failure"):
        run_renormalization_v2_experiment(config)

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_fixture_is_loaded_once_and_complete_hash_plan_precedes_runstore_create(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    load_calls: list[str] = []
    real_load = experiment_module.load_fixture
    real_create = RunStore.create.__func__

    def load_once(fixture_id: str) -> LocalFirstFixture:
        load_calls.append(fixture_id)
        return real_load(fixture_id)

    def checked_create(
        cls: type[RunStore],
        config: ExperimentConfig,
        provenance: dict[str, object],
    ) -> RunStore:
        artifact_hashes = provenance["semantic_artifact_sha256"]
        assert tuple(artifact_hashes) == (
            "fixture_snapshot",
            "population_joint",
            "population_inference",
            "aggregate_datum",
            "metrics",
            "arrays",
        )
        assert all(len(value) == 64 for value in artifact_hashes.values())
        assert tuple(provenance["arrays_direct_inputs"]) == (
            "fixture_snapshot",
            "population_joint",
            "population_inference",
            "aggregate_datum",
            "metrics",
        )
        return real_create(cls, config, provenance)

    monkeypatch.setattr(experiment_module, "load_fixture", load_once)
    monkeypatch.setattr(
        experiment_module.RunStore,
        "create",
        classmethod(checked_create),
    )

    run_renormalization_v2_experiment(_config(tmp_path, "lf3_product_v1"))

    assert load_calls == ["lf3_product_v1"]


def test_mathematical_results_are_equal_across_output_roots(
    tmp_path: Path,
) -> None:
    first = run_renormalization_v2_experiment(
        _config(tmp_path / "first", "lf3_correlated_v1")
    )
    second = run_renormalization_v2_experiment(
        _config(tmp_path / "second", "lf3_correlated_v1")
    )

    assert first.config_hash != second.config_hash
    assert first.metrics == second.metrics
    for name in _JSON_ARTIFACTS:
        assert _read_json(first.run_dir, name)["payload"] == _read_json(
            second.run_dir, name
        )["payload"]
    with (
        np.load(first.run_dir / "arrays.npz", allow_pickle=False) as first_arrays,
        np.load(second.run_dir / "arrays.npz", allow_pickle=False) as second_arrays,
    ):
        science_names = tuple(
            name for name in first_arrays.files if name not in _NPZ_PROVENANCE
        )
        assert science_names == tuple(
            name for name in second_arrays.files if name not in _NPZ_PROVENANCE
        )
        for name in science_names:
            np.testing.assert_array_equal(first_arrays[name], second_arrays[name])
