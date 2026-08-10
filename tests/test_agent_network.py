from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "two_scale_application_v1.json"


def test_load_application_fixture_preserves_exact_declared_tuple() -> None:
    """Catches reordered labels, rounded literals, or an unvalidated scale arrow."""
    from multiagent_elbo.finite.agent_network import load_application_fixture

    fixture = load_application_fixture(FIXTURE_PATH)

    assert fixture.application_id == (
        "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"
    )
    assert fixture.fine_labels == tuple(f"{state:04b}" for state in range(16))
    assert fixture.coarse_labels == ("00", "01", "10", "11")
    assert sum(fixture.baseline) == Fraction(1)
    assert sum(fixture.evidence_measure) == fixture.evidence == Fraction(1, 2)
    assert fixture.posterior == tuple(
        mass / fixture.evidence for mass in fixture.evidence_measure
    )
    assert all(sum(row) == Fraction(1) for row in fixture.channel)
    assert fixture.channel[0] == (
        Fraction(9, 16),
        Fraction(3, 16),
        Fraction(3, 16),
        Fraction(1, 16),
    )
    assert fixture.configuration_scale_map == (
        (Fraction(1, 2), Fraction(1, 2), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1, 2), Fraction(1, 2)),
    )
    assert fixture.local_blocks == {
        "local_B01": ((0, 1), (2, 3)),
        "local_B23": ((2, 3), (0, 1)),
    }


@pytest.mark.parametrize(
    ("scenario", "expected_action", "expected_evidence", "expected_first_mass"),
    (
        (
            "aligned",
            (0, 2, 2, 2, 2, 4, 2, 2, 2, 2, 4, 2, 2, 2, 2, 0),
            Fraction(91, 512),
            Fraction(12, 91),
        ),
        (
            "frustrated",
            (1, 1, 3, 1, 3, 3, 3, 1, 1, 3, 3, 3, 1, 3, 1, 1),
            Fraction(5, 32),
            Fraction(3, 40),
        ),
        (
            "asymmetric_evidence",
            (0, 7, 5, 6, 3, 10, 4, 5, 5, 4, 10, 3, 6, 5, 7, 0),
            Fraction(3515, 32768),
            Fraction(768, 3515),
        ),
        (
            "higher_order",
            (0, 2, 4, 4, 4, 6, 2, 2, 4, 4, 4, 2, 2, 2, 4, 2),
            Fraction(775, 8192),
            Fraction(192, 775),
        ),
    ),
)
def test_scenarios_construct_normalized_records_and_exact_laws(
    scenario: str,
    expected_action: tuple[int, ...],
    expected_evidence: Fraction,
    expected_first_mass: Fraction,
) -> None:
    """Catches unnormalized records or scenario arithmetic detached from literals."""
    from multiagent_elbo.finite.agent_network import (
        build_scenario_application,
        load_application_fixture,
    )

    application = build_scenario_application(
        load_application_fixture(FIXTURE_PATH), scenario
    )

    assert application.interaction_action_log2 == tuple(
        Fraction(value) for value in expected_action
    )
    assert application.evidence == expected_evidence
    assert application.posterior[0] == expected_first_mass
    assert sum(application.posterior) == Fraction(1)
    assert all(
        success + failure == Fraction(1)
        for record in application.interaction_record_kernels.values()
        for success, failure in record
    )


def test_exact_one_arrow_pushforward_preserves_evidence_and_expected_coarse_law() -> None:
    """Catches transposed channels or pushing only the normalized posterior."""
    from multiagent_elbo.finite.agent_network import (
        build_scenario_application,
        load_application_fixture,
    )

    application = build_scenario_application(
        load_application_fixture(FIXTURE_PATH), "aligned"
    )

    assert sum(application.coarse_evidence_measure) == application.evidence
    assert application.coarse_posterior == (
        Fraction(603, 1456),
        Fraction(305, 1456),
        Fraction(305, 1456),
        Fraction(243, 1456),
    )


def test_recognition_product_lift_is_an_exact_right_inverse() -> None:
    """Catches a lift whose coordinate extraction does not recover its input."""
    from multiagent_elbo.finite.agent_network import (
        extract_bernoulli_coordinates,
        product_bernoulli_law,
        recognition_lift_residual,
    )

    parameters = (
        Fraction(2, 5),
        Fraction(3, 5),
        Fraction(1, 3),
        Fraction(2, 3),
    )
    lifted = product_bernoulli_law(parameters)

    assert sum(lifted) == Fraction(1)
    assert extract_bernoulli_coordinates(lifted) == parameters
    assert recognition_lift_residual(parameters) == Fraction(0)


def test_wrong_recognition_lift_is_detected_by_literal_residual() -> None:
    """Catches a right-inverse check that ignores the supplied lifted law."""
    from multiagent_elbo.finite.agent_network import recognition_lift_residual

    parameters = (Fraction(2, 5),) * 4
    wrong_uniform_lift = (Fraction(1, 16),) * 16

    assert recognition_lift_residual(parameters, wrong_uniform_lift) == Fraction(1, 10)


