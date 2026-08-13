# Interim referee review: ELBO to PIFB2 continuum-action program

**Reviewed revision:** `caa4a15eccb1d086650d81b06d4a7dc4992a24ca`

**Recommendation:** Major revision of `overview.md` and the live worklog; retain the program-decision packet as a sound bounded checkpoint with `terminal_status: null`.

The strategic conclusion is defensible: exact finite fixed-joint ELBO theory should remain the normalization and inference companion, while PIFB2 remains an effective section action whose sectors receive separate proof-status labels. The normalized tied-replica construction, its KL expansion, its mutual-information correction, the scoped moving-peer no-go, and the generic KL-disintegration theorem survive review. The principal defects arise when those scoped results are transferred to literal PIFB2, same-time cross-context coupling, or the continuum program.

## Major findings

### 1. The theorem proves a repaired scalar, not equality to literal PIFB2

**Location:** `overview.md:118`; `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:31`; `docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/exact-elbo-proof.md:109`; `Theory/PIFB2.tex:663-694`

**Severity:** High. **Status:** Proven counterexample; survived adversarial challenge.

The exact theorem uses the joint likelihood term

\[
-\mathbb E_{\zeta_a}\log L_a(o_a\mid K_a,M_a).
\]

It then defines the repaired lagged scalar as the same display with the mutual-information term removed. Literal PIFB2 instead writes an expectation under `q_i`; its boxed display leaves `m_i` unbound, while its pointwise display naturally reads as the predictive likelihood. Under mean field,

\[
-\mathbb E_{q\otimes s}\log L(o\mid K,M)
\ne
-\mathbb E_q\log\int L(o\mid K,m)s(dm)
\]

in general. A two-point model with likelihood values `1/4` and `3/4` gives the exact Jensen gap `log(2)-0.5 log(3)=0.1438410362`.

**Fix:** Name the theorem's target a repaired lagged unit-coefficient scalar and state that equality to the literal PIFB2 display or predictive-marginal objective has not been proved.

### 2. The base-neighbor proposition conflates lagged templates with current cross-context coupling

**Location:** `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:213-242,280-301`; `docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/typed-construction.md:39-87`

**Severity:** High. **Status:** Proven dichotomy; survived adversarial challenge.

The exact witness freezes `u_ab^n=(Omega_ab^n)_# q_b^n` in history and explicitly constructs `P_h^n` as a product over current agent-site records. If the neighbor is lagged, the label-copy KL is exact but does not require relaxation of design-product independence. If the neighbor is contemporaneous, the displayed generative factor depends on the recognition law being optimized and fixed-joint exactness is lost unless a new normalized joint is constructed.

The worklog's claims that the exact law exists iff design-product independence is relaxed, that the Dirichlet term vanishes iff independence holds, and that `eta_q` measures the strength of cross-context dependence do not follow. Equal-marginal dependent Bernoullis and unequal-marginal independent Bernoullis give immediate counterexamples to the latter equivalence.

**Fix:** Separate the exact history-lagged label-copy model from a still-open same-step cross-context model. Treat `eta_q` as declared until a normalized joint derives it.

## Substantive medium findings

### 3. The exact-contraction arrow is a conditional theorem schema, not an instantiated PIFB2 result

**Location:** `overview.md:96,105-107`; `docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/exact-contraction-proof.md`

KL disintegration is exact for a normalized posterior, a recognition-independent measurable map `C_h`, and the same pushforward path for the recognition and posterior laws. A density action also requires a declared reference measure. The intended tied-replica application still lacks the explicit `C_h`, pushed-forward posterior, and computed residual; the worklog correctly leaves `T-RESID` pending.

**Fix:** Label the generic arrow `PROVEN, conditional`; label the intended tied-replica/PIFB2 instantiation `OPEN`.

### 4. The local KL expansion does not prove the displayed global continuum estimate

**Location:** `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:71-106,213-249`; `docs/verification/kl_expansion_check.py`

The local coefficients `1/2`, `1/3`, and `1/6` reproduce exactly. The script cancels `s(h)+s(-h)` at one center; it does not define edge orientation and multiplicity, treat boundaries, prove a Riemann-sum theorem, or close the transported covariant case. A one-direction Poisson edge sum has `O(h)`, not `O(h^2)`, global error. In addition, the exact finite ELBO block lacks the required `h^(d-2)` coefficient, so its unweighted sum has the desired finite scaling only in `d=2` unless a new normalized construction supplies that coefficient and its normalizers.

The skeptic upheld the mathematical issue but downgraded it because the worklog elsewhere marks coefficient derivation and continuum convergence open.

**Fix:** State only a flat local consistency expansion. Define a bidirected or symmetrized stencil, derive the mesh coefficient probabilistically, and prove the global covariant limit separately.

### 5. The U(1) witness detects flat monodromy, not curvature or bundle topology

**Location:** `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:410-418,460-476,498-568`; `docs/verification/u1_two_path_holonomy_witness.py`

