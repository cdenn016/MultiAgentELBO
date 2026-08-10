from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess

import numpy as np
import pytest

import multiagent_elbo.cuda_backend as cuda_backend_module
from multiagent_elbo.cuda_backend import (
    WorkerBackendError,
    canonical_array_sha256,
    parity_diagnostics,
    run_worker_job,
    validate_worker_provenance,
    validate_worker_result,
)
from multiagent_elbo.experiment_support import (
    validate_worker_protocol_manifest,
    worker_output_identity,
)


REPOSITORY = Path(__file__).resolve().parents[1]
WORKER = REPOSITORY / "tools" / "cuda_worker.py"
ENVIRONMENT_LOCK = REPOSITORY / "environments" / "cuda-rtx5090-cu128.lock.txt"
ANACONDA = Path(r"C:\anaconda\python.exe")
CPU_PYTHON = Path(r"C:\Python314\python.exe")


def literal_inputs(*, rows: int = 5, batch_size: int = 4):
    coefficients_base = np.arange(rows * 12, dtype=np.float64).reshape(rows, 12)
    coefficients = coefficients_base[:, ::2]
    spatial_map = np.array(
        [
            [0.50, 0.10, 0.10, 0.10, 0.10, 0.10],
            [0.05, 0.55, 0.10, 0.10, 0.10, 0.10],
            [0.05, 0.05, 0.60, 0.10, 0.10, 0.10],
            [0.05, 0.05, 0.05, 0.65, 0.10, 0.10],
            [0.05, 0.05, 0.05, 0.05, 0.70, 0.10],
            [0.05, 0.05, 0.05, 0.05, 0.05, 0.75],
        ],
        dtype=np.float64,
    )
    matrix_direction = np.array([[1.0e-10, 0.0], [0.0, 1.0]], dtype=np.float64)
    return {
        "coefficients": coefficients,
        "spatial_map": spatial_map,
        "matrix_direction": matrix_direction,
        "batch_size": np.array(batch_size, dtype=np.int64),
    }


def test_array_digest_matches_frozen_literal_and_normalizes_noncontiguous_input():
    literal = np.array([1.0, -0.0], dtype=np.float64)
    assert canonical_array_sha256("coefficients", literal, "float64") == (
        "a77ebe68740919a943646783e8316167a40769a6d2d5023d97bde4dccd083664"
    )

    noncontiguous = np.arange(24.0).reshape(2, 12)[:, ::2]
    contiguous = np.ascontiguousarray(noncontiguous)
    assert not noncontiguous.flags.c_contiguous
    assert canonical_array_sha256("coefficients", noncontiguous, "float64") == canonical_array_sha256(
        "coefficients", contiguous, "float64"
    )


def test_array_digest_and_environment_lock_fail_closed_edges(tmp_path: Path):
    with pytest.raises(ValueError, match="invalid array name"):
        canonical_array_sha256("invalid array name", np.ones(1), "float64")
    with pytest.raises(ValueError, match="unsupported worker dtype"):
        canonical_array_sha256("coefficients", np.ones(1), "complex64")
    with pytest.raises(ValueError, match="uint16 bit patterns"):
        canonical_array_sha256("coefficients", np.ones(1), "bfloat16")
    assert canonical_array_sha256(
        "coefficients", np.array([0x3F80], dtype=np.uint16), "bfloat16"
    )
    assert canonical_array_sha256(
        "coefficients", np.array([True, False]), "bool"
    )
    with pytest.raises(ValueError, match="unsupported array dtype"):
        cuda_backend_module._dtype_name(np.array([1], dtype=np.uint16))
    with pytest.raises(WorkerBackendError, match="does not exist"):
        cuda_backend_module._parse_environment_lock(tmp_path / "missing.lock")
    incomplete = tmp_path / "incomplete.lock"
    incomplete.write_text("python_executable_sha256=0\n", encoding="utf-8")
    with pytest.raises(WorkerBackendError, match="missing required records"):
        cuda_backend_module._parse_environment_lock(incomplete)


