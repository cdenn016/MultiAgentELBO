STATUS: COMPLETE
ROLE: adversarial skeptic (wave 2)
TARGET FINDING: `P1-High-3-null-slice` (severity as filed: High)
REVISION UNDER REVIEW: `8ce635807a6ca2a388255fc996c98f7c535e5843`
BRANCH: `review/2026-08-15-deep-review`

# Verdict: UPHELD_REDUCED — corrected severity **Low**

The investigator's mathematics is correct and I reproduced it independently: at a `\nu_X`-null
admitted observation the pointwise quantities `\mathcal F_I`, `\mathcal F_A`, and `\Delta_A` depend
on the declared regular-conditional version and are therefore not functionals of
`(\mathbb P_I(\cdot\mid X),\lambda_X,o,\mathbb Q_{I,o,X})`. I could not break the counterexample on
any frozen premise, including the strongest available reading of "admitted regular observation".

What does not survive is the finding's headline and its severity. The finding is filed as an
undisclosed weakness — "only the evidence term is treated", "the KL term ... receives only a fiat
declaration", "§9's long list of non-claims does not include this". The package discloses exactly
this, by name, against exactly the KL/VFE claim id, in four places at the reviewed revision, and the
repository's own probability chapter states the same phenomenon with its own two-version example and
prescribes the declared-version route the derivation then follows. The finding's own **Fix** text is
a near-paraphrase of language already shipped in `evidence/adversarial-attacks.md:36` and
`approach-registry.json:162,177`. That is the wave-1 death condition "the hypothesis they say is
missing is stated elsewhere in the package".

