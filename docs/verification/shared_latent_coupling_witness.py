"""Shared-latent coupling witness: can a genuinely coupled generative law produce
PIFB2's transported-KL interaction, and at what rank?

Addresses the validated-ledger claim `genuine-coupling-before-continuum` (HIGH,
INCONCLUSIVE), which states that tied product replicas alone cannot generate the
required cross-agent interaction family. The tied-replica law is blockwise-product
by construction, P_h^n = (x)_a P_a^n, so its total correlation is identically zero
and it cannot carry a multi-body operator. The minimal repair is a SHARED LATENT.

Gaussian instance, closed form throughout:

    z ~ N(0, T),   k_a | z ~ N((Lambda z)_a, sigma_a^2),   a = 1..N

so marginally Sigma = D + Lambda T Lambda^T with D = diag(sigma_a^2). Integrating
out z gives the effective action -log p(k) = (1/2) k^T Sigma^{-1} k, and by
Sherman-Morrison Sigma^{-1} = D^{-1} - (rank-R correction).

CLAIM 1  A shared latent supplies genuine cross-agent dependence that the product
         law cannot: TC = 0 exactly for the product law, TC > 0 for the latent law.

CLAIM 2  With ONE latent and same-sign loadings, the induced effective action is
         EXACTLY a positive-weight transported-KL coupling plus a prior,

             (1/2) k^T Sigma^{-1} k
                 = sum_{a<b} beta_ab (k_a - k_b)^2 / 2  +  sum_a pi_a k_a^2 / 2 ,

         with rank-one weights beta_ab = c v_a v_b, v = D^{-1} lambda. This is the
         functional form PIFB2 declares, obtained from a genuinely coupled law.

CLAIM 3  The construction is rank-limited, and that is a real obstruction. The
         number of shared latents equals the rank of the induced coupling; but for
         R >= 2 the weights are no longer all positive, so the coupling stops being
         a sum of KLs. A shared-latent law can deliver EITHER the transported-KL
         form (R = 1, rank-one attention) OR higher-rank attention, not both.

CLAIM 4  Two side conditions. Same-sign loadings are necessary: flipping one sign
         makes a weight negative (repulsive), which no KL sum can represent. And the
         residual diagonal need not be a valid prior precision -- entries can be
         negative, i.e. the induced "prior" can be improper.

Run:  python docs/verification/shared_latent_coupling_witness.py
Requires: numpy.
"""

import numpy as np

SEED = 20260813


def total_correlation(S):
    """TC of a centred Gaussian with covariance S."""
    return 0.5 * (np.sum(np.log(np.diag(S))) - np.linalg.slogdet(S)[1])


def laplacian_split(P):
    """Write a symmetric P as L(beta) + diag(pi) with L a graph Laplacian.

    The split is unique: off-diagonal Laplacian entries are -beta_ab, so
    beta_ab = -P_ab, and the residual diagonal absorbs the rest.
    """
    n = P.shape[0]
    beta = -(P - np.diag(np.diag(P)))
    L = np.diag(beta.sum(1)) - beta
    pi = np.diag(P - L)
    return beta, pi, L


def claim_1_and_2():
    print("=" * 74)
    print("CLAIM 1 -- a shared latent creates dependence the product law cannot")
    print("=" * 74)
    rng = np.random.default_rng(SEED)
    N = 4
    lam = rng.uniform(0.6, 1.4, N)
    sig2 = rng.uniform(0.3, 0.9, N)
    tau2 = 0.7
    D = np.diag(sig2)
    Sig_prod = D.copy()
    Sig_lat = D + tau2 * np.outer(lam, lam)
    tc_p, tc_l = total_correlation(Sig_prod), total_correlation(Sig_lat)
    print(f"  TC(tied-replica product law) = {tc_p:.3e}")
    print(f"  TC(shared-latent law)        = {tc_l:.6f}")
    assert abs(tc_p) < 1e-12 and tc_l > 0.1

    print()
    print("=" * 74)
    print("CLAIM 2 -- one latent gives EXACTLY the transported-KL form plus a prior")
    print("=" * 74)
    Di = np.linalg.inv(D)
    P = np.linalg.inv(Sig_lat)
    v = Di @ lam
    c = tau2 / (1 + tau2 * lam @ Di @ lam)
    print(f"  Sherman-Morrison  ||Sigma^-1 - (D^-1 - c v v^T)|| = "
          f"{np.linalg.norm(P - (Di - c * np.outer(v, v))):.2e}")
    beta, pi, L = laplacian_split(P)
    iu = np.triu_indices(N, 1)
    pred = c * np.outer(v, v)
    print(f"  beta_ab all strictly positive : {bool(np.all(beta[iu] > 0))}   "
          f"range [{beta[iu].min():.4f}, {beta[iu].max():.4f}]")
    print(f"  beta_ab == c v_a v_b to        : {np.max(np.abs(beta[iu] - pred[iu])):.2e}")
    print(f"  exact split ||P - (L + diag(pi))|| = {np.linalg.norm(P - (L + np.diag(pi))):.2e}")

    mu = rng.normal(size=N)
    E_full = 0.5 * mu @ P @ mu
    E_kl = 0.5 * sum(beta[a, b] * (mu[a] - mu[b]) ** 2
                     for a in range(N) for b in range(a + 1, N))
    E_pri = 0.5 * float(np.sum(pi * mu ** 2))
    print(f"\n  energy decomposition on a random state:")
    print(f"    (1/2) k^T Sigma^-1 k                = {E_full:+.10f}")
    print(f"    sum_{{a<b}} beta_ab (k_a-k_b)^2 / 2  = {E_kl:+.10f}")
    print(f"    prior  sum_a pi_a k_a^2 / 2         = {E_pri:+.10f}")
    print(f"    residual                            = {E_full - E_kl - E_pri:+.2e}")
    assert abs(E_full - E_kl - E_pri) < 1e-12
    assert np.all(beta[iu] > 0)
    print("\n  PASS -- the induced interaction IS PIFB2's transported-KL form, obtained")
    print("         from a law with strictly positive total correlation.")
    return pi


