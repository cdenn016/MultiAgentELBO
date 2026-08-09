from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

import numpy as np
import pytest
import scipy.linalg

from multiagent_elbo.config import ExperimentConfig, NumericsConfig
from multiagent_elbo.realizations.gaussian.experiment import (
    GaussianExperimentResult,
    run_gaussian_experiment,
)
from multiagent_elbo.realizations.gaussian.gauge import (
    GaussianNumericalError,
    apply_frame_change,
    generate_positive_orientation_frames,
    transform_prolongator,
)
from multiagent_elbo.realizations.gaussian.interactions import (
    GaussianInteraction,
    galerkin_aggregate_precision,
    schur_complement_precision,
)


NUMERICS = NumericsConfig(
    dtype="float64",
    atol=1e-12,
    rtol=1e-10,
    min_spd_rcond=1e-12,
    max_frame_condition=1.0e6,
)


def scalar_interaction() -> GaussianInteraction:
    return GaussianInteraction.from_self_and_edges(
        (1.0, 2.0, 3.0), {(0, 1): 4.0, (1, 2): 5.0}, NUMERICS
    )


def matrix_interaction() -> GaussianInteraction:
    weight = np.array([[1.0, 0.2], [0.2, 2.0]])
    return GaussianInteraction.from_self_and_edges(
        (np.diag([2.0, 3.0]), np.diag([4.0, 5.0])),
        {(0, 1): weight},
        NUMERICS,
    )


def literal_frames() -> np.ndarray:
    return np.array([np.diag([2.0, 1.0]), np.diag([1.0, 3.0])])


def test_scalar_galerkin_aggregation_matches_literal_operator_and_cut_blocks():
    interaction = scalar_interaction()

    result = galerkin_aggregate_precision(interaction, ((0, 1), (2,)))

    np.testing.assert_allclose(
        interaction.precision,
        [[5.0, -4.0, 0.0], [-4.0, 11.0, -5.0], [0.0, -5.0, 8.0]],
    )
    np.testing.assert_allclose(result.precision, [[8.0, -5.0], [-5.0, 8.0]])
    assert result.self_blocks[:, 0, 0] == pytest.approx([3.0, 3.0])
    assert result.edge_blocks[(0, 1)][0, 0] == pytest.approx(5.0)
    assert (0, 0) not in result.edge_blocks
    assert result.method == "operator_level_hard_identification_galerkin"
    assert result.is_gaussian_marginal is False
    assert result.is_probability_pushforward is False


def test_scalar_schur_marginal_is_distinct_from_galerkin_restriction():
    interaction = scalar_interaction()

    marginal = schur_complement_precision(
        interaction.precision, retained_vertices=(0, 2), block_size=1, numerics=NUMERICS
    )
    galerkin = galerkin_aggregate_precision(interaction, ((0, 1), (2,)))

    np.testing.assert_allclose(
        marginal,
        [[39.0 / 11.0, -20.0 / 11.0], [-20.0 / 11.0, 63.0 / 11.0]],
    )
    assert not np.allclose(marginal, galerkin.precision)


def test_retain_all_schur_honors_requested_vertex_order():
    interaction = scalar_interaction()

    reordered = schur_complement_precision(
        interaction.precision,
        retained_vertices=(2, 0, 1),
        block_size=1,
        numerics=NUMERICS,
    )

    requested = np.array([2, 0, 1])
    expected = interaction.precision[np.ix_(requested, requested)]
    np.testing.assert_allclose(reordered, expected)
    assert not np.array_equal(reordered, interaction.precision)


def test_unrestricted_matrix_weight_kron_reduction_leaves_declared_family():
    identity = np.eye(2)
    interaction = GaussianInteraction.from_self_and_edges(
        (identity, identity, identity),
        {
            (0, 1): np.zeros((2, 2)),
            (0, 2): np.diag([1.0, 2.0]),
            (1, 2): np.array([[2.0, 1.0], [1.0, 2.0]]),
        },
        NUMERICS,
    )

    marginal = schur_complement_precision(
        interaction.precision, retained_vertices=(0, 1), block_size=2, numerics=NUMERICS
    )
    expected = np.array(
        [[33.0, 2.0, -9.0, -3.0],
         [2.0, 41.0, -4.0, -14.0],
         [-9.0, -4.0, 37.0, 6.0],
         [-3.0, -14.0, 6.0, 40.0]]
    ) / 19.0
    manufactured_weight = -marginal[:2, 2:]

    assert marginal == pytest.approx(expected)
    assert manufactured_weight == pytest.approx(
        np.array([[9.0, 3.0], [4.0, 14.0]]) / 19.0
    )
    assert not np.allclose(manufactured_weight, manufactured_weight.T)


