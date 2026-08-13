"""Finite U(1) two-path record-law witness with exact controls.

This witness asks a deliberately narrow question: once parallel transport along a
curve is declared as an argument of a normalized generative record kernel, can two
flat connections on S^1 with different monodromy produce different record laws?

The load-bearing separator is a moment of the marginalized observation law.  For
equal path weights and path-angle difference Theta,

    ||E[O | Theta]||^2 = ||mu||^2 (1 + cos Theta) / 2.

It is therefore gauge invariant, observable without the latent path label, and
separates Theta=0 from Theta=pi/2 exactly.  Sampled total variation is retained only
as a numerical diagnostic; a sampled gauge grid cannot prove a lower bound on an
orbit infimum.

The exact controls also show the interpretation boundary.  A zero-connection model
with label-dependent group twists reproduces the same component laws exactly.  Thus
the constrained curve-transport family is monodromy-sensitive, but records alone
identify a relative group twist, not its connection origin.

Run: C:\\Python314\\python.exe docs/verification/u1_two_path_holonomy_witness.py
Requires: numpy.
"""

from __future__ import annotations

import json

import numpy as np


TWO_PI = 2.0 * np.pi
PHI0 = np.pi / 2
MU_J = np.array([1.0, 0.0])
SIG_J = np.diag([0.50, 0.20])
SIGMA_O = 0.35
PI_ROW = np.array([0.5, 0.5])


def R(theta: float) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])


