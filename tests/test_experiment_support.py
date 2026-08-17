from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np
import pytest

import multiagent_elbo.experiment_support as experiment_support
from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.experiment_support import (
    lower_bounded_metric,
    readonly_array,
    target_metric,
)
from multiagent_elbo.finite.agent_network_experiment import (
    run_agent_network_experiment,
)
from multiagent_elbo.finite.attention_experiment import run_attention_experiment
from multiagent_elbo.finite.categorical_falsification_experiment import (
    run_categorical_falsification_experiment,
)
from multiagent_elbo.finite.categorical_dqm_experiment import (
    run_categorical_dqm_experiment,
)
from multiagent_elbo.finite.counterexample_experiment import (
    run_finite_counterexample_experiment,
)
from multiagent_elbo.finite.information_history_experiment import (
    run_information_history_experiment,
)
from multiagent_elbo.finite.scale_cocycle_experiment import (
    run_scale_cocycle_experiment,
)
from multiagent_elbo.finite.theory_oracle_experiment import (
    run_theory_oracle_experiment,
)
from multiagent_elbo.geometry.holonomy_experiment import run_holonomy_experiment
from multiagent_elbo.realizations.gaussian.fixed_ray_experiment import (
    run_gaussian_fixed_ray_experiment,
)
from multiagent_elbo.rendering import validated_renderer_status


_NUMERICS = {
    "dtype": "float64",
    "atol": 1.0e-12,
    "rtol": 1.0e-10,
    "min_spd_rcond": 1.0e-12,
    "max_frame_condition": 1.0e6,
}
_CPU_COMPUTE = {
    "backend": "cpu",
    "dtype": "float64",
    "device_index": 0,
    "batch_size": 3,
    "deterministic": True,
    "allow_tf32": False,
    "cpu_cuda_parity": True,
    "cuda_worker_python": str(Path(sys.executable).resolve()),
    "heavy_sweep_enabled": False,
}


def _lab_config(
    root: Path,
    theory: dict[str, object],
    *,
    diagnostics: bool = False,
    compute: dict[str, object] | None = None,
) -> ExperimentConfig:
    arguments: list[dict[str, object]] = [
        {"name": f"candidate state {theory['experiment']}", "seed": 20260809},
        theory,
        dict(_NUMERICS),
        {
            "root": str(root),
            "collect_diagnostics": diagnostics,
            "render_figures": False,
        },
    ]
    if compute is not None:
        arguments.append(compute)
    return ExperimentConfig.from_dicts(*arguments)


def _network_config(root: Path) -> ExperimentConfig:
    return _lab_config(
        root,
        {
            "experiment": "multiagent_network",
            "fixture": "two_scale_application_v1",
            "scenario": "aligned",
            "arithmetic": "exact_rational",
        },
        diagnostics=True,
    )


def _attention_config(root: Path) -> ExperimentConfig:
    return _lab_config(
        root,
        {"experiment": "attention_marked_event", "fixture": "nested_nonuniform_v1"},
    )


def _categorical_dqm_config(root: Path) -> ExperimentConfig:
    return _lab_config(
        root,
        {
            "experiment": "categorical_dqm",
            "fixture": "three_category_softmax_v1",
            "theta": (0.6931471805599453, 1.0986122886681098),
            "finite_difference_step": 1.0e-5,
            "dqm_step_sizes": (0.1, 0.05, 0.025, 0.0125),
        },
    )


def _counterexample_config(root: Path) -> ExperimentConfig:
    return _lab_config(
        root,
        {
            "experiment": "finite_counterexample",
            "fixture": "counterexample_catalog_v1",
            "max_states": 4,
            "max_denominator": 8,
            "arithmetic": "exact_rational",
        },
    )


def _information_history_config(root: Path) -> ExperimentConfig:
    return _lab_config(
        root,
        {
            "experiment": "information_history",
            "fixture": "two_scale_application_v1",
            "family": "categorical_softmax",
            "history_steps": 16,
            "step_size": 0.05,
        },
        diagnostics=True,
    )


