# Skeptic review of P7-High-1-no-RG

STATUS: COMPLETE

| Field | Value |
|---|---|
| Finding attacked | `P7-High-1-no-RG` |
| Wave-1 severity | High |
| Title | `solid_RG_theory.md` contains no renormalization group, and its "Certified boundary" section does not fence that |
| Reviewed revision | `8ce635807a6ca2a388255fc996c98f7c535e5843` |
| **VERDICT** | **UPHELD_REDUCED** |
| **Corrected severity** | **Medium** |
| Corrected scope | Confined to `solid_RG_theory.md` (filename, title, §11 list, §12 roadmap, §11 repository map). The package-level charge is refuted: `overview.md` and `docs/STATUS.md` already fence the RG state, more sharply than the finding's own proposed fix. |

Working-tree check: `git diff --stat 8ce6358 HEAD` touches only `docs/reviews/**`. Every file cited
below is byte-identical to the reviewed revision, `solid_RG_theory.md` included.

---

## 1. What I confirmed against the finding

### 1.1 The absence of RG objects in `solid_RG_theory.md` — CONFIRMED

I read all 399 lines and ran the vocabulary sweep myself:

```
$ grep -n -i -E "semigroup|rescal|blocking|beta function|relevant|irrelevant|universalit|critical|RG depth|renormaliz|fixed point|flow|scale|compos" solid_RG_theory.md
2:# Pointwise meta-agent renormalization
202:... composes exactly under typed nested kernels. ESTABLISHED.
247:Nested normalized memberships compose by
254:Nested endpoint assignments require composition of the full endpoint kernels; ...
281:## 9. Inference flow is optional and typed after the fact
283:Only after declaring a fine flow $\dot y=X_t(y)$ ...
297:... The parameter $t$ is not a base coordinate, physical time, or RG depth. ESTABLISHED.
299:For frozen memberships and the constant-metric Gaussian or feature flow
309:... exponential convergence to the $R$-orthogonal projection onto $\ker L$ ...
321:| A spectral gap is an intrinsic agreement scale | ... arbitrary under $c$-rescaling |
330:ESTABLISHED: fixed-point types; ...
365:### Phase 1: full pointwise probabilistic datum at one fixed point -- ESTABLISHED
391:### Phase 5: participatory and cross-scale nonequilibrium -- OPEN
399:... Frozen dissipative gradient flow may relax toward equilibrium; ...
```

Zero hits for `semigroup`, `rescaling/identification kernel`, `blocking ratio`, `beta function`,
`relevant`, `irrelevant`, `universality`. Every `fixed point` hit is the fixed *base* point `r_*`
(lines 18, 330, 365) or the holonomy-fixed subspace of §2. `flow` is the declared inference flow of
§9. The single `RG` occurrence (line 297) is a disclaimer.

### 1.2 The certified channel cannot be iterated — CONFIRMED by type, not by prose

This is the load-bearing structural point and it survives. From the theorem statement itself
(`Theory/07b_agent_network_rg.tex:84-101`):

```
Let $\mathsf O,\mathsf Y_I,\mathsf B_A,\mathsf M_A,\boldsymbol\Xi_A,$ and $\mathsf H_A$ be
nonempty standard-Borel spaces, and put
    \mathsf Z_A=\mathsf B_A\times\mathsf M_A\times\boldsymbol\Xi_A\times\mathsf H_A.
...
    C_A:\mathsf Y_I\rightsquigarrow\mathsf Z_A.
```

`\mathsf Y_I` and `\mathsf Z_A` are two independently declared standard-Borel spaces with no
declared relation and no declared map `\mathsf Z_A\to\mathsf Y_I`. Therefore `C_A\circ C_A` is not
type-correct: `\mathbb Q_{A,o,X}\in\mathcal P(\mathsf Z_A)` cannot be fed to a kernel with source
`\mathsf Y_I`. There is no endomorphism of any one space in the certificate, hence no iterate, no
flow, and no object of which a fixed point could be predicated. This is a fact about the declared
signature, not an interpretation of anyone's prose.

### 1.3 The criterion the finding applies is the artifact's own, and it is standard — CONFIRMED

The finding is not importing an outside standard. `Theory/07_general_renormalization.tex` opens
(lines 4-6):

> Coarse arrows alone form a scale diagram. They become a renormalization dynamics only after
> comparison and rescaling data identify what is being compared across levels.

and closes the chapter's physicist summary:

> Blocking removes detail; renormalization adds the maps that say how the blocked theory is compared
> with the original units. ... Fixed points, universality, and continuum laws are meaningful only
> after these types and limits have been declared.

