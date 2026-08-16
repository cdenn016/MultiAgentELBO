# V-P1-High-1-prior-work — adversarial skeptic attack

STATUS: COMPLETE

AGENT: skeptic, assigned to kill `P1-High-1-prior-work`
TARGET REVISION: `8ce635807a6ca2a388255fc996c98f7c535e5843` (branch `review/2026-08-15-deep-review`)
FINDING UNDER ATTACK: `[High-1]` in `docs/reviews/2026-08-15-deep-review/findings/P1-measure-probability.md:47-146`

## Verdict

**UPHELD_REDUCED. Corrected severity: Low.**

The mathematical half of the finding is correct and I reconstructed it independently: the affirmative
probabilistic core of `evidence/direct-derivation.md` §3 and §6 is a renaming of results already
`\status{ESTABLISHED}` in this repository on 2026-08-08. The finding actually *understates* how much
is prior art (see Correction 1 below).

The accusatory half — "with no citation and no hypothesis mapping ... violating the frozen contract's
own `literature_policy`" — is **false as stated**, and the finding's own declared falsifier is
satisfied by material inside the package. Four separate mechanical checks kill the High framing.
What survives is a documentation-placement and citation-form defect confined to one file, worth Low.

---

## What I checked, and how

Every claim below was established by executing the command shown or by reconstructing the
mathematics. No adjudication by reading either party's prose.

### Check 1 — the prior art exists (finding CORRECT)

```
$ git log -1 --format="%h %ad %s" bd46058
bd46058 Sat Aug 8 22:29:51 2026 -0500 docs: add gauge VFE RG theory snapshot
```

`git show 060f80e^:Theory/06_general_coarsegraining.tex` contains, all `\status{ESTABLISHED}`:

| label | lines | content |
|---|---|---|
| `def:cg-coarse-channel` / `prop:cg-markov-category` | 14–52 | channel definition, functoriality `P(KL)=(PK)L` |
| `thm:cg-kl-dpi-extended` | 65–82 | `KL(PK‖QK) ≤ KL(P‖Q)` in `[0,+∞]`, **no AC or finiteness hypothesis**, proof via `φ₀(t)=t log t − t + 1` |
| `thm:cg-dpi-equality` | 85–122 | `d(PK)/d(QK)=r̄`; equality iff `r(X)=r̄(Y)` `Q`-a.s.; **carries `\citet{Kullback1951,Csiszar1967}`** |
| `cor:cg-pairwise-bayes-recovery` | 124–140 | `QKR_Q=Q`; `PKR_Q=P` under equality; converse by DPI through `K` then `R` |
| `cor:cg-dpi-infinite-equality-warning` | 142–152 | `∞=∞` carries no recovery conclusion, **with a 3-point counterexample proof** |
| `thm:cg-evidence-preserving-channel` | 258–302 | `o↦P_oK` is a selected RCP version including exceptional-point values; `P̄^O=P^O`; ELBO monotonicity |

This is genuine prior art, seven days ahead of the program's first commit `ceffda2`. The finding is
right about this and I confirm it.

### Check 2 — my own side-by-side of statements, hypotheses, and proofs

**§3 vs `thm:cg-evidence-preserving-channel`.** Under the renaming
`(𝖮,𝖷,𝖸,K,P_o,Q_o) ↦ (𝖮,𝖸_I,𝖹_A,C_A,𝚷_{I,o,X},ℚ_{I,o,X})`:

- new (3.1) = prior `eq:cg-fixed-joint-pushforward` first component;
- new (3.3) `ℙ_A^O = ν_X` = prior `P̄^O = P^O`;
- new (3.4) first formula = prior `P̄_o := P_oK for every o`;
- new (3.5) + "indicators followed by a monotone-class argument" = prior "π–λ extension proves the
  regular-conditional identity";
