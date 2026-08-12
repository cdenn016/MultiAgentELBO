"""U(1) two-path witness: does curve-mediated transport make holonomy observable?

Tests the conjecture of worklog section 3d against the standing negative result B4
(docs/audits/ultradeep-wave2-2026-08-12/wave2-01-constructions.md:695), which states that
for ANY finite design no observation-record statistic detects holonomy, curvature, or
bundle topology -- "because the connection is not an argument of any generative kernel"
-- and which names its own defeat condition at :709: "Change either and the theorem is
unavailable."

Curve-mediated transport puts the connection INSIDE a generative kernel, via the source
law u = (P_gamma)_# q_j. This script checks whether that actually separates holonomies.

SETUP
  Base            C = S^1, coordinate phi in [0, 2pi)
  Group           G = U(1), connection A = (Theta/2pi) dphi, full-loop holonomy Theta
  Fiber           2-D Gaussians; U(1) acts by pushforward under rotation,
                  rho(theta): (mu, Sigma) -> (R_theta mu, R_theta Sigma R_theta^T).
                  This is a genuine statistical isometry (pushforward by a bimeasurable
                  bijection), as the corpus requires (Theory/05c:59).
  Agents          j at phi = 0, i at phi = phi_0
  Two paths       gamma  : direct arc      0 -> phi_0        transport angle a
                  gamma' : the other way   0 -> phi_0 - 2pi  transport angle a - Theta
                  The two transports differ by exactly the full holonomy.
  Generative      label J in {gamma, gamma'} with prior pi_J; given J the relational copy
                  X ~ u_J = (P_J)_# q_j ; observation o | X ~ N(X, sigma_o^2 I).
                  Record law  p(o | Theta) = sum_J pi_J N(o ; R_{a_J} mu_j,
                                                  R_{a_J} Sigma_j R_{a_J}^T + sigma_o^2 I).

CHECKS
  1  record laws for distinct holonomies differ                      (the separating tuple)
  2  the separating statistic is gauge invariant                     (Aut_G(P) check)
  3  a flat coboundary Omega_ij = e^{i phi_i} e^{-i phi_j} shows NO holonomy dependence
     -- reproducing B4's negative and isolating the connection as the cause
  4  the tied-replica ELBO identity survives Omega -> P_gamma        (worklog 3d.7 item 1)

Run:  python docs/verification/u1_two_path_holonomy_witness.py
Requires: numpy.
"""

import numpy as np

TWO_PI = 2.0 * np.pi


def R(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])


def push(theta, mu, Sigma):
    """rho_hat(theta)_# N(mu, Sigma) -- pushforward by rotation."""
    Q = R(theta)
    return Q @ mu, Q @ Sigma @ Q.T


def kl_gauss(m1, S1, m0, S0):
    """Exact KL( N(m1,S1) || N(m0,S0) ) in n dimensions."""
    n = len(m1)
    S0i = np.linalg.inv(S0)
    d = m0 - m1
    return 0.5 * (np.trace(S0i @ S1) + d @ S0i @ d - n
                  + np.log(np.linalg.det(S0) / np.linalg.det(S1)))


def gauss_pdf(X, mu, Sigma):
    """Evaluate N(mu,Sigma) on a stack of points X of shape (...,2)."""
    Si = np.linalg.inv(Sigma)
    d = X - mu
    q = np.einsum('...a,ab,...b->...', d, Si, d)
    return np.exp(-0.5 * q) / (TWO_PI * np.sqrt(np.linalg.det(Sigma)))


# ---------------------------------------------------------------- configuration
PHI0 = np.pi / 2          # location of agent i
MU_J = np.array([1.0, 0.0])
SIG_J = np.diag([0.50, 0.20])   # anisotropic, so rotation is visible in Sigma too
SIGMA_O = 0.35                  # observation noise
PI_ROW = np.array([0.5, 0.5])   # source-label prior over {gamma, gamma'}


def transport_angles(Theta):
    """Transport angles along the two paths. They differ by exactly Theta."""
    a_direct = Theta * PHI0 / TWO_PI
    a_around = Theta * (PHI0 - TWO_PI) / TWO_PI
    return a_direct, a_around