and `07:147-148`: "a scale sequence is a cocycle until the comparison data of
\Cref{sec:rg-scale-category} identify its varying spaces." I verified the `07b:2277-2298` quote the
finding relies on verbatim; it reads exactly as quoted, including "otherwise the sequence is a typed
cocycle rather than an autonomous semigroup."

The external standard agrees: the Kadanoff/Wilson block-spin step is coarse-grain **then rescale the
lattice spacing back**, and it is the non-invertibility of the composite that makes the resulting
structure a semigroup rather than a group. The rescale-back step is what makes iteration meaningful.
So the finding's definition of an RG step is neither idiosyncratic nor imported against the artifact.

### 1.4 §11 and §12 do not name the RG obligations — CONFIRMED as a fact about that file

The §11 OPEN/TODO list (line 336) names 19 obligations; none is a rescaling/identification kernel, a
scale-composition semigroup, an RG fixed point, a linearization, or a relevant/irrelevant
classification. §12's roadmap declares itself to record "the next theory program" and runs Phase 0
(notation) → 1 (pointwise datum) → 2 (static VFE) → 3 (comparison theorem) → 4 (extend across
`\mathcal U_A`) → 5 (participatory / cross-scale nonequilibrium). No phase constructs an RG step.

I tested and rejected the most promising rescue here. §11's OPEN item "the frozen comparison
category" is **not** `Theory/07`'s comparison data `I_\ell`. §12 Phase 3 defines its own term —
"target erasure, boundary exchange, time reversal, protocol-dependent relabeling, or latent
dilation ... monotonicity under enlargement of the admitted morphism category" — which is
Blackwell-style comparison of experiments, and every other occurrence in the repo
(`docs/derivations/2026-08-14-operational-intervention-extensions/evidence/adversarial-attacks.md:84,213`;
`docs/superpowers/specs/2026-08-14-operational-intervention-extensions-design.md:109`) uses it that
way. It does not fence the scale-identification datum.

---

## 2. What I refuted in the finding

Four of the finding's supporting sub-claims are wrong or materially overstated. None of them is the
load-bearing point of §1.2, so the finding does not die — but they are why the severity does not
stand.

### 2.1 REFUTED: "no ... scale index, [no] composed-scale composition law ... appears anywhere in `solid_RG_theory.md`"

`solid_RG_theory.md:247-252`:

$$
C_{20}(B\mid i)=\sum_A C_{21}(B\mid A)\,C_{10}(A\mid i).
$$

The subscripts are level pairs 0→1, 1→2, 0→2. This is literally `Theory/07`'s scale-diagram axiom
`eq:rg-scale-diagram` (`07:28`, `C_{kr}\circ C_{\ell k}=C_{\ell r}`) written in the right-acting
kernel juxtaposition of `eq:rg-right-acting-kernel-composition` (`07:35`), instantiated on
membership kernels. Line 202 states the same for the joint-event pushforward: "composes exactly
under typed nested kernels."

This matters procedurally: the finding's own stated falsifier is "exhibiting, in
`solid_RG_theory.md`, a scale-labeled family of coarse maps together with a composition law at the
composed scale." Read literally, §7 is exactly that, and the finding would have to be withdrawn by
its author's own rule. I decline to kill it on that technicality, because the artifact's own
criterion (§1.3) says a scale diagram is not yet an RG — but the enumerated absence list is
factually wrong on two of its eight items, and the falsifier as written was too weak to defend the
thesis it was attached to.

The strongest steelman of the document also fails, and I record it because it is the only route to a
genuine semigroup here: if the membership alphabet were closed under coarse-graining
(`C_{21}` and `C_{10}` the same kernel `C` on one label set), then `\{C^n\}` would be a bona fide
discrete semigroup. It is unavailable for two reasons. The document never declares such a self-map;
and even if it did, the iteration would live on the *label* simplex, while the certified datum is a
law on `\mathsf Z_A`, whose mark/root structure explicitly fails to close — line 235: "collapsing
disconnected component roots or mark fibers to one parent root requires another declared coarse
channel."

### 2.2 REFUTED: "Nothing in the document says which of these two directions 'renormalization' refers to"

Line 10, in the opening paragraph:

> The certificate fixes one base point $r_*\in\mathcal U_A$ and works with a finite network in the
> single fiber over $r_*$. It does not extend the construction across $\mathcal U_A$ or across the
> contextual base $\mathcal C$.

That is an explicit statement that the base direction is held fixed and is not what is being
coarse-grained, reinforced by §11's OPEN item "extension across $\mathcal U_A$" and by Phase 4,
which is precisely the base-direction extension. The document does not print a sentence contrasting
its fiber-direction coarse-graining with `07`'s `c_\ell:\mathcal C_\ell\to\mathcal C_{\ell+1}`, but
the claim that the direction is unstated is false.