def _scale_cocycle_config(root: Path) -> ExperimentConfig:
    return _lab_config(
        root,
        {
            "experiment": "scale_cocycle",
            "fixture": "two_scale_application_v1",
            "extension": "three_level_composition_v1",
            "retained_interaction_order": 2,
            "arithmetic": "exact_rational",
        },
        diagnostics=True,
    )


def _theory_oracle_config(root: Path) -> ExperimentConfig:
    return _lab_config(
        root,
        {
            "experiment": "theory_oracle",
            "fixture": "two_scale_application_v1",
            "oracle_set": "core_identities",
            "arithmetic": "exact_rational",
        },
        diagnostics=True,
        compute={**_CPU_COMPUTE, "batch_size": 4096},
    )


def _holonomy_config(root: Path) -> ExperimentConfig:
    return _lab_config(
        root,
        {
            "experiment": "gauge_holonomy",
            "fixture": "two_scale_application_v1",
            "scenario": "nonflat_plaquette",
            "group": "GL+(2)",
        },
    )


def _gaussian_fixed_ray_config(root: Path) -> ExperimentConfig:
    return _lab_config(
        root,
        {
            "experiment": "gaussian_fixed_ray",
            "fixture": "gaussian_fixed_ray_v1",
            "preregistration": "2026-08-09-gaussian-fixed-ray-v1",
            "blocking_schemes": ("adjacent_pairs", "balanced_alternating"),
            "matrix_dimension": 2,
        },
        diagnostics=True,
        compute=dict(_CPU_COMPUTE),
    )


def _categorical_falsification_config(root: Path) -> ExperimentConfig:
    return _lab_config(
        root,
        {
            "experiment": "categorical_falsification",
            "fixture": "two_channel_z3_v1",
            "admitted_family": "both",
            "null_control_seeds": 2,
            "descent_restarts": 4,
            "arithmetic": "exact_rational",
        },
    )


ALL_LAB_RUNNERS = (
    (run_agent_network_experiment, _network_config),
    (run_categorical_falsification_experiment, _categorical_falsification_config),
    (run_attention_experiment, _attention_config),
    (run_categorical_dqm_experiment, _categorical_dqm_config),
    (run_finite_counterexample_experiment, _counterexample_config),
    (run_information_history_experiment, _information_history_config),
    (run_scale_cocycle_experiment, _scale_cocycle_config),
    (run_theory_oracle_experiment, _theory_oracle_config),
    (run_holonomy_experiment, _holonomy_config),
    (run_gaussian_fixed_ray_experiment, _gaussian_fixed_ray_config),
)
_EXPECTED_INCONCLUSIVE_METRICS = {
    run_categorical_falsification_experiment: {
        "CFL-12_partition_residence_ratio",
        "CFL-13_exit_time_fit_r_squared",
        "CFL-15_deterministic_control_collapse",
        "CFL-16_null_control_separation",
    },
    run_information_history_experiment: {"semiconjugacy_defect_norm"},
    run_gaussian_fixed_ray_experiment: {"cpu_cuda_parity_residual"},
}


def test_target_and_lower_bound_metrics_keep_established_json_schema():
    exact = target_metric(
        1.0e-13,
        1.0e-10,
        target=0.0,
        interpretation="identity",
        theorem_status="established_conditional_identity",
    )
    control = lower_bounded_metric(
        0.2,
        1.0e-10,
        lower_bound=0.1,
        interpretation="negative control",
        theorem_status="negative_control",
    )

    assert asdict(exact).keys() == {
        "value", "tolerance", "status", "interpretation",
        "assessment_scope", "theorem_status", "verification_state",
        "claim_origin",
    }
    assert exact.status == "pass"
    assert control.status == "pass"
    assert exact.verification_state == "CANDIDATE"
    assert exact.claim_origin == "PROJECT_NOVEL"


@pytest.mark.parametrize(
    ("runner", "config_factory"),
    ALL_LAB_RUNNERS,
    ids=[runner.__name__ for runner, _ in ALL_LAB_RUNNERS],
)
def test_laboratory_producers_do_not_self_promote(
    runner, config_factory, tmp_path: Path
):
    result = runner(config_factory(tmp_path))
    expected_inconclusive = _EXPECTED_INCONCLUSIVE_METRICS.get(runner, set())

    assert {
        metric.verification_state for metric in result.metrics.values()
    } <= {"CANDIDATE", "INCONCLUSIVE"}
    assert {
        name
        for name, metric in result.metrics.items()
        if metric.verification_state == "INCONCLUSIVE"
    } == expected_inconclusive
    assert all(
        metric.verification_state == "CANDIDATE"
        for name, metric in result.metrics.items()
        if name not in expected_inconclusive
    )


