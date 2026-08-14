# Canonical Dependence Selection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove the finite canonical-selector no-go, construct the strongest reference-relative and identifiable-quotient replacements, integrate the verified boundary into the central theory, and publish a revision-bound certificate.

**Architecture:** A rigorous-theory-search package owns the frozen existential target, direct nonexistence proof, conditional positive theorems, counterexamples, and adversarial evidence. A pure exact-arithmetic witness corroborates finite identities under TDD. Central Theory and overview documents receive only claims certified by the package; the August 13 and August 14 certificates remain unchanged.

**Tech Stack:** Python 3.14 standard library (`fractions`, `itertools`, `json`, `math`), pytest, LaTeX/pdflatex, rigorous-theory-search validator, verification schema 1.1, Git worktrees.

**Spec:** `docs/superpowers/specs/2026-08-14-canonical-dependence-selection-design.md`

## Global Constraints

- Work only in `codex/canonical-dependence-selection-20260814`, based on `origin/main` commit `0b4bf580d99ca1be640367003c2528ca47d9b7a5`.
- Use the finite normalized-law tier. Positivity is required only where Fisher smoothness, analytic I-projection, or finite KL requires it.
- The absolute target is existential and uses `negative_certificate_kind = NONEXISTENCE_PROOF`.
- Product selection is canonical only under independent coordinatewise Markov channels; no text may call it an assumption-free derivation of independence.
- Every nonproduct positive selector must name its reference, posterior, interaction coordinate, shared kernel, constraint, or intervention data.
- Quotient-level node decomposition is relative to declared smooth, basic typed blocks. Additive Fisher-energy attribution additionally requires pairwise Fisher orthogonality. Neither establishes autonomous agency, causal ownership, or intervention identity.
- Do not edit either `docs/derivations/2026-08-13-finite-presentation-descent-joint-fisher/` or `docs/derivations/2026-08-14-collective-joint-lift-fisher/`.
- Exact probability, marginal, derivative, Markov-kernel, and Fisher checks use `fractions.Fraction`. Logarithmic KL/VFE evaluations are floating corroboration and must be labeled accordingly.
- Mathematical closure requires direct derivations. Tests and symbolic checks do not prove theorem claims.
- Use American English in all new prose and code.
- CPU commands use `C:\Python314\python.exe`, `CUDA_VISIBLE_DEVICES=-1`, `PYTHONHASHSEED=0`, and absent `MULTIAGENTELBO_RUN_CUDA_TESTS`, `VFE3_TEST_DEVICE`, and `CUBLAS_WORKSPACE_CONFIG`.
- Every persisted JUnit file under the run package uses LF bytes and is hash-bound before release.
- The final rigorous package must pass `validate_run.py --mode release`; the final closure ledger must pass the installed verification gate against the final commit.

---

### Task 1: Scaffold the frozen run and establish witness RED

**Files:**
- Create: `docs/derivations/2026-08-14-canonical-dependence-selection/` through the rigorous scaffold
- Create: `tests/test_canonical_dependence_selection_witness.py`
- Create: `docs/derivations/2026-08-14-canonical-dependence-selection/evidence/red-junit.xml`
- Create: `docs/derivations/2026-08-14-canonical-dependence-selection/evidence/tdd-record.md`

**Interfaces:**
- Consumes: the approved spec and rigorous-theory-search templates.
- Produces: the nine scaffold artifacts, frozen target fields, a failing executable contract, and the API required by Task 2.

- [ ] **Step 1: Scaffold the run**

Run from the repository root:

```powershell
C:\Python314\python.exe "C:\Users\chris and christine\.agents\skills\rigorous-theory-search\scripts\scaffold_run.py" --date 2026-08-14 --slug canonical-dependence-selection docs\derivations
```

Confirm the run contains exactly the nine required root artifacts before adding `evidence/`.

- [ ] **Step 2: Freeze the target before opening proof routes**

