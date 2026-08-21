"""Primitive-fixture tests for the local-first v2 exact witness."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path

import pytest

from rg_v2.fixtures import LocalFirstFixture, _build_fixture, load_fixture


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "rg_v2" / "data"
CONTEXT_ID = "lf3-context-v1"
PRODUCT_SELECTOR_ID = "lf3-product-selector-v1"
CORRELATED_SELECTOR_ID = "lf3-correlated-selector-v1"
COARSE_CHANNEL_ID = "lf3-belief-parity-channel-v1"
STRUCTURAL_INPUT_ID = "lf3-belief-parity-structural-input-v1"
BOUNDARY_CONTEXT_ID = "lf3-dirac-boundary-context-v1"
BOUNDARY_SELECTOR_ID = "lf3-dirac-boundary-selector-v1"
BOUNDARY_CHANNEL_ID = "lf3-dirac-boundary-channel-v1"
BOUNDARY_STRUCTURAL_INPUT_ID = "lf3-dirac-boundary-structural-input-v1"


def _local(belief: str, model: str) -> str:
    return json.dumps([belief, model], ensure_ascii=True, separators=(",", ":"))


def _assignment(*entries: tuple[str, str, str]) -> str:
    return json.dumps([list(entry) for entry in entries], ensure_ascii=True, separators=(",", ":"))


def _payload(name: str) -> dict[str, object]:
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


def _rebuilt(name: str, payload: dict[str, object]) -> LocalFirstFixture:
    path = DATA / f"{name}.json"
    return _build_fixture(name, path, hashlib.sha256(path.read_bytes()).hexdigest(), payload)


def test_product_fixture_decodes_canonical_local_data_and_frozen_identifiers() -> None:
    fixture = load_fixture("lf3_product_v1")

    assert fixture.fixture_id == "lf3_product_v1"
    assert fixture.context_id == CONTEXT_ID
    assert fixture.fixture_path == DATA / "lf3_product_v1.json"
    assert fixture.fixture_sha256 == hashlib.sha256(fixture.fixture_path.read_bytes()).hexdigest()
    assert tuple(agent.agent_id for agent in fixture.agents) == ("a", "b", "c")
    assert fixture.observation == (("r_a", "1"), ("r_b", "1"), ("r_c", "1"))
    assert fixture.selector.selector_id == PRODUCT_SELECTOR_ID
    assert fixture.coarse_channel.channel_id == COARSE_CHANNEL_ID
    assert fixture.coarse_channel.structural_input_ids == (STRUCTURAL_INPUT_ID,)

    expected_states = tuple(_local(belief, model) for belief in ("b0", "b1") for model in ("m0", "m1"))
    assert all(agent.state_labels == expected_states for agent in fixture.agents)
    assert fixture.agents[0].generative_kernel.matrix == ((Fraction(3, 8), Fraction(1, 8), Fraction(1, 8), Fraction(3, 8)),)
    child_rows = (
        (Fraction(3, 5), Fraction(3, 20), Fraction(3, 20), Fraction(1, 10)),
        (Fraction(1, 5), Fraction(9, 20), Fraction(1, 20), Fraction(3, 10)),
        (Fraction(3, 10), Fraction(1, 20), Fraction(9, 20), Fraction(1, 5)),
        (Fraction(1, 10), Fraction(3, 20), Fraction(3, 20), Fraction(3, 5)),
    )
    assert fixture.agents[1].generative_kernel.matrix == child_rows
    assert fixture.agents[2].generative_kernel.matrix == child_rows
    assert fixture.agents[1].evaluator[0].kernel.matrix == (
        (Fraction(4, 5), Fraction(1, 5)),
        (Fraction(4, 5), Fraction(1, 5)),
        (Fraction(2, 5), Fraction(3, 5)),
        (Fraction(2, 5), Fraction(3, 5)),
    )
    assert fixture.agents[1].evaluator[1].kernel.matrix == (
        (Fraction(3, 5), Fraction(2, 5)),
        (Fraction(3, 5), Fraction(2, 5)),
        (Fraction(1, 5), Fraction(4, 5)),
        (Fraction(1, 5), Fraction(4, 5)),
    )
    assert all(record.kernel.matrix == ((Fraction(4, 5), Fraction(1, 5)),) * 2 + ((Fraction(1, 5), Fraction(4, 5)),) * 2 for record in fixture.records)


def test_product_and_correlated_share_decoded_local_data_but_not_selector() -> None:
    product = load_fixture("lf3_product_v1")
    correlated = load_fixture("lf3_correlated_v1")

    assert product.agents == correlated.agents
    assert product.recognitions == correlated.recognitions
    assert product.records == correlated.records
    assert product.observation == correlated.observation
    assert product.selector.coupling is None
    assert correlated.selector.selector_id == CORRELATED_SELECTOR_ID
    assert correlated.selector.selector_kind == "declared_correlated"
    assert correlated.selector.coupling is not None
    assert product.fixture_sha256 != correlated.fixture_sha256


def test_recognitions_and_declared_correlated_table_have_literal_marginals() -> None:
    product = load_fixture("lf3_product_v1")
    correlated = load_fixture("lf3_correlated_v1")
    coupling = correlated.selector.coupling
    assert coupling is not None

    for recognition in product.recognitions:
        assert recognition.joint.masses == (Fraction(1, 4),) * 4
        assert recognition.belief_marginal.masses == (Fraction(1, 2), Fraction(1, 2))
        assert recognition.model_marginal.masses == (Fraction(1, 2), Fraction(1, 2))

    expected_labels = tuple(
        _assignment(("a", ba, ma), ("b", bb, mb), ("c", bc, mc))
        for ba in ("b0", "b1")
        for ma in ("m0", "m1")
        for bb in ("b0", "b1")
        for mb in ("m0", "m1")
        for bc in ("b0", "b1")
        for mc in ("m0", "m1")
    )
    expected_masses = tuple(
        Fraction(1, 32) if (int(ba[-1]) + int(bb[-1]) + int(bc[-1])) % 2 == 0 else Fraction(0)
        for ba in ("b0", "b1")
        for _ma in ("m0", "m1")
        for bb in ("b0", "b1")
        for _mb in ("m0", "m1")
        for bc in ("b0", "b1")
        for _mc in ("m0", "m1")
    )
    assert coupling.labels == expected_labels
    assert coupling.masses == expected_masses
    product_mass = Fraction(1, 64)
    assert sum(abs(mass - product_mass) for mass in coupling.masses) / 2 == Fraction(1, 2)


def test_coarse_channel_is_explicit_full_latent_deterministic_parity_map() -> None:
    fixture = load_fixture("lf3_product_v1")
    channel = fixture.coarse_channel.channel

    assert len(channel.source_labels) == 64
    assert channel.target_labels == ("even", "odd")
    assert all(row in ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))) for row in channel.matrix)
    assert channel.source_labels[0] == _assignment(("a", "b0", "m0"), ("b", "b0", "m0"), ("c", "b0", "m0"))
    assert channel.source_labels[-1] == _assignment(("a", "b1", "m1"), ("b", "b1", "m1"), ("c", "b1", "m1"))


def test_dirac_boundary_fixture_has_frozen_singleton_supports() -> None:
    fixture = load_fixture("lf3_dirac_boundary_v1")

    assert fixture.context_id == BOUNDARY_CONTEXT_ID
    assert fixture.selector.selector_id == BOUNDARY_SELECTOR_ID
    assert fixture.coarse_channel.channel_id == BOUNDARY_CHANNEL_ID
    assert fixture.coarse_channel.structural_input_ids == (BOUNDARY_STRUCTURAL_INPUT_ID,)
    assert all(agent.state_labels == (_local("b0", "m0"),) for agent in fixture.agents)
    assert all(recognition.joint.masses == (Fraction(1),) for recognition in fixture.recognitions)
    assert fixture.observation == (("r_a", "1"), ("r_b", "1"), ("r_c", "1"))
    assert fixture.coarse_channel.channel.source_labels == (_assignment(("a", "b0", "m0"), ("b", "b0", "m0"), ("c", "b0", "m0")),)
    assert fixture.coarse_channel.channel.matrix == ((Fraction(1),),)


@pytest.mark.parametrize("bad_mass", [True, 0.5, "1", {"numerator": 2, "denominator": 4}, {"numerator": 1, "denominator": 0}])
def test_loader_rejects_noncanonical_rational_records(bad_mass: object) -> None:
    payload = _payload("lf3_product_v1")
    payload["recognitions"][0]["masses"][0] = bad_mass  # type: ignore[index]

    with pytest.raises((TypeError, ValueError)):
        _rebuilt("lf3_product_v1", payload)


@pytest.mark.parametrize("prohibited", ["population", "inference", "evidence", "posterior", "coarse_result", "vfe", "status", "pass"])
def test_loader_recursively_rejects_derived_result_keys(prohibited: str) -> None:
    payload = _payload("lf3_product_v1")
    payload["agents"][0][prohibited] = None  # type: ignore[index]

    with pytest.raises(ValueError, match="prohibited|keys"):
        _rebuilt("lf3_product_v1", payload)


def test_loader_rejects_unknown_keys_and_recognition_marginals() -> None:
    payload = _payload("lf3_product_v1")
    payload["unexpected"] = None
    with pytest.raises(ValueError, match="keys"):
        _rebuilt("lf3_product_v1", payload)

    payload = _payload("lf3_product_v1")
    payload["recognitions"][0]["belief_marginal"] = []  # type: ignore[index]
    with pytest.raises(ValueError, match="keys"):
        _rebuilt("lf3_product_v1", payload)
