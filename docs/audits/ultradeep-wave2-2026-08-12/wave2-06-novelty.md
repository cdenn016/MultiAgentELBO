# Wave 2 / Report 06 — Priority and novelty audit

Date: 2026-08-11. Scope: `MultiAgentELBO/Theory/` + `Research/manuscripts/PIFB2.tex`.
Method: web + arXiv search, retrieved abstracts/full text where cited. CPU only; no GPU/CUDA job started.
The arXiv Atom API returned HTTP 403 from the sandbox (both with and without a User-Agent header), so all
arXiv checks were done through `WebSearch` and direct `arxiv.org/abs/` fetches instead. One `web_fetch`
call was lost to a 429 rate limit (`arxiv.org/a/search`); its query was re-run through `WebSearch`.

---

## 0. The single most important finding, first

**The author has already publicly disclosed the headline construction, and neither manuscript cites it.**

> Robert C. Dennis, *Epistemic Gauge Theory: Emergence of U(1) Interactions from Agent Based Inference
> Dynamics*, Preprints.org 202505.1773.v1, 23 May 2025. DOI `10.20944/preprints202505.1773.v1`.

Its abstract, verbatim: *"agent qualia and perceptions can be represented by **pullbacks of geometric
quantities** unique to each agent. Agents are constructed as pairs of **local sections of associated
bundles** $E_i$ to a **principal $G$-bundle** $N$ composed of a **base manifold** $C$ and Lie group $G$.
Agents interact via **induced connections** and evolve according to a **generalized variational energy**."*

That is the project's stated goal sentence, in public, dated 2025-05-23. `grep -rn "preprints.org|20944|Epistemic Gauge Theory"` over
`Theory/`, `references.bib`, and the whole `Research/` vault returns **zero hits**.

Consequences, all of which are fixable in an afternoon but none of which are optional:

1. Every novelty claim in `Theory/` has a **priority date of May 2025, not 2026**, and must be phrased
   relative to Dennis (2025), not absolutely.
2. A referee who finds this and sees it uncited will read it as concealment rather than oversight. Self-plagiarism
   and duplicate-submission checks at most venues search preprint servers.
3. It also *helps*: it establishes the author's own priority over the construction against any third party,
   and it gives `Theory/` a clean framing — "the 2025 preprint asserted these pullbacks; this paper constructs
   them rigorously, and finds that three of the assertions are false as stated." That is a much stronger
   paper than "here is a new idea."

---

## 1. Priority table