def test_readonly_array_makes_a_c_contiguous_float64_copy():
    source = np.array([[1, 2], [3, 4]], dtype=np.int64, order="F")

    result = readonly_array(source)

    assert result.dtype == np.float64
    assert result.flags.c_contiguous
    assert not result.flags.writeable
    source[0, 0] = 99
    assert result[0, 0] == 1.0
    with pytest.raises(ValueError):
        result[0, 0] = 0.0


def _renderer_manifest(
    run_dir: Path,
    output_dir: Path,
    requested: tuple[str, ...],
    *,
    status: str = "complete",
) -> SimpleNamespace:
    output_dir.mkdir(parents=True, exist_ok=True)
    figures: list[dict[str, str]] = []
    message: str | None = None
    if status == "complete":
        for name in requested:
            png = output_dir / f"{name}.png"
            pdf = output_dir / f"{name}.pdf"
            png.write_bytes(b"\x89PNG\r\n\x1a\nfixture")
            pdf.write_bytes(b"%PDF-1.7\nfixture")
            figures.append(
                {
                    "name": name,
                    "png": png.name,
                    "png_sha256": hashlib.sha256(png.read_bytes()).hexdigest(),
                    "pdf": pdf.name,
                    "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
                }
            )
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
    return SimpleNamespace(
        status=status,
        run_dir=run_dir,
        output_dir=output_dir,
        requested=requested,
        manifest_path=manifest_path,
    )


def test_validated_renderer_status_accepts_backed_complete_and_failed_manifests(
    tmp_path: Path,
):
    run_dir = tmp_path / "run"
    output_dir = tmp_path / "figures"
    requested = ("first", "second")
    run_dir.mkdir()

    complete = _renderer_manifest(run_dir, output_dir, requested)
    assert validated_renderer_status(complete, run_dir, output_dir, requested) == "complete"

    failed = _renderer_manifest(run_dir, output_dir, requested, status="failed")
    assert validated_renderer_status(failed, run_dir, output_dir, requested) == "failed"


@pytest.mark.parametrize(
    "forge",
    [
        "wrong_run_directory",
        "wrong_request_ordering",
        "uncontained_manifest_path",
        "wrong_image_sha256",
        "missing_image",
        "empty_failure_message",
        "status_only_object",
    ],
)
def test_validated_renderer_status_rejects_unbacked_renderer_output(
    tmp_path: Path, forge: str
):
    run_dir = tmp_path / "run"
    output_dir = tmp_path / "figures"
    requested = ("first", "second")
    run_dir.mkdir()
    manifest = _renderer_manifest(run_dir, output_dir, requested)

    if forge == "wrong_run_directory":
        manifest.run_dir = tmp_path / "other-run"
    elif forge == "wrong_request_ordering":
        manifest.requested = tuple(reversed(requested))
    elif forge == "uncontained_manifest_path":
        outside = tmp_path / "outside.json"
        outside.write_text(manifest.manifest_path.read_text("utf-8"), encoding="utf-8")
        manifest.manifest_path = outside
    elif forge == "wrong_image_sha256":
        payload = json.loads(manifest.manifest_path.read_text("utf-8"))
        payload["figures"][0]["png_sha256"] = "0" * 64
        manifest.manifest_path.write_text(json.dumps(payload), encoding="utf-8")
    elif forge == "missing_image":
        (output_dir / "first.png").unlink()
    elif forge == "empty_failure_message":
        manifest = _renderer_manifest(run_dir, output_dir, requested, status="failed")
        payload = json.loads(manifest.manifest_path.read_text("utf-8"))
        payload["message"] = ""
        manifest.manifest_path.write_text(json.dumps(payload), encoding="utf-8")
    else:
        manifest = SimpleNamespace(status="complete")

    with pytest.raises(ValueError, match="unbacked|invalid status"):
        validated_renderer_status(manifest, run_dir, output_dir, requested)