Set the target statement to the existential family-of-sections question in the spec. Use:

```json
{
  "quantifier_class": "EXISTENTIAL",
  "negative_certificate_kind": "NONEXISTENCE_PROOF",
  "search_priors": ["SEARCH_PRIOR_AFFIRMATIVE"]
}
```

The prose quantifier must range over one family `S_X` and require all local kernels, all admitted marginal-compatible presentation refinements, and independent faithful recovery targets for compatible full-joint VFE models, positive `C^1` Fisher families, and enriched intervention structures. Canonically serialize the complete target, compute its SHA-256, and propagate the resulting `contract_id` and `target_digest` to every scaffold artifact. Do not place the search prior anywhere except `target.search_priors`.

- [ ] **Step 3: Write the failing witness tests**

The test module loads:

```python
ROOT = Path(__file__).resolve().parents[1]
WITNESS = ROOT / (
    "docs/derivations/2026-08-14-canonical-dependence-selection/"
    "evidence/exact_selection_witness.py"
)
```

Require these public functions:

```python
q_rho(rho: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]
singleton_marginals(law) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]
product_coupling(left, right) -> tuple[Fraction, ...]
preparation_pushforward(left, right) -> tuple[Fraction, ...]
split_pushforward(rho: Fraction) -> tuple[Fraction, ...]
faithful_quasi_inverse_counterexample(rho_a: Fraction, rho_b: Fraction) -> dict[str, object]
dependence_fisher(rho: Fraction) -> Fraction
pushforward(law, coarse_map, coarse_size) -> tuple[Fraction, ...]
deterministic_completion(reference, coarse_map, target) -> tuple[Fraction, ...]
completion_conditional_defect(reference, coarse_map, target, candidate) -> Fraction
reference_selector_control(rho: Fraction) -> dict[str, object]
matrix_rank(matrix) -> int
bsc_retained_quotient(a: Fraction, b: Fraction) -> dict[str, object]
promoted_parity_rank() -> dict[str, object]
main() -> int
```

Write separate tests asserting:

```python
assert q_rho(Fraction(1, 3)) == (
    Fraction(1, 3), Fraction(1, 6), Fraction(1, 6), Fraction(1, 3)
)
assert singleton_marginals(q_rho(Fraction(1, 3))) == (
    (Fraction(1, 2), Fraction(1, 2)),
    (Fraction(1, 2), Fraction(1, 2)),
)
assert dependence_fisher(Fraction(1, 3)) == Fraction(9, 8)
assert sorted(q_rho(Fraction(1, 3))) != sorted(q_rho(Fraction(1, 2)))
assert preparation_pushforward((Fraction(1, 3), Fraction(2, 3)), (Fraction(1, 4), Fraction(3, 4))) == product_coupling((Fraction(1, 3), Fraction(2, 3)), (Fraction(1, 4), Fraction(3, 4)))
quasi = faithful_quasi_inverse_counterexample(Fraction(1, 3), Fraction(1, 2))
assert quasi["same_marginals"]
assert quasi["distinct_joints"]
assert quasi["distinct_relabeling_orbits"]
```

For deterministic completion, use the eight-state reference `p_x = (1,2,3,4,5,6,7,8)/36`, `f=(0,0,1,1,2,2,3,3)`, `g=(0,0,1,1)`, and target `(1/3,2/3)`. Assert exact target pushforward and equality of direct and staged completion.

Construct one distinct feasible candidate with the same target pushforward. Require `completion_conditional_defect` to be exactly zero for the selected completion and strictly positive for that candidate; logarithmic conditional-KL excess remains explicitly labeled floating corroboration.

For the BSC quotient, use `a=1/5`, `b=1/4`; assert retained rank one and that the two exact kernel vectors are killed by both the Jacobian and pulled-back Fisher matrix.