| # | Construction (file:line) | Prior art found? | Citation | Verdict |
|---|---|---|---|---|
| **N1a** | Fisher + Amari–Chentsov as **pullbacks** of canonical tensors along a map from a parameter manifold (`05c:70-130`) | **Yes — this is the definition in the field** | Ay, Jost, Lê, Schwachhöfer, *Parametrized measure models*, **Bernoulli 24(3):1692–1725 (2018)**, arXiv:1510.07305 — abstract: *"a natural definition of the Fisher metric and the Amari-Chentsov tensor as the pullback of tensors defined on the space of roots of measures"* | **STANDARD.** Already `AyJostLeSchwachhoefer2018` in the bib, cited twice. The word "pullback" carries no novelty. |
| **N1b** | Pulling a **fiber metric** back through $D^\omega s=\mathrm{ver}^\omega\!\circ Ts$, the connection-split vertical jet of a section of a **nonlinear** associated bundle (`05c:89-124`, `eq:pb-covariant-first-jet`) | **Yes** | C. M. Wood, *Harmonic sections of homogeneous fibre bundles*, **Diff. Geom. Appl. 19(2):193–210 (2003)** — the *vertical energy* $\int\lVert\mathrm{ver}\circ d\sigma\rVert^2$ is exactly $\mathrm{tr}_g h_s^\omega$. Same object appears throughout gauged sigma models / Yang–Mills–Higgs (Mundet i Riera; Cieliebak–Gaio–Salamon symplectic vortices). | **STANDARD.** $h_s^\omega$ is the gauged-harmonic-map energy density tensor. Uncited. |
| **N1c** | Base manifold carrying a **field of statistical manifolds** with Fisher-Rao fibers, section = belief field | **Yes — the ungauged case is an active ML programme** | Cai, Savarino, Schnörr et al., *Sigma Flows for Image and Data Labeling and Learning Structured Prediction*, **arXiv:2408.15946**, JMIV 2025 — *"a harmonic map from a closed Riemannian domain manifold to a statistical manifold, equipped with the Fisher-Rao metric"*. Discrete precursor: Åström–Petra–Schmitzer–Schnörr assignment flow (JMIV 2017), a product of Fisher-Rao simplices over a pixel base. Axiomatic precursor: Lebanon, *An Extended Čencov–Campbell Characterization of Conditional Information Geometry*, UAI 2004 / arXiv:1207.4139 (Fisher geometry on a fiberwise product of simplices over an input space). | **GENERALIZES.** The gauged version (principal connection $\Rightarrow$ vertical projection) is the increment; the field-of-Fisher-fibers is not. All uncited. |
| **N1d** | Terminology: "statistical bundle" | **Name is taken, object is different** | Pistone & Sempi, *Ann. Statist.* 23(5):1543–1561 (1995); Pistone, *Lagrangian Function on the Finite State Space Statistical Bundle*, **Entropy 20(2):139 (2018)**; Chirco–Malagò–Pistone, IJGMMP 19(13):2250214 (2022). Pistone's *statistical bundle* is a **vector bundle over the statistical manifold** with fiber $\{v: \mathbb{E}_p[v]=0\}$ (Orlicz/$L^2_0$) — the score/velocity space. | **DOES NOT ANTICIPATE**, but the collision is real. All three entries are **already in `references.bib` and cited zero times in `Theory/`.** Add one sentence distinguishing the two, or a referee will assume confusion. |
| **N1e** | **Horizontal-defect cocycle**: $A_\Psi(e;X)=T\Psi(H^{\omega_0}X)-H^{\omega_1}(Tf X)$, `thm:pb-anomaly-composition` (`05c:979`), `thm:pb-fisher-defect-cocycle` (`05c:1230`), `thm:pb-base-defect-cocycle` with exact residual + sign-convention criterion (`05c:1267`) | **No prior art found** | — | **NOVEL.** Searches run below (§4). This is the surviving core of N1. |
| **N2** | `thm:obs-local-global-potential` (`05b:347`): $\mathcal F(Q')-\mathcal F(Q)=\mathbb E_{Q_{B^c}}[\mathcal F_B(r'_B)-\mathcal F_B(r_B)]$ for **correlated** $Q=Q_{B^c}r_B$ | **Yes** | The exact-potential property of **blocked / structured coordinate-ascent VI**: Saul & Jordan, *Exploiting tractable substructures in intractable networks*, NIPS 1995; Jordan, Ghahramani, Jaakkola & Saul, *An introduction to variational methods for graphical models*, **Mach. Learn. 37:183–233 (1999)**; Wainwright & Jordan, *FnT ML* 1(1–2) (2008) §5; Hoffman & Blei, *Structured stochastic variational inference*, AISTATS 2015. All four families already in the bib (`Wainwright2008`, `Blei2017`, `Hoffman2015`). | **REDISCOVERS**, in greater measure-theoretic generality. **Not Bethe/Kikuchi** — see §2. |
| **N2′** | `eq:obs-global-ledger` (`05b:441`): $\mathcal F=\mathrm{TC}(Q)+\sum_i\mathrm{KL}(Q_i\Vert\rho_i)+\mathbb E_Q\sum_a E_{a,o}$ | **Yes** | Total-correlation chain rule; Watanabe, *IBM J. Res. Dev.* 4:66–82 (1960). Not a counting-number/region-graph identity. | **STANDARD.** |
| **N3a** | `prop:obs-declared-root-unavoidable` (`11:239`): every finite DAG has a parentless node | **Yes — textbook** | Existence of a topological order in a finite DAG (Kahn, CACM 5(11), 1962). In graphical-model form: the recursive factorization, Lauritzen, *Graphical Models* (1996) §3 — **already cited twice in `Theory/`**. | **STANDARD.** One-line graph fact presented as a Proposition + Proof. Demote to a Remark. |
| **N3b** | `cor:obs-flat-fold-singular` — flat unanchored reciprocal Gaussian fold is singular (`11:20-107`) | **Yes** | Besag, JRSS-B 36(2):192–236 (1974); **Besag & Kooperberg, *On conditional and intrinsic autoregressions*, Biometrika 82(4):733–746 (1995)**; Rue & Held, *Gaussian Markov Random Fields* (2005) Ch. 3. Pairwise-difference precision matrices are only PSD; the joint is improper (IGMRF/ICAR). | **REDISCOVERS** the IGMRF impropriety fact. The *application* to the Ouroboros fold is new; the linear algebra is not. |
| **N3c** | No joint generative model consistent with pairwise variational couplings (`05b:389` remark; ch. 11 framing) | **Yes — a whole literature** | Arnold & Press, *JASA* 84:152–156 (1989); Gelman & Speed, *Characterizing a joint probability distribution by conditionals*, **JRSS-B 55(1):185–188 (1993)**; Arnold, Castillo & Sarabia, *Conditional Specification of Statistical Models* (Springer 1999); Wang & Kuo, *Statist. Sinica* 20:423–440 (2010). | **REDISCOVERS.** Zero of these are in the bib. The manuscript's remark is correct and is the standard incompatible-conditionals phenomenon. |
| **N3d** | `prop:obs-normalizer-link-dependence` (`11:120`) + `prop:obs-holonomy-determinant-factorization` (`11:355`): the Gaussian global normalizer's dependence on the model graph link **factors through holonomy** | **No prior art found** | — | **NOVEL.** The strongest thing in chapter 11, and it is not the proposition the audit foregrounded. |
| **N3e** | Impossibility results for gauge-covariant consensus / equivariant barycenters | **Nearest existing result, different theorem** | Dym, Lawrence & Siegel, *Equivariant Frames and the Impossibility of Continuous Canonicalization*, **arXiv:2402.16077**, ICML 2024 — no continuous equivariant frame/canonicalization for common groups. | **DIFFERENT**, but the nearest neighbour in the equivariance literature and the obvious "related no-go" citation. `cor:cg-compact-holonomy-barycenter` (`09:700`) — the Haar-constrained barycenter, with the holonomy constraint active even at zero pairwise disagreement — has **no prior art found** and is the genuine result here. |
| **R1** | Fields of fibers with transport (`02_geometry.tex`, whole chapter) | **Yes — this is exactly their framework** | Cohen, Weiler, Kicanaoglu, Welling, *Gauge Equivariant Convolutional Networks and the Icosahedral CNN*, **ICML 2019, PMLR 97:1321–1330**, arXiv:1902.04615. Weiler, Forré, Verlinde, Welling, *Coordinate Independent Convolutional Networks — Isometry and Gauge Equivariant Convolutions on Riemannian Manifolds*, **arXiv:2106.06020** (2021); book, World Scientific (2023). | **STANDARD.** See §3 for the line-by-line comparison. Damage: **HIGH.** |
| **R2** | `prop:cg-markov-category` (`06:28`) | **Yes — textbook** | Lawvere, *The category of probabilistic mappings* (1962, unpublished); **Giry, *A categorical approach to probability theory*, LNM 915:68–85 (1982)**; Panangaden, *The category of Markov kernels*, ENTCS 22 (1999). Modern synthetic account: **Fritz, *A synthetic approach to Markov kernels, conditional independence and theorems on sufficient statistics*, Adv. Math. 370:107239 (2020), arXiv:1908.07021**; Cho & Jacobs, MSCS 29(7):938–971 (2019). | **STANDARD** (this is `BorelStoch`). Damage: **MODERATE.** See §3 for why the audit's "typed separation is a Markov-category argument" is *not* quite right. |
| **R3** | Fisher contraction under coarse-graining (`06`, `09`, `07b`) | **Yes — three distinct owners** | Čencov (1972; AMS transl. **1982**) owns invariance/uniqueness under Markov morphisms — **already cited, correctly, at `08:493`**. Ay–Jost–Lê–Schwachhöfer (2017 monograph; 2018 Bernoulli) own the general monotonicity formula — cited. **Bény & Osborne, *Information-geometric approach to the renormalization group*, Phys. Rev. A 92:022330 (2015), arXiv:1206.7004** own the RG-as-coarse-graining reading that chapters 6/9/07b actually use. | **STANDARD.** `beny2015information` is in the bib, **cited zero times**, while chapter 9 runs their framing. Damage: **HIGH.** |
| **R4** | `prop:cg-gaussian-forward-kl-barycenter` (`09:639`) | Yes, trivially | Moment matching / m-projection: Amari & Nagaoka (2000) §3 (cited 8×); Bishop (2006) §10.7 (cited 2×). | **STANDARD — and no novelty is claimed.** Verified: `grep -i "to our knowledge\|for the first time\|is novel\|appears to be new"` over all 24 TeX files returns **zero hits**, and the proposition is immediately followed by a `NOT-CLAIMED` disclaimer at `09:687`. **No action needed** beyond a parenthetical "(the standard moment-matching result)". Damage: **NONE.** |
| **R5** | Sengupta–Friston neuronal gauge theory | **Yes, and it is the named precursor** | Sengupta, Tozzi, Cooray, Douglas & Friston, *Towards a Neuronal Gauge Theory*, **PLoS Biology 14(3):e1002400 (2016)**, DOI 10.1371/journal.pbio.1002400. Technical companion: Sengupta & Friston, *Approximate Bayesian inference as a gauge theory*, **arXiv:1705.06614** (2017). | **DIFFERENT — and `Theory/` wins the comparison.** See §3. Damage of omission: **SEVERE.** |

