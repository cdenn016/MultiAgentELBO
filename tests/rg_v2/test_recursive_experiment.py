from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import shutil

import numpy as np
import pytest

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import (
    ExperimentConfig,
    RenormalizationV2TheoryConfig,
)
from multiagent_elbo.experiment_support import EXPERIMENT_REGISTRY
from rg_v2.coarse_agent import (
    _enumerate_coarse_population_independently,
    construct_coarse_information_interfaces,
    construct_coarse_population_joint,
    construct_coarse_recognition,
    derive_recursive_observation,
    validate_recursive_observation,
)
from rg_v2.contracts import (
    AgentRecognitionDatum,
    ExactProbabilityLaw,
    SelectorSpec,
)
import rg_v2.recursive_experiment as experiment_module
from rg_v2.recursive_experiment import (
    run_renormalization_v2_recursive_experiment,
)
from rg_v2.recursive_fixtures import RecursiveFixture, load_recursive_fixture
from rg_v2.population import (
    construct_population_joint,
    derive_population_inference,
    enumerate_population_joint_independently,
)


_JSON_STEMS = (
    "fixture_snapshot",
    "fine_population",
    "coarse_generative",
    "coarse_interfaces",
    "coarse_population",
    "all_observation_inference",
    "metrics",
)
_ARTIFACT_STEMS = (*_JSON_STEMS, "arrays")
_CORE_FILES = ("config.json", "manifest.json")
_ARTIFACT_FILES = tuple(f"{name}.json" for name in _JSON_STEMS) + (
    "arrays.npz",
)
_PROVENANCE_ARRAYS = (
    "schema_version",
    "fixture_id",
    "producer_commit",
    "config_hash",
    "direct_input_names",
    "direct_input_sha256",
)
_FLOAT_ARRAYS = (
    "fine_population",
    "fine_population_oracle",
    "coarse_pushed_population",
    "coarse_reconstructed_population",
    "fine_recognition",
    "coarse_recognition",
    "fine_evidences",
    "coarse_evidences",
    "pushed_posteriors",
    "coarse_posteriors",
    "coarse_update_A",
    "coarse_update_B",
    "sparse_conditional_tv",
    "metric_values",
    "metric_tolerances",
)


def _config(
    root: Path,
    *,
    collect_diagnostics: bool = True,
    render_figures: bool = False,
    atol: float = 1.0e-12,
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "renormalization-v2-recursive", "seed": 20260821},
        {
            "experiment": "renormalization_v2_recursive",
            "fixture": "lf4_two_parent_recursive_v1",
            "arithmetic": "exact_rational",
        },
        {
            "dtype": "float64",
            "atol": atol,
            "rtol": 1.0e-12,
            "min_spd_rcond": 1.0e-12,
            "max_frame_condition": 1.0e12,
        },
        {
            "root": root,
            "collect_diagnostics": collect_diagnostics,
            "render_figures": render_figures,
        },
    )


def _read_json(run_dir: Path, stem: str) -> dict[str, object]:
    payload = json.loads((run_dir / f"{stem}.json").read_text(encoding="utf-8"))
    assert type(payload) is dict
    return payload


def _canonical_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _canonical_sha256(payload: object) -> str:
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _direct_inputs(envelope: dict[str, object]) -> tuple[tuple[str, str], ...]:
    records = envelope["direct_inputs"]
    assert type(records) is list
    return tuple((record["name"], record["sha256"]) for record in records)


def _fraction(payload: object) -> Fraction:
    assert type(payload) is dict
    assert set(payload) == {"numerator", "denominator"}
    numerator = payload["numerator"]
    denominator = payload["denominator"]
    assert type(numerator) is int
    assert type(denominator) is int and denominator > 0
    value = Fraction(numerator, denominator)
    assert (value.numerator, value.denominator) == (numerator, denominator)
    return value


def _vector(payload: object) -> tuple[Fraction, ...]:
    assert type(payload) is list
    return tuple(_fraction(value) for value in payload)


def _matrix(payload: object) -> tuple[tuple[Fraction, ...], ...]:
    assert type(payload) is list
    return tuple(_vector(row) for row in payload)


