# Independent Scientific Review: Shared Scientific Contract Remediation

**Review date:** 2026-08-10

**Verdict:** `APPROVED`

**Scientific code revision:** `f4966db1127ad952e3f3f1ce118b518ca58b5811`

**Phase-A documentation revision:** `a6dd33255f8bb74a1bd78a5b1466992fe98d053f`

**Interpreter:** `C:\Python314\python.exe` (CPython 3.14.4, CPU)

## Summary and recommendation

The remediated permutation, SPD-conditioning, Session-3 stress, producer-state,
and deterministic-replay contracts are scientifically and mechanically
consistent at the revisions named above. I independently reconstructed the
load-bearing finite and spectral identities, evaluated nonidentity fixtures,
parsed the replay, JUnit, and coverage artifacts directly, and sought coupled
oracle, threshold, stale-evidence, and status-precedence failures. I found no
Critical or Important issue, so the review is approved.

The approval is revision-bound. It certifies the stated finite CPU contracts
and the accuracy of
`docs/results/2026-08-10-shared-scientific-contract-remediation-results.md` at
documentation revision `a6dd332`. It does not promote any producer record out
of `CANDIDATE` and does not replace the separate verification ledger.

## Findings

### Critical

None.

### Important

None.

### Minor

1. **The cross-producer three-cycle channel/action test is less independent
   than its name suggests.** In `tests/test_counterexamples.py:94`, the channel
   fixture is the identity and the channel and action assertions compare the
   exact adapters to the same shared pullback methods. Applying the same
   permutation to both axes leaves the identity channel unchanged, and a
   coupled defect in an adapter plus shared helper could evade that isolated
   test. This does not invalidate the current revision: the explicit
   inverse-direction mutation at `tests/test_shared_scientific_contracts.py:84`,
   the literal nontrivial channel oracle at
   `tests/test_finite_permutations.py:44`, and the independent nonidentity
   calculation in this review all agree with the implementation. A future
   strengthening should pin a nonidentity row-stochastic three-state channel
   and the literal action result directly in the cross-producer test.

## Claim-status assessment

| Claim family | Status | Review basis |
|---|---|---|
| Old-to-new permutation law and group action | Derived | Literal inverse and composition derivation, followed by direct source execution |
| Exact SPD membership | Derived | Exact leading-principal-minor calculation before floating conditioning |
| Spectral decisions and proxy reversals | Derived plus numerical | Closed-form eigenvalues, float64 eigenspectrum reproduction, and direct implementation output |
| Threshold-band default result | Derived plus numerical | Direct substitution into the declared tolerance rule and replay artifact agreement |
| Numerical-policy reachability and stress precedence | Mechanically verified | Direct calls, source trace, mutation tests, and serialized policy |
| Producer states and support boundaries | Mechanically verified | Direct parsing of all emitted records and source trace |
| Replay determinism | Reproduced output | Parsed semantic equality, exact array equality, byte equality, and six SHA-256 identities |
| JUnit and focused coverage totals | Reproduced source record | Direct XML/JSON parsing and file hashing |

## Mathematical derivations

### 1. Three-cycle old-to-new oracle and group law

Let the stored permutation be the old-to-new map

$$
p=(1,2,0), \qquad p(0)=1,\;p(1)=2,\;p(2)=0.
$$

Its inverse is therefore

$$
p^{-1}=(2,0,1).
$$

The pullback places the old value at $p^{-1}(j)$ into new index $j$. For the
law

$$
\mu=(1/5,3/10,1/2),
$$

the exact pullback is

$$
(p^*\mu)_j=\mu_{p^{-1}(j)}=(1/2,1/5,3/10).
$$

This is the result stated in the Phase-A record and returned by
`FinitePermutation.pullback_law` and `relabel_law`. The source implements the
inverse in `src/multiagent_elbo/finite/permutations.py:69`, the generic axis
pullback at line 96, and the exact adapter at
`src/multiagent_elbo/finite/counterexamples.py:315`.

