# Canonical Dependence Selection and Identifiable Quotient Design

**Date:** 2026-08-14
**Status:** Approved design
**Repository baseline:** `0b4bf580d99ca1be640367003c2528ca47d9b7a5`
**Theory tier:** finite, normalized, strictly positive where Fisher smoothness is used

## Purpose

The current theory proves that retained VFE and retained Fisher information descend across a finite observational presentation equivalence once the retained joint law is supplied. It also constructs one explicit six-bit collective joint lift whose singleton marginals coincide with the displayed paired sections. What remains open is selection: whether the displayed marginal sections themselves canonically determine a nonproduct collective law, or whether dependence must be supplied as relational state or relational law.

This design freezes the next theory gate. It separates three meanings of canonicality that must not be conflated:

1. **Monoidal-product canonicality:** naturality under independent local stochastic processing.
2. **Reference-relative canonicality:** uniqueness relative to a declared positive reference or posterior.
3. **Identifiable-quotient canonicality:** invariance of first-order retained-law directions after invisible presentation directions are quotiented out.

There is no unqualified claim that marginal sections alone select a nonproduct law or autonomous agents.

## Existing boundary

The design builds directly on two certified finite results.

- `docs/derivations/2026-08-13-finite-presentation-descent-joint-fisher/` proves that collapsed retained VFE and retained Fisher geometry descend when presentations have the same retained joint law and completed retained conditioning algebra. Full auxiliary VFE, full Fisher geometry, node inventory, and typed interventions do not generally descend.
- `docs/derivations/2026-08-14-collective-joint-lift-fisher/` constructs the parity lift `Q_{theta,kappa}`. It is one smooth line in the 57-dimensional fiber obtained by fixing the six singleton marginals. Along this parity line all 63 proper marginals remain fixed, while the full all-proper-marginal fiber is one-dimensional. The displayed sections select neither `kappa` nor the hyperedge record law.

The new gate is not another existence witness and does not revisit either theorem. It classifies selection rules, gives the strongest reference-relative replacement, and identifies exactly what first-order information survives presentation redundancy.

## Frozen absolute target

For each finite nonempty typed list `X = (X_i)`, define

```text
J(X) = Delta(product_i X_i)
M(X) = product_i Delta(X_i)
m_X : J(X) -> M(X)
```

where `m_X` extracts the declared singleton or disjoint-block marginals. The absolute target asks whether there exists a family of single-valued, law-valued sections

```text
S_X : M(X) -> J(X),       m_X S_X = identity,
```

that simultaneously satisfies all of the following.

1. It is natural under every coordinatewise finite Markov kernel.
2. It extends naturally to every admitted marginal-compatible arity-changing presentation kernel, including correlation-generating split refinements.
3. It is faithful to every compatible full joint law: `S_X(m_X Q) = Q` whenever `Q` is an admitted positive joint presentation.
4. Marginal data alone recover each of the following independently typed objects for every compatible enrichment:
   - full-joint VFE for every compatible recognition law and generative law;
   - full-joint Fisher information for every compatible positive `C^1` parameterized family; and
   - typed intervention semantics for every compatible enriched causal/intervention structure.

Recovery of one joint law at one parameter is not treated as recovery of a statistical family, a VFE model, or an intervention structure.

The three recovery conjuncts are typed factorization predicates through `m_X`:

- **Full-joint VFE factorization:** there is one `V_X : M(X) x M(X) x (0,infinity) -> extended-real` such that `V_X(m_X Q,m_X P,z) = -log z + KL(Q || P)` for every compatible recognition law `Q`, positive posterior law `P`, and evidence `z`.
- **Full-joint Fisher factorization:** whenever two positive `C^1` families `p_0,p_1 : Theta -> J(X)` have `m_X p_0 = m_X p_1` as maps, their pulled-back full-joint Fisher tensors are equal on `Theta`; equivalently the tensor assignment factors through the complete marginal family, not merely one law value.
- **Typed-intervention factorization:** every two enriched presentations with the same marginal observational datum are isomorphic in the declared typed causal/intervention category, and a reconstruction is a section of the forgetful map up to that type-preserving intervention isomorphism.

