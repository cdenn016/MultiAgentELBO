from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import importlib
import json
from pathlib import Path
import shutil
import subprocess
from typing import Callable

import numpy as np
import pytest

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.realizations.gaussian.confirmatory_analysis import (
    analyze_holdout,
    analyze_primary,
)
from multiagent_elbo.realizations.gaussian.fixed_ray import (
    FixedRayTrajectory,
    blocking_scheme_dispersion,
    build_preregistered_system,
    generate_initial_coefficients,
    iterate_fixed_ray,
    job_seed,
)


SCIENTIFIC_REVISION = "a" * 40
DIAGNOSTIC_REVISION = "d" * 40
SCHEMES = ("adjacent_pairs", "balanced_alternating")
PRIMARY_JOB_IDS = tuple(f"C{index:03d}" for index in range(1, 31))
HOLDOUT_JOB_IDS = tuple(f"H{index:03d}" for index in range(1, 11))
JOB_IDS = PRIMARY_JOB_IDS + HOLDOUT_JOB_IDS
ORIGINAL_INVENTORY_NAMES = (
    "config.json",
    "confirmatory_arrays.npz",
    "confirmatory_endpoints.json",
    "confirmatory_execution.json",
    "confirmatory_job_table.json",
    "holdout_analysis.json",
    "manifest.json",
    "metrics.json",
    "primary_analysis.json",
    "primary_execution.json",
)
TRACKED_SCIENTIFIC_SUBSET = (
    "config.json",
    "confirmatory_arrays.npz",
    "confirmatory_endpoints.json",
    "confirmatory_job_table.json",
    "holdout_analysis.json",
    "manifest.json",
    "metrics.json",
    "primary_analysis.json",
)
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TRACKED_EXTRACT = (
    REPOSITORY_ROOT
    / "docs"
    / "verification"
    / "evidence"
    / "2026-08-10-gaussian-confirmatory-fcb2c49"
)
DIAGNOSTIC_ARTIFACTS = {
    "config.json",
    "manifest.json",
    "fixed_model_support_certificate.json",
    "fixed_model_spectral_diagnostics.json",
    "fixed_model_trajectory_diagnostics.json",
    "fixed_model_explanation.json",
    "fixed_model_diagnostic_arrays.npz",
    "metrics.json",
}
SEMANTIC_DIAGNOSTIC_JSON = (
    "fixed_model_support_certificate.json",
    "fixed_model_spectral_diagnostics.json",
    "fixed_model_trajectory_diagnostics.json",
    "fixed_model_explanation.json",
    "metrics.json",
)


def _diagnostic_module():
    return importlib.import_module(
        "multiagent_elbo.realizations.gaussian.fixed_ray_diagnostic_experiment"
    )


def _diagnostic_config(root: Path) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "fixed-model-attraction-diagnostic", "seed": 20260809},
        {
            "experiment": "gaussian_fixed_ray",
            "fixture": "gaussian_fixed_ray_v1",
            "preregistration": "2026-08-09-gaussian-fixed-ray-v1",
            "blocking_schemes": list(SCHEMES),
            "matrix_dimension": 2,
        },
        {
            "dtype": "float64",
            "atol": 1.0e-12,
            "rtol": 1.0e-10,
            "min_spd_rcond": 1.0e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(root),
            "collect_diagnostics": True,
            "render_figures": False,
        },
        {
            "backend": "cpu",
            "dtype": "float64",
            "device_index": 0,
            "batch_size": 4096,
            "deterministic": True,
            "allow_tf32": False,
            "cpu_cuda_parity": False,
            "cuda_worker_python": r"C:\anaconda\python.exe",
            "heavy_sweep_enabled": False,
        },
    )


def _patch_clean_provenance(
    monkeypatch: pytest.MonkeyPatch,
    module: object,
    *,
    dirty: bool = False,
) -> None:
    def provenance(
        _repo_root: Path,
        _theory_root: Path,
        config_hash: str,
        _streams: object,
    ) -> dict[str, object]:
        return {
            "config_hash": config_hash,
            "git_commit": DIAGNOSTIC_REVISION,
            "git_dirty": dirty,
            "theory_sha256": "e" * 64,
            "input_hashes": {
                "resolved_config_sha256": config_hash,
                "theory_tree_sha256": "e" * 64,
            },
        }

    monkeypatch.setattr(module, "collect_provenance", provenance, raising=False)


def _independent_array_sha256(name: str, values: np.ndarray) -> str:
    array = np.ascontiguousarray(values)
    digest = sha256()
    for payload in (
        b"fixed-model-diagnostic-array-v1",
        name.encode("utf-8"),
        array.dtype.str.encode("ascii"),
    ):
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    digest.update(array.ndim.to_bytes(8, "big"))
    for dimension in array.shape:
        digest.update(int(dimension).to_bytes(8, "big", signed=False))
    content = array.tobytes(order="C")
    digest.update(len(content).to_bytes(8, "big"))
    digest.update(content)
    return digest.hexdigest()


def _stored_output_trajectory(
    source: object,
    job_index: int,
    scheme: str,
    system: object,
) -> FixedRayTrajectory:
    job_id = JOB_IDS[job_index]
    coefficients = np.asarray(
        source.arrays[f"{job_id}_{scheme}_coefficients"],
        dtype=np.float64,
    )
    endpoint = source.endpoint_records[job_index]["schemes"][scheme]
    ray = np.asarray(system.perron_ray, dtype=np.float64)
    projection = np.outer(ray, ray) / float(np.dot(ray, ray))
    retained_vectors = np.asarray(
        [
            (np.eye(coefficients.shape[1]) - projection)
            @ difference
            / system.log_block_scale
            for difference in coefficients[1:] - coefficients[:-1]
        ],
        dtype=np.float64,
    )
    return FixedRayTrajectory(
        scheme=scheme,
        coefficients=coefficients,
        coupling_matrices=(coefficients[:, :, None, None] * system.matrix_direction),
        projective_ray_angles=np.asarray(
            endpoint["projective_ray_angles"],
            dtype=np.float64,
        ),
        normalized_coupling_distances=np.asarray(
            endpoint["normalized_coupling_distances"],
            dtype=np.float64,
        ),
        scalarized_ray_construction_residuals=np.asarray(
            endpoint["scalarized_ray_construction_residuals"],
            dtype=np.float64,
        ),
        retained_beta_residual_vectors=retained_vectors,
        retained_beta_residuals=np.asarray(
            endpoint["retained_beta_residuals"],
            dtype=np.float64,
        ),
        basin_exits=np.any(
            (coefficients < system.basin_lower) | (coefficients > system.basin_upper),
            axis=1,
        ),
        coefficient_conditioning=np.asarray(
            endpoint["coefficient_conditioning"],
            dtype=np.float64,
        ),
        matrix_condition=float(endpoint["matrix_condition"]),
    )