---

## 2. N2 in detail: it is not Bethe/Kikuchi, and that matters

The audit suspected `thm:obs-local-global-potential` rediscovers a region-graph counting-number identity.
Having read both, that comparison is **wrong**, and it is worth being precise because the mis-comparison would
send the author to fix the wrong thing.

- **Bethe/Kikuchi region-graph free energies** (Yedidia, Freeman & Weiss, *Constructing free-energy
  approximations and generalized belief propagation algorithms*, IEEE Trans. IT 51(7):2282–2312, 2005 —
  `Yedidia2005`, in the bib, cited zero times) are **approximations**. Their structure is
  $F_{\text{region}}=\sum_R c_R F_R$ with counting numbers $c_R$ chosen so each variable and factor is counted
  once. They are exact only on trees / junction structures, and the "overcounting correction" is precisely the
  counting numbers.
- `thm:obs-local-global-potential` is **exact for arbitrary joints**, involves **no region decomposition, no
  counting numbers, and no approximation**. It is a two-term KL chain rule.

So it does not rediscover Yedidia–Freeman–Weiss. What it *does* rediscover is the exactness argument
underlying **blocked / structured coordinate-ascent VI**: the global free energy depends on the block
conditional $r_B$ only through the expected block-local free energy, which is exactly why block updates
monotonically decrease the global objective and why structured (non-mean-field) VI is legitimate. That is
Saul–Jordan (1995), Jordan–Ghahramani–Jaakkola–Saul (1999), Wainwright–Jordan (2008 §5), Hoffman–Blei (2015).

