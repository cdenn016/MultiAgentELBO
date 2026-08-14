"""Shared-latent coupling witness for finite Gaussian mean-alignment sectors.

The tied-replica product law has zero total correlation and cannot carry a
cross-agent operator. This witness studies the minimal shared-latent extension

    z ~ N(0, T),   k | z ~ N(Lambda z, D),

whose marginal covariance is Sigma = D + Lambda T Lambda^T. For positive-definite
D and T, Woodbury gives

    Sigma^-1 = D^-1 - C,
    C = D^-1 Lambda (T^-1 + Lambda^T D^-1 Lambda)^-1 Lambda^T D^-1,

and rank(C) = rank(Lambda) <= R. Equality with the declared latent width R needs
Lambda to have full column rank.

CLAIM 1  A shared latent supplies genuine cross-agent dependence that the product
         law cannot: TC = 0 exactly for the product law, TC > 0 for the latent law.

CLAIM 2  One scalar latent with same-sign loadings gives an exact flat scalar
         mean-alignment skeleton plus a residual diagonal:

             (1/2) k^T Sigma^-1 k
                 = sum_{a<b} beta_ab (k_a - k_b)^2 / 2
                   + sum_a pi_a k_a^2 / 2.

CLAIM 3  Latent width does not decide positivity. An exact rank-two loading has
         strictly positive edge weights and a proper residual prior, while a
         dependent-column loading has correction rank strictly below its width.
         Seeded rank tables are numerical instances, not general theorems.

CLAIM 4  In the rank-one skeleton, flipping one loading sign makes some edge
         weights negative. The residual diagonal can also be improper.

CLAIM 5  A fiber cross-block identifies the product beta_ab W_ab Omega_ab, not
         Omega_ab alone. Edge strength and metric must be divided out before a
         transport cocycle is tested.

CLAIM 6  A three-agent, two-dimensional rotation construction has beta = 1/4,
         W = I, an exact transport cocycle, exact precision reconstruction, and
         residual prior I/4. For general loadings, d >= K is necessary but not
         sufficient for an induced K-by-K coefficient to be invertible.

Run:  python docs/verification/shared_latent_coupling_witness.py
Requires: numpy.
"""

import numpy as np

SEED = 20260813


def total_correlation(S):
    """TC of a centered Gaussian with covariance S."""
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


def woodbury_correction(private_covariance, loading, latent_covariance):
    """Return D^-1 - (D + Lambda T Lambda^T)^-1 in Woodbury form."""
    private_precision = np.linalg.inv(private_covariance)
    middle = np.linalg.inv(
        np.linalg.inv(latent_covariance)
        + loading.T @ private_precision @ loading
    )
    return private_precision @ loading @ middle @ loading.T @ private_precision


def correction_rank(private_covariance, loading, latent_covariance, tol=1e-10):
    """Rank of the Woodbury correction for positive-definite D and T."""
    correction = woodbury_correction(private_covariance, loading, latent_covariance)
    return int(np.linalg.matrix_rank(correction, tol=tol))


def rank_two_positive_split_example():
    """Exact-data rank-two control with positive edges and a proper prior."""
    private_covariance = np.eye(4)
    latent_covariance = np.eye(2)
    loading = np.array(
        [
            [1.0, 0.1],
            [1.0, 0.2],
            [1.0, 0.3],
            [1.0, 0.4],
        ]
    )
    private_precision = np.linalg.inv(private_covariance)
    correction = woodbury_correction(
        private_covariance, loading, latent_covariance
    )
    precision = private_precision - correction
    beta, prior, laplacian = laplacian_split(precision)
    return {
        "loading": loading,
        "precision": precision,
        "beta": beta,
        "prior": prior,
        "laplacian": laplacian,
        "correction_rank": int(np.linalg.matrix_rank(correction, tol=1e-12)),
        "split_residual": float(
            np.linalg.norm(precision - laplacian - np.diag(prior))
        ),
    }


def rank_one_improper_prior_example():
    """Exact-data rank-one control with positive edges and an improper prior."""
    loading = np.array([10.0, 1.0, 1.0, 1.0])
    normalizer = 1.0 + loading @ loading
    correction = np.outer(loading, loading) / normalizer
    precision = np.eye(4) - correction
    beta, prior, laplacian = laplacian_split(precision)
    return {
        "loading": loading,
        "precision": precision,
        "beta": beta,
        "prior": prior,
        "laplacian": laplacian,
        "correction_rank": int(np.linalg.matrix_rank(correction, tol=1e-12)),
        "split_residual": float(
            np.linalg.norm(precision - laplacian - np.diag(prior))
        ),
    }


