# Wave 2, Audit 4 — Deep read of `05d_relational_inference.tex` and `07b_agent_network_rg.tex`

Date: 2026-08-11. Auditor scope: the two largest under-examined chapters, plus a bounded pass over
`09_coarsegraining.tex` and `10_renormalization.tex`.
Execution policy: **CPU only. No GPU or CUDA job was started.** All numerical work was done in an
isolated Linux sandbox with `sympy 1.14.0` / `numpy 2.2.6` / `mpmath 1.3.0`, exact rationals where
possible.

Both chapters were read in full (`05d`: lines 1–1624; `07b`: lines 1–2828 across seven passes).
Sixteen quantitative claims were re-derived rather than accepted; **every one of them reproduced
exactly.** The findings below are structural, not arithmetic.

Wave-1 findings RG-1, RG-4, RG-5, RG-6, RG-8, G8, F6, T-07 are not restated. They are extended,
sharpened, or (in one case, RG-8) corrected.

---

## 0. Headline

| | `05d` | `07b` |
|---|---|---|
| Lines | 1,624 | 2,828 (17% of corpus) |
| Formal results | 29 | 35 |
| Results with a **mathematical** consumer outside the chapter | **6 (20.7%)** | **5 (14.3%)** |
| Results whose only external reference is the ledger appendix | 8 | 4 |
| Results referenced **nowhere in the corpus** | 15 | 26 |
| Results referenced nowhere at all, *not even inside their own chapter* | 4 | **12** |
| Lines belonging to a section with any external consumer | ~700 (43%) | **752 (26.6%)** |
| `\status{ESTABLISHED}` | 48 | 81 |
| `\status{HYPOTHESIS}` | 11 | **0** |
| `\status{OPEN}` / `NOT-CLAIMED` | 1 / 4 | 1 / 1 |
| Spacing-macro violations (`\;` `\,` `\!`) | 1 | 18 |
| Banned Claude-isms | 0 | 0 |
| Undischarged hand-waves | 1 | 4 |
| Citations | 3 | 5 |

Two sentences of verdict.

**`05d` is the better chapter in the corpus on epistemic discipline and one of the weakest on
integration**: its `L^1`/domination standard is maintained, its witnesses are all correct, its OPEN
is honestly placed and honored — but from line 521 onward the object it studies is *an arbitrary
`C^2` function on `\mathbb R^N` with a constant Gram metric*, and the words "variational free
energy" do no mathematical work in 1,100 of its 1,624 lines.

**`07b` is a competent 2,800-line monograph on Markov-kernel coarse-graining wearing an agent-network
costume**: `\Fenergy` appears on 2 lines, "agent" on 19, the entire gauge/graph sector occupies a
130-line island whose objects are used nowhere else in the chapter or the corpus, and the chapter
carries **zero HYPOTHESIS tags** while its flagship theorem consumes sixteen supplied hypotheses.

---

# PART I — `Theory/05d_relational_inference.tex`

## 1. Structural map

The chapter proves, in order:

**§1 Fixed-base kinematics (22–105).** `def:hist-curve-types` (42) partitions total-space velocities
into stationary / vertical / horizontal / mixed, with the correct warning (63–68) that the
*interval-level* labels are not exhaustive. `prop:hist-horizontal-connection-dependence` (93) gives a
two-line trivial-line-bundle witness that horizontality is connection-relative.

**§2 Curves of sections (107–217).** `hyp:hist-regular-section-space` (109) declares the section
space. `eq:hist-pointwise-history-verticality` (133) is the chapter's genuine kinematic content: a
curve of *sections* has vertical evaluation velocity at every fixed context. `def:hist-oriented-history`
(157) defines `\mathscr H_i` as an oriented reparameterization class.

**§3 VFE selection of an orbit (219–571).** `hyp:hist-regular-metric-domain` (222) is the standing
regularity. `def:hist-finite-configuration-tier` (235) + `thm:hist-finite-tier-regularity` (275)
exhibit a nonempty model: `\mathcal Q_\ell \cong \mathbb R^N`, metric the constant Gram matrix
`\Phi`. `hyp:hist-exact-vfe-lift` (372) is the joint-law lift. `prop:hist-scalar-mobility-orbit` (522)
and `prop:hist-semidefinite-gradient-obstruction` (560) are two-line counterexample propositions.

**§4 Fisher duration (573–672).** `def:hist-fisher-clock` (576), `thm:hist-fisher-clock-invariance`
(594), `prop:hist-realized-length-versus-distance` (643).

**§5 Clock tiers (674–769).** Pointwise / finite-design / continuum / gauge-quotient speeds, each
with its declared prerequisites and its failure witness.

**§6 Global clock obstruction (771–842).** `thm:hist-global-clock-exactness` (787) plus the exact
obstruction 2-form `eq:hist-normalized-form-curvature` (819).

**§7 Record clocks (844–960).** `thm:hist-record-clock-contraction` (860) — score projection and the
conditional-variance defect.

**§8 Coarse configuration map (962–1149).** `hyp:hist-joint-convexity` (1018),
`thm:hist-averaging-defect` (1027) with its three-term decomposition, `prop:hist-coarse-map-smoothness`
(1097).

**§9 Independently recomputed flows (1151–1435).** `def:hist-oriented-semiconjugacy` (1160),
`lem:hist-semiconjugacy-factor` (1172), `thm:hist-oriented-semiconjugacy` (1205),
`prop:hist-noncollapse` (1280), `thm:hist-duration-relation` (1295), `thm:hist-duration-criterion`
(1336), `thm:hist-pointwise-contraction-lift` (1397).

**§10 Sufficient conditions (1437–1553).** `hyp:hist-functional-compatibility` (1454),
`prop:hist-natural-gradient-sufficiency` (1461), then `\status{OPEN}` at 1553.

**§11 RG depth is not time (1555–1624).** `prop:hist-coordinate-independence` (1586) and two
`NOT-CLAIMED` closures.

### 1.1 Dependency graph

```
hyp:hist-regular-section-space ──► def:hist-oriented-history ──► [05b, 09]      EXTERNAL
hyp:hist-regular-metric-domain ──► def:hist-finite-configuration-tier
                                      └─► thm:hist-finite-tier-regularity ──► hyp:hist-standing-configuration-tier
                                                                                 (declares the whole chapter's tier)
def:hist-fisher-clock ──► thm:hist-fisher-clock-invariance ──► [05b, 09]        EXTERNAL
                       └─► prop:hist-realized-length-versus-distance            TERMINAL
                       └─► thm:hist-global-clock-exactness ──► (05d:1611 only)  TERMINAL (ledger-only)
                       └─► thm:hist-record-clock-contraction ──► [06_gen_cg]    EXTERNAL
hyp:hist-joint-convexity ──► thm:hist-averaging-defect ──► prop:hist-coarse-map-smoothness
                                                        └─► (05d:1365 only)     TERMINAL
def:hist-oriented-semiconjugacy ──► lem:hist-semiconjugacy-factor ──► thm:hist-oriented-semiconjugacy
                                          └─► prop:hist-noncollapse             TERMINAL (ledger-only)
                                          └─► thm:hist-duration-relation        TERMINAL (ledger-only)
                                          └─► thm:hist-duration-criterion       TERMINAL (ledger-only)
thm:hist-pointwise-contraction-lift ──► [08_infogeometry]                       EXTERNAL
hyp:hist-functional-compatibility ──► prop:hist-natural-gradient-sufficiency ──► [05c]  EXTERNAL
hyp:hist-exact-vfe-lift ──► (05d:518 only)                                      TERMINAL (ledger-only)
prop:hist-coordinate-independence                                               TERMINAL (0 refs)
def:hist-curve-types, prop:hist-horizontal-connection-dependence,
prop:hist-scalar-mobility-orbit, prop:hist-semidefinite-gradient-obstruction     0 external refs
```

Load-bearing outside the chapter: **6 of 29 (20.7%)**, and the six are consumed by five files
(`05b`, `05c`, `06_general_coarsegraining`, `08`, `09`), one reference each.

### 1.2 FINDING 05D-S1 — HIGH — the VFE is decorative in 68% of the chapter

`hyp:hist-exact-vfe-lift` is referenced **exactly once in the entire corpus outside the ledger**:
at `05d:518`, inside a `\status{DEFINITION}` paragraph that says

> "When `\Fenergy_i` is the pullback specified in `\Cref{hyp:hist-exact-vfe-lift}`, this is an exact
> VFE history; otherwise it is a history for a generic declared objective and no exact-VFE
> identification is asserted." (`05d:517–520`)