@pytest.mark.parametrize(
    ("self_terms", "edges", "message"),
    [
        ((1.0, -1.0), {}, "self block 1 is not positive semidefinite"),
        ((1.0, 1.0), {(0, 1): -1.0}, r"edge \(0, 1\) is not positive semidefinite"),
        ((1.0, np.eye(2)), {}, "mixed scalar and matrix block sizes"),
        ((1.0, 1.0), {(0, 0): 1.0}, "self-loop edge"),
        ((1.0, 1.0), {(0, 1): 1.0, (1, 0): 2.0}, "duplicate reversed edge"),
    ],
)
def test_interaction_rejects_invalid_blocks_without_repair(
    self_terms: tuple[object, ...], edges: dict, message: str
):
    with pytest.raises(GaussianNumericalError, match=message):
        GaussianInteraction.from_self_and_edges(self_terms, edges, NUMERICS)


@pytest.mark.parametrize(
    "partition",
    [
        ((0, 1),),
        ((0, 1), (1, 2)),
        ((0,), (0,), (1, 2)),
        ((), (0, 1, 2)),
        ((0, 1), (2,), ()),
        ((0, 3), (1, 2)),
    ],
)
def test_galerkin_partition_must_own_each_vertex_exactly_once(partition: tuple):
    with pytest.raises(GaussianNumericalError, match="partition"):
        galerkin_aggregate_precision(scalar_interaction(), partition)


def test_interaction_and_partition_inputs_are_defensively_owned():
    self_blocks = np.array([np.eye(2), 2.0 * np.eye(2)])
    weight = np.eye(2)
    partition = [[0], [1]]
    interaction = GaussianInteraction.from_self_and_edges(
        self_blocks, {(0, 1): weight}, NUMERICS
    )
    result = galerkin_aggregate_precision(interaction, partition)

    self_blocks[:] = 99.0
    weight[:] = 88.0
    partition[0][0] = 1

    np.testing.assert_allclose(interaction.self_blocks, [np.eye(2), 2.0 * np.eye(2)])
    assert interaction.edge_blocks[(0, 1)] == pytest.approx(np.eye(2))
    assert result.partition == ((0,), (1,))
    assert not interaction.precision.flags.writeable
    assert not result.precision.flags.writeable


def test_scale_aware_symmetry_projects_only_a_within_tolerance_block():
    almost_symmetric = np.array([[2.0e8, 1.0], [1.0 + 1.0e-4, 3.0e8]])

    interaction = GaussianInteraction.from_self_and_edges(
        (almost_symmetric,), {}, NUMERICS
    )

    np.testing.assert_allclose(
        interaction.self_blocks[0], (almost_symmetric + almost_symmetric.T) * 0.5
    )
    np.testing.assert_allclose(interaction.self_blocks[0], interaction.self_blocks[0].T)

    with pytest.raises(GaussianNumericalError, match="not symmetric within tolerance"):
        GaussianInteraction.from_self_and_edges(
            (np.array([[2.0, 0.0], [1.0e-3, 3.0]]),), {}, NUMERICS
        )


def test_scale_aware_edge_psd_gate_does_not_clamp_accepted_raw_eigenvalue():
    edge = np.diag([1.0e6, -1.0e-5])
    interaction = GaussianInteraction.from_self_and_edges(
        (2.0 * np.eye(2), 2.0 * np.eye(2)), {(0, 1): edge}, NUMERICS
    )

    assert np.linalg.eigvalsh(interaction.edge_blocks[(0, 1)])[0] == pytest.approx(-1e-5)


