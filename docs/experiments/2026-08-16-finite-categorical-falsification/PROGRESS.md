# Resume ledger — finite categorical falsification experiment

**Task.** Build and run the experiment specified in `gauge_vfe_rg_status.tex` §9
("What would settle it") and detailed in
`docs/derivations/2026-08-16-multiscale-two-channel-graph-vfe-rg/REPORT-part4-literature-experiment-verdict.md`
§13: a fully finite *categorical* (deliberately non-Gaussian) falsification model,
six agents on two directed three-cycles, structure group $\mathbb Z_3$ with two
distinct representations, six measurements plus a mandatory null control.

**Mode.** Multi-agent, user-requested ("deploy multiple expert agents to plan,
build, and test"). User is asleep; work proceeds autonomously.

**Baseline.** `main` at `cd8b7b1` (PR #22 merged) at session start. Working tree
clean apart from four untracked PDFs, which are intentional and must not be touched.

---

## Design decisions already fixed

* **Reuse, do not rebuild.** The repo already carries a finite laboratory
  (`src/multiagent_elbo/finite/`, `geometry/`, 46 modules, 50 test files) with
  measures/KL, $\eta=\alpha\beta$ attention coarsening, Hoeffding/Möbius
  interactions, and discrete holonomy. The new lab extends that, matching house
  conventions.
* **Tractability.** Full flat enumeration of $\mathsf W$ is infeasible
  ($\sim10^8$–$10^9$ states). The design exploits conditional factorization of
  scale 0 given the parent: with $L(o\mid Z_0)=\prod_i L_i(o_i\mid z_i)$ and
  $K^0_\downarrow=\prod_i K(z_i\mid\cdot)$, the inner sum over $Z_0$ factorizes
  into six sums of nine terms. The *direct* brute-force route is then run on a
  reduced but still six-agent instance so that the two routes remain genuinely
  independent computations.
* **No torch.** Pure numpy plus `fractions.Fraction` where exactness is wanted.
  Bare `python` (CPU) is correct here; no CUDA lane is needed.

---

## Stage log

| # | Stage | Status | Notes |
|---|-------|--------|-------|
| 0 | Read §9 + §13 spec, Theorem 2, Prop 1 typing | **done** | fixed-pool indexing (H1), soft endpoint factor in $\mu^x_{IJ}$ (H3), forward-only convolution (H4) all must be respected |
| 1 | Survey wave: 4 parallel agents map existing API vs the six measurements | **done** | see "Survey findings" below |
| 2 | Frozen spec `spec.md` | **done** | 6 agents, two 3-cycles, $\mathbb Z_3$ with $\rho_b(k)=k$, $\rho_m(k)=2k$; two admitted families |
| 3 | Core modules written and smoke-tested | **done** | `finite/two_channel_gauge.py`, `finite/categorical_falsification_model.py` |
| 4 | Build measurement modules: M1, M2, M3, M4 | **done** | 54 new measurement tests passing |
| 4b | Build M5 partition persistence and M6 downward influence | **done** | both return negative results |
| 5 | Config registration, experiment runner, launcher, both test registries | **done** | 16 metrics published; complete manifest |
| 6 | Integrate all six, run the full suite | **done** | 19 failed / 1291 passed, exactly the pre-existing baseline; 78 new tests all pass |
| 7 | Results document | **done** | `docs/results/2026-08-16-categorical-falsification-results.md` |
| 8 | Cross-model verification (Opus author ⇒ **fable** verifiers) | **BLOCKED** | all four verifiers died on the session rate limit; see below |
| 9 | Push, PR, merge, ff | pending | |

## Cross-model verification is NOT done — resume here

Four Fable verifiers were dispatched and **all four terminated on the session
limit** before returning findings: a `verifier-math` pass on the four load-bearing
derivations, a `verifier-code` pass on implementation-versus-spec, an
`audit-skeptic` attack on the headline claims, and a second `audit-skeptic` on the
two negative results. Nothing in this package carries `EVIDENCE_VERIFIED`; every
claim is a candidate supported by executed output on one declared instance.

Re-dispatch all four on `model: "fable"` (this session deploys Opus 5, so Fable is
the required verifier side). The four briefs are recoverable from the session
transcript. The highest-value targets, in order:

1. Whether the M6 pre-registered prediction is mis-stated. A deterministic parent
   has disjoint fibers, so a supremum of total variation across distinct parent
   values may be near maximal by construction rather than near zero. If so the spec
   named the wrong statistic and the implementation is behaving correctly.
2. Whether the M5 null-control failure is real or an artifact of a null that is too
   weak. The present null holds the partition prior and capacity bound fixed, so it
   cannot separate their contribution from the transports'.
3. Whether the measured relaxation time is trustworthy enough to support the
   timescale verdict; the transient is small (rate 0.40 to 0.36) so it is pinned
   only to about a factor of four.
4. Whether the identical influence supremum across all six agents and both blocks
   has the proposed explanation, which is currently plausible and unverified.

## Final measured results

All numbers below were re-executed by the integrator, not taken from builder
reports. Full detail is in the results document.

| Measurement | Outcome |
|---|---|
| M1 accounting | holds, residual $2.66\times10^{-15}$ vs $10^{-12}$; falsifier did not fire |
| M2 composition | holds to $5.6\times10^{-17}$; witness gap exactly $0.4$; product-form trap $0.0514$ |
| M3 closure | **falsifier FIRED**, three-body $6.672\times10^{-2}$, flow-weighted $2\%$ |
| M4 holonomy | all three predictions held; theory falsifier did not fire |
| M5 persistence | **falsifier FIRED**, ratio $1.02$ vs threshold $10$ |
| Null control | **PIPELINE FAILS IT** — reference sits inside the null range on every statistic |
| M6 influence | supremum $0.557$, not decorative; **control did not collapse** |

The single most important result is the null-control failure: randomizing every
transport and the belief family, with the skeleton fixed, changes no
block-formation statistic. The declared prior and capacity structure are doing all
of the work, which is exactly what the mandatory control exists to detect.

## Commits on branch `experiments/finite-categorical-falsification`

```
931a73e feat(finite): measure holonomy retention and wire it into the laboratory
1ffb4af feat(finite): publish the categorical falsification laboratory
edd41c9 feat(finite): measure the closure residual and the generated three-body term
4a0cc0b docs: pre-register the finite categorical falsification metric contracts
63e5d5b feat(finite): measure tower VFE accounting and coarse-edge composition
af2302a feat(finite): declare the two-channel categorical falsification model
```

Branched from `main` at `cd8b7b1`, which equals `origin/main`.

## Survey findings that shape the build

* **Reuse:** `finite/vfe.py` private helpers `_kl_arrays`, `_block_conditionals`,
  `_weighted_conditional_kl` are the label-free ndarray lane and are the right base
  for M1. `scale_cocycle.anchored_mobius_decompose` is exactly the M3 primitive
  (exact `Fraction`, all $2^n$ subsets, anchored at a declared ground state).
  `attention.py` already has the event-law push, disintegration, and a staged-versus-direct
  associativity harness.
* **Extend, do not rebuild:** `attention.pushforward` hardwires the **product**
  endpoint kernel through the einsum `"yz,iI,jJ,yij->zIJ"`. A general joint
  endpoint kernel over ordered pairs is not expressible through the existing public
  API, which is the exact trap M2 has to be able to violate.
* **Build new:** `geometry/discrete_holonomy.py` is hardcoded to $2\times2$
  $\mathrm{GL}^+(2)$, has no root parameter, and its fundamental cycles are not
  based at a common root, so it cannot supply a based holonomy group. The new
  `two_channel_gauge.py` replaces it for this task and attaches both tree legs.
* **Repo house style differs from the global defaults** and wins here, per the
  surgical-changes rule: no LaTeX in docstrings, no aligned signature columns,
  every dataclass frozen, `type(x) is T` checks, sorted `__all__`.
* **Registration:** a new lab needs a frozen `TheoryConfig` plus a branch in
  `config._resolve_theory_config`, an entry in `tests/test_launchers.py::NEW_LAUNCHERS`
  and in `tests/test_experiment_support.py::ALL_LAB_RUNNERS`. It should **not** join
  `NEW_EXPERIMENT_NAMES` / `_EXPERIMENT_CONTRACTS`; precedent for staying out is
  `attention_marked_event` and `categorical_dqm`, and joining forces edits to two
  frozen 7-tuples and their tests.
* **Producers may only emit `CANDIDATE` or `INCONCLUSIVE`.** A lab that
  self-declares `EVIDENCE_VERIFIED` fails `test_laboratory_producers_do_not_self_promote`.

## Verified facts recorded so far

* Core holonomy reproduces the design prediction exactly: block $\{1,2,3\}$ belief
  holonomy group is all of $\mathbb Z_3$ (generator 2), model group is $\{0\}$;
  block $\{4,5,6\}$ trivial in both channels; the whole graph has belief generators
  $(2,2,1)$ and a **flat** model channel.
* Because the structure group is abelian, flipping the global direction convention
  negates every holonomy but preserves triviality, so the belief-versus-model
  separation under test is convention independent. This neutralizes the direction
  or inverse ambiguity flagged as the highest silent-bug risk in the geometry survey.
* CRP prior normalizes to exactly 1 over all partitions of 3. Likelihood entries lie
  in $[0.25,0.75]$, so the observation term is finite and Theorem 2 hypothesis (iv)
  holds by construction.

## Test baseline, measured not assumed

Full suite on the working tree: **19 failed, 1213 passed, 16 skipped** (200 s).
The same 19 failures reproduce on a clean detached worktree of `origin/main` at
`cd8b7b1` (`19 failed, 150 passed, 13 skipped` for those two files alone), so every
one of them predates this work: 18 in `tests/test_remediation_evidence.py` and 1 in
`tests/test_markdown_hygiene.py`. The clean worktree was removed after the check.

New tests added so far, all passing: `tests/test_two_channel_gauge.py` (16) and
`tests/test_categorical_falsification_model.py` (14).

## Measurement results as they land

**M1 VFE accounting — complete, 7 tests passing.**
The two routes agree. Worst residual over three observation records and two
recognition seeds is $2.66\times10^{-15}$, against a pre-registered falsifier
threshold of $10^{-12}$, so **the M1 falsifier did not fire**. The flat joint sums to
$0.99999999999999989$ over all eight records and all 944,784 tower states, which is
one ulp below one; the builder reported this as exactly $1.0$ and that is a slight
overstatement, corrected here from an independent rerun. Setting the
recognition law to the exact posterior gives a gap of exactly $0.0$ and
$\mathcal F=-\log p(o\mid X)$ to the bit. The naive sum of local row potentials is
strictly larger than the free energy in every case, with overcount between $0.7704$
and $0.7801$; because every declared interaction factor is a graph edge with
boundary size two, the naive sum equals exactly twice the overcount, which the tests
check to $10^{-12}$.
Bounded independence claim, stated honestly by the builder: route (a) materializes
all 944,784 joint entries, sums them for the evidence, normalizes, and takes one flat
KL, using no chain rule and no analytic marginalization. It does evaluate the
downward kernel as a per-agent product, because that product *is* the declared
definition of the kernel, so the two routes share the declared factor builders and
share nothing of the free-energy assembly. That is the sense in which route (a) is
independent, and no more is claimed.

**M4 holonomy retention — complete, 20 tests passing, all three predictions held.**
On the block carrying nontrivial belief holonomy the belief score is $+\infty$ under
the orbit family, whose fixed sector is empty, and $0.0872080$ under the whole
simplex, whose fixed sector is the single uniform law. That finite value equals
$\log 3 - H(p)$ exactly, an independent closed form the integrator reproduced to
$10^{-16}$. The same block reaches exactly zero in the flat model channel at an
explicit witness configuration, and both channels reach zero on the flat block.
**The theory falsifier did not fire**: twenty block-and-family pairs admit a
zero-distortion belief parent, namely every block whose induced belief holonomy is
trivial.
The dressed-transport law normalizes to exactly one in rationals when the endpoint
factor is carried over all ordered pairs. The restricted form gives masses
$1.27,\ 2.30,\ 1.50,\ 2.40$, so it is not a probability measure under soft
memberships, which reproduces counterexample C27. The barycenter lies outside the
represented group in the measured belief cases and is guarded rather than used. The
convolution converse is exhibited false by a maximally dependent joint on
$\mathbb Z_3$, which is counterexample C25.
Honest limit carried in the record: stabilization without flatness has **no** witness
inside the orbit families, because no nontrivial element of $\mathbb Z_3$ fixes any
of their laws. The witness is supplied on the uniform law of the simplex family and
is reported as exactly that, not as the general statement. The builder also had to
declare an extension for disconnected candidate blocks, rooting each component
separately and taking an infimum over relative alignments; for connected blocks the
code reduces to the spec formula and a test pins the agreement.

**M3 closure residual — REDIRECTED 2026-08-17; its earlier falsifier withdrawn.**
The original implementation eliminated a block's parent and read off the
interaction content among its children. That runs *against* the coarse-graining
direction and is not a renormalization step; the specification had pre-registered
the projection onto the declared parent family, and the implementation deviated.
Measured as pre-registered, eliminating the children and reading off the theory the
parents obey, the generated three-body coarse coupling is under about one percent
of the pairwise one across three connected partitions, with a flow-weighted
residual of a few parts in a thousand and interaction orders that decay. **The M3
falsifier no longer fires.** Real-space blocking generates couplings outside the
starting family in every scheme, so a nonzero coefficient was never the right test.
The against-direction number, $6.672\times10^{-2}$ with no decay in order, is kept
under its own name as the generic common-cause mechanism.
The result depends on a load-bearing declaration the builder added and flagged:
the block parent must be eliminated exactly, because an action built from the
per-agent likelihood and the declared per-edge divergences alone is *exactly*
pairwise and would leave M3 nothing to measure. That control returns a triple
coefficient of $-4.4\times10^{-16}$, pure float rounding and fourteen orders below
the measured value, which pins the measurement as real rather than numerical.
The Ising star oracle converges to the leading-order form with ratios
$0.470,\ 0.815,\ 0.951,\ 0.988,\ 0.997$ over successive halvings of the coupling
scale, the gap quartering each time as an order-$\varepsilon^2$ correction should,
and is exactly zero at both analytic degeneracies. No equality is asserted at
finite coupling.
Correction to my own brief, recorded: I told the builder that `_fraction` rejects
`float`. It rejects only `bool`, so the exact rational path was available and was
used.

**M2 coarse-edge composition — complete, 15 tests passing.**
The literal three-node witness reproduces exactly: $\beta^c_{IJ}=0.9$ against
$\beta^{\rm naive}_{IJ}=0.5$, a gap of exactly $0.4$ at bit-exact float equality.
On the six-agent instance the row-average discrepancy reaches $0.0875$. Substituting
the product form $K=C\otimes C$ for a genuinely correlated endpoint kernel moves the
coarse event law by $0.0514$, so the named trap is real and measurable rather than
hypothetical. Composition residual is $5.55\times10^{-17}$, one to two ulps.
Two honest caveats recorded by the builder: total mass is 1 to within one ulp rather
than bit-exactly, partly because `edge_event_law` already returns $1-1.11\times10^{-16}$
before any push; and the matrix identity $K_{20}=K_{21}K_{10}$ is near tautological
because the composition is implemented as a matrix product, so the substantive check
is the pushed-law agreement, not that identity.

## Independent reruns performed by the integrator, not taken on trust

Every builder headline below was re-executed directly before being recorded. For M1
the rerun confirmed the posterior gap is exactly zero, the flat-versus-decomposed
residual is exactly zero at an unseen recognition seed, all five non-observation
groups are nonnegative, and the naive local sum equals exactly twice the reported
overcount. It also corrected the total-mass claim from bit-exact to one ulp.

## Pre-existing defect found, not caused by this work

`tests/test_markdown_hygiene.py` **fails on `main`**:
`docs/prompts/2026-08-16-fixed-point-graph-rg-deep-research-prompt.md` carries seven
forbidden C0 bytes (`0x08`, `0x09`) committed in `35f3556`. Left untouched, since
the intent of those bytes is unknown and the file is unrelated to this task. It will
show as one red test in any full-suite run.

---

## Standing constraints for this task

* Cross-model verification is mandatory: this session deploys **Opus 5**, so every
  verifier/adjudicator/judge role dispatches with `model: "fable"`. A same-model
  verifier must return `INCONCLUSIVE_SAME_MODEL`.
* CPU tests must be tiny and finish well under a second; never run a
  production-scale model inside a test.
* Do not touch the four untracked PDFs; do not revert or modify config toggles.
* American English, academic prose, no banned Claude-isms in any prose artifact.
* Report what was actually executed. Skipped, failed, and unrun are all reportable.

---

## Open questions parked for the user

*(none yet)*