def recover_transport(cross_precision_block, beta, weight):
    """Recover Omega from P_ab = -beta W Omega after beta and W are declared."""
    if beta <= 0:
        raise ValueError("beta must be strictly positive")
    return np.linalg.solve(weight, -cross_precision_block) / beta


def induced_transport_coefficient(loading_a, middle, loading_b, private_covariance_b):
    """Return Lambda_a M Lambda_b^T S_b^-1 before choosing beta and W."""
    return loading_a @ middle @ loading_b.T @ np.linalg.inv(private_covariance_b)


def induced_block_rank(loading_a, middle, loading_b, private_covariance_b, tol=1e-10):
    """Rank entering the exact invertibility condition for the induced block."""
    coefficient = induced_transport_coefficient(
        loading_a, middle, loading_b, private_covariance_b
    )
    return int(np.linalg.matrix_rank(coefficient, tol=tol))


def weighted_rotation_cocycle_example():
    """Return an exact N=3, K=d=2 weighted rotation-cocycle construction."""
    rotations = {
        0: np.eye(2),
        1: np.array([[0.0, -1.0], [1.0, 0.0]]),
        2: -np.eye(2),
    }
    beta = 1 / 4
    loading = np.vstack([rotations[a] for a in range(3)])
    precision = np.eye(6) - loading @ (np.eye(2) / 4) @ loading.T
    transports = {
        (a, b): rotations[a] @ rotations[b].T
        for a in range(3)
        for b in range(3)
    }

    reconstructed = np.zeros_like(precision)
    for a in range(3):
        a_slice = slice(2 * a, 2 * a + 2)
        for b in range(a + 1, 3):
            b_slice = slice(2 * b, 2 * b + 2)
            omega_ab = transports[(a, b)]
            reconstructed[a_slice, a_slice] += beta * np.eye(2)
            reconstructed[b_slice, b_slice] += beta * omega_ab.T @ omega_ab
            reconstructed[a_slice, b_slice] -= beta * omega_ab
            reconstructed[b_slice, a_slice] -= beta * omega_ab.T

    residual_priors = {}
    for a in range(3):
        a_slice = slice(2 * a, 2 * a + 2)
        residual_priors[a] = (
            precision[a_slice, a_slice] - reconstructed[a_slice, a_slice]
        )
        reconstructed[a_slice, a_slice] += residual_priors[a]

    return {
        "beta": beta,
        "precision": precision,
        "transports": transports,
        "residual_priors": residual_priors,
        "reconstructed_precision": reconstructed,
    }


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
    print("CLAIM 2 -- an exact flat scalar mean-alignment skeleton plus a prior")
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
    print("\n  PASS -- this exact flat scalar mean-alignment skeleton is obtained")
    print("         from a law with strictly positive total correlation.")
    print("         It is narrower than the complete directed two-channel PIFB2 action.")
    return pi


def claim_3():
    print()
    print("=" * 74)
    print("CLAIM 3 -- correction rank follows loading rank; positivity is separate")
    print("=" * 74)
    rng = np.random.default_rng(SEED)
    N = 6
    sig2 = rng.uniform(0.3, 0.9, N)
    D = np.diag(sig2)
    Di = np.linalg.inv(D)
    print(
        "   R    rank(Lambda)    rank(D^-1 - Sigma^-1)    all beta > 0    min beta"
    )
    print("  Seeded numerical instances only; this table is not a general theorem.")
    for R in (1, 2, 3, 5):
        Lam = np.abs(rng.normal(size=(N, R))) * 0.9      # same-sign loadings
        T = np.diag(rng.uniform(0.4, 1.0, R))
        correction = woodbury_correction(D, Lam, T)
        P = Di - correction
        beta, _, _ = laplacian_split(P)
        iu = np.triu_indices(N, 1)
        loading_rank = int(np.linalg.matrix_rank(Lam, tol=1e-9))
        rank = int(np.linalg.matrix_rank(correction, tol=1e-9))
        allpos = bool(np.all(beta[iu] > 0))
        print(
            f"   {R}    {loading_rank:^12d}    {rank:^25d}    "
            f"{str(allpos):^12s}    {beta[iu].min():+.4f}"
        )
        assert rank == loading_rank
        assert rank <= R
        if R == 1:
            assert allpos
    print("\n  DESCRIPTIVE ONLY -- higher-rank rows above are one seeded sample each.")
    print("  Their signs cannot support a universal positivity or nonpositivity claim.")

    exact = rank_two_positive_split_example()
    exact_off = exact["beta"][np.triu_indices(4, 1)]
    assert exact["correction_rank"] == 2
    assert np.all(exact_off > 0)
    assert np.all(exact["prior"] > 0)
    assert exact["split_residual"] < 1e-12
    print("\n  Exact rank-two all-positive control:")
    print(f"    min beta = {exact_off.min():.12f}; min prior = {exact['prior'].min():.12f}")

    base_column = np.arange(1.0, 5.0)
    dependent = np.column_stack([base_column, 2.0 * base_column])
    dependent_D = np.eye(4)
    dependent_T = np.eye(2)
    dependent_rank = correction_rank(
        dependent_D, dependent, dependent_T, tol=1e-12
    )
    assert np.linalg.matrix_rank(dependent, tol=1e-12) == 1
    assert dependent_rank == 1
    assert dependent_rank < dependent.shape[1]
    print("\n  Dependent-column control:")
    print(f"    declared R = 2; rank(Lambda) = rank(correction) = {dependent_rank}")

    print("\n  PASS -- for SPD D and T, rank(correction) = rank(Lambda) <= R.")
    print("         Equality with R requires full column rank of Lambda.")
    print("         The exact rank-two control shows rank alone does not obstruct positivity.")