def test_cholesky_and_rcond_gates_reject_singular_or_unacceptable_precision():
    with pytest.raises(GaussianNumericalError, match="not positive definite"):
        GaussianInteraction.from_self_and_edges((0.0,), {}, NUMERICS)

    with pytest.raises(GaussianNumericalError, match="reciprocal condition"):
        GaussianInteraction.from_self_and_edges(
            (np.diag([1.0, 1.0e-14]),), {}, NUMERICS
        )


def test_inverse_congruence_preserves_both_quadratic_energies_and_exact_determinants(
    monkeypatch: pytest.MonkeyPatch,
):
    interaction = matrix_interaction()
    frames = literal_frames()
    coordinates = np.array([1.0, 2.0, -1.0, 1.0])
    transformed_coordinates = scipy.linalg.block_diag(*frames) @ coordinates

    def forbidden(*_: object, **__: object) -> None:
        raise AssertionError("explicit matrix inverse is forbidden")

    monkeypatch.setattr(np.linalg, "inv", forbidden)
    monkeypatch.setattr(np.linalg, "pinv", forbidden)
    monkeypatch.setattr(scipy.linalg, "inv", forbidden)
    monkeypatch.setattr(scipy.linalg, "pinv", forbidden)

    result = apply_frame_change(
        interaction.precision, interaction.laplacian, frames, NUMERICS
    )

    original_energy = coordinates @ interaction.precision @ coordinates
    transformed_energy = (
        transformed_coordinates @ result.transformed_precision @ transformed_coordinates
    )
    original_laplacian_energy = coordinates @ interaction.laplacian @ coordinates
    transformed_laplacian_energy = (
        transformed_coordinates
        @ result.transformed_laplacian
        @ transformed_coordinates
    )
    assert original_energy == pytest.approx(149.0 / 5.0)
    assert transformed_energy == pytest.approx(149.0 / 5.0)
    assert original_laplacian_energy == pytest.approx(34.0 / 5.0)
    assert transformed_laplacian_energy == pytest.approx(34.0 / 5.0)
    assert np.linalg.det(interaction.precision) == pytest.approx(10802.0 / 25.0)
    assert np.linalg.det(result.transformed_precision) == pytest.approx(5401.0 / 450.0)
    assert result.transformed_logdet - result.original_logdet == pytest.approx(
        -2.0 * math.log(6.0)
    )


def test_generalized_roots_match_independent_exact_oracle_and_diagnostics():
    interaction = matrix_interaction()
    result = apply_frame_change(
        interaction.precision, interaction.laplacian, literal_frames(), NUMERICS
    )
    root = math.sqrt(14785.0)
    expected = np.array(
        [0.0, 0.0, (5077.0 - 5.0 * root) / 10802.0, (5077.0 + 5.0 * root) / 10802.0]
    )

    assert result.generalized_eigenvalues == pytest.approx(expected, abs=1e-12)
    assert result.transformed_generalized_eigenvalues == pytest.approx(
        expected, abs=1e-12
    )
    assert np.max(result.eigenpair_residuals) < 1e-14
    assert np.max(result.transformed_eigenpair_residuals) < 1e-14
    assert result.metric_orthogonality_residual < 1e-14
    assert result.transformed_metric_orthogonality_residual < 1e-14
    assert result.generalized_eigenvectors.T @ interaction.precision @ result.generalized_eigenvectors == pytest.approx(
        np.eye(4), abs=1e-12
    )


def test_ordinary_laplacian_spectrum_is_a_pinned_noninvariant_control():
    interaction = matrix_interaction()
    result = apply_frame_change(
        interaction.precision, interaction.laplacian, literal_frames(), NUMERICS
    )
    expected_before = np.array([0.0, 0.0, 3.0 - math.sqrt(29.0) / 5.0, 3.0 + math.sqrt(29.0) / 5.0])
    expected_after = np.array(
        [0.0, 0.0, (125.0 - math.sqrt(1513.0)) / 72.0, (125.0 + math.sqrt(1513.0)) / 72.0]
    )

    assert result.ordinary_eigenvalues == pytest.approx(expected_before, abs=1e-12)
    assert result.transformed_ordinary_eigenvalues == pytest.approx(
        expected_after, abs=1e-12
    )
    assert not np.allclose(
        result.ordinary_eigenvalues, result.transformed_ordinary_eigenvalues
    )