For two nonzero `rho` values, assert `reference_selector_control` returns the feasible reference itself, preserves the same marginal target, and selects different correlated laws as the reference changes.

For promoted parity, assert full-joint derivative rank seven, singleton derivative rank six, and singleton kernel generator `(0,0,0,0,0,0,1)`.

Finally call `main()` twice, parse JSON, and require byte-identical output.

- [ ] **Step 4: Run RED and preserve machine evidence**

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
$env:PYTHONHASHSEED='0'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
C:\Python314\python.exe -m pytest tests\test_canonical_dependence_selection_witness.py -q -p no:cacheprovider --basetemp=C:\tmp\maelbo-selector-red-20260814 --junitxml=docs\derivations\2026-08-14-canonical-dependence-selection\evidence\red-junit.xml
```

Expected result: failures caused only by the absent `exact_selection_witness.py` or missing required API. Record the command, exit status, failing test names, and expected reason in `evidence/tdd-record.md`.

- [ ] **Step 5: Validate the checkpoint and commit**

```powershell
C:\Python314\python.exe "C:\Users\chris and christine\.agents\skills\rigorous-theory-search\scripts\validate_run.py" --mode checkpoint docs\derivations\2026-08-14-canonical-dependence-selection
git diff --check
git add -- docs/derivations/2026-08-14-canonical-dependence-selection tests/test_canonical_dependence_selection_witness.py
git commit -m "test: freeze canonical selection theorem contract"
```

---

### Task 2: Implement the exact finite witness and reach GREEN

**Files:**
- Create: `docs/derivations/2026-08-14-canonical-dependence-selection/evidence/exact_selection_witness.py`
- Modify: `tests/test_canonical_dependence_selection_witness.py`
- Modify: `docs/derivations/2026-08-14-canonical-dependence-selection/evidence/tdd-record.md`
- Create: `docs/derivations/2026-08-14-canonical-dependence-selection/evidence/green-junit.xml`
- Create: `docs/derivations/2026-08-14-canonical-dependence-selection/evidence/test_canonical_dependence_selection_witness.snapshot.py`

**Interfaces:**
- Consumes: the exact API and fixtures frozen by Task 1.
- Produces: deterministic exact corroboration consumed by the proof package and later code verification.

- [ ] **Step 1: Implement the binary family and local selector controls**

Use state order `(00,01,10,11)`:

```python
def q_rho(rho: Fraction):
    return (
        (1 + rho) / 4,
        (1 - rho) / 4,
        (1 - rho) / 4,
        (1 + rho) / 4,
    )
```

Implement exact marginalization, product coupling, preparation-kernel pushforward, split pushforward, the faithful quasi-inverse counterexample, and the feasible-reference selector control.

Compute Fisher information from the categorical atom derivatives rather than returning the target formula:

```python
def dependence_fisher(rho: Fraction) -> Fraction:
    law = q_rho(rho)
    derivatives = (Fraction(1, 4), Fraction(-1, 4), Fraction(-1, 4), Fraction(1, 4))
    return sum((derivative * derivative) / atom for atom, derivative in zip(law, derivatives))