That sentence is exactly correct, and it is the right way to honor the ledger's `Joint-law lift
(open)` entry (`appendix_claim_ledger.tex:50–57`). **The conditionality discipline is clean: no
result in `05d` depends on `hyp:hist-exact-vfe-lift` without saying so, because none depends on it
at all.**

The consequence the chapter does not draw is the finding. The only standing hypothesis on the
objective anywhere in `05d` is "`\Fenergy_i:\mathcal Q_i\to\R` is `C^2`" (`05d:227`, restated
`05d:1442`). The exhibited configuration tier is `\mathbb R^N` with the *constant* Gram form `\Phi`
(`05d:282`, `eq:hist-configuration-gram`). Therefore every result from `05d:521` to `05d:1624` —
1,104 lines, 68% of the chapter, including all seven theorems of §§4–10 — is a statement about
**gradient-flow arc-length calculus for an arbitrary `C^2` function on a Euclidean space**. Delete
the word "VFE" and every hypothesis, proof, and witness is unchanged.

This is not an error and the chapter never claims otherwise. It is a misallocation signal: the
chapter's title promises "Relational Inference Histories" and delivers Riemannian gradient-flow
bookkeeping, correct and careful, with the inference content confined to one 76-line hypothesis
(372–448) that nothing consumes.

**Fix (cheap, high value):** discharge `hyp:hist-exact-vfe-lift` on the exhibited tier of
`def:hist-finite-configuration-tier`, where `\mathcal Q_\ell` is `\mathbb R^N` and the fiber is
`\{\mathcal N(m,\Sigma_0)\}`. On that tier a lift `\iota_i` exists explicitly (take the block
recognition law Gaussian with the displayed mean field and a declared fixed cross-block covariance);
the commuting condition `\pi^{\mathrm{conf}}\circ\iota_i=\mathrm{id}` is then a linear-algebra check,
and `eq:hist-exact-fisher-lift` becomes the block-orthogonality condition already characterized
exactly at `eq:hist-joint-versus-product` (`05d:461`). This is perhaps two pages and it converts the
chapter's central hypothesis into an inhabited one, exactly as
`thm:hist-finite-tier-regularity` already does for `hyp:hist-regular-metric-domain`.

### 1.3 FINDING 05D-S2 — LOW — stale duplicate label

```
05d:1205  \theoremheading{Oriented semiconjugacy and maximal intervals}{thm:hist-oriented-semiconjugacy}
05d:1206  \label{prop:hist-oriented-semiconjugacy}%
```

Two labels on one theorem. `06_general_coarsegraining.tex:240` cites the `prop:` alias;
`appendix_claim_ledger.tex:150` cites the `thm:` name. SPEC §4 mandates semantic label prefixes, and
a `prop:` label on a Theorem environment misdescribes it. Any label-reference census (including this
one) double-counts the result. Delete line 1206 and repoint `06:240`.

## 2. Status-tag audit — `05d`

48 ESTABLISHED-governing paragraphs. Classified by nearest available support:

| Support | Count |
|---|---|
| Followed by `\paragraph{Proof.}` | 17 |
| Contains a `\cite` | 2 |
| Contains only a `\Cref`/`\eqref` pointer | 20 |
| **No proof, no citation, no pointer** | **9** |

### Triage of the 9 unsupported ESTABLISHED claims

| # | Location | Claim | Triage |
|---|---|---|---|
| 1 | `05d:117–137` | `T\varpi_i(\partial_\lambda\widehat\Sigma_i)=0` | **(i)** — immediate from `\varpi_i\circ\widehat\Sigma_i(\lambda,c)=c`, constant in `\lambda`. The display *is* the argument. One connecting clause. |
| 2 | `05d:208–217` | "A smooth section is injective … and it is an embedding **under the usual smooth-bundle hypotheses**" | **(ii)** and a SPEC §2.2 violation. Injectivity is one line. "The usual smooth-bundle hypotheses" is an unnamed condition inside an ESTABLISHED tag — the exact pattern §2.2 forbids. Name it (`\varpi_i` a submersion with locally trivial fibers; section continuous and proper onto its image) or convert to OPEN. **This is the single worst prose defect in `05d`.** |
| 3 | `05d:331–353` | The `L^2`/Sobolev tier dichotomy, ending "**No third option is available**" | **(iii) for the exhaustiveness clause only.** The two exhibited tiers and the `H^1` witness are correct (re-derived: `Q=\sum k^{-2}\sin k\theta` has finite `H^1` norm while `-Q''=\sum\sin k\theta` has infinite `L^2` norm ✓). But "no third option is available" is an unproved exhaustiveness assertion — weighted `L^2`, reflexive Banach tiers with a declared duality, and Riesz-representable subdomains are all third options. Weaken to "the two options this manuscript uses are", or prove it. |
| 4 | `05d:450–484` | Joint-vs-product Fisher criterion, Loewner non-ordering, lift non-uniqueness | **(i)** — fully self-contained. Verified: the identity at `eq:hist-joint-versus-product` reproduces to `2.8e-14` on 5 random 200-dim draws (seed 0); `\det(\Lambda-(1-\rho^2)I)=\rho^2(\rho^2-1)`, `q(1,1)=2\rho(1+\rho)`, `q(1,-1)=2\rho(\rho-1)` all exact in sympy. |
| 5 | `05d:690–705` | Finite-design speed is not positive definite; bump-variation witness | **(i)** — correct and self-evident from the definition. |
| 6 | `05d:1011–1016` | `f`-basic sections descend under the averaging map | **(i)** — normalization of the disintegration, one line. |
| 7 | `05d:1154–1158` | Pointwise contraction does not imply orbit mapping | **(i)** — true; the two witnesses are supplied 200 lines later at `05d:1369–1395`. Add a forward `\Cref`. |
| 8 | `05d:1256–1278` | arsinh / arctan / orientation witnesses | **(i)** — all three verified symbolically: `\mathsf R=\mathrm{arsinh}\Rightarrow a_\ell=(1+x^2)^{-1/2}`, `\inf a_\ell=0`, `\sigma_0=\mathrm{arsinh}` onto `\mathbb R`; `\mathsf R=\arctan\Rightarrow a_\ell=(1+x^2)^{-1}`, `\Sigma_0=(-\pi/2,\pi/2)`; the orientation witness forces `a_\ell\equiv-1`. |
| 9 | `05d:1328–1334` | `a_\ell` is a parameter rate, not a duration | **(i)** — typing remark; arguably should be DEFINITION not ESTABLISHED. |

**Triage totals for `05d`: (i) obviously true, needs a line — 7; (ii) true but needs real work — 1;
(iii) doubtful as stated — 1 (the exhaustiveness clause at 331–353).**

Tag-type observations:
- Item 9 and `05d:1200–1203` are typing conventions tagged ESTABLISHED where DEFINITION is the
  correct tag. Two instances, LOW.
- The rest of the tag discipline is genuinely exemplary. Every hypothesis is a `HYPOTHESIS`, every
  refusal is a `NOT-CLAIMED`, the one open route is `OPEN` (`05d:1553`) and states exactly what would
  close it.

## 3. Timeless histories — the four specific questions

### 3.1 Is "history" a well-defined object?

**Yes, and this is the chapter's strongest piece of type discipline.** The construction is:

- A `C^1` representative `Q_i:I\to\mathfrak S_i` into a **declared regular section space**
  (`hyp:hist-regular-section-space`, `05d:109`), which explicitly refuses to infer a manifold
  structure from "all smooth sections": *"No such structure follows merely from writing down all
  smooth sections."* (`05d:114–115`).
- Regularity: `C^1` in the representative; the ambient space is either a finite-dimensional
  submanifold or a specified smooth locally convex manifold with differentiable evaluation.
- The history proper `\mathscr H_i` is the quotient by orientation-preserving `C^1`
  reparameterization (`eq:hist-oriented-reparameterization-equivalence`, `05d:166`), with
  self-intersections handled: *"With self-intersections, `\mathscr H_i` retains traversal order and
  multiplicity and is not merely the set-theoretic image."* (`05d:179–180`).
- The adjoint evaluation has the SPEC-mandated type
  `\Sigma_i:\mathscr H_i\times\mathcal C_i\to\mathcal E_b\times_{\mathcal C}\mathcal E_m` with
  `\varpi\circ\Sigma_i(r,c)=c` (`05d:171–176`) — matching SPEC §3 verbatim.
- The type prohibition is stated and enforced: *"Applying a verticality predicate directly to a base
  curve or to a configuration curve is a type error."* (`05d:79–80`).

The one gap: `\mathfrak S_i` is declared, never constructed at the general tier; the only inhabited
instance is `def:hist-finite-configuration-tier` (`\mathbb R^N`). That is stated
(`hyp:hist-standing-configuration-tier`, `05d:355–370`) and the model class is proved nonempty
(`05d:366–367`). No defect.

### 3.2 Is the Fisher arc length reparameterization-invariant? — verified by explicit computation

`thm:hist-fisher-clock-invariance` (`05d:594`). The proof (623–634) is: `\dot{\widetilde Q}=(\dot
Q\circ\phi)\phi'`, hence `\widetilde\nu_F=(\nu_F\circ\phi)\phi'` **because `\phi'>0`**, then
substitute `u=\phi(\widetilde\lambda)`.

**Correct, and the `\phi'>0` step is load-bearing and correctly flagged.** Explicitly:
`\widetilde\nu_F(\widetilde\lambda)=\sqrt{\mathsf G(\dot Q(\phi)\phi',\dot Q(\phi)\phi')}=|\phi'|\,\nu_F(\phi)`.
Orientation preservation removes the absolute value; without it the *length* is still invariant but
the *cumulative clock* `\tau` reverses sign, so the theorem's `\tau`-statement genuinely needs the
orientation hypothesis and the chapter has it. Change of variables in
`\int_{\widetilde\lambda_0}^{\widetilde\lambda}(\nu_F\circ\phi)\phi'\,d\widetilde\lambda
=\int_{\lambda_0}^{\phi(\widetilde\lambda)}\nu_F\,du` requires `\phi\in C^1` and `\nu_F` continuous —
both supplied. **No defect. The invariance claim is exactly right and exactly as strong as stated.**