def test_transformed_prolongator_closes_the_commuting_square():
    interaction = matrix_interaction()
    frames = literal_frames()
    coarse_frames = np.array([np.diag([5.0, 2.0])])
    prolongator = np.vstack([np.eye(2), np.eye(2)])
    result = apply_frame_change(
        interaction.precision,
        interaction.laplacian,
        frames,
        NUMERICS,
        prolongator=prolongator,
        coarse_frames=coarse_frames,
    )

    expected_transformed = np.array(
        [[2.0 / 5.0, 0.0], [0.0, 1.0 / 2.0], [1.0 / 5.0, 0.0], [0.0, 3.0 / 2.0]]
    )
    coarse = prolongator.T @ interaction.precision @ prolongator
    transformed_coarse = (
        result.transformed_prolongator.T
        @ result.transformed_precision
        @ result.transformed_prolongator
    )
    assert result.transformed_prolongator == pytest.approx(expected_transformed)
    assert coarse == pytest.approx(np.diag([6.0, 8.0]))
    assert transformed_coarse == pytest.approx(np.diag([6.0 / 25.0, 2.0]))
    expected_via_coarse_frame = scipy.linalg.solve(
        coarse_frames[0].T,
        scipy.linalg.solve(coarse_frames[0].T, coarse.T).T,
    )
    assert transformed_coarse == pytest.approx(expected_via_coarse_frame)


def test_holding_prolongator_fixed_requires_the_literal_intertwiner_identity():
    prolongator = np.vstack([np.eye(2), np.eye(2)])
    with pytest.raises(GaussianNumericalError, match="does not intertwine"):
        transform_prolongator(
            prolongator,
            literal_frames(),
            np.array([np.diag([5.0, 2.0])]),
            NUMERICS,
            hold_fixed=True,
        )

    common = np.array([np.diag([2.0, 3.0]), np.diag([2.0, 3.0])])
    held = transform_prolongator(
        prolongator,
        common,
        np.array([np.diag([2.0, 3.0])]),
        NUMERICS,
        hold_fixed=True,
    )
    assert held == pytest.approx(prolongator)


@pytest.mark.parametrize(
    ("frames", "message"),
    [
        (np.array([np.diag([-1.0, 1.0]), np.eye(2)]), "positive determinant"),
        (np.array([np.diag([1.0e7, 1.0]), np.eye(2)]), "condition number"),
        (np.ones((2, 2)), r"shape \(N, K, K\)"),
    ],
)
def test_frame_validation_rejects_wrong_orientation_condition_or_shape(
    frames: np.ndarray, message: str
):
    interaction = matrix_interaction()
    with pytest.raises(GaussianNumericalError, match=message):
        apply_frame_change(
            interaction.precision, interaction.laplacian, frames, NUMERICS
        )


def test_seeded_frames_are_deterministic_positive_and_bounded():
    first = generate_positive_orientation_frames(
        np.random.default_rng(20260808), 4, 3, max_condition=50.0
    )
    second = generate_positive_orientation_frames(
        np.random.default_rng(20260808), 4, 3, max_condition=50.0
    )

    assert first == pytest.approx(second)
    assert np.all(np.linalg.det(first) > 0.0)
    assert np.max(np.linalg.cond(first)) <= 50.0 * (1.0 + 1e-12)


def test_generated_frames_are_accepted_at_the_declared_condition_boundary():
    boundary_numerics = NumericsConfig(
        dtype="float64",
        atol=1e-12,
        rtol=1e-10,
        min_spd_rcond=1e-12,
        max_frame_condition=50.0,
    )
    frames = generate_positive_orientation_frames(
        np.random.default_rng(20260808), 4, 3, max_condition=50.0
    )

    result = apply_frame_change(
        np.eye(12), np.zeros((12, 12)), frames, boundary_numerics
    )

    assert np.max(result.frame_condition_numbers) == pytest.approx(50.0)


