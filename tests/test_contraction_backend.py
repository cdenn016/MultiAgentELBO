"""Tests for the blocked-contraction worker route of the rescaling step."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pytest

from multiagent_elbo.cuda_backend import WorkerBackendError, run_worker_job
from multiagent_elbo.finite.contraction_backend import (
    DEFAULT_ENVIRONMENT_LOCK,
    DEFAULT_WORKER_PYTHON,
    DEFAULT_WORKER_SCRIPT,
    fine_step_factors,
    initial_step_via_worker,
    iterated_step_via_worker,
)
from multiagent_elbo.finite.closure_residual import _coarse_child_weights
from multiagent_elbo.finite.coupling_readback import initial_step, iterated_step
from multiagent_elbo.finite.nested_tower import reference_tower, tower_blocks

OBSERVATION = (1, 0, 1, 0, 1, 0)


def blocked_job_arrays(states: int = 3):
    """Return a tiny valid blocked-contraction job for validation tests."""
    kernels = np.full((2, states, states, states), 1.0 / states, dtype=np.float64)
    return {
        "site_factors": np.ones((4, states), dtype=np.float64),
        "edge_factors": np.ones((1, states, states), dtype=np.float64),
        "edge_axes": np.array([[0, 2]], dtype=np.int64),
        "block_kernels": kernels,
        "block_axes": np.array([[0, 1], [2, 3]], dtype=np.int64),
        "batch_size": np.array(1, dtype=np.int64),
    }


def test_the_factorized_child_theory_reproduces_the_audited_weight_tensor() -> None:
    tower = reference_tower()
    site, edge, axes = fine_step_factors(tower, OBSERVATION)
    states = tower.state_count
    count = len(tower.agents)
    weights = np.ones((states,) * count)
    for index in range(count):
        shape = [1] * count
        shape[index] = states
        weights = weights * site[index].reshape(shape)
    for factor, (low, high) in zip(edge, axes):
        shape = [1] * count
        shape[int(low)] = states
        shape[int(high)] = states
        weights = weights * factor.reshape(shape)
    audited = _coarse_child_weights(tower, OBSERVATION)
    assert np.abs(weights - audited).max() <= 1.0e-13 * np.abs(audited).max()


def test_the_controller_rejects_undeclared_blocked_contraction_jobs(
    tmp_path: Path,
) -> None:
    good = blocked_job_arrays()
    bad_kernels = dict(good)
    bad_kernels["block_kernels"] = good["block_kernels"] * 2.0
    bad_axes = dict(good)
    bad_axes["block_axes"] = np.array([[0, 1], [1, 3]], dtype=np.int64)
    for label, arrays in (("kernels", bad_kernels), ("axes", bad_axes)):
        with pytest.raises(WorkerBackendError):
            run_worker_job(
                worker_python=DEFAULT_WORKER_PYTHON,
                worker_script=DEFAULT_WORKER_SCRIPT,
                work_root=tmp_path / f"rejected-{label}",
                job_id=f"blocked-contraction.rejected.{label}",
                requested_backend="cpu",
                requested_dtype="float64",
                arrays=arrays,
                environment_lock=DEFAULT_ENVIRONMENT_LOCK,
            )
    with pytest.raises(WorkerBackendError, match="bfloat16"):
        run_worker_job(
            worker_python=DEFAULT_WORKER_PYTHON,
            worker_script=DEFAULT_WORKER_SCRIPT,
            work_root=tmp_path / "rejected-bfloat16",
            job_id="blocked-contraction.rejected.bfloat16",
            requested_backend="cpu",
            requested_dtype="bfloat16",
            arrays=good,
            environment_lock=DEFAULT_ENVIRONMENT_LOCK,
        )


def test_the_cpu_worker_step_matches_the_in_process_step(tmp_path: Path) -> None:
    tower = reference_tower()
    blocks = tower_blocks(2, 3)
    reference = initial_step(tower, OBSERVATION, blocks)
    routed = initial_step_via_worker(
        tower,
        OBSERVATION,
        blocks,
        work_root=tmp_path / "worker-initial",
        backend="cpu",
    )
    deviation = max(
        abs(float(routed.action[state]) - float(value))
        for state, value in reference.action.items()
    )
    assert deviation <= 1.0e-12
    assert routed.connection.graph == reference.connection.graph
    assert routed.projection_ratio <= 1.0e-9


def test_the_cpu_worker_iterated_step_matches_the_in_process_couplings(
    tmp_path: Path,
) -> None:
    tower = reference_tower()
    step = initial_step(tower, OBSERVATION, tower_blocks(2, 3))
    reference = iterated_step(step.instance, ((1, 2),))
    routed = iterated_step_via_worker(
        step.instance,
        ((1, 2),),
        work_root=tmp_path / "worker-iterated",
        backend="cpu",
    )
    for left, right in zip(routed.mobius.sites[0], reference.mobius.sites[0]):
        assert abs(float(left) - float(right)) <= 1.0e-11


@pytest.mark.skipif(
    os.environ.get("MULTIAGENTELBO_RUN_CUDA_TESTS") != "1",
    reason="requires explicit dedicated CUDA-lane opt-in",
)
def test_the_cuda_worker_step_matches_the_in_process_step(tmp_path: Path) -> None:
    tower = reference_tower()
    blocks = tower_blocks(2, 3)
    reference = initial_step(tower, OBSERVATION, blocks)
    routed = initial_step_via_worker(
        tower,
        OBSERVATION,
        blocks,
        work_root=tmp_path / "worker-cuda",
        backend="cuda",
    )
    deviation = max(
        abs(float(routed.action[state]) - float(value))
        for state, value in reference.action.items()
    )
    assert deviation <= 1.0e-12