```

The test independently compares this score-sum result with `1/(1-rho^2)`. It must fail under a mutated derivative sign or atom denominator.

Reject `abs(rho) >= 1` in strictly positive witness paths.

- [ ] **Step 2: Implement deterministic completion and composition**

For each coarse cell `y`, compute `p_y = sum_{f(x)=y} p_x`, require `target_y == 0` when `p_y == 0`, and otherwise return

```python
q_x = target[f_x] * reference[x] / pushed_reference[f_x]
```

Validate normalization and exact pushforward. The staged composition fixture must equal the direct completion cell by cell. Implement the exact cross-product conditional defect so it is zero exactly at posterior completion and positive for the declared distinct feasible candidate.

- [ ] **Step 3: Implement exact rank controls**

Implement fraction-preserving Gaussian elimination in `matrix_rank`.

For the BSC retained map `p=a+b-2ab`, use Jacobian

```python
j = (1 - 2*b, 1 - 2*a, 0)
```

and Fisher pullback `h = outer(j,j)/(p(1-p))`. Return the exact kernel generators `(1-2*a, -(1-2*b), 0)` and `(0,0,1)`.

For the promoted parity map, build the 64-by-7 derivative matrix at `theta=(1/2)^6`, `kappa=1/2` using the existing parity-lift formula. Return full rank seven, marginal rank six, and the exact singleton-null `kappa` direction.

- [ ] **Step 4: Emit deterministic JSON**

Serialize every `Fraction` as `numerator` or `numerator/denominator`, use sorted keys, and include no timestamps, paths, host data, or random values. `main()` prints one JSON document and returns zero.

- [ ] **Step 5: Run GREEN, snapshot source, and commit**

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
$env:PYTHONHASHSEED='0'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
C:\Python314\python.exe -m pytest tests\test_canonical_dependence_selection_witness.py -q -p no:cacheprovider --basetemp=C:\tmp\maelbo-selector-green-20260814 --junitxml=docs\derivations\2026-08-14-canonical-dependence-selection\evidence\green-junit.xml
Copy-Item -LiteralPath tests\test_canonical_dependence_selection_witness.py -Destination docs\derivations\2026-08-14-canonical-dependence-selection\evidence\test_canonical_dependence_selection_witness.snapshot.py
git diff --check
git add -- docs/derivations/2026-08-14-canonical-dependence-selection/evidence tests/test_canonical_dependence_selection_witness.py
git commit -m "test: add exact canonical selection witness"
```

Append RED-to-GREEN commands and exact JUnit totals to `tdd-record.md`. Do not call the logarithmic checks exact arithmetic.

---

### Task 3: Prove selector classification and reference-relative completion

**Files:**
- Create: `docs/derivations/2026-08-14-canonical-dependence-selection/evidence/natural-selector-no-go-proof.md`
- Create: `docs/derivations/2026-08-14-canonical-dependence-selection/evidence/reference-relative-selection-proof.md`
- Create: `docs/derivations/2026-08-14-canonical-dependence-selection/evidence/recovery-factorization-no-go-proof.md`
- Modify: `docs/derivations/2026-08-14-canonical-dependence-selection/construction-or-strongest-theorem.md`
- Modify: `docs/derivations/2026-08-14-canonical-dependence-selection/counterexample-register.md`

**Interfaces:**
- Consumes: the frozen categories and exact finite controls.
- Produces: direct mathematical evidence for selector uniqueness, maximality, nonexistence, each typed recovery-factorization no-go, I-projection, completion, and retained descent.

- [ ] **Step 1: Write the local naturality and maximal-category proof**

Prove product uniqueness with preparation kernels from singleton objects. Then prove: a wide marginal-compatible category containing all local kernels admits a natural section if and only if every additional morphism preserves product laws. State both directions and the uniqueness conclusion.

- [ ] **Step 2: Write the refinement and faithfulness nonexistence proofs**

Use two `R_rho` values with unequal absolute correlations. Prove normalization, common marginals, distinct atom multisets, marginal compatibility, and contradiction with one law-valued selector. Separately prove that `m` is noninjective and hence no section can satisfy `S m = identity` on every compatible joint.

- [ ] **Step 3: Prove the three typed recovery-factorization no-gos**

In `evidence/recovery-factorization-no-go-proof.md`, refute the VFE factorization with a fixed product posterior and two recognition joints having identical displayed marginals but unequal KL/VFE values. Refute the Fisher factorization with the `kappa=0` and `kappa=1/2` parity families, whose singleton marginal maps agree while their pulled-back full-joint Fisher tensors differ at the symmetric point. Refute typed-intervention factorization with the certified August 13 direct/latent/null BSC presentations, whose retained observational law agrees while the enriched intervention structures are nonisomorphic.