@pytest.mark.parametrize("scale", [1.0e100, 1.0e-100])
def test_positive_orientation_validation_is_invariant_to_uniform_frame_scaling(
    scale: float,
):
    frame = np.array([scale * np.eye(4)])
    prolongator = np.eye(4)

    held = transform_prolongator(
        prolongator,
        frame,
        frame,
        NUMERICS,
        hold_fixed=True,
    )

    np.testing.assert_array_equal(held, prolongator)


def gaussian_config(
    root: Path,
    *,
    diagnostics: bool = False,
    figures: bool = False,
    name: str = "gaussian realization",
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": name, "seed": 20260808},
        {"experiment": "gaussian_realization", "retained_interaction_order": None},
        {
            "dtype": "float64",
            "atol": 1e-12,
            "rtol": 1e-10,
            "min_spd_rcond": 1e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(root),
            "collect_diagnostics": diagnostics,
            "render_figures": figures,
        },
    )


@pytest.mark.parametrize("diagnostics", [False, True])
def test_gaussian_experiment_writes_core_bundle_and_only_requested_diagnostics(
    tmp_path: Path, diagnostics: bool
):
    result = run_gaussian_experiment(gaussian_config(tmp_path, diagnostics=diagnostics))

    assert isinstance(result, GaussianExperimentResult)
    assert result.status == "pass"
    assert result.figure_status == "not_requested"
    assert result.figure_dir is None
    assert (result.run_dir / "metrics.json").is_file()
    assert (result.run_dir / "arrays.npz").is_file()
    assert (result.run_dir / "diagnostics.npz").is_file() is diagnostics
    assert set(result.arrays) >= {
        "generalized_eigenvalues",
        "transformed_generalized_eigenvalues",
        "expected_generalized_eigenvalues",
    }
    if diagnostics:
        with np.load(result.run_dir / "diagnostics.npz") as archive:
            seeded = archive["seeded_positive_frames"]
            assert np.all(np.linalg.det(seeded) > 0.0)
            assert np.max(np.linalg.cond(seeded)) <= 100.0 * (1.0 + 1e-12)


def test_gaussian_experiment_renders_only_after_numerical_finalization(tmp_path: Path):
    calls: list[tuple[Path, Path, tuple[str, ...], bytes]] = []

    def renderer(
        run_dir: Path, output_dir: Path, *, requested: tuple[str, ...]
    ) -> object:
        manifest_bytes = (run_dir / "manifest.json").read_bytes()
        calls.append((run_dir, output_dir, requested, manifest_bytes))
        assert b'"complete":true' in manifest_bytes
        return _write_test_figure_manifest(
            run_dir, output_dir, requested=requested, status="complete"
        )

    result = run_gaussian_experiment(
        gaussian_config(tmp_path, figures=True), renderer=renderer
    )

    assert result.figure_status == "complete"
    assert result.figure_dir == result.run_dir.parent / "figures" / result.run_dir.name
    assert calls == [
        (
            result.run_dir,
            result.figure_dir,
            ("gaussian_spectrum",),
            (result.run_dir / "manifest.json").read_bytes(),
        )
    ]


def _write_test_figure_manifest(
    run_dir: Path,
    output_dir: Path,
    *,
    requested: tuple[str, ...],
    status: str,
) -> object:
    output_dir.mkdir(parents=True, exist_ok=True)
    figures: list[dict[str, str]] = []
    if status == "complete":
        png = output_dir / "gaussian-generalized-spectrum.png"
        pdf = output_dir / "gaussian-generalized-spectrum.pdf"
        png.write_bytes(b"\x89PNG test")
        pdf.write_bytes(b"%PDF test")
        figures.append(
            {
                "name": "gaussian_spectrum",
                "png": png.name,
                "png_sha256": hashlib.sha256(png.read_bytes()).hexdigest(),
                "pdf": pdf.name,
                "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            }
        )
        message = None
    else:
        message = "renderer reported failure"
    manifest_path = output_dir / "figure-manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "figures": figures,
                "message": message,
                "requested": list(requested),
                "run_dir": str(run_dir.resolve()),
                "status": status,
            }
        ),
        encoding="utf-8",
    )

    class Manifest:
        pass

    manifest = Manifest()
    manifest.status = status
    manifest.run_dir = run_dir
    manifest.output_dir = output_dir
    manifest.requested = requested
    manifest.manifest_path = manifest_path
    return manifest


