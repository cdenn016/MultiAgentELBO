# P6 — Blackwell / Le Cam comparison-of-experiments investigator

STATUS: COMPLETE

Agent: P6 (comparison of statistical experiments; garbling/sufficiency; convex geometry of
experiment representations; binary symmetric channels; Markov semigroups; heat kernels on the
circle).

Review target: git rev `8ce635807a6ca2a388255fc996c98f7c535e5843`, branch
`review/2026-08-15-deep-review`, repo `C:/Users/chris and christine/Desktop/MultiAgentELBO`.

Scope: the quantitative claims of
`docs/derivations/2026-08-14-operational-intervention-extensions/`.

My verification scripts (written outside the repo, per mandate):

- `C:/Users/CHRISA~1/AppData/Local/Temp/claude/C--Users-chris-and-christine-Desktop-MultiAgentELBO/dee27a29-2275-4d51-8468-1859e5ece79b/scratchpad/p6_independent_check.py`
- `.../scratchpad/p6_pivot_search.py`

## Headline

**Within my scope I found no Critical and no High findings. Every load-bearing quantitative
claim I was asked to test is correct**, including the one I most expected to fail (the fifteen-
coordinate determinant, verified symbolically as a polynomial identity, not just at the two
specializations). The certified conjuncts (iii) and (vi) of the frozen contract are
*quantitative facts about two specific witness pairs*, and all of those facts hold. The defects
I did find are three Medium and four Low items located in surrounding prose and in derivation
remarks that lie **outside** the frozen conjuncts, not in the certified statements themselves.

I want to be explicit, because the mandate warns against inheriting self-certification: I did
not take any internal review, ledger state, or adversarial-report entry as evidence. I
recomputed the passive laws by marginalizing over the mediator rather than using the package's
`delta = a+b-2ab` shortcut; I rebuilt the 15x15 signature matrix from the declared semantics
before comparing it to the displayed table; I ran the Bareiss elimination myself and searched
four interpretations of the stated row interchanges; and I re-derived every step of the circle
heat argument. The mathematics survived all of it.

---

# Part 1 — Results that CHECK OUT (verified independently)

## V1. The BSC passive retained laws are genuinely equal