Give each factorization predicate its own theorem, witness, assumptions, dependency edge, and conditional replacement. Bind `RECOVERY-FULL-VFE-NOGO`, `RECOVERY-FULL-FISHER-NOGO`, and `RECOVERY-TYPED-INTERVENTION-NOGO` directly to this proof artifact. Propagate all three bounded results to `Theory/05d_relational_inference.tex`, `Theory/SPEC.md`, `Theory/appendix_claim_ledger.tex`, `overview.md`, `docs/STATUS.md`, and the chronological worklog in Task 6.

- [ ] **Step 4: Write the finite I-projection theorem**

Prove existence exactly on `conv T(supp p)`, uniqueness of the finite minimizer as a law, exact support on the minimal face, exponential form after statistic minimalization, multiplier uniqueness modulo affine redundancies, the oriented Pythagorean identity with support conventions, analytic dependence on each fixed relative-interior support stratum, and transported-reference equivariance. State support failure and boundary-smoothness counterexamples.

- [ ] **Step 5: Write deterministic completion, composition, and VFE descent**

Derive the conditional KL chain and the exact lift `L_f^p`, including the zero-reference-fiber convention. Prove strict composition for deterministic nested coarse maps using pushed references. Specialize to the retained posterior and prove that the retained optimizer and optimum VFE descend under the August 13 equivalence while the full auxiliary law does not. Prove the envelope differential only for a positive `C^1` parameterized family with a common locally fixed feasible set/support stratum and a unique `C^1` optimizer.

- [ ] **Step 6: Self-check quantifiers and commit**

Search every use of `canonical`, `natural`, `unique`, `smooth`, and `descend`. Each occurrence must carry its morphism class, reference, support/stratum, or equivalence hypotheses in the same paragraph.

```powershell
git diff --check
git add -- docs/derivations/2026-08-14-canonical-dependence-selection
git commit -m "docs: prove finite dependence selection boundary"
```

---

### Task 4: Prove the retained Fisher quotient and agentization boundary

**Files:**
- Create: `docs/derivations/2026-08-14-canonical-dependence-selection/evidence/fisher-quotient-agentization-proof.md`
- Modify: `docs/derivations/2026-08-14-canonical-dependence-selection/construction-or-strongest-theorem.md`
- Modify: `docs/derivations/2026-08-14-canonical-dependence-selection/counterexample-register.md`

**Interfaces:**
- Consumes: the retained-law map and current parity lift.
- Produces: exact radical, quotient, presentation-isometry, declared-block, law-only no-go, and promoted-interaction claims.

- [ ] **Step 1: Prove the pointwise radical and quotient theorem**

Prove `rad(rho^*g) = d rho^(-1)(rad g)` for a PSD tensor. State the exact iff condition for reduction to `ker d rho`. Use constant rank only to obtain smooth kernel, image, and quotient bundles. Separate the fiberwise quotient metric from a global quotient manifold.

- [ ] **Step 2: Prove presentation isometry**

For `rho_B F = J rho_A`, with `F` a diffeomorphism and `J` a Fisher isometry, prove kernel transport and quotient isometry. State the surjective-submersion variant and explain why a generic Markov contraction is insufficient.

- [ ] **Step 3: Prove the declared-block equivalence and basicness requirement**

Prove equivalence of quotient direct sum, image direct sum, blockwise kernel splitting, and unique quotient-tangent decomposition. Prove that additive Fisher-energy attribution additionally requires pairwise Fisher orthogonality. Add the rotating-block counterexample showing that pointwise directness and orthogonality do not imply descent along a retained-law fiber without smooth/basic image subbundles.

- [ ] **Step 4: Prove the finite law-only agentization no-go**

At the uniform seven-outcome law, prove that a natural three-by-two decomposition would give `A_7 -> S_3`, that the homomorphism is trivial, and that the six-dimensional sum-zero representation is irreducible by its scalar commutant. Conclude only that law/Fisher data cannot manufacture those blocks without typing or another symmetry-breaking structure.