### 2.3 OVERSTATED: "without listing the joint-parent law as an open obligation"

The multi-parent joint obligation is declared open twice in the same file. Line 237: "OPEN outside
this certificate: induced hyperedge or shared-factor closure requires the separate Theory/07b
complete joint-density/factorization hypotheses ..." Line 243: "Any shared-factor claim requires a
separately declared joint-factor model." What is true is narrower: those fences live in §6-§7 and
are not repeated in §11's list.

### 2.4 REFUTED at package level: the RG state *is* fenced, and more sharply than the proposed fix

This is the decisive reduction. The finding's charge is that the absence of RG goes unfenced. It
does not — it is fenced in the two repository status documents, both current at the reviewed
revision:

- `docs/STATUS.md:41` — "| Agent-network RG **equations** | **D** | `Theory/07b` — equations only;
  no interacting fixed point exists |"
- `docs/STATUS.md:77` — "**O** No interacting fixed point in `07b`. Every exhibited fixed sector is
  trivial."
- `docs/STATUS.md:193`, `:215` — "... continuum laws, physical geometry, physical time, units, and
  renormalization remain open."
- `overview.md:251` — "... physical geometry, physical time, units, and renormalization remain
  open."
- `overview.md:560-565` — "exact agent-network RG (`Theory/07b`) — where 'exact' governs the
  *equations* (`thm:rg-fixed-point-equations`), not the existence of a fixed point: every fixed
  sector exhibited there is trivial (identity channel, one-point coarse space, or constant
  likelihood ...), and the chapter's only computed exponent lives in an $O(d)$-reduced sector that a
  general $GL(d)$ action destroys (`07b:992-997`)."

That last passage is a harder self-assessment than the finding's own recommended fix, and it
pre-empts the finding's check-out 9: the repository already records that its one inhabited relevance
spectrum sits in a reduced sector destroyed by the general group action.

The frozen certification apparatus is also clean. `problem-contract.json`'s target statement,
domains, codomains, boundary conditions, and permitted theorems make no RG claim of any kind: the
permitted theorems are "Normalized Markov-kernel pushforward and composition", "regular conditional
probabilities and disintegrations", and "KL data processing and the common-channel conditional-KL
chain rule". `evidence/notation-registry.json` goes further and *forbids* reading `\mathcal C`,
`r_*`, or `t` as RG depth. Nothing in the certified package asserts an RG object.

---

## 3. What actually survives

One documentation defect, local to one file:

`solid_RG_theory.md` declares itself "the repository start page" (line 4) and the "sole human-facing
pointwise guide" (line 340); it is named `solid_RG_theory.md` and titled "Pointwise meta-agent
renormalization"; it establishes no RG object under the criterion its own manuscript states; its §11
certified-boundary buckets and §12 "next theory program" roadmap omit the RG obligations; and its
repository map (lines 338-345) routes the reader to `Theory/`, the worklog, and the two derivation
packages, but **not** to `overview.md` or `docs/STATUS.md`, which are the two documents that do
record "renormalization remains open" and "no interacting fixed point exists". A reader who starts
where the file says to start, and stops where the file's own map stops, is not told the state of the
program the file is named after.

That is the whole of it. No statement in the document is false; no theorem is inflated; no proof is
missing, because no RG proof is attempted or claimed. The finding's own check-out 5 concedes that
the `Theory/07b` RG apparatus is logically independent of the pointwise theorem, so nothing
downstream is contaminated.

## 4. Why Medium, not High

The review's rubric (`docs/reviews/2026-08-15-deep-review/RESUME.md`) is explicit:

> **High** (a claim is materially stronger than its proof, or a proof has a repairable gap),
> **Medium** (imprecision, missing hypothesis, notation collision, or a citation/novelty problem),
> **Low** (wording, presentation, hedging).

High requires a claim stronger than its proof or a repairable proof gap. There is neither: the body
of `solid_RG_theory.md` makes no RG claim, and the frozen contract makes none. The overstatement
lives entirely in a filename and a title, and the surviving substantive defect is an obligation
missing from a boundary list and a missing cross-reference in a repository map. "Missing hypothesis"
/ imprecision in a formal boundary declaration is Medium; it is above Low because §11 is a formal
certified-boundary section whose stated function is to enumerate what the certificate does not
close, and the omitted item is the one named in the document's own title.

The finding's own smallest fix — one line in §11 plus a rename — is a Medium-shaped fix. I would
amend it: the missing line should quote the repository's existing language rather than invent new
language, and the repository map should gain rows for `overview.md` and `docs/STATUS.md`:

> OPEN/TODO (add): no rescaling or identification kernel, no scale-composition semigroup, no RG
> fixed point, and no relevant/irrelevant classification is supplied by this pointwise certificate;
> the certified object is a single lossy coarse-graining channel `C_A:\mathsf Y_I\rightsquigarrow
> \mathsf Z_A`, not an RG step. Per `Theory/07`, coarse arrows form a scale diagram and become
> renormalization dynamics only after comparison and rescaling data are declared. The repository's
> RG state is recorded in `docs/STATUS.md:41,77` and `overview.md:560-565`: the `Theory/07b`
> equations are exact, every exhibited fixed sector is trivial, and renormalization remains open.

Renaming the file `solid_coarsegraining_theory.md` remains the honest restatement and I endorse it.

## 5. Relation to the principal reviewer's notes

No conflict. `P0-principal-reviewer-notes.md` reconstructs the parent posterior version, parent
absolute continuity, the additive KL chain and its defect, and the DPI-equality/sufficiency recovery
theorem, plus four items from the operational package. None of those touches the RG question, and
this finding does not dispute any of them. P0's standing conclusion — "the mathematics is correct,
the fencing is unusually careful and honest, the novelty is thin and the certification language
oversells it" — is consistent with the reduction I am recording: this is a labeling and routing
problem, in the same family as P0's novelty concern, not a correctness problem.

## 6. Falsifier of my own attack

My verdict is wrong, and High should be restored, if either of the following holds:

1. A tracked document at rev `8ce6358` presents `solid_RG_theory.md` as the repository's statement of
   the renormalization program — e.g. a `README`, `docs/STATUS.md`, `overview.md`, `Theory/SPEC.md`,
   or release-metadata line billing it as the RG theory or the RG status of record. I searched
   (`grep -rn "solid_RG_theory"` across `*.md`, `*.tex`, `*.py`, `*.json`, excluding `docs/reviews`)
   and found only `.superpowers/sdd/.../task-2-report.md` and the notation scanner's
   collision-report paths — no billing line anywhere. If one exists in a file type I did not sweep,
   the title becomes a load-bearing claim rather than a program name and High is right.
2. `docs/STATUS.md:41,77` or `overview.md:251,560-565` turn out to be stale relative to
   `8ce6358` — i.e. superseded by the 8/15 work rather than updated by it. `git diff --stat
   8ce6358 HEAD` shows only `docs/reviews/**` changed, so the text I quoted is the reviewed text;
   but if the 8/15 diff *removed* an older, stronger RG fence from those files, the package-level
   refutation in §2.4 weakens and the finding moves back toward High.

Conversely my verdict is too harsh on the finding — REFUTED rather than UPHELD_REDUCED — only if
§11's "the frozen comparison category" is shown to denote `Theory/07`'s comparison/identification
data `I_\ell` rather than the Blackwell comparison-of-experiments category. §12 Phase 3's own
enumeration ("target erasure, boundary exchange, time reversal, protocol-dependent relabeling,
latent dilation ... monotonicity under enlargement of the admitted morphism category") and every
other repository occurrence say otherwise, but that reading rests on cross-package terminology
rather than on a definition printed in `solid_RG_theory.md` itself.

---

## Evidence index

| Claim | How checked |
|---|---|
| RG vocabulary absent from `solid_RG_theory.md` | `grep` sweep + full 399-line read |
| `C_A` not iterable | type declaration at `Theory/07b:84-101` and `docs/derivations/2026-08-15-full-pointwise-meta-agent/construction-or-strongest-theorem.md:6-15` |
| Artifact's own RG criterion | `Theory/07_general_renormalization.tex:4-6`, `:147-148`, physicist summary at `:1155-1170`; `Theory/07b:2277-2298` |
| External standard (block spin + rescale ⇒ semigroup) | web search, Kadanoff/Wilson block-spin: coarse-grain, rescale lattice spacing back, non-invertible ⇒ semigroup |
| Scale-composition law present after all | `solid_RG_theory.md:247-252` vs `Theory/07:28,35` |
| Direction stated | `solid_RG_theory.md:10` |
| Joint-parent obligation fenced | `solid_RG_theory.md:237,243` |
| RG state fenced at package level | `docs/STATUS.md:41,77,193,215`; `overview.md:251,560-565` |
| Contract makes no RG claim | `docs/derivations/2026-08-15-full-pointwise-meta-agent/problem-contract.json` (`target.*`, `permitted_theorems`) |
| "comparison category" ≠ scale identification | `solid_RG_theory.md:385`; `docs/.../2026-08-14-operational-intervention-extensions/evidence/adversarial-attacks.md:84,213` |
| Reviewed text unchanged | `git diff --stat 8ce6358 HEAD` → only `docs/reviews/**` |
