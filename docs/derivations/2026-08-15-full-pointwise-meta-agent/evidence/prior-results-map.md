<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87","schema_version":"rigorous-theory-search/v1","target_digest":"15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87"} -->
# Prior-results map for `direct-derivation.md`

Added by the 2026-08-16 remediation of finding L1 in `docs/reviews/2026-08-15-deep-review/`.

`evidence/direct-derivation.md` contains no citation to any prior result: `grep -c "Theory/"` returns
`0`, no canonical theorem label (`cg-…`, `rg-…`) appears anywhere in the package, and neither
`Kullback1951` nor `Csiszar1967` is carried forward. Read alone, its §3 and §6 therefore present as
first derivations. They are not. This file supplies the mapping.

**Why the mapping lives here rather than inline.** `direct-derivation.md` is the hash-bound
mathematical evidence artifact. Its SHA-256 `2aa70b07751d07712a3d9395f77817317d48d77d97c3fd5fb8cd1a3f6fda226a`
is recorded in `construction-or-strongest-theorem.md`, in all three provenance snapshots, and in the
four domain reviews, and it is byte-identical at `1b18842`, `8ce6358` and `HEAD` — so a third party
can obtain and check exactly the derivation those reviews claim to have read. Editing it to insert
cross-references would destroy that property, which is the one binding in this package that still
verifies end to end. The mapping is therefore additive. If the inline form is preferred later, it is
one line per section at the cost of that binding.

**No priority is claimed and none was.** `problem-contract.json`'s `literature_policy` permits
"checked primary sources **or** released repository derivations" and ends "No novelty or priority
claim is made." Three of the four domain reviews already cite these ancestors by line range. The
defect L1 records is that the mathematics document itself does not.

## Section-by-section correspondence

| `direct-derivation.md` | Prior result | Location at the 8/15 diff base |
|---|---|---|
| §3, (3.1)–(3.5): channel pushforward of the generative joint; the pushed posterior is a *version* including its selected exceptional values; observation marginal preserved | `thm:cg-evidence-preserving-channel` | `Theory/06_general_coarsegraining.tex:258-302` |
| §3, (3.6): absolute continuity transfers through the channel | corollary of the same theorem's null-set argument | `Theory/06_general_coarsegraining.tex:258-302` |
| §6, (6.1)–(6.4): joint lifts through a shared channel; lift-invariance of the Radon–Nikodym derivative; the additive extended-real chain identity with its nonnegative discarded-conditional defect | `thm:rg-exact-coarse-vfe` | `Theory/07b_agent_network_rg.tex:34-73` |
| §6, extended-real data processing and the nonnegative generator $\phi_0(t)=t\log t-t+1$ | `thm:cg-kl-dpi-extended` | `Theory/06_general_coarsegraining.tex:65-82` |
| §6, (6.8): the equality criterion | `thm:cg-dpi-equality` | `Theory/06_general_coarsegraining.tex:85-122` |
| §6, (6.9)–(6.12): the pairwise common-recovery equivalence, including the converse by data processing through $C_A$ and then through $R$ | `cor:cg-pairwise-bayes-recovery` | `Theory/06_general_coarsegraining.tex:124-140` |
| §6, line 379: $+\infty=+\infty$ carries no recovery consequence | `cor:cg-dpi-infinite-equality-warning` | `Theory/06_general_coarsegraining.tex:142-165` |

All seven prior results carry `\status{ESTABLISHED}` and were added by commit `bd46058`
(2026-08-08), a week before this package.

## External attribution

`thm:cg-dpi-equality` carries `\citet{Kullback1951,Csiszar1967}` in its proof at
`Theory/06_general_coarsegraining.tex:122`. That attribution is correct and should be read as
attaching to §6 of the derivation as well:

- S. Kullback and R. A. Leibler, "On information and sufficiency", *Annals of Mathematical
  Statistics* **22** (1951), 79–86.
- I. Csiszár, "Information-type measures of difference of probability distributions and indirect
  observations", *Studia Scientiarum Mathematicarum Hungarica* **2** (1967), 299–318.

The recovery statement (6.12) is the equality case of the data-processing inequality — sufficiency of
the channel for the pair, with $R$ the reverse map — and the chain identity (6.4) is the chain rule
for relative entropy applied to a joint lift through a common kernel. Both are standard; see also
Dobrushin (1959) and Polyanskiy–Wu, *Information Theory: From Coding to Learning*, Thm 2.14.

## What is genuinely new in this package

Not the four ancestors above. What §§1–9 add is the typed parent construction on top of them: the
belief/model/evaluator/holonomy coordinate structure of $\mathsf Z_A$, the pointwise framing at fixed
$r_*$, fixed structural $X$ and one admitted observation, the two-tier evaluator seam with its
explicit almost-sure compatibility hypothesis, the declared holonomy branch, and the five finite
categorical negative witnesses. Those are the parts a reader should assess for novelty.