- [ ] **Step 5: Prove the promoted-parity rank statement and commit**

Show that singleton marginalization of a zero derivative first forces the six `theta` components to vanish and then forces the `kappa` component to vanish in the full-joint family. Contrast with singleton marginalization, whose kernel is exactly `span(partial_kappa)`.

```powershell
git diff --check
git add -- docs/derivations/2026-08-14-canonical-dependence-selection
git commit -m "docs: establish identifiable Fisher quotient boundary"
```

---

### Task 5: Assemble and release-validate the rigorous theory package

**Files:**
- Modify: all nine root artifacts under `docs/derivations/2026-08-14-canonical-dependence-selection/`
- Create: `evidence/independent-reconstruction.md`
- Create: `evidence/oracle-erasure.md`
- Create: `evidence/adversarial-attacks.md`

**Interfaces:**
- Consumes: Tasks 1-4 proof and witness artifacts.
- Produces: one `COMPLETE_NEGATIVE` certificate and verified conditional replacement claims.

- [ ] **Step 1: Populate the mechanism portfolio**

Register separate families for product naturality, correlated refinement obstruction, faithful-quasi-inverse obstruction, full-VFE recovery obstruction, full-Fisher recovery obstruction, typed-intervention recovery obstruction, maximum entropy, reference I-projection, deterministic completion, Fisher quotient, declared-block attribution, and intervention-enriched agentization. Retire routes only with an exact reason.

- [ ] **Step 2: Populate atomic claims and dependency DAG**

Use stable IDs:

```text
TARGET-ABSOLUTE-CANONICAL-SELECTOR
RECOVERY-FULL-VFE-NOGO
RECOVERY-FULL-FISHER-NOGO
RECOVERY-TYPED-INTERVENTION-NOGO
SEL-PRODUCT-UNIQUENESS
SEL-MAXIMAL-PRODUCT-CATEGORY
SEL-CORRELATED-REFINEMENT-NOGO
SEL-FAITHFUL-QUASI-INVERSE-NOGO
SEL-REFERENCE-IPROJECTION
SEL-DETERMINISTIC-COMPLETION
SEL-PRESENTATION-DESCENT
FISHER-RETAINED-QUOTIENT
FISHER-DECLARED-BLOCK-ATTRIBUTION
AGENT-LAW-ONLY-DECOMPOSITION-NOGO
PARITY-PROMOTED-RANK
SELECTION-WITNESS-REGRESSION
```

The target's negative certificate depends only on the typed category definitions and the direct nonexistence proof. Each of the three independently typed recovery predicates has its own claim and terminal disposition before release. Positive replacement claims remain independently certified and must not be smuggled in as premises of the refutation.

- [ ] **Step 3: Bind evidence and hashes**

Mathematics claims use contained derivation artifacts. The witness claim uses GREEN JUnit and source snapshot as mechanical evidence. RED evidence supports TDD history only. Recompute every SHA-256 from LF worktree bytes after all prose edits.

- [ ] **Step 4: Complete independent reconstruction, attacks, and oracle erasure**

The independent reconstruction starts from `problem-contract.json`, `claim-ledger.json`, and `dependency-dag.json`, not the intended theorem narrative. The attack portfolio must cover target and every ancestor and must include at least: omitted preparation kernels, relabeling quotient, set-valued selector, support-zero I-projection, stochastic coarse channel, nonbasic node blocks, singular Fisher target, and intervention overreach.

Oracle erasure must remove both the literal search prior and any paraphrased assumption that asserts nonexistence, product uniqueness, or the intended ontology conclusion.

- [ ] **Step 5: Release validate and commit**

