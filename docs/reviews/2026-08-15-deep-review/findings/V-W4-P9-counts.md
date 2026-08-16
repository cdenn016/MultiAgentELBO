STATUS: COMPLETE
ROLE: adversarial skeptic (wave 4)
TARGET FINDING: `W4-P9-counts` (grouped: `P9-selfcert-falsifiability.md:157` and `:323`)
TARGET REVISION: `8ce635807a6ca2a388255fc996c98f7c535e5843`, branch `review/2026-08-15-deep-review`

# Verdict: UPHELD_REDUCED — corrected severity **Low**

A real defect survives, but it is one narrow sentence's worth, not the "carries no information" /
"unfalsifiable token" charge the finding makes. Five of the finding's load-bearing sub-claims are
refuted by the package text or by arithmetic, including the two that do the most rhetorical work:
the convention *is* disclosed, in every release-facing artifact, and the alleged internal
contradiction in `view-probability-kernel.md` does not exist.

---

## 1. What I conceded first, because it is true

**The pre-fix mathematics was genuinely wrong, not merely loose.** I reconstructed it rather than
reading either party's prose.

The bytes at `add1a69` (`git show add1a69:.../evidence/direct-derivation.md`, sha256
`52015760e5b9ee2f07e983039d93a526a120e51753e95c650cc70303e1f3fa12`) justify the chain rule as

> "…factorizing the Radon--Nikodym derivative into its (z)-marginal density and conditional density
> and applying **monotone truncation to the nonnegative relative-entropy integrands**, gives the
> additive identity"

Reconstruction. With `rho = dQ~/dPi~` factored as `rho_A(z) * rho_c(Y|z)`, the split
`int log rho dQ~ = int log rho_A dQ~ + int log rho_c dQ~` is legitimate only because *both pieces are
in `[0,+inf]`*, and that lower bound is Jensen (equivalently the `phi_0` device), not pointwise
nonnegativity of any integrand. The raw integrand is not nonnegative: `t log t >= -1/e`, attained at
`t = 1/e`. Executed:

```
$ "C:/Python314/python.exe" -c "...":
min t log t = -0.367879 at t = 0.3679   -1/e = -0.367879
min phi_0   = 0.0
pointwise r log r at (0,1): r = 0.25  r log r = -0.346574     # a real negative integrand value
KL fine = 0.456434819   KL coarse + Delta = 0.456434819   Delta = 0.375341798
```

`phi_0(t) = t log t - t + 1` has `phi_0' = log t`, `phi_0'' = 1/t > 0`, `phi_0(1) = 0`, hence
`phi_0 >= 0` on `(0,inf)`; and `int phi_0(r) dPi = KL - 1 + 1 = KL` for probability laws, so the
generator is exactly the fix. Monotone truncation of a signed integrand does not give monotone
convergence. **The pre-fix justification clause did not prove (6.4).** The identity itself is true and
was independently confirmed by the principal reviewer (`P0-principal-reviewer-notes.md:42-64`) and
numerically above; what failed was the document's stated route through that step.

So the investigator's factual predicate is correct: a real defect existed in the load-bearing step at
the commit the reviews name, and the released reviews report Medium: 0.

**Second concession.** The two superseded review documents themselves (`1cb45d74…`, `32a9fb63…`) are
not archived in the repository. Only their findings' identifiers and closure records are.

---

## 2. Where the finding dies

### 2.1 The convention IS disclosed — in every release-facing artifact. (Kills the core of (a).)

The finding's own Fix demands: "state the counting rule explicitly ('counts are against post-fix
bytes')." It is stated, at four independent levels:

| Location | Text |
|---|---|
| `release-assembly.json` `release_gate.reason` | "all four **corrected-byte** domain reviews are current APPROVE records with no Critical, High, or Medium finding" |
| `release-assembly.json` `review_binding_rule` | "Reviews bind the **corrected pre-review payload snapshot**… **Review agreement is adjudication and cannot replace direct mathematical evidence.**" |
| `final-report.md:14` | "The **corrected-byte** reviews are current `APPROVE` records with Critical/High/Medium counts of zero" |
| `release.json:5` `checkpoint` | "Task 5 final certified release **after corrected-byte same-view domain review**" |
| `view-dynamics-scope.md:2`, `:14`, `:65` | title "**Same-view bounded** dynamics and scope **re-review**"; "The **corrected bytes close prior findings** `M-DYN-01` through `M-DYN-03`"; "**No new** Critical, High, or Medium finding arose **in the corrected bytes**." |
| `view-gauge-holonomy.md:6` | "This **bounded same-view re-review**… **supersedes the initial pre-correction review**" |
| `view-information-vfe.md:6`, `:34-46` | a whole section headed "**Bounded correction re-review**"; ":46" — "The corrected release also binds the four initial review hashes **while correctly recording that they predate the correction and cannot authorize promotion without same-view bounded re-review**." |
| `view-probability-kernel.md:4`, `:59`, `:76` | heading "**Corrected review-input identity**"; ":59" states the defect and its repair verbatim; ":76" "APPROVE for the **corrected** … domain **after same-view bounded re-review**" |
| `release-provenance.json:11` | `"snapshot_id": "corrected-pre-review-add1a69"` |

