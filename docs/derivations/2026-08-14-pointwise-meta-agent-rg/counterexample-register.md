<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-a0d61fb082b9632a9aac685fced7bf4a82f1a9f115a72b9583a6ed96f636c952","schema_version":"rigorous-theory-search/v1","target_digest":"a0d61fb082b9632a9aac685fced7bf4a82f1a9f115a72b9583a6ed96f636c952"} -->
# Counterexample register

These witnesses refute eight shortcuts excluded from the frozen theorem. They do not refute TARGET-POINTWISE-RG. The mathematical derivations are in evidence/counterexample-proofs.md (SHA-256 dc375fc39c19e4607c2c8fe63475641dbd0836feb45ac8684fd4bdbe01d3abd9).

## CE-1: KL-threshold adjacency is not transitive

Take Bernoulli parameters (1/10), (1/2), and (9/10), with directed forward-KL threshold (0.6). The first two successive KL values are approximately (0.368064) and (0.510826), while the endpoint KL is approximately (1.757780). Status: EVIDENCE_VERIFIED by exact logarithmic expressions; decimal values are display-only.

## CE-2: zero singleton-marginal KL can hide infinite joint VFE defect

On the binary square, put mass (1/2) on the two parity atoms for one law and mass (1/2) on the two anti-parity atoms for the other. Both singleton marginals are fair, but the joint supports are disjoint, so the directed joint KL and the common-channel conditional defect are positive infinity. Status: EVIDENCE_VERIFIED.

## CE-3: trivial holonomy does not force belief agreement

On a two-vertex tree with identity transport, choose (N(-a e_1,I_K)) and (N(a e_1,I_K)). Holonomy is trivial, while the directed KL is exactly (2a^2) and is unbounded with (a). Status: EVIDENCE_VERIFIED.

## CE-4: belief agreement does not force trivial holonomy

On a three-dimensional cycle, let the closing holonomy be (diag(1,-1,-1)). It is not the identity and has only a one-dimensional vector fixed sector, yet it stabilizes every centered isotropic Gaussian. Assigning that law consistently makes all transported marginal KL terms vanish. Status: EVIDENCE_VERIFIED.

## CE-5: a connection spectral gap is state blind and scalable

The two-node connection Laplacian with identity link and scalar conductance (c>0) has positive gap (2c). It contains no law data and can accompany either identical or arbitrarily separated laws. Rescaling (c) changes the gap without changing those laws. Status: EVIDENCE_VERIFIED.

## CE-6: one-way KL does not control reverse KL

For (P=(1,0)) and (Q=(1/2,1/2)), (KL(P||Q)=log 2) is finite while (KL(Q||P)=+infinity) because reverse absolute continuity fails. Status: EVIDENCE_VERIFIED.

## CE-7: Gaussian moment projection leaves a nonlinear boundary residual

Let the equally weighted children be (P_-=N(-a,1)) and (P_+=N(a,1)). Their full-Gaussian forward-KL barycenter is (G=N(0,1+a^2)). For (H(x)=lambda x^4),

\[
\mathbb E_G[H]
-\tfrac12\left(\mathbb E_{P_-}[H]+\mathbb E_{P_+}[H]\right)
=2\lambda a^4.
\]

This is nonzero whenever (a lambda) is nonzero, so Gaussian projection does not exactly preserve the nonlinear boundary action. The unrestricted mixture retains the child-average expectation by linearity. As an additional family-closure control, cubing a standard Gaussian gives second and fourth moments (15) and (10395), incompatible with the fourth moment (675) of the variance-matched Gaussian. Status: EVIDENCE_VERIFIED.

## CE-8: literal overlapping parents duplicate mass

Give one unit-mass child full incidence in two parents. The parent mass is then (2), not (1); independently replicating both endpoints of its self-edge yields four copies and event mass (4). Normalizing each incidence to (1/2) defines a different stochastic kernel. Status: EVIDENCE_VERIFIED.

## Recalculation boundary

evidence/recompute.py and evidence/recompute-output.json deterministically corroborate the finite arithmetic. The exact Fraction check for CE-7 uses (a=3/2), (lambda=5/7), and obtains residual (405/56) on both sides of the identity. The script reports all eleven checks true, but it is a SYMBOLIC_CHECK, not proof of the quantified claims.
