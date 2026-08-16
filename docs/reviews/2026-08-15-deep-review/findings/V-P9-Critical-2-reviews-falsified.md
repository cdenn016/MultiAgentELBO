STATUS: COMPLETE
ROLE: adversarial skeptic (wave 2), assigned to kill `P9-Critical-2-reviews-falsified`
TARGET REVISION: 8ce635807a6ca2a388255fc996c98f7c535e5843
VERDICT: **UPHELD** at **Critical**, with one correction to the finding's headline count
(four reviews -> two of four fire unambiguously; the defect and its severity are unchanged).

# V-P9-Critical-2: attack on "The four domain reviews satisfy their own stated falsification condition"

## Summary of the attack and its outcome

I tried five distinct ways to kill this finding. Four of them are the standard kills for a finding of
this shape, and every one of them fails against reconstructable evidence. The fifth lands, but only
against the finding's headline count, not against the defect.

| Attack | Outcome |
|---|---|
| A. "The reviews name `add1a69` openly, so the release does not misrepresent them as current." | **Fails.** `release-assembly.json` stamps `"binding_state": "BOUND_CURRENT_APPROVE"` and `release.json` ships `terminal_status: COMPLETE_AFFIRMATIVE`, `unresolved_obligations: []`, whose gate reason asserts the four reviews are *current*. |
| B. "Only bookkeeping metadata changed; the mathematics the reviews saw is byte-identical." | **Fails.** True inside the package (`direct-derivation.md`, `counterexample-proofs.md`, `notation-standard.md`, `dependency-dag.json` are all unchanged) but false for the bound canonical sources: `Theory/07b_agent_network_rg.tex` gained 112 lines containing the entire certified theorem, and its zero-defect sentence was rewritten. |
| C. "The falsifier reads `¬re-review ∧ ¬re-hash`, and re-hashing did happen." | **Fails.** For the two canonical sources *both* conjuncts are absent: neither post-mutation hash appears anywhere in the package. The falsifier fires under either parse. |
| D. "The bound hashes were never reproducible, so 'mutation' is unprovable (cf. Critical-1)." | **Fails.** Unlike the package snapshot, the canonical-source bindings reproduce *exactly* from git. This is the one leg of the P9 evidence that is fully auditable. |
| E. "Not all four reviews have such a condition." | **Lands, partially.** `view-information-vfe.md` has no byte-mutation falsifier and none of its eight mathematical conditions is exhibited; `view-dynamics-scope.md`'s condition 6 is qualified and ambiguous. Correct count is two of four. |

The finding survives. The certification is invalid by the release's own rules, which under the review
protocol's severity scale (`RESUME.md:64`: *Critical = a stated theorem is false **or the
certification is invalid***) is Critical on the second disjunct.

---

## 1. The quoted falsification conditions, verbatim and located

`evidence/reviews/view-probability-kernel.md:63,72`

> This approval is falsified for the frozen bytes if any of the following is exhibited:
> […]
> - post-review mutation of any bound artifact byte, hypothesis, claim statement, or canonical source
>   without re-review and re-hashing.

`evidence/reviews/view-gauge-holonomy.md:185,196`

> This approval must be withdrawn if any of the following is exhibited for the frozen bytes:
> […]
> 10. Mutation of any bound artifact, canonical source, assumption, or claim statement without
>     re-review and recomputation of its SHA-256.

`evidence/reviews/view-dynamics-scope.md:106,113`

> This approval would be falsified by any of the following:
> […]
> 6. drift of any corrected input hash above before coordinator rebinding.

`evidence/reviews/view-information-vfe.md:146-157` — eight conditions, **all mathematical**. There is
no byte-mutation or hash-drift clause in this review at all.

## 2. Both canonical sources are bound by three reviews and both mutated at the release

The bindings (identical value in all three tables):

- `view-probability-kernel.md:31-32`
- `view-gauge-holonomy.md:30-31`
- `view-information-vfe.md:29-30`

```
| `Theory/06_general_coarsegraining.tex` | `4891a8f5fa86ac0fa5266381e2c67161125645034ca40395cb2e3ed1b67dc9b2` |
| `Theory/07b_agent_network_rg.tex`      | `5eb159493ec727218e2eaca4cf47f3fddeb090f6e193352846ad2a43181437ca` |
```

`.gitattributes:22` is `Theory/** text eol=crlf`, so the worktree bytes are CRLF. Executed:

```bash
$ for rev in add1a69 1b18842 b9ba51f fe08359 063a5bb 8ce6358; do
    for f in Theory/06_general_coarsegraining.tex Theory/07b_agent_network_rg.tex; do
      printf "%s %-40s " "$rev" "$(basename $f)"
      git show $rev:$f | sed 's/$/\r/' | sha256sum | cut -c1-64
    done
  done
add1a69 06_general_coarsegraining.tex   4891a8f5fa86ac0fa5266381e2c67161125645034ca40395cb2e3ed1b67dc9b2
add1a69 07b_agent_network_rg.tex        5eb159493ec727218e2eaca4cf47f3fddeb090f6e193352846ad2a43181437ca
1b18842 06_general_coarsegraining.tex   4891a8f5fa86ac0fa5266381e2c67161125645034ca40395cb2e3ed1b67dc9b2
1b18842 07b_agent_network_rg.tex        5eb159493ec727218e2eaca4cf47f3fddeb090f6e193352846ad2a43181437ca
b9ba51f 06_general_coarsegraining.tex   1c6bf3e6ece30b884629f613efedf99992dab4b439deed18a209ae3f85f8753a
b9ba51f 07b_agent_network_rg.tex        33560b050436dd77fd61a8e857de544018cb0d6120912ee4a867a60982d99d28
fe08359 06_general_coarsegraining.tex   fa10620d2a1d0e51b5a50b88d0a7434afcde6a0112af062e74fed586e97d7166
fe08359 07b_agent_network_rg.tex        268f9c3b75b09966ed05a6c08e0cbd3f17188d88143f599037ff371d9c3e598c
063a5bb 06_general_coarsegraining.tex   fa10620d2a1d0e51b5a50b88d0a7434afcde6a0112af062e74fed586e97d7166
063a5bb 07b_agent_network_rg.tex        268f9c3b75b09966ed05a6c08e0cbd3f17188d88143f599037ff371d9c3e598c
8ce6358 06_general_coarsegraining.tex   fa10620d2a1d0e51b5a50b88d0a7434afcde6a0112af062e74fed586e97d7166
8ce6358 07b_agent_network_rg.tex        268f9c3b75b09966ed05a6c08e0cbd3f17188d88143f599037ff371d9c3e598c
$ sha256sum Theory/06_general_coarsegraining.tex Theory/07b_agent_network_rg.tex   # worktree
fa10620d2a1d0e51b5a50b88d0a7434afcde6a0112af062e74fed586e97d7166 *Theory/06_general_coarsegraining.tex
268f9c3b75b09966ed05a6c08e0cbd3f17188d88143f599037ff371d9c3e598c *Theory/07b_agent_network_rg.tex
```

The bound values reproduce **exactly** at `add1a69` and `1b18842`; they are different at the released
revision, having mutated twice (`b9ba51f`, then `fe08359`). Attack D is dead: this is the one
hash-binding leg in the whole P9 evidence set that a third party can fully audit, and it fails.

## 3. Neither re-review nor re-hash exists for the mutated canonical sources

```bash
$ grep -rn "fa10620d\|268f9c3b\|c12c16d9\|489e8128" --include=*.md --include=*.json .
docs/reviews/2026-08-15-deep-review/findings/P8-integration-overclaim.md:374,391,392
docs/reviews/2026-08-15-deep-review/findings/P9-selfcert-falsifiability.md:143,151
```

The only occurrences in the repository are inside the two wave-1 finding files written *by this
review*. Independently:

```bash
$ grep -rn "4891a8f5\|5eb15949\|Theory/06\|Theory/07b" docs/derivations/2026-08-15-full-pointwise-meta-agent
# only: the three review tables (old hashes), and unhashed `"path"` strings in notation-collision-report.json
```

No `Theory/*` SHA-256 appears in `release.json`, `release-assembly.json`, or `release-provenance.json`
at all. So for the canonical sources the mutation carries **neither** re-review **nor** re-hashing.
Attack C is dead: the falsifier fires under the strict parse `¬(re-review ∧ re-hash)` and equally
under the charitable parse `¬re-review ∧ ¬re-hash`.

## 4. The mutation is mathematical content, not cosmetics

`b9ba51f` ("docs: integrate pointwise probabilistic datum") inserted the certified theorem into the
canonical source. At the released revision, `Theory/07b_agent_network_rg.tex:76-185` is