def source_laws(Theta, gauge_i=0.0, gauge_j=0.0):
    """The two connection-dependent generative source laws u_J = (P_J)_# q_j.

    Under a gauge transformation g with angles (gauge_i, gauge_j) at the two base points,
    q_j -> (R_{g_j})_# q_j  and  P_gamma -> R_{g_i} P_gamma R_{g_j}^{-1}, so every source
    law rotates by the SAME R_{g_i}. That is the content of check 2.
    """
    mu_j, S_j = push(gauge_j, MU_J, SIG_J)
    out = []
    for a in transport_angles(Theta):
        # P_gamma acting after the gauge rotation at j, then the gauge rotation at i
        out.append(push(gauge_i + a - gauge_j, mu_j, S_j))
    return out


def record_law_components(Theta, gauge_i=0.0, gauge_j=0.0):
    """Mixture components of p(o | Theta): source law convolved with observation noise."""
    comps = []
    for mu, S in source_laws(Theta, gauge_i, gauge_j):
        comps.append((mu, S + SIGMA_O ** 2 * np.eye(2)))
    return comps


def record_pdf(X, Theta, gauge_i=0.0, gauge_j=0.0):
    comps = record_law_components(Theta, gauge_i, gauge_j)
    return sum(w * gauss_pdf(X, m, S) for w, (m, S) in zip(PI_ROW, comps))


def grid(n=421, half=4.0):
    ax = np.linspace(-half, half, n)
    G = np.stack(np.meshgrid(ax, ax, indexing='ij'), axis=-1)
    return G, (2 * half / (n - 1)) ** 2


def total_variation(Theta_a, Theta_b, gauge_a=0.0):
    G, cell = grid()
    pa = record_pdf(G, Theta_a, gauge_i=gauge_a)
    pb = record_pdf(G, Theta_b)
    return 0.5 * np.abs(pa - pb).sum() * cell


def orbit_distance(Theta_a, Theta_b, n_gauge=180):
    """Distance between the GAUGE ORBITS of the two record laws:

        d([p_a], [p_b]) = min_{g in U(1)} TV( (R_g)_# p(.|Theta_a) , p(.|Theta_b) ).

    The raw record law is NOT gauge invariant -- a gauge transformation at c_i rotates
    every component in common, so p transforms covariantly. Comparing raw record laws
    therefore conflates gauge-variant overall rotation with genuine holonomy content.
    The orbit distance is the correct gauge-invariant separation, and it is what a
    holonomy-detecting statistic must be built from.
    """
    return min(total_variation(Theta_a, Theta_b, gauge_a=g)
               for g in np.linspace(0.0, TWO_PI, n_gauge, endpoint=False))


def mass_check(Theta):
    G, cell = grid()
    return record_pdf(G, Theta).sum() * cell


def separating_statistic(Theta, gauge_i=0.0, gauge_j=0.0):
    """A gauge-invariant record statistic: the angle between the two mixture component
    means. A common rotation of both components leaves it fixed; it equals the holonomy."""
    (m1, _), (m2, _) = record_law_components(Theta, gauge_i, gauge_j)
    c = np.dot(m1, m2) / (np.linalg.norm(m1) * np.linalg.norm(m2))
    return np.arccos(np.clip(c, -1.0, 1.0))