- new :141 ("selects a globally measurable parent version, including declared exceptional-point
  values") = prior :271-272 ("including its selected exceptional-point values") and :296-298.

Same statement, same proof move, same load-bearing hypothesis (`K` normalized on every point,
recognition-independent, acting only on the conditioned variable). Hypotheses **coincide** on the
shared content. The new version adds three things the prior theorem does not have: the fixed
structural datum `X` with the explicit no-cross-`X`-factorization fence (:6), the product typing
`𝖹_A = 𝖡_A × 𝖬_A × 𝚵_A × 𝖧_A`, and an explicit σ-finite `λ_X` with a density representative
(:47-53) where the prior merely says "use the same declared evidence density representative `p(o)`".
It also drops the prior's ELBO-monotonicity conclusion (deferred to §6). One step is genuinely
absent from the prior theorem: (3.6), absolute-continuity transfer — `thm:cg-evidence-preserving-channel`
explicitly needs no AC and handles `Q_o ⋠ P_o` with `−∞`. The finding lumps (3.6) in with the rest;
it should not.

**§6 (6.9)–(6.12) vs `cor:cg-pairwise-bayes-recovery`.** Under `(P,Q,K,R_Q) ↦ (ℚ_I,𝚷_I,C_A,R_𝚷)`:
`QKR_Q=Q` ↦ (6.10) `𝚷_A R_𝚷 = 𝚷_I`; `PKR_Q=P` under equality ↦ (6.11); "any one kernel `R`
recovering both forces equality" ↦ (6.12), with the identical one-line proof ("data processing
through `C_A` and then through `R`"). The finiteness hypothesis is present in both (prior: inherited
from `thm:cg-dpi-equality`; new: stated explicitly at :370). **Identical.**

**(6.8) vs `eq:cg-kl-equality`.** The finding calls these "equivalent, not stronger". I verified it.
With `r = dℚ_I/d𝚷_I`, (6.2) gives `dℚ̂/d𝚷̂(Y,z) = r(Y)`. Disintegrating over `z`:
`dℚ_A/d𝚷_A(z) = r̄(z) := ∫ r(Y) 𝚷̂(dY|z)`, and therefore
`dℚ̂(·|z)/d𝚷̂(·|z)(Y) = r(Y)/r̄(z)` for `ℚ_A`-a.e. `z`. Hence `ℚ̂(·|z) = 𝚷̂(·|z)` for `ℚ_A`-a.e. `z`
iff `r(Y) = r̄(z)` `𝚷̂`-a.s., which is exactly `eq:cg-kl-equality`. Equivalent. Confirmed.

**:379 vs `cor:cg-dpi-infinite-equality-warning`.** The new text asserts "Equality `+∞=+∞` supplies
neither (6.8) nor (6.12)" as a bare sentence; the prior corollary *proves* it with an explicit
three-point counterexample. The new version is the weaker of the two here.

So the finding's mathematics is right: the affirmative probabilistic core of §3 and §6 is a
renaming, not a new derivation.

### Check 3 — the finding's declared falsifier is SATISFIED (kills the High framing)

The finding states its own falsifier at :134-137:

> "A citation, hypothesis-mapping table, or 'prior repository result' note **anywhere in the 8/15
> package** pointing at `Theory/06_general_coarsegraining.tex`. I grepped the package for
> `06_general`, `cg-`, `Kullback`, `Csiszar` and for `\cite`: **nothing**."

That grep result is wrong.

```
$ grep -rn "06_general" docs/derivations/2026-08-15-full-pointwise-meta-agent/ | wc -l
19
```

Nineteen hits across five package files. The substantive ones are exact line-range citations inside
the package's own domain-review evidence documents, each carrying a mapping sentence:

| package location | cites | prior result it maps to |
|---|---|---|
| `evidence/reviews/view-probability-kernel.md:43` | `06:14-52` | "matches the canonical channel definition and functorial normalization proof" → `def:cg-coarse-channel`, `prop:cg-markov-category` |
| `evidence/reviews/view-probability-kernel.md:45` | `06:258-302` | "**This is the selected-version-qualified identity already proved canonically**" → `thm:cg-evidence-preserving-channel` |
| `evidence/reviews/view-probability-kernel.md:51` | `06:65-82` | the `φ₀` extended proof → `thm:cg-kl-dpi-extended` |
| `evidence/reviews/view-probability-kernel.md:51` | `06:124-165` | "**matching the canonical recovery boundary**" → `cor:cg-pairwise-bayes-recovery`, `cor:cg-dpi-infinite-equality-warning` |
| `evidence/reviews/view-probability-kernel.md:51` | `07b:34-66` | "**consistent with the canonical exact VFE theorem**" → `thm:rg-exact-coarse-vfe` |
| `evidence/reviews/view-information-vfe.md:50` | `06:62-165`, `06:255-311`, `07b:13-73` | "I independently reconstructed the load-bearing relative-entropy argument and **checked it against the canonical statements in** …" |
| `evidence/reviews/view-information-vfe.md:112` | `06:85-165` | "This reconstructs `VFE-FINITE-ZERO-DEFECT-RECOVERY` at `direct-derivation.md:333-381` and **matches** …" |