The auxiliary-parameter disclaimer at `05d:590–591` ("The auxiliary parameter `\lambda` is not part
of the resulting arc length") matches SPEC §3's "Any local parameter used to calculate a path
integral is auxiliary and must disappear from the final arc length." Honored.

Corroborating computation: the "finite length, infinite parameter" example
`\int_0^\infty e^{-t}dt=1` (`eq:hist-finite-length-infinite-parameter`, `05d:665–670`) is correct and
is correctly tagged `NOT-CLAIMED` rather than ESTABLISHED, because its content is a refusal.

### 3.3 Does `thm:hist-global-clock-exactness` deliver a clock?

**No. It delivers a necessary and sufficient condition that the chapter's one worked instance
violates — and the chapter says so.**

The statement (`05d:788–804`) reads: *"There is a smooth scalar `T:U\to\R` satisfying `dT=\alpha_F`
if and only if `\alpha_F` is exact."* That biconditional is the **definition of exactness** — a
tautology. The content is the second sentence, "Equivalently, it must be closed and have vanishing
period around every piecewise `C^1` closed curve", which is the standard line-integral criterion.

Two observations, both minor and both worth fixing:

- **FINDING 05D-C1 — LOW — the criterion is over-stated.** For a continuous 1-form on an open
  connected `U`, vanishing periods over all piecewise-`C^1` closed curves already implies path
  independence, hence exactness, hence closedness. `d\alpha_F=0` in
  `eq:hist-global-clock-period-criterion` (`05d:796`) is a *consequence*, not a conjunct. The proof
  at `05d:809` ("Closedness and vanishing periods make this integral path independent") over-assumes.
  Drop `d\alpha_F=0` from the display or mark it "equivalently, and then necessarily closed".
- **FINDING 05D-C2 — LOW — the theorem title over-promises.** "Exact criterion for a global
  orthogonal clock" names a criterion, and the criterion is Poincaré's. The genuinely new content of
  the section is `eq:hist-normalized-form-curvature` (`05d:819`),
  `d\alpha_F=N^{-2}\,dN\wedge d\Fenergy_i`, plus its correct reading (`05d:822–823`) that `N` must be
  locally constant on regular level sets of `\Fenergy_i`.

**Both displays verified symbolically.** For the general identity: with `\alpha_F=-d\Fenergy/N`,
`d\alpha_F=-d(N^{-1})\wedge d\Fenergy=N^{-2}dN\wedge d\Fenergy`; sympy residual for a symbolic
`F(x,y)` is **exactly 0**. For the worked obstruction (`05d:829–835`), `\Fenergy=xy` gives
`d\alpha_F=\frac{x^2-y^2}{(x^2+y^2)^{3/2}}dx\wedge dy`; sympy difference from the displayed value is
**exactly 0**.

**Ledger honoring — verified clean.** `appendix_claim_ledger.tex:59–66` marks the global relational
information clock `\status{OPEN}` and names the missing pieces (period conditions, critical and null
strata, base measure and function-space theory). The chapter honors this everywhere:

- `T` is constructed only inside the conditional of `thm:hist-global-clock-exactness` and **never
  used again** — grep for `clock` across `05d` returns 55 hits and none of them is a downstream use
  of the global potential.
- `05d:836–842` immediately exhibits a case where the clock does *not* exist and says
  *"those orbitwise origins do not assemble into the orthogonal scalar"*.
- The chapter's final substantive statement (`05d:1609–1614`, `NOT-CLAIMED`) reads: *"A regional
  clock potential requires the exactness and vanishing period conditions of
  `\Cref{thm:hist-global-clock-exactness}`, and those can fail locally … No operational
  identification of `\tau^{(\ell)}` with a clock reading is made here."*

**Verdict: `05d` does not use a clock it has not built. This is one of the cleanest OPEN-honoring
records in the manuscript and should be preserved as written.**

### 3.4 Is the `L^1` dominating-function discipline maintained throughout?

**Partially. It is exemplary where it appears and absent where the same obligation recurs.**

Where it is maintained — and it is genuinely first-rate:

- `eq:hist-chartwise-vfe-envelope` (`05d:405–426`) is the reference standard for the whole corpus:
  a jointly measurable version in `(\xi,b)` is *required*, a chartwise compact-set dominating
  function `G_K\in L^1(Q_{B^c})` is *named*, the multi-index range `|\alpha|\le2` is *stated*, and
  the text says exactly what each case buys: *"The case `|\alpha|=0` controls the objective
  integrand, and the cases `|\alpha|=1,2` justify two differentiations under the `Q_{B^c}`
  expectation."*
- `thm:hist-averaging-defect` (`05d:1027–1031`) states "finiteness of every integral" as a named
  hypothesis and lists Bochner integrability and barycenter-in-fiber separately (`05d:1002–1003`).
- `eq:hist-continuum-clock-speed` (`05d:707–723`) requires square-integrable evaluation velocities
  before the integral is written, and then explicitly refuses the object without them: *"Without
  those declarations, [the integral] is not an available clock."*

Where it lapses:

- **FINDING 05D-L1 — MEDIUM.** `thm:hist-pointwise-contraction-lift` (`05d:1397–1416`) says only
  "assume every integral is finite" and then differentiates the pointwise action under the integral
  in the proof (`05d:1419`, *"Differentiate the pointwise action, insert into the coarse metric"*).
  This is the same differentiation-under-the-integral that `eq:hist-chartwise-vfe-envelope` pays for
  in full 1,000 lines earlier, discharged here by a five-word hedge. The theorem has an external
  consumer (`08_infogeometry.tex`), so the gap propagates. Import the chartwise envelope.
- **FINDING 05D-L2 — LOW.** `eq:hist-quotient-gauge-speed` (`05d:737–751`) asserts the infimum equals
  the orthogonal-complement norm without an attainment hypothesis at that point; attainment is
  supplied 20 lines later (`05d:753–769`) as a closedness discussion, and correctly. Reorder.
- **FINDING 05D-L3 — LOW.** `prop:hist-natural-gradient-sufficiency` (`05d:1461`) requires "closed
  orbit-tangent splitting" in the finite-dimensional statement where SPEC §5e demands the
  infinite-dimensional caveat; the caveat is present at `05d:753–769` but not cross-referenced from
  the proposition.

## 4. What is strong in `05d`

Stated explicitly because it is substantial and easy to lose in a defect list.

1. **Every witness re-derived reproduced exactly** (7 independent checks; see §7). The anisotropic
   mobility orbit `y=y_0(x/x_0)^2`, the joint-convexity failure with ratio `2/(1+\delta)^2` and its
   exact value `20000/10201` at `\delta=10^{-2}`, the Hessian determinant `-A^2\Sigma^{-6}`, the
   Gram matrix `\mathrm{diag}(1,\tfrac12,\tfrac12)` with determinant `\tfrac14`, the length
   `\int_0^1\sqrt{1+16u^6}\,du=1.60022942767\ldots>\sqrt2`, the exhibited-tier conformality factor
   `a_\ell=\tfrac12` with speed ratio `1/\sqrt2` — all exact.
2. **`hyp:hist-joint-convexity` is proved to be non-decorative** (`05d:1077–1095`). The chapter
   constructs a datum where every other hypothesis of `thm:hist-averaging-defect` holds, only joint
   convexity fails, and the defect is *strictly negative*, tending to `-\tfrac14`, negative exactly
   for `\delta<\sqrt2-1`. Then it explains why: `\det\mathrm{Hess}(A^2/2\Sigma^2)=-A^2\Sigma^{-6}<0`
   in the moment chart while the law-chart integrand `\dot p^2/p` has Hessian determinant zero and
   positive trace. **This is exactly how a hypothesis should be justified and almost nowhere else in
   the corpus does it happen.**
3. **`prop:hist-hoeffding`-style negative discipline throughout.** Nine of the 29 results are
   propositions whose entire content is "X does not imply Y, and here is the witness".
   `prop:hist-noncollapse` (`05d:1280`) catches the total-collapse degeneracy of a semiconjugacy;
   `prop:hist-semidefinite-gradient-obstruction` (`05d:560`) forbids a silent pseudoinverse
   (correctly; wave-1 F6 shows the code violates it).
4. **The chapter retires its own apparent counterexample honestly** (`05d:918–932`): the `b`-fold
   replication pair is explicitly forbidden as a Markov-contraction counterexample, with the
   `\sqrt b` factor correctly attributed to `prop:rg-score-block-lift`'s reference-space change
   rather than to any arrow.
5. **Zero banned phrases, zero bullet lists, one spacing macro, one hand-wave in 1,624 lines.**

---

# PART II — `Theory/07b_agent_network_rg.tex`

## 5. Structural map

Fourteen sections. What is actually proved, in order:

| § | Lines | Content | External consumer |
|---|---|---|---|
| `sec:rg-law-level-vfe` | 13–74 | `thm:rg-exact-coarse-vfe`: KL chain rule under a shared Markov channel; fine VFE = coarse VFE + conditional KL | ledger only |
| `sec:rg-effective-action` | 75–148 | `thm:rg-effective-action`: `e^{-H^c}=\int e^{-H}dR_\rho`; evidence preserved | none |
| `sec:rg-local-action-calculus` | 149–366 | `thm:rg-bounded-action-calculus`: `Q(\varphi)=-\log U(e^{-\varphi})` is real analytic on `\|\varphi\|_\infty<\log2`, with `DQ=U`, `D^2Q=-\mathrm{Cov}`; `prop:rg-action-bounded-recentering` extends to every bounded center | **`08`** |
| `sec:rg-action-contraction` | 367–516 | `thm:rg-action-lp-contraction` (`L^p` contraction, exact `L^2` defect); `prop:rg-dobrushin-cocycle` + two sharp witnesses | none |
| `sec:rg-score-lift` | 517–1050 | DQM, `lem:rg-dqm-realization`, `prop:rg-score-block-lift` (`\|\mathscr I_b\|=\sqrt b`), `thm:rg-score-pushforward-defect`, `prop:rg-action-score-isometry`, `thm:rg-gaussian-hermite-spectrum`, `prop:rg-hermite-scope` | **`08`** ×4, **`05d`** ×1 |
| `sec:rg-action-spectrum-topology` | 1050–1129 | `thm:rg-unital-essential-spectrum`; `prop:rg-circle-norm-witness` | none |
| `sec:rg-finite-network-interactions` | 1130–1363 | `prop:rg-product-equivalence-not-preserved`; `thm:rg-hoeffding-action-isomorphism`; `prop:rg-interaction-rn-gauge-covariance` | `07` (§ ref only) |
| `sec:rg-exact-nonlinear-interaction-rg` | 1364–1513 | `def:rg-interaction-modes`; `cor:rg-interaction-tempered`; retained projections and residuals | none |
| `sec:rg-hypergraph-closure` | 1514–1566 | Möbius inversion; Ising-star non-closure | none |
| `sec:rg-cross-scale-kernels` | 1567–1617 | Bridge kernels, adjointness | none |
| `sec:rg-gauge-cross-scale` | 1618–1744 | Tree transports, holonomy `H_I^x`, dressed edges, `\mathsf C_x\mathsf P_x=I` | none |
| `sec:rg-meta-attention` | 1745–1932 | `\eta^c` pushforward, log-sum-exp merge, Hom operator | none |
| `sec:rg-path-space` | 1933–2120 | `thm:rg-strong-lumpability`; `thm:rg-projection-memory` (Mori–Zwanzig); `cor:rg-resolved-autonomy` | none |
| `sec:rg-beta-function` | 2121–2486 | `prop:rg-action-beta-reference-change`; `def:rg-interaction-beta`; `prop:rg-retained-beta-residual`; `def:rg-scale-connection`; `prop:rg-continuous-beta-underdetermined` | ledger only ×3 |
| `sec:rg-fixed-points` | 2487–2732 | `thm:rg-fixed-point-equations`; two definitions; `prop:rg-fixed-object-nonimplication` | none |
| `sec:rg-closure-theorem` | 2733–2828 | `thm:rg-complete-effective-theory`; `cor:rg-complete-analytic-tier` | none |

### 5.1 FINDING 07B-S1 — HIGH — 73% of the chapter is terminal, and 12 results are referenced nowhere at all

Of 35 formal results:
- **5 (14.3%)** have a mathematical consumer outside `07b`. Four of the five are consumed by a
  single file, `08_infogeometry.tex`; the fifth (`prop:rg-score-block-lift`) by `05d:927`.
- 4 more are referenced only by `appendix_claim_ledger.tex`, which is an audit index, not a
  consumer.
- **26 are referenced nowhere in the corpus.**
- **12 are referenced nowhere at all — not even once inside `07b` itself**:
  `prop:rg-dobrushin-cocycle`, `def:rg-dqm-score`, `prop:rg-circle-norm-witness`,
  `prop:rg-product-equivalence-not-preserved`, `def:rg-interaction-modes`,
  `thm:rg-strong-lumpability`, `thm:rg-projection-memory`, `cor:rg-resolved-autonomy`,
  `def:rg-action-relevance-conventions`, `def:rg-typed-fixed-objects`,
  `prop:rg-fixed-object-nonimplication`, `cor:rg-complete-analytic-tier`.

Two of those twelve are **theorems** (`thm:rg-strong-lumpability`, `thm:rg-projection-memory`) and one
is the chapter's **final corollary**. `thm:rg-projection-memory` is a correct 90-line
Nakajima–Zwanzig derivation for the discrete linear observable tier; nothing anywhere uses a memory
kernel. `thm:rg-strong-lumpability` is a correct standard-Borel extension of Kemeny–Snell; nothing
anywhere lumps a chain.

By line count, only `sec:rg-local-action-calculus` (218 lines) and `sec:rg-score-lift` (534 lines)
contain results with external consumers: **752 of 2,828 lines, 26.6%.** The remaining 2,076 lines
(73.4%) are load-bearing for nothing outside themselves.

This substantially strengthens wave-1's recommendation to demote `07b` to a companion paper. The
two load-bearing sections are the two that `08_infogeometry.tex` uses; they would fit in ~25 pages.

### 5.2 FINDING 07B-S2 — HIGH — zero HYPOTHESIS tags in 2,828 lines

Status census: **81 ESTABLISHED, 10 DEFINITION, 1 OPEN, 1 NOT-CLAIMED, 0 HYPOTHESIS, 0 CONJECTURE,
0 NUMERICAL.** 87% of the chapter's tags are ESTABLISHED. Compare `05d` (48/11/1/4 → 62%
ESTABLISHED), `09` (45/3 → 70%), `10` (19/0 → 68%).