```latex
\theoremheading{Full pointwise probabilistic datum for a candidate parent}{thm:rg-pointwise-parent-datum}
...
\KL(\mathbb Q_{I,o,X}\Vert\boldsymbol\Pi_{I,o,X})
=\KL(\mathbb Q_{A,o,X}\Vert\boldsymbol\Pi_{A,o,X})+\Delta_A(o,X),
...
\status{ESTABLISHED}
```

— the whole target datum (spaces, channel, three parent laws, evaluator, six marginals, KL chain,
defect, zero-defect criterion) as `\status{ESTABLISHED}` canonical theory. `Theory/06` likewise gained
a `\status{ESTABLISHED}` "Pointwise parent specialization" paragraph carrying
`\boldsymbol\Pi_{A,o,X}=\boldsymbol\Pi_{I,o,X}C_A`, the certified `POSTERIOR-PUSHFORWARD` identity.

This matters concretely for the review record. `view-probability-kernel.md:34` states: "I read … all
of canonical `Theory/06_general_coarsegraining.tex`, and the complete probability/kernel spans of
canonical `Theory/07b_agent_network_rg.tex` (`1-204`, `1130-1912`, and `2725-2828`)." At the released
bytes, `1-204` contains a 110-line theorem that did not exist when the reviewer read the file, and
every line citation above 72 is off by 112.

`fe08359` then rewrote the zero-defect statement inside that block:

```diff
-If the fine KL is finite, the ordinary difference ... and $\Delta_A=0$ exactly when the two discarded
-conditional laws ... agree $\mathbb Q_{A,o,X}$-almost surely. On that finite tier, zero defect is
-equivalent to one normalized pairwise recovery kernel recovering both declared fine laws.
+Without a finite-fine-KL premise, $\Delta_A=0$ exactly when the two discarded conditional laws in
+\eqref{eq:rg-pointwise-parent-defect} agree $\mathbb Q_{A,o,X}$-almost surely. Finite fine KL is
+required for the ordinary subtraction ... and for the stated two-way pairwise common-recovery equivalence.
```

with two further corrections to the same statement in `Theory/appendix_notation.tex` at `f4b1a61` and
`063a5bb`. Attack B is dead.

## 5. Sequencing: the certification was declared final, then the certified statement was corrected four times

```bash
$ for c in add1a69 1b18842 a623b6e b9ba51f fe08359 9ddd757 f4b1a61 063a5bb; do
    printf "%s %-38s " "$c" "$(git log -1 --format=%s $c | cut -c1-38)"
    git show $c:docs/derivations/2026-08-15-full-pointwise-meta-agent/release.json \
      | grep -o '"terminal_status": *"[^"]*"\|"terminal_status": *null' | head -1
  done
add1a69 docs: witness pointwise meta-agent clo   "terminal_status": null
1b18842 docs: certify full pointwise meta-agen   "terminal_status": "COMPLETE_AFFIRMATIVE"
a623b6e docs: refresh pointwise meta-agent evi   "terminal_status": "COMPLETE_AFFIRMATIVE"
b9ba51f docs: integrate pointwise probabilisti   "terminal_status": "COMPLETE_AFFIRMATIVE"
fe08359 docs: correct pointwise VFE scope        "terminal_status": "COMPLETE_AFFIRMATIVE"
9ddd757 docs: close full pointwise meta-agent    "terminal_status": "COMPLETE_AFFIRMATIVE"
f4b1a61 docs: correct zero-defect notation bou   "terminal_status": "COMPLETE_AFFIRMATIVE"
063a5bb docs: finalize zero-defect closure wor   "terminal_status": "COMPLETE_AFFIRMATIVE"

$ git log --oneline -- .../evidence/reviews/
a623b6e docs: refresh pointwise meta-agent evidence
1b18842 docs: certify full pointwise meta-agent
```

The four review files were last touched at `a623b6e`. Every subsequent commit — including two that
rewrite the certified zero-defect statement in canonical sources — leaves `terminal_status:
COMPLETE_AFFIRMATIVE` and `unresolved_obligations: []` untouched. A certification that is declared
terminal at *t* and whose subject is then corrected four times after *t*, with the obligation list
frozen empty, is invalid on its face, independent of any hash argument.

## 6. Attack A: the package's own rule, turned on the package

The strongest defense is that the release is transparent — `release.json:57-62` records
`"review_input_snapshot": "corrected-pre-review-add1a69"`, so a reader knows the reviews predate the
release metadata. That defense dies on two texts.