**What genuinely is an increment, and should be the claim:** the identity is stated for general standard Borel
spaces with $[0,+\infty]$-valued KL, using regular conditional versions, with *no* exponential family, *no*
mean field, and with the integrability side conditions that make the subtraction legal isolated explicitly
(`05b:347-360`). The textbook statements all assume finiteness or an exponential family. That is a
**careful-generality remark**, not a theorem. Publishable as a lemma inside a larger paper; not publishable as
a result.

The accompanying negative remark at `05b:389` — *"Independently replacing all correlated full conditionals
need not define any joint recognition law, so such a parallel prescription is not licensed"* — is correct and
is the **incompatible-conditionals** phenomenon (Arnold–Press 1989; Gelman–Speed 1993). Citing that literature
there costs one line and converts a bare assertion into a connected result.

---

## 3. R1, R2, R5 in detail

### R1 — how close is `02_geometry.tex` to Cohen (2019) / Weiler (2021)?

Very close. Weiler et al.'s setup is: a manifold $M$; a principal $G$-bundle (usually the frame bundle);
associated **vector** bundles $P\times_\rho V$ for a representation $\rho$ ("feature fields"); gauge
transformations as changes of local frame; the requirement that layers be well-defined independently of local
trivialization; Čech-style transition functions between overlapping charts; and parallel transport by a
connection to compare fibers at different points.

Chapter 2 has, item for item: `def:geo-principal-systems` (`02:40`) = the principal bundle;
`def:geo-associated-bundles` (`02:120`) with the quotient convention $(u\cdot g,\beta)\sim(u,g\cdot\beta)$ =
the associated bundle; `sec:geo-frame-gauge` (`02:148`) = gauge transformations as frame change;
`def:geo-connections` (`02:282`) = the connection; `sec:geo-cech` (`02:485`) = the Čech cocycle;
`def:geo-graph-links` (`02:561`) = discretized transport.

**Two real differences.** (i) The fibers $\mathcal B_b,\mathcal B_m$ are **nonlinear statistical manifolds**,
so $\widehat\rho$ is a group *action*, not a representation, and the bundle is not a vector bundle. Weiler's
book treats general fibers, but essentially all of the ML literature uses vector fibers, and the
nonlinear-fiber case genuinely changes what "weight sharing" and "linearity of layers" can mean. (ii) The base
$\mathcal C$ is an abstract contextual base with no metric and no data on it, rather than a data domain.

**Neither difference is large enough to justify zero citations.** Chapter 2 will be read as Cohen/Weiler by
anyone in geometric deep learning, and the vault note `Research/wiki/themes/Gauge equivariance and geometric
deep learning.md` proves the author knows the literature. Fix: one paragraph in §2.1 saying "this is the
coordinate-independent-CNN setup of [Cohen 2019, Weiler 2021] with the associated-vector-bundle fiber replaced
by a statistical manifold; the consequences of nonlinearity are §5c." That paragraph *strengthens* the paper —
it converts a suspicious silence into a stated increment.

### R2 — is the typed coarse-operation separation a Markov-category argument?

Partly, and the audit slightly overstates it.

- `prop:cg-markov-category` itself (`06:28`) — "Markov kernels form a category, composition is associative,
  law-pushforward is functorial" — **is** the standard construction of `Stoch`/`BorelStoch`, due to Lawvere
  (1962) and Giry (1982). Proving it from scratch with a Tonelli argument and no citation reads as
  unawareness. Demote to a cited remark.
- The **typed separation** (normalized Markov channel vs. energy precomposition needing a new reference
  measure vs. Galerkin restriction needing a reference form) is **not** Markov-category content. Fritz's
  Markov categories axiomatize copy/discard, conditionals, a.s.-equality, sufficient statistics — not the
  distinction between measure-pushforward and energy-precomposition. The audit's phrasing here should not be
  propagated.
- Where the manuscript **does** overlap Fritz is `thm:cg-kl-dpi-extended` and the KL equality/recovery results
  in `sec:cg-kl-recovery`: sufficiency, Fisher–Neyman, and the equality-in-DPI characterization are Fritz
  (2020) §11–§13 in synthetic form. That is the honest cite.

### R5 — exactly how `Theory/` differs from Sengupta–Friston (2016)

I read the full PLoS Biology text and the arXiv:1705.06614 abstract. Sengupta et al. is a **programmatic
essay**, not a construction. Its actual content:

1. Lagrangian $=$ variational free energy / sensory entropy.
2. The "manifold" is the space of **sufficient statistics of one agent's recognition density**, carrying the
   Fisher information metric (they invoke Čencov's theorem by name for this).
3. The "connection" they name is the **Levi-Civita connection of the Fisher metric on that belief manifold**:
   *"neuronal dynamics, in a local frame of reference, will (appear to) be subject to forces and drives (i.e.,
   Levi-Civita connections)."*
4. The "gauge field" is identified **informally with precision weighting**, whose cognitive homologue is
   **attention**: *"attention is a force that manifests from the curvature of information geometry."*
5. The invariance is over **symmetry groups of the generative model** that leave model evidence unchanged.
6. The 2017 companion's sole technical contribution is a **Schild's-ladder algorithm** for parallel transport
   of sufficient statistics.

