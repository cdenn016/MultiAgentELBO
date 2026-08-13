from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
WITNESS_PATH = ROOT / "docs/verification/u1_two_path_holonomy_witness.py"


def _load_witness():
    spec = importlib.util.spec_from_file_location("u1_two_path_holonomy_witness", WITNESS_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_marginal_record_moments_separate_zero_from_quarter_turn() -> None:
    witness = _load_witness()
    statistic_zero = witness.record_mean_norm_sq(0.0)
    statistic_quarter_turn = witness.record_mean_norm_sq(np.pi / 2)
    spectrum_zero = witness.record_covariance_spectrum(0.0)
    spectrum_quarter_turn = witness.record_covariance_spectrum(np.pi / 2)

    np.testing.assert_allclose(
        [statistic_zero, statistic_quarter_turn], [1.0, 0.5], atol=1e-12, rtol=0.0
    )
    np.testing.assert_allclose(spectrum_zero, [0.3225, 0.6225], atol=1e-12, rtol=0.0)
    np.testing.assert_allclose(
        spectrum_quarter_turn,
        [0.4725, 0.9725],
        atol=1e-12,
        rtol=0.0,
    )
    assert abs(float(np.sum(spectrum_quarter_turn) - np.sum(spectrum_zero)) - 0.5) < 1e-12


def test_periodicity_uses_the_exact_common_gauge() -> None:
    witness = _load_witness()

    assert witness.periodic_aligned_component_error(np.pi / 3, turns=1) < 1e-12


def test_mirror_equivalence_uses_an_exact_gauge_and_label_swap() -> None:
    witness = _load_witness()

    assert witness.mirror_aligned_component_error(np.pi / 3) < 1e-12


def test_coboundary_records_align_under_the_exact_endpoint_gauge() -> None:
    witness = _load_witness()

    for theta in (0.0, np.pi / 4, np.pi / 2, np.pi):
        assert witness.coboundary_aligned_component_error(theta) < 1e-12


def test_flat_twist_presentation_reproduces_connection_record_components() -> None:
    witness = _load_witness()

    for theta in (0.0, np.pi / 4, np.pi / 2, np.pi):
        connection = witness.record_law_components(theta)
        flat_twist = witness.flat_twist_record_law_components(theta)
        for (connection_mean, connection_cov), (flat_mean, flat_cov) in zip(
            connection, flat_twist, strict=True
        ):
            np.testing.assert_allclose(flat_mean, connection_mean, atol=1e-12, rtol=0.0)
            np.testing.assert_allclose(flat_cov, connection_cov, atol=1e-12, rtol=0.0)
