r"""Route the blocked contraction of the rescaling step through the worker.

The in-process contraction in :mod:`coupling_readback` is the default and the
reference. This module carries the same step through the declared CUDA worker
protocol for instances whose joint state space no longer fits comfortable
in-process work: the child theory is shipped factorized, one nonnegative factor
per site and per edge plus one normalized Bayes kernel per block, kilobytes in
total, and the worker builds the dense child-weight tensor on the compute
device and contracts it to the coarse marginal. Reproducibility, hashing, and
CPU/CUDA parity therefore come from machinery that already exists and is
tested, rather than from a new path, which is what the design requires.

The factorization is exact, not an approximation: the auxiliary pairwise child
theory is a product of site likelihood factors and per-edge divergence factors
by construction, and a coarse instance's coupling action is a sum of site and
pair tables by construction, so the worker's product reproduces the in-process
weight tensor entry for entry up to floating-point association order.

float64 is the admissible precision; float32 is permitted only with the
protocol's parity diagnostics, and bfloat16 is refused on both sides of the
protocol, because the measured three-body components sit three decades below
the pairwise ones and bfloat16 carries roughly three decimal digits.

Reproducibility boundary (2026-08-18 audit, F9): the declared worker
interpreter is the Anaconda CUDA build, whose numpy 2.0.0 is nondeterministic
within a session at the 1e-8 level for the 8-cycle reduced step, while the
in-process route on numpy 2.4.4 is deterministic. A bit-level reproducibility
claim about a worker-routed step must therefore pin the worker's numpy
version, not only the interpreter path; the 1e-8-scale disagreement between
routes is an interpreter artifact, not a protocol defect.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np

from ..cuda_backend import Backend, run_worker_job
from .categorical_falsification_model import FalsificationModel
from .closure_residual import (
    _action_and_flow_from_marginal,
    _block_bayes_kernel,
    _block_prior_vector,
    _divergence_table,
)
from .coupling_readback import (
    PairwiseCouplings,
    PairwiseInstance,
    RescalingStep,
    _checked_step_blocks,
    _kernel_model,
    _readback_from_action,
)

_REPOSITORY = Path(__file__).resolve().parents[3]
DEFAULT_WORKER_PYTHON = Path(r"C:\anaconda\python.exe")
DEFAULT_WORKER_SCRIPT = _REPOSITORY / "tools" / "cuda_worker.py"
DEFAULT_ENVIRONMENT_LOCK = _REPOSITORY / "environments" / "cuda-rtx5090-cu128.lock.txt"


def fine_step_factors(
    model: FalsificationModel,
    observation: Sequence[int],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the factorized child theory of the declared model at one record.

    The factors reproduce the audited child-weight construction exactly: one
    likelihood column per agent, and per edge the exponential of both channels'
    weighted divergences, transposed onto ascending axes whenever the receiver
    occupies the later axis.
    """
    size = model.state_count
    agents = model.agents
    index_of = {agent: position for position, agent in enumerate(agents)}
    likelihood = model.likelihood_table()
    configuration = model.row_configurations[0]
    event_law = {
        channel: model.edge_event_law(configuration, channel)
        for channel in ("belief", "model")
    }
    kappa = {"belief": model.kappa_belief, "model": model.kappa_model}
    site_factors = np.stack(
        [likelihood[:, observation[index_of[agent]]] for agent in agents]
    )
    edge_factors: list[np.ndarray] = []
    edge_axes: list[tuple[int, int]] = []
    for edge_index, edge in enumerate(model.graph.edges):
        if edge.receiver == edge.source:
            continue
        receiver = index_of[edge.receiver]
        source = index_of[edge.source]
        table = np.zeros((size, size), dtype=np.float64)
        for channel in ("belief", "model"):
            strength = kappa[channel] * float(
                event_law[channel][receiver, source]
            )
            element = model.graph.channel_elements(channel)[edge_index]
            table = table + strength * _divergence_table(model, channel, element)
        factor = np.exp(-table)
        if receiver > source:
            factor = factor.T
        edge_factors.append(factor)
        edge_axes.append((min(receiver, source), max(receiver, source)))
    return (
        site_factors,
        np.stack(edge_factors) if edge_factors else np.zeros((0, size, size)),
        np.array(edge_axes, dtype=np.int64).reshape(len(edge_axes), 2),
    )