**All four of the finding's named ancestors are cited by exact file and line range inside the
package, each with an explicit "already proved canonically / matches / consistent with" mapping
sentence.** The finding's stated falsifier is met.

(The obvious rejoinder — "the domain reviews are internal attestations and P1's stance excludes
them as evidence" — does not rescue the finding. That stance governs whether an attestation can
*verify mathematics*. Whether a citation exists is a textual fact about bytes on disk, not an
attestation. And Check 4 supplies a pointer that is not an attestation at all.)

### Check 4 — the program wrote the "prior results invoked" note the finding demands (kills it again)

The finding asserts at :137-139: "the program's only edit to that file (`fe08359`) changed two
lines." False.

```
$ git log --oneline --follow -- Theory/06_general_coarsegraining.tex
fe08359 docs: correct pointwise VFE scope
b9ba51f docs: integrate pointwise probabilistic datum
bd46058 docs: add gauge VFE RG theory snapshot
```

`b9ba51f` (this program, 2026-08-15) added a 29-line paragraph to the canonical chapter at
`Theory/06_general_coarsegraining.tex:304-331`, reading in part:

> "Specializing `\Cref{thm:cg-evidence-preserving-channel}` gives [(3.1) and `𝚷_{A,o,X}=𝚷_{I,o,X}C_A`]
> … **This is a typed specialization of the preceding theorem, not a second posterior-pushforward
> theorem.** The associated KL/VFE loss is the common-channel chain rule of
> `\Cref{thm:rg-exact-coarse-vfe}`, specialized in `\Cref{thm:rg-pointwise-parent-datum}`."

That is precisely the note the finding's own **Fix** section demands ("an explicit 'prior results
invoked' note naming `thm:cg-evidence-preserving-channel` … with the symbol map"), naming the prior
theorem by `\Cref` label, written by the same program in the same commit series. `b9ba51f` also
added 152 lines to `Theory/07b_agent_network_rg.tex` establishing `thm:rg-pointwise-parent-datum` as
the canonical integration. The program did not pass these results off as new; it labeled them a
specialization of a named prior theorem. The defect is that the label sits in `Theory/`, at the
other end of the link from `evidence/direct-derivation.md`.

### Check 5 — the contract clause is quoted truncated, and the omitted half reverses its force

`problem-contract.json:74` in full:

> `"literature_policy": "Use only checked primary sources **or released repository derivations** for
> invoked theorems; record exact statements and hypothesis mappings. **No novelty or priority claim
> is made.**"`

The finding quotes through "hypothesis mappings" and stops. Two consequences:

1. The policy is **disjunctive**. Citing the released repository derivation discharges it; primary
   sources are not additionally required. The package cites the released repository derivation
   (Check 3). No violation.
2. The clause's final sentence expressly disclaims novelty and priority. The finding is a
   prior-art/priority charge levied against a contract that pre-emptively disclaims priority.

The finding also omits `problem-contract.json:67-71`, `permitted_theorems`, which pre-declares as
invoked background: "Normalized Markov-kernel pushforward and composition on standard-Borel spaces",
"Existence and use of declared regular conditional probabilities and disintegrations", and
"**KL data processing and the common-channel conditional-KL chain rule** under the recorded
finiteness hypotheses". The contract names the very results at issue as *invoked*, not derived.

I also checked `final-report.md` and `construction-or-strongest-theorem.md` for any novelty or
priority language: none. `grep -rniE "novel|priority|first |original contribution"` over the package
returns only the `novelty_fingerprint` schema field in `approach-registry.json`, which is the
search skill's per-approach de-duplication key, not a literature claim.

---

## Corrections to the finding (errors in the investigator's own record)