def test_validated_renderer_status_controls_an_unhashable_unsupported_status(
    tmp_path: Path,
):
    manifest = SimpleNamespace(status=[])

    with pytest.raises(ValueError, match="invalid status"):
        validated_renderer_status(manifest, tmp_path, tmp_path, ())


def test_validated_renderer_status_rejects_a_publication_symlink_escape(
    tmp_path: Path,
):
    run_dir = tmp_path / "run"
    output_dir = tmp_path / "figures"
    requested = ("first",)
    run_dir.mkdir()
    manifest = _renderer_manifest(run_dir, output_dir, requested)
    outside = tmp_path / "outside.png"
    outside.write_bytes(b"\x89PNG\r\n\x1a\noutside fixture")
    publication = output_dir / "first.png"
    publication.unlink()
    try:
        publication.symlink_to(outside)
    except (NotImplementedError, OSError):
        pytest.skip("capability unavailable: symbolic_link")
    payload = json.loads(manifest.manifest_path.read_text("utf-8"))
    payload["figures"][0]["png_sha256"] = hashlib.sha256(
        outside.read_bytes()
    ).hexdigest()
    manifest.manifest_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="unbacked"):
        validated_renderer_status(manifest, run_dir, output_dir, requested)


def test_canonical_metric_fields_are_explicit_and_orthogonal():
    passing_open = target_metric(
        0.0,
        1.0e-12,
        target=0.0,
        interpretation="finite diagnostic only",
        theorem_status="OPEN",
        verification_state="INCONCLUSIVE",
        claim_origin="PROJECT_NOVEL",
    )
    failing_established = target_metric(
        1.0,
        1.0e-12,
        target=0.0,
        interpretation="implementation mutation",
        theorem_status="ESTABLISHED",
        verification_state="EVIDENCE_VERIFIED",
        claim_origin="STANDARD",
    )

    assert passing_open.status == "pass"
    assert passing_open.theorem_status == "OPEN"
    assert passing_open.verification_state == "INCONCLUSIVE"
    assert failing_established.status == "fail"
    assert failing_established.theorem_status == "ESTABLISHED"
    assert failing_established.verification_state == "EVIDENCE_VERIFIED"


def test_canonical_metric_metadata_cannot_be_omitted_or_misspelled():
    with pytest.raises(ValueError, match="canonical metrics require explicit"):
        target_metric(
            0.0,
            1.0e-12,
            target=0.0,
            interpretation="missing metadata",
            theorem_status="NUMERICAL",
        )

    with pytest.raises(ValueError, match="invalid verification_state"):
        target_metric(
            0.0,
            1.0e-12,
            target=0.0,
            interpretation="bad metadata",
            theorem_status="NUMERICAL",
            verification_state="verified",  # type: ignore[arg-type]
            claim_origin="APPLICATION_SPECIFIC",
        )


@pytest.mark.parametrize(
    ("verification_state", "claim_origin", "message"),
    [
        ("", "APPLICATION_SPECIFIC", "invalid verification_state"),
        ("CANDIDATE", "", "invalid claim_origin"),
    ],
)
def test_supplied_empty_canonical_metric_metadata_is_invalid(
    verification_state: str, claim_origin: str, message: str
):
    with pytest.raises(ValueError, match=message):
        target_metric(
            0.0,
            1.0e-12,
            target=0.0,
            interpretation="explicit empty metadata is not legacy omission",
            theorem_status="NUMERICAL",
            verification_state=verification_state,  # type: ignore[arg-type]
            claim_origin=claim_origin,  # type: ignore[arg-type]
        )


def test_experiment_registry_is_complete_typed_and_immutable():
    registry = experiment_support.EXPERIMENT_REGISTRY

    assert tuple(registry) == (
        "multiagent_network",
        "theory_oracle",
        "finite_counterexample",
        "information_history",
        "gauge_holonomy",
        "scale_cocycle",
        "gaussian_fixed_ray",
    )
    for name, contract in registry.items():
        assert contract.experiment == name
        assert contract.launcher.startswith("run_")
        assert contract.launcher.endswith("_lab.py")
        assert contract.config_keys[0] == "experiment"
        assert contract.artifact_inventory
        assert contract.metric_inventory
        assert contract.lane_owner.startswith("session_")
    with pytest.raises(TypeError):
        registry["other"] = registry["multiagent_network"]  # type: ignore[index]
    with pytest.raises(AttributeError):
        registry["multiagent_network"].launcher = "changed.py"  # type: ignore[misc]