SPEC §2.1 defines HYPOTHESIS as *"A restriction the development adopts by choice. What it excludes,
and where it is used, are stated."* and §1 requires *"State hypotheses before results. A proposition
with an unstated hypothesis is a defect."* `07b` adopts at minimum the following by choice, and tags
none of them:

| Restriction | Location | Currently tagged |
|---|---|---|
| `K_{b_1b_2}=K_{b_1}K_{b_2}` (the semigroup compatibility) | `eq:rg-kernel-semigroup`, `07b:2131` | ESTABLISHED (para 2124–2145) |
| `\pi_\ell\sim\nu_\ell` product-reference equivalence | `07b:1140`, `1148–1149` | DEFINITION |
| `\pi_{\ell+1}=\pi_\ell K_\ell\sim\nu_{\ell+1}` at the target | `07b:1149` | DEFINITION |
| Componentwise/permutation gauge realization | `07b:1258–1262`, `1284–1286` | ESTABLISHED |
| Retained projection `R_\ell` bounded, idempotent, intertwining | `07b:1468–1470` | ESTABLISHED |
| Comparison isomorphisms `J_\ell` bounded with bounded inverse | `eq:rg-interaction-trivialization`, `07b:2227` | DEFINITION |
| Tempering `\lvert V_n\rvert/s_{n\leftarrow\ell}\to0` | `07b:1448` | ESTABLISHED |
| Bochner integrability of the attention Hom moment | `eq:rg-attention-bochner-domain`, `07b:1837` | ESTABLISHED |
| `0<L_*^c<\infty` at the fixed point | `eq:rg-linearization-positive-likelihood`, `07b:2542` | ESTABLISHED |
| Positive-unital resolvent-pole + positive eigenfunctional assumption | `07b:1062–1064` | ESTABLISHED (inside the theorem) |
| Schauder/Riesz basis + interchange | `07b:2404–2407` | ESTABLISHED |
| `\mathcal A^*`-domain, differentiability, pointwise ratios, dual pairings | `07b:2382–2387` | ESTABLISHED |

The chapter is not dishonest about these — it says "suppose", "assume", "require", "declared"
throughout, and the closure theorem (`07b:2736–2752`) lists sixteen supplied hypotheses explicitly.
The defect is that **a reader scanning tags sees an 87%-ESTABLISHED chapter**, which is precisely the
ambiguity SPEC §2 calls "the worst defect this document can have". This is the sharpest available
statement of wave-1's RG-1 and RG-6.

### 5.3 FINDING 07B-S3 — HIGH — `eq:rg-kernel-semigroup` is declared inside an ESTABLISHED tag and never instantiated

`07b:2124–2145` (one paragraph, `\status{ESTABLISHED}` at 2145) contains:

> "Compatibility means, after the declared canonical identifications, `K_{b_1b_2}=K_{b_1}K_{b_2}`.
> … Equation~(2131) makes `\mathcal R_{b_1b_2}=\mathcal R_{b_2}\mathcal R_{b_1}`; otherwise the
> sequence is a typed cocycle rather than an autonomous semigroup."

The *implication* is true and is the ESTABLISHED content. But the paragraph also **defines** the
compatibility condition under the same tag, and:

1. No `(C_b,I_b)` pair satisfying `eq:rg-kernel-semigroup` is exhibited anywhere in `07b` or the
   corpus. `eq:rg-kernel-semigroup` has 2 self-references and 0 external references.
2. `thm:rg-complete-effective-theory` (`07b:2751`) then **supplies it as a hypothesis**: *"and
   rescaling kernels satisfying `\eqref{eq:rg-kernel-semigroup}`."*
3. `thm:rg-fixed-point-equations` (`07b:2492`) quantifies over "every declared `b`", which is empty
   until such a family exists.

This is wave-1 RG-1, now with the additional fact that the declaration carries an ESTABLISHED tag
rather than a HYPOTHESIS one, and that the chapter's *own* fixed-point section (`07b:2705–2711`)
supplies exactly one family that would work — strictly `\alpha`-stable baselines with
`Z=b^{-1/\alpha}\sum_i Y_i` — without connecting it back to `eq:rg-kernel-semigroup`. **That
connection is one paragraph of work and would instantiate the semigroup.** Do it.

### 5.4 FINDING 07B-S4 — HIGH — what remains after the agent language is stripped

Direct measurement:

- `\Fenergy` occurs on **2 lines** of 2,828 (`07b:46,47`), both inside `thm:rg-exact-coarse-vfe`.
  `ELBO` occurs on 4 more. The variational free energy — the manuscript's central object — is
  touched by exactly one theorem, whose only external reference is the ledger.
- The string `agent` occurs on **19 lines** (0.67%): `2, 79, 1530, 1575–1594, 1622, 1633, 1745,
  1905, 2736, 2753, 2813–2814`. Eight are in the chapter opener, the closure theorem, or the
  infinite-extension paragraph.
- The **entire gauge/graph sector** is `07b:1619–1743` plus two lines at `1834–1835`: ~130 lines,
  4.6% of the chapter. Occurrence counts: `\Theta_e` — **1** (`1658`); `\pi_1(` — **1** (`1650`);
  `H_I^x` — 3; `V_e^x` — 3; `\tau^x` — 8. None of these symbols appears in
  `sec:rg-local-action-calculus`, `sec:rg-action-contraction`, `sec:rg-score-lift`,
  `sec:rg-finite-network-interactions`, `sec:rg-path-space`, `sec:rg-beta-function`, or
  `sec:rg-fixed-points`. They appear in **zero other files**.

Section by section, what survives stripping "agent":

| § | Mathematical content with agents removed |
|---|---|
| `law-level-vfe`, `effective-action` | Relative-entropy chain rule and conditional-partition formula for a Markov kernel. Textbook data processing. |
| `local-action-calculus`, `action-contraction` | Banach-algebra analyticity of `\varphi\mapsto-\log U(e^{-\varphi})` for a positive unital `U`; `L^p` contraction of conditional expectation; Dobrushin coefficient. **Zero agents, zero networks, zero gauge.** |
| `score-lift` | Differentiability in quadratic mean; product-path score; **i.i.d. scalar Gaussians** and the Mehler/Hermite spectrum. Wave-1 RG-4 confirmed verbatim: the "inhabited relevance spectrum" (`07b:961`) is the spectrum of `\mathbb E[\cdot\mid b^{-1/2}\sum X_i]` on `L^2_0(\gamma)`. |
| `action-spectrum-topology` | Banach-lattice essential spectrum + the doubling map on `\mathbb T`. **Zero agents.** |
| `finite-network-interactions` | The Hoeffding/ANOVA decomposition of `L^\infty` of a finite product probability space. The "network" contributes **the index set `V_\ell` and the word "hyperedge" for `\lvert A\rvert\ge2`**, nothing more. |
| `hypergraph-closure` | Möbius inversion on a Boolean lattice; Ising-star elimination. Index set only. |
| `cross-scale-kernels` | Bayes adjointness of a bivariate disintegration. Index set only. |
| `gauge-cross-scale` | **The only genuinely agent-network mathematics in the chapter.** Rooted spanning-tree transports, `H_I^x:\pi_1(\Gamma_I,r_I)\to G`, dressed boundary generators, `\mathsf C_x\mathsf P_x=I`. Finite-graph group algebra — no bundle, no connection, no curvature. 130 lines, used nowhere else. |
| `meta-attention` | Pushforward + disintegration of a joint event measure; log-sum-exp merge. Index set. |
| `path-space` | Lumpability; Mori–Zwanzig. **Zero agents.** |
| `beta-function`, `fixed-points`, `closure` | Typing discipline for scale diagrams. Object-agnostic. |

**Answer to the assignment's question: the agent network contributes an index set, a naming
convention for Hoeffding components, and one 130-line island of finite-graph gauge algebra that
nothing consumes. Everything else is generic Markov-kernel coarse-graining, done well.** The chapter
would lose no theorem if retitled *Exact Coarse-Graining of Product Measure Pairs*.

### 5.5 Is the operator apparatus necessary, or decoration?

Assessed case by case.