```powershell
C:\Python314\python.exe "C:\Users\chris and christine\.agents\skills\rigorous-theory-search\scripts\validate_run.py" --mode release docs\derivations\2026-08-14-canonical-dependence-selection
git diff --check
git add -- docs/derivations/2026-08-14-canonical-dependence-selection
git commit -m "docs: certify canonical dependence selection no-go"
```

---

### Task 6: Integrate the certified boundary into the central theory

**Files:**
- Modify: `Theory/05d_relational_inference.tex`
- Modify: `Theory/SPEC.md`
- Modify: `Theory/appendix_claim_ledger.tex`
- Modify: `overview.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md`

**Interfaces:**
- Consumes: released claims and exact boundaries from Task 5.
- Produces: one coherent central statement of what is canonical, what is reference-relative, and what remains explicit relational structure.

- [ ] **Step 1: Add the theorem sequence to `Theory/05d_relational_inference.tex`**

Insert after the finite parity-lift section and before the next natural-gradient characterization. Include typed definitions, product uniqueness, correlated-refinement no-go, all three typed recovery-factorization no-gos, reference-relative completion, retained Fisher quotient, declared-block boundary, and promoted-`kappa` corollary. Every result gets a unique LaTeX label.

- [ ] **Step 2: Update governing summaries**

Add a governing dated correction to `Theory/SPEC.md` and `Theory/appendix_claim_ledger.tex`. Update `overview.md` so “agent-only closure” says:

```text
Local Markov naturality uniquely selects the product law. Nonproduct dependence is not selected by paired sections; it must enter through declared relational state or law. A positive reference/posterior supplies a unique relative selector, and the retained Fisher quotient identifies only the directions visible at the declared retained scope.
```

Keep autonomous agency, interventions, continuum, and physicalization open.

- [ ] **Step 3: Record chronology without rewriting history**

Append new dated sections to `docs/STATUS.md` and the worklog. Do not edit the bodies of the August 13 or August 14 certificates and do not rewrite older worklog entries.
- [ ] **Step 4: Run static, integration, and LaTeX checks**

Use the deterministic CPU environment and run:

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
$env:PYTHONHASHSEED='0'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
C:\Python314\python.exe -m pytest tests\test_markdown_hygiene.py tests\test_canonical_dependence_selection_witness.py -q -p no:cacheprovider --basetemp=C:\tmp\maelbo-selector-integration-20260814 --junitxml=C:\tmp\maelbo-selector-integration-20260814.xml
New-Item -ItemType Directory -Force -Path C:\tmp\maelbo-selector-tex-20260814 | Out-Null
Push-Location Theory
pdflatex -interaction=nonstopmode -halt-on-error -output-directory C:\tmp\maelbo-selector-tex-20260814 main.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory C:\tmp\maelbo-selector-tex-20260814 main.tex
Pop-Location
git diff --check
```

Read JUnit totals from XML. Scan the LaTeX log for fatal errors, undefined controls, duplicate labels, and unresolved references.

- [ ] **Step 5: Commit the central integration**

```powershell
git add -- Theory/05d_relational_inference.tex Theory/SPEC.md Theory/appendix_claim_ledger.tex overview.md docs/STATUS.md docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md
git commit -m "docs: integrate canonical dependence selection boundary"
```

---

### Task 7: Perform independent/adversarial closure and final verification

**Files:**
- Modify as required by review: files owned by Tasks 2-6
- Create: final contained review evidence under `docs/derivations/2026-08-14-canonical-dependence-selection/evidence/`
- Create/update ignored after the final tracked commit: `.verification/ledger.json`

**Interfaces:**
- Consumes: the complete branch and release candidate.
- Produces: revision-bound mathematical, code, source, and integration closure evidence plus a safely published fast-forward.

- [ ] **Step 1: Run independent proof and implementation reviews**

Use separate expert views for naturality/category theory, variational/KL geometry, Fisher quotient/representation theory, and implementation/provenance. The high-severity absolute target requires four views, one skeptic, and one adjudicator. Shared-agent results are adversarial views, not independent empirical corroboration.

- [ ] **Step 2: Repair every load-bearing finding through scoped review loops**

For each source fix, rerun the covering proof check or test and repeat scoped review. Any source change invalidates existing verification evidence. If a repair touches tests, `Theory/`, `overview.md`, `docs/STATUS.md`, or the worklog, stage exactly those repaired paths and make a scoped repair commit immediately after the covering reruns and re-review.

Only after all nonpackage repairs are committed may final review/adjudication artifacts be added to the derivation package, hash-bound, release-validated, and committed in Step 4. Do not start repository closure mode until every tracked source and evidence artifact is committed and the tracked worktree is clean.

- [ ] **Step 3: Run the final deterministic CPU suite**

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
$env:PYTHONHASHSEED='0'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
C:\Python314\python.exe -m pytest -q --basetemp=C:\tmp\maelbo-selector-final-20260814 --junitxml=C:\tmp\maelbo-selector-final-20260814.xml
C:\Python314\python.exe "C:\Users\chris and christine\.agents\skills\rigorous-theory-search\scripts\validate_run.py" --mode release docs\derivations\2026-08-14-canonical-dependence-selection
```

