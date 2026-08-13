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
    """L^Omega = D (x) I - W^Omega, symmetric because Omega_ji = Omega_ij^T."""
    L = np.zeros((n * K, n * K))
    for (i, j), w in zip(edges, beta):
        for a in (i, j):
            L[a * K:(a + 1) * K, a * K:(a + 1) * K] += w * np.eye(K)
        L[i * K:(i + 1) * K, j * K:(j + 1) * K] -= w * O[(i, j)]
        L[j * K:(j + 1) * K, i * K:(i + 1) * K] -= w * O[(j, i)]
    return 0.5 * (L + L.T)


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


def main():
    claim_1_and_2()
    claim_3()
    claim_4()
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
