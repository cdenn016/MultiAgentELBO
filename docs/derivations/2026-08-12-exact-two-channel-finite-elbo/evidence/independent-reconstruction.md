# Independent reconstruction

This reconstruction starts only from the frozen contract.

1. Multiply the normalized private, belief-label-copy, and model-label-copy kernels. Finite products
   and finite source sums preserve unit mass.
2. Form the tied recognition product. Tying parameters across distinct factors restricts the
   recognition family but does not alter normalization.
3. Expand the fixed-observation density ratio. Factorization separates the negative ELBO into one
   private and two relational KLs per agent-site record.
4. Apply the product-reference KL chain rule to the private joint. This produces both marginal
   self KLs and (I_\zeta(K;M)).
5. Apply the finite-mixture KL chain rule independently to the belief and model relational blocks.
   This produces categorical row KL plus expected transported marginal KL in each channel.
6. Define the remaining well-typed terms, including the joint-private observation expectation, as
   the joint-typed lagged unit-coefficient two-channel scalar
   (\mathcal F_{\mathrm{JT},h}^{\mathrm{lag},1}). Under (\zeta=q\otimes s), the mutual
   information vanishes and the exact negative ELBO equals this scalar.
7. Push every fiber law through the declared endpoint coordinate bijection. Relative-entropy
   invariance and likelihood covariance reproduce the same scalar.

No manuscript formula is required to establish the construction or identity. Comparing the
derived joint-private observation expectation with the literal PIFB2 observation display is a
separate, nondependency question, and the current manuscript typing does not close it.