For a nonidentity row-stochastic channel

$$
K=\begin{pmatrix}
1/2&1/3&1/6\\
1/4&1/2&1/4\\
1/6&1/3&1/2
\end{pmatrix},
$$

using the same cycle on source and target gives the independently indexed
oracle

$$
(p^*K)_{ij}=K_{p^{-1}(i),p^{-1}(j)}=
\begin{pmatrix}
1/2&1/6&1/3\\
1/6&1/2&1/3\\
1/4&1/4&1/2
\end{pmatrix}.
$$

The repository's `pullback_channel` and `relabel_channel` return this exact
rational matrix. For the one-axis action $A=(2,3,5)$, the literal pullback is
$p^*A=(5,2,3)$, matching `ExactAction.relabel` at
`src/multiagent_elbo/finite/counterexamples.py:123`.

For old-to-new maps $p$ followed by $q$, the stored composite is

$$
(q\circ p)(i)=q(p(i)).
$$

Thus `p.then(q)` must store `q[p[i]]`, which is exactly the implementation at
`src/multiagent_elbo/finite/permutations.py:86`. With
$q=(1,0,2)$, $q\circ p=(0,2,1)$ and both sequential and composite pullbacks of
$(10,20,30)$ are $(10,30,20)$. Both inverse compositions return the identity.
The non-involutive fixture also defeats the wrong indexing rule: pulling
$(0.2,0.3,0.5)$ by `new_to_old` gives $(0.5,0.2,0.3)$, while indexing by the
stored `old_to_new` tuple gives $(0.3,0.5,0.2)$, with maximum difference $0.3$.

### 2. Exact SPD membership, spectral decisions, and proxy reversals

The finite adapter first applies exact Sylvester membership through positive
leading principal minors at
`src/multiagent_elbo/finite/counterexamples.py:545`. Only after exact
membership succeeds does it call the shared float64 spectral assessment. The
Gaussian adapter independently applies symmetry and Cholesky membership before
the same spectral assessment at
`src/multiagent_elbo/realizations/gaussian/interactions.py:55`.

For the correlated control

$$
C=\begin{pmatrix}1&1-10^{-12}\\1-10^{-12}&1\end{pmatrix},
$$

the exact leading minors are

$$
1,\qquad 1-(1-10^{-12})^2
=1.999999999999\times10^{-12}>0.
$$

It is therefore SPD. Its exact eigenvalues are $10^{-12}$ and
$2-10^{-12}$, so its exact reciprocal condition is
$5.0000000000025\times10^{-13}$. The actual float64/scipy path returns

$$
\lambda_{\min}=9.999778782798785\times10^{-13},\quad
\lambda_{\max}=1.999999999999,
$$

and $r_{\mathrm{cond}}=4.999889391401893\times10^{-13}$. With threshold
$10^{-12}$ and zero band, the decision is `fail`. The retired proxy is

$$
1/|\det C|\approx5.0001106110475214\times10^{11}<10^{12},
$$

so it returns `pass`, a false acceptance.

For the repeated-small-diagonal control

$$
D=\operatorname{diag}(1,10^{-7},10^{-7}),
$$

the exact leading minors are $1$, $10^{-7}$, and $10^{-14}$, all positive.
Its minimum and maximum eigenvalues are $10^{-7}$ and $1$, hence
$r_{\mathrm{cond}}=10^{-7}$ and the spectral decision is `pass`. The retired
proxy is approximately $1.0000000000000012\times10^{14}>10^{12}$ in float64,
so it returns `fail`, a false rejection.

The policy in `src/multiagent_elbo/conditioning.py:48` uses

$$
b=\mathrm{atol}+\mathrm{rtol}|t|,
$$