def claim_4(pi=None):
    exact = rank_one_improper_prior_example()
    exact_beta = exact["beta"][np.triu_indices(4, 1)]
    assert exact["correction_rank"] == 1
    assert exact["split_residual"] < 1e-12
    assert np.all(exact_beta > 0)
    if pi is None:
        pi = exact["prior"]
    pi = np.asarray(pi, dtype=float)
    if not np.min(pi) < 0:
        raise AssertionError("Claim 4 requires a negative residual prior entry")

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
    print("  (a) same-sign loadings are necessary for this rank-one positive split.")
    print(f"      flip one loading's sign -> beta_01 = {b01:+.4f}  (repulsive; no KL sum")
    print(f"      can represent a negative weight, since each term is >= 0)")
    assert b01 < 0
    print(f"\n  (b) the residual diagonal need not be a valid prior precision.")
    print(
        f"      exact control: rank = {exact['correction_rank']}; "
        f"split residual = {exact['split_residual']:.2e}; min beta = {exact_beta.min():.5f}"
    )
    print(f"      pi = {np.round(pi, 5)}")
    print(f"      all entries positive? {bool(np.all(pi > 0))}   min = {pi.min():+.5f}")
    print(f"      a negative entry is an IMPROPER induced prior for that agent.")
    print("\n  PASS -- both side conditions are live and must be declared, not assumed.")