| Apparatus | Where | Necessary? |
|---|---|---|
| Banach-algebra log/exp series with radius `\epsilon<\log2` | `thm:rg-bounded-action-calculus`, `07b:230–239` | **Necessary and sharp.** `\|U(e^{-\varphi})-1\|_\infty\le e^\epsilon-1<1` holds *iff* `\epsilon<\log2`; the constant is not slack. Verified. |
| Conditional-expectation `L^p` contraction | `thm:rg-action-lp-contraction` | **Necessary.** The exact `L^2` defect `\int\mathrm{Var}_{\Pi(z,\cdot)}(\varphi)d\pi^c` is the chapter's workhorse and is reused three times. |
| Dobrushin coefficient | `prop:rg-dobrushin-cocycle`, `07b:434` | **Decoration, and the chapter says so.** The proposition proves a *sufficient* certificate, then supplies two witnesses showing it is neither necessary (`07b:481–498`) nor sufficient in the nonautonomous case (`07b:503–510`). Both witnesses verified numerically. `prop:rg-dobrushin-cocycle` has **zero references anywhere**. Honest, correct, and load-bearing for nothing. |
| Krein–Rutman / positive-unital essential spectrum | `thm:rg-unital-essential-spectrum`, `07b:1053` | **Decoration on a two-line argument.** The proof (`07b:1072–1087`) is: quotient contractivity gives `r_{\mathrm{ess}}\le r`; the *assumed* positive eigenfunctional plus unitality gives `r(U)\lambda(\mathbf1)=\lambda(U\mathbf1)=\lambda(\mathbf1)`, hence `r(U)=1`, contradiction. **The Perron–Frobenius content is entirely in the hypothesis** — "Assume that whenever `r(U)>r_{\mathrm{ess}}(U)`, the value `r(U)` is a pole of the resolvent and `U^*` has a nonzero positive eigenfunctional" (`07b:1062–1064`). That assumption *is* Krein–Rutman's conclusion. The theorem is honest about this ("This does not assert quasi-compactness or a Perron theorem under weaker hypotheses", `07b:1069–1070`) but the Banach-lattice / Calkin-quotient apparatus is decoration on `\lambda(U\mathbf1)=\lambda(\mathbf1)`. It has 1 self-reference and 0 external references. |
| Memory kernels (Nakajima–Zwanzig) | `thm:rg-projection-memory`, `07b:2027` | **Decoration.** 90 lines, correct, elementary linear algebra (`\mathsf C\mathsf P=I` plus induction). **Zero references anywhere in the corpus.** No memory kernel is ever computed, bounded, or used. |
| Hyperedges (Möbius/Hoeffding) | `07b:1193–1255`, `1530–1546` | **Necessary for the closure claim.** `thm:rg-hoeffding-action-isomorphism` genuinely proves that the full hyperedge family is a Banach isomorphism with a *sharp* extraction bound, and `cor:rg-interaction-tempered` uses that sharpness. This is the chapter's best original result. |
| Strong lumpability | `thm:rg-strong-lumpability`, `07b:1946` | **Decoration.** Correct standard-Borel extension of Kemeny–Snell with a real measurable-selection caveat, plus a clean weak-lumpability witness. **Zero references anywhere.** |
| Scale connection / covariant beta | `def:rg-scale-connection`, `07b:2343` | **Necessary for the typing argument** it supports (`prop:rg-continuous-beta-underdetermined`), which is a genuine and useful negative result. |

Summary: **four of eight apparatus items (Dobrushin, Krein–Rutman, memory kernels, lumpability) are
decoration by the chapter's own reference graph** — each is correct, each is honestly scoped, and
each is used by nothing.

### 5.6 FINDING 07B-S5 — MEDIUM — the exact interaction map rests on a premise the chapter shows can fail

`T_\ell^{\mathcal G}=\mathsf H_{\ell+1}\overline Q_\ell E_\ell` (`eq:rg-exact-nonlinear-interaction-map`,
`07b:1373`) is the chapter's central "exact RG step". It is *"exact as a change of the bounded action
class, **conditional on the product-equivalence premises at both scales**"* (`07b:1380–1381`).

`prop:rg-product-equivalence-not-preserved` (`07b:1160`) then **proves** that the premise fails for
the diagonal-cloning channel: `\pi_1=\pi_0K` is supported on `\{(0,0),(1,1)\}` and no product law on
`\{0,1\}^2` is equivalent to it. Correct.

So the chapter proves that its own key premise can fail, never verifies it for any channel, and
tags the premise DEFINITION rather than HYPOTHESIS. Note `prop:rg-product-equivalence-not-preserved`
has **zero references anywhere** — including from `sec:rg-exact-nonlinear-interaction-rg`, which is
the section it constrains. Add the cross-reference and retag.