where $t$ is `min_spd_rcond`, and declares `inconclusive` when
$|r_{\mathrm{cond}}-t|\leq b` before considering pass or fail. For the default
Session-3 control $\operatorname{diag}(1,10^{-100})$,

$$
t=10^{-12},\quad b=10^{-12}+10^{-10}10^{-12}
=1.0000000001\times10^{-12},
$$

while $|10^{-100}-10^{-12}|$ rounds to $10^{-12}$. It lies inside the band,
so the required default decision is `inconclusive`, not `fail`. The replay's
serialized minimum, maximum, reciprocal condition, threshold, band, method,
membership flag, reason, and decision all match this derivation.

## Numerical and mechanical evidence

### 3. Numerical-policy reachability

A direct call on $\operatorname{diag}(1,1.05\times10^{-6})$ produced the
following independent reachability matrix:

| Change | Decision |
|---|---:|
| `min_spd_rcond=1e-6`, zero band | `pass` |
| `min_spd_rcond=1.1e-6`, zero band | `fail` |
| `atol=1e-7` at threshold `1e-6` | `inconclusive` |
| `rtol=0.1` at threshold `1e-6` | `inconclusive` |

Session 3 passes all three values into both finite SPD assessments at
`src/multiagent_elbo/finite/counterexample_experiment.py:438` and line 568,
then serializes requested and effective values at line 518. Within this stress
contract, `max_frame_condition` is not used to decide SPD membership or
spectral conditioning and is accurately serialized under `not_applicable` at
line 529. This is a Session-3 scope statement, not a claim that the setting is
unused elsewhere.

### 4. Separate stress gates and aggregate precedence

The source constructs four separate required assessments at
`src/multiagent_elbo/finite/counterexample_experiment.py:455`: deep channel
composition, relabeling, retained-space visibility, and conditioning. The
relabeling gate requires both `coherent` and an exact zero residual. Mutation
tests separately force false coherence and nonzero residual, and either one
forces the relabel and aggregate statuses to `fail`. Separate mutations also
force the deep-composition, retained-space, and conditioning gates to fail.

The aggregate at line 265 collects every metric and stress status and applies
the exact order `fail`, then `inconclusive`, then `pass`. Direct calls returned
`pass` for all-pass inputs, `inconclusive` when no failure but one inconclusive
was present, and `fail` when a failure and an inconclusive were both present.
The reproduced default stress statuses are three passes and one inconclusive,
so the aggregate is correctly `inconclusive`.

### 5. Candidate-only producer records and support boundaries

The Session-3 metric constructor explicitly writes `CANDIDATE` at
`src/multiagent_elbo/finite/counterexample_experiment.py:85`; the candidate
constructor does the same at line 105. Direct parsing found exactly 19,587
candidate records and five metric records, with the unique verification-state
set `{CANDIDATE}` for each collection.

There are 12 `support_boundary` records. Every one has
`inside_declared_domain=false`, `assumptions_satisfied=false`, classification
`assumption_boundary`, state `CANDIDATE`, and an applicability explanation
that explicitly names the absolute-continuity requirement for $KL(q\|p)$.
The source construction is at
`src/multiagent_elbo/finite/counterexample_experiment.py:158`. No producer-side
ledger promotion was found or inferred.

### 6. Replay equality and six file hashes

Both manifests are complete, record `git_commit=f4966db1127ad952e3f3f1ce118b518ca58b5811`,
and record `git_dirty=false`. Their resolved scientific configurations are
identical after replacing only the output-root value. The differing
root-sensitive configuration hashes are therefore expected.

All five JSON files were parsed and compared as structured values, then
compared as bytes. The NPZ files were loaded with `allow_pickle=False`; their
41 names match and all arrays compare equal with `numpy.array_equal`, including
36 numerator/denominator arrays forming 18 exact-rational pairs. The NPZ bytes
also match.

| Artifact | SHA-256 in replay A and replay B |
|---|---|
| `metrics.json` | `b4fd3d6514ca1ed14dabe8df5691eb0683ba5205da42f40b07ca95950ab1e71b` |
| `enumeration_bounds.json` | `6919d7f9ea4bc17698fe806c9947157debbfbae03f71e041b2db26a77d64656e` |
| `candidate_records.json` | `ee3b876d6ca889bcc81be31c19f385c03f21a6b488fd0808cfb33b0f22ea4801` |
| `minimal_witnesses.json` | `281c4d1e3d1f49d9fea87a0762656a78d1f7507808220ae1e3f773d9a04eec06` |
| `stress_matrix.json` | `072be1d4c9f6bc18f9e50ba9563da5ee210ec663a9fb84a91c59c4cf67caf200` |
| `arrays.npz` | `aafa135e901d5425eaaf996c535903a5c0dc59a52ff5cb82ec87667d82f678de` |

The parsed catalog counts are 7 laws, 49 channels, 6,561 actions, 19,587
candidate records, and 5 global minima. The five minimal residuals and their
boundary classifications also match the Phase-A result document.

### 7. Parsed JUnit and coverage evidence

The XML was parsed rather than read from console progress:

| Artifact | Parsed totals | SHA-256 |
|---|---|---|
| `.pytest-tmp/task6-contracts.xml` | 11 tests; 11 passed; 0 failures; 0 errors; 0 skipped | `b764b53f2dcecb205c90bacc4fa07ab1d604ac0140eba72d0c066eab4b802c30` |
| `.pytest-tmp/task6-full.xml` | 756 tests; 754 passed; 0 failures; 0 errors; 2 skipped | `0ada528427bdd5b410f6aa62dbe97349dd052ad804658bc8492342fe6d662995` |

The two skips are the existing Windows privilege-dependent symbolic-link
cases. They do not intersect the scientific contracts reviewed here.

Coverage XML and JSON agree on 131 of 139 statements and 49 of 52 branches:
94.24% line and 94.23% branch coverage in aggregate. Per module,
`src/multiagent_elbo/conditioning.py` has 52 of 60 statements (86.67%) and 17
of 20 branches (85%); `src/multiagent_elbo/finite/permutations.py` has 79 of
79 statements and 32 of 32 branches (100% each). The coverage XML SHA-256 is
`9984bf4abcf63b21296231309be5f5299c3246e56751e20cc2d477e658f3fbcf`.

## Result-document accuracy and revision binding

Every numerical, categorical, replay, JUnit, coverage, hash, and supersession
statement checked in
`docs/results/2026-08-10-shared-scientific-contract-remediation-results.md`
matches the direct source/artifact reconstruction. Git history identifies
`a6dd332` as the direct child of `f4966db`, and the only changes between them
are the two Phase-A result documents. A path-restricted diff confirms no
change under `src`, `tests`, or `run_finite_counterexample_lab.py` between the
scientific and documentation revisions.

The JUnit and coverage formats do not embed a Git SHA. Their revision binding
therefore depends on the contemporaneous clean-worktree record, exact artifact
hashes, commit timing, unchanged scientific tree through `a6dd332`, and the
task-scoped command report. By contrast, both replay manifests embed the full
scientific code SHA directly. This distinction is an evidence limit, not an
unresolved scientific defect.

## Evidence limits and non-goals

This review did not create or modify a `.verification` ledger or active marker.
Producer metadata remains evidence awaiting external adjudication, not
evidence-state promotion. The review does not certify the historical bundles
under current semantics and does not rewrite their revision-bound records.

The reviewed evidence is a finite, deterministic CPU realization using exact
rational arithmetic where declared and float64 spectral calculations where
declared. It does not establish a continuum limit, an infinite-volume result,
general SPD-manifold convergence, CUDA behavior, security behavior,
provenance-hardening behavior, or registry behavior. It also does not claim
that the finite recognition law uniquely determines a continuum section or a
lattice gauge theory.

## Final recommendation

`APPROVED`. There is no unresolved Important issue and no scientific blocker
to committing this independent review. The Minor test-isolation improvement
may be handled later without changing this verdict.