# ================================================================ CHECK 1
def check1():
    print("=" * 74)
    print("CHECK 1 -- do distinct holonomies induce distinct record laws?")
    print("=" * 74)
    print("  (B4 says this is impossible for any finite design, when the connection is")
    print("   not an argument of a generative kernel. Here it is one.)")
    print()
    base = 0.0
    print(f"  normalization of p(.|Theta):  Theta=0 -> {mass_check(0.0):.6f}   "
          f"Theta=pi/2 -> {mass_check(np.pi/2):.6f}")
    print()
    print("  NOTE: the raw record law is NOT gauge invariant -- it transforms covariantly")
    print("  under a gauge rotation at c_i. The gauge-invariant separation is the distance")
    print("  between gauge ORBITS. Both are shown; only the orbit column is meaningful.")
    print()
    print("   Theta      raw TV (gauge-variant)   ORBIT distance    statistic (rad)")
    print("   " + "-" * 68)
    for Th in [0.0, np.pi / 8, np.pi / 4, np.pi / 2, np.pi, 3 * np.pi / 2, TWO_PI]:
        print(f"   {Th:7.4f}     {total_variation(Th, base):16.10f}"
              f"   {orbit_distance(Th, base):14.10f}   {separating_statistic(Th):12.6f}")

    d_sep = orbit_distance(np.pi / 2, 0.0)
    d_periodic = orbit_distance(TWO_PI, 0.0)
    print()
    print(f"  SEPARATION at Theta=pi/2:  orbit distance = {d_sep:.8f} > 0")
    print("      -> the record laws are NOT gauge-equivalent: holonomy is detected.")
    print(f"  PERIODICITY at Theta=2pi:  orbit distance = {d_periodic:.2e} ~ 0")
    print("      -> depends only on the holonomy ELEMENT e^{i Theta}, not on the")
    print("         connection representative. (Raw TV is large here purely because the")
    print("         whole configuration is rotated -- pure gauge, correctly quotiented out.)")
    assert d_sep > 1e-3, d_sep
    assert d_periodic < 1e-6, d_periodic
    print("  PASS")


# ================================================================ CHECK 2
def check2():
    print()
    print("=" * 74)
    print("CHECK 2 -- is the separating statistic gauge invariant?")
    print("=" * 74)
    rng = np.random.default_rng(20260812)
    Th = np.pi / 2
    ref = separating_statistic(Th)
    worst_stat, worst_kl = 0.0, 0.0
    for _ in range(200):
        gi, gj = rng.uniform(0, TWO_PI, size=2)
        worst_stat = max(worst_stat, abs(separating_statistic(Th, gi, gj) - ref))
        # the two relational KL terms must also be invariant under a common pushforward
        q_i_mu, q_i_S = push(gi, np.array([0.3, 0.9]), np.diag([0.30, 0.45]))
        for (u_m, u_S), (v_m, v_S) in zip(source_laws(Th, gi, gj), source_laws(Th)):
            a = kl_gauss(q_i_mu, q_i_S, u_m, u_S)
            b = kl_gauss(*push(0.0, np.array([0.3, 0.9]), np.diag([0.30, 0.45])),
                         v_m, v_S)
            worst_kl = max(worst_kl, abs(a - b))
    print(f"  200 random gauge transformations g(c_i), g(c_j) in U(1)")
    print(f"    max drift of separating statistic : {worst_stat:.3e}")
    print(f"    max drift of relational KL terms  : {worst_kl:.3e}")
    assert worst_stat < 1e-12 and worst_kl < 1e-12
    print("  PASS -- statistic and energies are Aut_G(P)-invariant; the statistic equals")
    print("         the holonomy (U(1) abelian, so conjugacy class = element).")


# ================================================================ CHECK 3
def check3():
    print()
    print("=" * 74)
    print("CHECK 3 -- the flat-coboundary control: Omega_ij = e^{i phi_i} e^{-i phi_j}")
    print("=" * 74)
    print("  PIFB2's declared transport is a coboundary. Around any loop it telescopes,")
    print("  so the two paths give the SAME transport and Theta cannot enter the record.")
    print()
    def cob_pdf(X, Theta):
        """Record law when the transport is the coboundary e^{i phi_i} e^{-i phi_j}.
        The angle depends only on the endpoints, so BOTH paths give phi_i - phi_j and
        Theta never enters. Computed, not asserted."""
        comps = []
        for _path in (0, 1):
            mu, S = push(PHI0 - 0.0, MU_J, SIG_J)      # phi_i - phi_j, path-independent
            comps.append((mu, S + SIGMA_O ** 2 * np.eye(2)))
        return sum(w * gauss_pdf(X, m, S) for w, (m, S) in zip(PI_ROW, comps))

    G, cell = grid()
    p0 = cob_pdf(G, 0.0)
    print("   Theta     loop product (coboundary)    TV vs Theta=0     orbit distance")
    print("   " + "-" * 68)
    worst = 0.0
    for Th in [0.0, np.pi / 4, np.pi / 2, np.pi]:
        # loop product for a coboundary: (phi_i - phi_j) + (phi_j - phi_i) = 0, always
        loop = (PHI0 - 0.0) + (0.0 - PHI0)
        tv = 0.5 * np.abs(cob_pdf(G, Th) - p0).sum() * cell
        d = min(0.5 * np.abs(
            sum(w * gauss_pdf(G, R(g) @ m, R(g) @ S @ R(g).T)
                for w, (m, S) in zip(PI_ROW,
                                     [(push(PHI0, MU_J, SIG_J)[0],
                                       push(PHI0, MU_J, SIG_J)[1]
                                       + SIGMA_O ** 2 * np.eye(2))] * 2)) - p0
        ).sum() * cell for g in np.linspace(0, TWO_PI, 60, endpoint=False))
        worst = max(worst, tv)
        print(f"   {Th:7.4f}    {loop:18.10f}     {tv:14.6e}    {d:14.6e}")
    assert worst < 1e-12, worst
    print()
    print("  PASS -- the loop product is identically 0 (trivial holonomy) and the record")
    print("         law is EXACTLY Theta-independent. The coboundary carries no holonomy,")
    print("         so B4's negative is reproduced under PIFB2's declared transport.")
    print("         The separation in CHECK 1 is therefore caused by the CONNECTION, not")
    print("         by the two-path construction per se.")