**Correction 1 — the finding misses a fifth prior result, and it is the one the finding credits as
new.** The finding's "What is actually new, stated fairly" list leads with: "the upgrade of the DPI
*inequality plus separate equality condition* to the *additive chain identity* (6.4) with the named
nonnegative defect `Δ_A` (**a genuine strengthening, and the correct one**)". That is prior art too.
`git show 060f80e^:Theory/07b_agent_network_rg.tex:34-73` is `thm:rg-exact-coarse-vfe`
(`\status{ESTABLISHED}`, commit `bd46058`, 2026-08-08), which already contains verbatim:

- `eq:rg-bridge-lifts` — the two joint lifts through the common channel = new (6.1);
- "Attaching the same channel to both measures preserves the fine relative entropy,
  `KL(Q_o‖Π_o)=KL(Q̂_o‖Π̂_o)`" = new (6.3);
- `eq:rg-vfe-chain-rule` — `F_P(Q_o) = F_{P^c}(Q_o^c) + ∫ KL(Q̂_o(dy|z)‖Π̂_o(dy|z)) Q_o^c(dz)`,
  declared as an extended-real additive identity = new (6.4)/(6.6), with the defect already named
  "discarded conditional information";
- "If the fine KL is finite, their ordinary real-valued difference equals the displayed conditional
  KL" = new (6.7);
- the same four-step proof (observation marginal unchanged; attach channel; disintegrate on `z`;
  relative-entropy chain rule).

This strengthens the "not new" conclusion and simultaneously falsifies the finding's novelty
inventory. Notably, the package cites this too (`view-probability-kernel.md:51`,
`view-information-vfe.md:93` → `07b:34-66`).

**Correction 2 — misattributed theorem.** The finding attributes both the equality condition
`r(X)=r̄(Y)` and the `\citet{Kullback1951,Csiszar1967}` citation to `thm:cg-kl-dpi-extended`. Both
belong to `thm:cg-dpi-equality` (`06:85-122`). `thm:cg-kl-dpi-extended` (`06:65-82`) is the
hypothesis-free inequality and carries no citation at all. One of the four named "prior theorems" is
therefore misidentified in the finding's evidence block.

**Correction 3 — false statement about the program's edits.** See Check 4.

**Correction 4 — the falsifier check was not performed correctly.** See Check 3.

## Primary-source check on the "standard result"

Per the review brief I verified the prior chapter's attribution rather than trusting it.
Kullback & Leibler, *On Information and Sufficiency*, Ann. Math. Statist. **22**(1):79–86 (1951) —
confirmed to establish that information is non-increasing under a statistic with equality attained
by sufficient statistics. Csiszár, *Information-type measures of difference of probability
distributions and indirect observations*, Studia Sci. Math. Hungar. **2**:299–318 (1967) — confirmed
as the introduction of the `f`-divergence class and its behavior under observation channels. The
prior chapter's "This is the information-loss theorem of `\citet{Kullback1951,Csiszar1967}` in kernel
form" is an accurate attribution. Dropping these two keys from the 8/15 package therefore loses real
attribution value — which is the residue that survives below.

