# Response to review PR #17

**Review:** `docs/reviews/2026-08-16-claude-multiscale-vfe-rg-review.md`
**Reviewed revision:** `8ec8f4a` · **Reviewing system:** Codex/GPT-5
**Disposition accepted in full.** All four High and all six Medium findings are
correct and were confirmed against the committed bytes before repair, not against
memory of them. Nothing is contested.

The contract id is unchanged (`contract-sha256-7d2c4a48…`): the frozen target was
not touched, so every binding remains comparable across the repair.

## High findings

| # | Finding | Verdict | Fix | Where |
|---|---|---|---|---|
| H1 | Random occupied node sets make the joint ill-typed | **Sustained** | Every scale-$s$ object is now indexed by the fixed pool $\Lambda_s$; occupancy is the derived predicate $\alpha^{x,s}_A>0$. The disjoint-union alternative is recorded. Differing $C^b,C^m$ route through Proposition 7's declared correspondence instead of presuming a common occupied index. | P1 §3.1 (+ diagram), `construction-or-strongest-theorem.md`, claim-table row 2 |
| H2 | Parent Gibbs update omits live descendant terms | **Sustained** | $\mathcal V_{s+1}$ now collects all four parent-dependent conditional divergences ($P^s_R$, $P^s_G$, $P^s_H$, $K^s_\downarrow$), each conditioned on $Z_{s+1}=z$. The truncated form is admissible only under a declared parent-independent factorization. | P3 §11.1, `construction-or-strongest-theorem.md` item 3, row 40 |
| H3 | Dressed-transport law omits the soft endpoint factor | **Sustained** | Numerator now sums over all ordered pairs carrying $K^x(I,J\mid i,j)$, matching the denominator. The restricted "$i\in I,j\in J$" form is retained only for hard deterministic assignment, where the omitted factor is identically one. | P3 §9.4, `construction-or-strongest-theorem.md` item 6, row 32 |
| H4 | Convolution equality does not imply conditional independence | **Sustained** | Proposition 9 keeps the forward implication only. The false converse is removed from the prose, the claim table, and the generator. | P3 §9.4, row 34, `_build_artifacts.py` |

**New counterexamples added**, one per defect that needed a witness:

* **C25** — $G=\mathbb Z_3$, $U$ uniform, $V=U$: maximally dependent, yet
  $U+V=2U$ is uniform and equals the convolution of the marginals. General reason:
  if either marginal is Haar on a compact group the product is Haar regardless of
  dependence, so convolution equality cannot test independence.
* **C26** — two parent states, uniform prior, zero downward mismatch, descendant
  term $1$ versus $\tfrac12$: true optimum $(\tfrac23,\tfrac13)$, truncated formula
  returns uniform. The omission moves the **argmin**, not just the value.
* **C27** — one child split $\tfrac12/\tfrac12$ across two parents with all mass on
  one microscopic edge: the restricted numerator gives total mass $2$ or $0$ while
  the denominator counts $\tfrac12$.

## Medium findings