def claim_5_and_6():
    """Separate weighted cross-block coefficients from transport geometry.

    Woodbury gives P_ab = -B_a Lambda_a M Lambda_b^T B_b. A quadratic
    edge identifies -P_ab = beta_ab W_ab Omega_ab; beta_ab and W_ab must be
    declared before Omega_ab can be recovered or tested as a cocycle.

    The induced coefficient is invertible exactly when its matrix rank is K.
    Consequently d >= K is necessary but not sufficient. The exact weighted
    rotation construction below refutes the universal cocycle obstruction.
    """
    print()
    print("=" * 74)
    print("CLAIM 5 -- cross-blocks identify beta W Omega, not Omega alone")
    print("=" * 74)
    rng = np.random.default_rng(SEED)
    N, K, d = 4, 3, 4
    Lam = {a: rng.normal(size=(K, d)) * 0.8 for a in range(N)}
    S = {}
    for a in range(N):
        A = np.eye(K) + 0.3 * rng.normal(size=(K, K))
        S[a] = A @ A.T
    T = np.eye(d) * 0.9

    B = np.zeros((N * K, N * K))
    L = np.zeros((N * K, d))
    Sig = np.zeros((N * K, N * K))
    for a in range(N):
        B[a * K:(a + 1) * K, a * K:(a + 1) * K] = np.linalg.inv(S[a])
        L[a * K:(a + 1) * K, :] = Lam[a]
        Sig[a * K:(a + 1) * K, a * K:(a + 1) * K] = S[a]
    Sig = Sig + L @ T @ L.T
    P = np.linalg.inv(Sig)
    M = np.linalg.inv(np.linalg.inv(T) + L.T @ B @ L)
    wood = np.linalg.norm(P - (B - B @ L @ M @ L.T @ B))
    print(f"  Woodbury  ||Sigma^-1 - (B - B L M L^T B)|| = {wood:.2e}")
    assert wood < 1e-10

    coefficient = induced_transport_coefficient(Lam[0], M, Lam[1], S[1])
    precision_coefficient = S[0] @ (
        -P[0:K, K:2 * K]
    )
    coefficient_residual = float(np.linalg.norm(coefficient - precision_coefficient))
    rk = induced_block_rank(Lam[0], M, Lam[1], S[1], tol=1e-9)
    rank_upper = min(
        np.linalg.matrix_rank(Lam[0], tol=1e-9),
        np.linalg.matrix_rank(Lam[1], tol=1e-9),
        np.linalg.matrix_rank(M, tol=1e-9),
        K,
    )
    print(
        f"  sampled rank(Lambda_0 M Lambda_1^T S_1^-1) = {rk}; "
        f"upper bound = {rank_upper}; coefficient residual = {coefficient_residual:.2e}"
    )
    print("  Exact condition: the K-by-K coefficient is invertible iff its rank is K.")
    assert coefficient_residual < 1e-10
    assert rk <= rank_upper

    dependent = np.array([[1.0, 0.0], [0.0, 0.0]])
    singular = induced_transport_coefficient(
        dependent, np.eye(2), dependent, np.eye(2)
    )
    singular_rank = int(np.linalg.matrix_rank(singular, tol=1e-12))
    assert dependent.shape == (2, 2)
    assert singular_rank == 1
    print(f"  d = K = 2 dependent-loading control: rank = {singular_rank}, det = 0")
    print("  Therefore d >= K is necessary only; loading/middle-factor rank is decisive.")

    print()
    print("=" * 74)
    print("CLAIM 6 -- a weighted rotation transport is an exact cocycle")
    print("=" * 74)
    example = weighted_rotation_cocycle_example()
    beta = example["beta"]
    precision = example["precision"]
    transports = example["transports"]
    cross_residual = 0.0
    cocycle_residual = 0.0
    self_residual = 0.0
    for a in range(3):
        a_slice = slice(2 * a, 2 * a + 2)
        self_residual = max(
            self_residual, float(np.linalg.norm(transports[(a, a)] - np.eye(2)))
        )
        for b in range(3):
            omega_ab = transports[(a, b)]
            if a != b:
                b_slice = slice(2 * b, 2 * b + 2)
                block = precision[a_slice, b_slice]
                recovered = recover_transport(block, beta, np.eye(2))
                cross_residual = max(
                    cross_residual,
                    float(np.linalg.norm(block + beta * omega_ab)),
                    float(np.linalg.norm(recovered - omega_ab)),
                )
            for c in range(3):
                cocycle_residual = max(
                    cocycle_residual,
                    float(
                        np.linalg.norm(
                            omega_ab @ transports[(b, c)] - transports[(a, c)]
                        )
                    ),
                )

    reconstruction_residual = float(
        np.linalg.norm(example["reconstructed_precision"] - precision)
    )
    prior_residual = max(
        float(np.linalg.norm(prior - np.eye(2) / 4))
        for prior in example["residual_priors"].values()
    )
    min_prior = min(
        float(np.linalg.eigvalsh(prior).min())
        for prior in example["residual_priors"].values()
    )
    print(f"  beta = {beta:.2f}, W = I; remove both before testing Omega")
    print(f"  max cross-block/recovery residual = {cross_residual:.2e}")
    print(f"  max self-edge residual = {self_residual:.2e}")
    print(f"  max cocycle residual = {cocycle_residual:.2e}")
    print(f"  full precision reconstruction residual = {reconstruction_residual:.2e}")
    print(f"  residual prior error from I/4 = {prior_residual:.2e}")
    assert beta == 1 / 4
    assert max(
        cross_residual, self_residual, cocycle_residual, reconstruction_residual,
        prior_residual,
    ) < 1e-12
    assert min_prior > 0

    print("\n  PASS -- the exact weighted cross-blocks reconstruct a proper cocycle model.")
    print("         The off-diagonal precision identifies beta W Omega, not Omega alone.")
    print("         The former universal cocycle obstruction is therefore refuted.")


def main():
    claim_1_and_2()
    claim_3()
    claim_4()
    claim_5_and_6()
    print()
    print("=" * 74)
    print("SCOPE -- exact finite skeletons and explicit open boundaries")
    print("=" * 74)
    print("""
  ESTABLISHED -- an exact flat scalar mean-alignment skeleton can have a rank-two
  positive edge split and a proper residual prior.

  ESTABLISHED -- after beta and W are separated, the N=3, K=d=2 construction has
  beta=1/4, W=I, an exact rotation cocycle, residual prior I/4, and exact recovery.

  OPEN -- directed row-simplex attention
      The symmetric complete-graph coefficients here are not an arbitrary row law.

  OPEN -- categorical entropy
      No source-label entropy or row-prior term is represented by this quadratic.

  OPEN -- two transported law channels
      Only one Gaussian mean-alignment channel is constructed.

  OPEN -- full-law representability
      No complete PIFB2 generative/recognition law or mean-field closure is proved.

  The shared latent is an explicit extension of the declared generative inventory;
  Theory/04 membership is not automatic. Recognition-side gaps remain unpriced.

  No h -> 0 limit, residual eps_h bound, or Gamma-convergence statement
  is established by these fixed-finite-N witnesses.
""")


if __name__ == "__main__":
    main()