What remains is real but small: three *limitation* lists — `direct-derivation.md:498` (§9 "exact
limitations"), `construction-or-strongest-theorem.md:118`, and `final-report.md:40` — omit a
limitation the same package records as an open gap elsewhere. That is an internal-consistency defect
in a document that advertises itself as the exact-limitations section. It is not a proof gap, not a
correctness defect, and not an overclaim in any displayed equation (the investigator concedes the
last point themselves).

---

## 1. I rebuilt the counterexample. It is valid.

Setup as filed: `\mathsf O=[0,1]`, `\lambda_X=\mathrm{Leb}`, `\mathsf Y_I=\{0,1\}`,
`\mathbb P_I(do,dY\mid X)=\mathrm{Leb}(do)\otimes\mathrm{Ber}(1/2)`, so `\nu_X=\mathrm{Leb}` and
`p_X\equiv1`.

*Both versions are admissible kernels.* `\mathsf Y_I` is finite, so kernel measurability is
measurability of the four maps `o\mapsto\boldsymbol\Pi_{I,o,X}(D)`, `D\subseteq\{0,1\}`. Version B
modifies each of these on the Borel set `\{1/2\}`, so each stays Borel. Normalization is immediate.
Identity (1.1) holds for B because for every Borel `E` and every `D`,

  `\int_E\boldsymbol\Pi^{B}(D)\,do=\int_{E\setminus\{1/2\}}\boldsymbol\Pi^{A}(D)\,do=\int_E\boldsymbol\Pi^{A}(D)\,do`,

since `\mathrm{Leb}(\{1/2\})=0`, and A satisfies (1.1) by Fubini. So both are selected measurable
regular-conditional kernels for the same `\mathbb P_I`, exactly as (1.1) at `:39–:43` requires.

*Premise sweep — I checked every frozen premise and found no exclusion.*

| Premise | Source | Does it exclude `o=1/2`? |
|---|---|---|
| `0<p_X(o)<\infty` | `direct-derivation.md:53`; `claim-ledger.json:24` | No. `p_X(1/2)=1`. |
| "admitted regular observation with finite unchanged evidence" | `problem-contract.json:25,30,57` | No. "regular" is nowhere given a definition that excludes `\nu_X`-null points; in context it modifies *regular conditional*. See §2 for the strongest possible reading and why it still fails to exclude. |
| `\mathbb Q_{I,o,X}\ll\boldsymbol\Pi_{I,o,X}` (1.2) | `direct-derivation.md:55–62` | No. `\delta_0\ll\mathrm{Ber}(1/2)` and `\delta_0\ll\delta_0`. |
| Finiteness of displayed KL terms | `problem-contract.json:41` | No. Both values are finite (`\log 2` and `0`). |
| `C_A` normalized measurable, recognition/observation independent | `direct-derivation.md:77–84` | No. `C_A=\mathrm{id}` needs only `\mathsf B_A=\mathsf Y_I` with `\mathsf M_A,\boldsymbol\Xi_A,\mathsf H_A` singletons — all nonempty standard Borel. |
| `ev_A` normalized measurable + a.s. evaluation compatibility | `problem-contract.json:59` | No. With `\mathsf M_A\times\boldsymbol\Xi_A` a one-point space, take `ev_A` to be the induced conditional; the seam holds by construction. |

*Executed check.* Script at
`C:/Users/chris and christine/Desktop/MultiAgentELBO/docs/reviews/2026-08-15-deep-review/findings/V-P1-High-3-null-slice-check.py`,
run with the CPU interpreter (no torch involved; all spaces finite, so every KL is an exact finite
sum). Output:

```
=== Part 1: investigator's exhibited example, Y_I = {0,1} ===
  F_I under Version A = 0.6931471805599453  (log 2 = 0.6931471805599453 )
  F_I under Version B = 0.0
  Q << Pi^A ? True
  Q << Pi^B ? True
```

The arithmetic as filed is correct.

## 2. The one premise that could have killed it, and why it does not

`problem-contract.json:25,30,57` says "admitted **regular** observation". If that imports the
repository's defined regular-observation set `\mathsf O_{\theta,X}^{\mathrm{reg}}`
(`Theory/03_probability.tex:190–197`), the counterexample would have to place `o=1/2` inside it. It
does. That set is only required to be *marginal-full*, `P^{O}_{\theta,X}(\mathsf O^{\mathrm{reg}})=1`
(`:192`), so in my construction one may take `\mathsf O^{\mathrm{reg}}=[0,1]` outright — `p_X\equiv1`
is already an everywhere-defined representative and both A and B are selected regular-conditional
versions valid on all of `[0,1]`. The chapter says so in as many words at `:413`: membership in
`\mathsf O^{\mathrm{reg}}` "makes the statement invariant under changes of density version **outside
a marginal-full set**" — a single-point change *inside* the full set is untouched by it. So the
strongest reading of the contract's "regular" does not exclude the witness. The finding's stated
falsifier ("a hypothesis in the package that `\nu_X(\{o\})>0`, or a canonicity requirement on the
version") does not exist; I looked for it and agree it is absent.

## 3. Where the finding dies: the disclosure it says is missing is shipped

All four quoted at the reviewed revision via `git show 8ce6358:<path>`.

**(a) `evidence/adversarial-attacks.md:30–36` — the attack is registered verbatim, against the VFE
claim id.**

> `## A4. Null posterior versions`
> `Attack: A regular conditional is unique only almost surely, so evaluating an arbitrary version at a selected null observation can make the pointwise theorem version dependent.`
> `Response: ... It does not claim canonical null-slice values or version independence.`
> `Disposition: REJECTED for POSTERIOR-PUSHFORWARD and VFE-CHAIN-EXTENDED as version-qualified claims. Any canonical-null-version theorem remains outside scope.`

`VFE-CHAIN-EXTENDED` is the KL/VFE claim. `adversarial-report.json:47–56`
(`ATTACK-NULL-POSTERIOR-VERSION`) binds the same two claim ids and records "Canonical null-slice
values are not claimed." This is the direct refutation of the finding's title — the KL term is not
untreated, and the treatment is not silent.

**(b) `approach-registry.json:162,177` — recorded as an obstruction and an open gap.**

> `"invariant_or_obstruction": "Regular conditionals are version-defined on null observations; global disintegration does not make a null-slice value canonical."`
> `"open_gaps": ["Canonical null-slice versions and cross-X compatibility are not proved."]`

**(c) `direct-derivation.md:45` covers the KL term, not only the evidence term.** The finding's title
asserts "only the evidence term is treated". The sentence reads: "An admitted observation `o` is a
point at which this selected version, **its evidence representative, and every later slice-wise
expression** are declared to be used." `\operatorname{KL}(\mathbb Q_{I,o,X}\Vert\boldsymbol\Pi_{I,o,X})`
is a later slice-wise expression. The same qualification recurs at `:141` ("including declared
exceptional-point values inherited from the fine selected version"), `:210`, and `:424`
("almost-sure uniqueness of regular conditionals does not choose covariant null-slice values
automatically"); `evidence/independent-reconstruction.md:30` and
`evidence/reviews/view-information-vfe.md:119` ("Exceptional values remain version-qualified") repeat
it.

**(d) The repository already states the phenomenon, with its own two-version example.**
`Theory/03_probability.tex:214`, `\status{HYPOTHESIS}`, pre-dating this package:

> "are versions of the same joint density because they differ only on the Lebesgue-null slice
> `\{0\}\times\R`. Both displayed evidence representatives equal `\phi(0)` at `o=0`, but their
> density-ratio conditionals there are `\phi(y)dy` and `\psi(y)dy`. The joint measure therefore
> determines neither pointwise posterior at that exceptional observation. ... An everywhere pointwise
> statement instead requires a particular jointly measurable density, evidence representative, and
> regular-conditional version to be declared as part of the model data; its exceptional-point values
> then belong to that declaration and are not determined by the joint measure alone."

That is the investigator's finding, including the construction (two versions agreeing off a null
slice, identical evidence representative, different conditionals at the exceptional point) and the
conclusion the finding asks to have added. `Theory/05_elbo.tex:8` applies the same qualification to
"every posterior and ELBO statement" in the ELBO chapter. `direct-derivation.md:45` is precisely the
"declared as part of the model data" route that `03_probability.tex:214` prescribes. The 8/15 package
is following the house convention, not evading it.

**(e) Nothing in the package quantifies the pointwise VFE over the model rather than over the
selection.** I checked the two ledger claims the finding implicates and the contract:

- `POSTERIOR-PUSHFORWARD`: `"For every selected fine observation-indexed posterior kernel and common channel ..."`
- `VFE-CHAIN-EXTENDED`: `"For every pair satisfying ASM-RECOGNITION-AC, ASM-COMMON-CHANNEL, and ASM-EVIDENCE-REPRESENTATIVE."`
- `problem-contract.json:25`: `"... every selected posterior Pi_{I,o,X} derived from that law ..."`
- `problem-contract.json:54`: `"Equality is equality of the declared normalized full laws or kernels up to their stated almost-sure versions."`

Every relevant statement is universally quantified over the selection, which is exactly the
version-relative reading. The finding's charge that "the theorem is a true statement about the
declared objects; it is not a statement about the model at `o`" is therefore not an indictment — it
is the package's own stated quantifier structure, restated.

## 4. Two defects in the finding itself

**(i) The range `[0,\infty]` violates a frozen premise at its upper endpoint.** The finding says
"Replacing `\delta_0` at `o=1/2` by `\mathrm{Ber}(\varepsilon)` makes `\mathcal F_I` any value in
`[0,\infty]`." With `\mathbb Q=\delta_0` held fixed,
`\operatorname{KL}(\delta_0\Vert\mathrm{Ber}(\varepsilon))=-\log(1-\varepsilon)`, which is finite for
every `\varepsilon<1`; reaching `+\infty` requires `\boldsymbol\Pi(\{0\})=0`, which breaks (1.2)
`\mathbb Q\ll\boldsymbol\Pi`. On a finite `\mathsf Y_I`, absolute continuity forces finiteness, so
**no** admissible version attains `+\infty` here. Executed:

```
  eps=0.999999   KL(delta_0||Ber(eps)) = 13.815510557935518    Q<<Pi: True
  eps=1.0        KL = inf  Q<<Pi: False   <-- violates premise (1.2) Q << Pi
```

The correct statement is: the attainable set is `[0,\infty)`, unbounded above but with the endpoint
excluded by a stated premise.

**(ii) The exhibited witness does not establish the `\Delta_A` half of the claim.** The finding
asserts that "`\mathcal F_I(o,X)`, `\mathcal F_A(o,X)` and `\Delta_A(o,X)` ... can be given
essentially arbitrary values", but its own construction takes `C_A=\mathrm{id}`, under which
`\Delta_A=0` for *both* versions — as the finding itself notes. So the claim about the defect is
asserted, not exhibited. It is nevertheless true, and I supply the missing witness so the record is
complete: take `\mathsf Y_I=\{0,1\}^2`, `\mathsf Z_A=\{0,1\}`, `C_A` the (deterministic) projection
onto the first coordinate, `\mathbb Q_{I,1/2,X}=` uniform on the diagonal; Version A at `o=1/2` is
the uniform product law, Version B is uniform on the diagonal. Both agree off `\{1/2\}` with the
uniform product law, so both satisfy (1.1); both dominate `\mathbb Q`. Executed:

```
=== Part 3: is the DEFECT Delta_A itself version dependent? ===
  Version A (product)   KL_fine=0.693147 KL_coarse=0.000000 Delta_A=0.693147  Q<<Pi:True
  Version B (diagonal)  KL_fine=0.000000 KL_coarse=0.000000 Delta_A=0.000000  Q<<Pi:True
```

So `\Delta_A` is genuinely version dependent — `\log 2` versus `0` — and by (6.8) so is the
zero-defect verdict itself. This *strengthens* the mathematics of the finding while showing the filed
evidence did not reach it.

## 5. On line `:53`, "makes a pointwise evidence term meaningful"

The finding says this "does no such thing in any sense stronger than 'we picked one'". That
undersells what the declaration buys, and the shortfall matters for severity. Two things follow from
it that are not "we picked one":

1. Without a fixed representative `-\log p_X(o)` is not defined at a point at all, only
   `\lambda_X`-a.e.; with one it is defined. That is the ordinary sense of "meaningful", and it is
   the sense `Theory/03_probability.tex:214` uses for "an everywhere pointwise statement".
2. Because `:53` requires "the same representative is used at both scales", `-\log p_X(o)` cancels
   in (6.6)–(6.7): `\mathcal F_I-\mathcal F_A=\Delta_A` is *independent of the density-representative
   choice*. The evidence-representative declaration is therefore doing real, checkable work on the
   theorem's actual payload, not decorating it.

Residual looseness: "meaningful" could be misread as "canonical" by a reader who skips the sentence
immediately above it. Softening it is fair polish. It is not a defect that changes what is proved.

## 6. Relation to the principal reviewer's reconstructions

No contradiction. `P0-principal-reviewer-notes.md` independently re-derived the pushed-posterior
version identity, parent absolute continuity, the additive KL chain, and the recovery/DPI-equality
theorem, and marked all four CHECKS OUT. None of those reconstructions is touched by version choice
at a null slice: each is an identity that holds *for whichever selection is declared*, which is why
P0's derivations go through with `\boldsymbol\Pi_{I,o,X}` treated as a given kernel. P0's own summary
— "the mathematics is correct", "the fencing is unusually careful and honest", and the live issue is
attribution and novelty rather than correctness — is consistent with the reduction I am recording
here. The wave-1 finding, as filed at High, would have been a correctness/fencing defect; the
evidence says the fencing is present and the defect is bookkeeping.

## 7. Corrected finding

**Severity: Low. Category: internal-consistency / documentation, not correctness.**

> Three limitation lists — `evidence/direct-derivation.md:498` (§9, titled "Strongest Task-3 theorem
> and exact limitations"), `construction-or-strongest-theorem.md:118`, and `final-report.md:40` —
> omit the null-slice version dependence of `\mathcal F_I`, `\mathcal F_A`, and `\Delta_A`, although
> the package records it as an obstruction and an open gap at `approach-registry.json:162,177`,
> disposes of it as a registered attack at `evidence/adversarial-attacks.md:30–36` /
> `adversarial-report.json:47–56`, and declares the governing convention at
> `direct-derivation.md:45`. Add one clause to the three lists so that a reader of the limitation
> sections alone learns what a reader of the attack register already knows. Optionally soften `:53`
> from "makes a pointwise evidence term meaningful" to "fixes one finite representative, shared
> across scales, so that the pointwise evidence term is defined and cancels in (6.7); it does not
> make the value canonical."

`problem-contract.json` needs no change: its quantifier at `:25` ("every selected posterior") and its
equivalence clause at `:54` ("up to their stated almost-sure versions") already carry the
version-relative reading.

## 8. Falsifier of my own attack

My verdict is wrong — and the finding returns to High — if any of the following is exhibited:

1. A load-bearing statement in the package that asserts `\mathcal F_I`, `\mathcal F_A`, or
   `\Delta_A` at the admitted `o` is determined by `(\mathbb P_I(\cdot\mid X),\lambda_X,o,\mathbb Q_{I,o,X})`,
   i.e. a claim or displayed conclusion quantified over the *model* rather than over the *selection*.
   I checked `problem-contract.json:22–61`, the `POSTERIOR-PUSHFORWARD` and `VFE-CHAIN-EXTENDED`
   ledger entries, `construction-or-strongest-theorem.md`, and `final-report.md`, and found the
   opposite in every case; a passage I missed would overturn this.
2. Evidence that `evidence/adversarial-attacks.md:30–36`, `adversarial-report.json`'s
   `ATTACK-NULL-POSTERIOR-VERSION`, or `Theory/03_probability.tex:214` post-dates the reviewed
   revision. I verified all three by `git show 8ce6358:<path>`; if that binding is wrong, the
   disclosure argument collapses.
3. A downstream artifact in this repository that *consumes* the pointwise `\Delta_A` or the
   zero-defect criterion (6.8) as if it were selection-independent — for instance a comparison,
   coarse-graining, or meta-agent result that quantifies over models and invokes `\Delta_A=0`. The
   version dependence is harmless where every statement is per-selection; it becomes a genuine
   correctness defect the moment something quantifies over the model. I did not audit the downstream
   consumers, and that is the one check that could still move this back up.