def test_worker_cpu_roundtrip_validates_binding_remainder_batch_and_provenance(
    tmp_path: Path,
):
    inputs = literal_inputs(rows=5, batch_size=4)
    result = run_worker_job(
        worker_python=ANACONDA,
        worker_script=WORKER,
        work_root=tmp_path / "job",
        job_id="fixed-ray.cpu.remainder",
        requested_backend="cpu",
        requested_dtype="float64",
        arrays=inputs,
        environment_lock=ENVIRONMENT_LOCK,
    )

    request = validate_worker_protocol_manifest(
        result.request_manifest, expected_message_type="request"
    )
    response = validate_worker_protocol_manifest(
        result.response_manifest,
        expected_message_type="response",
        request_manifest=result.request_manifest,
    )
    expected = inputs["coefficients"] @ inputs["spatial_map"].T
    np.testing.assert_allclose(
        result.arrays["updated_coefficients"], expected, rtol=1e-15, atol=1e-15
    )
    assert result.arrays["matrix_condition"].item() == pytest.approx(1.0e10)
    assert request.job_id == response.job_id == "fixed-ray.cpu.remainder"
    assert response.effective_backend == "cpu"
    assert response.effective_dtype == "float64"
    assert result.provenance["environment_sha256"] == request.environment_sha256
    assert result.provenance["worker_executable"] == str(ANACONDA.resolve())
    assert result.provenance["worker_executable_sha256"] == hashlib.sha256(
        ANACONDA.read_bytes()
    ).hexdigest()
    assert result.provenance["schema_version"] == "cuda-worker-provenance-v1"
    assert result.provenance["kernel_strategy"] == "rowwise_spatial_map_matvec"
    assert result.provenance["batch_size"] == 4
    assert result.provenance["requested_backend"] == "cpu"
    assert result.provenance["effective_backend"] == "cpu"
    assert result.provenance["requested_dtype"] == "float64"
    assert result.provenance["effective_dtype"] == "float64"
    assert result.provenance["driver_version"] is None
    assert result.provenance["cublas_library_version"] is None
    assert result.provenance["environment_lock_consistent"] is True
    assert result.provenance["runtime_seconds"] >= 0.0
    assert result.provenance["retry_lineage"] == {
        "attempt": 1,
        "parent_job_id": None,
    }
    validate_worker_provenance(
        result.provenance,
        requested_backend="cpu",
        requested_dtype="float64",
        environment_sha256=request.environment_sha256,
        batch_size=4,
    )

    missing_driver = dict(result.provenance)
    del missing_driver["driver_version"]
    with pytest.raises(WorkerBackendError, match="provenance schema"):
        validate_worker_provenance(
            missing_driver,
            requested_backend="cpu",
            requested_dtype="float64",
            environment_sha256=request.environment_sha256,
            batch_size=4,
        )

    drifted_lock = dict(result.provenance)
    drifted_lock["environment_sha256"] = "0" * 64
    with pytest.raises(WorkerBackendError, match="environment lock"):
        validate_worker_provenance(
            drifted_lock,
            requested_backend="cpu",
            requested_dtype="float64",
            environment_sha256=request.environment_sha256,
            batch_size=4,
        )