def _canonical_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _write_json(path: Path, payload: object) -> None:
    path.write_bytes(_canonical_bytes(payload))


def _file_record(path: Path) -> dict[str, object]:
    content = path.read_bytes()
    return {"sha256": sha256(content).hexdigest(), "size_bytes": len(content)}


def _job_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    specifications = (
        ("P", "pilot", 4, 202608090001),
        ("C", "confirmatory_primary", 30, 202608090101),
        ("H", "confirmatory_holdout", 10, 202608090201),
    )
    for prefix, role, count, first_seed in specifications:
        for offset in range(count):
            job_id = f"{prefix}{offset + 1:03d}"
            master_seed = first_seed + offset
            rows.append(
                {
                    "job_id": job_id,
                    "master_seed": master_seed,
                    "role": role,
                    "schemes": list(SCHEMES),
                    "steps": 8,
                    "substream_seed_u64": job_seed(master_seed, job_id),
                }
            )
    return rows


def _scheme_record(trajectory: FixedRayTrajectory) -> dict[str, object]:
    return {
        "basin_exit": bool(np.any(trajectory.basin_exits)),
        "coefficient_conditioning": trajectory.coefficient_conditioning.tolist(),
        "matrix_condition": trajectory.matrix_condition,
        "normalized_coupling_distances": (
            trajectory.normalized_coupling_distances.tolist()
        ),
        "projective_ray_angles": trajectory.projective_ray_angles.tolist(),
        "rejected": False,
        "rejection_reason": None,
        "retained_beta_residuals": trajectory.retained_beta_residuals.tolist(),
        "scalarized_ray_construction_residuals": (
            trajectory.scalarized_ray_construction_residuals.tolist()
        ),
    }


@dataclass
class SyntheticExtract:
    path: Path
    binding_payload: dict[str, object]

    def binding(self):
        module = _diagnostic_module()
        return module.ConfirmatorySourceBinding.from_mapping(
            json.loads(json.dumps(self.binding_payload)),
            diagnostic_revision=DIAGNOSTIC_REVISION,
        )

    def read_json(self, name: str) -> dict[str, object]:
        return json.loads((self.path / name).read_text(encoding="utf-8"))

    def rewrite_json(
        self,
        name: str,
        mutate: Callable[[dict[str, object]], None],
    ) -> None:
        payload = self.read_json(name)
        mutate(payload)
        _write_json(self.path / name, payload)
        self.refresh_owned_hash(name)

    def rewrite_arrays(
        self,
        mutate: Callable[[dict[str, np.ndarray]], None],
    ) -> None:
        archive_path = self.path / "confirmatory_arrays.npz"
        with np.load(archive_path, allow_pickle=False) as archive:
            arrays = {
                name: np.array(archive[name], copy=True) for name in archive.files
            }
        mutate(arrays)
        np.savez(archive_path, **arrays)
        self.refresh_owned_hash("confirmatory_arrays.npz")

    def refresh_owned_hash(self, name: str) -> None:
        inventory = self.binding_payload["complete_original_inventory"]
        assert isinstance(inventory, dict)
        inventory[name] = _file_record(self.path / name)
        _write_json(self.path / "source_binding.json", self.binding_payload)