`release-assembly.json:73,86,99,112` stamp the four slots `"binding_state": "BOUND_CURRENT_APPROVE"`,
and `release-assembly.json:193` (`release_gate.reason`) reads: "…all four corrected-byte domain
reviews are **current** APPROVE records with no Critical, High, or Medium finding."
`release.json:9` says the same in `strongest_result`: "four **current** corrected-byte domain
approvals."

And `view-information-vfe.md:46` states the package's *own* rule for exactly this situation:

> The corrected release also binds the four initial review hashes while correctly recording that they
> predate the correction and cannot authorize promotion without same-view bounded re-review.

Apply that rule to the corrected reviews: they predate the `b9ba51f`/`fe08359` corrections to the
canonical sources they bind, therefore they "cannot authorize promotion without same-view bounded
re-review." Promotion happened anyway — `target` went `CANDIDATE` -> `EVIDENCE_VERIFIED`,
`terminal_status` `null` -> `COMPLETE_AFFIRMATIVE`. This is not an outside standard imposed on the
package; it is the package's stated rule violated by the package.

A weaker fallback defense is that `"BOUND_CURRENT_APPROVE"` means only "the bound value is the
review file's current hash". Even granting that parse, the gate still counts as a support four reviews
whose own written invalidation clauses have fired, which is the defect.

## 7. Attack E: the one place the finding overstates — the count

This is the only attack that lands, and it lands on the headline, not the defect.

- `view-probability-kernel.md:72` — **fires**, unambiguously (bound canonical source mutated, no
  re-review, no re-hash).
- `view-gauge-holonomy.md:196` — **fires**, unambiguously (same two canonical sources are in its
  binding table at `:30-31`).
- `view-dynamics-scope.md:113` — **ambiguous.** Its binding table (`:20-35`) contains no canonical
  source, only package artifacts, and its clause is qualified "*before coordinator rebinding*". The
  two-stage provenance model expressly anticipates that the ledger/report/release hashes change when
  the coordinator rebinds. I do not count this one as fired.
- `view-information-vfe.md:148-157` — **does not fire.** Its eight conditions are purely mathematical
  and none is exhibited. In particular its condition 2, "a finite-KL in-domain pair with `Delta_A=0`
  but unequal discarded conditionals on a set of positive `Q_A` mass," cannot be exhibited: `Delta_A`
  is the integral of a nonnegative measurable integrand against `Q_A`, so `Delta_A=0` iff that
  integrand vanishes `Q_A`-a.e., and a KL vanishes iff the two laws coincide. No finiteness enters.

So the correct headline is **two of four**, not four. This does not touch the severity or the fix:
the gate's stated reason is "all four … are current", so one falsified review already makes it false.

## 8. A defect adjacent to the finding, which the finding misses

The orchestration prompt asked whether any review text still states the superseded finite-KL
zero-defect criterion. It does — but the direction is the opposite of what was hypothesized.

`view-probability-kernel.md:51`: "**On finite fine KL**, zero defect is equivalent to equality of
discarded conditionals `Q_A`-almost surely…"

That finite-KL qualifier is not in the reviewed derivation. `evidence/direct-derivation.md` (6.8),
whose hash `2aa70b07751d…` is **identical** in the review-input snapshot and at the released revision,
already states the criterion unconditionally and gives the right reason: "A nonnegative measurable
function has zero integral exactly when it is zero almost surely, and KL vanishes exactly at equality
of probability measures." The reviewer read a strictly weaker statement than the one proved and than
the one shipped. That is a scope gap between the review and the release, but it is conservative — it
certifies less than the package claims, so it introduces no error into the release.

I reconstructed the released statement independently and it is correct: with
`Delta_A = ∫ KL(Q̂(·|z) ‖ Π̂(·|z)) Q_A(dz)` and integrand in `[0,+∞]`, `Delta_A = 0` iff the integrand
vanishes `Q_A`-a.e. iff `Q̂(·|z) = Π̂(·|z)` for `Q_A`-a.e. `z`; finiteness is needed only for the
subtraction `F_I − F_A = Delta_A` and for the recovery converse. The post-certification edits at
`fe08359`/`f4b1a61`/`063a5bb` therefore moved the canonical text *toward* correctness. That is a point
in the author's favor on the mathematics — and simultaneously the sharpest evidence for this finding
on the process: those corrections are precisely the changes a certification is supposed to be made
after, not before.

