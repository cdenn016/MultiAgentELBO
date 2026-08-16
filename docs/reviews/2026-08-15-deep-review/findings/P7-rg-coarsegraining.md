# P7 — RG / Coarse-Graining Investigator Findings

STATUS: COMPLETE

Counts: Critical 0 · High 2 · Medium 4 · Low 2.

Reviewer scope: renormalization group theory, coarse-graining, effective actions,
lumpability / exact decimation, semigroup and commuting-diagram consistency of
coarse-graining maps.

Review target: rev `8ce635807a6ca2a388255fc996c98f7c535e5843` (branch
`review/2026-08-15-deep-review`). 8/15 diff base:
`060f80e5556e41e0f31aeafcd9ef8564c1544c16^`.

## Files to examine

- [x] `solid_RG_theory.md` (read in full, 400 lines)
- [x] 8/15 diff of `solid_RG_theory.md`
- [x] 8/15 diff of `Theory/07b_agent_network_rg.tex` (+153 lines)
- [x] 8/15 diff of `Theory/06_general_coarsegraining.tex` (+29 lines)
- [x] 8/15 diff of `Theory/06a_generative_gaussian.tex` (+3/-3, notation only)
- [x] `Theory/07b_agent_network_rg.tex` §§ RG transformation / beta / fixed points / cross-scale / lumpability (read in full)
- [x] `Theory/07_general_renormalization.tex` scale-category section (read)
- [x] `Theory/06_general_coarsegraining.tex` KL-DPI section (read)
- [x] `docs/derivations/2026-08-15-full-pointwise-meta-agent/` final-report, notation-standard, notation_scan.py
- [x] `docs/derivations/2026-08-14-pointwise-meta-agent-rg/` (sampled: direct-derivation, independent-reconstruction, adversarial-attacks)
- [x] Scale-local bundle vs RG scale
- [x] KL/VFE monotonicity direction (numerically reconstructed)

---

## Findings

### [High] `solid_RG_theory.md` contains no renormalization group, and its "Certified boundary" section does not fence that

**Location:** `solid_RG_theory.md` (whole file); title line 2; §11 lines 328–346.

**Claim as stated:** filename `solid_RG_theory.md`; title `# Pointwise meta-agent
renormalization`; §11 is headed "Certified boundary and repository map" and closes with
"No status crosses an OPEN/TODO boundary above".

**Defect:** the document contains no renormalization-group content in the technical sense
and its exhaustive OPEN/TODO list omits every RG obligation. A coarse-graining map becomes
an RG step only when it is composed with a rescaling/identification kernel that returns the
coarse system to a common state space, so that the step is an endomorphism of one theory
space, can be iterated, and admits fixed points and a linearization. This document's own
manuscript source states that requirement explicitly (`Theory/07b_agent_network_rg.tex:2277–2298`:
"A genuine RG step consists of a coarse channel $C_b$ and a declared rescaling/identification
kernel $I_b$ that returns the target to a common measurable state space"; and
"otherwise the sequence is a typed cocycle rather than an autonomous semigroup"). None of
$I_b$, $K_b$, a blocking ratio, a scale index, a composed-scale composition law, an RG fixed
point, a beta function, or a relevant/marginal/irrelevant classification appears anywhere in
`solid_RG_theory.md`.

Two structural facts make the gap concrete rather than terminological:

1. The certified channel is $C_A:\mathsf Y_I\rightsquigarrow\mathsf Z_A$ — into a
   *different* space, with a *different* index set (parents vs children), and no map back.
   There is no object whose iteration is a flow, hence nothing for a fixed point to be a
   fixed point of.
