from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

import numpy as np
import pytest

from multiagent_elbo.cuda_backend import (
    WorkerBackendError,
    canonical_array_sha256,
    parity_diagnostics,
    run_worker_job,
    validate_worker_result,
)
from multiagent_elbo.experiment_support import validate_worker_protocol_manifest


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
    assert result.provenance["kernel_strategy"] == "batched_spatial_map_matmul"
    assert result.provenance["batch_size"] == 4
    assert result.provenance["requested_backend"] == "cpu"
    assert result.provenance["effective_backend"] == "cpu"
    assert result.provenance["requested_dtype"] == "float64"
    assert result.provenance["effective_dtype"] == "float64"


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