Recomputed by explicit marginalization over the mediator `E` (a different computation from the
package's):

```
L(1/4,1/3) joint (R,O): {(0,0): 7/24, (0,1): 5/24, (1,0): 5/24, (1,1): 7/24}
L(1/3,1/4) joint (R,O): {(0,0): 7/24, (0,1): 5/24, (1,0): 5/24, (1,1): 7/24}
EQUAL: True     crossover both = 5/12
symbolic delta(a,b) from marginalization = a + b - 2ab ;  symmetric under a<->b: True
```

The equality is not a numerical accident at `(1/4,1/3)`. Two BSCs compose to a BSC whose
"bias" multiplies, `(1-2delta) = (1-2a)(1-2b)`, so composition of BSCs is commutative and
`L(a,b)`, `L(b,a)` have identical passive retained laws for *every* `(a,b)` under uniform `R`.
The document's `5/12` and `(7/24,5/24,5/24,7/24)` are correct.

## V2. The marked-soft-face TV diameters are correct, and the metric IS stated

The mandate asked whether "diameter" has a stated metric. It does: total variation on the
retained joint law of `(R,O)`, named in the heading of §2.2 and used consistently
(`counterexample-proofs.md` §2.2, eq. (2.2)-(2.3)). The numbers are not metric-free.

Derived from scratch. With `K_t(E=0|R=r) = t_r` and `R` uniform,
`p_r(t) = b + (1-2b)t_r`, and since the two `O`-atoms in row `r` carry equal and opposite
differences of magnitude `|p_r - p'_r|/2`,

```
TV(Q_b(t), Q_b(t')) = |1-2b|/2 * ( |t_0 - t'_0| + |t_1 - t'_1| ),
```

whose maximum over `t, t' in [eps, 1-eps]^2` is `(1-2eps)|1-2b|`, attained at
`t=(eps,eps)`, `t'=(1-eps,1-eps)`. I confirmed maximality by exhaustive search over rational
grids of the admissible square rather than by evaluating the claimed argmax:

```
eps=1/8   b=1/3: grid-max TV = 1/4   claimed 1/4   argmax ((1/8,1/8),(7/8,7/8))
eps=1/8   b=1/4: grid-max TV = 3/8   claimed 3/8
eps=1/10  b=1/3: 4/15 = claimed;  b=1/4: 2/5  = claimed
eps=1/3   b=1/3: 1/9  = claimed;  b=1/4: 1/6  = claimed
eps=2/5   b=1/3: 1/15 = claimed;  b=1/4: 1/10 = claimed
```

So `D_{1/3}(eps) = (1-2eps)/3` and `D_{1/4}(eps) = (1-2eps)/2`, and `(1-2eps)/3 < (1-2eps)/2`
strictly for **every** admissible `0 < eps < 1/2`. The mandate's "unequal for all admissible
epsilon" is confirmed.

**Why the pair separates, stated plainly:** the diameter depends only on `b`, the second leg.
The mediator replacement erases the first leg `a` entirely. So the marked soft face recovers
`|1-2b|`, while the passive law only gives `(1-2a)(1-2b)`. That is the entire mechanism.

**Do unequal diameters genuinely obstruct isomorphism in the declared category?** Yes, and I
checked the two steps the argument needs rather than accepting them:

1. *`U` is a TV-isometry.* By `direct-derivation.md` §1 eq. (2)-(3) and the contract,
   `U` is the pushforward induced by `f_R x f_O` with `f_R, f_O` bijections of `{0,1}`. Any
   bijective pushforward preserves total variation. Confirmed.
2. *`Theta` carries the marked face ONTO the marked face.* `Theta` is induced by pushing
   kernels through `(f_R,f_E,f_O)`, so `K_t` maps to `K_{t'}` with `t'` obtained by permuting
   the coordinates (via `f_R`) and possibly `t -> 1-t` (via `f_E`). The palette `[eps,1-eps]^2`
   is closed under both operations, so `Theta` maps the palette *bijectively onto itself*. The
   diameter is therefore preserved, and `(1-2eps)/3 = (1-2eps)/2` is false. Confirmed.

A useful consistency check that the invariant is well chosen rather than an artifact: the pair
`L(1-a,1-b)` also has the same passive law as `L(a,b)`, and `|1-2b|` correctly *fails* to
separate it — because `L(1-a,1-b)` really is isomorphic to `L(a,b)` via `f_E =` bit flip. The
invariant is exactly `|1-2b|`, the flip-invariant content of the second leg.

## V3. The fifteen-coordinate contextual determinant — exact value

I transcribed the 15x15 matrix **as displayed in the markdown** (§3.2) and computed its
determinant symbolically in `(b,d)` with SymPy 1.14.0:

```
det(displayed M) = (2*b - 1)**6*(2*d - 1)**3/32
claimed (3.3)    = (2*b - 1)**6*(2*d - 1)**3/32       IDENTICAL: True
det M(b=1/3, d=5/12) = -1/5038848        (matches (3.4))
det M(b=1/4, d=5/12) = -1/442368         (matches (3.4))
rank at both specializations = 15
```

**Exact value requested by the mandate: `det M(b,d) = (2b-1)^6 (2d-1)^3 / 32`, equal to
`-1/5038848` at `(b,d)=(1/3,5/12)` and `-1/442368` at `(1/4,5/12)`.** Both nonzero. Note this
is a *polynomial identity in two indeterminates*, stronger than the two numbers the package
needs; I verified it as such, so it cannot be an accident of the specialization.

## V4. The displayed matrix is itself semantically correct

The determinant is only meaningful if the table is the right table. I rebuilt the signature
matrix from scratch from the declared semantics — right-override composition `u a v`; `R`
uniform unless assigned; `O` deterministic if assigned, else `BSC_b` from an assigned `E`, else
`BSC_delta` from `R` — independently of both the markdown table and the package's
`recompute.py`, and compared entrywise:

```
entrywise mismatches vs displayed matrix: 0
det(reconstructed) = (2*b - 1)**6*(2*d - 1)**3/32
```

I had also hand-checked all fifteen rows against the semantics before running anything; all
fifteen agree (e.g. row `R1E1` column `c9 = (noop,R0;00)`: the composite is `{R=0,E=1}`, whose
`(0,0)` atom is `P(O=0|E=1) = b`, matching the displayed `b`). Separately, the flat indices in
`recompute.py`'s `SELECTED_COLUMNS = (0,1,2,3,12,14,16,18,20,42,300,301,302,312,316)` decode
exactly to the fifteen coordinates `c1..c15` listed in §3.2 — the script is testing the
document's stated minor, not a different one.

## V5. The hand Bareiss pivot list reproduces exactly (under 0-based row indexing)

This is the check the document explicitly stakes its proof on: "The displayed matrix,
recurrence, pivots, and row-swap sign are the determinant proof." Under the 0-based reading of
"interchange `3<->5`, then `5<->6`, and finally `13<->14`" — the indexing established two
paragraphs earlier in the same section (`0 noop, 1 O0, ... 14 R1E1`) — all fourteen listed
pivots `p0..p13` reproduce exactly, and so does the final entry and the sign:

```
--- (b) upfront 0-indexed (3,5),(5,6),(13,14)
    swaps used = 3; matched claimed pivots = 14/14; broke at k=None
    final SE entry = -(2*b - 1)**6*(2*d - 1)**3/32   matches claimed final: True
    (-1)^swaps * final = (2*b - 1)**6*(2*d - 1)**3/32
```

All Bareiss divisions were exact polynomial cancellations, as the document asserts. See finding
F5 for the indexing-convention caveat.

## V6. Convexification identity (3.1) is exact

`q_* = (1/3,1/6,1/3,1/6)` is L_1's `do(E=0)` response (`b=1/3`); L_2's (`b=1/4`) are
`q_0=(3/8,1/8,3/8,1/8)` and `q_1=(1/8,3/8,1/8,3/8)`; and
`(5/6)q_0 + (1/6)q_1 = (5/6)(3/8)+(1/6)(1/8) = 16/48 = 1/3` in the first coordinate, `8/48=1/6`
in the second, giving exactly `q_*`. The package is here *refuting its own earlier certificate*,
and the refutation is correct: the hard response-image obstruction genuinely does not survive
convexification. That is honest self-criticism and it checks out.

## V7. The randomized-nonisomorphism logic is valid, and the hard ancestor is proved in-package

The mandate asked me to verify the chain "nonzero determinant => affine map determined =>
restricts to a hard isomorphism that was already refuted". The actual chain in the package is
slightly different from that phrasing, and it is sound:

1. Rank 15 (V3) => randomized contextual equivalence on `Delta(S)` is literal equality
   (`0 = sum_x (p(x)-q(x)) c_x` forces `p=q`). So the randomized object is the full 15-vertex
   simplex, not a proper quotient. **This is where the determinant is load-bearing** — without
   it the object could collapse and its extreme points would not be the fifteen hard classes.
2. An affine bijection between finite simplices maps extreme points to extreme points (standard
   convexity; the package's one-line proof via the affine inverse is correct, and an affine
   bijection of convex sets does have an affine inverse). So `T(delta_x) = delta_{theta(x)}`.
3. Convolution and unit preservation make `theta` a unital monoid isomorphism; response
   compatibility through the single `U` makes it response-compatible.
4. The hard theorem forbids exactly that. **Critically, the hard theorem is proved inside this
   package** (`evidence/prior-hard-operational-reduction-proof.md`), not merely hash-cited, and
   I verified it: the fifteen-class enumeration (class sizes `(1,3,3,1,1,1,3,3,1,1,1,3,3,1,1)`
   summing to 27), the response table, and the orbit obstruction (21). The orbit of `q_*` under
   the four typed flips is `{(1/3,1/6,1/3,1/6),(1/6,1/3,1/6,1/3)}` because its two rows are
   equal; the only full-support L_2 responses are `(7/24,...)`, `(3/8,...)`, `(1/8,...)`, with
   first atoms `7/24, 9/24, 3/24` versus `8/24, 4/24`. Disjoint. Correct.

I also checked the category match, which is where a reduction like this usually breaks: the
hard theorem admits an *arbitrary* bijective monoid map on the fifteen classes plus a product
boundary flip, which is a **broader** morphism class than the randomized category produces, so
the reduction lands strictly inside what the hard theorem refutes. No gap.

## V8. Circle heat: passive equality, strict Blackwell domination, strict nesting

*Passive equality.* `H_s H_t = H_{s+t} = H_t H_s` since `H_tau e_n = e^{-n^2 tau} e_n`. Both
chains retain `m(dR) H_{s+t}(R,dO)`. True (see F7 on how this is presented).

*What actually distinguishes the two ordered chains* — the mandate's highest-value question.
The composite kernel is identical, so nothing about the composite can separate them. What
separates them is the **second leg**: `P_1 = m H_s H_t` has `E->O` kernel `H_t`, and
`P_2 = m H_t H_s` has `E->O` kernel `H_s`. Under mediator replacement the first leg is
*deleted* and only the second leg acts on the injected preparation, so the achievable output
laws are `C_t = {nu H_t}` for `P_1` and `C_s = {nu H_s}` for `P_2`. This is a **real
experimental difference, not an encoding artifact**: the achievable sets genuinely differ, and
I verified the strictness survives the *full* soft palette rather than only the constant-parent
one used in the text — if `m(dr)K(r,de)H_t(e,do) = m(dr) (x) (nu_rho H_s)(do)` then
`K(r,.)H_t = nu_rho H_s` for a.e. `r`, and the same Fourier bound applies. The distinction is
"real but declarative": the two chains are the *same* heat flow observed at two different
intermediate times, `(X_0, X_s, X_{s+t})` versus `(X_0, X_t, X_{s+t})`, and the difference is
the declared time index of the mediator. See F7.

*Strict domination.* `H_t = H_s H_{t-s}` exhibits `H_t` as a garbling of `H_s`, hence
`H_s >= H_t` in the Blackwell order (Blackwell, "Equivalent comparisons of experiments", Ann.
Math. Statist. 24 (1953), 265-272, Thm 4: one experiment is more informative iff the other is
obtained from it by a stochastic transformation; Le Cam (1964) for the general randomization
criterion). Strictness: suppose `H_s = H_t L` with `L` Markov and set `g = L e_1`. Then
`|g(y)| = |int e^{iz} L(y,dz)| <= 1` pointwise, while
`H_t g = H_s e_1 = e^{-s} e_1` forces, by Fourier diagonalization,
`ghat(n) e^{-n^2 t} = e^{-s} delta_{n,1}`, so `ghat(n) = 0` for `n != 1` and
`ghat(1) = e^{t-s} > 1`. Then `||g||_2 = e^{t-s} > 1 >= ||g||_inf >= ||g||_2` under normalized
Haar measure. Contradiction. Every step reproduces; `g` is in `L^inf` hence `L^2` on a
probability space, and `H_t` is convolution with Fourier multipliers `e^{-n^2 t}`, so the
diagonalization step is legitimate. The strictness is genuine, not merely non-strictness of a
reverse inequality.

*Strict nesting.* `C_t subset C_s` via `nu H_t = (nu H_{t-s}) H_s`. Strictness with
`nu_rho = H_rho(x_0,.)`, `0 < rho < t-s`: `nu_rho H_s = H_{rho+s}(x_0,.)` has first Fourier
modulus `e^{-(rho+s)}`; writing it as `nu H_t` would need `|nuhat(1)| = e^{t-s-rho} > 1`,
impossible for a probability measure. **Strict, not merely non-strict** — confirmed, with an
explicit witness that has a positive smooth density, as claimed.

## V9. `recompute.py` executes and reproduces the stored JSON with zero differences

```
$ python recompute.py        # Python 3.14.4, stdlib only, exit code 0
parsed structural diff vs evidence/recompute-output.json:   NUM DIFFS: 0
```

**Arithmetic audit (mandate item 5).** Every finite/algebraic quantity is computed in
`fractions.Fraction`, i.e. exact rationals. **There is no floating point and no tolerance
anywhere in the finite claims.** The determinant is cross-checked by two independent exact
routines — `Fraction` Gaussian elimination and integer Bareiss after per-row denominator
scaling — *and* against the closed formula, gated by exact equality
`require(gaussian == bareiss == formula)`. The soft-face diameters, interior separations,
convex-mixture identity, and boundary-vertex checks are all exact rational equalities. The only
non-rational arithmetic is `decimal_heat_record()` (`Decimal`, precision 60), which the script
itself flags `"corroborative_only": True` and the JSON flags
`"decimal_values_are_corroborative_only": true`; the inequalities it checks (`e^{t-s} > 1`)
are proved analytically in the text, so nothing rests on it. The script also uses a custom
`require()` rather than `assert` so it fails closed under `-O`, and records
`"python_assertions_used": false`.

**So the mandate's suspicion — that a claimed "exact" value is really a float comparison with
a tolerance — is not borne out.** The script also declines to overclaim:
`"exact_rational_values_are_corroborative_not_proofs": true`, and `final-report.md` §Certificate
states the executable artifacts "are bound separately as corroboration and are not theorem
evidence". That is the correct posture and it is honored.

---

# Part 2 — Findings

## [MEDIUM] F1. The circle obstruction argument invokes Theorem 8 without a supporting lemma

**Location:** `evidence/direct-derivation.md` §8, lines 534-538

**Claim as stated:** "Any admitted isomorphism in the frozen circle category uses the
compatible `Theta` and the same global `U` for all protocols, intertwines every heat kernel,
and preserves the ordered external roles. Such an isomorphism would preserve Blackwell
equivalence and the soft response sets. Theorems 8 and 9 therefore obstruct it."

**Defect:** the phrase "would preserve Blackwell equivalence" is asserted with no proof and no
definition of what Blackwell equivalence of the *mediator-to-output* experiment means as a
property of the object. `E` is unretained: the `E->O` kernel is raw presentation data, not a
retained response. The package's own position elsewhere is that raw presentation data are *not*
operational invariants — `counterexample-proofs.md` §6 / CE-OIE-011 states exactly that raw
node count, kernels, and protocol coordinates are forgotten by the operational quotient. So an
obstruction argument may not help itself to a raw-kernel-level invariant without first showing
it is operationally recoverable. Theorem 8's strictness (the no-reverse-garbling Fourier
argument) does no work in the obstruction: Theorem 9 alone carries it.