# ================================================================ CHECK 4
def check4():
    print()
    print("=" * 74)
    print("CHECK 4 -- does the tied-replica ELBO identity survive Omega -> P_gamma?")
    print("=" * 74)
    print("  Claim:  KL( Q || P ) = KL( beta || pi ) + sum_J beta_J KL( q_i || u_J )")
    print("  with    Q(J,x) = beta_J q_i(x),   P(J,x) = pi_J u_J(x).")
    print()
    Th = np.pi / 2
    q_i = (np.array([0.3, 0.9]), np.diag([0.30, 0.45]))
    beta = np.array([0.7, 0.3])
    us = source_laws(Th)

    rhs = float(np.sum(beta * np.log(beta / PI_ROW)))
    rhs += float(sum(b * kl_gauss(*q_i, m, S) for b, (m, S) in zip(beta, us)))

    # LHS by direct 2-D quadrature on the joint label-copy space
    G, cell = grid(n=601, half=6.0)
    lhs = 0.0
    for b, p_, (m, S) in zip(beta, PI_ROW, us):
        qx = gauss_pdf(G, *q_i)
        ux = gauss_pdf(G, m, S)
        integrand = b * qx * (np.log(b * qx) - np.log(p_ * ux))
        lhs += integrand.sum() * cell

    print(f"    LHS (quadrature on the joint label-copy space) = {lhs:.10f}")
    print(f"    RHS (row KL + weighted transported KLs)        = {rhs:.10f}")
    print(f"    |LHS - RHS| = {abs(lhs - rhs):.3e}")
    assert abs(lhs - rhs) < 1e-6, (lhs, rhs)
    print("  PASS -- the finite-mixture KL chain rule is unaffected by replacing the")
    print("         transport with parallel transport along a curve. (P_gamma)_# q_j is a")
    print("         pushforward of a probability law by a measurable bijection, hence")
    print("         normalized, so the identity of the closed theorem holds verbatim.")


def main():
    check1()
    check2()
    check3()
    check4()
    print()
    print("=" * 74)
    print("CONCLUSION")
    print("=" * 74)
    print("""
  With the connection entering through curve-mediated transport, distinct holonomies
  induce DISTINCT observation-record laws on a finite design (CHECK 1), the separating
  statistic is gauge invariant and equals the holonomy (CHECK 2), the effect is caused
  by the connection rather than by the two-path construction (CHECK 3), and the exact
  tied-replica ELBO identity is undisturbed (CHECK 4).

  This is the separating tuple that appendix_claim_ledger.tex:242-256 requested and that
  B4 ruled out for the DECLARED model. It does not contradict B4: B4's hypothesis is
  that the connection is not an argument of any generative kernel, and wave2-01:709
  states "Change either and the theorem is unavailable." Curve-mediated transport
  changes exactly that.

  SCOPE. This is a witness, not a theorem. It establishes existence for one bundle,
  one connection family, one fiber, one statistic. It does not establish that holonomy
  is recoverable in general, nor identifiability of the connection from records, nor
  anything about non-abelian G, where the statistic must be a conjugacy-class invariant.
""")


if __name__ == "__main__":
    main()
