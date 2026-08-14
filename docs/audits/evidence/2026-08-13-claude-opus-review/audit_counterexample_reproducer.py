"""Deterministic counterexamples for the 2026-08-13 Claude Opus audit.

This file is audit evidence, not part of the project runtime. It reproduces only
the narrow mathematical and implementation claims named in its JSON output.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.special import polygamma


ROOT = Path(__file__).resolve().parents[4]
META_PATH = ROOT / "docs" / "verification" / "meta_agent_coherence_witness.py"
SEED = 20260813


def load_meta_module():
    spec = importlib.util.spec_from_file_location("meta_agent_coherence_witness", META_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {META_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rank_two_positive_split() -> dict[str, float | int]:
    lam = np.array([[1.0, 0.1], [1.0, 0.2], [1.0, 0.3], [1.0, 0.4]])
    precision = np.linalg.inv(np.eye(4) + lam @ lam.T)
    beta = -(precision - np.diag(np.diag(precision)))
    laplacian = np.diag(beta.sum(axis=1)) - beta
    prior = np.diag(precision - laplacian)
    correction_rank = int(np.linalg.matrix_rank(np.eye(4) - precision, tol=1e-12))
    residual = float(np.linalg.norm(precision - laplacian - np.diag(prior)))
    off = beta[np.triu_indices(4, 1)]
    assert correction_rank == 2
    assert float(off.min()) > 0.0
    assert float(prior.min()) > 0.0
    assert residual < 1e-12
    return {
        "correction_rank": correction_rank,
        "min_beta": float(off.min()),
        "min_prior": float(prior.min()),
        "split_residual": residual,
    }


def weighted_rotation_cocycle() -> dict[str, float]:
    def rotation(theta: float) -> np.ndarray:
        return np.array(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
        )

    rotations = [rotation(theta) for theta in (0.1, 0.7, -0.4)]
    beta = 0.25
    precision = np.eye(6)
    loading = np.vstack(rotations)
    precision -= loading @ (0.25 * np.eye(2)) @ loading.T
    max_cross_residual = 0.0
    max_cocycle_residual = 0.0
    for a in range(3):
        for b in range(3):
            omega_ab = rotations[a] @ rotations[b].T
            if a != b:
                block = precision[2 * a : 2 * a + 2, 2 * b : 2 * b + 2]
                max_cross_residual = max(
                    max_cross_residual, float(np.linalg.norm(block + beta * omega_ab))
                )
            for c in range(3):
                omega_bc = rotations[b] @ rotations[c].T
                omega_ac = rotations[a] @ rotations[c].T
                max_cocycle_residual = max(
                    max_cocycle_residual,
                    float(np.linalg.norm(omega_ab @ omega_bc - omega_ac)),
                )
    residual_prior = precision[:2, :2] - 2.0 * beta * np.eye(2)
    min_prior_eigenvalue = float(np.linalg.eigvalsh(residual_prior).min())
    assert max_cross_residual < 1e-12
    assert max_cocycle_residual < 1e-12
    assert min_prior_eigenvalue > 0.0
    return {
        "max_cross_block_residual": max_cross_residual,
        "max_cocycle_residual": max_cocycle_residual,
        "min_residual_prior_eigenvalue": min_prior_eigenvalue,
    }


def support_scaled_prior(meta) -> dict[str, float | int]:
    k, n = 3, 5
    core = [(1, 0), (2, 1), (0, 2)]
    edges = core + [(3, 0), (4, 3)]
    rng_prior = np.random.default_rng(SEED)

    def spd() -> np.ndarray:
        a = expm(rng_prior.normal(size=(k, k)) * 0.5)
        return a @ a.T

    prior = {i: spd() for i in range(n)}
    rng_links = np.random.default_rng(SEED + 7)
    theta = {edge: meta.so3(rng_links.normal(size=3) * 0.8) for edge in edges}
    weights = {edge: 1.0 for edge in core}
    weights[(3, 0)] = 1.0
    weights[(4, 3)] = 0.0

    def assemble(chi: np.ndarray) -> np.ndarray:
        result = np.zeros((n * k, n * k))
        for edge in edges:
            i, j = edge
            transform = theta[edge]
            weight = weights[edge] * chi[i] * chi[j]
            metric = weight * np.eye(k)
            result[i * k : (i + 1) * k, i * k : (i + 1) * k] += metric
            result[j * k : (j + 1) * k, j * k : (j + 1) * k] += (
                transform.T @ metric @ transform
            )
            result[i * k : (i + 1) * k, j * k : (j + 1) * k] -= metric @ transform
            result[j * k : (j + 1) * k, i * k : (i + 1) * k] -= transform.T @ metric
        for i in range(n):
            result[i * k : (i + 1) * k, i * k : (i + 1) * k] += 0.25 * chi[i] * prior[i]
        return result

    chi_departed = np.ones(n)
    chi_departed[4] = 0.0
    eigenvalues = np.linalg.eigvalsh(assemble(chi_departed))
    zero_modes = int(np.sum(np.abs(eigenvalues) < 1e-10))
    assert zero_modes == k
    return {"chi_scaled_lambda_min": float(eigenvalues[0]), "zero_modes": zero_modes}


def regime_table_mismatch(meta) -> dict[str, float | list[float]]:
    k, n = 3, 4
    edges = [(1, 0), (2, 1), (3, 2), (0, 2), (0, 3)]
    rng = np.random.default_rng(SEED + 1)
    omega = {}
    for edge in edges:
        transform = meta.so3(rng.normal(size=3) * 0.9)
        transform = transform @ np.diag(np.exp(rng.normal(size=3) * 0.4))
        omega[edge] = transform
        omega[(edge[1], edge[0])] = np.linalg.inv(transform)
    forward = rng.uniform(0.1, 1.0, len(edges))
    reverse = rng.uniform(0.1, 1.0, len(edges))
    source = meta._retracted_laplacian(omega, edges, forward, reverse, n)
    intended = np.zeros_like(source)
    row_sums = np.zeros(n)
    for (i, j), a, b in zip(edges, forward, reverse):
        intended[i * k : (i + 1) * k, i * k : (i + 1) * k] += a * np.eye(k)
        intended[j * k : (j + 1) * k, j * k : (j + 1) * k] += b * np.eye(k)
        intended[i * k : (i + 1) * k, j * k : (j + 1) * k] -= a * omega[(i, j)]
        intended[j * k : (j + 1) * k, i * k : (i + 1) * k] -= b * omega[(j, i)]
        row_sums[i] += a
        row_sums[j] += b
    relative_operator_mismatch = float(np.linalg.norm(source - intended) / np.linalg.norm(intended))
    source_asymmetry = float(np.linalg.norm(source - source.T) / np.linalg.norm(source))
    intended_asymmetry = float(np.linalg.norm(intended - intended.T) / np.linalg.norm(intended))
    source_min_real = float(np.linalg.eigvals(source).real.min())
    intended_min_real = float(np.linalg.eigvals(intended).real.min())
    assert relative_operator_mismatch > 0.1
    assert np.max(np.abs(row_sums - 1.0)) > 0.2
    return {
        "relative_operator_mismatch": relative_operator_mismatch,
        "source_asymmetry": source_asymmetry,
        "intended_asymmetry": intended_asymmetry,
        "source_min_real_eigenvalue": source_min_real,
        "intended_min_real_eigenvalue": intended_min_real,
        "outgoing_row_sums": [float(value) for value in row_sums],
    }


def fisher_kl_slot() -> dict[str, float]:
    sigma_i = np.diag([1.0, 4.0])
    sigma_j = np.diag([9.0, 1.0])
    first_slot = np.linalg.inv(sigma_i)
    second_slot = np.linalg.inv(sigma_j)
    step = 1e-4

    def variable_mean_part(x: np.ndarray) -> float:
        return 0.5 * float(x @ second_slot @ x)

    finite_difference = np.zeros((2, 2))
    origin = np.zeros(2)
    for a in range(2):
        for b in range(2):
            ea = np.zeros(2)
            eb = np.zeros(2)
            ea[a] = step
            eb[b] = step
            finite_difference[a, b] = (
                variable_mean_part(origin + ea + eb)
                - variable_mean_part(origin + ea - eb)
                - variable_mean_part(origin - ea + eb)
                + variable_mean_part(origin - ea - eb)
            ) / (4.0 * step * step)
    first_error = float(np.linalg.norm(finite_difference - first_slot))
    second_error = float(np.linalg.norm(finite_difference - second_slot))
    assert second_error < 1e-8
    assert first_error > 0.5
    return {"first_slot_hessian_error": first_error, "second_slot_hessian_error": second_error}


def curved_zero_mode(meta) -> dict[str, float]:
    theta = 0.6
    rotation_z = np.array(
        [
            [np.cos(theta), -np.sin(theta), 0.0],
            [np.sin(theta), np.cos(theta), 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    edges = [(0, 1), (1, 2), (2, 0)]
    omega = {(0, 1): np.eye(3), (1, 2): np.eye(3), (2, 0): rotation_z}
    laplacian = meta.connection_laplacian(omega, edges, [1.0, 1.0, 1.0], 3)
    parallel_z = np.tile(np.array([0.0, 0.0, 1.0]), 3)
    holonomy_residual = float(np.linalg.norm(rotation_z - np.eye(3)))
    kernel_residual = float(np.linalg.norm(laplacian @ parallel_z))
    lambda_min = float(np.linalg.eigvalsh(laplacian)[0])
    assert holonomy_residual > 0.1
    assert kernel_residual < 1e-12
    assert abs(lambda_min) < 1e-12
    return {
        "nonidentity_holonomy_residual": holonomy_residual,
        "parallel_section_residual": kernel_residual,
        "lambda_min": lambda_min,
    }


def gamma_nontransitive_isometry() -> dict[str, float]:
    shape, rate, scale = 2.3, 1.7, 3.2

    def fisher(a: float, b: float) -> np.ndarray:
        return np.array([[polygamma(1, a), -1.0 / b], [-1.0 / b, a / (b * b)]])

    target_rate = rate / scale
    jacobian = np.diag([1.0, 1.0 / scale])
    residual = float(
        np.linalg.norm(jacobian.T @ fisher(shape, target_rate) @ jacobian - fisher(shape, rate))
    )
    assert residual < 1e-12
    return {"fisher_pullback_residual": residual, "shape_before": shape, "shape_after": shape}


def dimension_not_sufficient_for_invertibility() -> dict[str, float | int]:
    loading_a = np.array([[1.0, 0.0], [0.0, 0.0]])
    loading_b = np.array([[1.0, 0.0], [0.0, 0.0]])
    induced = loading_a @ np.eye(2) @ loading_b.T
    rank = int(np.linalg.matrix_rank(induced))
    determinant = float(np.linalg.det(induced))
    assert loading_a.shape[1] == loading_a.shape[0]
    assert rank < 2
    return {"K": 2, "d": 2, "induced_rank": rank, "determinant": determinant}


def main() -> None:
    meta = load_meta_module()
    results = {
        "rank_two_positive_split": rank_two_positive_split(),
        "weighted_rotation_cocycle": weighted_rotation_cocycle(),
        "support_scaled_prior": support_scaled_prior(meta),
        "regime_table_mismatch": regime_table_mismatch(meta),
        "fisher_kl_slot": fisher_kl_slot(),
        "curved_zero_mode": curved_zero_mode(meta),
        "gamma_nontransitive_isometry": gamma_nontransitive_isometry(),
        "dimension_not_sufficient_for_invertibility": dimension_not_sufficient_for_invertibility(),
    }
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