A "compatible enrichment" is therefore an object in the relevant declared domain whose forgetful image is the supplied marginal datum; it is not inferred from that datum. Equality for VFE means equality in the extended reals with the same evidence convention, Fisher equality means equality of tensors on the same parameter base, and intervention equality means the declared type-preserving causal isomorphism.

Each recovery predicate receives its own atomic claim, dependency path, terminal disposition, and strongest conditional replacement before the absolute target may close.

This is an existential target with universal internal quantifiers. The negative certificate kind is `NONEXISTENCE_PROOF`. The intended terminal result is `COMPLETE_NEGATIVE` if the direct contradictions below survive certification. Each conjunct must nevertheless receive its own disposition and strongest conditional replacement.

## Mathematical categories

### Fixed-arity local category

At fixed arity, a morphism is a tuple of finite Markov kernels `K_i : X_i -> Y_i`. It acts by

```text
J(K) = (tensor_i K_i)_#
M(K) = product_i (K_i)_#.
```

The tensor product declares independent channel randomness. Marginalization is a natural transformation `m : J => M`.

### Marginal-compatible presentation category

An arity-changing kernel

```text
K : product_i X_i -> product_j Y_j
```

is marginal-compatible when there exists `K_bar` satisfying

```text
m_Y K_# = K_bar m_X.
```

Because `m_X` is surjective through product couplings, `K_bar` is unique when it exists. Interaction-sensitive maps such as XOR often fail this condition: their output law depends on source dependence rather than on source marginals. Such maps require relational input and do not act on the marginal-only category.

### Presentation equivalence

The August 13 equivalence remains authoritative for descent: equality of the complete retained joint law and completed retained conditioning algebra, parameterwise for Fisher claims. Equality of singleton marginals is strictly weaker and is not a presentation equivalence for full-joint objects.

## Theorem program

### T1. Unique local Markov-natural selector

On every fixed finite arity, the product selector

```text
S_X(mu_1,...,mu_n) = tensor_i mu_i
```

is the unique natural section under all coordinatewise finite Markov kernels. Preparation kernels from the singleton object force the formula. No continuity, positivity, or entropy argument is needed.

The stronger classification states that any wide category containing all local kernels admits a natural marginal section exactly when every additional morphism preserves product laws. The product-preserving marginal-compatible kernels form the maximal such category.

Interpretation: independence is not derived without assumptions; it is the unique rule compatible with the declared independent monoidal channel structure.

### T2. Correlation-generating refinement no-go

For a fair source bit `u`, use the smooth support-fixed split family

```text
R_rho(y,z | x)
  = 1[y=x] (1+rho)/2,  when z=x,
  = 1[y=x] (1-rho)/2,  when z!=x,
```

with `|rho| < 1`. The kernel has structural zeros from `1[y=x]`, while its output joint law is strictly positive:

```text
Q_rho(y,z) = (1 + rho (-1)^(y xor z)) / 4,
```

and every `Q_rho` has the same two fair marginals. Naturality under two distinct `R_rho` values would require one selected law to equal two distinct joint laws. Choosing different absolute correlations makes the contradiction survive every sample relabeling.

Combined with T1, naturality under any one nonproduct `R_rho` already contradicts the forced product selector.

### T3. Faithful reconstruction no-go

Marginalization is noninjective. Therefore no section can also be a quasi-inverse satisfying `S m = identity` on all admitted joints. The binary `Q_rho` family is the minimal witness.

The current parity lift sharpens this at the Fisher level. At the symmetric point,

```text
G_kappa = 4 / (1 - (kappa/64)^2) I_6.
```

All displayed marginals are identical, but compatible full-joint Fisher tensors differ positively for `kappa=0` and `kappa=1/2`. No marginal-only tensor can equal every compatible full-joint tensor.

Typed interventions are also not recoverable from the observational quotient, as the certified direct/latent/null BSC presentations already prove.

### T4. Reference-relative entropic selector

For finite `X`, reference `p`, statistics `T`, and feasible moment `m`, define

```text
q_(p,m) = argmin { KL(q || p) : E_q T = m }.
```

A finite minimizer exists exactly when `m` lies in the convex hull of `T(supp p)`, and it is then unique as a law. For `p > 0` and `m` in the relative interior of the moment polytope, the law `q_(p,m)` is analytic on every fixed minimal-support stratum and has exponential form

