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
| 4 | Build measurement modules: 5 parallel agents (M1 / M2 / M3 / M4 / M5+M6) | **running** | each writes one module + one test file, no edits to existing files |
| 5 | Core-module tests, config registration, experiment runner, launcher | in progress (me) | |
| 6 | Run full suite, record results | pending | |
| 7 | Cross-model verification (Opus author ⇒ **fable** verifiers, per CLAUDE.md) | pending | |
| 8 | Write up, commit, push, PR, merge, ff | pending | |

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
exactly $1.0$ over all eight records and all 944,784 tower states. Setting the
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