Not one of these hides the convention; every one names it. Under the finding's own framing — "a
fix-then-count convention … is not per se deceptive if disclosed" — this collapses the charge from
epistemic misconduct to a bookkeeping preference.

### 2.2 "A nonzero count is unreachable by construction" is refuted by the finding's own exhibit.

The finding cites `release-provenance.json:65-107` as proof of concealment. That block is the package
**publishing a nonzero count**: `"review_result": "WITHHOLD"`, `{"critical":0,"high":0,"medium":2}`,
with both finding IDs named. `view-dynamics-scope.md:49-68` publishes three more prior findings.
`docs/change-logs/2026-08-15.md:35-37` publishes two later rounds that found defects. Nonzero counts
are reachable, were reached, and are printed in the release package. The claim that the process makes
zero "the only reachable value" is false on the finding's own evidence.

### 2.3 The "internal inconsistency proving back-dating" does not exist. (Kills the sharpest edge.)

The finding asserts (`:179`, repeated `:348`): `view-probability-kernel.md:51` reads the *uncorrected*
sentence while `:59` says it *now* contains the generator, so "Both cannot describe the same bytes.
The review was assembled after the fix and back-dated."

Both describe the same bytes. The corrected line 286 reads:

```
$ sed -n '286p' evidence/direct-derivation.md
The relative-entropy chain rule, obtained by factorizing the Radon--Nikodym derivative into its
(z)-marginal density and conditional density and invoking the standard extended-valued chain theorem
through the nonnegative generator (\phi_0(t)=t\log t-t+1) and its monotone truncations, rather than
treating the raw (t\log t) integrand as pointwise nonnegative, gives the additive identity
```

The corrected line still contains "**and its monotone truncations**". So `:51`'s sentence — "The line
about monotone truncation is read through the canonical nonnegative generator `phi_0(t)=t log t-t+1`,
which gives the extended proof without rearranging signed or infinite integrals (`Theory/06:65-82`);
therefore it is not a closure gap" — is an accurate, non-charitable description of the *corrected*
line: that line does discuss monotone truncations, and it does invoke `phi_0`. `:51` points at the
canonical proof; `:59` records the repair. No contradiction, and no back-dating inference follows.

This is confirmed mechanically: every review binds `evidence/direct-derivation.md` =
`2aa70b07751d07712a3d9395f77817317d48d77d97c3fd5fb8cd1a3f6fda226a`, and

```
$ git show add1a69:.../evidence/direct-derivation.md | sha256sum -> 52015760…   (pre-fix)
$ git show HEAD:.../evidence/direct-derivation.md    | sha256sum -> 2aa70b07…   (post-fix)
```

The reviews bind **post-fix** bytes. They are internally consistent about post-fix bytes throughout.
The mislabeling of that snapshot as `HEAD add1a69` is a real problem, but it is the *separate*
Critical provenance finding at `P9:50`; it is not additional evidence for this one, and this finding
double-counts it.

### 2.4 "Only a hash and a closure narrative survive" is false.

`view-dynamics-scope.md:46-68` preserves `M-DYN-01`, `M-DYN-02`, `M-DYN-03` with their substance and
their corrected locations — a nonexistent claim alias on release-facing surfaces; missing scope
exclusions for canonical channel/partition selection, the downstream comparison theorem, and unique
latent DAG/physics recovery; and a design statement that needed retyping to "exact trajectory
semiconjugacy on the declared state class" with autonomous-field and well-posedness preconditions. An
outside reader can see what was found and where it was fixed. What is missing is the original review
*document*, which is narrower than the finding claims.

### 2.5 The Fix Round 1 Mediums lie outside the four views' declared scopes.

`M1-NOTATION-EVIDENCE-FRESHNESS` and `M2-ARTIFACT-METADATA-CONTRACT` are notation-freshness and
artifact-metadata defects. `view-probability-kernel.md:37` declares a claim-ID scope
(`POSTERIOR-PUSHFORWARD`, `VFE-CHAIN-EXTENDED`, …); the other three declare information/VFE,
gauge/holonomy, and dynamics/scope. None owns notation freshness or metadata contracts, and each says
so ("This is a domain-only approval"). "Two Mediums existed in bytes four expert views had just
cleared at zero" is literally true and evidentially near-empty: the four views never claimed that
territory. The change-log rounds 2 and 3 (`:37`) are a better instance — those *are* mathematical
(a stale notation-appendix sentence, a missing `Q_{A,o,X}`-a.s. qualifier) — but they too were found
when the scope widened from "that corrected central content" to whole-branch.