def coupling_step_factors(
    couplings: PairwiseCouplings,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the factorized Boltzmann weights of one declared coupling vector.

    The constant is folded into the first site factor so the product equals
    the exponential of the full coupling action rather than of a shifted one.
    """
    size = len(couplings.sites[0])
    site_factors = np.stack(
        [
            np.exp(-np.array([float(value) for value in table]))
            for table in couplings.sites
        ]
    )
    site_factors[0] = site_factors[0] * math.exp(-float(couplings.constant))
    edge_factors: list[np.ndarray] = []
    edge_axes: list[tuple[int, int]] = []
    for (left, right), table in couplings.pairs:
        edge_factors.append(
            np.exp(-np.array([[float(value) for value in row] for row in table]))
        )
        edge_axes.append((left, right))
    return (
        site_factors,
        np.stack(edge_factors) if edge_factors else np.zeros((0, size, size)),
        np.array(edge_axes, dtype=np.int64).reshape(len(edge_axes), 2),
    )


def _worker_readback(
    model: FalsificationModel,
    site_factors: np.ndarray,
    edge_factors: np.ndarray,
    edge_axes: np.ndarray,
    declared: tuple[tuple[int, ...], ...],
    *,
    work_root: Path,
    job_id: str,
    backend: Backend,
    dtype: str,
    worker_python: Path,
    worker_script: Path,
    environment_lock: Path,
    timeout_seconds: float,
    parent_priors: Mapping[int, Sequence[float]] | None = None,
) -> RescalingStep:
    """Contract one factorized step through the worker and read couplings back."""
    widths = {len(block) for block in declared}
    if len(widths) != 1:
        raise ValueError(
            "the worker job carries one stacked kernel tensor, so every block "
            "must have the same size"
        )
    index_of = {agent: position for position, agent in enumerate(model.agents)}
    numpy_dtype = np.dtype(np.float64 if dtype == "float64" else np.float32)
    arrays = {
        "site_factors": site_factors.astype(numpy_dtype),
        "edge_factors": edge_factors.astype(numpy_dtype),
        "edge_axes": np.asarray(edge_axes, dtype=np.int64),
        "block_kernels": np.stack(
            [
                _block_bayes_kernel(
                    model, block, _block_prior_vector(model, block, parent_priors)
                )
                for block in declared
            ]
        ).astype(numpy_dtype),
        "block_axes": np.array(
            [[index_of[agent] for agent in block] for block in declared],
            dtype=np.int64,
        ),
        "batch_size": np.array(1, dtype=np.int64),
    }
    result = run_worker_job(
        worker_python=worker_python,
        worker_script=worker_script,
        work_root=work_root,
        job_id=job_id,
        requested_backend=backend,
        requested_dtype=dtype,
        arrays=arrays,
        environment_lock=environment_lock,
        timeout_seconds=timeout_seconds,
    )
    marginal = np.asarray(result.arrays["coarse_marginal"], dtype=np.float64)
    action, flow = _action_and_flow_from_marginal(marginal)
    return _readback_from_action(model, action, flow, declared)


def initial_step_via_worker(
    model: FalsificationModel,
    observation: Sequence[int],
    blocks: Sequence[Sequence[int]],
    *,
    work_root: Path,
    backend: Backend = "cuda",
    dtype: str = "float64",
    worker_python: Path = DEFAULT_WORKER_PYTHON,
    worker_script: Path = DEFAULT_WORKER_SCRIPT,
    environment_lock: Path = DEFAULT_ENVIRONMENT_LOCK,
    timeout_seconds: float = 600.0,
    job_id: str | None = None,
) -> RescalingStep:
    """Run one closed renormalization step with the contraction on the worker."""
    if type(model) is not FalsificationModel:
        raise TypeError("model must be a FalsificationModel")
    record = tuple(observation)
    if len(record) != len(model.agents):
        raise ValueError("the observation must carry one record per declared agent")
    if any(type(value) is not int or value not in (0, 1) for value in record):
        raise ValueError("every observation record must be binary")
    declared = _checked_step_blocks(model, blocks)
    site_factors, edge_factors, edge_axes = fine_step_factors(model, record)
    return _worker_readback(
        model,
        site_factors,
        edge_factors,
        edge_axes,
        declared,
        work_root=work_root,
        job_id=job_id or f"blocked-contraction.initial.{backend}",
        backend=backend,
        dtype=dtype,
        worker_python=worker_python,
        worker_script=worker_script,
        environment_lock=environment_lock,
        timeout_seconds=timeout_seconds,
    )


def iterated_step_via_worker(
    instance: PairwiseInstance,
    blocks: Sequence[Sequence[int]],
    *,
    work_root: Path,
    backend: Backend = "cuda",
    dtype: str = "float64",
    worker_python: Path = DEFAULT_WORKER_PYTHON,
    worker_script: Path = DEFAULT_WORKER_SCRIPT,
    environment_lock: Path = DEFAULT_ENVIRONMENT_LOCK,
    timeout_seconds: float = 600.0,
    job_id: str | None = None,
) -> RescalingStep:
    """Run one coarse-instance renormalization step on the worker."""
    if type(instance) is not PairwiseInstance:
        raise TypeError("instance must be a PairwiseInstance")
    model = _kernel_model(instance.graph, "coarse-instance")
    declared = _checked_step_blocks(model, blocks)
    site_factors, edge_factors, edge_axes = coupling_step_factors(instance.couplings)
    return _worker_readback(
        model,
        site_factors,
        edge_factors,
        edge_axes,
        declared,
        work_root=work_root,
        job_id=job_id or f"blocked-contraction.iterated.{backend}",
        backend=backend,
        dtype=dtype,
        worker_python=worker_python,
        worker_script=worker_script,
        environment_lock=environment_lock,
        timeout_seconds=timeout_seconds,
    )


__all__ = [
    "DEFAULT_ENVIRONMENT_LOCK",
    "DEFAULT_WORKER_PYTHON",
    "DEFAULT_WORKER_SCRIPT",
    "coupling_step_factors",
    "fine_step_factors",
    "initial_step_via_worker",
    "iterated_step_via_worker",
]