2. The construction builds one parent $A$ from one child block $I$. A second coarse step
   needs the joint law over *all* parents plus the parent-level graph. The pointwise theorem
   (`Theory/07b:76–178`, "Fix a nonempty finite child block $I$, a parent label $A$",
   singular) does not construct that joint; `solid_RG_theory.md` §7 concedes the related
   point ("Shared children can require a correlated endpoint kernel... Any shared-factor
   claim requires a separately declared joint-factor model") without listing the joint-parent
   law as an open obligation.

Additionally, the coarse-graining direction is orthogonal to the direction 07/07b calls
scale. `Theory/07_general_renormalization.tex:248–266` coarse-grains the *base* through
$c_\ell:\mathcal C_\ell\to\mathcal C_{\ell+1}$ with a covering principal map
$\mathcal P_\ell:\mathscr P_\ell\to\mathscr P_{\ell+1}$. The pointwise program holds the
base fixed at $r_*$ and coarse-grains only the *fiber*; Phase 4 of the roadmap
(`solid_RG_theory.md:387–389`) then puts the parent sections over $\mathcal U_A\subseteq
\mathcal C$, i.e. still over the fine base. Nothing in the document says which of these two
directions "renormalization" refers to.

**Evidence:** exhaustive grep over `solid_RG_theory.md` for RG vocabulary
(`semigroup|rescal|blocking|block ratio|beta function|relevant|irrelevant|universality|critical|RG depth|renormaliz|fixed point`)
returns: `renormalization` once (title, line 2); `RG` once (line 297, in the *disclaimer*
"The parameter $t$ is not a base coordinate, physical time, or RG depth"); `fixed point`
only in the sense of the fixed *base* point $r_*$ (see next finding); zero hits for
`semigroup`, `rescaling`, `blocking`, `beta function`, `relevant`, `irrelevant`,
`universality`, `critical`. The §11 OPEN/TODO list (line 336) enumerates ~25 obligations —
"family-wide common recovery... frozen comparison category; extension across $\mathcal U_A$;
parent local sections and patch gluing; active-set changes; canonical channel, membership,
and partition selection; literal replicated-parent semantics; a geometric meta-agent;
autonomous agency; nonequilibrium persistence; physical time; continuum limits; unique
latent DAG or microscopic physics; ontology; an intrinsic threshold; general noncompact
holonomy averaging; adaptive attention dynamics; nonlinear full-law VFE semiconjugacy; and
dynamically selected memberships" — and does not contain "rescaling/identification kernel",
"scale composition", "RG fixed point", "beta function", "relevant/irrelevant classification",
or "joint law over multiple parents".

**Falsifier:** exhibiting, in `solid_RG_theory.md`, a scale-labeled family of coarse maps
together with a composition law at the composed scale, or any fixed-point/linearization/
exponent statement for the coarse map. (I would also withdraw the finding if §11 already
listed the RG obligations above among OPEN/TODO; it does not.)

**Fix (smallest):** add one line to the §11 OPEN/TODO list — "no rescaling or identification
kernel, no scale-composition (semigroup) law, no RG fixed point, no linearization or
relevant/irrelevant classification, and no joint law over several parents is supplied by this
pointwise certificate; those objects live in `Theory/07` and `Theory/07b` under separately
declared hypotheses" — and, in the opening paragraph, state that the certified object is a
single lossy coarse-graining channel rather than an RG step. Renaming the file
`solid_coarsegraining_theory.md` would be the honest restatement.

---

### [High] The flagship 8/15 theorem is the only stated result in `Theory/07b` carrying no proof

**Location:** `Theory/07b_agent_network_rg.tex:76–178`
(`thm:rg-pointwise-parent-datum`, "Full pointwise probabilistic datum for a candidate
parent"), added by the 8/15 diff.

**Claim as stated:** the 103-line theorem ends at line 178 with `\status{ESTABLISHED}`.
`solid_RG_theory.md` §8 (line 279) routes the reader here: "The canonical sources are
[Theory/06_general_coarsegraining.tex] and [Theory/07b_agent_network_rg.tex]." The status key
(line 16) defines "ESTABLISHED means proved in the contained package or in the cited canonical
theorem source."

**Defect:** the theorem has no `\paragraph{Proof.}`, no proof sketch, and no cross-reference
to any derivation package. It is the *only* one of the 27 stated results in the file in that
condition. The reader who follows the guide's pointer to the "canonical theorem source"
finds an unproved assertion; the actual derivation lives in
`docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md`, which
the manuscript never names. Contrast `solid_RG_theory.md` §3 line 117, which *does* point at
`direct-derivation.md` for the older two-channel theorem.

**Evidence:** enumerating environments in `Theory/07b_agent_network_rg.tex`:

```
$ grep -n "theoremheading{\|propositionheading{\|corollaryheading{\|lemmaheading{\|paragraph{Proof" Theory/07b_agent_network_rg.tex
34:\theoremheading{...}{thm:rg-exact-coarse-vfe}
59:\paragraph{Proof.}
76:\theoremheading{Full pointwise probabilistic datum...}{thm:rg-pointwise-parent-datum}   <-- no proof follows
224:\theoremheading{...}{thm:rg-effective-action}
241:\paragraph{Proof.}
...
```

Every other `\theoremheading`/`\propositionheading`/`\corollaryheading`/`\lemmaheading` in
the file (lines 34, 224, 302, 371, 482, 546, 671, 713, 766, 874, 983, 1085, 1165, 1201, 1272,
1336, 1404, 1545, 2082, 2180, 2238, 2323, 2409, 2572, 2642, 2805, 2888, 2927) is followed by
a `\paragraph{Proof.}`. Line 76 is followed by the theorem statement, `\status{ESTABLISHED}`,
a `\status{NOT-CLAIMED}` scope paragraph, and then `\section{The exact effective likelihood
and action}`. `grep -rn "rg-pointwise-parent-datum"` outside the file returns only
`Theory/06_general_coarsegraining.tex:331` and `Theory/appendix_claim_ledger.tex:191,222` —
all *citing* it, none supplying its proof.

Mitigating fact I verified myself (report honestly): every clause of the theorem is in fact
true and each is a one-to-three-line consequence of results already proved elsewhere in the
same manuscript — normalization and observation-marginal preservation from
$C_A(Y,\mathsf Z_A)=1$; the parent posterior identity from the test-function computation now
added at `Theory/06_general_coarsegraining.tex:319–327`; $\mathbb Q_A\ll\boldsymbol\Pi_A$
because $\boldsymbol\Pi_A(D)=0\Rightarrow C_A(Y,D)=0$ $\boldsymbol\Pi_I$-a.e. $\Rightarrow$
$\mathbb Q_I$-a.e.; and the KL chain (`eq:rg-pointwise-parent-kl-chain`) is the $I\to A$
specialization of the already-proved `thm:rg-exact-coarse-vfe` (line 34). So this is a
proof-presentation defect, not a false theorem.

The 8/15 diff compounds this by adding a matching entry to the manuscript's own claim ledger
(`Theory/appendix_claim_ledger.tex:184–214`), which closes: "The manuscript status is
\textsc{established}; the bound release records ledger state `EVIDENCE_VERIFIED` and terminal
package status `COMPLETE_AFFIRMATIVE`." The manuscript therefore asserts ESTABLISHED, does not
prove it, and cites in support the release metadata produced by the same agent — a closed
loop. `solid_RG_theory.md:346` does distinguish the two labels ("Those package labels report
release evidence; the canonical manuscript theorem is ESTABLISHED"), which makes the missing
manuscript proof the load-bearing gap rather than a redundancy.

**Falsifier:** a `\paragraph{Proof.}` or an explicit "the proof is in ..." pointer attached
to `thm:rg-pointwise-parent-datum` in the committed revision. There is none at rev `8ce6358`.

**Fix (smallest):** insert after line 178 —
`\paragraph{Proof.} Normalization and the preserved observation marginal are $C_A(Y,\mathsf Z_A)=1$. The parent posterior version and its test-function identity are the specialization of \Cref{thm:cg-evidence-preserving-channel} recorded at \eqref{eq:cg-pointwise-parent-posterior-test}. Absolute continuity follows because $\boldsymbol\Pi_A(D)=0$ forces $C_A(\cdot,D)=0$ $\boldsymbol\Pi_I$-a.e. and hence $\mathbb Q_I$-a.e. Equations \eqref{eq:rg-pointwise-parent-kl-chain}--\eqref{eq:rg-pointwise-parent-defect} are \Cref{thm:rg-exact-coarse-vfe} applied to $(\mathbb Q_{I,o,X},\boldsymbol\Pi_{I,o,X},C_A)$. The full derivation is \texttt{docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md}. $\square$`

---

### [Medium] "Composes exactly" is Markov-kernel functoriality; the certified *marked* closure is a cocycle, not a semigroup, and that is nowhere stated

**Location:** `solid_RG_theory.md:202` and §6 lines 204–235; §11 line 330; compare
`Theory/07b_agent_network_rg.tex:1782–1784` and `1831–1843`.

**Claim as stated:** line 202 — "Pushing the joint law and then disintegrating is normalized
and composes exactly under typed nested kernels. ESTABLISHED." §11 line 330 lists as
ESTABLISHED, in one sentence, "normalized joint-event pushforward and disintegration;
incidence-supported component-indexed retained mark laws; ... normalized nested composition".

**Defect:** two distinct objects are being run together. (a) The *scalar* event-law
pushforward $\eta^c_{AB}=\sum_{ij}\eta_{ij}K(A,B\mid i,j)$ does compose exactly — but that is
just Chapman–Kolmogorov for Markov kernels, a property every channel has, including the
terminal one-point channel that destroys all information. It carries no RG content. (b) The
*marked* closure of the same section — component meta-labels $\widehat A=(A,c)$, one chosen
root and rooted spanning tree per component, dressed transports
$\widehat V^x_{ij;(A,c),(B,d)}=\tau^x_{(A,c)\leftarrow i}T^x_{ij}(\tau^x_{(B,d)\leftarrow j})^{-1}$ —
does **not** compose exactly, because a two-step coarse-graining and the corresponding
one-step coarse-graining generally place the parent root at different vertices, and the
dressed marks then differ by a root-gauge conjugation. `Theory/07b` says this explicitly in
both places it arises ("Different trees change the presentation by Nielsen transformations;
nested trees with the compatibility below give strict composition, while arbitrary choices
give a root-gauge-equivariant isomorphism of presentations", 1782–1784; and the explicit
nested condition `eq:rg-linear-nested-compatibility` at 1834–1839 with the warning "nested
forests alone would not imply either equality", 1843). `solid_RG_theory.md` states neither
the compatibility condition nor the failure, while placing "normalized nested composition"
and "component-indexed retained mark laws" side by side in the ESTABLISHED list.

**Evidence (counterexample I built):** take $G=(\mathbb R,+)$ acting by translation; positive-support
transport graph the path $1-2-3$ with $\Omega_{21}=+g$, $\Omega_{32}=+h$, $g\neq0$.

*Two-step.* Step 1: hard memberships $A=\{1,2\}$, $B=\{3\}$. $V_A=\{1,2\}$ is connected;
choose root $r_A=1$, so $\tau_{A\leftarrow1}=0$, $\tau_{A\leftarrow2}=-g$. Step 2: memberships
$Z=\{A,B\}$; choose root $r_Z=A$, so $\sigma_{Z\leftarrow A}=0$. Composed transports are
$\tau^{(2)}_{Z\leftarrow(1,2,3)}=(0,\,-g,\,-g-h)$, i.e. the composite frames everything at
vertex 1.

*One-step.* Compose the memberships as §7 prescribes: $C_{20}(Z\mid i)=1$ for $i=1,2,3$.
Now $V_Z=\{1,2,3\}$ is a single component and the construction instructs "choose one root and
one rooted spanning tree in every component". Choosing $r_Z=2$ — a legitimate choice, since
nothing in `solid_RG_theory.md` constrains it — gives
$\tau^{02}_{Z\leftarrow(1,2,3)}=(+g,\,0,\,-h)$.

The two dressed-mark families differ by the constant left translation $+g$; the pushed-forward
conditional mark laws therefore differ by that root-gauge action and are *not* equal. Equality
holds only under the extra hypothesis $\tau^{02}_{Z\leftarrow i}=\sigma^{12}_{Z\leftarrow A}
\tau^{01}_{A\leftarrow i}$ — which is exactly `Theory/07b:eq:rg-linear-nested-compatibility`.
So the certified marked coarse-graining is a *cocycle over the root/tree choice*, not a
semigroup, which is the precise sense in which the construction is not yet an RG.

**Falsifier:** a sentence in `solid_RG_theory.md` §6 or §7 requiring nested roots/trees, or a
proof that the marked closure is root-choice independent. Neither exists at rev `8ce6358`.

**Fix (smallest):** append to §6 after line 235 — "Composition of two marked steps is exact
only under the nested-root and nested-tree compatibility $\tau^{02}_{A\leftarrow i}=
\sigma^{12}_{A\leftarrow I}\tau^{01}_{I\leftarrow i}$ of
[Theory/07b](Theory/07b_agent_network_rg.tex); with arbitrary root choices the two-step and
one-step presentations agree only up to a root-gauge isomorphism. ESTABLISHED boundary."

---

### [Medium] §6's "canonical network source" pointer names a chapter that does not contain §6's or §7's construction

**Location:** `solid_RG_theory.md:239` ("The canonical network source is
[Theory/07b_agent_network_rg.tex]"), covering §6 lines 183–237 and, by continuity, §7.

**Claim as stated:** line 239, immediately after §6's ESTABLISHED scalar and marked
coarse-graining results and immediately before §7's hard/soft/replicated membership section.

**Defect:** none of §6's or §7's objects occurs in `Theory/07b`. Searched the whole `Theory/`
tree: `C(A\mid i)` (membership kernel), `K(A,B\mid i,j)` (correlated endpoint kernel),
`K_\otimes`, `\eta^c_{AB}`, "soft membership", "replicated cover", "normalized membership",
$V_A=\{i:C(A\mid i)>0\}$, and the component meta-label $\widehat A=(A,c)$ built from soft
memberships — all return zero hits in `Theory/*.tex`. What `Theory/07b` actually contains
(`eq:rg-meta-attention`, lines 1896–1912) is a *different* operation on a *different* object:
a **hard node partition** ($i\in I$, $j\in J$) coarse-grained by a **posterior-bridge
conditional expectation** $\eta^c_{IJ}(z)=\mathbb E_{B_o}[\sum_{i\in I}\sum_{j\in J}\eta_{ij}(Y)\mid Z=z]$,
whose associativity is justified "by the tower property" for nested $\sigma$-algebras.
Likewise `eq:rg-component-meta-index` (1735–1740) builds $\widehat{\mathcal P}$ from a
partition $\mathcal P$, not from a membership kernel. The soft-membership generalization has
no manuscript counterpart at all.

The result itself is not unsupported — the derivation is in
`docs/derivations/2026-08-14-pointwise-meta-agent-rg/evidence/direct-derivation.md:220–240`
and `independent-reconstruction.md:30–32`, which the status key admits as "the contained
package". The defect is that the guide names the wrong source, and that the reader is told a
chapter proves something it does not mention.

**Evidence:**
```
$ grep -rn "C(A\\mid\|K(A,B\|soft membership\|replicated cover\|normalized membership" Theory/*.tex
(no matches)
$ grep -n "membership" Theory/07b_agent_network_rg.tex
182:  channel and child membership are declared inputs, not canonical selections. ...
1809: does not select $I$, $A$, a partition, or a membership kernel.
2176: ... moving-membership ...
```
i.e. `Theory/07b` mentions memberships only to disclaim them.

**Falsifier:** locating $C(A\mid i)$ or $K(A,B\mid i,j)$ anywhere in `Theory/`.

**Fix (smallest):** change line 239 to "The membership-kernel and marked-closure derivations
are in [direct-derivation.md](docs/derivations/2026-08-14-pointwise-meta-agent-rg/evidence/direct-derivation.md);
[Theory/07b](Theory/07b_agent_network_rg.tex) states the hard-partition, posterior-bridge case."

---

### [Medium] "Fixed point" means the base point here and the RG fixed point in the cited chapter; the Phase-0 "collision-free" exit gate cannot see this or several other RG-scale collisions

**Location:** `solid_RG_theory.md:18` (§1 "Fixed-point data and conventions"), line 365
("Phase 1: full pointwise probabilistic datum at one fixed point"), line 330
("ESTABLISHED: fixed-point types"); §12 Phase 0 at lines 352–363; scanner at
`docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation_scan.py:369–395`.

**Claim as stated:** line 352 — "### Phase 0: collision-free notation standard -- COMPLETE";
line 363 — "The exit gate is closed by the authoritative registry, migration record, scanner
self-test, and stored collision report in the full-datum package."

**Defect (two parts).**

(a) In a document titled "Pointwise meta-agent renormalization", the unqualified phrase
"fixed point" denotes the fixed *base* point $r_*\in\mathcal U_A\subseteq\mathcal C$, while in
the chapter this document names as its canonical source the same phrase denotes a fixed point
of the RG map: `Theory/07b` §`sec:rg-fixed-points`, `thm:rg-fixed-point-equations`
(`\mathcal R_b(\rho_*,m_*)=(\rho_*,m_*)`), `def:rg-typed-fixed-objects`,
`prop:rg-fixed-object-nonimplication`, `eq:rg-fixed-action-ray`. "Phase 1: full pointwise
probabilistic datum at one fixed point -- ESTABLISHED" reads, to an RG reader, as a claim
about an RG fixed point; it is a claim about one point of the contextual base.

(b) The Phase-0 exit gate does not support the word "collision-free". `notation_scan.py`
does not detect collisions; `_hazards()` (lines 369–395) is a hard-coded list of ten regexes
for *previously known* collisions: `Q_q`, `Q_m`, `C_t`, `\varpi_i`, `P_A`, `Q_A`,
"P (principal bundle)", "P,Q (local dummy measures)", `m_i`, `C_A`. It has no general
symbol-collision mechanism, no English-phrase check, and no cross-file type comparison. RG-scale
collisions it therefore cannot see, all live in the active sources:

| symbol | meaning 1 | meaning 2 |
|---|---|---|
| $\mathcal C_\bullet$ | agent support $\mathcal C_i$ (registry; `07b:79`) | contextual base at RG scale $\ell$, $\mathcal C_\ell$ (`07_general:154`; registry's own "Scale principal bundle $\mathscr P_\ell\to\mathcal C_\ell$" row) |
| $c_\bullet$ | moving deterministic coarse map $c_t$ (registry; `solid_RG_theory.md:283`) | base scale map $c_\ell:\mathcal C_\ell\to\mathcal C_{\ell+1}$ (`07_general:249`) |
| $C_\bullet$ | coarse Markov kernel $C_A$ (registry) | associated-bundle scale morphism $C_{\ell,s}:\mathcal E_{\ell,s}\to\mathcal E_{\ell+1,s}$ (`07_general:279`) |
| $C(\cdot\mid\cdot)$ | membership kernel $C(A\mid i)$ (`solid_RG_theory.md:185`) | not registered at all |
| $\mathsf C$ | posterior conditional expectation (`07b:1720`) | linear feature aggregation $\mathsf C_x$ (`07b:1815`), projection operator $\mathsf C$ (`07b:2182`) |
| $\mathcal U_\bullet$ | overlap patch $\mathcal U_A=\bigcap_{i\in I}\mathcal C_i$ (registry) | trivializing neighborhood $U_i$ (`07_general:225`) |

None of $\mathcal C_\ell$, $c_\ell$, $C_{\ell,s}$, $C(A\mid i)$, $\mathsf C_x$, or $U_i$ is in
the registry, and none is in the scanner's hazard list, so a clean collision report is
consistent with all of them.

**Evidence:** `notation_scan.py:370` — `for token in ("Q_q", "Q_m", "C_t", "\\varpi_i")`;
`:375` — `for token in ("P_A", "Q_A")`; plus five further one-off `re.search` calls, then
`return sorted(set(tokens))`. The `canonical_tokens` loop (lines 411–415) only records
*canonical* occurrences; it never compares types across files. `notation-standard.md`'s
registry table contains no row for any symbol in the table above except $C_A$ and $c_t$.

**Falsifier:** a general collision-detection pass in `notation_scan.py`, or registry rows
disambiguating $\mathcal C_i$ from $\mathcal C_\ell$ and $c_t$ from $c_\ell$. Neither exists.

**Fix (smallest):** downgrade Phase 0 from "collision-free notation standard -- COMPLETE" to
"registered-hazard re-check -- COMPLETE (ten enumerated collisions; the scanner is a targeted
regression check, not a collision detector)"; retitle §1 "Base-point data and conventions" and
Phase 1 "...at one fixed base point $r_*$"; add registry rows for $\mathcal C_\ell$, $c_\ell$,
$C_{\ell,s}$, and $C(A\mid i)$.

---

### [Medium] The RG semigroup is assumed as a hypothesis, listed among the conclusions of the closure theorem, and never instantiated for any agent-network coarse channel

**Location:** `Theory/07b_agent_network_rg.tex:2277–2298` (`eq:rg-kernel-semigroup`) and
`2888–2909` (`thm:rg-complete-effective-theory`, "Complete finite law-level gauge-VFE
theory", `\status{ESTABLISHED}`).

**Claim as stated:** hypotheses of the closure theorem include (line 2904–2905) "and
rescaling kernels satisfying \eqref{eq:rg-kernel-semigroup}"; its conclusion (2905–2909)
reads "Then the global and local ELBOs, agent--meta bridge kernels, meta-agent interaction
kernels, meta-attention, effective likelihoods, **measure-pair scale composition**, and
measure-pair fixed equations ... are simultaneously normalized, gauge covariant, and exact."

**Defect:** "measure-pair scale composition" is the assumed hypothesis restated as a
conclusion. Given $K_{b_1b_2}=K_{b_1}K_{b_2}$, the composition
$\mathcal R_{b_1b_2}=\mathcal R_{b_2}\mathcal R_{b_1}$ is a one-line consequence
(I checked it: $\mathcal R_{b_2}(\mathcal R_{b_1}\rho)=(\rho K_{b_1})K_{b_2}=\rho K_{b_1b_2}$,
and the stated order is correct). So the clause is true but empty, and the theorem's title
plus `ESTABLISHED` status conveys more than the argument delivers.

The substantive gap behind it: the semigroup property — the *defining* property of a
renormalization group — is nowhere verified for a coarse channel of the kind this chapter
studies. The only fixed sectors exhibited (2856–2876) are the identity channel, the terminal
one-point channel, and strictly $\alpha$-stable block sums (the classical CLT fixed point) —
none of which is an agent-network coarse-graining with memberships, holonomy marks, or an
attention event law. The preceding finding gives a concrete obstruction for the marked
construction: root/tree choices make the composite a cocycle, and 07b itself concedes
"otherwise the sequence is a typed cocycle rather than an autonomous semigroup" (2297–2298)
and "a scale sequence is a cocycle until the comparison data ... identify its varying spaces"
(`07_general:147–148`).

**Evidence:** `07b:2282–2285` states `eq:rg-kernel-semigroup` under "Compatibility means,
after the declared canonical identifications, ..." — a declaration, not a lemma. `grep -rn`
for any verification of `eq:rg-kernel-semigroup` returns only its definition (2284), its
use as a hypothesis in the closure theorem (2905), and the fixed-point discussion. No
proposition establishes it for any nontrivial channel in this theory.

**Falsifier:** a proposition anywhere in the repository proving $K_{b_1b_2}=K_{b_1}K_{b_2}$
for a membership-kernel or marked agent-network coarse channel.

**Fix (smallest):** remove "measure-pair scale composition" from the conclusion list of
`thm:rg-complete-effective-theory` (it is a hypothesis), and add after 2298: "No coarse
channel constructed in this chapter is proved to satisfy \eqref{eq:rg-kernel-semigroup};
for the marked construction of \Cref{sec:rg-gauge-cross-scale} it holds only under the nested
root/tree compatibility \eqref{eq:rg-linear-nested-compatibility}. \status{OPEN}"

---

### [Medium] The unrestricted forward-KL barycenter identity is a classical result presented with no attribution

**Location:** `solid_RG_theory.md:119–140` (§4 "The unrestricted forward-KL parent"),
boxed identity at lines 130–134.

**Claim as stated:** "$\sum_iw_i\operatorname{KL}(P_i\Vert R)=\sum_iw_i\operatorname{KL}(P_i\Vert M)+\operatorname{KL}(M\Vert R)$
... Therefore $M$ is the unique unrestricted full-law forward-KL barycenter. The proof is
exact Radon-Nikodym algebra ... ESTABLISHED."

**Defect:** the identity is correct (I reconstructed it below), but it is the classical
*compensation identity* for relative entropy, the defining property of Sibson's information
radius, and it is presented with no citation anywhere in the document, in `Theory/`, or in
`references.bib`. Under the repository's own convention that ESTABLISHED means "proved in the
contained package **or in the cited canonical theorem source**", presenting a 1969 result with
"the proof is exact Radon-Nikodym algebra" and no source is a novelty/attribution defect.

**Evidence:** the identity, reconstructed: with $M=\sum_iw_iP_i$ every $P_i\ll M$, so
$$\sum_iw_i\int\log\frac{dP_i}{dR}dP_i=\sum_iw_i\int\log\frac{dP_i}{dM}dP_i+\int\log\frac{dM}{dR}\,d\!\left(\sum_iw_iP_i\right)=\sum_iw_i\KL(P_i\Vert M)+\KL(M\Vert R),$$
valid in $[0,+\infty]$ with the stated support conventions. Primary sources: R. Sibson,
"Information radius", *Zeitschrift für Wahrscheinlichkeitstheorie und verwandte Gebiete* 14
(1969) 149–160, which introduces $K_\alpha$ and identifies the $\alpha=1$ minimizer as the
weighted mixture; the same decomposition is standard as the "compensation identity" in
Topsøe's information-theoretic optimization work. `grep -in "sibson\|information radius\|topsoe"
references.bib` returns no matches over its 466 entries.

**Falsifier:** an existing citation for this identity in `references.bib` or in the
derivation packages. I found none.

**Fix (smallest):** add "This is the compensation identity of \citet{Sibson1969}; the
Radon–Nikodym argument below is included for the extended-real support conventions" plus the
`.bib` entry.

---

### [Low] `thm:rg-strong-lumpability` is stated more restrictively than necessary and its selection caveat is misphrased

**Location:** `Theory/07b_agent_network_rg.tex:2098–2111`.

**Claim as stated:** "Conversely, if \eqref{eq:rg-strong-lumpability} holds and $c$ admits a
Borel right inverse $\varsigma:\mathsf Z\to\mathsf Y$ with $c\circ\varsigma=\operatorname{id}$,
then \eqref{eq:rg-lumped-kernel-formula} is a Markov kernel ... Without a measurable
selection, \eqref{eq:rg-lumped-kernel-formula} still defines the coarse transition on the
range of $c$ and the selection must be declared separately."

**Defect:** (i) $c$ is assumed *surjective* in the theorem's hypotheses (line 2084), so "the
range of $c$" is all of $\mathsf Z$ and the caveat as written is vacuous; the real obstruction
is measurability of $z\mapsto T(\varsigma(z),c^{-1}B)$, not the domain. (ii) The *Borel*
right-inverse hypothesis is stronger than needed: by Jankov–von Neumann uniformization (Kechris,
*Classical Descriptive Set Theory*, Theorem 18.1), every Borel surjection between standard
Borel spaces admits a $\sigma(\boldsymbol\Sigma^1_1)$-measurable, hence universally
measurable, right inverse. So $T^c$ always exists as a universally measurable kernel; only
Borel-measurability of $T^c$ requires the stronger selection. The theorem as stated therefore
under-delivers.

The mathematics of the theorem is otherwise correct. I verified both directions (the
$\mu=\delta_y$ argument and the converse computation) and the weak-lumpability witness at
2145–2155: with $\mathsf Y=\{1,2,3\}$, $c(1)=c(2)=a$, $c(3)=\beta$, $T(1,\cdot)=\delta_3$,
$T(2,\cdot)=\tfrac12(\delta_1+\delta_2)$, $T(3,\cdot)=\tfrac12(\delta_1+\delta_3)$, we get
$T(1,\{1,2\})=0\neq1=T(2,\{1,2\})$ so strong lumpability fails, while from $\delta_3$ the
chain stays in $\{1,3\}$, on which $c$ is injective, giving the stated coarse chain
$a\mapsto\beta$ surely and $\beta\mapsto a$ or $\beta$ with probability $\tfrac12$. The
attribution to \citet[Ch.~6]{KemenySnell1976} at the finite-state scope is correct.

**Falsifier:** a reason the Jankov–von Neumann section is unusable here (e.g. if the intended
$T^c$ must be Borel rather than universally measurable for downstream use — but the chapter
does not say so).

**Fix (smallest):** replace the last sentence with "Without a Borel selection, Jankov–von
Neumann uniformization still supplies a universally measurable right inverse and hence a
universally measurable $T^c$; a Borel version requires the declared Borel selection."

---

### [Low] The guide's counterexample register was not updated for the 8/15 release

**Location:** `solid_RG_theory.md:311–326` (§10, "Eight shortcut failures"); compare §11
line 330 and `docs/derivations/2026-08-15-full-pointwise-meta-agent/final-report.md`.

**Claim as stated:** §10 heading "Eight shortcut failures"; §326 "See
[counterexample-proofs.md](docs/derivations/2026-08-14-pointwise-meta-agent-rg/evidence/counterexample-proofs.md)."

**Defect:** the 8/15 diff changed §11's ESTABLISHED list from "the eight counterexamples" to
"the released counterexamples", but §10 — the only place the guide actually exhibits negative
results — still says "Eight", still contains exactly the eight 8/14 rows, and still points only
at the 8/14 register. The 8/15 package reports five further exact finite negative constructions
("failure of full-law reconstruction from marginals, unconditional split-channel VFE,
model-marginal-only evaluator compatibility, agreement from trivial holonomy, and joint
invariance from marginal invariance"), of which at least three (split-channel VFE,
evaluator-compatibility from the model marginal, joint invariance from marginal invariance) are
new and are not surfaced anywhere in the document that calls itself the "sole human-facing
pointwise guide". The two most RG-relevant new negatives — that marginal invariance does not
give joint invariance, and that a split channel breaks the VFE identity — are exactly the
shortcuts an RG reader would take.

**Evidence:** `solid_RG_theory.md:311` "## 10. Eight shortcut failures"; the table at
315–324 has eight rows; line 326 cites only the 8/14 register. `find` on
`docs/derivations/2026-08-15-full-pointwise-meta-agent/` shows a separate
`counterexample-register.md` (63 lines) and `evidence/counterexample-proofs.md` (222 lines)
that the guide never links.

**Falsifier:** a link from `solid_RG_theory.md` to the 8/15 counterexample register. There is
none; the repository map at 338–345 links the 8/15 package only as a whole.

**Fix (smallest):** retitle §10 "Shortcut failures", append the five 8/15 rows, and add the
8/15 `counterexample-proofs.md` link beside the 8/14 one.

---

## Claims that CHECK OUT (verified, no finding)

These were load-bearing and I reconstructed them rather than accepting them.

1. **KL/VFE contraction has the channel on the correct side and the correct inequality
   direction.** `thm:cg-kl-dpi-extended` (`Theory/06_general_coarsegraining.tex:65–82`)
   states $\KL(PK\Vert QK)\leq\KL(P\Vert Q)$ in $[0,+\infty]$ with no absolute-continuity
   hypothesis; the proof's use of the *shifted* generator $\phi_0(t)=t\log t-t+1$ (nonnegative
   and convex) is exactly the right device to make conditional Jensen and monotone
   approximation legitimate in the extended case without rearranging a signed integral. The
   equality condition in `thm:cg-dpi-equality` and the pairwise Bayes-recovery corollary are
   correct, and `cor:cg-dpi-infinite-equality-warning` supplies a valid three-point witness
   that $+\infty=+\infty$ carries no recovery conclusion. Attribution to
   \citet{Kullback1951,Csiszar1967} is appropriate.

2. **The new chain rule `eq:rg-pointwise-parent-kl-chain` is exactly right, including the
   measure the defect is averaged against.** The defect is integrated against
   $\mathbb Q_{A,o,X}$ (the *recognition* pushforward), which is the correct side; averaging
   against $\boldsymbol\Pi_{A,o,X}$ breaks the identity. Verified numerically to machine
   precision on randomized 6-point/3-point channels:
   ```
   trial 0: KL_fine=1.202234289383  KL_coarse=0.110817750412  defect=1.091416538971  diff=-2.220e-16
   trial 1: KL_fine=0.313743587857  KL_coarse=0.017307309882  defect=0.296436277975  diff= 0.000e+00
   ... (5/5 exact; contraction KL_coarse <= KL_fine held in all trials)
   control: KL_fine=0.275183120270  KL_coarse+defect(Q_A)=0.275183120270  KL_coarse+defect(Pi_A)=0.245790786276
   ```
   Consequently $\Fenergy_I\geq\Fenergy_A$ and the coarse ELBO is nondecreasing — the
   direction asserted at `07b:2878–2883` is correct, and the accompanying warning that this
   "is information loss under resolution, not a proof of approach to a nontrivial critical
   fixed point" is the right caveat (the terminal channel drives the monotone to zero
   immediately, so it is not a nontrivial RG monotone; 07b acknowledges the terminal channel
   at 2858–2859).

3. **The parent posterior identity added to `Theory/06` is correct.** With
   $\mathbb P_A(do,dz)=\mathbb P^O_I(do)(\boldsymbol\Pi_{I,o,X}C_A)(dz)$, the displayed
   test-function identity (`06:326–332`) is precisely the defining property of the selected
   parent posterior version. The added paragraph is a genuine specialization, and it says so
   ("This is a typed specialization of the preceding theorem, not a second
   posterior-pushforward theorem").

4. **The two scale notions in question 5 are explicitly distinguished, not silently
   identified.** `def:rg-scale-connection` (`07b:2496–2532`) separates the scale connection
   $\nabla^{\mathrm{scale}}$ on $\mathscr G\to S$ from the contextual principal connections
   $\omega_b,\omega_m$ on $\mathscr P_\ell\to\mathcal C_\ell$ ("the former has base $S$ and
   compares coupling fibers at different resolutions, the latter have base $\mathcal C_\ell$
   at one fixed resolution") and from the inference-orbit parameter and Fisher duration, and
   closes with "Nothing is proved by this declaration. \status{DEFINITION}".
   `prop:rg-continuous-beta-underdetermined` (2572–2610) then *proves* that discrete blocking
   does not determine the continuous beta. I verified the witness: with
   $f(s)=e^{\epsilon\sin2\pi s}$, $\mathsf V^{(\epsilon)}(s,t)=f(s)/f(t)$ satisfies the
   two-parameter cocycle law and $\mathsf V(t,t)=1$ by inspection, equals $1$ at all integer
   pairs, and has generator $\partial_s\mathsf V|_{s=t}=2\pi\epsilon\cos(2\pi t)\not\equiv0$.
   Correct. This is the one place where the manuscript is genuinely more careful than the
   surrounding literature usually is.

5. **The RG machinery in `Theory/07b` does not depend on the pointwise theorem, and the
   pointwise theorem does not depend on the RG machinery.** `grep -rn
   "rg-pointwise-parent-datum"` shows the new theorem is cited only by
   `Theory/06_general_coarsegraining.tex:331` and `Theory/appendix_claim_ledger.tex:191,222`.
   No beta function, fixed-point equation, or scaling operator in §§`sec:rg-beta-function`,
   `sec:rg-fixed-points` is derived from it. So the specific failure mode question 2 asks
   about — the RG story written as if the meta-agent construction supports it — does **not**
   occur inside `Theory/07b`. It occurs only at the level of the guide's title and framing,
   which is finding 1.

6. **`prop:rg-retained-beta-residual` and the projected-fixed-point witness are correct.**
   $\delta\beta_\ell(g)=(I-\widehat R_{\ell+1})\widehat T^{\mathcal G}_\ell(g)/\Delta s_\ell$
   follows by subtraction as claimed, and the $\mathbb R^2$ witness $R(x,y)=(x,0)$,
   $T(x,y)=(x,x)$ does give $\beta^{\mathrm{ret}}\equiv0$ on the retained line while
   $\beta^{\mathrm{ex}}(x,0)=(0,x)\neq0$ for $x\neq0$. The stated moral — "A projected fixed
   point is not an exact fixed point" — is right and is the correct RG hygiene point.
   `prop:rg-fixed-object-nonimplication` (2805–2840) similarly checks out clause by clause;
   the monodromy witness $F_0(x)=x+1$, $F_1(x)=x-1$ on $\mathbb R$ is correct.

7. **§5's total-variation control is correct.** From $\mathcal D_x\leq\varepsilon_x$ and
   nonnegativity of every term, each selected tree edge obeys
   $\KL\leq\varepsilon_x/\eta^x_{\min}$, so Pinsker gives
   $\TV\leq\sqrt{\varepsilon_x/(2\eta^x_{\min})}=\delta_x$; TV is invariant under the
   bimeasurable bijections $T^x_{ij}$, and the triangle inequality along a tree path of length
   $\leq d_x$ gives $\TV(P^x_u,P^x_v)\leq d_x\delta_x$, with convexity of TV in its second
   argument giving the mixture bound. The disclaimer "No KL triangle inequality is used or
   claimed" is accurate and appropriate.

8. **The 8/15 diff to `Theory/06a_generative_gaussian.tex` is notation only** (3 lines:
   $P\to\mathscr P_G$ for the principal bundle). No mathematical content changed. No finding.

9. **`Theory/07b` does contain one genuine, correct, inhabited relevance spectrum.** This is
   the most important honest counterweight to finding 1.
   `thm:rg-gaussian-hermite-spectrum` (983–1058) computes the block-sum operator
   $\mathscr L_b=U_b\mathscr I_b$ on $L^2_0(\gamma)$ and gets
   $\mathscr L_be_k=b^{1-k/2}e_k$; `def:rg-hermite-relevance` (1060–1071) reads off
   $y_k=1-k/2$, so degree 1 is relevant ($y_1=\tfrac12$), degree 2 marginal ($y_2=0$),
   degree $k\geq3$ irrelevant. I checked every step. For jointly standard Gaussian $(X_i,Z)$
   with $\rho=\operatorname{Cov}(X_i,Z)=b^{-1/2}$, the Mehler regression identity
   $\E[\mathrm{He}_k(X_i)\mid Z]=\rho^k\mathrm{He}_k(Z)=b^{-k/2}\mathrm{He}_k(Z)$ is correct,
   and summing over $b$ replicas gives $b^{1-k/2}$. The Hilbert–Schmidt sum
   $\sum_{k\geq1}b^{2-k}=b^2/(b-1)$ is correct, the norm/spectral radius $\sqrt b$ is correct,
   and the continuous-spectrum argument is correct: the witness
   $y=\sum_{k\geq1}b^{1-k/2}e_k$ is square-summable while any preimage would have all Hermite
   coefficients $1$, so the range is dense and not closed, putting $0$ in the continuous
   spectrum of an injective compact operator. These are the classical CLT/Gaussian-fixed-point
   exponents. The chapter's insistence that "Relevance in this theory is therefore a joint
   property of the operator, the extensive normalization, the declared norms, and the block
   scale" (1080–1082) is the correct and often-elided caveat.
   So: the RG in `Theory/07b` is real for the classical Gaussian sector. What is absent is any
   instance for the *agent-network* coarse channel the program is actually about — that is
   finding 6 — and `solid_RG_theory.md` reproduces none of this material.

10. **The 8/15 additions to `Theory/appendix_claim_ledger.tex` do not overclaim in the RG
    section.** The new "Downstream comparison, gluing, and agency (open)" entry is correctly
    `\status{OPEN}` and correctly states that none of its members lies in the static release
    ancestry; the amended "Partition selection and experiment-level recovery (open)" entry
    correctly keeps the common recovery kernel and the partition selector open. No finding.

## Direct answers to the five questions

1. **Is `solid_RG_theory.md` a solid RG theory?** No. It is a solid *coarse-graining*
   document with an RG title. There is no semigroup (only Markov-kernel functoriality, which
   every channel has), no scale parameter, no rescaling/identification kernel, no flow, no RG
   fixed point, and no relevant/irrelevant classification. The RG language in that file is
   decorative. Finding 1. The RG machinery that *does* exist is in `Theory/07` and
   `Theory/07b`, is largely careful, and is not what `solid_RG_theory.md` describes.

2. **Does the RG story depend on what the pointwise theorem disclaims?** Inside
   `Theory/07b`, no — the beta/fixed-point apparatus is logically independent of the new
   theorem (check-out 5), and 07b explicitly requires the additional data (the $I_b$
   identification, `eq:rg-kernel-semigroup`, nested-tree compatibility) that the pointwise
   theorem does not supply. At the level of `solid_RG_theory.md`, yes: the file is titled and
   framed as renormalization while its content is one pointwise, non-composable,
   non-canonical channel. That framing gap is finding 1; the specific composability defect is
   finding 3.

3. **The +153/+29 line additions.** `Theory/07b` gained (i) `thm:rg-pointwise-parent-datum`
   (lines 76–185, 110 lines) — **asserted, not proved**, no proof paragraph and no pointer,
   uniquely among the file's 27 results (finding 2), though every clause is true; (ii) the
   "Full-law holonomy alternatives" paragraph (1787–1809, 23 lines) — asserted by
   "substitution", which I verified is genuinely a one-line equivariance computation, so the
   ESTABLISHED label is defensible; (iii) `open:rg-pointwise-parent-dynamics` (2164–2178,
   15 lines) — correctly labeled `\status{OPEN}` and correctly identifies semigroup
   intertwining, not just a generator identity, as the exact Markov condition. `Theory/06`
   gained a 29-line "Pointwise parent specialization" paragraph that *is* derived (a
   test-function computation) and correctly labels itself a specialization.

4. **KL/VFE structure.** Yes, and the direction is correct. The channel is applied to both
   arguments (recognition and posterior), giving DPI contraction with an exact nonnegative
   defect; the defect is averaged against the correct measure. Verified analytically and
   numerically (check-outs 1–2). No finding.

5. **Same scale?** No conflation found in the manuscript. `07b:2525–2531` explicitly
   distinguishes the coupling-bundle scale $S$ from the contextual base
   $\mathcal C_\ell$ from the inference-orbit parameter, and
   `prop:rg-continuous-beta-underdetermined` proves the discrete and continuous scales are not
   determined by one another (check-out 4). Two residual problems: the *symbol*
   $\mathcal C_\bullet$ carries agent index in one place and scale index in another with no
   registry disambiguation (finding 5), and `solid_RG_theory.md` never states that its
   coarse-graining runs in the fiber at fixed base point while `07_general`'s scale arrows
   coarse-grain the base through $c_\ell:\mathcal C_\ell\to\mathcal C_{\ell+1}$ (folded into
   finding 1).

---

## Coverage

**Read in full (every line):**

- `solid_RG_theory.md` — 400 lines, complete.
- `git diff 060f80e^ 8ce6358 -- solid_RG_theory.md` — complete (+96/-26).
- `git diff 060f80e^ 8ce6358 -- Theory/07b_agent_network_rg.tex` — complete (+153, three
  blocks: `thm:rg-pointwise-parent-datum` at 76–185; "Full-law holonomy alternatives" at
  1787–1809; `open:rg-pointwise-parent-dynamics` at 2164–2178).
- `git diff 060f80e^ 8ce6358 -- Theory/06_general_coarsegraining.tex` — complete (+29, the
  "Pointwise parent specialization" paragraph at 304–332).
- `git diff 060f80e^ 8ce6358 -- Theory/06a_generative_gaussian.tex` — complete (+3/-3,
  $P\to\mathscr P_G$ only).
- `git diff 060f80e^ 8ce6358 -- Theory/appendix_claim_ledger.tex` — complete (+140/-33).
- `Theory/07b_agent_network_rg.tex` lines 1–200, 983–1120, 1680–1960, 2040–2300, 2300–2981 —
  i.e. all of §§ law-level VFE, gauge-covariant cross-scale operators, meta-attention,
  path-space/lumpability, RG transformation and beta functions, fixed points and scaling
  operators, and the closure theorem.
- `Theory/06_general_coarsegraining.tex` lines 55–170 (KL contraction/equality/recovery) and
  560–650 (holonomy-conditioned marginal-law mode).
- `Theory/07_general_renormalization.tex` lines 100–320 (measure-pair arrow, geometric RG
  state, scale-change typing, scale functor).
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/final-report.md` and
  `evidence/notation-standard.md`.
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation_scan.py` — the
  `_hazards` and `scan_active_sources` functions in full, plus the function index.

**Sampled (targeted greps and section reads, not line-by-line):**

- `Theory/07b_agent_network_rg.tex` lines 200–980 and 1120–1680 (effective action, bounded
  action calculus, DQM/Fisher sector, essential-spectrum and interaction-coordinate sections).
  I read the theorem statements and status labels via the environment index and read
  `thm:rg-gaussian-hermite-spectrum` and `def:rg-hermite-relevance` in full; I did not verify
  the DQM/score-lift or Hoeffding-assembly proofs line by line.
- `docs/derivations/2026-08-14-pointwise-meta-agent-rg/` — `direct-derivation.md`,
  `independent-reconstruction.md`, `adversarial-attacks.md`, `counterexample-proofs.md`
  targeted at the membership-kernel and marked-closure material only.
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/counterexample-register.md` (CE-1
  through CE-5 headers).
- `Theory/09_coarsegraining.tex`, `Theory/10_renormalization.tex` — grepped for barycenter and
  hard-partition material; not read.
- `references.bib` — grepped for the relevant primary sources; not read.

**Did not reach:**

- `Theory/05d_relational_inference.tex` (+326 lines in the 8/15 diff) — outside RG scope,
  and the largest single content change in the diff. Another reviewer should cover it.
- `Theory/SPEC.md` (+150), `Theory/appendix_notation.tex` (+90), `overview.md` (+182),
  `docs/STATUS.md` (+101), `docs/change-logs/2026-08-15.md`, the research-plan and design
  documents.
- The 8/15 package's `adversarial-attacks.md`, `direct-derivation.md`,
  `independent-reconstruction.md`, `oracle-erasure.md`, `claim-ledger.json`,
  `adversarial-report.json`, and the four internal domain reviews. Per the mandate I treated
  none of these as evidence; I also did not audit them, so nothing here should be read as
  clearing them.
- `evidence/finite_nongaussian_witness.py` and `evidence/recompute.py` were not executed.

**Computations I actually ran:** one scratch script verifying the KL chain rule
`eq:rg-pointwise-parent-kl-chain` on randomized 6-point/3-point channels (5/5 exact to
$\sim10^{-16}$, contraction held in all trials) plus a control showing the identity fails when
the defect is averaged against $\boldsymbol\Pi_A$ instead of $\mathbb Q_{A,o,X}$. Output quoted
in check-out 2. Everything else was reconstructed by hand: the compensation identity, the
Pinsker/tree TV chain, the Mehler regression eigenvalues, the lumpability biconditional and its
weak-lumpability witness, the $\mathcal R_{b_1b_2}=\mathcal R_{b_2}\mathcal R_{b_1}$ ordering,
the linear cross-scale composition under `eq:rg-linear-nested-compatibility`, the
root-gauge non-composition counterexample in finding 3, and the two-parameter cocycle witness
in `prop:rg-continuous-beta-underdetermined`.