| # | Finding | Verdict | Fix |
|---|---|---|---|
| M1 | Theorem 2 omits its integrability premise | **Sustained** | Promoted to hypothesis (iv), with an explicit note that it is not implied by positive finite evidence plus absolute continuity. |
| M2 | Capacity and node-count control described as necessary | **Sustained** | Downgraded to **sufficient design mechanisms**, one per degeneracy; joint necessity is now an open obligation in `release.json` and row 22 reads **E**/**O**. |
| M3 | Flatness and stabilization called logically independent | **Sustained** | Corrected to the chain: flatness $\Rightarrow$ stabilization; flatness $\not\Rightarrow$ agreement; stabilization $\not\Rightarrow$ flatness. The earlier phrasing conflated stabilization of one law with agreement between different agents' laws. |
| M4 | Support-based holonomy criterion lacks topological hypotheses | **Sustained** | Restated at the measurable tier as $\mu^x_{\rm loop}(\mathrm{Stab}(Q_I))=1$; the support form is deferred to a separately declared topological group and continuous action. |
| M5 | "Exactly MSM-consistent" overstates the connection | **Sustained** | Fixed in **two passes** — see the note below. The linear rule is now justified internally at all three sites: $\phi=1$ is the unique $\phi$-norm that is a fixed input-independent Markov pushforward, which is what the KL chain rule requires. Zheng et al. cited for the $\phi$-family that refutes universal additivity. |
| M6 | "Strongest verified result" contradicts the release state | **Sustained, with a constraint** | The heading is fixed verbatim by the `rigorous-theory-search` output contract, which requires exactly nine headings and forbids others; renaming it fails the structural validator. The correction is carried in the section's opening paragraph, which states that nothing is verified and that what follows is the strongest **author-derived** result. |

## M5 needed a second pass, and why

The first repair pass fixed M5 only in Part 2 §8.1. Two further sites survived —
the MSM bullet of Part 4 §12.2 and mechanism M4 of Part 3 §10.1 — both still
asserting that renormalizability is additivity of the defining parameter and that
this is "precisely why" Part 2 pushes $\eta$. The cause is worth recording because
it is the same failure mode as H1: the patch that was supposed to correct Part 4
was written with a guard, `if old_msm in s:`, whose pattern did not match the
wrapped text, so it silently did nothing and the pass reported success. A guarded
replacement that no-ops is indistinguishable from one that worked unless the result
is checked, and it was not checked.

Both sites are now corrected, and the claim table carries the refutation
explicitly as row 71 rather than leaving it implicit in prose. The lesson
generalizes past this package: every textual repair in a byte-bound artifact should
be verified by grepping for the *old* string afterwards, not by trusting the
patch's exit status.

## Mechanism M5: the $\sup$-aggregation transplant, now added

The review directed that the $\sup$-aggregation mechanism be added only after
H1–H4 and M1–M6 were repaired, placed beside the existing block-proposal
mechanisms, and explicitly separated from the exact $\eta$ pushforward. That
condition is now met, and it appears as **mechanism M5** in Part 3 §10.1, labeled
`CONJECTURE`, with three caveats attached:

1. The $\phi$/sup weight rule acts only after blocks are supplied. Effective
   resistance may motivate a separate conjectural blocking map, but no such map or
   semigroup is currently defined.
2. No theorem transfers: not self-similarity, not the hidden-degree
   recursion $\langle\sigma'\rangle=\langle\sigma\rangle r^{\psi}$, not the angular
   sector construction, all of which depend on the weighted-$\mathbb S^1$ model.
3. For $\phi\ne1$, no fixed input-independent normalization makes the $\phi$-norm
   a mass-preserving Markov pushforward for all probability inputs and nontrivial
   blocks; GRW instead uses rescaling $C$. Effective resistance is computed on the
   **symmetrized** graph, so the mechanism discards
   the directionality that $\beta$ and $\gamma$ exist to carry — the review's own
   added objection.

The resulting discipline is that proposal and accounting are different jobs:
propose blocks with a $\sup$ or $\phi$-norm rule on the resistance scale, then score
and coarse-grain them with the exact linear $\eta$ pushforward. Only the second is
bound by the VFE identity. Claim-table rows 71–75 record the refutation, the
$\phi=1$ uniqueness argument, the conjectural transplant, its directionality cost,
and the open directed-$\phi$-family question.

## On the adversarial process, not just the mathematics

H1 is worse than a miss. It is verbatim attack **A1** in this package's own
adversarial report, where it was marked `REJECTED` on the grounds that fixed label
pools fix every later codomain — the correct repair, described and never
implemented in the body. An adversarial pass that raises the right objection and
then dismisses it on an unexecuted fix is less useful than one that misses it
outright, because it converts an open question into a false clearance.

A1 is now recorded `SUSTAINED` with that history stated, and a new attack **A9**
records H2, H3, H4, M1, M3, and M4 together with their repairs. The independent
reconstruction record already carried three self-caught discrepancies; it did not
catch these six, which is the honest measure of what a same-model reconstruction
is worth.

## What the review granted, and what it corrected in the follow-up

Granted as surviving: the normalized-kernel formulation of a collective multiscale
VFE; the Reading A / Reading B distinction; the edge-event law rather than a
row-normalized attention matrix as the graph-level primitive for exact
coarse-graining; and retention of a full non-flat holonomy law rather than a mean
transport.

On the two references, the review confirms the follow-up analysis and adds one
point this package did not have: a max-weight mechanism built on the **symmetrized**
Laplacian discards directionality, which is the whole content of the $\beta/\gamma$
structure. That objection is now attached to the Proposition 11 transplant
conjecture rather than left implicit. Per the review's repair order, the
$\sup$-aggregation mechanism itself is **not** added in this pass; it belongs
beside the existing block-proposal mechanisms and explicitly outside the exact
$\eta$ pushforward used in the VFE decomposition.

## Verification of this repair

Digests regenerated; `validate_run.py --mode release` exits 0 on the working tree
**and** on a clean `git archive` extraction of the committed tree, which is the
check that the earlier line-ending defect escaped. Zero CR bytes in the package.
The terminal status remains **INCONCLUSIVE** and no claim carries
`EVIDENCE_VERIFIED`.