@pytest.fixture
def synthetic_extract(tmp_path: Path) -> SyntheticExtract:
    source_dir = tmp_path / "scientific-extract"
    source_dir.mkdir()
    system = build_preregistered_system()
    rows = _job_rows()
    selected = [row for row in rows if row["job_id"] in JOB_IDS]
    arrays: dict[str, np.ndarray] = {}
    records: list[dict[str, object]] = []
    for row in selected:
        job_id = str(row["job_id"])
        master_seed = int(row["master_seed"])
        initial = generate_initial_coefficients(master_seed, job_id)
        trajectories = {
            scheme: iterate_fixed_ray(
                system,
                initial,
                scheme=scheme,
                steps=8,
            )
            for scheme in SCHEMES
        }
        arrays[f"{job_id}_initial_coefficients"] = initial
        for scheme, trajectory in trajectories.items():
            arrays[f"{job_id}_{scheme}_coefficients"] = trajectory.coefficients
        records.append(
            {
                "accepted_gate_sha256": "1" * 64,
                "blocking_scheme_dispersion": blocking_scheme_dispersion(
                    trajectories[SCHEMES[0]].coefficients,
                    trajectories[SCHEMES[1]].coefficients,
                ).tolist(),
                "config_sha256": "",
                "initial_coefficients": initial.tolist(),
                "initial_coefficients_sha256": sha256(
                    initial.tobytes(order="C")
                ).hexdigest(),
                "job_id": job_id,
                "master_seed": master_seed,
                "outer_attempt_count": 1,
                "retry_lineage": [{"outer_attempt": 1, "parent_attempt": None}],
                "role": str(row["role"]),
                "schema_version": "gaussian-fixed-ray-confirmatory-job-v1",
                "schemes": {
                    scheme: _scheme_record(trajectories[scheme]) for scheme in SCHEMES
                },
                "scientific_analysis_eligibility": True,
                "source_revision": SCIENTIFIC_REVISION,
                "terminal_status": "completed",
                "worker_exchange_count": 16,
            }
        )

    resolved_config = {
        "compute": {
            "backend": "cuda",
            "deterministic": True,
            "dtype": "float64",
            "heavy_sweep_enabled": True,
        },
        "run": {"name": "synthetic-confirmatory", "seed": 20260809},
        "theory": {
            "blocking_schemes": list(SCHEMES),
            "experiment": "gaussian_fixed_ray",
            "fixture": "gaussian_fixed_ray_v1",
            "matrix_dimension": 2,
            "preregistration": "2026-08-09-gaussian-fixed-ray-v1",
        },
    }
    config_hash = sha256(_canonical_bytes(resolved_config)).hexdigest()
    for record in records:
        record["config_sha256"] = config_hash
    config = {"config_hash": config_hash, "resolved_config": resolved_config}
    job_table = {
        "confirmatory_executed": True,
        "executed_holdout_job_ids": list(HOLDOUT_JOB_IDS),
        "executed_pilot_jobs": rows[:4],
        "executed_primary_job_ids": list(PRIMARY_JOB_IDS),
        "heavy_sweep_enabled": True,
        "jobs": rows,
        "preregistration": "2026-08-09-gaussian-fixed-ray-v1",
        "primary_scale_window": [4, 5, 6, 7, 8],
        "schema_version": "gaussian-fixed-ray-job-table-v1",
        "sentinel_job_ids": ["C001", "C015", "C030", "H001", "H010"],
    }
    planned_table = dict(job_table)
    planned_table.pop("executed_primary_job_ids")
    planned_table.pop("executed_holdout_job_ids")
    planned_table["confirmatory_executed"] = False
    canonical_job_table_hash = sha256(_canonical_bytes(planned_table)).hexdigest()

    primary_execution_hash = "2" * 64
    primary = analyze_primary(
        records[:30],
        protocol_id="2026-08-09-gaussian-fixed-ray-v1a",
        job_table_sha256=canonical_job_table_hash,
        decision_stability=True,
        premises_passed=True,
        gpu_gate_complete=True,
        primary_execution_sha256=primary_execution_hash,
        config_sha256=config_hash,
        source_revision=SCIENTIFIC_REVISION,
        accepted_gate_sha256="1" * 64,
    )
    _write_json(source_dir / "primary_analysis.json", primary)
    primary_hash = _file_record(source_dir / "primary_analysis.json")["sha256"]
    assert isinstance(primary_hash, str)
    holdout = analyze_holdout(
        records[30:],
        protocol_id="2026-08-09-gaussian-fixed-ray-v1a",
        job_table_sha256=canonical_job_table_hash,
        primary_analysis_sha256=primary_hash,
    )
    metrics = {
        "confirmatory_primary_classification": {
            "assessment_scope": "implementation_check",
            "claim_origin": "APPLICATION_SPECIFIC",
            "interpretation": "Synthetic finite confirmatory classification.",
            "status": primary["classification"],
            "theorem_status": "NUMERICAL",
            "tolerance": 0.0,
            "value": 0.0,
            "verification_state": "CANDIDATE",
        }
    }
    manifest = {
        "artifacts": {name: "complete" for name in ORIGINAL_INVENTORY_NAMES},
        "complete": True,
        "config_hash": config_hash,
        "provenance": {
            "config_hash": config_hash,
            "confirmatory_executed": True,
            "effective_backend": "cuda_worker",
            "effective_dtype": "float64",
            "experiment_scope": "gaussian_fixed_ray_confirmatory_40_job",
            "git_commit": SCIENTIFIC_REVISION,
            "git_dirty": False,
            "input_hashes": {
                "job_table_sha256": canonical_job_table_hash,
                "primary_analysis_sha256": primary_hash,
                "primary_execution_sha256": primary_execution_hash,
                "resolved_config_sha256": config_hash,
            },
        },
    }
    payloads = {
        "config.json": config,
        "confirmatory_endpoints.json": {
            "records": records,
            "schema_version": "gaussian-fixed-ray-confirmatory-endpoints-v1",
        },
        "confirmatory_job_table.json": job_table,
        "holdout_analysis.json": holdout,
        "manifest.json": manifest,
        "metrics.json": metrics,
    }
    for name, payload in payloads.items():
        _write_json(source_dir / name, payload)
    np.savez(source_dir / "confirmatory_arrays.npz", **arrays)

    original_inventory: dict[str, dict[str, object]] = {
        name: _file_record(source_dir / name) for name in TRACKED_SCIENTIFIC_SUBSET
    }
    original_inventory["confirmatory_execution.json"] = {
        "sha256": "3" * 64,
        "size_bytes": 9_000_000,
    }
    original_inventory["primary_execution.json"] = {
        "sha256": primary_execution_hash,
        "size_bytes": 7_000_000,
    }
    ordered_inventory = {
        name: original_inventory[name] for name in ORIGINAL_INVENTORY_NAMES
    }
    binding_payload: dict[str, object] = {
        "schema_version": "gaussian-confirmatory-source-binding-v1",
        "scientific_revision": SCIENTIFIC_REVISION,
        "coordinator_evidence_sha256": "4" * 64,
        "complete_original_inventory": ordered_inventory,
        "scientific_payload_hashes": {
            "job_table_canonical_json_sha256": canonical_job_table_hash,
            "job_table_canonical_json_format": (
                "json.dumps(_job_table(config), sort_keys=True, "
                "separators=(',', ':'), allow_nan=False).encode('utf-8')"
            ),
            "published_job_table_reconstruction": {
                "remove_fields": [
                    "executed_primary_job_ids",
                    "executed_holdout_job_ids",
                ],
                "set_confirmatory_executed": False,
            },
        },
        "tracked_scientific_subset": list(TRACKED_SCIENTIFIC_SUBSET),
    }
    _write_json(source_dir / "source_binding.json", binding_payload)
    return SyntheticExtract(source_dir, binding_payload)


def _assert_validation_rejects(extract: SyntheticExtract) -> None:
    module = _diagnostic_module()
    forbidden_output = extract.path.parent / "must-not-be-created"
    with pytest.raises((TypeError, ValueError)):
        binding = extract.binding()
        module.validate_scientific_extract(extract.path, binding)
    assert not forbidden_output.exists()


def _head_revision() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _tracked_binding():
    module = _diagnostic_module()
    return module.ConfirmatorySourceBinding.from_path(
        TRACKED_EXTRACT / "source_binding.json",
        diagnostic_revision=_head_revision(),
    )