## 9. Relation to `P0-principal-reviewer-notes.md`

No contradiction. P0 reconstructs the posterior-version pushforward, parent absolute continuity, the
additive KL chain, and the recovery/DPI-equality theorem and marks each **CHECKS OUT**, and P0's
§"the unconditional zero-defect criterion also checks out" agrees with my §8 reconstruction line for
line. This finding asserts no mathematical error and is fully compatible with all of that: it is a
defect in the *certification apparatus*, which is the same organ P0 independently faults ("a process
that … does not notice that the theorem was already proved in the same repository is not measuring
what its `EVIDENCE_VERIFIED` label claims to measure"; "the certification apparatus should be read as
bookkeeping, not as evidence").

One P0 observation does blunt part of the finding's *rhetoric*, and I record it against the
investigator: P0 verifies that `thm:cg-evidence-preserving-channel` was already `\status{ESTABLISHED}`
in `Theory/06` before this work (commit `bd46058`). So the wave-1 sentence "The certification's
'canonical source' was amended, after the review, to contain the proposition being certified" overstates
the circularity — the general theorem predates the package, and the inserted paragraph labels itself
"a typed specialization of the preceding theorem, not a second posterior-pushforward theorem." The
mutation is real and load-bearing for the falsification clause; it is not the manufacture of a premise
out of nothing. The final report should use the mutation, not the circularity framing.

## 10. Severity

`RESUME.md:64` defines **Critical** as "a stated theorem is false **or the certification is invalid**."
No stated theorem is shown false here. The certification is invalid, on three independent grounds:
(i) two of the four reviews the gate counts have had their own written invalidation clauses fire and
no re-review exists; (ii) two bound canonical sources changed with neither re-review nor re-hash;
(iii) `terminal_status: COMPLETE_AFFIRMATIVE` with `unresolved_obligations: []` was frozen at
`1b18842` and the certified statement was corrected four times afterward. Critical stands on the
second disjunct of the scale. I initially wanted to reduce this to High by analogy with P0's
attribution finding; the rubric does not permit that, because the rubric puts certification validity
on par with theorem falsity.

## 11. Corrected finding text for the final report

Replace the title with:

> **[Critical] Two of the four domain reviews have had their own stated falsification condition fire
> at the released bytes, and the release gate counts all four as current**

and amend the Evidence section to (a) state the count as two of four, naming
`view-information-vfe.md` as having no byte-mutation clause and `view-dynamics-scope.md` as ambiguous;
(b) lead with the canonical-source hash reconstruction, which is fully auditable, rather than with the
unrecoverable package snapshot, which belongs to Critical-1; (c) drop the "amended to contain the
proposition being certified" framing per §9; (d) add the `1b18842`-then-four-corrections sequencing
from §5, which establishes the defect without any hash argument at all.

The finding's stated Fix is correct as written: re-run the views against the released bytes, or
downgrade `binding_state` to `STALE` and remove the reviews from the release gate's `reason`.

## Falsifier of this attack

My verdict is wrong if any of the following is produced:

1. A review artifact anywhere in this repository or in a branch the release cites that binds
   `Theory/06_general_coarsegraining.tex` = `fa10620d2a1d…` and `Theory/07b_agent_network_rg.tex` =
   `268f9c3b75b0…` with a current `APPROVE`. My `grep -rn` over all `.md`/`.json` found those strings
   only inside wave-1 finding files.
2. A written definition, inside the package, of `BOUND_CURRENT_APPROVE` and of the gate's word
   "current" that explicitly means "hash of the review file as committed" and explicitly disclaims
   currency with respect to the released payload — which would defuse §6 but not §3 or §5.
3. A demonstration that `Theory/06`/`Theory/07b` are not review *inputs* but decorative citations —
   refuted already by `view-probability-kernel.md:34` (declared read spans) and `:51` plus the
   `POSTERIOR-PUSHFORWARD` item of its derivation audit, both of which verify package claims *against*
   those files ("This is the selected-version-qualified identity already proved canonically
   (`Theory/06_general_coarsegraining.tex:258-302`)"; "consistent with the canonical exact VFE theorem
   (`Theory/07b_agent_network_rg.tex:34-66`)").
4. A change to `RESUME.md:64` removing "or the certification is invalid" from the Critical band, which
   would move this finding to High.