Sources: [Kullback & Leibler 1951 (Project Euclid)](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-22/issue-1/On-Information-and-Sufficiency/10.1214/aoms/1177729694.full),
[Csiszár 1967 / f-divergence (DML-CZ)](https://dml.cz/handle/10338.dmlcz/140026).

---

## What survives, and at what severity

**Corrected finding (Low):** `evidence/direct-derivation.md` — the sole `DERIVATION` evidence
(`EV-TASK3-DIRECT-DERIVATION`) for `PARENT-NORMALIZATION`, `POSTERIOR-PUSHFORWARD`,
`COMMON-CHANNEL-ABSOLUTE-CONTINUITY`, `VFE-CHAIN-EXTENDED`, and
`VFE-FINITE-ZERO-DEFECT-RECOVERY` — contains no pointer to the prior repository theorems it
re-derives (`grep "06_general\|07b_agent\|cg-\|rg-exact" evidence/direct-derivation.md` → 0). Read
alone, the mathematics document presents §3 and §6 as first derivations. The linkage exists, but
only in `evidence/reviews/*.md` and in `Theory/06`/`Theory/07b`. Two smaller companions:
prior theorem *labels* appear nowhere in the package (`grep -rn "cg-" package` → 0), so the citations
are line ranges that drift under edits; and `Kullback1951`/`Csiszar1967` are carried nowhere into the
package (`grep -rniE "kullback|csisz" package` → 0), losing an accurate primary attribution.

**Why Low, not High:**
- No correctness consequence. The finding alleges no mathematical error, and I found none; my
  reconstruction agrees with the principal reviewer's.
- No contract violation. The policy is disjunctive, the repository derivation is cited, the contract
  disclaims novelty and priority outright, and it pre-declares these very theorems as
  `permitted_theorems`.
- No novelty or priority claim is made anywhere in the package.
- The finding's own declared falsifier is satisfied by package bytes.
- The remedy is one cross-reference line per section, in one file.

The *substantive* observation inside the finding — that the affirmative probabilistic core is not new
— stands, is correct, and is in fact stronger than the finding states (Correction 1). But that is an
attribution/novelty observation, and P0 already logged it as "NOT a correctness finding". It belongs
in the report's novelty accounting, not as a High defect against the derivation.

## Relation to the principal reviewer's notes

No contradiction. `P0-principal-reviewer-notes.md:42-64` and `:88-105` independently reconstruct the
KL chain and the recovery theorem and find both correct and classical, and `:66-86` records that
"Attribution and novelty are the live issues, not correctness." My reconstruction reaches the same
place from the repository side and adds the specific fact P0 did not have: the classical results
were already written down *in this repository* on 2026-08-08 with correct primary-source citations,
and the 8/15 package does cite them — by line range, in its review documents and in the canonical
chapter, but not in the derivation itself.

## Falsifier of my own attack

My verdict is wrong if the intended scope of "the 8/15 package" excludes both
`docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/reviews/*.md` and the program's
`Theory/` integration commits. Under that narrow reading — package = `direct-derivation.md` plus the
top-level JSON/markdown artifacts only — the citation gap is total within scope and High could be
argued. I reject that reading because the finding's own falsifier says "**anywhere in the 8/15
package**", and `evidence/reviews/` sits inside the package directory; and because the
`Theory/06` specialization paragraph was authored by the same program in the same commit series and
is not an attestation.

A second, sharper falsifier: if `git show 060f80e^:Theory/07b_agent_network_rg.tex` did *not* contain
`thm:rg-exact-coarse-vfe`, Correction 1 collapses and the finding's novelty inventory is restored. I
ran that command; it does contain it, at lines 34–73.

A third: if any package artifact were shown to assert novelty or priority for §3 or §6, the High
severity would return. I grepped `*.md` and `*.json` in the package for
`novel|priority|first |original contribution|new theorem` and found only the schema field
`novelty_fingerprint`.

## Commands executed

```
git log -1 --format="%h %ad %s" bd46058
git log --oneline --follow -- Theory/06_general_coarsegraining.tex
git log --oneline -- Theory/07b_agent_network_rg.tex
git show 060f80e^:Theory/06_general_coarsegraining.tex   (765 lines, read 1-170, 254-343)
git show 060f80e^:Theory/07b_agent_network_rg.tex        (read 20-70)
git show b9ba51f -- Theory/06_general_coarsegraining.tex (+29 lines)
git show fe08359 -- Theory/06_general_coarsegraining.tex (+1/-1 line)
git show b9ba51f --stat -- Theory/07b_agent_network_rg.tex  (+152 lines)
grep -rn "06_general" docs/derivations/2026-08-15-full-pointwise-meta-agent/ | wc -l   -> 19
grep -rn "cg-"       docs/derivations/2026-08-15-full-pointwise-meta-agent/ | wc -l   -> 0
grep -rniE "kullback|csisz" docs/derivations/2026-08-15-full-pointwise-meta-agent/    -> 0 hits
grep -rno "06_general_coarsegraining\.tex:[0-9-]*"  .../evidence/reviews/ | sort -u
grep -rno "07b_agent_network_rg\.tex:[0-9-]*"       .../evidence/reviews/ | sort -u
grep -niE "canonical|prior|already|estab" .../evidence/direct-derivation.md   -> no prior-art pointer
```
