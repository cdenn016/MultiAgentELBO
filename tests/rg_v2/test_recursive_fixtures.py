"""Public-loader tests for the LF4 recursive primitive witness."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path

import pytest

import rg_v2.recursive_fixtures as recursive_fixtures
from rg_v2.recursive_fixtures import load_recursive_fixture


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "rg_v2" / "data"
NAME = "lf4_two_parent_recursive_v1"


def _payload() -> dict[str, object]:
    return json.loads((DATA / f"{NAME}.json").read_text(encoding="utf-8"))


def _load_mutated(monkeypatch: pytest.MonkeyPatch, payload: dict[str, object]) -> object:
    path = (DATA / f"{NAME}.json").resolve()
    original_read_bytes = recursive_fixtures.Path.read_bytes
    raw = json.dumps(payload, ensure_ascii=True, separators=(",", ":"), indent=2).encode("utf-8")

    def read_mutated_bytes(candidate: Path) -> bytes:
        if candidate.resolve() == path:
            return raw
        return original_read_bytes(candidate)

    monkeypatch.setattr(recursive_fixtures.Path, "read_bytes", read_mutated_bytes)
    return load_recursive_fixture(NAME)


def test_flagship_fixture_is_primitive_positive_and_exact() -> None:
    fixture = load_recursive_fixture(NAME)

    assert tuple(agent.agent_id for agent in fixture.agents) == ("a0", "a1", "a2", "a3")
    assert tuple(record.record_id for record in fixture.records) == ("r0", "r1", "r2", "r3")
    assert fixture.structure.source_agent_order == ("a0", "a1", "a2", "a3")
    assert fixture.structure.coarse_agent_order == ("A", "B")
    assert len(fixture.structure.observation.fine_observation_labels) == 16
    assert fixture.observation == (("r0", "1"), ("r1", "1"), ("r2", "1"), ("r3", "1"))
    assert tuple(name for name, _ in fixture.subrecord_sha256) == ("generative", "recognition", "structure", "access")
    assert fixture.fixture_sha256 == hashlib.sha256(fixture.fixture_path.read_bytes()).hexdigest()
    assert all(mass > 0 for agent in fixture.agents for row in agent.generative_kernel.matrix for mass in row)
    assert all(mass > 0 for record in fixture.records for row in record.kernel.matrix for mass in row)


def test_declared_fine_coupling_is_correlated_with_uniform_local_marginals() -> None:
    fixture = load_recursive_fixture(NAME)

    coupling = fixture.selector.coupling
    assert coupling is not None
    assert coupling.masses.count(Fraction(1, 128)) == 128
    assert coupling.masses.count(Fraction(0)) == 128
    assert all(recognition.joint.masses == (Fraction(1, 4),) * 4 for recognition in fixture.recognitions)


@pytest.mark.parametrize(
    "path",
    (
        ("population",),
        ("agents", 0, "posterior"),
        ("agents", 0, "evaluator", 0, "inference"),
        ("recognitions", 0, "evidence"),
        ("records", 0, "coarse_result"),
        ("selector", "coupling", "aggregate"),
        ("recursive_structure", "agents", 0, "vfe"),
        ("access_specs", 0, "status"),
    ),
)
def test_public_loader_recursively_rejects_derived_keys(monkeypatch: pytest.MonkeyPatch, path: tuple[object, ...]) -> None:
    payload = _payload()
    target: object = payload
    for key in path[:-1]:
        target = target[key]  # type: ignore[index]
    target[path[-1]] = None  # type: ignore[index]

    with pytest.raises(ValueError, match="prohibited derived fixture key"):
        _load_mutated(monkeypatch, payload)


def test_public_loader_rejects_nonpositive_rational_denominator(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _payload()
    payload["agents"][0]["generative_rows"][0][0]["denominator"] = 0  # type: ignore[index]

    with pytest.raises(ValueError, match="denominator must be positive"):
        _load_mutated(monkeypatch, payload)


def test_public_loader_rejects_changed_agent_evaluator_row(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _payload()
    payload["agents"][1]["evaluator"][0]["rows"][0][0] = {"numerator": 3, "denominator": 4}  # type: ignore[index]

    with pytest.raises(ValueError, match="generative/evaluator"):
        _load_mutated(monkeypatch, payload)


def test_public_loader_rejects_missing_record_source_row(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _payload()
    payload["records"][1]["rows"].pop()  # type: ignore[index]

    with pytest.raises(ValueError, match="record rows"):
        _load_mutated(monkeypatch, payload)


def test_public_loader_rejects_broken_block_partition(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _payload()
    payload["recursive_structure"]["agents"][1]["source_agent_ids"] = ["a1", "a2"]  # type: ignore[index]

    with pytest.raises(ValueError, match="source blocks must be disjoint and exhaustive"):
        _load_mutated(monkeypatch, payload)


def test_public_loader_rejects_reordered_observation_bijection(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _payload()
    outcomes = payload["recursive_structure"]["observation"]["compound_outcome_by_fine_observation"]  # type: ignore[index]
    outcomes[0], outcomes[1] = outcomes[1], outcomes[0]  # type: ignore[index]

    with pytest.raises(ValueError, match="canonical fine-observation order"):
        _load_mutated(monkeypatch, payload)


def test_public_loader_rejects_changed_identity_access_label(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _payload()
    payload["access_specs"][0]["information_labels"][0] = "not-the-observation"  # type: ignore[index]

    with pytest.raises(ValueError, match="identity access"):
        _load_mutated(monkeypatch, payload)


@pytest.mark.parametrize("invalid", ("lf4_two_parent_recursive_v2", "../lf4_two_parent_recursive_v1", "lf4_two_parent_recursive_v1.json", 7))
def test_invalid_recursive_fixture_name_is_rejected_before_any_read(monkeypatch: pytest.MonkeyPatch, invalid: object) -> None:
    def forbidden_read(_: Path) -> bytes:
        raise AssertionError("fixture read occurred")

    monkeypatch.setattr(recursive_fixtures.Path, "read_bytes", forbidden_read)

    with pytest.raises((TypeError, ValueError), match="fixture"):
        load_recursive_fixture(invalid)  # type: ignore[arg-type]


def test_literal_fixture_tables_are_complete_and_canonical() -> None:
    payload = _payload()
    fixture = load_recursive_fixture(NAME)
    coupling = fixture.selector.coupling

    assert set(payload) == {"schema_version", "fixture_id", "context_id", "agents", "recognitions", "records", "selector", "observation", "recursive_structure", "access_specs"}
    assert len(payload["selector"]["coupling"]["masses"]) == 256  # type: ignore[index]
    assert [len(spec["block_rows"]) for spec in payload["recursive_structure"]["agents"]] == [16, 16]  # type: ignore[index]
    assert len(payload["recursive_structure"]["observation"]["fine_observation_labels"]) == 16  # type: ignore[index]
    assert len(payload["recursive_structure"]["sparse_record_candidate"]["left_outcome_by_fine_observation"]) == 16  # type: ignore[index]
    assert len(payload["recursive_structure"]["sparse_record_candidate"]["right_outcome_by_fine_observation"]) == 16  # type: ignore[index]
    assert len(payload["access_specs"]) == 2  # type: ignore[arg-type]
    assert all(len(access["observation_labels"]) == len(access["information_labels"]) == len(access["information_by_observation"]) == 16 for access in payload["access_specs"])  # type: ignore[index]
    assert coupling is not None
    assert all(mass == (Fraction(1, 128) if sum(int(entry[1][-1]) for entry in json.loads(label)) % 2 == 0 else Fraction(0)) for label, mass in zip(coupling.labels, coupling.masses, strict=True))


def test_subrecord_hashes_are_canonical_and_raw_bytes_are_separate() -> None:
    fixture = load_recursive_fixture(NAME)
    payload = _payload()
    subrecords = (
        ("generative", {"agents": payload["agents"], "records": payload["records"]}),
        ("recognition", {"recognitions": payload["recognitions"], "selector": payload["selector"]}),
        ("structure", payload["recursive_structure"]),
        ("access", payload["access_specs"]),
    )
    expected = tuple((name, hashlib.sha256(json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True, allow_nan=False).encode("utf-8")).hexdigest()) for name, value in subrecords)

    assert fixture.subrecord_sha256 == expected
    assert fixture.fixture_sha256 == hashlib.sha256((DATA / f"{NAME}.json").read_bytes()).hexdigest()


def test_selected_observation_changes_raw_sha_not_canonical_subrecord_hashes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    baseline = load_recursive_fixture(NAME)
    payload = _payload()
    payload["observation"][0][1] = "0"  # type: ignore[index]
    mutated_raw = json.dumps(payload, ensure_ascii=True, separators=(",", ":"), indent=2).encode("utf-8")

    mutated = _load_mutated(monkeypatch, payload)

    assert mutated.observation != baseline.observation
    assert mutated.fixture_sha256 == hashlib.sha256(mutated_raw).hexdigest()
    assert mutated.fixture_sha256 != baseline.fixture_sha256
    assert tuple(name for name, _ in mutated.subrecord_sha256) == ("generative", "recognition", "structure", "access")
    assert dict(mutated.subrecord_sha256)["generative"] == dict(baseline.subrecord_sha256)["generative"]
    assert mutated.subrecord_sha256 == baseline.subrecord_sha256


def test_public_loader_hashes_exact_read_bytes_once_without_rederiving_tables(monkeypatch: pytest.MonkeyPatch) -> None:
    path = (DATA / f"{NAME}.json").resolve()
    original_read_bytes = recursive_fixtures.Path.read_bytes
    original_raw = original_read_bytes(path)
    mutated_raw = original_raw + b"\n "
    reads = 0

    def read_mutated_bytes(candidate: Path) -> bytes:
        nonlocal reads
        if candidate.resolve() == path:
            reads += 1
            return mutated_raw
        return original_read_bytes(candidate)

    baseline = load_recursive_fixture(NAME)
    monkeypatch.setattr(recursive_fixtures.Path, "read_bytes", read_mutated_bytes)
    mutated = load_recursive_fixture(NAME)

    assert reads == 1
    assert json.loads(mutated_raw.decode("utf-8")) == json.loads(original_raw.decode("utf-8"))
    assert mutated.fixture_sha256 == hashlib.sha256(mutated_raw).hexdigest()
    assert mutated.fixture_sha256 != baseline.fixture_sha256
    assert mutated.subrecord_sha256 == baseline.subrecord_sha256


def test_public_loader_rejects_noncanonical_selector_table(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _payload()
    masses = payload["selector"]["coupling"]["masses"]  # type: ignore[index]
    masses[0], masses[2] = masses[2], masses[0]  # type: ignore[index]

    with pytest.raises(ValueError, match="canonical even-belief-parity table"):
        _load_mutated(monkeypatch, payload)


def test_public_loader_rejects_changed_sparse_projection(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _payload()
    projections = payload["recursive_structure"]["sparse_record_candidate"]["left_outcome_by_fine_observation"]  # type: ignore[index]
    projections[0] = "l01"  # type: ignore[index]

    with pytest.raises(ValueError, match="canonical record groups and projections"):
        _load_mutated(monkeypatch, payload)


def test_public_loader_rejects_replaced_exact_fixture_name(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _payload()
    payload["fixture_id"] = "lf4_two_parent_recursive_v2"

    with pytest.raises(ValueError, match="identity or schema version"):
        _load_mutated(monkeypatch, payload)


@pytest.mark.parametrize("mutation", ("block_channel", "record", "agent_evaluator"))
def test_public_loader_rejects_normalized_canonical_lf4_semantic_drift(
    monkeypatch: pytest.MonkeyPatch,
    mutation: str,
) -> None:
    payload = _payload()
    if mutation == "block_channel":
        rows = payload["recursive_structure"]["agents"][0]["block_rows"]  # type: ignore[index]
        rows[0], rows[1] = rows[1], rows[0]  # type: ignore[index]
    elif mutation == "record":
        payload["records"][0]["rows"][0] = [  # type: ignore[index]
            {"numerator": 3, "denominator": 4},
            {"numerator": 1, "denominator": 4},
        ]
    else:
        payload["agents"][1]["evaluator"][0]["rows"][0] = [  # type: ignore[index]
            {"numerator": 3, "denominator": 4},
            {"numerator": 1, "denominator": 4},
        ]
        payload["agents"][1]["generative_rows"][0] = [  # type: ignore[index]
            {"numerator": 9, "denominator": 16},
            {"numerator": 3, "denominator": 20},
            {"numerator": 3, "denominator": 16},
            {"numerator": 1, "denominator": 10},
        ]

    with pytest.raises(ValueError, match="canonical LF4"):
        _load_mutated(monkeypatch, payload)