def test_exact_hoeffding_reconstructs_pairwise_and_higher_order_actions() -> None:
    """Catches incomplete Mobius assembly or accidental pairwise closure."""
    from multiagent_elbo.finite.agent_network import (
        build_scenario_application,
        exact_hoeffding_decompose,
        load_application_fixture,
        retained_interaction_residual,
    )

    fixture = load_application_fixture(FIXTURE_PATH)
    aligned = build_scenario_application(fixture, "aligned")
    higher_order = build_scenario_application(fixture, "higher_order")
    aligned_components = exact_hoeffding_decompose(
        aligned.interaction_action_log2, fixture.fine_axis_references
    )
    higher_components = exact_hoeffding_decompose(
        higher_order.interaction_action_log2, fixture.fine_axis_references
    )

    assert aligned_components.reconstruction == aligned.interaction_action_log2
    assert higher_components.reconstruction == higher_order.interaction_action_log2
    assert aligned_components.reconstruction_residual == Fraction(0)
    assert higher_components.reconstruction_residual == Fraction(0)
    assert retained_interaction_residual(aligned_components, maximum_order=2) == Fraction(0)
    assert retained_interaction_residual(higher_components, maximum_order=2) == Fraction(1)
    assert higher_components.components[(0, 1, 2)][:8] == (
        Fraction(-1),
        Fraction(-1),
        Fraction(1),
        Fraction(1),
        Fraction(1),
        Fraction(1),
        Fraction(-1),
        Fraction(-1),
    )


def test_global_vfe_gap_and_fixed_outside_local_difference_match_literal_oracles() -> None:
    """Catches a marginal KL substituted for the joint VFE or a wrong block weighting."""
    from multiagent_elbo.finite.agent_network import (
        build_scenario_application,
        global_vfe_gap,
        load_application_fixture,
        local_collective_difference,
        product_bernoulli_law,
        scenario_recognition_target,
    )

    application = build_scenario_application(
        load_application_fixture(FIXTURE_PATH), "aligned"
    )
    q_before = product_bernoulli_law((Fraction(1, 2),) * 4)
    target = scenario_recognition_target("aligned")
    q_after_b01 = product_bernoulli_law(
        (target[0], target[1], Fraction(1, 2), Fraction(1, 2))
    )

    gap = global_vfe_gap(q_before, application.evidence_measure)
    local = local_collective_difference(
        application.posterior,
        q_before,
        q_after_b01,
        block_axes=(0, 1),
    )

    assert gap.direct_vfe == pytest.approx(2.367123614131617, abs=1e-15)
    assert gap.posterior_kl == pytest.approx(0.639658495608959, abs=1e-15)
    assert gap.residual == pytest.approx(0.0, abs=1e-15)
    assert local.local_difference == pytest.approx(0.4496337464793081, abs=1e-15)
    assert local.collective_difference == pytest.approx(0.4496337464793081, abs=1e-15)
    assert local.residual == pytest.approx(0.0, abs=1e-15)
    assert local.outside_marginal == (Fraction(1, 4),) * 4


def test_overlapping_local_objective_sum_is_not_the_collective_objective() -> None:
    """Catches the forbidden replacement of one joint VFE by overlapping local sums."""
    from multiagent_elbo.finite.agent_network import (
        build_scenario_application,
        load_application_fixture,
        overlapping_local_objective_gap,
        product_bernoulli_law,
    )

    application = build_scenario_application(
        load_application_fixture(FIXTURE_PATH), "aligned"
    )
    recognition = product_bernoulli_law((Fraction(1, 2),) * 4)

    assert overlapping_local_objective_gap(
        application.posterior,
        recognition,
        ((0, 1), (2, 3)),
    ) == pytest.approx(0.18747552763150188, abs=1e-15)


def test_non_normalized_fixture_channel_is_rejected(tmp_path: Path) -> None:
    """Catches acceptance of an application arrow that does not preserve mass."""
    from multiagent_elbo.experiment_support import fixture_application_id
    from multiagent_elbo.finite.agent_network import load_application_fixture

    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    payload["channel"]["arrows"][0]["rows"][0][0] = "1/2"
    payload["application_id"] = fixture_application_id(payload)
    invalid_path = tmp_path / "bad-channel.json"
    invalid_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="channel row 0 is not normalized"):
        load_application_fixture(invalid_path)


def test_parameter_dependent_channel_is_inconclusive_not_a_theorem_refutation() -> None:
    """Catches claim-state collapse at the fixed-channel theorem boundary."""
    from multiagent_elbo.finite.agent_network import assess_fixed_channel_premise

    fixed = assess_fixed_channel_premise(recognition_independent=True)
    parameter_dependent = assess_fixed_channel_premise(recognition_independent=False)

    assert fixed.satisfied is True
    assert fixed.theorem_status == "HYPOTHESIS"
    assert fixed.verification_state == "EVIDENCE_VERIFIED"
    assert parameter_dependent.satisfied is False
    assert parameter_dependent.theorem_status == "HYPOTHESIS"
    assert parameter_dependent.verification_state == "INCONCLUSIVE"
    assert "outside" in parameter_dependent.reason


def test_self_consistent_but_nonfrozen_fixture_identity_is_rejected(
    tmp_path: Path,
) -> None:
    """Catches silent substitution of a different application under the same schema."""
    from multiagent_elbo.experiment_support import fixture_application_id
    from multiagent_elbo.finite.agent_network import load_application_fixture

    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    payload["epistemic_boundary"]["scope"] = "mutated application"
    payload["application_id"] = fixture_application_id(payload)
    alternate = tmp_path / "alternate.json"
    alternate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="does not match frozen application_id"):
        load_application_fixture(alternate)