def _law(payload: object) -> tuple[tuple[str, ...], tuple[Fraction, ...]]:
    assert type(payload) is dict
    assert set(payload) == {"labels", "masses"}
    labels = payload["labels"]
    assert type(labels) is list and all(type(label) is str for label in labels)
    return tuple(labels), _vector(payload["masses"])


def _observation(label: str) -> tuple[tuple[str, str], ...]:
    decoded = json.loads(label)
    return tuple((str(record_id), str(outcome)) for record_id, outcome in decoded)


def _semantic_subhashes(fixture: RecursiveFixture) -> dict[str, str]:
    result = dict(fixture.subrecord_sha256)
    assert tuple(result) == ("generative", "recognition", "structure", "access")
    return result


def _assert_no_forbidden_generative_fields(value: object) -> None:
    forbidden = {
        "access",
        "access_specs",
        "update",
        "updates",
        "recognition",
        "recognitions",
        "selector",
        "realized_observation",
        "observed_record",
        "evidence",
        "evidence_measure",
        "posterior",
    }
    if type(value) is dict:
        assert forbidden.isdisjoint(value)
        for child in value.values():
            _assert_no_forbidden_generative_fields(child)
    elif type(value) is list:
        for child in value:
            _assert_no_forbidden_generative_fields(child)