def test_worker_cpu_handles_zero_support_and_batch_schedule_invariance(tmp_path: Path):
    zero = run_worker_job(
        worker_python=ANACONDA,
        worker_script=WORKER,
        work_root=tmp_path / "zero",
        job_id="fixed-ray.cpu.zero",
        requested_backend="cpu",
        requested_dtype="float64",
        arrays=literal_inputs(rows=0, batch_size=3),
        environment_lock=ENVIRONMENT_LOCK,
    )
    first = run_worker_job(
        worker_python=ANACONDA,
        worker_script=WORKER,
        work_root=tmp_path / "batch-2",
        job_id="fixed-ray.cpu.batch2",
        requested_backend="cpu",
        requested_dtype="float64",
        arrays=literal_inputs(rows=7, batch_size=2),
        environment_lock=ENVIRONMENT_LOCK,
    )
    second = run_worker_job(
        worker_python=ANACONDA,
        worker_script=WORKER,
        work_root=tmp_path / "batch-5",
        job_id="fixed-ray.cpu.batch5",
        requested_backend="cpu",
        requested_dtype="float64",
        arrays=literal_inputs(rows=7, batch_size=5),
        environment_lock=ENVIRONMENT_LOCK,
    )

    assert zero.arrays["updated_coefficients"].shape == (0, 6)
    np.testing.assert_array_equal(
        first.arrays["updated_coefficients"], second.arrays["updated_coefficients"]
    )


@pytest.mark.parametrize(
    ("case", "mutate", "message"),
    (
        ("negative-coefficient", lambda arrays: arrays["coefficients"].__setitem__((0, 0), -1.0), "nonnegative"),
        ("negative-spatial-map", lambda arrays: arrays["spatial_map"].__setitem__((0, 0), -0.5), "nonnegative"),
        ("nonnormalized-spatial-map", lambda arrays: arrays["spatial_map"].__setitem__((0, 0), 0.6), "row-stochastic"),
        ("nan-coefficient", lambda arrays: arrays["coefficients"].__setitem__((0, 0), np.nan), "finite"),
        ("inf-spatial-map", lambda arrays: arrays["spatial_map"].__setitem__((0, 0), np.inf), "finite"),
    ),
)
def test_controller_rejects_invalid_probability_payload_before_artifacts(
    tmp_path: Path, case: str, mutate: object, message: str
):
    inputs = {name: np.array(value, copy=True) for name, value in literal_inputs().items()}
    mutate(inputs)
    output = tmp_path / case
    with pytest.raises(WorkerBackendError, match=message):
        run_worker_job(
            worker_python=ANACONDA,
            worker_script=WORKER,
            work_root=output,
            job_id=f"fixed-ray.cpu.{case}",
            requested_backend="cpu",
            requested_dtype="float64",
            arrays=inputs,
            environment_lock=ENVIRONMENT_LOCK,
        )
    assert not output.exists()


@pytest.mark.parametrize(
    ("case", "message"),
    (
        ("job-id", "invalid immutable job ID"),
        ("backend", "requested backend"),
        ("dtype", "requested dtype"),
        ("inventory", "input arrays"),
        ("bfloat16", "bfloat16"),
        ("scientific-dtype", "scientific input dtypes"),
        ("coefficient-shape", "invalid shapes"),
        ("spatial-shape", "invalid shapes"),
        ("width", "coefficient width"),
        ("matrix-shape", "matrix_direction must be square"),
        ("batch-dtype", "batch_size"),
        ("batch-zero", "batch_size"),
        ("matrix-symmetry", "exactly symmetric"),
        ("matrix-positive", "positive definite"),
    ),
)
def test_controller_rejects_malformed_fixed_ray_contract_before_artifacts(
    tmp_path: Path, case: str, message: str
):
    inputs = {name: np.array(value, copy=True) for name, value in literal_inputs().items()}
    job_id = "fixed-ray.cpu.malformed"
    backend = "cpu"
    dtype = "float64"
    if case == "job-id":
        job_id = "invalid job id"
    elif case == "backend":
        backend = "metal"
    elif case == "dtype":
        dtype = "float16"
    elif case == "inventory":
        inputs.pop("matrix_direction")
    elif case == "bfloat16":
        dtype = "bfloat16"
    elif case == "scientific-dtype":
        inputs["coefficients"] = inputs["coefficients"].astype(np.float32)
    elif case == "coefficient-shape":
        inputs["coefficients"] = inputs["coefficients"].ravel()
    elif case == "spatial-shape":
        inputs["spatial_map"] = inputs["spatial_map"][:, :-1]
    elif case == "width":
        inputs["coefficients"] = inputs["coefficients"][:, :-1]
    elif case == "matrix-shape":
        inputs["matrix_direction"] = inputs["matrix_direction"][:1, :]
    elif case == "batch-dtype":
        inputs["batch_size"] = np.array(4.0, dtype=np.float64)
    elif case == "batch-zero":
        inputs["batch_size"] = np.array(0, dtype=np.int64)
    elif case == "matrix-symmetry":
        inputs["matrix_direction"] = np.array(
            [[1.0, 1.0], [0.0, 1.0]], dtype=np.float64
        )
    elif case == "matrix-positive":
        inputs["matrix_direction"] = np.diag([-1.0, 1.0])

    output = tmp_path / case
    with pytest.raises(WorkerBackendError, match=message):
        run_worker_job(
            worker_python=ANACONDA,
            worker_script=WORKER,
            work_root=output,
            job_id=job_id,
            requested_backend=backend,
            requested_dtype=dtype,
            arrays=inputs,
            environment_lock=ENVIRONMENT_LOCK,
        )
    assert not output.exists()