def test_renderer_backed_failed_manifest_is_validated(tmp_path: Path):
    def renderer(
        run_dir: Path, output_dir: Path, *, requested: tuple[str, ...]
    ) -> object:
        return _write_test_figure_manifest(
            run_dir, output_dir, requested=requested, status="failed"
        )

    result = run_gaussian_experiment(
        gaussian_config(tmp_path, figures=True), renderer=renderer
    )

    assert result.status == "pass"
    assert result.figure_status == "failed"
    saved = json.loads((result.figure_dir / "figure-manifest.json").read_text())
    assert saved["status"] == "failed"
    assert saved["message"] == "renderer reported failure"


def test_renderer_complete_manifest_with_wrong_inventory_hash_is_recorded_as_failure(
    tmp_path: Path,
):
    def renderer(
        run_dir: Path, output_dir: Path, *, requested: tuple[str, ...]
    ) -> object:
        manifest = _write_test_figure_manifest(
            run_dir, output_dir, requested=requested, status="complete"
        )
        (output_dir / "gaussian-generalized-spectrum.png").write_bytes(
            b"\x89PNG changed after manifest"
        )
        return manifest

    result = run_gaussian_experiment(
        gaussian_config(tmp_path, figures=True), renderer=renderer
    )

    assert result.status == "pass"
    assert result.figure_status == "failed"
    failure = json.loads((result.figure_dir / "figure-failure.json").read_text())
    assert failure["status"] == "failed"
    assert "unbacked" in failure["message"]


@pytest.mark.parametrize("returned_status", ["complete", "failed"])
def test_unbacked_renderer_status_is_recorded_as_failure(
    tmp_path: Path, returned_status: str
):
    class UnbackedManifest:
        status = returned_status
        manifest_path = None

    result = run_gaussian_experiment(
        gaussian_config(tmp_path, figures=True),
        renderer=lambda *_args, **_kwargs: UnbackedManifest(),
    )

    assert result.status == "pass"
    assert result.figure_status == "failed"
    saved = json.loads((result.figure_dir / "figure-manifest.json").read_text())
    assert saved["status"] == "failed"
    assert "unbacked" in saved["message"]


def test_renderer_failure_cannot_change_finalized_numerical_status_or_bytes(
    tmp_path: Path,
):
    baseline = run_gaussian_experiment(
        gaussian_config(tmp_path, name="gaussian baseline")
    )
    expected_metrics = (baseline.run_dir / "metrics.json").read_bytes()

    def failing_renderer(*_: object, **__: object) -> None:
        raise RuntimeError("deliberate renderer failure")

    failed = run_gaussian_experiment(
        gaussian_config(tmp_path, figures=True, name="gaussian failed figure"),
        renderer=failing_renderer,
    )

    assert failed.status == "pass"
    assert failed.figure_status == "failed"
    assert (failed.run_dir / "metrics.json").read_bytes() == expected_metrics
    assert b'"complete":true' in (failed.run_dir / "manifest.json").read_bytes()
    assert (failed.figure_dir / "figure-manifest.json").is_file()