What they do **not** have: no base manifold other than "the system"; no structure group; no principal bundle;
no associated bundle; no local sections; no Čech cocycle; no principal connection one-form; no curvature; no
multi-agent structure; and **no theorem**.

**The one-sentence difference a referee needs:** *Sengupta et al. place the geometry inside a single agent's
belief manifold and call the Levi-Civita connection of its Fisher metric a gauge field; we place a principal
$G$-connection on an external base of contexts and make the Fisher metric a fiber datum on an associated
bundle, so that the connection is exogenous to the statistics and the gauge group acts on frames rather than
on beliefs.*

Two further points, both in the author's favour and both worth stating:

- Sengupta et al.'s usage is arguably a **category error**: the Levi-Civita connection of a Riemannian metric
  is not a gauge field in the principal-bundle sense, and "gauge invariance" of free energy under
  reparametrization is ordinary diffeomorphism covariance, not local gauge symmetry. Saying this politely and
  precisely is the clearest possible justification for `Theory/` existing.
- But `Theory/`'s own gauge sector is currently **inert** (audit finding S3: zero curvature, connection absent
  from both free energies). Until that is fixed, `Theory/` is vulnerable to the mirror-image criticism. The
  Sengupta comparison and the curvature gap must be fixed together or not at all — writing the comparison
  while the connection still does not enter $\mathcal F$ invites the referee to make the point for you.

Four `Sengupta*` entries sit in `references.bib`, cited **zero** times. PIFB2 itself calls this "the closest
direct precursor." This is the first citation a referee will demand.

---

## 4. Negative-result log

So the negative results mean something, here is what was actually run. Searches were `WebSearch` unless noted;
arXiv Atom API returned 403 from the sandbox, so `abs:`-field searches were not available.