def _write_worker_request(
    root: Path, arrays: dict[str, np.ndarray]
) -> tuple[Path, Path, Path, Path]:
    root.mkdir()
    input_npz = root / "input.npz"
    request_json = root / "request.json"
    response_json = root / "response.json"
    output_npz = root / "output.npz"
    np.savez(input_npz, **arrays)
    descriptors = []
    for name, array in sorted(arrays.items()):
        dtype = "int64" if array.dtype == np.dtype(np.int64) else "float64"
        descriptors.append(
            {
                "name": name,
                "shape": list(array.shape),
                "dtype": dtype,
                "sha256": canonical_array_sha256(name, array, dtype),
            }
        )
    request_json.write_text(
        json.dumps(
            {
                "schema_version": "cuda-worker-protocol-v1",
                "message_type": "request",
                "job_id": "fixed-ray.worker.invalid-payload",
                "requested_backend": "cpu",
                "requested_dtype": "float64",
                "effective_backend": None,
                "effective_dtype": None,
                "environment_sha256": "0" * 64,
                "npz_sha256": hashlib.sha256(input_npz.read_bytes()).hexdigest(),
                "arrays": descriptors,
                "output_identity": None,
            },
            sort_keys=True,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )
    return request_json, input_npz, response_json, output_npz


@pytest.mark.parametrize(
    ("case", "mutate", "message"),
    (
        ("negative", lambda arrays: arrays["coefficients"].__setitem__((0, 0), -1.0), "nonnegative"),
        ("nonnormalized", lambda arrays: arrays["spatial_map"].__setitem__((0, 0), 0.6), "row-stochastic"),
        ("nan", lambda arrays: arrays["coefficients"].__setitem__((0, 0), np.nan), "finite"),
        ("inf", lambda arrays: arrays["spatial_map"].__setitem__((0, 0), np.inf), "finite"),
    ),
)
def test_standalone_worker_independently_rejects_invalid_probability_payload(
    tmp_path: Path, case: str, mutate: object, message: str
):
    inputs = {name: np.array(value, copy=True) for name, value in literal_inputs().items()}
    mutate(inputs)
    paths = _write_worker_request(tmp_path / case, inputs)
    environment = dict(os.environ)
    environment["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
    completed = subprocess.run(
        [str(ANACONDA), str(WORKER), *(str(path) for path in paths)],
        cwd=REPOSITORY,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 2
    assert message in completed.stderr
    assert not paths[2].exists()
    assert not paths[3].exists()


def test_torch_probability_checks_are_device_independent_and_fail_closed():
    script = f"""
import importlib.util
import torch
spec = importlib.util.spec_from_file_location('session6_cuda_worker', {str(WORKER)!r})
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)
valid_coefficients = torch.tensor([[0.2, 0.8]], dtype=torch.float64)
valid_map = torch.tensor([[0.75, 0.25], [0.1, 0.9]], dtype=torch.float64)
worker._validate_on_device_probability_payload(valid_coefficients, valid_map)
worker._validate_on_device_probability_output(valid_coefficients)
invalid_payloads = [
    (torch.tensor([[-0.2, 1.2]], dtype=torch.float64), valid_map),
    (valid_coefficients, torch.tensor([[0.8, 0.3], [0.1, 0.9]], dtype=torch.float64)),
    (torch.tensor([[float('nan'), 1.0]], dtype=torch.float64), valid_map),
    (valid_coefficients, torch.tensor([[float('inf'), 0.0], [0.1, 0.9]], dtype=torch.float64)),
]
for coefficients, spatial_map in invalid_payloads:
    try:
        worker._validate_on_device_probability_payload(coefficients, spatial_map)
    except worker.ProtocolError:
        pass
    else:
        raise AssertionError('invalid on-device payload accepted')
for output in (
    torch.tensor([[-1.0]], dtype=torch.float64),
    torch.tensor([[float('nan')]], dtype=torch.float64),
    torch.tensor([[float('inf')]], dtype=torch.float64),
):
    try:
        worker._validate_on_device_probability_output(output)
    except worker.ProtocolError:
        pass
    else:
        raise AssertionError('invalid on-device output accepted')
"""
    completed = subprocess.run(
        [str(ANACONDA), "-c", script],
        cwd=REPOSITORY,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr


def test_requested_cuda_on_unpinned_cpu_interpreter_fails_before_artifacts(tmp_path: Path):
    output = tmp_path / "must-not-exist"

    with pytest.raises(WorkerBackendError, match="pinned CUDA worker executable"):
        run_worker_job(
            worker_python=CPU_PYTHON,
            worker_script=WORKER,
            work_root=output,
            job_id="fixed-ray.cuda.rejected",
            requested_backend="cuda",
            requested_dtype="float64",
            arrays=literal_inputs(),
            environment_lock=ENVIRONMENT_LOCK,
        )
    assert not output.exists()


def test_pinned_cuda_preflight_rejects_hidden_device_before_job_artifacts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    output = tmp_path / "must-not-exist-hidden-device"
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")

    with pytest.raises(WorkerBackendError, match="CUDA preflight"):
        run_worker_job(
            worker_python=ANACONDA,
            worker_script=WORKER,
            work_root=output,
            job_id="fixed-ray.cuda.hidden",
            requested_backend="cuda",
            requested_dtype="float64",
            arrays=literal_inputs(),
            environment_lock=ENVIRONMENT_LOCK,
        )
    assert not output.exists()


def _rewrite_self_consistent_response(
    result: object,
    arrays: dict[str, np.ndarray],
) -> dict[str, object]:
    np.savez(result.output_npz, **arrays)
    response = dict(result.response_manifest)
    response["npz_sha256"] = hashlib.sha256(result.output_npz.read_bytes()).hexdigest()
    response["arrays"] = [
        {
            "name": name,
            "shape": list(array.shape),
            "dtype": "float64",
            "sha256": canonical_array_sha256(name, array, "float64"),
        }
        for name, array in sorted(arrays.items())
    ]
    response["output_identity"] = worker_output_identity(
        response, request_manifest=result.request_manifest
    )
    return response


def test_self_consistent_worker_output_must_match_fixed_kernel_contract(tmp_path: Path):
    result = run_worker_job(
        worker_python=ANACONDA,
        worker_script=WORKER,
        work_root=tmp_path / "contract",
        job_id="fixed-ray.cpu.contract",
        requested_backend="cpu",
        requested_dtype="float64",
        arrays=literal_inputs(rows=5),
        environment_lock=ENVIRONMENT_LOCK,
    )
    with np.load(result.output_npz, allow_pickle=False) as archive:
        valid = {name: np.array(archive[name], copy=True) for name in archive.files}

    extra = dict(valid)
    extra["unexpected"] = np.zeros((), dtype=np.float64)
    response = _rewrite_self_consistent_response(result, extra)
    with pytest.raises(WorkerBackendError, match="exact fixed-ray inventory"):
        validate_worker_result(
            request_manifest=result.request_manifest,
            response_manifest=response,
            output_npz=result.output_npz,
        )

    wrong_shape = dict(valid)
    wrong_shape["updated_coefficients"] = valid["updated_coefficients"][:, :-1]
    response = _rewrite_self_consistent_response(result, wrong_shape)
    with pytest.raises(WorkerBackendError, match="request-derived shape"):
        validate_worker_result(
            request_manifest=result.request_manifest,
            response_manifest=response,
            output_npz=result.output_npz,
        )


@pytest.mark.parametrize("invalid_value", (-1.0, np.nan, np.inf))
def test_self_consistent_support_invalid_or_nonfinite_worker_output_is_rejected(
    tmp_path: Path, invalid_value: float
):
    result = run_worker_job(
        worker_python=ANACONDA,
        worker_script=WORKER,
        work_root=tmp_path / "invalid-output",
        job_id="fixed-ray.cpu.invalid-output",
        requested_backend="cpu",
        requested_dtype="float64",
        arrays=literal_inputs(rows=5),
        environment_lock=ENVIRONMENT_LOCK,
    )
    with np.load(result.output_npz, allow_pickle=False) as archive:
        mutated = {name: np.array(archive[name], copy=True) for name in archive.files}
    mutated["updated_coefficients"][0, 0] = invalid_value
    response = _rewrite_self_consistent_response(result, mutated)
    with pytest.raises(WorkerBackendError, match="finite nonnegative"):
        validate_worker_result(
            request_manifest=result.request_manifest,
            response_manifest=response,
            output_npz=result.output_npz,
        )

def test_mutated_output_npz_and_parity_candidate_are_rejected(tmp_path: Path):
    result = run_worker_job(
        worker_python=ANACONDA,
        worker_script=WORKER,
        work_root=tmp_path / "mutation",
        job_id="fixed-ray.cpu.mutation",
        requested_backend="cpu",
        requested_dtype="float64",
        arrays=literal_inputs(),
        environment_lock=ENVIRONMENT_LOCK,
    )
    with np.load(result.output_npz) as archive:
        mutated = {name: archive[name].copy() for name in archive.files}
    mutated["updated_coefficients"][0, 0] += 1.0
    np.savez(result.output_npz, **mutated)

    with pytest.raises(WorkerBackendError, match="NPZ SHA-256"):
        validate_worker_result(
            request_manifest=result.request_manifest,
            response_manifest=result.response_manifest,
            output_npz=result.output_npz,
        )

    reference = np.ones((2, 3), dtype=np.float64)
    candidate = reference.copy()
    candidate[0, 0] += 1.0e-4
    parity = parity_diagnostics(
        reference,
        candidate,
        dtype="float64",
        condition_number=1.0,
    )
    assert parity.passed is False
    assert parity.maximum_absolute_residual == pytest.approx(1.0e-4)


def test_controller_import_has_no_torch_or_cuda_side_effects():
    completed = subprocess.run(
        [
            str(CPU_PYTHON),
            "-c",
            (
                "import sys; sys.path.insert(0, 'src'); import numpy as np; "
                "before=np.random.get_state()[1].copy(); "
                "import multiagent_elbo.cuda_backend; "
                "after=np.random.get_state()[1]; "
                "print('torch' in sys.modules, np.array_equal(before, after))"
            ),
        ],
        cwd=REPOSITORY,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() == "False True"
