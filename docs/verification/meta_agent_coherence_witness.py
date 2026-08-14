"""Meta-agent coherence witness: what makes a block of agents compressible?

Seven claim groups about agent -> meta-agent renormalization at a FIXED base point c, each
computed rather than asserted. Every transport here is a VERTICAL / internal fiber map
Omega_ij acting within the fiber over one c; none of this concerns the holonomy of the
principal connection omega on C, which is a different object (see SCOPE at the bottom).

CLAIM 1  Belief alignment does NOT force trivial holonomy. If q_i = (Omega_ij)_# q_j on
         every edge of a loop in the agent graph, the loop holonomy H satisfies only
         H in Stab(q_i). H is generically NOT the identity.

CLAIM 2  H in Stab(q) is nevertheless exactly what makes the coarse-graining well posed:
         two different spanning trees over an aligned block give the SAME compressed
         meta-state. Breaking alignment on one edge restores tree-dependence. This is the
         repair for the standing defect that Theory/07b's compressed meta-state is
         spanning-tree dependent.

CLAIM 3  The symmetric energy-form connection Laplacian detects the meta-agent on the
         aligned SO(3), symmetric-weight control: its lowest eigenvector agrees with every
         local q_i up to frame.

CLAIM 4  Kernel DIMENSION is the wrong diagnostic. A single SO(3) cycle always fixes an
         axis, so a zero mode survives even under frustration. The order parameter is the
         MAGNITUDE of lambda_1, which separates near-flat from frustrated once the
         graph carries two independent non-commuting cycles.

CLAIM 5  The retired non-energy operator is scoped by explicit executable controls.

CLAIM 6  For directed (i,j) = sender j -> receiver i, the exact frozen-beta Gaussian
         mean-sector edge precision is beta_ij(Theta_ij Sigma_j Theta_ij^T)^-1. The
         resulting Hessian is GL-congruence covariant. The local-product Fisher metric
         M = direct-sum Sigma_i^-1 is separately declared as an interim reading metric,
         not as an edge precision or a settled extent criterion.

CLAIM 7  Edge dropout, prescribed fixed-ambient support decoupling, and active-set
         deletion are distinct. Only the prescribed decoupling has chi_i = 0 together
         with externally zeroed incident effective edge weights; it adds K null modes.

Run:  python docs/verification/meta_agent_coherence_witness.py
Requires: numpy, scipy.
Collected regressions: tests/test_meta_agent_coherence_witness.py
"""

import numpy as np
from scipy.linalg import expm

SEED = 20260813


def so3(v):
    """exp of the so(3) element with axis-angle vector v."""
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return expm(K)