For `C=S^1` and `A=(Theta/2pi)dphi`, curvature is zero while loop holonomy can be nontrivial. The bundle is trivial. Therefore “nontrivial holonomy iff curvature,” “topological obstruction,” and “bundle invariant” are too strong. The numerical witness remains useful: it proves that putting curve transport inside the generative source can distinguish the trivial case from the selected nontrivial case.

The implemented statistic is `arccos(cos Theta)`, not the U(1) element `exp(iTheta)`. It identifies `Theta` and `-Theta`; a direct countercheck found the `pi/2` and `3pi/2` record-law orbits gauge-equivalent to numerical precision. It is an existence witness, not general holonomy identification.

**Fix:** Describe the result as a finite-design witness of operational connection holonomy. Separate flat monodromy, local curvature, and bundle topology; add an oriented/asymmetric observable before claiming full holonomy-element recovery.

### 6. The full-GL invariant-form no-go is worded too strongly

**Location:** `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:146`; `overview.md:153,195`; `docs/audits/roadmap-review-2026-08-12/rm-04-gauge-kinematics.md:275-302`

The correct result is that `gl(K,R)` has no positive-definite Ad-invariant inner product controlling every Lie-algebra direction. It is false that every Ad-invariant symmetric form is indefinite: `(tr F)^2` is nonnegative but degenerate. Fisher dressing can likewise provide a nonnegative invariant state-dependent sector while remaining stabilizer-degenerate and noncoercive along noncompact gauge orbits.

**Fix:** State the positive-definite full-direction no-go. Call compact type sufficient for the first coercive fixed-inner-product theory, not necessary for every degenerate or state-dependent curvature functional.

### 7. Integration into the ambient Theory manuscript conflicts with its governing SPEC

**Location:** `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:163`; `Theory/SPEC.md:17`

The worklog contemplates writing section 4 results into `Theory/`, while the governing SPEC excludes PIFB2 as source, crosswalk, motivation, and remark.

**Fix:** Keep this program in a distinct synthesis manuscript or explicitly revise the SPEC by author decision before integration.

### 8. The decision packet's closure provenance needs an explicit pointer

**Location:** `docs/derivations/2026-08-12-pifb2-elbo-program-decision/final-report.md:14`; `construction-or-strongest-theorem.md:4`; `claim-ledger.json`

The packet says a separate revision-bound ledger closes the state-level no-go but does not name it. Its own ledger contains one evidence-empty `INCONCLUSIVE` target. The underlying no-go is sound and appears as `live-peer-fixed-joint` in the effective-section-action precursor ledger; this is a provenance defect, not a mathematical defect.

**Fix:** Link the exact ledger path, claim ID, revision, and derivation artifact.

## Minor findings

- `overview.md` calls the closed theorem a finite-lattice ELBO although the theorem itself declares only a finite agent-site/source inventory, not an interaction complex with oriented links and plaquettes. Use `finite-site` until the lattice structure is supplied.
- The proposed `exp(-L(gamma)/xi)` curve weight cites vertical Fisher length. A horizontal lift has zero vertical Fisher length, and `xi` remains an explicit parameter. Declare a different path metric and derive both the kernel and scale before calling the correlation length derived.
- The worklog's conjecture/status block at lines 564-581 predates and contradicts the witness reported immediately above it; obligations 1-3 need reconciliation.
- The overview's repository-fragmentation table is stale at revision `caa4a15`: the Desktop checkout now contains the six referee reports and the program-decision packet.

## Claims that survive review

| Claim | Status |
|---|---|
| Finite normalized tied-replica joint | Proven |
| Exact tied-replica KL expansion and mutual-information correction | Proven |
| Equality to the repaired lagged unit-coefficient scalar | Proven under frozen assumptions |
| Equality to literal PIFB2 | Not established; false without an additional likelihood bridge |
| Scoped moving-peer fixed-joint obstruction | Proven on the declared fine product family |
| Generic KL disintegration under one fixed coarse map | Proven, conditional |
| Intended tied-replica/PIFB2 contraction and controlled residual | Open |
| Local flat exponential-family KL expansion | Derived and mechanically reproduced |
| Global covariant Dirichlet limit | Open |
| U(1) nontrivial-holonomy separation example | Numerical existence witness |
| General holonomy recovery, curvature recovery, or topology recovery | Open |
| Restricted compact-regime continuum existence theorem | Open |

## Recommended continuation order

1. Repair the literal-PIFB2 likelihood crosswalk.
2. Rewrite the base-neighbor section with explicit lagged versus contemporaneous semantics.
3. Instantiate `C_h` and compute `T-RESID` before extending the operator basis.
4. Define the lattice counting, mesh coefficient, boundary treatment, and covariant limit.
5. Correct the holonomy/curvature/topology language and strengthen the witness only if full class separation is needed.
6. Keep the continuum theorem in the restricted compact regime and outside the ambient `Theory/` manuscript unless its SPEC is deliberately changed.

## Verification notes

The current KL-expansion and U(1) scripts were reproduced successfully. The U(1) script's four asserted checks pass, but its narrative conclusion overstates what its statistic identifies. An isolated triage ledger was validated under the installed verification gate. No source repository file was modified.