Read totals from JUnit, not console memory. Re-run both LaTeX passes on the exact final source tree.

- [ ] **Step 4: Commit final tracked review artifacts**

```powershell
git diff --check
git add -- docs/derivations/2026-08-14-canonical-dependence-selection
git commit -m "docs: close canonical selection adversarial review"
git status --short --branch
```

Require a clean tracked tree before starting closure mode.

- [ ] **Step 5: Start and validate a fresh schema-1.1 closure ledger**

```powershell
C:\Python314\python.exe "C:\Users\chris and christine\.claude\skills\verification\scripts\verification_gate.py" start --cwd . --ledger .verification/ledger.json --mode closure
```

Populate one atomic ledger claim per check. Give the high target four eligible views, weakest-view criterion aggregation, one skeptic, and one adjudicator. Use direct derivation evidence for mathematics and current JUnit/deterministic evidence for code. The absolute selector claim closes `REFUTED`; proved positive replacements close `EVIDENCE_VERIFIED`; any unresolved obligation closes `INCONCLUSIVE`.

```powershell
C:\Python314\python.exe "C:\Users\chris and christine\.claude\skills\verification\scripts\verification_gate.py" validate .verification/ledger.json --cwd .
```

The ledger's artifact revision and worktree digest must match the final tracked commit. If a tracked byte changes, abandon and restart closure rather than repinning stale evidence.

- [ ] **Step 6: Publish with exact fast-forward checks**

From the feature worktree:

```powershell
git status --short --branch
git push -u origin codex/canonical-dependence-selection-20260814
git fetch --prune origin
git merge-base --is-ancestor origin/main codex/canonical-dependence-selection-20260814
git rev-list --left-right --count origin/main...codex/canonical-dependence-selection-20260814
```

Require `0 <ahead>` and a clean feature worktree. In the clean real `main` checkout:

```powershell
git merge --ff-only codex/canonical-dependence-selection-20260814
git push origin main
git fetch --prune origin
git rev-parse main
git rev-parse origin/main
git ls-remote origin refs/heads/main refs/heads/codex/canonical-dependence-selection-20260814
```

Require local `main`, `origin/main`, and the pushed feature tip to agree. If `origin/main` advances, stop, rebase or rebuild on the remote tip, and re-run revision-bound validation. Never force-push.

- [ ] **Step 7: Offer Research-wiki ingest**

The result is notable and the current wiki lags the August 13-14 theory. Do not edit `C:\Users\chris and christine\Desktop\Research` without separate explicit confirmation. Prepare an ingest summary naming the exact MultiAgentELBO commit, theorem boundary, source note, project/concept pages, `index.md`, and required `log.md` entry.
