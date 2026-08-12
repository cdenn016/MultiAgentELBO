<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-a4db58accfdd6c9563a7bd8cb34526351564b0737bd3931a96d3bac7e7674a6c","schema_version":"rigorous-theory-search/v1","target_digest":"a4db58accfdd6c9563a7bd8cb34526351564b0737bd3931a96d3bac7e7674a6c"} -->
# Counterexample register

1. **Missing base measure.** The current action uses bare coordinate \(dc\) although the base is declared to have no preferred metric or measure. A corrected theorem must declare a positive density or Borel measure.

2. **Locally defined sections in global integrals.** Multiplying by a vanishing support mask does not by itself define \(q_i\) or \(s_i\) outside \(U_i\). Self terms should be integrated on \(U_i\) and pair terms on \(U_i\cap U_j\), or explicit extensions must be supplied.

3. **Empty attention row.** The normalized absorbed prior is undefined when its denominator vanishes. The admissible space must use nonempty active neighbor sets or a declared null/self source, with extended-real relative entropy conventions.

4. **Ultralocal base dynamics.** With no derivative or nonlocal kernel involving \(q_i\) and \(s_i\), perturbations at distinct base points do not couple. This does not invalidate a static direct integral, but it falsifies any claim of base propagation.

5. **Pure-gauge transport.** If every comparison map is \(U_iU_j^{-1}\), cycle holonomy is trivial. Nontrivial curvature requires an independent connection or link field.

6. **Noncompact gauge escape.** Unqualified minimizer and Gibbs-normalization claims can fail for raw \(\mathrm{GL}^{+}(K)\) because of noncompact gauge directions and infinite volume. A first theorem should use compact gauge data or explicit gauge fixing and coercivity.

7. **Fixed-joint representation obstruction.** On the scoped open factorized family, moving-peer KL has a nonzero mixed third variation while an ordinary fixed-joint ELBO does not. This blocks only that representation; it does not block the action itself or a configuration-level Gibbs lift.