(For the record: the premise is usually *satisfiable* for nondegenerate blocking channels — block
statistics of a strictly positive joint density retain a positive density against a product — so
this is MEDIUM, not HIGH. But that is my argument, not the chapter's.)

### 5.7 FINDING 07B-S6 — MEDIUM — `H_I^x` is called a "representation" with no convention and no descent proof

`07b:1648–1655` asserts `H_I^x:\pi_1(\Gamma_I,r_I)\to G` is a homomorphism, tagged ESTABLISHED, no
proof. This extends wave-1 G8 with two specific gaps:

1. **No composition convention is fixed on either side.** `02_geometry.tex:591` defines
   `H^x(\gamma)=\prod_{a=0}^{r-1}\Theta_{e_a}^x` (left-to-right in traversal order). Whether that is
   a homomorphism or an *anti*-homomorphism depends on whether `\pi_1`'s product `\gamma\cdot\delta`
   means "first `\gamma`" or "first `\delta`". **Neither chapter states which.** The transformation
   law at `07b:1653`, `H'(\gamma)=(a_{r_I}^x)^{-1}H(\gamma)a_{r_I}^x`, is conjugation and is
   consistent with both, so it does not disambiguate.
2. **Well-definedness on `\pi_1` (rather than on the free edge-path groupoid) is not shown.** It is
   true — backtracking cancels because `\Theta_{\bar e}^x=(\Theta_e^x)^{-1}` (`02:568`) — but the
   one-line descent argument is absent.

Triage: **(ii) true but needs real work** — specifically, fix one convention in `02` and one in `07b`
and add the backtracking line. Ten minutes of writing; currently an ESTABLISHED claim that is
50/50 backwards.

### 5.8 Sign consistency — no analogue of RG-8 in `07b`, and RG-8 itself needs revising

I audited every exponentiated action or energy in `07b`. Result:

```
e^{-\varphi}      15      exp[-H_o^c(z)]   2      e^{-H_*}          1
e^{-H}             6      exp[-H_o(y)]     2      e^{-H_*(y)}       1
e^{-\Delta}        4      e^{-H_t}         2      e^{-H'}           1
exp[-H_t]          3      exp[-E_j/\tau]   1      exp[-E_J/\tau]    1
e^{-\phi_g}        3      exp[-D_{ij}/\tau] 1
```

**42 occurrences, all `e^{-\text{action}}`. Zero occurrences of `e^{+\text{action}}`,
`\exp[H]`, or `\exp[+\cdot]`.** The conventions chain correctly: `L_o=e^{-H_o}` (`07b:84`) →
`H_o^c=-\log L_o^c` (`07b:108`) → `e^{-H_o^c}=\int e^{-H_o}dR_\rho` (`07b:116`) →
`\Phi_A^c` Möbius potentials summing to `H_o^c` (`07b:1541`) → Ising star `-\log(2\cosh)`
(`07b:1562`). **No sign inconsistency exists in `07b`.**

**Correction to wave 1 (RG-8).** I checked the two flagged lines. `06_general_coarsegraining.tex:320`
writes `e^{-\bar E(z)}` where `\bar E(z)=E(\iota z)` is an *energy*.
`06_general_coarsegraining.tex:392` writes `e^{\mathcal E_\theta(\iota_{\mathcal P}\bar z)}` where
`\mathcal E_\theta` is defined at `06:345` (`def:cg-graph-exponential-energy`) as
`\sum_i\langle\alpha_i,t(z_i)\rangle+\sum_{\{i,j\}}\langle\beta_{ij},u(z_i,z_j)\rangle` — an
exponential-family **natural-parameter pairing**, for which `p\propto e^{+\mathcal E_\theta}` is the
standard and correct convention.

**RG-8 is therefore not a sign error.** It is a genuine but different defect: two symbols one glyph
apart (`E` and `\mathcal E`) carry *opposite* exponent conventions in the same chapter with no note
distinguishing them, and `appendix_notation.tex` has no row for either. Recommend re-classifying
RG-8 from `ERR` to `notation drift, MEDIUM` and adding a one-sentence convention note at `06:344`.

## 6. Status-tag audit — `07b`

81 ESTABLISHED-governing paragraphs:

| Support | Count |
|---|---|
| Followed by `\paragraph{Proof.}` | 29 |
| Contains a `\cite` | 5 |
| Contains only a `\Cref`/`\eqref` pointer | 28 |
| **No proof, no citation, no pointer** | **19** |

### Triage of the 19 unsupported ESTABLISHED claims

| # | Location | Claim | Triage |
|---|---|---|---|
| 1 | `68–73` | Scope: "Such operations **generally** change the comparison target … An invertible or evidence-sufficient observation channel is an exception" | **(ii)** — a negative scope claim with no witness and a hedge ("generally") inside ESTABLISHED. Supply one witness (a fitted `P^c` where evidence changes) or retag. |
| 2 | `141–147` | `0\le L_o\le1\Rightarrow0\le L_o^c\le1` | **(i)** — one line: `L^c` is a conditional expectation of `L` by `eq:rg-conditional-partition`. Add the `\eqref`. |
| 3 | `302–317` | `\|Q(\varphi)-Q(\psi)\|_\infty\le\|\varphi-\psi\|_\infty` | **(i)** — inline proof is present and correct. Verified: `\varphi\le\psi+c\Rightarrow e^{-\varphi}\ge e^{-c}e^{-\psi}\Rightarrow Q(\varphi)\le Q(\psi)+c`. |
| 4 | `319–328` | Projective quotient `\overline{\mathfrak B}=\mathfrak B/\R\mathbf1` well defined | **(i)** — `Q(\varphi+c)=Q(\varphi)+c` and `U\mathbf1=\mathbf1`, both stated. |
| 5 | `1257–1290` | Hoeffding gauge covariance (4 intertwining identities) + the `\mathbb T^2` shear witness | **(i)** for the identities (Fubini, as stated); **the shear witness is correct and valuable**. But the paragraph is a load-bearing result with **no `\label` and no heading**, so nothing can `\Cref` it; `prop:rg-interaction-rn-gauge-covariance`'s proof must cite the equation instead. Promote to a labeled proposition. |
| 6 | `1517–1528` | Variable elimination produces a factor on the union of incident scopes; order-independence by Tonelli | **(i)** — correct and standard. **Uncited.** SPEC §7 "cite, do not claim" applies (Lauritzen 1996 or Koller–Friedman 2009, §9.3). |
| 7 | `1530–1546` | Möbius inversion `H_o^c=\sum_A\Phi_A^c` | **(i)** — **verified numerically**: max residual `1.8\mathrm e{-15}` over all 16 configurations at `n=4`. Needs one line (`\sum_{A\supseteq B}(-1)^{|A|-|B|}=\mathbf1[B=\mathcal P]`) or a citation to Rota. |
| 8 | `1555–1565` | Ising-star cubic coefficient `2\,\mathrm{sech}^2(h_0)\tanh(h_0)J_1J_2J_3+O(J^5)` | **(i)** — **verified symbolically**: the `\varepsilon^3` coefficient of the multilinear expansion is exactly `2J_1J_2J_3\sinh h_0/\cosh^3h_0`, difference from the claim is `0`, and the `\varepsilon^4` coefficient is `0` (so `O(J^5)` is correct, not `O(J^4)`). |
| 9 | `1570–1592` | Bridge-kernel adjointness | **(i)** — Fubini on the bivariate joint, one line. |
| 10 | `1603–1616` | `\mathsf C\mathsf P=I` for a deterministic statistic | **(i)** — immediate. |
| 11 | `1648–1673` | `H_I^x` is a representation | **(ii)** — see FINDING 07B-S6. |
| 12 | `1675–1724` | `\mathsf C_x\mathsf P_x=I`; nested composition "**It then follows that** `\mathsf C_x^{02}=\mathsf C_x^{12}\mathsf C_x^{01}`" | `\mathsf C_x\mathsf P_x=I` is **(i)** (verified: `\sum_iw_{Ii}R(\tau)R(\tau)^{-1}=I` since `\sum w=1`). The nested composition is **(ii)** — an undischarged "it then follows" under a two-line hypothesis (`eq:rg-linear-nested-compatibility`). SPEC §2.2 violation. |
| 13 | `1733–1743` | `\Phi^c=\mathsf C_m\Phi_f\mathsf P_b` covariance | **(i)** — substitution. |
| 14 | `1748–1776` | Meta-attention `\eta^c` normalized, associative, gauge-invariant | **(i)** — tower property, as stated. |
| 15 | `1885–1907` | Conditional KL chain rule for `(J,Z_I)` | **(i)** — standard; add the pointer or a citation. |
| 16 | `2147–2168` | `\mathcal R_b^H` and `\mathfrak B_b^H` | **Tag mismatch:** this paragraph *declares* two objects. It should be DEFINITION. Currently ESTABLISHED. |
| 17 | `2318–2323` | Projected-fixed-point witness `R(x,y)=(x,0)`, `T(x,y)=(x,x)` | **(i)** — **verified**: `\beta^{\mathrm{ret}}=(0,0)` and `\beta^{\mathrm{ex}}=(0,x)` at `b=e`. |
| 18 | `2463–2484` | Replicator beta `\dot\beta_J=\beta_J(u_J-\sum_K\beta_Ku_K)` | **(i)** — **verified symbolically**: residual is exactly `0` for all three components with `\pi_J(t)`, `E_J(t)`, `\tau(t)` all time-dependent. Three lines would discharge it. |
| 19 | `2703–2714` | Strictly `\alpha`-stable baselines give fixed measure pairs; `b`-semistable laws also fixed; "with **the usual centering and regularity hypotheses**" | **(ii)/(iii)**. The `\alpha`-stable claim is (i) — it *is* the definition of strict stability. The semistability remark and the exhaustiveness claim are uncited and the hypotheses are gestured at. SPEC §2.2 violation on "the usual". **This is also the chapter's best missed opportunity: it is the one exhibited family that would instantiate `eq:rg-kernel-semigroup` (FINDING 07B-S3), and the connection is not made.** |

**Triage totals for `07b`: (i) obviously true, needs a line or a citation — 13; (ii) true but needs
real work — 4; (iii) doubtful as stated — 1 (the `\alpha`-stable exhaustiveness clause); plus 1
tag-type mismatch (#16).**

Adding the DEFINITION-should-be items and the untagged-hypothesis list of §5.2, the honest retag of
`07b` moves roughly **12–14 of 81 ESTABLISHED tags to HYPOTHESIS or DEFINITION**.

## 7. Numerical verification log

Sixteen claims re-derived. Every one reproduced. Commands were run under
`python3` (3.10.12) with `sympy 1.14.0`, `numpy 2.2.6`, `scipy`; exact rationals or symbolic
integration used wherever the claim is exact. No GPU or CUDA job was started.

| # | Claim | File:line | Method | Result |
|---|---|---|---|---|
| 1 | `\mathscr L_be_k=b^{1-k/2}e_k` | `07b:889` | symbolic Gaussian integration of `\mathrm{He}_k` against `N(z/\sqrt b,1-1/b)`, `b\in\{2,3,4,5,7\}`, `k=1..8` — **40 cases** | exact, 40/40 |
| 2 | `\mathscr L_{b,\rho}e_k=b^{1-k/2}[1+(b-1)\rho]^{k/2}` | `07b:983` | symbolic, `\rho=3/10`, `b\in\{2,3,5\}`, `k=1..4`; also `\mathrm{Corr}(X_i,Z)=\alpha` re-derived | exact, 12/12 |
| 3 | Hoeffding sharpness `(4p-1)^n-(2p-1)^n` | `07b:1254` | brute-force Möbius projectors over all `2^n` points, `n=1..4`, `p\in\{0.5,0.7,0.9,0.99\}` | max diff `3.6\mathrm e{-15}`, 16/16 |
| 4a | Dobrushin non-necessity witness | `07b:481–498` | `\delta(R_0)=1`, `\delta(R_1)=1`, `\delta(R_1R_0)=0`; both rows of `R_1R_0` are `(1/2,1/2)`; marginal compatibility with `\pi_0,\pi_1,\pi_2` re-derived | exact |
| 4b | One-step-insufficiency witness | `07b:503–510` | `\delta_k=1-2^{-k-2}`, `\prod_k\delta_k=0.5776>0` | exact |
| 5 | Ising star cubic coefficient | `07b:1563` | full multilinear expansion + series in a scaling parameter | `\varepsilon^3` coeff matches exactly; `\varepsilon^4` coeff `=0` |
| 6 | Circle Hölder lower bound `2^{1+\alpha(n+1)}` | `07b:1124` | direct evaluation at `0,2^{-(n+1)}`, `\alpha\in\{0.25,0.5,1\}`, `n\in\{1,2,3,5\}` | tight equality, 12/12 |
| 7 | `d\alpha_F=N^{-2}dN\wedge d\Fenergy` and the `xy` instance | `05d:819,833` | symbolic exterior derivative, general `F(x,y)` and `F=xy` | both residuals exactly `0` |
| 8 | Joint-convexity failure datum | `05d:1085–1091` | exact rational: fine `=1/4`, coarse `=1/(2(1+\delta)^2)`, ratio `2/(1+\delta)^2 = 20000/10201` at `\delta=10^{-2}`; defect limit `-1/4`; threshold `\sqrt2-1`; Hessian det `-A^2\Sigma^{-6}` | all exact |
| 9 | Gram matrix on `S^1` | `05d:327` | symbolic integration | `\mathrm{diag}(1,\tfrac12,\tfrac12)`, `\det=\tfrac14`, eigenvalues `\{1,\tfrac12\}` — exact |
| 10 | `\int_0^1\sqrt{1+16u^6}du>\sqrt2` | `05d:1390` | symbolic + independent quadrature of the original arc length | `1.60022942767221 > 1.41421356237` ; substitution verified to `10^{-14}` |
| 11 | `eq:hist-joint-versus-product` | `05d:461` | 5 random draws, `n=200`, orthogonal projections of ranks 40/35, seed 0 | max diff `2.8\mathrm e{-14}` |
| 12 | Loewner witness | `05d:471–474` | symbolic | `\det=\rho^2(\rho^2-1)`, `q(1,1)=2\rho(1+\rho)`, `q(1,-1)=2\rho(\rho-1)`; marginal precision `1-\rho^2` — exact |
| 13 | Möbius inversion `H^c=\sum_A\Phi_A^c` | `07b:1541` | brute force, `n=4`, all 16 points, random `H`, seed 7 | max residual `1.8\mathrm e{-15}` |
| 14 | Replicator beta | `07b:2475` | symbolic with `\pi_J(t),E_J(t),\tau(t)` all functions, `K=3` | residual exactly `0`, 3/3 |
| 15 | arsinh / arctan / orientation witnesses | `05d:1267–1277` | symbolic | `a_\ell=(1+x^2)^{-1/2}`, `\sigma_0=\mathrm{arsinh}`; `a_\ell=(1+x^2)^{-1}`, `\Sigma_0=(-\pi/2,\pi/2)`; `a\equiv-1` — all exact |
| 16 | Exhibited-tier conformality | `05d:1508–1511` | symbolic with `\Phi=\mathrm{diag}(1,\tfrac12,\tfrac12)`, `\mathsf G_{\ell+1}=\tfrac12\Phi` | `a_\ell=\tfrac12` via `eq:rg-semiconjugacy-factor-formula`; speed ratio `\sqrt2/2=1/\sqrt2` — exact |

Two remarks worth recording. First, in check 6 the claimed lower bound `2^{1+\alpha(n+1)}` is
attained with **equality** at the chosen evaluation points, so the `\ge` in
`eq:rg-circle-holder-lower-bound` is sharp, not slack. Second, in check 5 the `O(J^5)` remainder in
the Ising-star statement is correct and not conservative: the `\varepsilon^4` coefficient vanishes
identically by parity.

**Zero arithmetic or algebraic errors were found in either chapter.**

---

# PART III — Notation drift

Checked `05d` and `07b` against `appendix_notation.tex`, `SPEC.md` §3, `02_geometry.tex`, and
`05_elbo.tex`. Corpus-wide dangling-reference check: **1,290 labels defined, 0 dangling `\ref`/
`\Cref`/`\eqref` anywhere in 24 files.** Reference hygiene is otherwise excellent; what follows is
symbol-meaning drift.

| # | Symbol | Declared meaning + location | Conflicting use(s) | Sev |
|---|---|---|---|---|
| D1 | `\Theta` | `SPEC.md` §3 and `02_geometry.tex:566`, `appendix_notation.tex:214`: `\Theta_e^b,\Theta_e^m\in G`, graph-edge-copy links, with `\Theta_{\bar e}^x=(\Theta_e^x)^{-1}` | `05d:259` `\Theta^\ell_g(\xi)=\xi+\mathsf L_\ell g` — an **affine map on `\R^N`**, not an element of `G`; also `05d:316,1118,1136–1139`. `07b:1262` `\Theta_\ell f=f\circ\vartheta_\ell^{-1}` — a **composition operator on `L^\infty`**; also `07b:1266–1347`. `07b:1658` uses the correct SPEC meaning. **Three incompatible meanings, one of them SPEC-fixed, and neither new meaning has an appendix row.** | **HIGH** |
| D2 | `\tau` | `appendix_notation.tex:192,204`: `\tau^{(\ell)}(r)`, `\tau_{Q,\lambda_0}` — Fisher duration / information clock, the central object of `05d` (22 occurrences) | `07b:1636` `\tau^x_{I\leftarrow i}` — a **`G`-valued ordered transport product** (8 lines). `07b:1790,1821` `\tau` — **softmax temperature**. `07b:2583` `Y_\ell^{(\tau)}` — a **tier label** (appendix:459 records only this last one). Four meanings; `07b:2378` refers to "the Fisher duration of `\Cref{ch:relational-inference}`" in the same chapter that uses `\tau` for three other things. | **HIGH** |
| D3 | `\Phi` | `SPEC.md` §3, `appendix_notation.tex:57`: `\Phi:\mathcal E_b\to\mathcal E_m`, the cross-bundle morphism | `05d:282` `\mathsf G_\ell=\Phi` — the **constant Gram matrix** (also `284,291,292,298,308–314,327,1121–1123`). `05d:947,1156,1209–1325` `\Phi_t,\bar\Phi_u` — **local flows**. `07b:1533` `\Phi_A^c` — **Möbius potential**. `07b:791` `\Phi_\varphi` — **replicated block action**. `07b:1218` `\phi_g` — **assembled action** (this one *is* in the appendix, line 367). `07b:1733` `\Phi_f` — correct SPEC meaning. **Five extra meanings; only two have appendix rows.** | **HIGH** |
| D4 | `\mathcal G` | `appendix_notation.tex:367`: `\mathcal G_\ell` = the interaction Banach space of `07b` | `05d:734,739` `\mathcal G_i` = a **finite-dimensional gauge Lie group** acting on the configuration manifold. No appendix row. Distinguished from `07b`'s only by the index letter, in adjacent chapters. | **MEDIUM** |
| D5 | `Q` | `SPEC.md` §3: `Q_X(dY\mid o)` recognition kernel. `07b:18,30,38` uses `Q_o` correctly | `07b:172,190,272,306,326,335` `Q(\varphi)` — the **nonlinear action map**; `07b:1367,1369` `Q_\ell,\overline Q_\ell`; `07b:2034` `\mathsf Q=I-\Pi^{\mathrm{res}}` — the **complementary projection**; `07b:1886` `\beta_I^Q,K^Q` back to recognition. The recognition law and the action map both appear as `Q` within 150 lines of each other. | **MEDIUM** |
| D6 | `R` | `appendix_notation.tex:182–190` gives a 9-item disambiguation list for the `\mathsf R_\ell` family — genuinely good practice | The list omits four `07b` uses: `R_\rho(z,dy)` reverse conditional (`07b:113`), `R_x:G\to\GL(V_x)` representation (`07b:1676`), `R_0,R_1` reverse matrices (`07b:482–490`), `R_o(z,dy)` full reverse (`07b:1575`). `R_\ell` (retained projection) *is* listed, at appendix:379. | **MEDIUM** |
| D7 | `\alpha` | `SPEC.md` §3: `\alpha_i` = receiver occupancy. `07b:1767,1796` uses it correctly | `07b:980` `\alpha=\mathrm{Corr}(X_i,Z)`; `07b:991` `e_\alpha,\lvert\alpha\rvert` **multi-index**; `07b:1100–1126` `\alpha` **Hölder exponent**; `07b:2707` `\alpha` **stability index**; `05d:780` `\alpha_F` **normalized VFE one-form**. Five extra meanings. | **MEDIUM** |
| D8 | `H` | `07b:84` `H_o` action; `07b:1650` `H_I^x` holonomy map; `07b:1220` `\mathsf H_\ell` Hoeffding extraction; `07b:1727` `H_x` quadratic energy; `05d:186` `H^{\boldsymbol\omega_i}` horizontal lift; `05d:342–347` `H^s,H^1` Sobolev | Six meanings across the two chapters. The sans-serif and superscript distinctions carry the load and are not declared anywhere. | **MEDIUM** |
| D9 | `E` | `SPEC.md` §3: `E_{a,o}` fixed negative log record density. `\E` is the expectation macro | `07b:1219` `E_\ell` **Hoeffding assembly**; `07b:1822` `E_j` attention energy (SPEC-compatible); `05d:1107` `\mathsf E` **intertwining matrix**; `06:320` `\bar E` vs `06:345` `\mathcal E_\theta` with **opposite exponent signs** (see §5.8). | **MEDIUM** |
| D10 | `D` | `SPEC.md` §3: `D=\{c_a\}` the finite design; `D^{\omega_x}` covariant section derivative | `07b:1790` `D_{ij}(y)` **attention energy** — undeclared, appears once, nowhere in the appendix; `07b:1091` `D(z)=2z\bmod1` **doubling map**; `07b:1420` `D_\ell` derivative cocycle; `07b:205–224` `DQ,D^2Q` Fréchet. `D_{ij}` at `07b:1790` and `E_j` at `07b:1822` are the *same kind of object* (a row energy) written with two different letters five lines apart. | **MEDIUM** |
| D11 | `\pi` | `SPEC.md` §3: `\pi:P\to\mathcal C` bundle projection and `\pi_{ij}` generative source prior | `07b:88` `\pi(dy)` **normalized law** (dominant use, ~80 occurrences); `07b:1650` `\pi_1(\Gamma_I,r_I)` **fundamental group**; `07b:1786` `\pi_{ij}` correct SPEC meaning; `07b:1819` `\pi^c_J,\pi_j` coarse prior; `05d:379` `\pi_i^{\mathrm{conf}}` extraction map. Five meanings; `\pi_\ell` (scale-indexed law) and `\pi_j` (source-prior row) differ only by what the index means. | **MEDIUM** |
| D12 | `\mathsf C`,`\mathsf P` | `07b:1679–1683` `\mathsf C_x,\mathsf P_x` cross-scale feature maps; `07b:1606–1608` `\mathsf C g,\mathsf P f` conditional operators; `07b:2029` `\mathsf C:\mathsf X\to\mathsf W`, `\mathsf P:\mathsf W\to\mathsf X` in Mori–Zwanzig | Three uses of one pair of glyphs, all with `\mathsf C\mathsf P=I` — the coincidence is deliberate and unremarked. | **LOW** |
| D13 | `b` | `07b:442,2124` blocking ratio; `07b:602` replication count; `x\in\{b,m\}` **channel index** (SPEC-fixed, `07b:1635`) | `07b:1687` `R_{x,f}` with `x=b`, and `b>1` a block factor, coexist. | **LOW** |
| D14 | `a` | `05d:512` `a_i(\lambda)>0` mobility; `05d:1163` `a_\ell` semiconjugacy factor; `07b:506` `a_k=2^{-k-2}` Dobrushin sequence; `07b:1638` `a_i^x` passive section rechoice (SPEC-fixed via `02:573`); `07b:1782` `a_i` label prior | Five meanings. `05d`'s two are distinguished only by index letter. | **LOW** |
| D15 | `\psi` | `05d:1101` `\psi_b` coarse basis fields; `07b:2405` `\psi_A` Schauder basis; `07b:2568` `\psi_a` eigenoperator | Three. | **LOW** |

**Assessment.** SPEC.md opens by declaring that *"notation drift between chapters is the failure mode
this document exists to prevent."* By that standard these two chapters are the corpus's worst
offenders — `07b` in particular carries at minimum 15 overloaded glyphs, three of which (`\Theta`,
`\Phi`, `\tau`) collide directly with SPEC-fixed or appendix-declared meanings.

Mitigating and worth crediting: **`05d:965–979` is the single best piece of notation hygiene in the
manuscript.** `def:hist-configuration-coarse-map` explicitly enumerates eleven objects that
`\mathsf R_\ell` is *not*, and the appendix reproduces the list at `182–190`. That is exactly the
discipline SPEC asks for. The recommendation is to do the same for `\Theta`, `\Phi`, `\tau`, and `Q`.

---

# PART IV — Prose and SPEC compliance

| Metric | `05d` | `07b` | `09` | `10` |
|---|---|---|---|---|
| Lines | 1,624 | 2,828 | 1,065 | 625 |
| `\;` | 0 | 0 | 0 | 0 |
| `\,` | **1** | **18** | 0 | 0 |
| `\!` | 0 | 0 | 0 | 0 |
| Banned Claude-isms ("key insight", "crucially", "critically", "notably", "importantly", "it's worth noting", "fundamentally", "leverages", "underscores") | **0** | **0** | 0 | 0 |
| Horizontal rules in body | 0 | 0 | 0 | 0 |
| `\begin{itemize}` / `\begin{enumerate}` / `\item` in body | **0/0/0** | **0/0/0** | 0/0/0 | 0/0/0 |
| British spellings | 0 | 0 | 0 | 0 |
| Undischarged hand-waves | **1** | **4** | 0 | 0 |
| `\cite` commands | 3 | 5 | 4 | 14 |
| Citations per 1,000 lines | 1.8 | **1.8** | 3.8 | 22.4 |

### Spacing-macro violations (SPEC §1: "`\;` `\,` `\!` are banned")

`05d:1520` — one instance, `\Delta_F^{\Psi_c}\bigl(Z_x(c),W_x(c)\bigr)\,\mathrm d\mu_i(c)`.

`07b` — 18 instances at lines `532, 551, 552 (×2), 554, 555, 575, 592, 666 (×2), 675, 695, 916,
2072, 2074`. Fourteen of the eighteen are `\,d\mu` before a differential; four are `\,\middle|\,`
inside conditional expectations. All are trivially replaceable with ordinary spacing.

### The five worst prose defects, quoted

1. **`07b:2713`** — `\status{ESTABLISHED}`
   > "Exhaustiveness by strict stability requires invariance over all declared block sizes (or a
   > continuum of scales) **with the usual centering and regularity hypotheses**."

   Two SPEC §2.2 violations in one clause ("the usual", unnamed hypotheses), attached to an
   exhaustiveness claim, inside an ESTABLISHED tag, in the paragraph that supplies the chapter's
   only concrete fixed-point family. Worst instance in either chapter.

2. **`05d:209–210`** — `\status{ESTABLISHED}`
   > "A smooth section is injective because `\varpi_i\circ Q=\operatorname{id}_{\mathcal C_i}`, and
   > it is an embedding **under the usual smooth-bundle hypotheses**."

   The injectivity half is proved in the sentence. The embedding half is an unnamed hypothesis
   inside an ESTABLISHED tag. Worst instance in `05d`.

3. **`07b:1705–1707`** — `\status{ESTABLISHED}`
   > "**It then follows that** `\mathsf C_x^{02}=\mathsf C_x^{12}\mathsf C_x^{01}` and
   > `\mathsf P_x^{02}=\mathsf P_x^{01}\mathsf P_x^{12}`; nested forests alone would not imply either
   > equality."

   "It follows that" is named verbatim in SPEC §2.2 as a hand-wave requiring discharge. The
   discharge is two lines of substitution from `eq:rg-linear-nested-compatibility`; write them.

4. **`07b:68–72`** — `\status{ESTABLISHED}`
   > "Such operations **generally** change the comparison target or the evidence event. An invertible
   > or evidence-sufficient observation channel is an exception, but its preserved event and
   > posterior must be proved explicitly."

   SPEC §2.2: *"Do not smuggle a gap through by weakening the verb."* "Generally change" is a
   probabilistic hedge on a claim with no witness in either direction. Supply one fitted-`P^c`
   witness or retag `NOT-CLAIMED`.

5. **`05d:351–353`** — `\status{ESTABLISHED}`
   > "**No third option is available**: either the `L^2` tier with a strong metric and an objective
   > that is `C^1` there, or a Sobolev tier with the Riesz hypothesis declared and this witness
   > attached."

   An unproved exhaustiveness assertion. The rest of the paragraph is excellent — two tiers, exact
   two-sided bounds, an explicit `H^1` failure witness I re-verified — which makes the unearned
   dichotomy stand out more, not less.

Two near-misses worth noting: `07b:2451` writes "by inspection" but immediately supplies the reason
("because each is of the form `f(s)/f(t)` with `f` positive"), so it is discharged;
`07b:2335` "the usual pushforward relation" is a reference to a standard object, not a gap.

### What is strong on prose

Both chapters are, by the automated counts above, **the cleanest prose in the corpus after chapter 11**.
Zero banned phrases and zero bullet lists across 4,452 combined lines, against a spec that most
authors violate on the first page. Five hand-waves total in 4,452 lines is roughly one per 890
lines. The 19 spacing-macro violations are a five-minute `sed`.

### Citation density

`07b` at 5 citations per 2,828 lines (1.8/1,000) is the corpus's thinnest, and it is the chapter with
the most standard material. Specifically uncited where SPEC §7 says "cite, do not claim":
Hoeffding/ANOVA decomposition (`07b:1193–1211` — Efron–Stein, Hoeffding 1948); Möbius inversion
(`07b:1534` — Rota 1964); variable elimination (`07b:1517` — Lauritzen, Koller–Friedman); the
Dobrushin coefficient (`07b:427` — Dobrushin 1956); Krein–Rutman (`07b:1053`); strict `\alpha`-stability
(`07b:2707`). `Nakajima1958`, `Zwanzig1960`, `KemenySnell1976`, `JonaLasinio2001`, and
`Kallenberg2021` **are** cited, and the `JonaLasinio2001` `\paragraph{Source scope.}` at `07b:1032–1048`
is a model of honest attribution — it enumerates exactly the four items the source supports and
exactly the six that are proved here instead. That paragraph should be the template for the rest of
the corpus.

---

# PART V — Bounded pass over `09` and `10`

Not a full read; a targeted check of the wave-1 T-07 claim.

**`09_coarsegraining.tex`** — 45 ESTABLISHED-governing paragraphs: 13 with a following proof, 1 with
a citation, 9 pointer-only, **22 with no proof, citation, or pointer**. Wave 1 reported 26; my
classifier credits a following `\paragraph{Proof.}` as support, so 22 is the stricter count and the
two figures agree within classifier definition. The 22 are listed in the audit log; roughly
two-thirds contain an inline computation and are triage class (i). The genuinely bare ones are
`09:237–238` ("Positive-definite `W_e` forces `\Theta_e=I`; a singular weight may hide a nonidentity
twist" — one line, no argument, though the argument is one line) and `09:515–516` ("Thus the vertex
fixed spaces and sheaf endpoint maps are exactly functorial under nested partitions" — a
functoriality claim with no verification). Citation density 3.8/1,000.

**`10_renormalization.tex`** — 19 ESTABLISHED paragraphs: 8 proved, 4 cited, 4 pointer-only, **3
bare**. The best-cited chapter in the corpus at 22.4 citations/1,000 lines, and the only one of the
four with a `CONJECTURE` tag. Zero spacing macros, zero banned phrases, zero hand-waves. `10` is
in good shape and was correctly deprioritized by wave 1.

---

# PART VI — Ranked findings

| ID | Sev | Chapter | Finding |
|---|---|---|---|
| 07B-S1 | HIGH | `07b` | 73% of the chapter (2,076 lines) is load-bearing for nothing outside itself; 26 of 35 results referenced nowhere in the corpus; 12 referenced nowhere at all, including two theorems and the final corollary |
| 07B-S2 | HIGH | `07b` | **Zero `HYPOTHESIS` tags in 2,828 lines**; 87% ESTABLISHED; at least 12 restrictions adopted by choice carry no HYPOTHESIS tag |
| 07B-S4 | HIGH | `07b` | Strip the agent language and what remains is generic Markov-kernel coarse-graining. `\Fenergy` on 2 lines; "agent" on 19; the entire gauge/graph sector is a 130-line island (`\Theta_e` once, `\pi_1(` once) used nowhere else in the chapter or corpus |
| 07B-S3 | HIGH | `07b` | `eq:rg-kernel-semigroup` is declared under an ESTABLISHED tag, never instantiated, then supplied as a hypothesis to `thm:rg-complete-effective-theory`. The `\alpha`-stable family at `07b:2707` would instantiate it and the connection is not made |
| 05D-S1 | HIGH | `05d` | `hyp:hist-exact-vfe-lift` is invoked exactly once (`05d:518`); consequently all seven theorems of §§4–10 are statements about an arbitrary `C^2` function on `\R^N` with a constant Gram metric. 68% of the chapter, correctly conditional but with the VFE doing no work |
| D1–D3 | HIGH | both | `\Theta`, `\Phi`, `\tau` each carry 3–6 incompatible meanings, colliding with SPEC-fixed or appendix-declared uses |
| 07B-S5 | MED | `07b` | `T_\ell^{\mathcal G}` rests on a product-equivalence premise that `prop:rg-product-equivalence-not-preserved` proves can fail; the proposition has zero references, including from the section it constrains |
| 07B-S6 | MED | `07b` | `H_I^x:\pi_1\to G` asserted a representation with no composition convention on either side and no descent proof (extends wave-1 G8) |
| RG-8rev | MED | `06` | Wave-1's sign inconsistency is **not** a sign error: `\bar E` is an energy, `\mathcal E_\theta` a natural-parameter pairing. Reclassify as an undeclared sign-convention collision between `E` and `\mathcal E`, and add a convention note at `06:344` |
| 05D-L1 | MED | `05d` | `thm:hist-pointwise-contraction-lift` differentiates under the integral behind "assume every integral is finite", 1,000 lines after the chapter pays for the same operation in full at `eq:hist-chartwise-vfe-envelope`. Has an external consumer (`08`) |
| Tags-07b | MED | `07b` | 4 ESTABLISHED claims are triage class (ii), 1 is class (iii), 1 is a DEFINITION mistagged ESTABLISHED |
| Tags-05d | MED | `05d` | 1 ESTABLISHED claim is class (ii) (`05d:210`), 1 is class (iii) (`05d:351`), 2 are DEFINITION mistagged |
| D4–D11 | MED | both | `\mathcal G`, `Q`, `R`, `\alpha`, `H`, `E`, `D`, `\pi` overloaded; `D_{ij}` (`07b:1790`) undeclared and unindexed |
| Prose | MED | `07b` | 18 banned spacing macros; 4 undischarged hand-waves; 1.8 citations per 1,000 lines with six standard results uncited |
| 05D-C1 | LOW | `05d` | `eq:hist-global-clock-period-criterion` lists `d\alpha_F=0` as a conjunct where it is a consequence of the period condition; the proof over-assumes correspondingly |
| 05D-C2 | LOW | `05d` | `thm:hist-global-clock-exactness` is named as a criterion for a clock; its first biconditional is a tautology and the genuine content is `eq:hist-normalized-form-curvature` |
| 05D-S2 | LOW | `05d` | Stale duplicate label `prop:hist-oriented-semiconjugacy` at `05d:1206` on a Theorem, cited by `06:240` while the ledger cites the `thm:` name |
| 05D-L2/L3, D12–D15 | LOW | both | Ordering and minor overload items, listed above |

## Shortest credible path for these two chapters

1. **Retag `07b`.** Move the ~12 restrictions of §5.2 to `HYPOTHESIS`, retag `07b:2147–2168` and
   `07b:2124–2145` as `DEFINITION`, and add the "what it excludes / where it is used" sentences SPEC
   §2.1 requires. Half a day. This alone fixes the chapter's single largest epistemic defect.
2. **Instantiate `eq:rg-kernel-semigroup`** using the strictly `\alpha`-stable family already at
   `07b:2705–2711`. One paragraph. Closes wave-1 RG-1.
3. **Discharge `hyp:hist-exact-vfe-lift` on `def:hist-finite-configuration-tier`.** Two pages. Turns
   `05d` from gradient-flow calculus into inference geometry and closes a ledger OPEN.
4. **Add a `\Theta` / `\Phi` / `\tau` / `Q` disambiguation block**, modeled exactly on the excellent
   one at `05d:965–979`, and give each new meaning an appendix row.
5. **Fix the five quoted prose defects and the 19 spacing macros.** One hour.
6. **Add the six missing citations** (Hoeffding/Efron–Stein, Rota, Lauritzen, Dobrushin,
   Krein–Rutman, strict stability). One hour.
7. **Demote `07b` to a companion paper**, keeping `sec:rg-local-action-calculus` and
   `sec:rg-score-lift` (the 752 lines with external consumers) in the main text. This confirms and
   quantifies wave-1's recommendation.