**Evidence:** I ran the obstruction argument both ways myself.
(a) *If* the morphism must match baseline kernels, then since the circle tier requires the state
maps to intertwine every heat kernel, the pushforward of `H_t` is `H_t`, and matching
`P_1`'s `E->O` leg to `P_2`'s gives `H_t = H_s` outright — a contradiction that needs no
Blackwell theory at all.
(b) *If* only response compatibility (3) is required, take `a = K_nu`; then
`(f_R x f_O)_*(m (x) nu H_t) = m (x) ((f_E)_* nu) H_s` for every `nu`. At `nu = delta_x` this
gives `H_t(f_O(x),.) = H_s(f_E(x),.)`, whose first Fourier moduli are `e^{-t}` and `e^{-s}` —
contradiction. That is Theorem 9's mechanism, not Theorem 8's.
In neither reading does Theorem 8's strictness enter. Note also that the dependency DAG
(`dependency-dag.json`) attaches `OIE-CIRCLE-BLACKWELL` directly to `target` with no outgoing
edge, i.e. it is a *conjunct*, not a lemma — which is consistent with my finding that it is not
load-bearing, and inconsistent with the prose "Theorems 8 and 9 therefore obstruct it".

**Falsifier:** exhibit a lemma in the package showing that an admitted typed isomorphism induces
a Blackwell equivalence of the two unretained `E->O` experiments, or show that the frozen
category's definition of isomorphism explicitly requires baseline-kernel correspondence at the
mediator edge, in which case the obstruction sentence is licensed (though still redundant).