### 2.6 The headline number is wrong.

"0/0/0 on a **552-line** derivation":

```
$ wc -l evidence/direct-derivation.md evidence/reviews/*.md
  498 evidence/direct-derivation.md
  115 view-dynamics-scope.md   200 view-gauge-holonomy.md
  161 view-information-vfe.md   76 view-probability-kernel.md   (115+200+161+76 = 552)
```

The derivation is 498 lines. 552 is the combined length of the four reviews — the finding's own
`Location` line says so ("four files, 552 lines total") and the title transposes it onto the
derivation. Minor, but it is a factual error inside the headline of a finding about numbers that
"carry no information."

### 2.7 "Reclassify-as-exposition" is not a euphemism here.

`view-information-vfe.md:38-44` does not soften the defect; it states the mathematics correctly and
completely: "`t log t` is negative on `0<t<1`, whereas `phi_0` is nonnegative, convex, and has the
same relative-entropy expectation because the linear terms integrate to zero for probability laws."
That is precisely the reconstruction in §1 above, written by the reviewer, in the review. Given that
the identity (6.4) was stated correctly pre-fix and is canonically proved at `Theory/06:65-82`,
"removes a proof-exposition vulnerability" is a defensible classification of a wrong *justification
clause* for a true, already-proved step. A reader can disagree with the classification — the review
supplies everything needed to.

---

## 3. What actually survives, and at what severity

1. The four bound domain reviews report terminal-round counts only. The release gate's stated `reason`
   recites those counts. A terminal-round count from a fix-then-re-review loop is structurally zero and
   is therefore weak support for a release gate, even fully disclosed.
2. The pre-correction review documents are not archived, so the round-1 counts are not independently
   inspectable (their findings are).

Both are presentational/auditability defects on a correctly-fenced gate: the same file that recites the
counts also states "Review agreement is adjudication and cannot replace direct mathematical evidence,"
and the gate's load is carried by `EV-TASK3`/`EV-TASK4`. The remedy is one sentence per review
("round 1: 0/0/3 → repaired; round 2: 0/0/0 against corrected bytes") plus archiving two files.

Residue 1 is also substantially duplicative of the separate P9 finding "The ledger closes `target` as
`EVIDENCE_VERIFIED` using evidence the ledger itself types as ineligible," which is the correct place
for the "reviewer agreement carries the promotion" charge and which does not depend on any of the
refuted sub-claims above.

**Corrected severity: Low.** Not High. Nothing here is a correctness defect (the theorem holds, and
`P0-principal-reviewer-notes.md:42-64` and my §1 reconstruction agree), nothing is concealed, and the
"carries no information" framing requires the disclosure charge, which fails.

## 4. Relation to the principal reviewer's reconstructions

No contradiction. P0 verified the additive KL chain and its extended-real handling CHECK OUT
(`:42-64`), which is consistent with my §1: the theorem was always true; only the stated justification
route was invalid, and it was repaired. P0's closing note — "The certification apparatus should be read
as bookkeeping, not as evidence" — is the correct register for this finding, and it is a Low-severity
register, not a High one.

## 5. Falsifier of my own attack

Any one of these would restore the finding toward High:

- **Bytes.** If `evidence/direct-derivation.md` at `2aa70b07…` did **not** contain "monotone
  truncations" at line 286, then `view-probability-kernel.md:51` would necessarily be describing
  pre-fix text and the back-dating inference in §2.3 would stand. It does contain it (`sed -n '286p'`,
  quoted above).
- **Binding.** If the reviews' bound derivation hash were `52015760…` (the `add1a69` bytes) rather
  than `2aa70b07…`, `:51` and `:59` would describe different bytes and the contradiction would be real.
- **Disclosure.** If any release-facing artifact presented the 0/0/0 as an unqualified measurement of
  the proof — i.e. without "corrected-byte" / "same-view re-review" / "cannot replace direct
  mathematical evidence" — the non-disclosure charge would revive. I checked `release.json`,
  `release-assembly.json`, `final-report.md`, and all four reviews; the qualifier is present in every
  one.
- **Scope.** If `M1-NOTATION-EVIDENCE-FRESHNESS` or `M2-ARTIFACT-METADATA-CONTRACT` fell inside the
  declared claim scope of any of the four views, §2.5 collapses and "the process misses defects in its
  own territory" becomes directly evidenced.

STATUS: COMPLETE