```text
q_(p,m)(x) = p(x) exp(lambda(m) . T(x) - psi(lambda)).
```

The multiplier is unique only after replacing `T` by a minimal statistic; otherwise it is unique modulo affine redundancies that leave the law unchanged. On the minimal face containing `m`, with the usual finite-KL support convention, every feasible `q` obeys the exact oriented identity

```text
KL(q || p) = KL(q || q_(p,m)) + KL(q_(p,m) || p).
```

Equivariance holds only when the reference and constraint diagram are transported coherently. On a Frechet marginal fiber, higher-order log-linear interaction contrasts are inherited from `p`; they are not derived from the marginals.

Uniform or product reference gives the product selector. A correlated reference selects its own correlation when already feasible. Thus the positive theorem makes the extra relational input explicit.

### T5. Deterministic posterior completion

For deterministic `f : X -> Y`, reference `p`, and target `r << f_# p`, the unique KL-minimizing lift is

```text
L_f^p(r)(x) = r(f(x)) p(x) / (f_#p)(f(x))
```

on fibers with positive pushed-reference mass, and set `L_f^p(r)(x)=0` on zero-reference fibers. The hypothesis `r << f_#p` makes this convention normalized and removes every `0/0` ambiguity. KL disintegration proves uniqueness and the exact excess conditional KL. For `X -> Y -> Z`, completion composes strictly when each stage uses the pushed reference. An arbitrary stochastic channel need not admit a stochastic section, so no analogous right inverse is asserted without that extra hypothesis.

With the retained posterior as reference, this becomes a VFE-minimizing recognition closure. Across August 13-equivalent presentations, the retained optimizer and optimized VFE value descend. A separate parameterized envelope statement requires positive `C^1` posterior, evidence, and reference families; a common locally fixed feasible set and support stratum; a unique `C^1` optimizer; and differentiation with respect to the declared retained parameter. Under those hypotheses, the envelope identity is obtained by differentiating the objective at the optimizer, and the retained differential descends when the retained objective family agrees parameterwise. Presentation-specific auxiliary completions do not.

### T6. Retained-law Fisher quotient

Let `rho : Theta -> M` be `C^1`, let `g` be a positive-semidefinite Fisher tensor, and set `h = rho^* g`. Pointwise,

```text
rad h_theta = (d rho_theta)^(-1)(rad g_(rho(theta))).
```

On the interior finite simplex, `g` is positive definite, so `rad h = ker d rho`. Constant rank is needed only for the smooth vector-bundle quotient

```text
Q = T Theta / ker d rho,
```

whose metric is canonically isometric to `im d rho`. A global quotient manifold still requires a simple regular quotient; constant rank alone is insufficient.

Presentation isometry requires a familywise commuting diagram and a Fisher isometry, not equality at one parameter and not a generic information-contracting Markov map.

### T7. Declared-block attribution and law-only agentization no-go

Given declared node blocks `T Theta = direct_sum_a B_a`, define `E_a = d rho(B_a)`. Unique quotient-tangent decomposition relative to those blocks holds exactly when

```text
im d rho = direct_sum_a E_a,
```

equivalently when the invisible kernel splits blockwise. Additive Fisher-energy attribution additionally requires pairwise Fisher orthogonality, `g(E_a,E_b)=0` for `a != b`. To descend across a retained-law fiber, the image subspaces must form smooth subbundles and the induced subspaces or orthogonal projectors must be basic along the fiber and natural up to typed permutation.

This does not manufacture agents from law/Fisher data. At the uniform point of the seven-outcome simplex, the six-dimensional standard `A_7` representation is irreducible. A natural decomposition into three rank-two node spaces would induce `A_7 -> S_3`, necessarily trivial, which would make each rank-two space invariant and contradict irreducibility. Outcome typing, node blocks, marginal projections, or another symmetry-breaking tensor must be supplied.

### T8. Promoted parity interaction direction