def _valid_worker_manifest(
    message_type: str,
    *,
    request_manifest: dict[str, object] | None = None,
) -> dict[str, object]:
    response = message_type == "response"
    manifest: dict[str, object] = {
        "schema_version": "cuda-worker-protocol-v1",
        "message_type": message_type,
        "job_id": "job-0001",
        "requested_backend": "cuda",
        "requested_dtype": "float64",
        "effective_backend": "cuda" if response else None,
        "effective_dtype": "float64" if response else None,
        "environment_sha256": "1" * 64,
        "npz_sha256": "2" * 64,
        "arrays": [
            {
                "name": "couplings",
                "shape": [2, 3],
                "dtype": "float64",
                "sha256": "3" * 64,
            }
        ],
        "output_identity": None,
    }
    if response:
        if request_manifest is None:
            request_manifest = _valid_worker_manifest("request")
        manifest["output_identity"] = experiment_support.worker_output_identity(
            manifest, request_manifest=request_manifest
        )
    return manifest


def test_worker_protocol_validates_request_and_self_hashed_response():
    request = _valid_worker_manifest("request")
    response = _valid_worker_manifest("response", request_manifest=request)

    validated_request = experiment_support.validate_worker_protocol_manifest(
        request, expected_message_type="request"
    )
    validated_response = experiment_support.validate_worker_protocol_manifest(
        response,
        expected_message_type="response",
        request_manifest=request,
    )

    assert validated_request.message_type == "request"
    assert validated_request.arrays[0].shape == (2, 3)
    assert validated_response.output_identity == response["output_identity"]


def test_worker_output_identity_has_a_pinned_request_response_byte_domain():
    request = _valid_worker_manifest("request")
    response = _valid_worker_manifest("response", request_manifest=request)

    assert response["output_identity"] == (
        "b6ca8c4d7c65218e109c01471f03f45b456554031c01a60de39cd0beab4b5a29"
    )


def test_worker_protocol_rejects_a_self_hashed_response_without_its_request():
    request = _valid_worker_manifest("request")
    response = _valid_worker_manifest("response", request_manifest=request)

    with pytest.raises(ValueError, match="original request"):
        experiment_support.validate_worker_protocol_manifest(
            response, expected_message_type="response"
        )


@pytest.mark.parametrize(
    ("request_mutation", "response_mutation", "message"),
    [
        ({"job_id": "job-forged"}, {"job_id": "job-forged"}, "job_id"),
        (
            {"requested_backend": "cpu"},
            {"requested_backend": "cpu", "effective_backend": "cpu"},
            "requested_backend",
        ),
        (
            {"requested_dtype": "float32"},
            {"requested_dtype": "float32", "effective_dtype": "float32"},
            "requested_dtype",
        ),
        (
            {"environment_sha256": "4" * 64},
            {"environment_sha256": "4" * 64},
            "environment_sha256",
        ),
        ({"npz_sha256": "5" * 64}, {}, "output_identity"),
        (
            {
                "arrays": [
                    {
                        "name": "couplings",
                        "shape": [2, 3],
                        "dtype": "float64",
                        "sha256": "6" * 64,
                    }
                ]
            },
            {},
            "output_identity",
        ),
    ],
)
def test_worker_protocol_binds_response_to_original_request(
    request_mutation: dict[str, object],
    response_mutation: dict[str, object],
    message: str,
):
    original_request = _valid_worker_manifest("request")
    forged_request = json.loads(json.dumps(original_request))
    forged_request.update(request_mutation)
    response = _valid_worker_manifest("response", request_manifest=forged_request)
    response.update(response_mutation)
    response["output_identity"] = experiment_support.worker_output_identity(
        response, request_manifest=forged_request
    )

    with pytest.raises(ValueError, match=message):
        experiment_support.validate_worker_protocol_manifest(
            response,
            expected_message_type="response",
            request_manifest=original_request,
        )


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ({"schema_version": "v2"}, "schema_version"),
        ({"job_id": "../escape"}, "job_id"),
        ({"requested_dtype": "float16"}, "requested_dtype"),
        ({"effective_backend": "cpu"}, "effective backend"),
        ({"environment_sha256": "bad"}, "environment_sha256"),
        ({"npz_sha256": "bad"}, "npz_sha256"),
        ({"arrays": []}, "arrays must not be empty"),
        ({"output_identity": "0" * 64}, "output_identity"),
    ],
)
def test_worker_protocol_rejects_malformed_or_mismatched_response(
    mutation: dict[str, object], message: str
):
    request = _valid_worker_manifest("request")
    manifest = _valid_worker_manifest("response", request_manifest=request)
    manifest.update(mutation)

    with pytest.raises(ValueError, match=message):
        experiment_support.validate_worker_protocol_manifest(
            manifest,
            expected_message_type="response",
            request_manifest=request,
        )