def test_public_api_is_exported_from_the_gaussian_package() -> None:
    from multiagent_elbo.realizations.gaussian import (
        ConfirmatorySourceBinding,
        ReplayResult,
        ValidatedConfirmatorySource,
        replay_confirmatory_diagnostics,
        validate_scientific_extract,
    )

    assert ConfirmatorySourceBinding.__name__ == "ConfirmatorySourceBinding"
    assert ValidatedConfirmatorySource.__name__ == "ValidatedConfirmatorySource"
    assert ReplayResult.__name__ == "ReplayResult"
    assert callable(validate_scientific_extract)
    assert callable(replay_confirmatory_diagnostics)


def test_publication_emits_exact_artifact_inventory(
    synthetic_extract: SyntheticExtract,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _diagnostic_module()
    binding = synthetic_extract.binding()
    _patch_clean_provenance(monkeypatch, module)
    result = module.run_fixed_model_diagnostic(
        _diagnostic_config(tmp_path / "published"),
        binding,
        synthetic_extract.path,
    )

    assert {path.name for path in result.run_dir.iterdir()} == DIAGNOSTIC_ARTIFACTS
    manifest = json.loads((result.run_dir / "manifest.json").read_text("utf-8"))
    provenance = manifest["provenance"]
    assert provenance["artifact_kind"] == "fixed_model_attraction_diagnostic"
    assert provenance["git_commit"] == DIAGNOSTIC_REVISION
    assert provenance["git_dirty"] is False
    assert provenance["scientific_revision"] == SCIENTIFIC_REVISION
    assert provenance["source_binding_sha256"] == (
        binding.canonical_source_binding_sha256
    )
    assert provenance["theory_sha256"] == "e" * 64
    assert set(provenance["source_hashes"]) == set(ORIGINAL_INVENTORY_NAMES)
    artifact_hashes = provenance["artifact_sha256"]
    assert set(artifact_hashes) == DIAGNOSTIC_ARTIFACTS - {"manifest.json"}
    for name, digest in artifact_hashes.items():
        assert sha256((result.run_dir / name).read_bytes()).hexdigest() == digest


def test_source_binding_digest_separates_content_addressed_run_identity(
    synthetic_extract: SyntheticExtract,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _diagnostic_module()
    _patch_clean_provenance(monkeypatch, module)
    second_source = tmp_path / "second-scientific-extract"
    shutil.copytree(synthetic_extract.path, second_source)
    second_payload = json.loads(json.dumps(synthetic_extract.binding_payload))
    second_payload["complete_original_inventory"]["confirmatory_execution.json"][
        "sha256"
    ] = "5" * 64
    _write_json(second_source / "source_binding.json", second_payload)
    first_binding = synthetic_extract.binding()
    second_binding = module.ConfirmatorySourceBinding.from_mapping(
        second_payload,
        diagnostic_revision=DIAGNOSTIC_REVISION,
    )
    config = _diagnostic_config(tmp_path / "published")

    first = module.run_fixed_model_diagnostic(
        config,
        first_binding,
        synthetic_extract.path,
    )
    second = module.run_fixed_model_diagnostic(config, second_binding, second_source)

    assert first.run_dir != second.run_dir
    assert first_binding.canonical_source_binding_sha256 in first.run_dir.parts[-2]
    assert second_binding.canonical_source_binding_sha256 in second.run_dir.parts[-2]


def test_publication_preserves_status_and_separate_population_contracts(
    synthetic_extract: SyntheticExtract,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _diagnostic_module()
    _patch_clean_provenance(monkeypatch, module)
    result = module.run_fixed_model_diagnostic(
        _diagnostic_config(tmp_path / "published"),
        synthetic_extract.binding(),
        synthetic_extract.path,
    )

    support = json.loads(
        (result.run_dir / "fixed_model_support_certificate.json").read_text("utf-8")
    )
    spectral = json.loads(
        (result.run_dir / "fixed_model_spectral_diagnostics.json").read_text("utf-8")
    )
    trajectory = json.loads(
        (result.run_dir / "fixed_model_trajectory_diagnostics.json").read_text("utf-8")
    )
    explanation = json.loads(
        (result.run_dir / "fixed_model_explanation.json").read_text("utf-8")
    )
    metrics = json.loads((result.run_dir / "metrics.json").read_text("utf-8"))

    assert support["theorem_status"] == "ESTABLISHED"
    assert support["mathematical_verification_state"] == "CANDIDATE"
    assert support["verification_state"] == "CANDIDATE"
    assert support["claim_origin"] == "APPLICATION_SPECIFIC"
    assert support["actual_run_premises_validated"] is True
    assert support["paired_support_boundary_reachable"] is False
    assert set(spectral["maps"]) == set(SCHEMES)
    assert all(
        record["theorem_status"] == "NUMERICAL"
        and record["verification_state"] == "CANDIDATE"
        and record["claim_origin"] == "APPLICATION_SPECIFIC"
        for record in spectral["maps"].values()
    )
    assert trajectory["primary_C"]["population"] == "C"
    assert trajectory["primary_C"]["scope"] == "confirmatory_primary"
    assert trajectory["primary_C"]["job_count"] == 30
    assert trajectory["descriptive_H"]["population"] == "H"
    assert trajectory["descriptive_H"]["scope"] == "descriptive_replication_only"
    assert trajectory["descriptive_H"]["job_count"] == 10
    assert len(trajectory["records"]) == 80
    assert {record["job_id"][0] for record in trajectory["records"]} == {"C", "H"}
    assert "pooled" not in trajectory
    assert explanation["completed_finite_classification"] == "inconclusive"
    assert explanation["mathematical_attraction"]["conclusion"] == "INCONCLUSIVE"
    assert explanation["unrestricted_attraction"]["theorem_status"] == "OPEN"
    assert explanation["unrestricted_attraction"]["conclusion"] == "INCONCLUSIVE"
    assert explanation["universality"]["theorem_status"] == "OPEN"
    assert explanation["universality"]["conclusion"] == "INCONCLUSIVE"
    assert explanation["population_contract"] == {
        "primary": "C001-C030",
        "descriptive_replication_only": "H001-H010",
    }
    assert all(
        metric["verification_state"] == "CANDIDATE"
        and metric["claim_origin"] == "APPLICATION_SPECIFIC"
        for metric in metrics.values()
    )
    serialized = json.dumps(
        [support, spectral, trajectory, explanation, metrics],
        sort_keys=True,
    )
    assert "EVIDENCE_VERIFIED" not in serialized
    assert "REFUTED" not in serialized


def test_publication_is_semantically_deterministic_across_output_roots(
    synthetic_extract: SyntheticExtract,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _diagnostic_module()
    _patch_clean_provenance(monkeypatch, module)
    binding = synthetic_extract.binding()
    first = module.run_fixed_model_diagnostic(
        _diagnostic_config(tmp_path / "first-root"),
        binding,
        synthetic_extract.path,
    )
    second = module.run_fixed_model_diagnostic(
        _diagnostic_config(tmp_path / "second-root"),
        binding,
        synthetic_extract.path,
    )

    for name in SEMANTIC_DIAGNOSTIC_JSON:
        first_payload = json.loads((first.run_dir / name).read_text("utf-8"))
        second_payload = json.loads((second.run_dir / name).read_text("utf-8"))
        assert first_payload == second_payload
    first_trajectory = json.loads(
        (first.run_dir / "fixed_model_trajectory_diagnostics.json").read_text("utf-8")
    )
    second_trajectory = json.loads(
        (second.run_dir / "fixed_model_trajectory_diagnostics.json").read_text("utf-8")
    )
    assert first_trajectory["array_hash_algorithm"] == (
        "fixed-model-diagnostic-array-v1-name-dtype-shape-c-bytes"
    )
    assert first_trajectory["array_sha256"] == second_trajectory["array_sha256"]
    expected_hashes = first_trajectory["array_sha256"]
    for run in (first, second):
        with np.load(
            run.run_dir / "fixed_model_diagnostic_arrays.npz",
            allow_pickle=False,
        ) as archive:
            assert set(archive.files) == set(expected_hashes)
            for name in sorted(archive.files):
                values = archive[name]
                assert not values.dtype.hasobject
                assert values.dtype.kind not in {"O", "S", "U", "V"}
                assert bool(np.all(np.isfinite(values)))
                assert _independent_array_sha256(name, values) == expected_hashes[name]


@pytest.mark.parametrize(
    ("bad_array", "expected_message"),
    [
        (np.asarray([object()], dtype=object), "plain numeric dtypes"),
        (np.asarray([np.nan], dtype=np.float64), "only finite values"),
    ],
    ids=("object", "nonfinite"),
)
def test_publication_rejects_bad_diagnostic_arrays_before_output_creation(
    synthetic_extract: SyntheticExtract,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    bad_array: np.ndarray,
    expected_message: str,
) -> None:
    module = _diagnostic_module()
    _patch_clean_provenance(monkeypatch, module)
    original = module.spectral_diagnostics

    def poisoned_spectral_diagnostics(matrix: object, ray: object) -> dict[str, object]:
        record = dict(original(matrix, ray))
        record["invalid_array"] = bad_array
        return record

    monkeypatch.setattr(module, "spectral_diagnostics", poisoned_spectral_diagnostics)
    output_root = tmp_path / "must-not-exist"
    with pytest.raises(ValueError, match=expected_message):
        module.run_fixed_model_diagnostic(
            _diagnostic_config(output_root),
            synthetic_extract.binding(),
            synthetic_extract.path,
        )
    assert not output_root.exists()


def test_publication_rejects_dirty_provenance_with_zero_writes(
    synthetic_extract: SyntheticExtract,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _diagnostic_module()
    _patch_clean_provenance(monkeypatch, module, dirty=True)
    output_root = tmp_path / "must-not-exist"

    with pytest.raises(ValueError, match="clean source tree"):
        module.run_fixed_model_diagnostic(
            _diagnostic_config(output_root),
            synthetic_extract.binding(),
            synthetic_extract.path,
        )
    assert not output_root.exists()


def test_publication_rejects_invalid_source_with_zero_writes(
    synthetic_extract: SyntheticExtract,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _diagnostic_module()
    _patch_clean_provenance(monkeypatch, module)
    payload = json.loads(json.dumps(synthetic_extract.binding_payload))
    payload["complete_original_inventory"]["primary_analysis.json"]["sha256"] = "0" * 64
    invalid_binding = module.ConfirmatorySourceBinding.from_mapping(
        payload,
        diagnostic_revision=DIAGNOSTIC_REVISION,
    )
    output_root = tmp_path / "must-not-exist"

    with pytest.raises(ValueError, match="primary_analysis.json hash or size drifted"):
        module.run_fixed_model_diagnostic(
            _diagnostic_config(output_root),
            invalid_binding,
            synthetic_extract.path,
        )
    assert not output_root.exists()


def test_synthetic_extract_validates_into_immutable_defensive_copies(
    synthetic_extract: SyntheticExtract,
) -> None:
    module = _diagnostic_module()
    source = module.validate_scientific_extract(
        synthetic_extract.path,
        synthetic_extract.binding(),
    )

    assert source.scientific_revision == SCIENTIFIC_REVISION
    assert source.diagnostic_revision == DIAGNOSTIC_REVISION
    assert source.scientific_revision != source.diagnostic_revision
    assert source.job_ids == JOB_IDS
    assert source.schemes == SCHEMES
    assert len(source.arrays) == 120
    assert source.recorded_execution_metadata == {
        "recorded_worker_exchange_count": 640,
        "recorded_retried_job_count": 0,
        "omitted_execution_logs_revalidated": False,
        "omitted_execution_logs": (
            "confirmatory_execution.json",
            "primary_execution.json",
        ),
    }
    first = source.arrays["C001_initial_coefficients"]
    assert not first.flags.writeable
    with pytest.raises(ValueError):
        first[0] = -1.0
    with pytest.raises(TypeError):
        source.arrays["new"] = np.ones(1)
    with pytest.raises(TypeError):
        source.manifest["complete"] = False

    original = first.copy()
    synthetic_extract.rewrite_arrays(
        lambda arrays: arrays["C001_initial_coefficients"].__setitem__(0, 99.0)
    )
    assert np.array_equal(source.arrays["C001_initial_coefficients"], original)


def test_validated_source_array_backing_cannot_be_made_writeable(
    synthetic_extract: SyntheticExtract,
) -> None:
    module = _diagnostic_module()
    source = module.validate_scientific_extract(
        synthetic_extract.path,
        synthetic_extract.binding(),
    )

    validated = source.arrays["C001_initial_coefficients"]
    assert not validated.flags.writeable
    with pytest.raises(ValueError):
        validated.setflags(write=True)


@pytest.mark.parametrize("name", TRACKED_SCIENTIFIC_SUBSET)
def test_synthetic_extract_fails_closed_on_every_owned_hash(
    synthetic_extract: SyntheticExtract,
    name: str,
) -> None:
    path = synthetic_extract.path / name
    path.write_bytes(path.read_bytes() + b"\n")

    _assert_validation_rejects(synthetic_extract)


@pytest.mark.parametrize(
    "missing_name",
    ("confirmatory_execution.json", "primary_execution.json"),
)
def test_synthetic_extract_requires_all_ten_inventory_entries(
    synthetic_extract: SyntheticExtract,
    missing_name: str,
) -> None:
    inventory = synthetic_extract.binding_payload["complete_original_inventory"]
    assert isinstance(inventory, dict)
    inventory.pop(missing_name)

    _assert_validation_rejects(synthetic_extract)


def test_synthetic_extract_distinguishes_raw_and_canonical_job_table_hashes(
    synthetic_extract: SyntheticExtract,
) -> None:
    payload_hashes = synthetic_extract.binding_payload["scientific_payload_hashes"]
    assert isinstance(payload_hashes, dict)
    payload_hashes["job_table_canonical_json_sha256"] = "0" * 64

    _assert_validation_rejects(synthetic_extract)


def test_synthetic_extract_rejects_source_revision_drift(
    synthetic_extract: SyntheticExtract,
) -> None:
    def mutate(payload: dict[str, object]) -> None:
        records = payload["records"]
        assert isinstance(records, list)
        records[0]["source_revision"] = "f" * 40

    synthetic_extract.rewrite_json("confirmatory_endpoints.json", mutate)
    _assert_validation_rejects(synthetic_extract)


def test_synthetic_extract_rejects_job_order_drift(
    synthetic_extract: SyntheticExtract,
) -> None:
    def mutate(payload: dict[str, object]) -> None:
        records = payload["records"]
        assert isinstance(records, list)
        records[0], records[1] = records[1], records[0]

    synthetic_extract.rewrite_json("confirmatory_endpoints.json", mutate)
    _assert_validation_rejects(synthetic_extract)


def test_synthetic_extract_rejects_duplicate_job_ids(
    synthetic_extract: SyntheticExtract,
) -> None:
    def mutate(payload: dict[str, object]) -> None:
        records = payload["records"]
        assert isinstance(records, list)
        records[1]["job_id"] = records[0]["job_id"]

    synthetic_extract.rewrite_json("confirmatory_endpoints.json", mutate)
    _assert_validation_rejects(synthetic_extract)


def test_synthetic_extract_rejects_scheme_inventory_drift(
    synthetic_extract: SyntheticExtract,
) -> None:
    def mutate(payload: dict[str, object]) -> None:
        records = payload["records"]
        assert isinstance(records, list)
        records[0]["schemes"].pop("balanced_alternating")

    synthetic_extract.rewrite_json("confirmatory_endpoints.json", mutate)
    _assert_validation_rejects(synthetic_extract)


def test_synthetic_extract_rejects_trajectory_shape_drift(
    synthetic_extract: SyntheticExtract,
) -> None:
    synthetic_extract.rewrite_arrays(
        lambda arrays: arrays.__setitem__(
            "C001_adjacent_pairs_coefficients",
            arrays["C001_adjacent_pairs_coefficients"][:-1],
        )
    )

    _assert_validation_rejects(synthetic_extract)


def test_synthetic_extract_rejects_npz_object_dtype(
    synthetic_extract: SyntheticExtract,
) -> None:
    synthetic_extract.rewrite_arrays(
        lambda arrays: arrays.__setitem__(
            "C001_initial_coefficients",
            np.asarray([object()] * 6, dtype=object),
        )
    )

    _assert_validation_rejects(synthetic_extract)


def test_synthetic_extract_rejects_endpoint_drift(
    synthetic_extract: SyntheticExtract,
) -> None:
    def mutate(payload: dict[str, object]) -> None:
        endpoint = payload["primary_endpoint"]
        assert isinstance(endpoint, dict)
        endpoint["estimate"] = float(endpoint["estimate"]) + 0.1

    synthetic_extract.rewrite_json("primary_analysis.json", mutate)
    _assert_validation_rejects(synthetic_extract)


@pytest.mark.parametrize("population", ("primary", "holdout"))
def test_synthetic_extract_rejects_primary_or_holdout_binding_drift(
    synthetic_extract: SyntheticExtract,
    population: str,
) -> None:
    if population == "primary":

        def mutate(payload: dict[str, object]) -> None:
            ids = payload["primary_job_ids"]
            assert isinstance(ids, list)
            ids[0] = "H001"

        synthetic_extract.rewrite_json("primary_analysis.json", mutate)
    else:

        def mutate(payload: dict[str, object]) -> None:
            payload["primary_analysis_sha256"] = "0" * 64

        synthetic_extract.rewrite_json("holdout_analysis.json", mutate)

    _assert_validation_rejects(synthetic_extract)


def test_npz_loader_explicitly_disables_pickle(
    synthetic_extract: SyntheticExtract,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _diagnostic_module()
    observed: list[object] = []
    real_load = np.load

    def checked_load(*args: object, **kwargs: object):
        observed.append(kwargs.get("allow_pickle"))
        return real_load(*args, **kwargs)

    monkeypatch.setattr(module.np, "load", checked_load)
    module.validate_scientific_extract(
        synthetic_extract.path,
        synthetic_extract.binding(),
    )

    assert observed == [False]


def test_synthetic_replay_regenerates_initials_and_invokes_80_calls(
    synthetic_extract: SyntheticExtract,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _diagnostic_module()
    source = module.validate_scientific_extract(
        synthetic_extract.path,
        synthetic_extract.binding(),
    )
    generated: list[tuple[int, str]] = []
    calls: list[tuple[str, str]] = []
    frozen_generator = module.generate_initial_coefficients

    def generation_spy(master_seed: int, job_id: str) -> np.ndarray:
        generated.append((master_seed, job_id))
        return frozen_generator(master_seed, job_id)

    def observe(job_id: str, scheme: str) -> None:
        calls.append((job_id, scheme))

    monkeypatch.setattr(module, "generate_initial_coefficients", generation_spy)
    result = module.replay_confirmatory_diagnostics(
        source,
        call_observer=observe,
    )

    assert generated == [
        (int(job["master_seed"]), job_id) for job, job_id in zip(source.jobs, JOB_IDS)
    ]
    expected_calls = [(job_id, scheme) for job_id in JOB_IDS for scheme in SCHEMES]
    assert calls == expected_calls
    assert result.operation == "deterministic_replay"
    assert result.call_count == 80
    assert result.scientific_revision == SCIENTIFIC_REVISION
    assert result.diagnostic_revision == DIAGNOSTIC_REVISION
    assert result.cpu_replay_atol == module.CPU_REPLAY_ATOL
    assert set(result.max_absolute_errors) == {
        "coefficients",
        "projective_ray_angles",
        "normalized_coupling_distances",
        "scalarized_ray_construction_residuals",
        "retained_beta_residuals",
        "coefficient_conditioning",
        "blocking_scheme_dispersion",
    }
    assert not result.trajectories["C001"][SCHEMES[0]].coefficients.flags.writeable
    with pytest.raises(TypeError):
        result.trajectories["new"] = {}


def test_replay_trajectory_array_backing_cannot_be_made_writeable(
    synthetic_extract: SyntheticExtract,
) -> None:
    module = _diagnostic_module()
    source = module.validate_scientific_extract(
        synthetic_extract.path,
        synthetic_extract.binding(),
    )

    result = module.replay_confirmatory_diagnostics(source)
    replayed = result.trajectories["C001"][SCHEMES[0]].coefficients

    assert not replayed.flags.writeable
    with pytest.raises(ValueError):
        replayed.setflags(write=True)


def test_stored_output_supplier_cannot_replace_frozen_production_iterator(
    synthetic_extract: SyntheticExtract,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _diagnostic_module()
    source = module.validate_scientific_extract(
        synthetic_extract.path,
        synthetic_extract.binding(),
    )
    supplier_calls: list[tuple[str, str]] = []
    production_calls: list[str] = []
    frozen_production = module.iterate_fixed_ray

    def production_spy(*args: object, **kwargs: object) -> FixedRayTrajectory:
        production_calls.append(str(kwargs["scheme"]))
        return frozen_production(*args, **kwargs)

    def stored_output_supplier(
        system: object,
        initial: object,
        *,
        scheme: str,
        steps: int,
    ) -> FixedRayTrajectory:
        del initial
        assert steps == 8
        job_index = len(supplier_calls) // 2
        job_id = JOB_IDS[job_index]
        supplier_calls.append((job_id, scheme))
        return _stored_output_trajectory(source, job_index, scheme, system)

    monkeypatch.setattr(module, "iterate_fixed_ray", production_spy)
    try:
        module.replay_confirmatory_diagnostics(
            source,
            iterate_fn=stored_output_supplier,
        )
    except ValueError as error:
        assert "frozen production iterator" in str(error)
    else:
        pytest.fail(
            "stored-output supplier was accepted after "
            f"{len(supplier_calls)} supplier calls and "
            f"{len(production_calls)} production calls"
        )

    assert supplier_calls == []
    assert production_calls == []


def test_call_observer_records_all_80_validated_production_invocations(
    synthetic_extract: SyntheticExtract,
) -> None:
    module = _diagnostic_module()
    source = module.validate_scientific_extract(
        synthetic_extract.path,
        synthetic_extract.binding(),
    )
    observed: list[tuple[str, str]] = []

    def observe(job_id: str, scheme: str) -> None:
        observed.append((job_id, scheme))

    result = module.replay_confirmatory_diagnostics(
        source,
        call_observer=observe,
    )

    assert observed == [(job_id, scheme) for job_id in JOB_IDS for scheme in SCHEMES]
    assert result.call_count == 80


def test_call_observer_cannot_supply_stored_replay_output(
    synthetic_extract: SyntheticExtract,
) -> None:
    module = _diagnostic_module()
    source = module.validate_scientific_extract(
        synthetic_extract.path,
        synthetic_extract.binding(),
    )
    system = build_preregistered_system()
    observed: list[tuple[str, str]] = []

    def stored_output_observer(job_id: str, scheme: str) -> FixedRayTrajectory:
        observed.append((job_id, scheme))
        return _stored_output_trajectory(
            source,
            JOB_IDS.index(job_id),
            scheme,
            system,
        )

    try:
        module.replay_confirmatory_diagnostics(
            source,
            call_observer=stored_output_observer,
        )
    except ValueError as error:
        assert "call_observer must not produce replay results" in str(error)
    else:
        pytest.fail(
            "stored-output observer return was accepted after "
            f"{len(observed)} observed production calls"
        )

    assert observed == [("C001", SCHEMES[0])]


def test_call_observer_cannot_replace_subsequent_production_invocations(
    synthetic_extract: SyntheticExtract,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _diagnostic_module()
    source = module.validate_scientific_extract(
        synthetic_extract.path,
        synthetic_extract.binding(),
    )
    observed: list[tuple[str, str]] = []
    replacement_calls: list[tuple[str, str]] = []

    def stored_output_replacement(
        system: object,
        initial: object,
        *,
        scheme: str,
        steps: int,
    ) -> FixedRayTrajectory:
        del initial
        assert steps == 8
        job_index = len(observed) // 2
        job_id = JOB_IDS[job_index]
        replacement_calls.append((job_id, scheme))
        return _stored_output_trajectory(source, job_index, scheme, system)

    def observe(job_id: str, scheme: str) -> None:
        observed.append((job_id, scheme))
        if len(observed) == 1:
            monkeypatch.setattr(
                module,
                "_FROZEN_PRODUCTION_ITERATOR",
                stored_output_replacement,
            )

    result = module.replay_confirmatory_diagnostics(
        source,
        call_observer=observe,
    )

    assert result.call_count == 80
    assert observed == [(job_id, scheme) for job_id in JOB_IDS for scheme in SCHEMES]
    assert replacement_calls == [], (
        f"observer replaced {len(replacement_calls)} frozen production invocations"
    )


def test_call_observer_runs_after_production_function_globals_are_no_longer_used(
    synthetic_extract: SyntheticExtract,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _diagnostic_module()
    source = module.validate_scientific_extract(
        synthetic_extract.path,
        synthetic_extract.binding(),
    )
    system = build_preregistered_system()
    observed: list[tuple[str, str]] = []
    replacement_calls: list[tuple[str, str]] = []
    production_globals = module._FROZEN_PRODUCTION_ITERATOR.__globals__

    def stored_output_factory(**fields: object) -> FixedRayTrajectory:
        scheme = str(fields["scheme"])
        job_index = len(observed) // 2
        job_id = JOB_IDS[job_index]
        replacement_calls.append((job_id, scheme))
        return _stored_output_trajectory(source, job_index, scheme, system)

    def observe(job_id: str, scheme: str) -> None:
        observed.append((job_id, scheme))
        if len(observed) == 1:
            monkeypatch.setitem(
                production_globals,
                "FixedRayTrajectory",
                stored_output_factory,
            )

    result = module.replay_confirmatory_diagnostics(
        source,
        call_observer=observe,
    )

    assert result.call_count == 80
    assert observed == [(job_id, scheme) for job_id in JOB_IDS for scheme in SCHEMES]
    assert replacement_calls == [], (
        "observer replaced "
        f"{len(replacement_calls)} results through production-function globals"
    )


def test_synthetic_replay_rejects_a_result_outside_the_frozen_cpu_tolerance(
    synthetic_extract: SyntheticExtract,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _diagnostic_module()
    source = module.validate_scientific_extract(
        synthetic_extract.path,
        synthetic_extract.binding(),
    )
    first = True

    def corrupting_iterator(
        system: object,
        initial: object,
        *,
        scheme: str,
        steps: int,
    ) -> FixedRayTrajectory:
        nonlocal first
        trajectory = iterate_fixed_ray(system, initial, scheme=scheme, steps=steps)
        if not first:
            return trajectory
        first = False
        coefficients = trajectory.coefficients.copy()
        coefficients[-1, 0] += 10.0 * module.CPU_REPLAY_ATOL
        return FixedRayTrajectory(
            scheme=trajectory.scheme,
            coefficients=coefficients,
            coupling_matrices=trajectory.coupling_matrices,
            projective_ray_angles=trajectory.projective_ray_angles,
            normalized_coupling_distances=trajectory.normalized_coupling_distances,
            scalarized_ray_construction_residuals=(
                trajectory.scalarized_ray_construction_residuals
            ),
            retained_beta_residual_vectors=trajectory.retained_beta_residual_vectors,
            retained_beta_residuals=trajectory.retained_beta_residuals,
            basin_exits=trajectory.basin_exits,
            coefficient_conditioning=trajectory.coefficient_conditioning,
            matrix_condition=trajectory.matrix_condition,
        )

    monkeypatch.setattr(module, "_FROZEN_PRODUCTION_ITERATOR", corrupting_iterator)
    with pytest.raises(ValueError, match="replay"):
        module.replay_confirmatory_diagnostics(
            source,
            iterate_fn=corrupting_iterator,
        )


def test_synthetic_replay_gives_production_an_immutable_regenerated_initial(
    synthetic_extract: SyntheticExtract,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _diagnostic_module()
    source = module.validate_scientific_extract(
        synthetic_extract.path,
        synthetic_extract.binding(),
    )
    calls: list[tuple[str, str]] = []

    def inspecting_iterator(
        system: object,
        initial: object,
        *,
        scheme: str,
        steps: int,
    ) -> FixedRayTrajectory:
        job_index = len(calls) // 2
        job_id = JOB_IDS[job_index]
        expected = generate_initial_coefficients(
            int(source.jobs[job_index]["master_seed"]),
            job_id,
        )
        received = np.asarray(initial)
        assert np.array_equal(received, expected)
        with pytest.raises(ValueError):
            received.setflags(write=True)
        calls.append((job_id, scheme))
        return iterate_fixed_ray(system, received, scheme=scheme, steps=steps)

    monkeypatch.setattr(module, "_FROZEN_PRODUCTION_ITERATOR", inspecting_iterator)
    result = module.replay_confirmatory_diagnostics(
        source,
        iterate_fn=inspecting_iterator,
    )

    assert result.call_count == 80
    assert calls == [(job_id, scheme) for job_id in JOB_IDS for scheme in SCHEMES]


def test_tracked_extract_validates_all_owned_files_and_recorded_metadata() -> None:
    module = _diagnostic_module()
    source = module.validate_scientific_extract(TRACKED_EXTRACT, _tracked_binding())

    assert source.scientific_revision == ("fcb2c49efdca2ad3ee502dc08fbb82fc285e7a05")
    assert source.diagnostic_revision == _head_revision()
    assert source.scientific_revision != source.diagnostic_revision
    assert tuple(source.binding.complete_original_inventory) == (
        ORIGINAL_INVENTORY_NAMES
    )
    assert source.binding.tracked_scientific_subset == TRACKED_SCIENTIFIC_SUBSET
    assert source.job_ids == JOB_IDS
    assert source.schemes == SCHEMES
    assert len(source.arrays) == 120
    assert all(
        source.arrays[f"{job_id}_{scheme}_coefficients"].shape == (9, 6)
        for job_id in JOB_IDS
        for scheme in SCHEMES
    )
    assert source.recorded_execution_metadata["recorded_worker_exchange_count"] == 640
    assert source.recorded_execution_metadata["recorded_retried_job_count"] == 0
    assert (
        source.recorded_execution_metadata["omitted_execution_logs_revalidated"]
        is False
    )


def test_tracked_extract_deterministically_replays_all_80_trajectories() -> None:
    module = _diagnostic_module()
    source = module.validate_scientific_extract(TRACKED_EXTRACT, _tracked_binding())
    calls: list[tuple[str, str]] = []

    def observe(job_id: str, scheme: str) -> None:
        calls.append((job_id, scheme))

    result = module.replay_confirmatory_diagnostics(
        source,
        call_observer=observe,
    )

    assert calls == [(job_id, scheme) for job_id in JOB_IDS for scheme in SCHEMES]
    assert result.call_count == 80
    assert max(result.max_absolute_errors.values()) <= module.CPU_REPLAY_ATOL
    assert (
        result.recorded_execution_metadata["omitted_execution_logs_revalidated"]
        is False
    )
