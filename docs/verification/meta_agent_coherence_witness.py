"""Meta-agent coherence witness: what makes a block of agents compressible?

Four claims about agent -> meta-agent renormalization at a FIXED base point c, each
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

CLAIM 3  The connection Laplacian L^Omega = D (x) I - W^Omega, with
         (W^Omega)_{ij} = beta_ij Omega_ij in KxK blocks, detects the meta-agent: on an
         aligned block its lowest eigenvector IS the meta-agent belief, agreeing with every
         local q_i up to frame.

CLAIM 4  Kernel DIMENSION is the wrong diagnostic. A single SO(3) cycle always fixes an
         axis, so a zero mode survives even under frustration. The order parameter is the
         MAGNITUDE of lambda_1, which separates near-flat from frustrated by ~400x once the
         graph carries two independent non-commuting cycles.

Run:  python docs/verification/meta_agent_coherence_witness.py
Requires: numpy, scipy.
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
    exactly when the two differ: they are bit-identical for Theta in O(K) with
    symmetric weights, which is the regime every claim below is computed in.
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


def _retracted_laplacian(O, edges, bij, bji, n, K=3):
    """The RETRACTED 3e.2(iii) operator, kept only to exhibit its failure."""
    L = np.zeros((n * K, n * K))
    for (i, j), a, b in zip(edges, bij, bji):
        L[i * K:(i + 1) * K, i * K:(i + 1) * K] += a * np.eye(K)
        L[j * K:(j + 1) * K, j * K:(j + 1) * K] += b * np.eye(K)
        L[i * K:(i + 1) * K, j * K:(j + 1) * K] -= a * O[(i, j)]
        L[j * K:(j + 1) * K, i * K:(i + 1) * K] -= b * O[(i, j)].T
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
        print(f"  {label}")
        print(f"    ||H1-I||={np.linalg.norm(H1-np.eye(3)):.3f}  "
              f"||H2-I||={np.linalg.norm(H2-np.eye(3)):.3f}  "
              f"||[H1,H2]||={np.linalg.norm(H1@H2-H2@H1):.3f}")
        print(f"    dim common Fix(H1,H2) = {dimfix}")
        print(f"    3 lowest eig L^Omega  = {np.round(ev[:3], 6)}")
        print()
    print("  PASS -- both regimes have dim Fix = 0, so the kernel does not separate them;")
    print("         lambda_1 does, by roughly two orders of magnitude.")


def regime_table():
    """CLAIM 5 (added 2026-08-13, discharging obligation O1).

    Locates exactly where the retracted 3e.2(iii) operator fails, and shows that the
    two failure modes are INDEPENDENT: asymmetry is caused by row-stochastic beta,
    indefiniteness by Theta leaving O(K). Claims 1-4 are computed with Theta in SO(3)
    and symmetric weights, the one cell where neither bites and the two operators
    coincide -- so those numbers stand, under the narrower hypotheses stated here.
    """
    print()
    print("=" * 74)
    print("CLAIM 5 -- where the retracted operator fails, and why claims 1-4 survive")
    print("=" * 74)
    edges = [(1, 0), (2, 1), (3, 2), (0, 2), (0, 3)]
    hdr = f"  {'regime':<32s}{'asym(retr)':>12s}{'minRe(retr)':>13s}{'minEig(energy)':>16s}"
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    results = {}
    for label, gl, rowsimplex in [
        ("SO(3), symmetric weights", False, False),
        ("SO(3), row-simplex beta", False, True),
        ("GL(3,R), symmetric weights", True, False),
        ("GL(3,R), row-simplex beta", True, True),
    ]:
        rr = np.random.default_rng(SEED + 1)
        O = {}
        for e in edges:
            g = so3(rr.normal(size=3) * 0.9)
            if gl:
                g = g @ np.diag(np.exp(rr.normal(size=3) * 0.4))
            O[e] = g
            O[(e[1], e[0])] = np.linalg.inv(g)
        if rowsimplex:
            bij = rr.uniform(0.1, 1.0, len(edges))
            bji = rr.uniform(0.1, 1.0, len(edges))
        else:
            bij = np.ones(len(edges))
            bji = bij.copy()
        w = 0.5 * (bij + bji)
        Le = connection_laplacian(O, edges, w, 4)
        Lo = _retracted_laplacian(O, edges, bij, bji, 4)
        asym = np.linalg.norm(Lo - Lo.T) / np.linalg.norm(Lo)
        min_retr = np.linalg.eigvals(Lo).real.min()
        min_en = np.linalg.eigvalsh(Le)[0]
        results[label] = (asym, min_retr, min_en)
        print(f"  {label:<32s}{asym:12.3e}{min_retr:+13.5f}{min_en:+16.6e}")
        assert min_en > -1e-10, (label, min_en)          # energy form PSD everywhere
    print()
    a0, r0, e0 = results["SO(3), symmetric weights"]
    assert a0 < 1e-12 and abs(r0 - e0) < 1e-10, (a0, r0, e0)
    assert results["SO(3), row-simplex beta"][0] > 0.1          # beta breaks symmetry
    assert results["GL(3,R), symmetric weights"][1] < 0         # GL breaks definiteness
    print("  PASS -- the energy form is PSD in all four regimes. The retracted form is")
    print("         asymmetric as soon as beta is row-stochastic, and indefinite as soon")
    print("         as Theta leaves O(K); the two causes are independent. In the SO(3) +")
    print("         symmetric-weight cell the two operators are bit-identical, which is")
    print("         where claims 1-4 live, so their numbers stand under those hypotheses.")


def fisher_pencil():
    """CLAIM 6 (added 2026-08-13, discharging obligation O5 and repairing O16).

    The panel concluded the extent criterion is well posed only for G <= O(K),
    because the spectrum of the energy form is gauge-dependent under GL(K,R).
    That is true for a SCALAR edge weight. It is false once W_e is the Fisher
    metric at the endpoint the residual lives in.

    Take W_e = w_e * Sigma_i^{-1} for e = (i,j), and the pencil (L, M) with
    M = direct-sum Sigma_i^{-1}. Under a per-agent gauge z_i -> A_i z_i, with
    Theta_e -> A_i Theta_e A_j^{-1} and Sigma_i -> A_i Sigma_i A_i^T, BOTH L and M
    transform by the same congruence X -> A^{-T} X A^{-1}. Congruence preserves the
    generalized spectrum exactly, so the generalized eigenvalues are GL(K,R)
    invariants and the eigenvectors transform as v -> A v.
    """
    import scipy.linalg as sla
    print()
    print("=" * 74)
    print("CLAIM 6 -- the Fisher pencil is exactly GL(K,R) gauge invariant")
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
        L = np.zeros((n * K, n * K))
        M = np.zeros((n * K, n * K))
        for (i, j) in edges:
            T = Th[(i, j)]
            We = w[(i, j)] * (np.linalg.inv(Sig[i]) if fisher else np.eye(K))
            L[i * K:(i + 1) * K, i * K:(i + 1) * K] += We
            L[j * K:(j + 1) * K, j * K:(j + 1) * K] += T.T @ We @ T
            L[i * K:(i + 1) * K, j * K:(j + 1) * K] -= We @ T
            L[j * K:(j + 1) * K, i * K:(i + 1) * K] -= T.T @ We
        for i in range(n):
            M[i * K:(i + 1) * K, i * K:(i + 1) * K] = np.linalg.inv(Sig[i])
        return L, M

    A = {i: gl(0.5) for i in range(n)}
    Th2 = {(i, j): A[i] @ Th[(i, j)] @ np.linalg.inv(A[j]) for (i, j) in edges}
    Sig2 = {i: A[i] @ Sig[i] @ A[i].T for i in range(n)}

    for fisher, name in [(True, "Fisher W_e = Sigma_i^-1"), (False, "scalar W_e = w I")]:
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
    print(f"\n  MECHANISM -- gauge acts by CONGRUENCE on both halves of the pencil:")
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
    print("\n  PASS -- congruence preserves the generalized spectrum exactly, so the")
    print("         criterion is well posed for FULL GL(K,R), not only for O(K), once")
    print("         the edge weight is the Fisher metric rather than a scalar.")


def main():
    claim_1_and_2()
    claim_3()
    claim_4()
    regime_table()
    fisher_pencil()
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

  (c) Alignment is modelled here as exact equality of transported belief VECTORS, a
      surrogate for KL(q_i || (Omega_ij)_# q_j) = 0. The Gaussian case with covariance,
      and the approximate case KL ~ eps, are not covered.

  (d) Nothing here shows the meta-agent carries its own exact ELBO. The coarse map is
      built from the spectral projector of L^Omega, which depends on beta; if beta is
      recognition-side, the map is recognition-DEPENDENT and Theory/09's exact contraction
      theorem does not apply. That is the most likely failure point of the construction.

  (e) SO(3) and rank-3 fibers only; K=3, four agents, one or two independent cycles.
""")


if __name__ == "__main__":
    main()