def test_worker_protocol_rejects_bad_shape_dtype_and_array_hash():
    for key, value, message in (
        ("shape", [2, -1], "shape"),
        ("dtype", "float16", "dtype"),
        ("sha256", "bad", "sha256"),
    ):
        request = _valid_worker_manifest("request")
        manifest = _valid_worker_manifest("response", request_manifest=request)
        manifest["arrays"][0][key] = value  # type: ignore[index]
        manifest["output_identity"] = experiment_support.worker_output_identity(
            manifest, request_manifest=request
        )
        with pytest.raises(ValueError, match=message):
            experiment_support.validate_worker_protocol_manifest(
                manifest,
                expected_message_type="response",
                request_manifest=request,
            )


def test_two_scale_literal_fixture_has_valid_digest_and_typed_sections():
    fixture_path = Path(__file__).parent / "fixtures" / "two_scale_application_v1.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))

    application_id = experiment_support.validate_two_scale_application_fixture(
        payload
    )

    assert payload["application_id"] == (
        "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"
    )
    assert application_id == (
        "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"
    )
    assert payload["state_spaces"]["fine"]["labels"] == [
        f"{value:04b}" for value in range(16)
    ]
    assert payload["state_spaces"]["coarse"]["labels"] == [
        "00", "01", "10", "11"
    ]
    assert payload["organization"]["blocks"] == [
        {"block_id": "B01", "agents": ["0", "1"]},
        {"block_id": "B23", "agents": ["2", "3"]},
    ]
    assert len(payload["channel"]["arrows"]) == 1
    assert "three_level" not in json.dumps(payload)


def test_fixture_validation_rejects_digest_numeric_literal_and_bad_channel():
    fixture_path = Path(__file__).parent / "fixtures" / "two_scale_application_v1.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))

    bad_digest = json.loads(json.dumps(payload))
    bad_digest["application_id"] = "0" * 64
    with pytest.raises(ValueError, match="application_id"):
        experiment_support.validate_two_scale_application_fixture(bad_digest)

    numeric_literal = json.loads(json.dumps(payload))
    numeric_literal["reference_laws"]["fine"]["values"][0] = 0.0625
    numeric_literal["application_id"] = experiment_support.fixture_application_id(
        numeric_literal
    )
    with pytest.raises(ValueError, match="rational string"):
        experiment_support.validate_two_scale_application_fixture(numeric_literal)

    bad_channel = json.loads(json.dumps(payload))
    bad_channel["channel"]["arrows"][0]["rows"][0][0] = "1/2"
    bad_channel["application_id"] = experiment_support.fixture_application_id(
        bad_channel
    )
    with pytest.raises(ValueError, match="normalized"):
        experiment_support.validate_two_scale_application_fixture(bad_channel)


def test_fixture_validation_rejects_a_self_consistent_nonfrozen_application():
    fixture_path = Path(__file__).parent / "fixtures" / "two_scale_application_v1.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    rows = payload["channel"]["arrows"][0]["rows"]
    rows[0], rows[1] = rows[1], rows[0]
    payload["application_id"] = experiment_support.fixture_application_id(payload)

    with pytest.raises(ValueError, match="frozen application_id"):
        experiment_support.validate_two_scale_application_fixture(payload)