**Fix:** replace "Theorems 8 and 9 therefore obstruct it" with "Theorem 9 therefore obstructs
it", and state Theorem 8 as a conjunct in its own right (which is how the contract and the DAG
already treat it). Alternatively add one lemma: the soft response set `R_r` determines `r`
(since `sup_nu |first Fourier coefficient of nu H_r| = e^{-r}`), so the mediator-to-output
experiment *is* operationally recoverable here — after which the Blackwell statement becomes a
legitimate invariant rather than an assumed one.

**Note on severity:** this does not touch the certified conjunct (vi), which claims only equal
passive law + strict one-way Blackwell + strict soft-set inclusion. All three are true (V8).
The defective sentence is an extra-contractual remark.

## [MEDIUM] F2. The convolution hypothesis is dropped in a load-bearing restatement

**Location:** `evidence/direct-derivation.md` §5, lines 344-346

**Claim as stated:** "If the two randomized BSC experiments admitted an affine
response-compatible isomorphism, its restriction to their Dirac vertices would be a hard
response-compatible monoid isomorphism."

**Defect:** Theorem 5, three lines above, requires "affine unital **convolution-monoid**
isomorphism", and the contract's conjunct (iv) likewise says "response-compatible affine unital
convolution-monoid isomorphism". The restatement drops it. As written the implication is
unjustified: an affine response-compatible bijection restricts on vertices to a *bijection*
`theta`, but nothing makes `theta` multiplicative without convolution preservation, so it is
not a "monoid isomorphism". The sentence is self-corrected two lines later ("This argument
requires independent convolution, affinity, the unit, and the one global response
intertwiner"), so this is an internal inconsistency rather than a false theorem.

**Evidence:** the vertex-restriction step (V7 step 2) uses only affinity and bijectivity. The
monoid structure enters solely through `T(delta_a * delta_b) = T(delta_{ab})`, which is exactly
convolution preservation. Remove that hypothesis and `theta` is an arbitrary bijection of the
fifteen classes.

**Falsifier:** a proof that response compatibility alone forces multiplicativity of `theta` for
these two objects. I could not construct one and do not believe it exists in general.

**Fix:** insert "convolution-monoid" in line 344. Worth noting for the authors: the *conclusion*
of that sentence survives without the hypothesis, for a reason the document does not give — the
hard obstruction (21) in the annex is an **image** obstruction, refuting any response-compatible
*bijection* of classes (it only needs some L_2 class to carry relabeled response `q_*`), not
merely any monoid isomorphism. So the randomized theorem is actually true under a weaker
hypothesis than it assumes. Stating that would strengthen the result and remove the
inconsistency at once.

## [MEDIUM] F3. The three BSC nonidentifiability results are not evidentially independent

**Location:** `counterexample-register.md` CE-OIE-002 and CE-OIE-004;
`evidence/prior-hard-operational-reduction-proof.md` §6; `final-report.md` dependency closure
(`OIE-BSC-SOFT-SEPARATION`, `OIE-HARD-NONISOMORPHISM`, `OIE-RANDOMIZED-NONISOMORPHISM` listed as
three separate verified ancestors).

**Claim as stated:** the package presents three separately certified obstructions for the same
pair `L(1/4,1/3)` / `L(1/3,1/4)` — hard response-orbit, marked-soft TV diameter, randomized
contextual rank — and `approach-registry.json` advertises "Mechanism-diverse negative controls
that prevent category drift and theorem inflation".

**Defect:** the *mechanisms* differ (image obstruction / metric invariant / rank plus extreme
points), but the *separating datum* is one scalar in all three cases: the second-leg crossover
`b`. This matters because a certification that lists three independently verified ancestors
invites the reading that the conclusion has triple support, when in fact all three fail or
succeed together with the identifiability of `b`.

**Evidence:** (i) soft face: `D_b(eps) = (1-2eps)|1-2b|`, a function of `b` alone — the first
leg `a` is erased by the replacement (V2). (ii) hard obstruction: the separating responses are
`Phi(do(E=e))`, which equal `((1-b)/2, b/2, (1-b)/2, b/2)` and its flip — functions of `b`
alone; the annex itself notes at §6 lines 341-349 that the "diagnostic mediator-output contrast"
is `|1-2b| = 1/3` vs `1/2`. (iii) randomized: reduces by construction to (ii). Conversely, the
pair `L(1-a,1-b)` has the same passive law and is *not* separated by any of the three — correctly,
since it is genuinely isomorphic via the mediator bit flip.

**Falsifier:** exhibit a passively-equal admitted pair that one of the three obstructions
separates and another does not, with the difference not attributable to `|1-2b|`.

**Fix:** state once, in the register, that the three obstructions are three category-specific
packagings of the single fact that mediator interventions identify `|1-2b|` while the passive
law identifies only `(1-2a)(1-2b)`. This costs nothing — it is the clearest statement of the
result — and it forecloses an inflated reading of the dependency closure.

## [LOW] F4. A stronger and more canonical invariant is available for the BSC witness and is not used

**Location:** `evidence/counterexample-proofs.md` §2.2; contract conjunct (iii);
`approach-registry.json` FAM-CIRCLE-HEAT-BLACKWELL ("arbitrary-Markov Blackwell strictness")
presented as specific to the circle tier.

**Claim as stated:** the finite BSC witness is certified via "unequal exact total-variation
diameters", while strict one-way Blackwell comparison and strict soft-response-set inclusion are
presented as the circle tier's distinctive content.

**Defect:** not an error — an under-claim. The finite BSC witness carries *exactly the same two
structures* as the circle witness, in the same comparison-of-experiments sense, and they are
strictly stronger and more canonical invariants than an ad hoc TV diameter.

**Evidence (computed):**

```
BSC(1/4) garbled by BSC(1/6) gives crossover: 1/3   == 1/3 ? True
```

so `B_{1/3} = B_{1/6} . B_{1/4}`, i.e. L_1's mediator-to-output leg is a strict garbling of
L_2's: **L_2's marked mediator-to-output experiment strictly Blackwell-dominates L_1's**,
exactly parallel to `H_s > H_t` on the circle (strict because `|1-2b|` is `1/2 > 1/3`, and a
BSC(b') is a garbling of BSC(b) iff `|1-2b'| <= |1-2b|`). And the achievable retained-law sets
are strictly nested for every admissible `eps`: the achievable conditional `p_r` ranges over the
interval centered at `1/2` with half-width `(1-2b)(1-2eps)/2`, so

```
eps=1/8   b=1/3: p-interval [3/8,5/8]        b=1/4: [5/16,11/16]   L1 strictly inside L2: True
eps=1/10  b=1/3: [11/30,19/30]               b=1/4: [3/10,7/10]    True
eps=1/3   b=1/3: [4/9,5/9]                   b=1/4: [5/12,7/12]    True
eps=2/5   b=1/3: [7/15,8/15]                 b=1/4: [9/20,11/20]   True
eps=49/100 b=1/3: [149/300,151/300]          b=1/4: [99/200,101/200] True
```

(`1/4 + eps/2 < 1/3 + eps/3` for all `eps < 1/2`.)

**Falsifier:** show that `B_{1/3}` is not a BSC-garbling of `B_{1/4}`, or exhibit an admissible
`eps` for which the intervals are not strictly nested. Neither holds.

**Fix:** state the finite witness with the same two invariants as the circle witness. That
unifies the package around one comparison-of-experiments statement — *mediator replacement
identifies the second leg's Blackwell class, the passive law does not* — and makes conjunct
(iii) strictly stronger at no proof cost.

## [LOW] F5. "Row-position notation" is ambiguous, and the 1-based reading breaks the elimination

**Location:** `evidence/counterexample-proofs.md` §3.2, line 258

**Claim as stated:** "In row-position notation, interchange `3<->5`, then `5<->6`, and finally
`13<->14`."

**Defect:** the indexing base is unstated. A reader checking the proof by hand with 1-based row
positions gets a *different and failing* elimination, which will read as a refutation of the
proof rather than as a convention mismatch.

**Evidence (my run, four interpretations):**

```
(a) upfront 1-indexed (3,5),(5,6),(13,14):  matched 2/14 pivots; ZERO PIVOT at k=3
      first divergence p2: computed -(b-1)(2d-1)/8   vs claimed (2d-1)/8
(b) upfront 0-indexed (3,5),(5,6),(13,14):  matched 14/14 pivots; final SE entry exact
(c) during elimination, 1-indexed:          matched 2/14; ZERO PIVOT at k=3
(d) during elimination, 0-indexed:          matched 14/14
(e) no swaps:                               matched 3/14; ZERO PIVOT at k=3
```

The intended reading is clearly 0-based — the same section numbers the classes `0 noop ... 14
R1E1` — and under it everything reproduces (V5). But the failure mode under the other reading
is a hard breakdown, not a small discrepancy.

**Falsifier:** none; this is a reproduced computation. (It would only be wrong if the pivot list
also reproduced under 1-based indexing, which it does not.)

**Fix:** write "in 0-based row positions (the class indices above), interchange rows 3 and 5,
then 5 and 6, then 13 and 14."

## [LOW] F6. "Strict-interior" is compressed into the diameter claim in the summary

**Location:** `final-report.md` line 52 ("unequal exact marked mediator-face diameters,
**including strict-interior separation**"); `counterexample-register.md` CE-OIE-002.

**Claim as stated:** as quoted.

**Defect:** the diameter `(1-2eps)|1-2b|` is attained **only** at the corners `t=(eps,eps)`,
`t'=(1-eps,1-eps)` of the palette box — never at strictly interior preparations. Equation (2.5),
`|1-2b|(s_+ - s_-)`, is a *strictly smaller* quantity for `eps < s_- < s_+ < 1-eps`. Read as
"the diameters are attained including at strict-interior witnesses", the summary is false; read
as "and additionally there is a strict-interior separation statement", it is true.

**Evidence:** my grid search returns argmax `((eps,eps),(1-eps,1-eps))` at every `eps` tested
(V2), and `|1-2b|(s_+ - s_-) < |1-2b|(1-2eps)` strictly whenever `s_-,s_+` are interior.

**Falsifier:** an interior pair attaining the diameter. None exists, since `|t_r - t'_r|` is
maximized only at the box corners.

**Fix:** the source document already gets this right — `counterexample-proofs.md` §2.2 says
"Equation (2.5) is an interior robustness statement; the full-face diameter remains the
isomorphism obstruction." Propagate that wording to `final-report.md` and the register.

## [LOW] F7. The circle passive equality is an operator identity, and the classical content is unsignposted

**Location:** `evidence/counterexample-proofs.md` §5.1 line 453 ("Integrating out `E` gives the
same passive retained law in both cases"); `counterexample-register.md` CE-OIE-009 headline;
`final-report.md` §Strongest verified result.

**Claim as stated:** "Both retain `m(dR)H_(s+t)(R,dO)`. Yet `H_s` strictly Blackwell-dominates
`H_t` ..."

**Defect:** presentational. `H_s H_t` and `H_t H_s` are the *same operator*, so the passive
equality is a semigroup identity, not a computation that happened to come out equal — the
"Yet" frames it as a coincidence. Concretely, `P_1` and `P_2` are the same heat flow observed
at two different intermediate times, `(X_0, X_s, X_{s+t})` and `(X_0, X_t, X_{s+t})`, and the
counterexample's content is that a Markov semigroup factors through more than one intermediate
time slice, so the mediator's declared time index is not observationally determined. That is
true and correctly proved, but it is elementary, and the surrounding framing (a "certified
mathematical counterexample" with "arbitrary-Markov Blackwell strictness") reads as more than
it is. Relatedly, the package contains **zero citations**; the reader is not told that
`H_s >= H_t` for `s<t` is textbook Blackwell sufficiency for a Markov semigroup, nor that
Theorems 1, 2 and Corollary 2.1 are the classical syntactic (Myhill) congruence and syntactic-
monoid theorems.

**Evidence:** the semigroup identity is immediate from `H_tau e_n = e^{-n^2 tau} e_n`. For the
algebraic theorems: the two-sided relation `a == b iff Phi(uav)=Phi(ubv) for all u,v` is the
syntactic congruence, it is the coarsest congruence contained in `ker Phi`, and the quotient is
terminal among monoids recognizing `Phi` — Myhill, "Finite automata and the representation of
events", WADD TR-57-624 (1957); Nerode, "Linear automaton transformations", Proc. AMS 9 (1958)
541-544 (one-sided version); Rabin and Scott, "Finite automata and their decision problems",
IBM J. Res. Dev. 3 (1959) 114-125; textbook treatment in J.-E. Pin, *Mathematical Foundations
of Automata Theory*, Ch. IV (syntactic congruence of a subset of an arbitrary monoid; coarsest
congruence saturating it; minimality). The generalization from `Y = {0,1}` to arbitrary `Y` is
immediate and standard.

**Mitigating facts I checked, which is why this is Low and not Medium:** the contract's
`literature_policy` states "Standard monoid, probability-kernel, compactness, Feller, Blackwell,
and heat-semigroup facts must be proved directly or mapped hypothesis by hypothesis in the
package. **No novelty, priority, exhaustive-literature ... claim is made.**" The package honors
that policy — everything is proved in-package — and `problem-contract.json` line 19 does call
the object "the syntactic response quotient `Syn(Phi)`", with `direct-derivation.md` using the
standard notation `Syn(Phi)` throughout. So there is no violation of the package's own declared
policy, and no false novelty claim. The residual issue is only that a reader of
`final-report.md` alone, where Theorems 1-2 head the section titled "Strongest verified result",
gets no signal that the headline theorem is classical.

**Falsifier:** a citation or attribution anywhere in the package that I missed. I grepped the
whole directory for `syntactic|myhill|nerode|rabin|scott|blackwell 19|le cam|bibliograph|
references|arxiv|doi:|et al\.|\[[0-9]+\]` and the only hit is `problem-contract.json` line 19.

**Fix:** one sentence in `direct-derivation.md` §2 noting that Theorems 1-2 are the syntactic
congruence / syntactic monoid theorem in the general-monoid, general-codomain form, and one in
§8 noting that `H_s >= H_t` is the standard Blackwell garbling order for a Markov semigroup.
Neither weakens the certificate; both make the genuinely new content (the fifteen-coordinate
rank certificate and the marked-face separation) easier to see.

---

# Coverage

**Read in full (every line):**

- `docs/derivations/2026-08-14-operational-intervention-extensions/evidence/counterexample-proofs.md` (595 lines)
- `.../evidence/recompute.py` (495 lines)
- `.../counterexample-register.md` (221 lines)
- `.../evidence/direct-derivation.md` (553 lines)
- `.../evidence/prior-hard-operational-reduction-proof.md` (404 lines)
- `.../final-report.md` (133 lines)
- `.../dependency-dag.json` (full)

**Read in part / queried programmatically:**

- `.../evidence/recompute-output.json` — parsed and structurally diffed in full against a fresh
  run (0 differences), rather than read line by line.
- `.../problem-contract.json` — read the complete `target.statement`, `literature_policy`,
  `permitted_theorems`, `negative_certificate_kind`, `falsification_criterion`; did not read the
  remaining schema fields.
- `.../approach-registry.json` — extracted all twelve `novelty_fingerprint` fields and the first
  family record; did not read all twelve records in full.

**Not reached (outside my assigned scope):**

- `.../evidence/adversarial-attacks.md`, `.../evidence/independent-reconstruction.md`,
  `.../evidence/oracle-erasure.md`, `.../claim-ledger.json`, `.../adversarial-report.json`,
  `.../construction-or-strongest-theorem.md`, `.../release.json`.
- The second derivation package under `docs/derivations/` and the rest of the 8/15 diff.
- Per the mandate I deliberately did not use any of the internal review, ledger, or
  adversarial-report material as evidence for or against anything.

**Computations I ran (all reproducible from the two scratchpad scripts):** BSC passive law by
mediator marginalization; symbolic symmetry of `delta(a,b)`; exhaustive rational-grid TV
diameter search at four values of `eps` for both `b`; symbolic verification of eq. (2.2);
symbolic determinant of the transcribed 15x15 table in `(b,d)` plus both specializations plus
rank; from-scratch semantic reconstruction of the 15x15 table and entrywise comparison;
fraction-free Bareiss under five interpretations of the stated row interchanges, with pivot-by-
pivot comparison to the claimed list; garbling and strict-nesting check for the finite BSC pair;
`recompute.py` execution and structural diff against the stored JSON.

**Sections with zero findings, stated explicitly as a result:** §1 (power-set monoid
nonrigidity — the automorphism, the contextual-equivalence-is-equality claim, and the
"uniqueness over `A`" resolution all check out and match Corollary 2.1); §3.1 and §3.3
(convexification identity and the shared-noise three-composite-laws control both check out);
§4.1-4.3 (the null-version pair, the sigma-finite-atoms argument, the `E_0` non-smoothness
argument via the Kolmogorov zero-one law, and the `(R,+)` noncompactness witness are all
correct — these were adjacent to my scope and I verified them anyway); §6 (inert-node padding).