def test_saved_metrics_expose_independent_literal_oracles(tmp_path: Path):
    result = run_gaussian_experiment(gaussian_config(tmp_path))
    required = {
        "GAU-01_energy_residual",
        "GAU-01_laplacian_energy_residual",
        "GAU-01_determinant_oracle_residual",
        "GAU-01_ordinary_spectrum_oracle_residual",
        "GAU-01_ordinary_spectrum_change_control",
        "GAU-01_commuting_square_residual",
        "GAU-02_scalar_schur_oracle_residual",
        "GAU-02_kron_schur_oracle_residual",
        "GAU-02_kron_nonclosure_control",
    }

    assert required <= set(result.metrics)
    assert all(result.metrics[name].status == "pass" for name in required)
    assert result.metrics["GAU-01_energy_residual"].value <= result.metrics[
        "GAU-01_energy_residual"
    ].tolerance
    assert result.metrics["GAU-01_ordinary_spectrum_oracle_residual"].value <= result.metrics[
        "GAU-01_ordinary_spectrum_oracle_residual"
    ].tolerance
    assert result.metrics["GAU-01_ordinary_spectrum_change_control"].value > result.metrics[
        "GAU-01_ordinary_spectrum_change_control"
    ].tolerance
    assert result.metrics["GAU-01_commuting_square_residual"].value <= result.metrics[
        "GAU-01_commuting_square_residual"
    ].tolerance
    assert set(result.arrays) >= {
        "coarse_frames",
        "expected_coarse_precision",
        "expected_transformed_coarse_precision",
        "expected_transformed_prolongator",
    }
    np.testing.assert_allclose(result.arrays["coarse_frames"], [np.diag([5.0, 2.0])])
    np.testing.assert_allclose(result.arrays["expected_coarse_precision"], np.diag([6.0, 8.0]))
    np.testing.assert_allclose(
        result.arrays["expected_transformed_coarse_precision"],
        np.diag([6.0 / 25.0, 2.0]),
    )
    np.testing.assert_allclose(
        result.arrays["expected_transformed_prolongator"],
        np.array(
            [
                [2.0 / 5.0, 0.0],
                [0.0, 1.0 / 2.0],
                [1.0 / 5.0, 0.0],
                [0.0, 3.0 / 2.0],
            ]
        ),
    )


def test_invalid_renderer_status_is_recorded_as_a_figure_failure(tmp_path: Path):
    class InvalidManifest:
        status = "unknown"

    result = run_gaussian_experiment(
        gaussian_config(tmp_path, figures=True),
        renderer=lambda *_args, **_kwargs: InvalidManifest(),
    )

    assert result.status == "pass"
    assert result.figure_status == "failed"
    assert (result.figure_dir / "figure-manifest.json").is_file()


def test_failure_recorder_error_cannot_invalidate_finalized_numerics(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.figures as figures

    def fail_renderer(*_: object, **__: object) -> None:
        raise RuntimeError("primary render failure")

    def fail_recorder(*_: object, **__: object) -> None:
        raise OSError("secondary failure record error")

    monkeypatch.setattr(figures, "record_figure_failure", fail_recorder)
    result = run_gaussian_experiment(
        gaussian_config(tmp_path, figures=True), renderer=fail_renderer
    )

    assert result.status == "pass"
    assert result.figure_status == "failed"
    assert b'"complete":true' in (result.run_dir / "manifest.json").read_bytes()


def test_wrong_experiment_type_and_nonconfig_are_rejected_before_artifacts(tmp_path: Path):
    finite = gaussian_config(tmp_path)
    finite = ExperimentConfig.from_dicts(
        {"name": "wrong", "seed": 1},
        {"experiment": "finite_exact", "retained_interaction_order": 2},
        {
            "dtype": "float64",
            "atol": 1e-12,
            "rtol": 1e-10,
            "min_spd_rcond": 1e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(tmp_path),
            "collect_diagnostics": False,
            "render_figures": False,
        },
    )

    with pytest.raises(TypeError, match="ExperimentConfig"):
        run_gaussian_experiment({})  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="gaussian_realization"):
        run_gaussian_experiment(finite)
    assert list(tmp_path.iterdir()) == []


def test_gaussian_launcher_is_click_to_run_from_a_fresh_uninstalled_checkout(
    tmp_path: Path,
):
    repository = Path(__file__).resolve().parents[1]
    checkout = tmp_path / "fresh-checkout"
    checkout.mkdir()
    shutil.copy2(repository / "run_gaussian_lab.py", checkout / "run_gaussian_lab.py")
    shutil.copytree(repository / "src", checkout / "src")
    environment = {
        key: value
        for key, value in __import__("os").environ.items()
        if key not in {"PYTHONPATH", "PYTHONHOME"} and not key.startswith("PYTEST_")
    }

    completed = subprocess.run(
        [sys.executable, "run_gaussian_lab.py"],
        cwd=checkout,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "run_dir=" in completed.stdout
    assert "status=pass" in completed.stdout
    source = (checkout / "run_gaussian_lab.py").read_text(encoding="utf-8")
    assert "import argparse" not in source
    assert "from click" not in source.lower()
    assert "import typer" not in source.lower()