If `kappa` is promoted in the current lift, `(theta,kappa) -> Q_(theta,kappa)` has rank seven. Singleton marginalization maps `(theta,kappa) -> theta` and kills exactly the `partial_kappa` direction. The full-joint Fisher quotient therefore contains six declared marginal directions plus one declared relational direction, while the singleton quotient cannot see the relation.

Typing the seventh direction as relational is an input convention. Fisher geometry establishes identifiability at the chosen retained scope, not autonomous agency.

## Executable witness design

Create `docs/derivations/2026-08-14-canonical-dependence-selection/evidence/exact_selection_witness.py` and `tests/test_canonical_dependence_selection_witness.py`.

The witness uses `fractions.Fraction` for probability, marginal, Markov-kernel, derivative, and Fisher calculations. Floating point is permitted only for displayed logarithmic KL/VFE values, with the claim ledger labeling those checks as numerical corroboration.

Required exact checks are:

1. normalization and common marginals of `Q_rho`;
2. product selection forced by preparation kernels;
3. distinct positive correlated refinements with the same marginal data;
4. failure of a faithful marginal quasi-inverse;
5. exact dependence Fisher `1/(1-rho^2)`;
6. deterministic completion normalization, target pushforward, uniqueness defect, and strict composition;
7. reference dependence under `p_rho`;
8. retained Fisher radical/kernel identities for exact finite Jacobians;
9. rank-seven promoted parity map and loss of `partial_kappa` under singleton marginalization;
10. deterministic JSON output.

The tests must be written and observed failing before the witness implementation. Persist RED and GREEN JUnit artifacts, a test-source snapshot, and a TDD record inside the derivation package.

## Durable artifacts and integration

The rigorous run lives at `docs/derivations/2026-08-14-canonical-dependence-selection/` and contains all nine required rigorous-theory-search artifacts plus contained evidence files.

After certification, propagate only the verified boundary into:

- `Theory/05d_relational_inference.tex`
- `Theory/SPEC.md`
- `Theory/appendix_claim_ledger.tex`
- `overview.md`
- `docs/STATUS.md`
- `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md`

The August 13 and August 14 packages remain immutable historical certificates. Cross-reference them; do not rewrite them.

## Verification and release

The mathematical target requires direct derivations, not consensus or numerical agreement. Certification includes:

- a mechanism-diverse portfolio;
- direct proofs for every target ancestor;
- exact counterexamples and nonexistence proof;
- an isolated falsifier;
- an independent reconstruction from the frozen contract;
- oracle-erasure evidence showing that the result survives removal of the search prior;
- a deterministic exact-arithmetic witness, source snapshot, RED and GREEN JUnit records, and a TDD record;
- one skeptic and one adjudicator for the absolute target, plus independent category-theory, variational, Fisher/representation, and implementation/provenance views;
- a claim ledger, dependency DAG, adversarial report, release record, and SHA-256 bindings for every durable evidence artifact; and
- a final repository verification ledger bound to the exact final Git commit and worktree digest.

Mathematics claims are eligible for `EVIDENCE_VERIFIED` or `REFUTED` only through contained derivations or a formal proof. Exact executable checks corroborate finite identities but do not replace proofs. Code claims require current JUnit or deterministic execution evidence. Missing hypotheses, unresolved adversarial attacks, stale hashes, or a changed artifact revision force `INCONCLUSIVE` or a restarted verification run.

The rigorous package may declare `COMPLETE_NEGATIVE` only when the existential absolute target is directly refuted, every dependency is closed, all sustained attacks are resolved or explicitly narrow a claim, every evidence hash matches LF-normalized committed bytes, and the following command exits zero:

```powershell
C:\Python314\python.exe "C:\Users\chris and christine\.agents\skills\rigorous-theory-search\scripts\validate_run.py" --mode release docs\derivations\2026-08-14-canonical-dependence-selection
```

After the final tracked commit, start a fresh schema-1.1 closure ledger and require:

```powershell
C:\Python314\python.exe "C:\Users\chris and christine\.claude\skills\verification\scripts\verification_gate.py" validate .verification\ledger.json --cwd .
```

Release is aborted if either validator fails, if the target digest or contract binding drifts, if a reviewer sustains a Critical/High/Medium defect, or if local `main`, `origin/main`, and the published feature tip cannot be proven to share the intended fast-forward ancestry.