def rot_carrying(a, b):
    """Some rotation R with R a = b, for vectors of equal norm (Rodrigues)."""
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    v = np.cross(a, b)
    s = np.linalg.norm(v)
    c = a @ b
    if s < 1e-12:
        return np.eye(3) if c > 0 else -np.eye(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + K + K @ K * ((1 - c) / s ** 2)


def connection_laplacian(O, edges, beta, n, K=3):
    """Cluster connection Laplacian, `Theory/09` eq:cg-connection-laplacian-energy:

        z^T L z = sum_{e=(i,j) in E} (z_i - Theta_e z_j)^T W_e (z_i - Theta_e z_j),

    assembled with W_e = w_e * I. Symmetric and PSD for ANY Theta_e in GL(K,R),
    because the j-diagonal block is Theta^T W Theta and not W. Its kernel is the
    space of parallel sections, isomorphic to Fix(Hol) by eq:cg-fixed-rank
    (ESTABLISHED).

    Supersedes the operator originally asserted in worklog 3e.2(iii),
    L = D (x) I - W^Omega, which is RETRACTED by 3f.0 R1. See regime_table() for
    the proved identity cell: the two forms are algebraically equal for orthogonal
    reciprocal links with symmetric weights.
    """
    L = np.zeros((n * K, n * K))
    for (i, j), w in zip(edges, beta):
        Th = O[(i, j)]
        We = w * np.eye(K)
        L[i * K:(i + 1) * K, i * K:(i + 1) * K] += We
        L[j * K:(j + 1) * K, j * K:(j + 1) * K] += Th.T @ We @ Th
        L[i * K:(i + 1) * K, j * K:(j + 1) * K] -= We @ Th
        L[j * K:(j + 1) * K, i * K:(i + 1) * K] -= Th.T @ We
    return L
def forward_kl_edge_precision(theta_ij, sigma_j, beta_ij):
    """Mean-sector precision for the directed edge (i, j).

    The orientation is sender j to receiver i:
    Theta_ij: V_j -> V_i and r_ij = mu_i - Theta_ij mu_j. Therefore
    beta_ij KL(q_i || Theta_ij# q_j) has the frozen-covariance mean term

        1/2 r_ij^T W_ij r_ij,
        W_ij = beta_ij (Theta_ij Sigma_j Theta_ij^T)^-1.

    Reversing the KL is a separate directed edge and uses its own sender slot.
    """
    theta_ij = np.asarray(theta_ij, dtype=float)
    sigma_j = np.asarray(sigma_j, dtype=float)
    transported_sender = theta_ij @ sigma_j @ theta_ij.T
    precision = float(beta_ij) * np.linalg.inv(transported_sender)
    return 0.5 * (precision + precision.T)


def assemble_frozen_beta_mean_hessian(
    n,
    K,
    directed_edges,
    theta,
    covariance,
    beta,
    *,
    chi=None,
    alpha=None,
    prior_precision=None,
):
    """Assemble the frozen-beta Gaussian mean-sector Hessian.

    beta[(i, j)] is the effective frozen coefficient of the directed edge
    j -> i. This is not the full Hessian of the reduced attention objective:
    differentiating optimized normalized attention adds response terms. Support
    decoupling on a fixed ambient space likewise requires incident effective edge
    coefficients to be zeroed explicitly; canonical row normalization does not
    provide that limit by itself.

    If supplied, the local prior block is exactly
    chi_i * alpha_i * prior_precision_i.
    """
    hessian = np.zeros((n * K, n * K))
    for i, j in directed_edges:
        transform = np.asarray(theta[(i, j)], dtype=float)
        edge_precision = forward_kl_edge_precision(
            transform,
            covariance[j],
            beta[(i, j)],
        )
        i_slice = slice(i * K, (i + 1) * K)
        j_slice = slice(j * K, (j + 1) * K)
        hessian[i_slice, i_slice] += edge_precision
        hessian[j_slice, j_slice] += transform.T @ edge_precision @ transform
        hessian[i_slice, j_slice] -= edge_precision @ transform
        hessian[j_slice, i_slice] -= transform.T @ edge_precision

    if prior_precision is not None:
        for i in range(n):
            presence = 1.0 if chi is None else float(chi[i])
            prior_weight = 1.0 if alpha is None else float(alpha[i])
            i_slice = slice(i * K, (i + 1) * K)
            hessian[i_slice, i_slice] += (
                presence * prior_weight * np.asarray(prior_precision[i], dtype=float)
            )

    return 0.5 * (hessian + hessian.T)


def local_product_fisher_metric(covariance, n, K):
    """Interim local-product Fisher metric M = direct_sum Sigma_i^-1.

    This separately declared reading metric is not a KL edge precision and does
    not settle the spectral threshold or the meta-agent extent criterion.
    """
    metric = np.zeros((n * K, n * K))
    for i in range(n):
        i_slice = slice(i * K, (i + 1) * K)
        metric[i_slice, i_slice] = np.linalg.inv(covariance[i])
    return 0.5 * (metric + metric.T)


def canonical_normalized_attention_row(
    energies,
    prior,
    *,
    receiver_presence,
    sender_presence,
    temperature=1.0,
):
    """Evaluate the canonical support-weighted normalized receiver row.

    A common positive receiver-presence factor cancels from numerator and
    denominator. At exact zero all row masses and their normalizer vanish, so
    receiver departure is 0/0 rather than a smooth decoupling path.
    """
    if temperature <= 0.0:
        raise ValueError("temperature must be positive")
    energies = np.asarray(energies, dtype=float)
    prior = np.asarray(prior, dtype=float)
    sender_presence = np.asarray(sender_presence, dtype=float)
    logits = -energies / float(temperature)
    stabilized = np.exp(logits - np.max(logits))
    mass = float(receiver_presence) * sender_presence * prior * stabilized
    normalizer = float(np.sum(mass))
    if normalizer <= 0.0:
        raise ValueError("canonical normalized attention is 0/0 at exact zero support")
    return mass / normalizer


def _directed_receiver_row_sums(edges, bij, bji, n):
    """Return directed weight mass in each receiver row.

    For an undirected storage pair (i, j), bij is the directed weight received
    by i from j and bji is received by j from i.
    """
    row_sums = np.zeros(n, dtype=float)
    for (i, j), a, b in zip(edges, bij, bji):
        row_sums[i] += a
        row_sums[j] += b
    return row_sums


def receiver_normalized_directed_weights(edges, raw_bij, raw_bji, n):
    """Normalize actual directed weights over each active receiver row."""
    edges = list(edges)
    raw_bij = np.asarray(raw_bij, dtype=float)
    raw_bji = np.asarray(raw_bji, dtype=float)
    if raw_bij.shape != (len(edges),) or raw_bji.shape != (len(edges),):
        raise ValueError("each stored edge needs one weight in each direction")
    if np.any(raw_bij < 0.0) or np.any(raw_bji < 0.0):
        raise ValueError("directed row masses must be nonnegative")

    raw_row_sums = _directed_receiver_row_sums(edges, raw_bij, raw_bji, n)
    bij = np.array([
        a / raw_row_sums[i] if raw_row_sums[i] > 0.0 else 0.0
        for (i, _), a in zip(edges, raw_bij)
    ])
    bji = np.array([
        b / raw_row_sums[j] if raw_row_sums[j] > 0.0 else 0.0
        for (_, j), b in zip(edges, raw_bji)
    ])
    row_sums = _directed_receiver_row_sums(edges, bij, bji, n)
    active = raw_row_sums > 0.0
    assert np.allclose(row_sums[active], 1.0, atol=1e-14, rtol=0.0)
    return bij, bji, row_sums




def _retracted_laplacian(O, edges, bij, bji, n, K=3):
    """The RETRACTED 3e.2(iii) operator, kept only to exhibit its failure."""
    L = np.zeros((n * K, n * K))
    for (i, j), a, b in zip(edges, bij, bji):
        L[i * K:(i + 1) * K, i * K:(i + 1) * K] += a * np.eye(K)
        L[j * K:(j + 1) * K, j * K:(j + 1) * K] += b * np.eye(K)
        L[i * K:(i + 1) * K, j * K:(j + 1) * K] -= a * O[(i, j)]
        L[j * K:(j + 1) * K, i * K:(i + 1) * K] -= b * O[(j, i)]
    return L


def build_aligned_block(rng, chord_aligned=True):
    """4 agents, tree 0-1-2-3 plus chord (0,2): one independent cycle.

    Beliefs are built so that q_i = Omega_ij q_j holds on every TREE edge by
    construction; the chord is then either made consistent with that alignment or left
    generic.
    """
    O = {}
    for e in [(1, 0), (2, 1), (3, 2)]:
        g = so3(rng.normal(size=3) * 0.8)
        O[e] = g
        O[(e[1], e[0])] = g.T
    q = {0: np.array([1.0, 0.3, -0.5])}
    for i, p in [(1, 0), (2, 1), (3, 2)]:
        q[i] = O[(i, p)] @ q[p]
    O[(0, 2)] = rot_carrying(q[2], q[0]) if chord_aligned else so3(rng.normal(size=3) * 0.8)
    O[(2, 0)] = O[(0, 2)].T
    return O, q


def claim_1_and_2():
    print("=" * 74)
    print("CLAIM 1 -- alignment forces the holonomy into Stab(q), not to the identity")
    print("=" * 74)
    rng = np.random.default_rng(SEED)
    O, q = build_aligned_block(rng, chord_aligned=True)

    print("  edge alignment residuals ||q_i - Omega_ij q_j||:")
    worst_align = 0.0
    for (i, j) in [(1, 0), (2, 1), (3, 2), (0, 2)]:
        r = np.linalg.norm(q[i] - O[(i, j)] @ q[j])
        worst_align = max(worst_align, r)
        print(f"    ({i},{j}) : {r:.3e}")
    assert worst_align < 1e-12, worst_align

    H = O[(0, 2)] @ O[(2, 1)] @ O[(1, 0)]          # loop 0 -> 1 -> 2 -> 0, based at 0
    dev = np.linalg.norm(H - np.eye(3))
    fix = np.linalg.norm(H @ q[0] - q[0])
    print(f"\n  ||H - I||_F      = {dev:.6f}   <- holonomy is NOT trivial")
    print(f"  ||H q_0 - q_0||  = {fix:.3e}   <- but it fixes the aligned belief")
    print(f"  eig(H)           = {np.round(np.linalg.eigvals(H), 4)}")
    assert dev > 1e-3, "holonomy came out trivial; the witness is not exercising the point"
    assert fix < 1e-12, fix

    print()
    print("=" * 74)
    print("CLAIM 2 -- and that is exactly what makes the compression tree-independent")
    print("=" * 74)
    w = np.full(4, 0.25)

    def compress(tau):
        return sum(w[i] * (tau[i] @ q[i]) for i in range(4))

    tau_A = {0: np.eye(3), 1: O[(0, 1)], 2: O[(0, 1)] @ O[(1, 2)],
             3: O[(0, 1)] @ O[(1, 2)] @ O[(2, 3)]}
    tau_B = {0: np.eye(3), 1: O[(0, 1)], 2: O[(0, 2)], 3: O[(0, 2)] @ O[(2, 3)]}
    zA, zB = compress(tau_A), compress(tau_B)
    rel = np.linalg.norm(zA - zB) / np.linalg.norm(zA)
    print(f"  z(tree A) = {np.round(zA, 8)}")
    print(f"  z(tree B) = {np.round(zB, 8)}")
    print(f"  relative discrepancy = {rel:.3e}   <- TREE-INDEPENDENT")
    assert rel < 1e-12, rel

    O2, q2 = build_aligned_block(np.random.default_rng(SEED), chord_aligned=False)
    tau_B2 = {0: np.eye(3), 1: O2[(0, 1)], 2: O2[(0, 2)], 3: O2[(0, 2)] @ O2[(2, 3)]}
    tau_A2 = {0: np.eye(3), 1: O2[(0, 1)], 2: O2[(0, 1)] @ O2[(1, 2)],
              3: O2[(0, 1)] @ O2[(1, 2)] @ O2[(2, 3)]}
    zA2 = sum(w[i] * (tau_A2[i] @ q2[i]) for i in range(4))
    zB2 = sum(w[i] * (tau_B2[i] @ q2[i]) for i in range(4))
    rel2 = np.linalg.norm(zA2 - zB2) / np.linalg.norm(zA2)
    print(f"\n  CONTROL, alignment broken on the single chord edge:")
    print(f"  relative discrepancy = {rel2:.3f}   <- TREE-DEPENDENT again")
    assert rel2 > 0.1, rel2
    print("\n  PASS -- alignment is the condition under which coarse-graining is a")
    print("         function of the gauge orbit at all. This is the repair for the")
    print("         standing tree-dependence defect in Theory/07b.")


def claim_3():
    print()
    print("=" * 74)
    print("CLAIM 3 -- the connection-Laplacian low mode IS the meta-agent belief")
    print("=" * 74)
    rng = np.random.default_rng(SEED)
    O, q = build_aligned_block(rng, chord_aligned=True)
    edges = [(1, 0), (2, 1), (3, 2), (0, 2)]
    L = connection_laplacian(O, edges, [1.0] * 4, 4)
    ev, evec = np.linalg.eigh(L)
    v = evec[:, 0].reshape(4, 3)
    cos = [abs(v[i] @ q[i]) / (np.linalg.norm(v[i]) * np.linalg.norm(q[i])) for i in range(4)]
    print(f"  4 lowest eigenvalues of L^Omega : {np.round(ev[:4], 8)}")
    print(f"  |cos(low mode_i, q_i)| per agent: {np.round(cos, 10)}")
    assert min(cos) > 1 - 1e-8, cos
    print("\n  PASS -- the low mode agrees with every local belief up to frame, i.e. it is")
    print("         the meta-agent belief expressed in each agent's own gauge.")


def claim_4():
    print()
    print("=" * 74)
    print("CLAIM 4 -- kernel DIMENSION is the wrong diagnostic; lambda_1 is the order parameter")
    print("=" * 74)
    print("  A single SO(3) cycle always fixes an axis, so a zero mode survives even under")
    print("  frustration. Two independent NON-COMMUTING cycles are needed to kill it.")
    print()
    edges = [(1, 0), (2, 1), (3, 2), (0, 2), (0, 3)]   # 5 edges, 4 nodes -> 2 cycles
    lowest = {}
    fixed_dimensions = {}
    for label, scale in [("near-flat (coherent block)", 0.02), ("frustrated (generic)", 0.9)]:
        rng = np.random.default_rng(SEED + 1)
        O = {}
        for e in edges:
            g = so3(rng.normal(size=3) * scale)
            O[e] = g
            O[(e[1], e[0])] = g.T
        L = connection_laplacian(O, edges, [1.0] * len(edges), 4)
        ev = np.linalg.eigvalsh(L)
        H1 = O[(0, 2)] @ O[(2, 1)] @ O[(1, 0)]
        H2 = O[(0, 3)] @ O[(3, 2)] @ O[(2, 1)] @ O[(1, 0)]
        M = np.vstack([H1 - np.eye(3), H2 - np.eye(3)])
        dimfix = int(np.sum(np.linalg.svd(M, compute_uv=False) < 1e-8))
        fixed_dimensions[label] = dimfix
        lowest[label] = float(ev[0])
        print(f"  {label}")
        print(f"    ||H1-I||={np.linalg.norm(H1-np.eye(3)):.3f}  "
              f"||H2-I||={np.linalg.norm(H2-np.eye(3)):.3f}  "
              f"||[H1,H2]||={np.linalg.norm(H1@H2-H2@H1):.3f}")
        print(f"    dim common Fix(H1,H2) = {dimfix}")
        print(f"    3 lowest eig L^Omega  = {np.round(ev[:3], 6)}")
        print()
    ratio = lowest["frustrated (generic)"] / lowest["near-flat (coherent block)"]
    assert set(fixed_dimensions.values()) == {0}, fixed_dimensions
    assert ratio > 100.0, ratio
    print("  PASS -- both regimes have dim Fix = 0, so the kernel does not separate them;")
    print(f"         lambda_1 does on this control, by a factor of {ratio:.1f}.")


def regime_table():
    """CLAIM 5 (added 2026-08-13, discharging obligation O1).

    Proves only the exact identity cell: symmetric directed weights together with
    orthogonal reciprocal links make the retired operator equal the energy form.
    Edgewise, both forms then have blocks [[wI, -w Theta],
    [-w Theta^T, wI]], because Theta^T Theta = I and the stored reciprocal
    Theta_ji = Theta_ij^T.
    Values outside that cell are seeded diagnostics, not universal implications.
    Explicit countercontrols rule out universal claims from row-stochasticity alone
    or from a link merely leaving O(K).
    """
    print()
    print("=" * 74)
    print("CLAIM 5 -- exact identity cell and bounded diagnostics")
    print("=" * 74)
    edges = [(1, 0), (2, 1), (3, 2), (0, 2), (0, 3)]
    active_receivers = np.zeros(4, dtype=bool)
    for i, j in edges:
        active_receivers[[i, j]] = True
    hdr = (
        f"  {'regime':<38s}{'asym(retr)':>12s}{'minRe(retr)':>13s}"
        f"{'minEig(energy)':>16s}{'rowErr':>11s}"
    )
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    results = {}
    for label, gl, receiver_rows in [
        ("SO(3), symmetric weights", False, False),
        ("SO(3), receiver-normalized rows", False, True),
        ("GL(3,R), symmetric weights", True, False),
        ("GL(3,R), receiver-normalized rows", True, True),
    ]:
        rr = np.random.default_rng(SEED + 1)
        O = {}
        for e in edges:
            g = so3(rr.normal(size=3) * 0.9)
            if gl:
                g = g @ np.diag(np.exp(rr.normal(size=3) * 0.4))
            O[e] = g
            O[(e[1], e[0])] = np.linalg.inv(g)
        if receiver_rows:
            raw_bij = rr.uniform(0.1, 1.0, len(edges))
            raw_bji = rr.uniform(0.1, 1.0, len(edges))
            bij, bji, row_sums = receiver_normalized_directed_weights(
                edges, raw_bij, raw_bji, n=4
            )
            assert np.allclose(
                row_sums[active_receivers], 1.0, atol=1e-14, rtol=0.0
            )
            row_error = np.max(np.abs(row_sums[active_receivers] - 1.0))
        else:
            bij = np.ones(len(edges))
            bji = bij.copy()
            row_error = None
        w = 0.5 * (bij + bji)
        Le = connection_laplacian(O, edges, w, 4)
        Lo = _retracted_laplacian(O, edges, bij, bji, 4)
        asym = np.linalg.norm(Lo - Lo.T) / np.linalg.norm(Lo)
        min_retr = np.linalg.eigvals(Lo).real.min()
        min_en = np.linalg.eigvalsh(Le)[0]
        form_gap = np.linalg.norm(Lo - Le) / max(np.linalg.norm(Le), 1.0)
        results[label] = {
            "asymmetry": asym,
            "min_real": min_retr,
            "energy_minimum": min_en,
            "form_gap": form_gap,
        }
        row_display = "-" if row_error is None else f"{row_error:.1e}"
        print(
            f"  {label:<38s}{asym:12.3e}{min_retr:+13.5f}"
            f"{min_en:+16.6e}{row_display:>11s}"
        )
        assert min_en > -1e-10, (label, min_en)
    exact = results["SO(3), symmetric weights"]
    assert exact["asymmetry"] < 1e-12, exact
    assert exact["form_gap"] < 1e-12, exact

    nonorthogonal = np.diag([2.0, 0.5])
    nonorthogonal_reverse = np.linalg.inv(nonorthogonal)
    nonorthogonal_retired = _retracted_laplacian(
        {(0, 1): nonorthogonal, (1, 0): nonorthogonal_reverse},
        [(0, 1)],
        np.ones(1),
        np.ones(1),
        n=2,
        K=2,
    )
    nonorthogonal_spectrum = np.linalg.eigvals(nonorthogonal_retired)
    nonorthogonal_residual = np.linalg.norm(
        nonorthogonal.T @ nonorthogonal - np.eye(2)
    )
    assert nonorthogonal_residual > 1.0
    assert np.max(np.abs(nonorthogonal_spectrum.imag)) < 1e-12
    assert nonorthogonal_spectrum.real.min() >= -1e-12

    control_edges = [(0, 1), (1, 2), (2, 0)]
    control_bij, control_bji, control_rows = receiver_normalized_directed_weights(
        control_edges, np.ones(3), np.ones(3), n=3
    )
    identity_links = {}
    for edge in control_edges:
        identity_links[edge] = np.eye(2)
        identity_links[(edge[1], edge[0])] = np.eye(2)
    row_stochastic_retired = _retracted_laplacian(
        identity_links, control_edges, control_bij, control_bji, n=3, K=2
    )
    row_stochastic_asymmetry = np.linalg.norm(
        row_stochastic_retired - row_stochastic_retired.T
    )
    assert np.allclose(control_rows, 1.0, atol=1e-14, rtol=0.0)
    assert row_stochastic_asymmetry < 1e-12

    print()
    print("  PASS -- the energy-form PSD theorem is retained in every seeded regime.")
    print("         Symmetric weights plus orthogonal reciprocal links give the exact")
    print("         algebraic identity between the retired operator and the energy form.")
    print(
        "  DIAGNOSTIC -- seeded diagnostics outside the identity cell are not "
        "universal implications."
    )
    print(
        "  COUNTERCONTROL -- nonorthogonal reciprocal countercontrol: "
        f"orthogonality residual={nonorthogonal_residual:.3e}, "
        f"min real spectrum={nonorthogonal_spectrum.real.min():+.3e}."
    )
    print(
        "  COUNTERCONTROL -- symmetric row-stochastic countercontrol: "
        f"max row error={np.max(np.abs(control_rows - 1.0)):.3e}, "
        f"asymmetry={row_stochastic_asymmetry:.3e}."
    )


def fisher_pencil():
    """CLAIM 6: the directed forward-KL frozen-beta mean Hessian.

    Orientation (i,j) means sender j -> receiver i, Theta_ij: V_j -> V_i,
    and r_ij = mu_i - Theta_ij mu_j. Reverse KL is a second directed edge.
    The local-product Fisher metric M is displayed only as a separately declared
    interim reading metric; this computation does not settle the extent threshold.
    """
    import scipy.linalg as sla
    print()
    print("=" * 74)
    print("CLAIM 6 -- directed forward-KL frozen-beta mean Hessian")
    print("=" * 74)
    K, n = 3, 4
    edges = [(1, 0), (2, 1), (3, 2), (0, 2), (0, 3)]
    rng = np.random.default_rng(SEED)

    def gl(s=0.5):
        return expm(rng.normal(size=(K, K)) * s)

    def spd(s=0.4):
        A = gl(s)
        return A @ A.T

    Th = {e: gl(0.6) for e in edges}
    Sig = {i: spd() for i in range(n)}
    w = {e: rng.uniform(0.4, 1.4) for e in edges}

    def assemble(Th, Sig, fisher=True):
        if fisher:
            L = assemble_frozen_beta_mean_hessian(n, K, edges, Th, Sig, w)
        else:
            L = connection_laplacian(Th, edges, [w[e] for e in edges], n, K)
        M = local_product_fisher_metric(Sig, n, K)
        return L, M

    A = {i: gl(0.5) for i in range(n)}
    Th2 = {(i, j): A[i] @ Th[(i, j)] @ np.linalg.inv(A[j]) for (i, j) in edges}
    Sig2 = {i: A[i] @ Sig[i] @ A[i].T for i in range(n)}

    for fisher, name in [(True, "forward-KL sender slot"), (False, "scalar W_e = w I")]:
        L, M = assemble(Th, Sig, fisher)
        L2, M2 = assemble(Th2, Sig2, fisher)
        ev = sla.eigh(L, M, eigvals_only=True)
        ev2 = sla.eigh(L2, M2, eigvals_only=True)
        drift = np.max(np.abs(ev - ev2)) / max(1.0, np.max(np.abs(ev)))
        print(f"  {name:26s} min eig {ev[0]:+.4e}   GL(3) spectral drift {drift:.3e}")
        if fisher:
            assert drift < 1e-10, drift
        else:
            assert drift > 1e-2, drift

    Ab = np.zeros((n * K, n * K))
    for i in range(n):
        Ab[i * K:(i + 1) * K, i * K:(i + 1) * K] = A[i]
    Abi = np.linalg.inv(Ab)
    L, M = assemble(Th, Sig, True)
    L2, M2 = assemble(Th2, Sig2, True)
    rL = np.linalg.norm(L2 - Abi.T @ L @ Abi) / np.linalg.norm(L2)
    rM = np.linalg.norm(M2 - Abi.T @ M @ Abi) / np.linalg.norm(M2)
    print("\n  MECHANISM -- H and the separately declared interim M transform by congruence:")
    print(f"    ||L' - A^-T L A^-1|| / ||L'|| = {rL:.3e}")
    print(f"    ||M' - A^-T M A^-1|| / ||M'|| = {rM:.3e}")
    assert rL < 1e-10 and rM < 1e-10
    ev, V = sla.eigh(L, M)
    ev2, V2 = sla.eigh(L2, M2)
    pred = Ab @ V[:, 0]
    pred /= np.linalg.norm(pred)
    cos = abs(pred @ (V2[:, 0] / np.linalg.norm(V2[:, 0])))
    print(f"    eigenvector transforms as v -> A v:  |cos| = {cos:.12f}")
    assert cos > 1 - 1e-8, cos
    theta_control = np.diag([2.0, 3.0])
    sender_sigma = np.diag([5.0, 7.0])
    receiver_sigma = np.diag([1.0, 4.0])
    beta_control = 0.7
    forward = forward_kl_edge_precision(theta_control, sender_sigma, beta_control)
    receiver_slot = beta_control * np.linalg.inv(receiver_sigma)
    reverse = forward_kl_edge_precision(
        np.linalg.inv(theta_control), receiver_sigma, 0.9
    )
    matched_receiver_sigma = theta_control @ sender_sigma @ theta_control.T
    slot_control = np.linalg.norm(
        forward - beta_control * np.linalg.inv(matched_receiver_sigma)
    )
    print("\n  orientation: (i,j) means sender j -> receiver i")
    print("  W_ij = beta_ij (Theta_ij Sigma_j Theta_ij^T)^-1")
    print(f"  unequal-slot difference = {np.linalg.norm(forward-receiver_slot):.3e}")
    print(f"  transported-covariance slot control = {slot_control:.3e}")
    print(f"  reverse directed-edge difference = {np.linalg.norm(forward-reverse):.3e}")
    assert np.linalg.norm(forward - receiver_slot) > 1e-2
    assert slot_control < 1e-12
    assert np.linalg.norm(forward - reverse) > 1e-2
    print("\n  PASS -- the directed forward-KL frozen-beta mean Hessian uses the")
    print("         transported sender slot and is GL-congruence covariant.")
    print("  COLLECTED -- the finite-difference Hessian is checked in")
    print("         tests/test_meta_agent_coherence_witness.py.")
    print("  OPEN -- M is only an interim local-product Fisher reading metric; the")
    print("         normalized-row response, threshold, and extent criterion remain open.")


def support_boundary():
    """CLAIM 7: separate edge dropout, fixed-ambient decoupling, and deletion.

    Local priors contribute chi_i alpha_i Lambda_{p,i}. Canonical normalized
    attention does not itself define receiver departure: chi_i cancels for chi_i>0
    and gives a 0/0 row at chi_i=0. Fixed-ambient decoupling below is therefore a
    prescribed operation with externally zeroed incident effective weights.
    """
    print()
    print("=" * 74)
    print("CLAIM 7 -- three distinct support operations")
    print("=" * 74)
    K, n = 3, 5
    core = [(1, 0), (2, 1), (0, 2)]
    edges = core + [(3, 0), (4, 3)]          # agent 4 departs
    rp = np.random.default_rng(SEED)

    def spd(s=0.5):
        A = expm(rp.normal(size=(K, K)) * s)
        return A @ A.T


    prior = {i: spd() for i in range(n)}
    covariance = {i: spd() for i in range(n)}
    alpha = {i: 0.2 + 0.05 * i for i in range(n)}
    present = {i: 1.0 for i in range(n)}
    rr = np.random.default_rng(SEED + 7)
    Th = {e: so3(rr.normal(size=3) * 0.8) for e in edges}
    effective_beta = {e: 1.0 for e in edges}
    effective_beta[(4, 3)] = 0.0

    edge_dropout = assemble_frozen_beta_mean_hessian(
        n, K, edges, Th, covariance, effective_beta,
        chi=present, alpha=alpha, prior_precision=prior,
    )
    dropout_floor = float(np.linalg.eigvalsh(edge_dropout)[0])

    departed = dict(present)
    departed[4] = 0.0
    fixed_ambient = assemble_frozen_beta_mean_hessian(
        n, K, edges, Th, covariance, effective_beta,
        chi=departed, alpha=alpha, prior_precision=prior,
    )
    ambient_eigenvalues = np.linalg.eigvalsh(fixed_ambient)
    zero_modes = int(np.sum(np.abs(ambient_eigenvalues) < 1e-10))

    retained_edges = [edge for edge in edges if 4 not in edge]
    retained = assemble_frozen_beta_mean_hessian(
        n - 1,
        K,
        retained_edges,
        {edge: Th[edge] for edge in retained_edges},
        {i: covariance[i] for i in range(n - 1)},
        {edge: effective_beta[edge] for edge in retained_edges},
        chi={i: present[i] for i in range(n - 1)},
        alpha={i: alpha[i] for i in range(n - 1)},
        prior_precision={i: prior[i] for i in range(n - 1)},
    )
    principal_residual = np.linalg.norm(
        retained - fixed_ambient[: (n - 1) * K, : (n - 1) * K]
    )

    energies = np.array([0.2, 0.8])
    attention_prior = np.array([2.0, 1.0])
    sender_presence = np.array([1.0, 0.5])
    row_present = canonical_normalized_attention_row(
        energies, attention_prior, receiver_presence=1.0, sender_presence=sender_presence
    )
    row_near_zero = canonical_normalized_attention_row(
        energies, attention_prior, receiver_presence=1e-12, sender_presence=sender_presence
    )
    exact_zero_is_undefined = False
    try:
        canonical_normalized_attention_row(
            energies, attention_prior, receiver_presence=0.0, sender_presence=sender_presence
        )
    except ValueError:
        exact_zero_is_undefined = True

    print(f"  edge dropout, chi_4=1: prior floor lambda_min = {dropout_floor:.6f}")
    print(f"  prescribed fixed-ambient decoupling, chi_4=0: zero modes = {zero_modes}")
    print(f"  active-set deletion/principal-submatrix residual = {principal_residual:.3e}")
    print(f"  normalized row drift for chi_receiver 1 -> 1e-12 = "
          f"{np.linalg.norm(row_present-row_near_zero):.3e}")
    print("  normalized row at chi_receiver=0: 0/0 (undefined)")
    assert dropout_floor > 1e-6
    assert zero_modes == K
    assert principal_residual < 1e-12
    assert np.linalg.norm(row_present - row_near_zero) < 1e-12
    assert exact_zero_is_undefined
    print("\n  PASS -- the three prescribed operations have the stated distinct spectra.")
    print("  OPEN -- canonical normalized attention supplies no smooth")
    print("         decoupling/departure-to-zero path for the receiver; at exact chi=0")
    print("         the row is 0/0 and needs an extension convention.")


def main():
    claim_1_and_2()
    claim_3()
    claim_4()
    regime_table()
    fisher_pencil()
    support_boundary()
    print()
    print("=" * 74)
    print("SCOPE -- what this does NOT establish")
    print("=" * 74)
    print("""
  (a) Every transport here is VERTICAL: a fiber map within the fiber over one base point
      c. The holonomy computed is the AGENT-GRAPH holonomy, not the holonomy of the
      principal connection omega on C. B4 concerns the latter and does not bite on the
      former, because Omega_ij appears directly inside the transported KL coupling and
      inside the tied-replica source u_ab = (Omega_ab)_# q_b -- the graph transports ARE
      arguments of generative kernels.

  (b) Agents are SECTIONS with supports C_i, so a meta-agent has extent over C and this
      point-wise witness says nothing about it. The extent criterion is under
      investigation; the working hypothesis is a spectral gap plus an adiabatic bound
      ||Q D^omega P|| << gap, with gap closings as the merge/split events.

  (c) Claims 1-4 model exact transported belief VECTORS. Claim 6 covers only the
      Gaussian frozen-covariance MEAN sector. Covariance variation, optimized-beta
      response terms, and approximate alignment KL ~ eps are not covered.

  (d) Nothing here shows the meta-agent carries its own exact ELBO. The coarse map is
      built from the spectral projector of L^Omega, which depends on beta; if beta is
      recognition-side, the map is recognition-DEPENDENT and Theory/09's exact contraction
      theorem does not apply. That is the most likely failure point of the construction.

  (e) These are finite toy controls. Claims 1-4 use SO(3); Claim 5 includes seeded
      SO(3)/GL(3,R) diagnostics and countercontrols, while Claim 6 exercises GL(3,R).
      None establishes a universal threshold or an extent theorem.
""")


if __name__ == "__main__":
    main()