def test_recursive_publication_has_exact_dag_metrics_arrays_and_science(
    tmp_path: Path,
) -> None:
    fixture = load_recursive_fixture("lf4_two_parent_recursive_v1")
    result = run_renormalization_v2_recursive_experiment(_config(tmp_path))
    contract = EXPERIMENT_REGISTRY["renormalization_v2_recursive"]

    assert contract.artifact_inventory == _ARTIFACT_STEMS
    assert tuple(result.metrics) == contract.metric_inventory
    assert result.status == "pass"
    assert tuple(sorted(path.name for path in result.run_dir.iterdir())) == tuple(
        sorted(_CORE_FILES + _ARTIFACT_FILES)
    )
    manifest = _read_json(result.run_dir, "manifest")
    assert manifest["complete"] is True
    assert manifest["artifacts"] == {
        name: "complete" for name in sorted(_CORE_FILES + _ARTIFACT_FILES)
    }

    envelopes = {name: _read_json(result.run_dir, name) for name in _JSON_STEMS}
    assert all(
        envelope["schema_version"] == "rg-v2-recursive-phase2-artifact-v1"
        for envelope in envelopes.values()
    )
    hashes = {name: _canonical_sha256(envelope) for name, envelope in envelopes.items()}
    subhashes = _semantic_subhashes(fixture)
    assert _direct_inputs(envelopes["fixture_snapshot"]) == (
        ("fixture_raw", fixture.fixture_sha256),
        *(fixture.subrecord_sha256),
    )
    assert _direct_inputs(envelopes["fine_population"]) == (
        ("generative", subhashes["generative"]),
    )
    assert _direct_inputs(envelopes["coarse_generative"]) == (
        ("fine_population", hashes["fine_population"]),
        ("structure", subhashes["structure"]),
    )
    assert _direct_inputs(envelopes["coarse_interfaces"]) == (
        ("coarse_generative", hashes["coarse_generative"]),
        ("access", subhashes["access"]),
        ("recognition", subhashes["recognition"]),
    )
    assert _direct_inputs(envelopes["coarse_population"]) == (
        ("coarse_generative", hashes["coarse_generative"]),
    )
    scientific_names = _JSON_STEMS[:-1]
    assert _direct_inputs(envelopes["all_observation_inference"]) == (
        ("fine_population", hashes["fine_population"]),
        ("coarse_interfaces", hashes["coarse_interfaces"]),
        ("coarse_population", hashes["coarse_population"]),
    )
    assert _direct_inputs(envelopes["metrics"]) == tuple(
        (name, hashes[name]) for name in scientific_names
    )

    generative_payload = envelopes["coarse_generative"]["payload"]
    _assert_no_forbidden_generative_fields(generative_payload)
    assert _canonical_bytes(generative_payload) == _canonical_bytes(
        json.loads(_canonical_bytes(generative_payload))
    )

    fine_population = construct_population_joint(
        fixture.agents, fixture.records, fixture.context_id
    )
    fine_oracle = enumerate_population_joint_independently(
        fixture.agents, fixture.records, fixture.context_id
    )
    assert fine_population == fine_oracle
    coarse_population = construct_coarse_population_joint(
        fine_population, fixture.structure
    )
    coarse_oracle = _enumerate_coarse_population_independently(
        fine_population, fixture.structure
    )
    assert coarse_population == coarse_oracle
    information = construct_coarse_information_interfaces(
        coarse_population, fixture.access_specs
    )
    observation_records = envelopes["all_observation_inference"]["payload"][
        "observations"
    ]
    assert type(observation_records) is list and len(observation_records) == 16
    assert tuple(record["fine_observed_record"] for record in observation_records) == (
        fixture.structure.observation.fine_observation_labels
    )
    for fine_label, stored in zip(
        fixture.structure.observation.fine_observation_labels,
        observation_records,
        strict=True,
    ):
        fine_inference = derive_population_inference(
            fine_population,
            _observation(fine_label),
            fixture.recognitions,
            fixture.selector,
        )
        coarse_agents = construct_coarse_recognition(
            coarse_population, information, fine_inference
        )
        recursive = derive_recursive_observation(
            coarse_population, coarse_agents, fine_inference
        )
        validate_recursive_observation(recursive, coarse_population, _config(tmp_path / "unused").numerics)
        assert stored["coarse_observed_record"] == recursive.coarse_observed_record
        assert _fraction(stored["fine_evidence"]) == fine_inference.evidence
        assert _fraction(stored["coarse_evidence"]) == recursive.coarse_inference.evidence
        assert _law(stored["pushed_recognition"]) == (
            recursive.pushed_recognition.labels,
            recursive.pushed_recognition.masses,
        )
        assert _law(stored["coarse_recognition"]) == (
            recursive.coarse_inference.recognition.labels,
            recursive.coarse_inference.recognition.masses,
        )
        assert _law(stored["pushed_posterior"]) == (
            recursive.pushed_posterior.labels,
            recursive.pushed_posterior.masses,
        )
        assert _law(stored["coarse_posterior"]) == (
            recursive.coarse_inference.posterior.labels,
            recursive.coarse_inference.posterior.masses,
        )

    records = envelopes["metrics"]["payload"]["records"]
    assert type(records) is list and len(records) == 20
    names = tuple(record["name"] for record in records)
    assert names == contract.metric_inventory and len(set(names)) == 20
    serialized = tuple(record["record"] for record in records)
    assert all(record["status"] == "pass" for record in serialized)
    assert all(record["assessment_scope"] == "implementation_check" for record in serialized)
    assert all(record["verification_state"] == "CANDIDATE" for record in serialized)
    assert all(record["theorem_status"] for record in serialized)
    assert all(record["claim_origin"] for record in serialized)
    assert serialized[15]["value"] >= 2.0
    assert serialized[16]["value"] == 0.0
    assert serialized[17]["value"] >= 1.0
    assert serialized[18]["value"] >= -1.0e-12
    assert serialized[19]["value"] <= 1.0e-12

    assert tuple(result.arrays) == (*_PROVENANCE_ARRAYS, *_FLOAT_ARRAYS)
    assert all(array.flags.c_contiguous for array in result.arrays.values())
    assert all(not array.flags.writeable for array in result.arrays.values())
    with np.load(result.run_dir / "arrays.npz", allow_pickle=False) as archive:
        assert tuple(archive.files) == (*_PROVENANCE_ARRAYS, *_FLOAT_ARRAYS)
        assert all(archive[name].dtype.kind == "U" for name in _PROVENANCE_ARRAYS)
        assert all(archive[name].dtype == np.float64 for name in _FLOAT_ARRAYS)
        assert all(archive[name].dtype != object for name in archive.files)
        array_inputs = tuple(
            (name, hashes[name]) for name in (*scientific_names, "metrics")
        )
        assert tuple(archive["direct_input_names"].tolist()) == tuple(
            name for name, _ in array_inputs
        )
        assert tuple(archive["direct_input_sha256"].tolist()) == tuple(
            sha256 for _, sha256 in array_inputs
        )


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("wrong_theory", "theory.experiment='renormalization_v2_recursive'"),
        ("wrong_arithmetic", "exact_rational"),
        ("nondeterministic", "deterministic CPU float64"),
        ("cuda", "deterministic CPU float64"),
        ("compute_float32", "deterministic CPU float64"),
        ("numerics_float32", "float64 numerics"),
        ("zero_atol", "positive finite"),
        ("loose_atol", "at most 1e-12"),
        ("no_diagnostics", "collect_diagnostics=True"),
        ("figures", "render_figures=False"),
    ],
)
def test_invalid_config_is_rejected_before_all_effect_boundaries(
    mutation: str,
    message: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _config(tmp_path)
    if mutation == "wrong_theory":
        config = replace(
            config,
            theory=RenormalizationV2TheoryConfig(
                "renormalization_v2", "lf3_product_v1", "exact_rational"
            ),
        )
    elif mutation == "wrong_arithmetic":
        config = replace(config, theory=replace(config.theory, arithmetic="float"))
    elif mutation == "nondeterministic":
        config = replace(config, compute=replace(config.compute, deterministic=False))
    elif mutation == "cuda":
        config = replace(config, compute=replace(config.compute, backend="cuda"))
    elif mutation == "compute_float32":
        config = replace(config, compute=replace(config.compute, dtype="float32"))
    elif mutation == "numerics_float32":
        config = replace(config, numerics=replace(config.numerics, dtype="float32"))
    elif mutation == "zero_atol":
        config = replace(config, numerics=replace(config.numerics, atol=0.0))
    elif mutation == "loose_atol":
        config = replace(config, numerics=replace(config.numerics, atol=1.0e-11))
    elif mutation == "no_diagnostics":
        config = replace(config, output=replace(config.output, collect_diagnostics=False))
    else:
        config = replace(config, output=replace(config.output, render_figures=True))

    monkeypatch.setattr(experiment_module, "load_recursive_fixture", lambda *_: pytest.fail("fixture read"))
    monkeypatch.setattr(experiment_module.RngStreams, "from_seed", lambda *_: pytest.fail("RNG created"))
    monkeypatch.setattr(experiment_module, "collect_provenance", lambda *_: pytest.fail("provenance collected"))
    monkeypatch.setattr(experiment_module.RunStore, "create", lambda *_: pytest.fail("store created"))
    with pytest.raises((TypeError, ValueError), match=message):
        run_renormalization_v2_recursive_experiment(config)
    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_science_completes_before_rng_provenance_store_and_fixture_loads_once(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []
    real_load = experiment_module.load_recursive_fixture
    real_rng = experiment_module.RngStreams.from_seed.__func__
    real_provenance = experiment_module.collect_provenance
    real_create = RunStore.create.__func__

    def load_once(name: str) -> RecursiveFixture:
        events.append("load")
        return real_load(name)

    def rng(cls: type[object], seed: int) -> object:
        events.append("rng")
        return real_rng(cls, seed)

    def provenance(*args: object) -> dict[str, object]:
        events.append("provenance")
        return real_provenance(*args)

    def create(
        cls: type[RunStore],
        config: ExperimentConfig,
        provenance_data: dict[str, object],
    ) -> RunStore:
        events.append("store")
        hashes = provenance_data["semantic_artifact_sha256"]
        assert tuple(hashes) == _ARTIFACT_STEMS
        assert all(type(value) is str and len(value) == 64 for value in hashes.values())
        return real_create(cls, config, provenance_data)

    monkeypatch.setattr(experiment_module, "load_recursive_fixture", load_once)
    monkeypatch.setattr(experiment_module.RngStreams, "from_seed", classmethod(rng))
    monkeypatch.setattr(experiment_module, "collect_provenance", provenance)
    monkeypatch.setattr(experiment_module.RunStore, "create", classmethod(create))
    run_renormalization_v2_recursive_experiment(_config(tmp_path))
    assert events == ["load", "rng", "provenance", "store"]


def test_scientific_failure_has_no_rng_provenance_or_filesystem_effect(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        experiment_module,
        "_enumerate_coarse_population_independently",
        lambda *_: (_ for _ in ()).throw(ArithmeticError("coarse oracle failure")),
    )
    monkeypatch.setattr(experiment_module.RngStreams, "from_seed", lambda *_: pytest.fail("RNG created"))
    monkeypatch.setattr(experiment_module, "collect_provenance", lambda *_: pytest.fail("provenance collected"))
    monkeypatch.setattr(experiment_module.RunStore, "create", lambda *_: pytest.fail("store created"))
    with pytest.raises(ArithmeticError, match="coarse oracle failure"):
        run_renormalization_v2_recursive_experiment(_config(tmp_path))
    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def _product_selector(
    fixture: RecursiveFixture,
    recognitions: tuple[AgentRecognitionDatum, ...],
) -> SelectorSpec:
    population = construct_population_joint(
        fixture.agents, fixture.records, fixture.context_id
    )
    masses = tuple(
        np.prod([recognitions[index].joint.masses[state] for index, state in enumerate(indices)])
        for indices in product(range(4), repeat=4)
    )
    return SelectorSpec(
        "task6-product-selector",
        "declared_correlated",
        ExactProbabilityLaw(population.latent_labels, tuple(Fraction(value) for value in masses)),
    )


def test_coarse_generative_bytes_ignore_recognition_selector_and_default_observation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = load_recursive_fixture("lf4_two_parent_recursive_v1")
    config = _config(tmp_path / "runs")
    variants: list[RecursiveFixture] = [fixture]
    altered_recognitions = tuple(
        AgentRecognitionDatum(
            agent,
            ExactProbabilityLaw(
                agent.state_labels,
                (Fraction(1, 10), Fraction(2, 10), Fraction(3, 10), Fraction(4, 10)),
            ),
        )
        for agent in fixture.agents
    )
    variants.append(
        replace(
            fixture,
            recognitions=altered_recognitions,
            selector=_product_selector(fixture, altered_recognitions),
        )
    )
    variants.append(
        replace(fixture, selector=_product_selector(fixture, fixture.recognitions))
    )
    variants.append(
        replace(
            fixture,
            observation=_observation(
                fixture.structure.observation.fine_observation_labels[1]
            ),
        )
    )
    generative_bytes: list[bytes] = []
    generative_hashes: list[str] = []
    interface_payloads: list[object] = []
    for index, variant in enumerate(variants):
        monkeypatch.setattr(experiment_module, "load_recursive_fixture", lambda _name, value=variant: value)
        result = run_renormalization_v2_recursive_experiment(config)
        envelope = _read_json(result.run_dir, "coarse_generative")
        generative_bytes.append((result.run_dir / "coarse_generative.json").read_bytes())
        generative_hashes.append(_canonical_sha256(envelope))
        interface_payloads.append(_read_json(result.run_dir, "coarse_interfaces")["payload"])
        shutil.move(str(result.run_dir), str(tmp_path / f"saved-{index}"))
    assert len(set(generative_bytes)) == 1
    assert len(set(generative_hashes)) == 1
    assert interface_payloads[0] != interface_payloads[1]
    assert interface_payloads[0] != interface_payloads[2]


def test_mathematics_is_equal_across_output_roots_without_provenance_equality(
    tmp_path: Path,
) -> None:
    first = run_renormalization_v2_recursive_experiment(_config(tmp_path / "first"))
    second = run_renormalization_v2_recursive_experiment(_config(tmp_path / "second"))
    assert first.config_hash != second.config_hash
    assert first.metrics == second.metrics
    for name in _JSON_STEMS:
        assert _read_json(first.run_dir, name)["payload"] == _read_json(second.run_dir, name)["payload"]
    for name in _FLOAT_ARRAYS:
        np.testing.assert_array_equal(first.arrays[name], second.arrays[name])