**For N1e (horizontal-defect cocycle) — no prior art found after:**
`"pullback Fisher-Rao metric section of fiber bundle base manifold principal connection"`;
`"bundle of statistical manifolds" OR "statistical manifold fiber" associated bundle Amari-Chentsov tensor pullback`;
`"gauge theory" "statistical manifold" fiber bundle Fisher information gauge transformation Matsuzoe`;
`gauged sigma model energy "covariant derivative of a section" associated fiber bundle nonlinear fiber metric pullback`;
`"harmonic sections" fibre bundle vertical energy Ehresmann connection C.M. Wood`;
`"pullback" "Amari-Chentsov tensor" OR "skewness tensor" cubic form induced on parameter manifold via map`;
`arxiv "statistical manifold" fiber "principal bundle" connection belief agent variational free energy sections 2024 2025`;
`gauge equivariant network nonlinear fiber associated bundle probability simplex statistical manifold fiber deep learning`.
Retrieved and read: AJLS *Parametrized measure models* abstract (arXiv:1510.07305); Wood *Harmonic sections of
homogeneous fibre bundles* (DGA 2003) summary; Schnörr et al. sigma flow (arXiv:2408.15946) summary.
Checked and **excluded** as non-anticipating: `Principal bundles over statistical manifolds` (arXiv:1403.4471 —
opposite direction, statistical manifold as *base*); Pistone's statistical bundle (§N1d); `Pullback Bundles and
the Geometry of Learning` (Entropy 25(10):1450, 2023 — pullback along a *learning map*, no Fisher fiber, no
principal connection).

**For N3d/N3e (holonomy-determinant factorization; holonomy-constrained barycenter) — no prior art found after:**
`impossibility theorem equivariant barycenter frame-independent aggregation consensus manifold no-go`;
`multi-agent active inference gauge theory fiber bundle sections variational free energy field over base manifold`.
The only impossibility result retrieved in the equivariance literature was Dym–Lawrence–Siegel (arXiv:2402.16077),
which is a different theorem.

**Searched and found positive** (so these are *not* negative results): AJLS pullback definition; Wood harmonic
sections; Schnörr sigma/assignment flow; Lebanon conditional information geometry; Fritz Markov categories;
Giry; Bény–Osborne; Bauer–Bruveris–Michor; Besag–Kooperberg IGMRF; Arnold–Press / Gelman–Speed;
Yedidia–Freeman–Weiss; Cohen 2019; Weiler 2021; Sengupta 2016/2017; Dennis 2025.

---

## 5. Missing-comparison list — what each would be cited FOR

| Work | Cited for |
|---|---|
| **Dennis, *Epistemic Gauge Theory*, Preprints.org 202505.1773.v1 (2025)** | The author's own prior public disclosure of the associated-bundle agent construction; establishes priority date and prevents a duplicate-disclosure finding. **Non-negotiable.** |
| **Sengupta, Tozzi, Cooray, Douglas & Friston, PLoS Biol. 14(3):e1002400 (2016)**; Sengupta & Friston, arXiv:1705.06614 (2017) | The named closest precursor: free-energy-as-gauge-theory as a programme. Cite to say what they proposed and what `Theory/` supplies that they did not. |
| **Cohen, Weiler, Kicanaoglu & Welling, ICML 2019 (arXiv:1902.04615)**; **Weiler, Forré, Verlinde & Welling, arXiv:2106.06020 / World Scientific 2023** | Chapter 2's entire setup. Cite as "we adopt their formalism with a nonlinear statistical fiber." |
| **Ay, Jost, Lê & Schwachhöfer, *Parametrized measure models*, Bernoulli 24(3) (2018)** | That Fisher and Amari–Chentsov are *defined* as pullbacks; establishes that N1's novelty is the connection, not the pullback. Already in bib. |
| **C. M. Wood, DGA 19(2):193–210 (2003)** (+ gauged sigma models: Mundet i Riera; Cieliebak–Gaio–Salamon) | That $\mathrm{ver}^\omega\!\circ Ts$ and the vertical energy are the standard harmonic-section objects; $h_s^\omega$ is a known construction with a Fisher fiber. |
| **Cai/Savarino/Schnörr, arXiv:2408.15946 (2024/2025)**; **Åström–Petra–Schmitzer–Schnörr, JMIV 58 (2017)** | The ungauged case: fields of Fisher-Rao statistical manifolds over a base, already an active ML programme. The nearest live competitor. |
| **Pistone & Sempi (1995); Pistone, Entropy 20(2):139 (2018); Chirco–Malagò–Pistone (2022)** | Terminological disambiguation of "statistical bundle." All three already in bib, cited zero times. |
| **Lebanon, UAI 2004 / arXiv:1207.4139** | Čencov–Campbell uniqueness for *conditional* models — i.e. for a fiberwise product of simplices over a base, which is the discrete shadow of the associated bundle. Justifies the fiber choice in the fibered setting. |
| **Bauer, Bruveris & Michor, Bull. LMS 48(3):499–506 (2016), arXiv:1411.5577** | Fisher–Rao uniqueness on the *infinite-dimensional* space of smooth densities under $\mathrm{Diff}(M)$. Needed because the manuscript's fibers are not finite simplices and `08:505` correctly notes Čencov/Campbell do not apply directly — this is the theorem that does. |
| **Čencov (1982)** | Already cited and **already used correctly** at `08:493-515`, with an honest statement of why it is not strong enough here. **The audit's claim that Chentsov is "currently unused" is false** — do not "fix" this. |
| **Jordan, Kinderlehrer & Otto, SIAM J. Math. Anal. 29(1):1–17 (1998)**; **Ambrosio, Gigli & Savaré, *Gradient Flows* (2005)**; **Villani, *Optimal Transport: Old and New* (2009)** | The referee's inevitable "why Fisher–Rao and not Wasserstein?" One paragraph: Fisher–Rao is the metric characterized by invariance under sufficient statistics (Čencov/AJLS/BBM) and is what a *statistical* fiber carries intrinsically; Wasserstein requires a metric on the sample space, which the noumenal base explicitly does not supply. That last clause is a genuinely good answer — use it. Also cite **Chizat–Peyré–Schmitzer–Vialard** WFR / unbalanced transport as the interpolating geometry. |
| **Amari, *Natural gradient works efficiently in learning*, Neural Comput. 10(2):251–276 (1998)** | Already cited (`Amari1998`, 2×). Verify it is cited at the point where $h_s^\omega$ is used as a preconditioner, since that is what natural gradient *is*. |
| **Ramstead, Sakthivadivel, Heins, Koudahl, Millidge, Da Costa, Klein & Friston, *On Bayesian mechanics*, Interface Focus 13(3):20220029 (2023), arXiv:2205.11543**; **Sakthivadivel, arXiv:2204.11900 (2022)**; **Da Costa, Friston, Heins & Pavliotis, *Bayesian mechanics for stationary processes*, Proc. R. Soc. A 477 (2021)**; **Parr, Pezzulo & Friston, *Active Inference* (MIT Press 2022)** | The FEP's own geometry, including Sakthivadivel's explicit gauge reading of self-organizing constraints. 8 `Ramstead`, 3 `Sakthivadivel`, 9 `Parr`, 1 `DaCosta`, 15 `Friston` entries in bib, **all cited zero times in `Theory/`.** |
| **Yedidia, Freeman & Weiss, IEEE Trans. IT 51(7) (2005)** | Cite to *distinguish*: the local–global identity is exact and counting-number-free, unlike region-graph approximations. Already in bib, uncited. |
| **Saul & Jordan (NIPS 1995); Jordan, Ghahramani, Jaakkola & Saul, Mach. Learn. 37 (1999)** | The correct attribution for `thm:obs-local-global-potential`. |
| **Arnold & Press, JASA 84 (1989); Gelman & Speed, JRSS-B 55(1) (1993); Arnold, Castillo & Sarabia (1999)** | The correct attribution for "independently replacing all correlated full conditionals need not define any joint." |
| **Besag & Kooperberg, Biometrika 82(4):733–746 (1995); Rue & Held (2005)** | The correct attribution for the singular unanchored pairwise Gaussian (IGMRF impropriety) in chapter 11. |
| **Fritz, Adv. Math. 370:107239 (2020), arXiv:1908.07021; Cho & Jacobs, MSCS 29(7) (2019); Giry, LNM 915 (1982)** | `prop:cg-markov-category` and the sufficiency/DPI-equality results in `sec:cg-kl-recovery`. |
| **Bény & Osborne, Phys. Rev. A 92:022330 (2015), arXiv:1206.7004** | The information-geometric RG framing that chapters 6/9/07b use. In bib, cited zero times. |
| **Dym, Lawrence & Siegel, arXiv:2402.16077, ICML 2024** | The nearest existing impossibility result in the equivariance literature; frames chapter 11's no-gos. |
| **Vaswani et al., NeurIPS 2017** | `prop:obs-attention-elbo` (`05b:547`) derives exact row softmax; in bib, cited zero times. |

---

## 6. Verdict

### 6.1 Which novelty claims survive, ranked by strength

1. **The horizontal-defect calculus** (`thm:pb-anomaly-composition` `05c:979`; `thm:pb-fisher-defect-cocycle`
   `05c:1230`; `thm:pb-base-defect-cocycle` `05c:1267`). No prior art found after the eight searches logged in
   §4. The vertical cocycle is unconditional (no connection, no section); the base cocycle has a closed-form
   residual and a sharp criterion; and the sign/convention theorem — that the coarse jet carries
   $+\Delta_F(A,A)$ and the pushed fine jet $-\Delta_F(A,A)$, so mixing conventions inflates the residual by
   exactly $2\Delta_F(A,A)$ — is the kind of result nobody states unless they had to derive it. **Strongest
   surviving claim.**
2. **Exact connection-dependence of the emergent base geometry** (`05c:156-232`), i.e. $h_s^\omega$ depends on
   $\omega$ exactly, with an explicit counterexample at `05c:220-232`, alongside *passive* gauge covariance
   (`thm:pb-pullback-gauge-invariance`) and the active-gauge counterexample at `05c:148-155` showing the two
   are not the same. This is a **negative result about the author's own framework** and is therefore very
   well defended. It is also the sharpest available critique of Sengupta–Friston.
3. **Holonomy factorization of the Gaussian normalizer** (`prop:obs-normalizer-link-dependence` `11:120`;
   `prop:obs-holonomy-determinant-factorization` `11:355`) and the **holonomy-constrained barycenter**
   (`cor:cg-compact-holonomy-barycenter` `09:700`), including the witness where the constraint is active with
   *zero* pairwise disagreement. No prior art found.
4. **`prop:obs-attention-elbo`** (`05b:547`) — exact row softmax from a latent source label inside a fixed
   joint, strictly stronger than PIFB2's mean-field ansatz. Not exhaustively searched in this pass; flagged as
   probably-novel and worth a dedicated check.
5. `thm:pb-pullback-rank-quotient` (`05c:321`) and `thm:pb-section-descent` (`05c:715`) — plausible but
   **not searched** in this pass. Do not claim until checked.

### 6.2 Which die, and the exact wording changes

| Currently | Change to |
|---|---|
| `thm:obs-local-global-potential` presented as a theorem (`05b:347`) | Retitle **"Block chain-rule identity for correlated recognition laws"** and open with: *"The following is the exactness property underlying blocked and structured coordinate-ascent variational inference [Saul & Jordan 1995; Jordan et al. 1999; Wainwright & Jordan 2008 §5]. We record it here in the generality required below — arbitrary standard Borel spaces, $[0,+\infty]$-valued divergences, regular conditional versions, and no exponential-family or mean-field assumption — and isolate the integrability conditions that license the subtraction."* Keep the proof; drop any implication of priority. |
| `prop:obs-declared-root-unavoidable` as a Proposition with Proof (`11:239`) | Demote to **Remark**: *"Every finite DAG admits a topological order, hence a parentless node whose marginal is declared [Lauritzen 1996, §3]. The ambition to eliminate the declared root is therefore unachievable within finite acyclic models."* One sentence. Its value is architectural, not mathematical, and presenting a textbook fact as a Proposition invites the referee to discount the genuinely proved results beside it. |
| `cor:obs-flat-fold-singular` presented without attribution (`11:20-107`) | Add: *"This is the impropriety of intrinsic autoregressions [Besag 1974; Besag & Kooperberg 1995; Rue & Held 2005, Ch. 3] specialized to the reciprocal-pair fold."* The application stays; the linear algebra gets attributed. |
| `prop:cg-markov-category` with a full Tonelli proof (`06:28`) | Demote to a cited Remark: *"Markov kernels between standard Borel spaces form a category (`BorelStoch`) and law-pushforward is functorial [Lawvere 1962; Giry 1982; Panangaden 1999]; the synthetic theory built on it is [Fritz 2020; Cho & Jacobs 2019]."* Move the Tonelli computation to a footnote or drop it. |
| Chapter 2 with zero geometric-deep-learning citations | Add to §2.1: *"The construction below is the coordinate-independent-CNN formalism of [Cohen et al. 2019; Weiler et al. 2021/2023], with the associated vector bundle replaced by an associated bundle whose fiber is a statistical manifold. The consequences of that nonlinearity — the absence of a linear covariant derivative and the resulting connection-dependence of the induced base geometry — are the subject of Chapter 5c."* |
| `def:pb-informational-pullbacks` presented as new (`05c:124`) | Add immediately after: *"The Fisher metric and Amari–Chentsov tensor are pullbacks by definition [Ay–Jost–Lê–Schwachhöfer 2018]; the substance here is the replacement of $Ts$ by the connection-split vertical jet $D^\omega s$, in the sense of harmonic sections of fibre bundles [Wood 2003]. Compare the ungauged case, where a section of a bundle of Fisher–Rao simplices over a base is the assignment/sigma flow of [Åström et al. 2017; Cai et al. 2024]."* |
| "statistical bundle" used without disambiguation | Add a footnote at first use: *"Not to be confused with Pistone's statistical bundle [Pistone & Sempi 1995; Pistone 2018], a vector bundle over the statistical manifold whose fibers are score spaces; here the statistical manifold is the fiber, not the base."* |
| `prop:cg-gaussian-forward-kl-barycenter` (`09:639`) | **No change required** — no novelty is claimed anywhere. Optionally add "(moment matching / m-projection)" to the statement line. |
| Anywhere the associated-bundle agent construction is introduced | Cite **Dennis (2025)**. |

### 6.3 The strongest honest positioning sentence

> Building on the associated-bundle formulation of agents introduced in Dennis (2025) and on the informal
> proposal of Sengupta et al. (2016) that variational free-energy minimization constitutes a gauge theory, we
> give the first rigorous account of the informational geometry that a section of an associated bundle with
> statistical-manifold fibers induces on its base: the Fisher metric and Amari–Chentsov tensor — which are
> pullbacks by definition (Ay–Jost–Lê–Schwachhöfer 2018) — are pulled back not along the differential of the
> section but along its connection-split vertical jet, in the sense in which harmonic sections of fibre bundles
> pull back a fiber metric (Wood 2003), and we prove that the resulting base geometry is passively
> gauge-covariant yet *exactly* connection-dependent, with the dependence governed by a horizontal-defect
> calculus whose composition law and base-cocycle residual we compute in closed form.

Short version, for an abstract:

> We show that the geometry a belief field induces on its context space is gauge-covariant but not
> connection-independent, and we compute the exact defect: a horizontal-defect calculus with a closed
> composition law, an unconditional vertical Fisher cocycle, and a sharp base-cocycle residual.

Note the second sentence of the long version is doing the real work. It says the framework's central
geometric object is **not an observable** unless the connection is fixed by something — which is a *finding*,
not a construction, and it is the kind of finding that survives peer review because it can only be arrived at
by actually doing the calculation.

### 6.4 The adjacent, better-defended paper hiding in here

**Yes, clearly — and it is the paper the author should write first.**

> **"Connection-relative informational pullbacks: gauge covariance, connection dependence, and a
> horizontal-defect calculus."** Venue: *Information Geometry* (Springer) or *Differential Geometry and its
> Applications*. Length: 20–30 pages. Content: `05c` almost verbatim.

Setup: a principal $G$-bundle $P\to\mathcal C$, an associated bundle $E=P\times_{\widehat\rho}\mathcal B$ whose
fiber is a statistical manifold with $G$ acting by bimeasurable sample-coordinate changes, a principal
connection $\omega$, and a section $s$. Results, all already proved and numerically verified:

1. Descent of $g^F$ and $\mathcal T$ to vertical tensors (`prop:pb-statistical-tensor-descent`, `05c:59-88`) —
   with the bimeasurable-action hypothesis correctly isolated as load-bearing.
2. Definition of $h_s^\omega, c_s^\omega$ via $D^\omega s$, and passive gauge covariance
   (`thm:pb-pullback-gauge-invariance`) **with the active-gauge counterexample** showing the distinction is
   real.
3. Exact connection dependence, with counterexample (`05c:156-232`).
4. Constant-rank quotient theorem (`thm:pb-pullback-rank-quotient`).
5. Sharp section descent and the covariant first-jet chain rule (`thm:pb-section-descent`,
   `thm:pb-covariant-jet-naturality`).
6. The three defect identities — composition, vertical cocycle, base cocycle with exact residual.

**Why this is the better-defended paper.** All four of the ultradeep audit's structural criticisms —
(S1) the VFE is not a functional of a section; (S2) no source fixes; (S3) the gauge sector is inert, no
curvature; (S4) the numerical artifact does not bind — are criticisms of the *free-energy* layer. **This paper
does not contain a free energy.** It is pure differential geometry of statistical fibers. It needs no base
integral, no partition of unity, no sheaf gluing, no noumenal commitment, no philosophy chapter, and no
multi-agent story. It is also the only part of the corpus where the audit found genuinely unanticipated
mathematics.

A second, independent extraction: **`prop:obs-attention-elbo`** (`05b:547`) — exact row softmax derived from a
latent source label inside a fixed joint, strictly stronger than a mean-field ansatz — is a short, sharp ML
paper (cite Vaswani et al. 2017, which is in the bib and cited zero times). Keep the WikiText-103 sweep
excluded, per PIFB2's own fence F6.

**Recommended order:** (1) cite Dennis 2025 and Sengupta 2016 everywhere they belong; (2) extract the `05c`
geometry paper; (3) extract the attention paper; (4) return to the section-valued free energy — the one piece
of hard mathematics still open — with two published papers already banked.
