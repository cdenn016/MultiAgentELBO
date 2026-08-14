<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2","schema_version":"rigorous-theory-search/v1","target_digest":"ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2"} -->
# Finite collective joint-lift and shared-Fisher theorem

## Definitions

Let \(\Omega=\{0,1\}^6\), group the six singleton Bernoulli coordinates into
three declared agent pairs, and define

\[
P_\theta(x)=\prod_i\theta_i^{x_i}(1-\theta_i)^{1-x_i},\quad
D(\theta)=\prod_i\theta_i(1-\theta_i),\quad
\chi(x)=(-1)^{\sum_i x_i}.
\]

For fixed \(|\kappa|<1\), set

\[
Q_{\theta,\kappa}(x)=P_\theta(x)+\kappa\chi(x)D(\theta).\tag{1}
\]

The section data are the six singleton marginals, not three arbitrary
two-bit joint marginals.

## Theorem

On the frozen finite open domain:

1. Equation (1) is a strictly positive normalized polynomial family. Every
   one of its 63 proper marginals is the corresponding product marginal.

2. Singleton extraction is a smooth left inverse of the lift. Hence the lift
   is a rank-six immersion, its categorical-Fisher pullback is positive
   definite with zero radical, and any further section pullback has radical
   equal to the section differential's kernel. Quotient conclusions require
   the separately stated constant-rank, integrability, regular-leaf-space,
   and basicness hypotheses.

3. Fixed scalar \(\kappa\) is equivariant under the eight paired two-bit
   complements. Type-compatible agent-pair permutations are admitted finite
   relabelings; within-pair swaps are only accidental toy-coordinate
   symmetries. A nonzero fixed scalar is not equivariant under an odd
   complement. Odd-flip equivariance requires the additional pseudoscalar
   law \(\kappa\mapsto-\kappa\).

4. For a two-bit block \(A\), strictly positive target \(T\), and recognition
   laws \(Q,Q'\) sharing outside marginal \(m\),

   \[
   \mathcal F_T(Q)-\mathcal F_T(Q')
   =\sum_bm(b)\left[
   D_{\rm KL}(Q_{A|b}\|T_{A|b})
   -D_{\rm KL}(Q'_{A|b}\|T_{A|b})\right].
   \]

   Along every normalized fixed-outside conditional tangent, the global
   differential equals the outside-weighted conditional differential. One
   executable control varies \(\kappa\) and is explicitly labeled a
   lift-changing, non-per-unit-\(\kappa\) direction. Three parameterized
   controls fix \(\kappa\) and, for each agent pair in turn, vary exactly that
   agent's two \(\theta\) coordinates while keeping the complementary four
   coordinates and outside marginal fixed; each checks both the finite
   difference and analytic directional differential.

5. For any smooth positive joint family with the declared singleton
   marginals, if \(J=s+R\), then

   \[
   G_{\rm joint}
   =\mathbb E[ss^{\mathsf T}]
   +\mathbb E[sR^{\mathsf T}]
   +\mathbb E[Rs^{\mathsf T}]
   +\mathbb E[RR^{\mathsf T}].
   \]

   The cross terms are signed and cannot generally be dropped. In the
   six-bit parity family, pairwise independence and score projection make
   them vanish and give

   \[
   G_{\rm joint}
   =\operatorname{diag}\!\left(\frac1{\theta_i(1-\theta_i)}\right)
   +\mathbb E[RR^{\mathsf T}].
   \]

   The residual Gram matrix is positive definite for every
   \(\kappa\ne0\).

6. At \(\theta_i=1/2\), with \(c=\kappa/64\),

   \[
   G_{\rm joint}=\frac4{1-c^2}I_6.
   \]

   For \(\kappa=1/2\), its residual is \(4I_6/16383\). A weighted marginal
   metric \(G_w=\operatorname{diag}(w_i/[\theta_i(1-\theta_i)])\) agrees on
   the full center tangent space exactly when
   \(w_i=1/(1-c^2)\) for every \(i\); unit weights agree exactly at
   \(\kappa=0\).

7. With uniform prior and the declared binary hyperedge kernel

   \[
   K(1|x)=\tfrac12(1+c\chi(x)),\qquad
   K(0|x)=\tfrac12(1-c\chi(x)),
   \]

   the evidence is \(1/2\), the posterior for record 1 is (1), the
   correlated-lift VFE is \(\log2\), and the product-lift excess is
   \(-\tfrac12\log(1-c^2)\).

## Sharpness and selection boundary

The six singleton constraints define a 57-dimensional Frechet fiber in the
63-dimensional simplex interior. The parity family selects only one
direction. The sections do not select \(\kappa\), the hyperedge kernel, or any
other lift direction.

Pairwise-product record factorization is extra conditional-independence
structure. The exact cancelling joint kernel in
evidence/vfe-hyperedge-proof.md has the same record marginals and strict
positivity but zero \(ab\) coefficient, so it can erase a six-bit term created
by the product factorization.

The older two-bit lift has Fisher correction eigenvalues \(-4/9\) and
\(4/7\), proving the positive residual correction is family-specific. A
redundant promotion through the product \(\kappa\eta\) has interaction rank at
most one and only that product is identifiable.

Fixed-target VFE covariance requires coherent target pushforward. Full-joint
VFE and Fisher remain lift-dependent. No canonical lift, intervention
equivalence, agency, GL(K), continuum, physical geometry, time, units, or
renormalization conclusion follows.