def claim_3():
    print()
    print("=" * 74)
    print("CLAIM 3 -- the construction is rank-limited: KL form OR high-rank, not both")
    print("=" * 74)
    rng = np.random.default_rng(SEED)
    N = 6
    sig2 = rng.uniform(0.3, 0.9, N)
    D = np.diag(sig2)
    Di = np.linalg.inv(D)
    print("   R    rank(D^-1 - Sigma^-1)    all beta_ab > 0    min beta_ab")
    ok_at_1 = None
    for R in (1, 2, 3, 5):
        Lam = np.abs(rng.normal(size=(N, R))) * 0.9      # same-sign loadings
        T = np.diag(rng.uniform(0.4, 1.0, R))
        Sig = D + Lam @ T @ Lam.T
        P = np.linalg.inv(Sig)
        beta, _, _ = laplacian_split(P)
        iu = np.triu_indices(N, 1)
        rank = np.linalg.matrix_rank(Di - P, tol=1e-9)
        allpos = bool(np.all(beta[iu] > 0))
        print(f"   {R}    {rank:^21d}    {str(allpos):^15s}    {beta[iu].min():+.4f}")
        assert rank == R
        if R == 1:
            ok_at_1 = allpos
        if R >= 2:
            assert not allpos, R
    assert ok_at_1
    print("\n  PASS -- #latents = rank of the induced coupling, but positivity fails for")
    print("         R >= 2. A single latent buys rank-one attention with a genuine KL")
    print("         form; PIFB2's general row-stochastic beta needs rank up to N-1, and")
    print("         at that rank the coupling is no longer a sum of KLs.")


def claim_4(pi):
    print()
    print("=" * 74)
    print("CLAIM 4 -- two side conditions on the R = 1 result")
    print("=" * 74)
    rng = np.random.default_rng(SEED)
    N = 4
    lam = rng.uniform(0.6, 1.4, N)
    sig2 = rng.uniform(0.3, 0.9, N)
    tau2 = 0.7
    D = np.diag(sig2)
    lam2 = lam.copy()
    lam2[0] *= -1.0
    P2 = np.linalg.inv(D + tau2 * np.outer(lam2, lam2))
    b01 = -P2[0, 1]
    print(f"  (a) same-sign loadings are NECESSARY.")
    print(f"      flip one loading's sign -> beta_01 = {b01:+.4f}  (repulsive; no KL sum")
    print(f"      can represent a negative weight, since each term is >= 0)")
    assert b01 < 0
    print(f"\n  (b) the residual diagonal need not be a valid prior precision.")
    print(f"      pi = {np.round(pi, 5)}")
    print(f"      all entries positive? {bool(np.all(pi > 0))}   min = {pi.min():+.5f}")
    print(f"      a negative entry is an IMPROPER induced prior for that agent.")
    print("\n  PASS -- both side conditions are live and must be declared, not assumed.")


def main():
    pi = claim_1_and_2()
    claim_3()
    claim_4(pi)
    print()
    print("=" * 74)
    print("SCOPE -- what this does NOT establish")
    print("=" * 74)
    print("""
  (a) Scalar states (K = 1 per agent), centred Gaussians, one base point. The
      fiber-valued case with transports Omega_ij is NOT covered: here the "transport"
      is the identity, so beta_ab (k_a - k_b)^2 is the FLAT case of the transported
      KL. Whether a shared latent can generate beta_ab ||k_a - Omega_ab k_b||^2 with
      a nontrivial Omega is open, and is the obvious next witness.

  (b) Nothing here shows the shared-latent law is in Theory/04's declared generative
      class. Adding a latent z is a modification of that class, exactly as the
      label-copy block (J_a, X_a) was; the cost is a declaration.

  (c) The recognition side is untouched. If Q factorizes as q(z) (x) prod_a Q_a there
      is a mean-field gap to price, and if it does not, the tied-replica machinery
      does not apply verbatim.

  (d) CLAIM 3's negative is for same-sign loadings drawn at random. It shows
      positivity FAILS generically at R >= 2; it does not prove no R >= 2 loading
      matrix yields an all-positive beta. Whether the set of such matrices is
      nonempty, and how restrictive it is, is open.

  (e) No claim about the h -> 0 limit, the effective action's residual eps_h, or
      Gamma-convergence. This addresses only whether cross-agent coupling of the
      declared FORM can exist at all at fixed finite N.
""")


if __name__ == "__main__":
    main()