def push(theta: float, mu: np.ndarray, covariance: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Push a Gaussian law forward by the U(1) rotation with angle ``theta``."""
    rotation = R(theta)
    return rotation @ mu, rotation @ covariance @ rotation.T


def kl_gauss(
    mean_1: np.ndarray,
    covariance_1: np.ndarray,
    mean_0: np.ndarray,
    covariance_0: np.ndarray,
) -> float:
    """Exact KL(N(mean_1,covariance_1) || N(mean_0,covariance_0))."""
    dimension = len(mean_1)
    inverse_0 = np.linalg.inv(covariance_0)
    displacement = mean_0 - mean_1
    return float(
        0.5
        * (
            np.trace(inverse_0 @ covariance_1)
            + displacement @ inverse_0 @ displacement
            - dimension
            + np.log(np.linalg.det(covariance_0) / np.linalg.det(covariance_1))
        )
    )


def gauss_pdf(points: np.ndarray, mean: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    inverse = np.linalg.inv(covariance)
    displacement = points - mean
    quadratic = np.einsum("...a,ab,...b->...", displacement, inverse, displacement)
    return np.exp(-0.5 * quadratic) / (TWO_PI * np.sqrt(np.linalg.det(covariance)))


def transport_angles(theta: float) -> tuple[float, float]:
    """Angles along the short and long paths; their difference is ``theta``."""
    direct = theta * PHI0 / TWO_PI
    around = theta * (PHI0 - TWO_PI) / TWO_PI
    return direct, around


def source_laws(
    theta: float, gauge_i: float = 0.0, gauge_j: float = 0.0
) -> list[tuple[np.ndarray, np.ndarray]]:
    mean_j, covariance_j = push(gauge_j, MU_J, SIG_J)
    return [
        push(gauge_i + angle - gauge_j, mean_j, covariance_j)
        for angle in transport_angles(theta)
    ]


def record_law_components(
    theta: float, gauge_i: float = 0.0, gauge_j: float = 0.0
) -> list[tuple[np.ndarray, np.ndarray]]:
    noise = SIGMA_O**2 * np.eye(2)
    return [(mean, covariance + noise) for mean, covariance in source_laws(theta, gauge_i, gauge_j)]


def mixture_moments(
    components: list[tuple[np.ndarray, np.ndarray]],
    weights: np.ndarray = PI_ROW,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the exact mean and covariance of a finite Gaussian mixture."""
    mean = sum(weight * component_mean for weight, (component_mean, _) in zip(weights, components))
    covariance = np.zeros((2, 2))
    for weight, (component_mean, component_covariance) in zip(weights, components):
        offset = component_mean - mean
        covariance += weight * (component_covariance + np.outer(offset, offset))
    return mean, covariance


def record_mean_norm_sq(theta: float) -> float:
    mean, _ = mixture_moments(record_law_components(theta))
    return float(mean @ mean)


def record_covariance_spectrum(theta: float) -> np.ndarray:
    _, covariance = mixture_moments(record_law_components(theta))
    return np.linalg.eigvalsh(covariance)


def _component_error(
    left: list[tuple[np.ndarray, np.ndarray]],
    right: list[tuple[np.ndarray, np.ndarray]],
) -> float:
    errors: list[float] = []
    for (left_mean, left_covariance), (right_mean, right_covariance) in zip(left, right, strict=True):
        errors.extend(
            [
                float(np.max(np.abs(left_mean - right_mean))),
                float(np.max(np.abs(left_covariance - right_covariance))),
            ]
        )
    return max(errors, default=0.0)


def periodic_aligned_component_error(theta: float, turns: int) -> float:
    """Exact component error after aligning theta+2*pi*turns by one common gauge."""
    gauge = -turns * PHI0
    shifted = record_law_components(theta + TWO_PI * turns, gauge_i=gauge)
    return _component_error(shifted, record_law_components(theta))


def mirror_aligned_component_error(theta: float) -> float:
    """Exact theta <-> 2*pi-theta equivalence after common gauge and label swap."""
    gauge = np.pi / 2 + theta / 2
    gauged = record_law_components(theta, gauge_i=gauge)
    mirrored_and_swapped = list(reversed(record_law_components(TWO_PI - theta)))
    return _component_error(gauged, mirrored_and_swapped)


def coboundary_record_law_components(
    theta: float, gauge_i: float = 0.0
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Record components for A=d lambda, lambda=theta*sin(phi)/(2*pi).

    Both routes have the same endpoint angle alpha=lambda(PHI0)-lambda(0).
    """
    alpha = theta * np.sin(PHI0) / TWO_PI
    mean, covariance = push(alpha + gauge_i, MU_J, SIG_J)
    record_component = (mean, covariance + SIGMA_O**2 * np.eye(2))
    return [record_component, (record_component[0].copy(), record_component[1].copy())]


def coboundary_aligned_component_error(theta: float) -> float:
    alpha = theta * np.sin(PHI0) / TWO_PI
    aligned = coboundary_record_law_components(theta, gauge_i=-alpha)
    return _component_error(aligned, coboundary_record_law_components(0.0))


def flat_twist_record_law_components(theta: float) -> list[tuple[np.ndarray, np.ndarray]]:
    """Zero-connection presentation with explicit label-dependent kernel twists.

    The ordinary kernel parameters are the two group angles that the curve presentation
    obtains from its paths.  No connection variable is present in this presentation.
    """
    noise = SIGMA_O**2 * np.eye(2)
    return [
        (mean, covariance + noise)
        for mean, covariance in (push(twist, MU_J, SIG_J) for twist in transport_angles(theta))
    ]


def record_pdf(
    points: np.ndarray, theta: float, gauge_i: float = 0.0, gauge_j: float = 0.0
) -> np.ndarray:
    components = record_law_components(theta, gauge_i, gauge_j)
    return sum(
        weight * gauss_pdf(points, mean, covariance)
        for weight, (mean, covariance) in zip(PI_ROW, components)
    )


def grid(n: int = 421, half: float = 4.0) -> tuple[np.ndarray, float]:
    axis = np.linspace(-half, half, n)
    points = np.stack(np.meshgrid(axis, axis, indexing="ij"), axis=-1)
    return points, (2 * half / (n - 1)) ** 2


def mass_check(theta: float) -> float:
    points, cell = grid()
    return float(record_pdf(points, theta).sum() * cell)


def total_variation(theta_a: float, theta_b: float, gauge_a: float = 0.0) -> float:
    """Grid quadrature diagnostic; never used as a proof of orbit separation."""
    points, cell = grid()
    density_a = record_pdf(points, theta_a, gauge_i=gauge_a)
    density_b = record_pdf(points, theta_b)
    return float(0.5 * np.abs(density_a - density_b).sum() * cell)


def check1() -> dict[str, float]:
    print("=" * 78)
    print("CHECK 1 -- exact record-moment separation and exact gauge equivalences")
    print("=" * 78)
    rows = []
    for theta in (0.0, np.pi / 8, np.pi / 4, np.pi / 2, np.pi, 3 * np.pi / 2, TWO_PI):
        rows.append((theta, record_mean_norm_sq(theta), float(np.trace(mixture_moments(record_law_components(theta))[1]))))
    print("   Theta      ||E[O]||^2       tr Cov(O)")
    for theta, moment, covariance_trace in rows:
        print(f"   {theta:7.4f}     {moment:12.10f}     {covariance_trace:12.10f}")

    statistic_zero = record_mean_norm_sq(0.0)
    statistic_quarter_turn = record_mean_norm_sq(np.pi / 2)
    periodic_error = periodic_aligned_component_error(0.0, turns=1)
    mirror_error = mirror_aligned_component_error(np.pi / 3)
    raw_tv = total_variation(np.pi / 2, 0.0)
    assert abs(statistic_zero - 1.0) < 1e-12
    assert abs(statistic_quarter_turn - 0.5) < 1e-12
    assert periodic_error < 1e-12
    assert mirror_error < 1e-12
    print(f"  exact separator gap S(0)-S(pi/2) = {statistic_zero-statistic_quarter_turn:.12f}")
    print(f"  exact periodic component error    = {periodic_error:.3e}")
    print(f"  exact mirror component error      = {mirror_error:.3e}")
    print(f"  raw TV diagnostic (not a proof)   = {raw_tv:.10f}")
    print("  PASS")
    return {
        "record_moment_theta_0": statistic_zero,
        "record_moment_theta_pi_over_2": statistic_quarter_turn,
        "record_moment_gap": statistic_zero - statistic_quarter_turn,
        "periodic_component_error": periodic_error,
        "mirror_component_error": mirror_error,
        "raw_tv_diagnostic": raw_tv,
    }


def check2() -> dict[str, float]:
    print("\n" + "=" * 78)
    print("CHECK 2 -- passive gauge invariance of record moments and relational KL")
    print("=" * 78)
    rng = np.random.default_rng(20260812)
    theta = np.pi / 2
    reference_moment = record_mean_norm_sq(theta)
    worst_moment = 0.0
    worst_kl = 0.0
    for _ in range(200):
        gauge_i, gauge_j = rng.uniform(0.0, TWO_PI, size=2)
        mean, _ = mixture_moments(record_law_components(theta, gauge_i, gauge_j))
        worst_moment = max(worst_moment, abs(float(mean @ mean) - reference_moment))
        q_i = push(gauge_i, np.array([0.3, 0.9]), np.diag([0.30, 0.45]))
        q_reference = (np.array([0.3, 0.9]), np.diag([0.30, 0.45]))
        for transformed, reference in zip(source_laws(theta, gauge_i, gauge_j), source_laws(theta)):
            worst_kl = max(
                worst_kl,
                abs(kl_gauss(*q_i, *transformed) - kl_gauss(*q_reference, *reference)),
            )
    assert worst_moment < 1e-12
    assert worst_kl < 1e-12
    print(f"  max record-moment drift = {worst_moment:.3e}")
    print(f"  max relational-KL drift = {worst_kl:.3e}")
    print("  PASS")
    return {"record_moment_gauge_drift": worst_moment, "relational_kl_gauge_drift": worst_kl}


def check3() -> dict[str, float]:
    print("\n" + "=" * 78)
    print("CHECK 3 -- exact coboundary control and executable flat-twist counterpresentation")
    print("=" * 78)
    coboundary_error = max(
        coboundary_aligned_component_error(theta)
        for theta in (0.0, np.pi / 4, np.pi / 2, np.pi)
    )
    flat_twist_error = 0.0
    for theta in (0.0, np.pi / 4, np.pi / 2, np.pi):
        flat_twist_error = max(
            flat_twist_error,
            _component_error(record_law_components(theta), flat_twist_record_law_components(theta)),
        )
    assert coboundary_error < 1e-12
    assert flat_twist_error < 1e-12
    print(f"  exact coboundary alignment error = {coboundary_error:.3e}")
    print(f"  flat-twist reproduction error    = {flat_twist_error:.3e}")
    print("  PASS -- the constrained curve family is monodromy-sensitive, but the")
    print("          same record law has a zero-connection, explicit-twist presentation.")
    return {
        "coboundary_component_error": coboundary_error,
        "flat_twist_component_error": flat_twist_error,
    }


def check4() -> dict[str, float]:
    print("\n" + "=" * 78)
    print("CHECK 4 -- finite-mixture KL identity after curve transport")
    print("=" * 78)
    theta = np.pi / 2
    q_i = (np.array([0.3, 0.9]), np.diag([0.30, 0.45]))
    beta = np.array([0.7, 0.3])
    sources = source_laws(theta)
    rhs = float(np.sum(beta * np.log(beta / PI_ROW)))
    rhs += sum(weight * kl_gauss(*q_i, mean, covariance) for weight, (mean, covariance) in zip(beta, sources))

    points, cell = grid(n=801, half=8.0)
    q_density = gauss_pdf(points, *q_i)
    lhs = 0.0
    for weight, prior_weight, (mean, covariance) in zip(beta, PI_ROW, sources):
        source_density = gauss_pdf(points, mean, covariance)
        integrand = weight * q_density * (
            np.log(weight * q_density) - np.log(prior_weight * source_density)
        )
        lhs += float(integrand.sum() * cell)
    residual = abs(lhs - rhs)
    assert residual < 1e-6
    print(f"  LHS = {lhs:.12f}")
    print(f"  RHS = {rhs:.12f}")
    print(f"  residual = {residual:.3e}")
    print("  PASS")
    return {"lhs": lhs, "rhs": rhs, "residual": residual}


def run_checks() -> dict[str, object]:
    return {
        "schema_version": "u1-two-path-witness/v2",
        "check1_record_separation": check1(),
        "check2_gauge_invariance": check2(),
        "check3_controls": check3(),
        "check4_elbo_identity": check4(),
        "scope": {
            "base": "S1",
            "group": "U(1)",
            "curvature_tested": False,
            "bundle_topology_tested": False,
            "connection_identified_from_records": False,
            "live_source_law": False,
        },
    }


def main() -> None:
    result = run_checks()
    print("\n" + "=" * 78)
    print("RESULT JSON")
    print("=" * 78)
    print(json.dumps(result, indent=2, sort_keys=True))
    print("\nCONCLUSION")
    print("  Exact record moments distinguish the selected monodromies within the declared")
    print("  curve-transport model. Exact gauges establish periodic, mirror, and coboundary")
    print("  equivalences. The executable flat-twist control shows that records do not identify")
    print("  the connection origin across broader generative presentations. No claim is made")
    print("  about curvature, bundle topology, nonabelian groups, or live recognition sources.")


if __name__ == "__main__":
    main()
