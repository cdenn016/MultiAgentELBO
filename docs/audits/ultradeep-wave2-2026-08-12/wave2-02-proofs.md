# Wave 2 — Proof-completeness audit

Date: 2026-08-11. Scope: **do the stated hypotheses imply the stated conclusion by the argument
given?** Wave 1 checked identities and found no algebraic errors; that is not re-reported here.
Execution: CPU only. **No GPU or CUDA job was started.** All numerics run in the Linux sandbox with
float64 / sympy exact rationals.

Rating vocabulary: PROOF COMPLETE / HYPOTHESIS UNUSED / GAP / SILENT HYPOTHESIS / WEAKER STATEMENT /
CIRCULAR / ERROR.

## Summary table

| # | Result | file:line | Rating |
|---|---|---|---|
| 1 | `prop:pb-statistical-tensor-descent` | `05c:59` | PROOF COMPLETE (2 hypotheses unused here) |
| 2 | `thm:pb-pullback-gauge-invariance` | `05c:124` | **GAP** — the one substantive step is asserted |
| 3a | `thm:obs-local-global-potential` | `05b:347` | PROOF COMPLETE (load-bearing lemma uncited) |
| 3b | `eq:obs-global-ledger` | `05b:441` | PROOF COMPLETE (lemma exists at `05_elbo:38`, uncited) |
| 3c | overcounting `eq:obs-singleton-incident-counting` | `05b:463` | PROOF COMPLETE |
| 3d | descent corollary | `05b:670-700` | **SILENT HYPOTHESIS** (`E|log Z_B|<inf`; ODE existence) |
| 4 | `prop:obs-attention-elbo` | `05b:547` | PROOF COMPLETE except **GAP** at "unique interior minimizer" |
| 5 | `thm:obs-collective-vfe`, `thm:obs-local-multiagent-elbo` | `05b:153,294` | PROOF COMPLETE / mislabeled environment (wave-1 F4 partially upheld) |
| 6a | `prop:prob-marginals-do-not-determine-joint` | `03:391` | **ERROR — stated hypothesis does not imply the conclusion; counterexample below** |
| 6b | `prop:prob-compatibility-nonidentifiability` | `03:420` | inherits 6a; (ii) PROOF COMPLETE with a chart caveat |
| 7 | `prop:gen-product-evidence-invariance` | `04:408` | PROOF COMPLETE except **GAP** at the induction base (root identities undisplayed) |
| 8a | `def:rg-geometric-state` | `07:153` | **SILENT HYPOTHESIS** (smooth tier never invoked in ch. 7) |
| 8b | equivariant `P_l` existence iff | `07:258-262` | PROOF COMPLETE (both directions verified) |
| 8c | Hopf-bundle failure witness | `07:263-266` | **ERROR (witness under-specified)** — false for trivial `kappa_l` |
| 8d | `eq:rg-scale-intertwiner` biconditional | `07:266-300` | PROOF COMPLETE |
| 9 | `thm:rg-exact-coarse-vfe` | `07b:34` | PROOF COMPLETE (one step under-stated; `Q_o << Pi_o` unused) |
| 10 | `thm:rg-strong-lumpability` | `07b:1946` | PROOF COMPLETE, **standard-Borel hypothesis unused** |
| 11a | `prop:obs-declared-root-unavoidable` | `11:239` | **WEAKER/DIFFERENT STATEMENT** (two-word repair) |
| 11b | other ch. 11 negatives | `11:41-380` | PROOF COMPLETE (all re-verified) |
| 12 | `thm:obs-star-fixed-point-contraction` | `11:256` | PROOF COMPLETE; `Theta_i in GL+(K)` unused; citation-scope slip |

No result in scope was found to be **circular**. No proof in scope relies, directly or through a
chain, on the result it proves.

---

## 1. `prop:pb-statistical-tensor-descent` — `Theory/05c_pullback_geometry.tex:59`

**Rating: PROOF COMPLETE. HYPOTHESIS UNUSED (two).**

Statement: "Under `\Cref{hyp:pb-regular-models}`, the represented $G$-action preserves $g_x^F$ and
$\mathcal T_x$. Consequently they descend to smooth vertical tensors ... on
$\mathcal E_x=P\times_{\widehat\rho_x}\mathcal B_x$."

Step-by-step:

- "Pushforward defines the unitary map $L^2(p)\to L^2((r_g)_\#p)$ given by $f\mapsto f\circ
  r_g^{-1}$." Correct; $\int|f\circ r_g^{-1}|^2d(r_g)_\#p=\int|f|^2dp$ needs exactly the declared
  bimeasurable bijection $r_g$.
- "Because $r_g$ is independent of the statistical parameter, differentiability in quadratic mean
  identifies the score of the pushed-forward tangent direction with $\ell_u\circ r_g^{-1}$."
  Correct, and the parameter-independence is genuinely load bearing:
  $d((r_g)_\#p_t)/d((r_g)_\#\mu)=(dp_t/d\mu)\circ r_g^{-1}$, so DQM transfers isometrically and the
  DQM score is $\ell_u\circ r_g^{-1}$.
- "The pushforward integration identity preserves the second and third score moments." Correct.
- Descent: "$\iota_{ug}=\iota_u\circ\widehat\rho_x(g)$, so a fiber tensor $\tau$ has frame-independent
  transport $\tau^u:=(\iota_u^{-1})^*\tau$ exactly when $\widehat\rho_x(g)^*\tau=\tau$." Verified
  against the declared quotient convention `eq:geo-quotient-convention` $(u\cdot g,\beta)\sim(u,g\cdot\beta)$:
  $[ug,\beta]=[u,g\cdot\beta]$, so $\iota_{ug}=\iota_u\circ\widehat\rho_x(g)$, and
  $(\iota_{ug}^{-1})^*\tau=(\iota_u^{-1})^*(\widehat\rho_x(g)^{-1})^*\tau$. The "exactly when" is a
  genuine biconditional and is correct.
- "Smoothness of the descended tensor follows by evaluating this construction on local smooth
  sections of $P$." Discharged: $P$ is a smooth principal bundle hence locally trivial, and
  $(c,\beta)\mapsto[\sigma(c),\beta]$ is a local diffeomorphism under which the descended tensor is
  the constant-in-$c$ tensor $\tau$.

Unused: (a) **positive definiteness of the Fisher form** plays no role — descent of $g^F$ needs only
that $\widehat\rho_x(g)$ is a score isometry, and the proof never needs $u\mapsto\ell_u$ injective;
(b) **"domination sufficient to differentiate the divergence expressions ... through third order"** is
not used here (it is consumed by later results in the section). These are hypotheses of a shared
section-level block, so this is a scope observation, not a defect. The remark at `05c:84-88` that the
bimeasurable sample action is load bearing is accurate.

Inherited (wave-1 G7, not re-reported): $\mathcal B_x\subseteq\mathcal P(\mathsf K)$ is declared a
subset at `02:69-74` and given $T_p\mathcal B_x$ at `05c:52`.

## 2. `thm:pb-pullback-gauge-invariance` — `Theory/05c_pullback_geometry.tex:124`

**Rating: GAP (named step unjustified). The theorem is true; the proof does not prove it.**

The entire proof is:

> "In a local frame, the vertical jet transforms by the tangent representation,
> $D^{\omega'}s'(X)=T\widehat\rho_x(g^{-1})D^\omega s(X)$, ... where $g:\mathcal U\to G$ is the frame
> change and the inverse follows from the quotient convention `eq:geo-quotient-convention`. The
> connection law is `eq:geo-local-connection-b` or `eq:geo-local-connection-m`, according to the
> channel. By `\Cref{prop:pb-statistical-tensor-descent}`, the tangent representation is an isometry
> of $g^F$ and preserves $\mathcal T$. Substitution ... cancels the frame change in every argument."

Two problems.

(i) **`eq:pb-covariant-jet-gauge-law` is the whole content and is asserted, not derived.** In the
$u$-trivialization a section is $\beta$ with $D^\omega s=d\beta+\zeta_{A(X)}\beta$; after $u'=u\cdot g$
one has $\beta'=\widehat\rho_x(g)^{-1}\beta$ and $A'=\operatorname{Ad}_{g^{-1}}A+g^{-1}dg$. Proving
$d\beta'+\zeta_{A'(X)}\beta'=T\widehat\rho_x(g^{-1})(d\beta+\zeta_{A(X)}\beta)$ requires the chain rule
on $c\mapsto\widehat\rho_x(g(c))^{-1}\beta(c)$ **and** the equivariance identity
$T\widehat\rho_x(g)\circ\zeta_\xi=\zeta_{\operatorname{Ad}_g\xi}\circ\widehat\rho_x(g)$; it is exactly
the $g^{-1}dg$ term that has to cancel against the derivative of $g$. None of this appears. The
appeal to `\Cref{prop:pb-statistical-tensor-descent}` is used *inside its own hypotheses* (pointwise
in $c$, at $g(c)\in G$) and is correct; it is the preceding line that is undischarged. Under
`SPEC.md` 2.2 this is a hand-wave that is neither discharged nor declared.

(ii) **Symbol overload of $\omega'$ inside one chapter.** At `05c:133` $\omega'$ means the
gauge-transformed *local representative* of the same connection; at `05c:160`
(`eq:pb-connection-difference`, `prop:pb-pullback-connection-change`) $\omega'$ means a genuinely
*different* principal connection, for which $D^{\omega'}s=D^\omega s+R_a^s$ and the theorem is
**false** — that is the point of `eq:pb-connection-dependence-example`. The two are not the same
object: $\operatorname{Ad}_{g^{-1}}A+g^{-1}dg$ is not $A+a$ with $a\in\Omega^1(\mathcal C,\operatorname{Ad}(P))$.

**Repair (two lines, and strictly better than the current proof).** `eq:pb-covariant-first-jet`
defines $D^\omega s=\operatorname{ver}^\omega\circ Ts$ with no reference to any frame, and by item 1
$g^F,\mathcal T$ are well-defined tensors on $V\mathcal E_x$ with no reference to any frame. Hence
$h_s^\omega,c_s^\omega$ are frame-free by construction and the theorem is immediate. Then keep
`eq:pb-covariant-jet-gauge-law` as a separately labeled local-coordinate corollary with the chain-rule
computation supplied, and rename its $\omega'$ to $A'$ or $\omega^g$.

The active-gauge counterexample at `05c:148-155` was checked and is correct: for $P=\mathbb R\times\mathbb R$,
$F(x,g)=(x,x+g)$ is $G$-equivariant over $\mathrm{id}$, carries $s(x)=[u(x),\mathcal N(0,1)]$ to
$[u(x),\mathcal N(x,1)]$, so $h=0\mapsto dx^2$ since the location-family Fisher information is 1.

## 3. `thm:obs-local-global-potential`, the global ledger, the overcounting identity, and the descent corollary

### 3a. `thm:obs-local-global-potential` — `05b:347` — **PROOF COMPLETE**

Every hypothesis is used. $Q_{B^c}\ll\Pi_{o,B^c}$ is what makes the pointwise cancellation of
$-\log Z_B(Y_{B^c})$ legitimate: $\Pi_{o,B^c}(\mathsf R_{B,o})=1$ (proved at `05b:262-272`) transfers
to $Q_{B^c}$, and on $\mathsf R_{B,o}$ one has $0<Z_B<\infty$. The two finiteness hypotheses are what
make $\mathbb E_{Q_{B^c}}\mathrm{KL}(r_B\Vert\Pi_{o,B})$ and its primed twin separately finite, so
"the finite-difference hypotheses permit the remaining subtraction under the integral" is honest.

Re-verified numerically, independent implementation, $|V|=3$, state sizes $(3,2,4)$, **correlated**
baseline $P_0$, three overlapping factor scopes $\{0,1\},\{1,2\},\{0,2\}$, block $B=\{0,1\}$:
LHS $=0.7827050700693006$, RHS $=0.7827050700693001$, $|{\rm diff}|=4.44\times10^{-16}$.

**One debt.** The sole substantive input, `eq:obs-posterior-block-kl-chain` (`05b:325-340`), is
displayed with **no proof, no citation and no `\status` tag**. It is true (disintegration chain rule
for relative entropy on standard Borel products, valid in $[0,+\infty]$), and the corpus already
cites it correctly elsewhere — `05_elbo.tex:452` cites `\citep{Klenke2020}` for exactly this. Repair:
add that citation and a status tag at `05b:325`.

### 3b. `eq:obs-global-ledger` — `05b:441` — **PROOF COMPLETE**

`eq:obs-correlated-complexity-ledger` is asserted with "the extended chain rule gives", with no
pointer. That lemma is **already proved in this corpus** as `thm:elbo-total-correlation-chain`
(`05_elbo.tex:38-52`), including the full singular-branch audit; `05b` does not cite it. The
extended-real bookkeeping is the only non-obvious part and is exactly what that theorem supplies.
Verified numerically on a correlated $Q$ over $2\times3\times2$: $\mathrm{KL}(Q\Vert P_0)=0.986132207252546$
versus $\mathrm{TC}+\sum_i\mathrm{KL}(Q_i\Vert\rho_i)=0.986132207252546$, difference exactly $0$.
Repair: one `\Cref`.

### 3c. Overcounting `eq:obs-singleton-incident-counting` — `05b:463` — **PROOF COMPLETE**

$\sum_{i\in V}H_{\{i\},o}=\sum_a|\partial a|E_{a,o}$ verified pointwise to $1.78\times10^{-15}$ on the
same instance. The nonempty-scope hypothesis is used and the empty-scope exception is stated
explicitly. The extended-real rearrangement justification ("both index sets are finite", values in
$\mathbb R\cup\{+\infty\}$) is correct and is the right thing to say.

### 3d. Descent corollary, `sec:local-natural-gradient` `05b:670-700` — **SILENT HYPOTHESIS**

Two, both distinct from wave-1 F5.

(i) **$\mathbb E_{Q_{B^c}}|\log Z_B(Y_{B^c})|<\infty$ is needed and is not assumed.** The text says
"the gradient of the outside-averaged local VFE is the corresponding block gradient of $F$". But
`thm:obs-local-global-potential` only equates **differences**; the outside-averaged local VFE itself,
$\Phi_i(\eta_i)=\mathbb E_{Q_{B^c}}[-\log Z_B(Y_{B^c})+\mathrm{KL}(\cdot)]$, is a well-defined real
function only if $\log Z_B$ is $Q_{B^c}$-integrable. Nothing in the chapter supplies that:
$Z_B$ is only known to lie in $(0,\infty)$ pointwise on $\mathsf R_{B,o}$. Repair: either assume
integrability, or restate the sentence about the gradient of the *difference*, for which the theorem
suffices verbatim.

(ii) **Existence/uniqueness of the flow.** "Assume $F(\eta)$ is $C^1$ ... and the trajectory remains
in this domain" presupposes a trajectory. With $F$ merely $C^1$ and $G_i^{-1}$ continuous the vector
field is continuous but not locally Lipschitz, so Peano gives existence and *not* uniqueness; "the
trajectory" is not licensed. `eq:obs-global-dissipation` holds along any solution, so the repair is
cosmetic: say "any solution", or assume $F\in C^{1,1}_{\rm loc}$.

## 4. `prop:obs-attention-elbo` — `05b:547` — PROOF COMPLETE except one **GAP**

The posterior row is correctly derived, and both stated hypotheses are used: $\pi_{ij}>0$ on the
finite source set and $D_{ij}$ finite make $Z_i^{\rm att}(y)\in(0,\infty)$; label exclusivity
`eq:obs-attention-augmented-likelihood` is what lets every $j$-free factor cancel. The displayed
identity
$\mathrm{KL}(\beta^Q_i\Vert\beta^P_i)=\mathrm{KL}(\beta^Q_i\Vert\pi_i)+\tau_i^{-1}\sum_j\beta^Q_{ij}D_{ij}+\log Z_i^{\rm att}(y)$
is exact, and the resulting row contribution matches a direct expansion of
$\mathrm{KL}(Q\Vert P_0^{\rm aug})+\mathbb E_Q H_o^{\rm aug}$ term by term.
`eq:obs-attention-recognition-factorization` and the two integrability assumptions are used and are
correctly flagged as not implied by the generative law. The correlated ledger at `05b:614-640` is the
right honest complement and correctly refuses to assert a row softmax under coupling.

**GAP.** "Lagrange multiplication under $\sum_j\beta^Q_{ij}=1$ proves
`eq:obs-attention-recognition-optimum`" proves neither of the two words in the claim
"**unique interior** minimizer": a Lagrange stationarity condition is necessary, not sufficient, gives
no uniqueness, and presupposes interiority rather than establishing it.

**Repair (one line, exact).** With $\beta^{Q\star}$ the displayed Gibbs row and
$Z=\sum_k\pi_{ik}e^{-\mathbb E_{Q_Y}D_{ik}/\tau_i}$,
$$\Fenergy_i^{\rm att}(\beta)=\mathrm{KL}(\beta\Vert\beta^{Q\star})-\log Z ,$$
so the minimizer is unique by strict positivity of relative entropy, and interior because
$\pi_{ij}>0$ and $\mathbb E_{Q_Y}D_{ij}$ is finite. Verified numerically ($J=5$, random
$\pi,D$, $\tau=0.7$): $\Fenergy(\beta^{Q\star})=-1.3411037820240943$ versus best of 20000 random rows
$-1.3303776688419782$, and $\max|\Fenergy(\beta)-\Fenergy(\beta^\star)-\mathrm{KL}(\beta\Vert\beta^\star)|
=8.9\times10^{-16}$ over 500 random rows.

## 5. Adjudication of wave-1 F4: `thm:obs-collective-vfe` (`05b:153`) and `thm:obs-local-multiagent-elbo` (`05b:294`)

**Verdict: wave-1 F4 is upheld in substance for the first and only partially for the second. Neither
is circular, neither is vacuous, and neither is wrong.**

- The boxed displays are `:=` definitions. That part of F4 is correct.
- But each environment additionally asserts three things that are *not* definitional: the range
  ($\mathbb R\cup\{+\infty\}$, which needs $0<Z(o)<\infty$ from `eq:obs-global-evidence`); the
  identification with `def:elbo-extended`/`thm:elbo-extended-gap`; and
  $\mathcal L\le\log Z$ **with equality exactly at** $\Pi_o$. The equality case is a genuine
  proposition (the zero condition for relative entropy), even if its proof is one line. So "definitions
  dressed as theorems" overstates it slightly: they are *definition plus immediate corollary*, merged
  into one environment.
- `thm:obs-local-multiagent-elbo` carries more real content than F4 credits: it is stated only for
  $b\in\mathsf R_{B,o}$, and that this set is $\Pi_{o,B^c}$-full is a nontrivial argument proved at
  `05b:262-272` (finiteness of $w_B$, positivity forcing $L_{\bar B,o}>0$, then
  $Z_B=w_B/L_{\bar B,o}\in(0,\infty)$). Without it the local functional is not even defined.

**Separate finding, applying to both.** Both proofs invoke `\Cref{thm:elbo-extended-gap}`, whose own
hypotheses are (H1)–(H2) of `hyp:elbo-evidence-domain` (`05_elbo.tex:120-134`) — statements about the
*finite-design* construction of chapters 3–4 ($p_\theta(o,y\given X)$, $\nu_D^Y$,
$\mathsf O_{\theta,X}^{\rm reg}$). Chapter `05b` deliberately starts over at `05b:18` with a different
construction ($P_0$, $L_o$, $Z(o)$) and never verifies (H1)–(H2) for it; the transfer is asserted by
"The regular-observation qualifications of `\Cref{ch:elbo}` apply." The transfer **is** sound —
`thm:elbo-extended-gap` uses only that $\log z$ is finite, that $\Pi=M_o/z$ is a probability measure,
and that $\mathrm{KL}\ge0$ with equality iff equal, all of which hold for $(L_oP_0,Z(o),\Pi_o)$ — but a
proof-checker should note that a cited theorem is being applied outside its literal hypothesis set.
Repair: state the gap theorem once in reference-measure-agnostic form (finite positive slice mass,
normalized slice), and cite that.

**Recommended fix for F4:** split each into `def:obs-collective-vfe` + `prop:obs-collective-vfe-gap`.
Purely taxonomic; no mathematics changes.

## 6. `prop:prob-marginals-do-not-determine-joint` (`03:391`) and `prop:prob-compatibility-nonidentifiability` (`03:420`)

### 6a. **ERROR — the stated hypothesis does not imply the conclusion. Highest-severity finding in this wave.**

Statement (`03:391`): "Suppose $\mathsf Y_D$ contains **at least two nondegenerate real coordinates** ...
Then there exist distinct probability measures on $\mathsf Y_D$ with identical coordinate marginals.
Consequently the family $\{q^{o,X}_{i,a},s^{o,X}_{i,a}\}$ does not determine $Q_X(\cdot\given o)$
under this richness hypothesis."

The failing step is the last sentence of the proof: "**Embedding this pair in any two coordinates of
$\mathsf Y_D$** and keeping the remaining coordinates fixed produces two distinct elements of
$\mathcal P(\mathsf Y_D,\mathscr Y_D)$ with the same family `eq:prob-recognition-marginals`."

That is false, because `def:prob-recognition-marginals` (`03:385`) does **not** marginalize onto scalar
coordinates. It marginalizes onto **blocks**:
$\operatorname{Marg}^k_{i,a}(R)=(\operatorname{pr}^k_{i,a})_\#R$ where
$\operatorname{pr}^k_{i,a}:\mathsf Y_D\to\mathsf K_{i,a}$, and in the Gaussian realization
$\mathsf K_{i,a}=\mathbb R^{K}$ with $K$ possibly $\ge2$ (`03:38`). If the two chosen real coordinates
lie inside one block, the $\mathcal N(0,I_2)$ / $\mathcal N(0,\Sigma_r)$ pair has **different** block
marginals and the witness collapses.

**Counterexample satisfying the stated hypothesis and violating the conclusion.** Take $|V|=1$,
$M=1$, $\mathsf K_{1,1}=\mathbb R^2$, $\mathsf M_{1,1}=\{0\}$ (one point with the trivial
$\sigma$-algebra). Then $\mathsf Y_D=\mathbb R^2\times\{0\}$ **contains two nondegenerate real
coordinates**, so the stated hypothesis holds. But there are exactly two marginalization blocks,
$q_{1,1}=(\operatorname{pr}^k_{1,1})_\#Q_X$ and $s_{1,1}=\delta_0$, and $\operatorname{pr}^k_{1,1}$ is a
bimeasurable bijection onto $\mathbb R^2$. Hence $q_{1,1}$ **determines $Q_X$ exactly**, contradicting
the conclusion. Numerically: the manuscript's own witness pair has identical scalar marginals
($\mathrm{var}=1$ in both coordinates for both laws) but block marginals separated by
$\mathrm{KL}(\mathcal N(0,I_2)\Vert\mathcal N(0,\Sigma_{0.6}))=0.3393564486857903$.

**Repair.** The correct richness hypothesis is about *blocks*, not coordinates: "at least two of the
declared marginal blocks $\{\mathsf K_{i,a}\}\cup\{\mathsf M_{i,a}\}$ are nondegenerate", equivalently
"the two nondegenerate real coordinates lie in distinct blocks". Then the proof goes through verbatim
by embedding one coordinate in each of two distinct blocks. Note the manuscript's own "without it the
conclusion can fail" example ($\mathsf K=\mathsf M=\{0\}$) understates the failure set by a lot: the
real obstruction is a single-block latent space of any dimension, not a singleton.

**Propagation.** The same wrong hypothesis is restated at `03:387` ("In the Gaussian realization with
at least two nondegenerate real coordinates, the marginals are therefore a lossy summary") and at
`05_elbo.tex:32-34` ("these marginals do not reconstruct $Q_X(\cdot\given o)$ whenever the latent
space contains at least two nondegenerate real coordinates"). Both need the same edit. In the
*reference presentation* of `def:prob-finite-design` there are always $\ge2$ blocks whenever
$|\mathfrak A|\ge1$ and both channels are nondegenerate, so no downstream result is believed to be
false — but the stated hypothesis is genuinely insufficient and the proof step is genuinely wrong.

**Secondary, quantifier order.** The conclusion "the family does not determine $Q_X$" is
existential as proved (there exist two laws with a common marginal family) but is used and phrased
universally ("Suppose the compatibility relation holds. Then ... does not determine $Q_X$"). Under the
corrected block hypothesis the universal version is still not implied by the stated hypothesis alone,
because it depends on the *law*: if two block marginals of the particular $Q_X$ are Dirac, the coupling
is unique. A universal statement needs "at least two block marginals of $Q_X$ are non-Dirac", which is
a condition on the law, not on the space.

### 6b. `prop:prob-compatibility-nonidentifiability` — `03:420`

Part (i) inherits 6a verbatim, since it cites the richness hypothesis by name and reasons only
through the marginals.

Part (ii) is **PROOF COMPLETE** with one silent hypothesis. The construction is sound: $D$ is finite
and $\mathcal C$ is a smooth manifold, so a neighborhood of $c^\star\in\mathcal C_i\setminus D$
disjoint from $D$ exists; the Gaussian mean coordinate is unconstrained in $\mathbb R^K$, so
$\mu_i+\chi v$ stays in the fiber; and it agrees with $q_i^{o,X}$ on $D$, so it satisfies
`eq:prob-compatibility` against the same marginals. **Silent hypothesis:** $\mu_i(c)$ is a
*local-trivialization* coordinate, so $\mu_i(c)+\chi(c)v$ defines a global section of
$\mathcal E_b|_{\mathcal C_i}$ only if $\operatorname{supp}\chi$ is contained in a trivializing open
set. Add "contained in a trivializing neighborhood" to the choice of the bump support. Both stated
hypotheses of (ii) are used. The proof deforms only $q_i$, not $s_i$, which is enough because the
conclusion is non-determination of the pair.

## 7. `prop:gen-product-evidence-invariance` — `04_generative.tex:408` — PROOF COMPLETE except one **GAP**

The measure-level claim, the density claim, and the Lebesgue claim were each re-derived and are
correct, including the change of variables: with $\varphi(y')=F(o,y')p_\theta(o,R^{-1}y'\given X)$ one has
$\int\varphi(Ry)\nu_D^Y(dy)=\int\varphi\, d(R_\#\nu_D^Y)=\int\varphi\, j_R\, d\nu_D^Y$, and
$(R_\#\lambda)(A)=\lambda(R^{-1}A)=|\det R|^{-1}\lambda(A)$ gives $j_R=|\det R|^{-1}$. $R$ is invertible
by construction (each block is $\rho_x(g)\in\operatorname{Aut}$), so the appearance of $R^{-1}$ in
`eq:gen-gauge-rn-density` before invertibility is mentioned is safe. Every displayed hypothesis of
`hyp:gen-kernel-covariance` is used: `eq:gen-gauge-pushforward-obs` is what makes $T$ the identity on
observations, which is what makes the observation marginals agree.

**GAP: the base case of the induction is not displayed.** The proof is "Apply
`eq:gen-gauge-pushforward-model`–`eq:gen-gauge-pushforward-obs` along the topological ordering. Each
factor is the receiving-coordinate pushforward of the original factor, so the composed law is
$T_\#P_\theta$." The topologically first factor is a **root**, and the root covariance identities are
not displayed anywhere: `hyp:gen-kernel-covariance` ends "with the analogous root identities"
(`04:399`). The induction therefore rests on an undisplayed hypothesis. Two repairs, either is cheap:
display the root identities in `hyp:gen-kernel-covariance`, or state the induction explicitly
(base = roots, step = one factor, conclusion by finiteness of the DAG). The compression of the
induction itself into one sentence is borderline under `SPEC.md` 2.2 but is defensible; the
undisplayed root identity is not.

This matters more than its severity suggests, because the wave-1 synthesis names N3(a) — built on this
proposition plus `hyp:gen-kernel-covariance` — as the highest value-to-cost item in the program.
Anything built on it inherits the undisplayed root case.

## 8. `def:rg-geometric-state` and the scale-equivariance material — `07_general_renormalization.tex:153, 258-300`

### 8a. `def:rg-geometric-state` — **SILENT HYPOTHESIS**

The definition declares "statistical fibers $\mathcal B_{\ell,b},\mathcal B_{\ell,m}$" with no
regularity, then asserts that the two principal connections "induce horizontal distributions
$H^b_\ell,H^m_\ell$ **and** parallel transports $\Omega_{\ell,\gamma},\widetilde\Omega_{\ell,\gamma}$
on the two associated bundles."

The transports are fine without smoothness: the horizontal lift lives in $\mathscr P_\ell$ (smooth by
declaration) and $[p,z]\mapsto[\tilde p,z]$ needs nothing from the fiber. The **horizontal
distributions do not exist** unless $\mathcal E_{\ell,s}$ is a smooth manifold, which needs
$\mathcal B_{\ell,s}$ smooth and the actions $\widehat\rho_{\ell,s}$ smooth. Chapter 2 has exactly
this as `hyp:geo-smooth-tier` (`02:103`), and `02:135-137` records that "Smoothness of $P$ alone does
not upgrade an arbitrary law fiber." But `grep` over the corpus shows `hyp:geo-smooth-tier` is
referenced **only** in `02_geometry.tex` and `05c_pullback_geometry.tex` — it is never invoked in
`07_general_renormalization.tex`. So `def:rg-geometric-state` re-declares the geometric state and
silently drops the hypothesis that makes half of it typecheck. Repair: one clause, "under the
levelwise analogue of `\Cref{hyp:geo-smooth-tier}`".

### 8b. Existence of an equivariant $\mathcal P_\ell$ — **PROOF COMPLETE**

"an equivariant $\mathcal P_\ell$ over $c_\ell$ exists **if and only if** the extended bundle
$\mathscr P_\ell\times_{\kappa_\ell}G_{\ell+1}$ is isomorphic to the pullback $c_\ell^*\mathscr P_{\ell+1}$
as a principal $G_{\ell+1}$-bundle over $\mathcal C_\ell$." No proof is given, but both directions
check out and are two lines each, so this is at worst a discharge-able omission:

- ($\Leftarrow$) $p\mapsto\varphi([p,e])$ followed by $c^*\mathscr P_{\ell+1}\to\mathscr P_{\ell+1}$
  satisfies $p\cdot g\mapsto[pg,e]=[p,\kappa(g)]=[p,e]\cdot\kappa(g)$.
- ($\Rightarrow$) $[p,h]\mapsto(\varpi_\ell(p),\mathcal P_\ell(p)h)$ is well defined by equivariance,
  is $G_{\ell+1}$-equivariant over $\mathrm{id}_{\mathcal C_\ell}$, and any such map of principal
  bundles over a common base is an isomorphism.

Calling this "a genuine topological condition on the declared data, not a normalization" is correct
and is the right thing to have said.

### 8c. The Hopf-bundle failure witness — **ERROR (witness under-specified)**

"It can fail, for instance for the Hopf bundle over $S^2$ against the trivial bundle with $c_\ell$ the
identity." **This does not specify $\kappa_\ell$, and the claim is false for some admissible
$\kappa_\ell$.** Take $G_\ell=G_{\ell+1}=U(1)$, $\mathscr P_\ell=S^3\to S^2$, $\mathscr P_{\ell+1}=S^2\times U(1)$,
$c_\ell=\mathrm{id}$, and $\kappa_\ell\equiv1$ the **trivial** homomorphism. Then
$\mathscr P_\ell\times_{\kappa_\ell}U(1)=(S^3\times U(1))/\!\sim$ with $(p\cdot g,h)\sim(p,h)$, i.e.
$S^2\times U(1)$, which **is** isomorphic to $c_\ell^*\mathscr P_{\ell+1}$; concretely
$\mathcal P_\ell(p)=(\varpi_\ell(p),e)$ is $\kappa_\ell$-equivariant and covers $c_\ell$. So the
witness exhibits no failure.

**Repair: specify $\kappa_\ell=\mathrm{id}_{U(1)}$.** With that, $\mathscr P_\ell\times_{\rm id}U(1)\cong S^3$,
which is not isomorphic to $S^2\times U(1)$ (first Chern class $1$ versus $0$; equivalently
$\pi_1(S^3)=0\neq\mathbb Z=\pi_1(S^2\times S^1)$), and the witness is correct. This is a one-symbol
edit, but as printed the corpus's only witness for a stated topological obstruction does not witness it.

### 8d. `eq:rg-scale-intertwiner` biconditional — **PROOF COMPLETE**

"The biconditional is a two-line computation on representatives" is followed by the two lines, which
are correct in both directions, plus an honest degenerate-case note (a $G_{\ell+1}$-fixed singleton
coarse fiber makes the condition vacuous) and an explicit statement of the two further hypotheses
consumed at the information-geometric tier. This is the model the rest of the chapter should follow.

Minor: `eq:rg-relative-frame-naturality` is introduced with "equivariance of $\mathcal P_\ell$ forces";
the one-line derivation ($\mathcal P_\ell(u^b_\ell h_\ell)=\mathcal P_\ell(u^b_\ell)\kappa_\ell(h_\ell)$
versus $\mathcal P_\ell(u^m_\ell)=u^m_{\ell+1}(c_\ell\cdot)a^m_\ell$) is omitted but correct.

## 9. `thm:rg-exact-coarse-vfe` — `07b_agent_network_rg.tex:34` — **PROOF COMPLETE**

All four proof steps check out: $C(y,\mathsf Z)=1$ gives the observation marginal;
$\mathrm{KL}(Q_o\Vert\Pi_o)=\mathrm{KL}(\widehat Q_o\Vert\widehat\Pi_o)$ because the same kernel is
attached to both; disintegration on $z$ plus the chain rule splits it; the evidence terms cancel.

Verified numerically on finite spaces ($|\mathsf O|=3,|\mathsf Y|=6,|\mathsf Z|=3$, random $P$ and
row-stochastic $C$): evidence match exact ($0.3354363087722779$ both scales),
$\Fenergy_P(Q_o)=2.398583993793041$ versus $\Fenergy_{P^c}(Q^c_o)+{\rm cond}=2.3985839937930415$,
$|{\rm diff}|=4.44\times10^{-16}$, conditional term $=1.2761926119961409\ge0$.

Two observations.

- **One step is under-stated.** "Substitute the exact evidence identities at the two scales" silently
  uses that the posterior of $P^c$ at $o$ **is** $\Pi_oC$. That is true —
  $P^c(do,dz)=P^O(do)(\Pi_oC)(dz)$ because $C$ does not read $o$ — but it is the only place the
  "does not alter the observation coordinate" clause of `eq:rg-coarse-channel` does work, and it
  deserves the sentence.
- **`Q_o\ll\Pi_o` (declared at `07b:20`) is unused.** The identity holds in $[0,+\infty]$ regardless.

## 10. `thm:rg-strong-lumpability` — `07b_agent_network_rg.tex:1946` — **PROOF COMPLETE, HYPOTHESIS UNUSED**

Both directions verified line by line. Forward: $\mu=\delta_y$ gives
$T(y,c^{-1}B)=T^c(c(y),B)$, whose right side depends on $y$ only through $c(y)$; surjectivity is used,
and is used only, for uniqueness. Converse: $B\mapsto T(\varsigma(z),c^{-1}B)$ is a probability measure
because $c^{-1}$ commutes with countable disjoint unions; $z\mapsto T(\varsigma(z),c^{-1}B)$ is
measurable as a composition; $c(\varsigma(c(y)))=c(y)$ plus the hypothesis gives
$T^c(c(y),B)=T(y,c^{-1}B)$; and the pushforward change of variables closes it. The weak-lumpability
counterexample at the end is correct as stated: $T(1,\{1,2\})=0\neq1=T(2,\{1,2\})$ with $c(1)=c(2)$,
while from $\delta_3$ the chain stays in $\{1,3\}$, on which $c$ is injective.

**Standard Borel is never used** in the proof, which is valid on arbitrary measurable spaces. It
earns its place only in the scope note (for countable $\mathsf Z$, standard Borel makes the
$\sigma$-algebra discrete, so any selection is Borel). The honest treatment of the measurable-selection
issue — "Without a measurable selection, `eq:rg-lumped-kernel-formula` still defines the coarse
transition on the range of $c$ and the selection must be declared separately" — is exactly right;
a Borel right inverse of a surjective Borel map between standard Borel spaces does **not** exist in
general, and the manuscript does not claim it does.

## 11. Negative results in `11_obstructions.tex`

### 11a. `prop:obs-declared-root-unavoidable` — `11:239` — **PROVES A SLIGHTLY DIFFERENT STATEMENT**

Statement: "In any finite directed acyclic generative model there is at least one latent with no
parents, whose marginal law is therefore part of the declared parameters."
Proof: "A finite directed acyclic graph admits a topological order, and its first element has no
incoming edges. Its factor in the joint is unconditional, so it is declared."

Two defects, both in the statement rather than the argument.

1. **The DAG must be restricted to latent nodes, and the conclusion must be weakened accordingly.**
   The generative models of `ch:generative` have an exogenous structural configuration $X$ and
   observation nodes. A model in which the unique latent $b$ satisfies $b\given X\sim\mathcal N(f(X),\Sigma)$
   is finite and acyclic and has **no latent with no parents** in the full graph; the first element of
   a topological order of the full graph is $X$, not a latent. What survives, and is what the section
   actually needs, is: *some latent has no latent parent, and its factor is conditional only on
   declared exogenous data, hence is a declaration and not constituted by other latents.* The proof's
   word "unconditional" should be "unconditioned on other latents".
2. **Nonemptiness.** "there is at least one latent with no parents" is false if there are no latents.

Neither affects the use made of the proposition at `11:245` and `11:250`. Repair is two words plus a
nonemptiness clause.

### 11b. The remaining ch. 11 negatives — **PROOF COMPLETE**

Each was re-derived.

- `prop:obs-reciprocal-pair-kernel` (`11:41`). $\ker J=\ker E_e\cap\ker E_f$ is correctly justified via
  $w^\top E^\top R^{-1}Ew=0\iff Ew=0$ for $R\succ0$; the substitution gives $v=Hv$; the converse
  direction and the injectivity of $v\mapsto(\Theta_ev,v)$ are both checked. Complete.
- `cor:obs-flat-fold-singular` (`11:56`) and the "Boundary of the no-go" paragraph. Complete, and the
  scoping — "the obstruction is exactly the conjunction of the reciprocal-pair energy, no SPD anchor,
  and flat parallel-edge holonomy $H=I$" — is exactly the right statement of what was proved.
- `prop:obs-normalizer-link-dependence` (`11:122`). Re-derived symbolically: $\det J=0$;
  $\det(J+p_0I)-(p_0^2+p_0(a+a^{-1})^2)=0$ identically; $\mathsf A'(1)=0$ and
  $\mathsf A''(1)=-4/(p_0+4)<0$. The "strict maximum, not minimum" reading and the disclaimer at
  `11:154` that this is a change of model rather than motion along a gauge orbit are both correct, and
  the latter cites `prop:gen-product-evidence-invariance` inside its hypotheses.
- `cor:obs-holonomy-kernel-shrinkage` (`11:336`). All three biconditionals read off correctly; the
  genericity argument is valid, and $H=2I$ with $\det(H-I)=1$ is a legitimate witness that the
  polynomial is not identically zero on $\GL^+(K)$.
- `prop:obs-holonomy-determinant-factorization` (`11:352`). $J=\widetilde E^\top\widetilde R^{-1}\widetilde E$
  and the Schur complement give $\det\widetilde E=\det(I-\Theta_f\Theta_e)$. Re-verified numerically at
  $K=3$ with random $\Theta_e,\Theta_f,R_e,R_f$: $\det J=2.3595352369018106\times10^{-5}$ versus formula
  $2.3595352369018736\times10^{-5}$.
- `prop:obs-star-definite`, `prop:obs-anchor-coercivity`. Complete.
- `prop:obs-star-meanfield-coordinate` (`11:227`). Complete, with one **silent hypothesis**: writing
  $\log q^*(b)=\mathbb E_{-b}[\log p(b,y)]+\text{const}$ and reading off the linear coefficient
  $\sum_i\Theta_i^\top R_i^{-1}\mathbb E[y_i]$ requires the non-$b$ factors to have finite first
  moments. The conclusion presupposes $\mathbb E[y_i]$ exists but the family is never restricted.

## 12. `thm:obs-star-fixed-point-contraction` — `11_obstructions.tex:256` — **PROOF COMPLETE**

Every step re-derived: the constituent update (precision $R_i^{-1}$, information vector
$R_i^{-1}\Theta_im_b^{(t)}+r_i$, hence $m_i^{(t+1)}=\Theta_im_b^{(t)}+R_ir_i$); the substitution
$\sum_i\Theta_i^\top R_i^{-1}(\Theta_im_b+R_ir_i)=Bm_b+\sum_i\Theta_i^\top r_i$ giving $m_b^{(t+1)}=c+Mm_b^{(t)}$;
$I-M=P_b^{-1}P_0$ and hence $m_b^\star=P_0^{-1}(r_b+\sum_i\Theta_i^\top r_i)$;
$P_b^{1/2}e_{t+1}=SP_b^{1/2}e_t$ with $S=P_b^{-1/2}BP_b^{-1/2}=I-P_b^{-1/2}P_0P_b^{-1/2}$, so
$\operatorname{spec}(S)\subseteq[0,1)$ and $\rho=\lambda_{\max}(S)<1$; the KL statements
($\tfrac12\Vert e_t\Vert^2_{P_b}$ for the apex, $\tfrac12e_t^\top Be_t\le\tfrac12e_t^\top P_be_t$ summed
over constituents).

Numerical confirmation ($K=3$, $n=4$, random SPD $P_0,R_i$): fixed-point residual $2.2\times10^{-16}$;
$\operatorname{spec}(S)=(0.146190285228,\,0.258644753926,\,0.544136637469)$; observed worst per-step
$P_b$-contraction ratio $0.5441366374678$ against $\rho=0.5441366374690$ — the rate is **attained**, so
`eq:obs-star-rate` is sharp and not merely valid. (An earlier run reported a ratio above $\rho$; that
was float noise from steps where $\Vert e_t\Vert\sim10^{-15}$, and it disappears when the measurement
is restricted to $\Vert e_t\Vert>10^{-8}$.)

Three observations.

- **`Theta_i in GL^+(K)` is unused.** The theorem holds verbatim for arbitrary, even singular or
  rectangular, $\Theta_i$, since only $B=\sum_i\Theta_i^\top R_i^{-1}\Theta_i\succeq0$ enters. The
  numerical run above deliberately used $\Theta_1=0$ and non-orientation-preserving $\Theta_i$ and the
  conclusion held. The hypothesis is inherited from `prop:obs-star-definite`, where it is likewise
  unused ($P_0\succ0$ alone does the work). Stating the theorem for arbitrary $\Theta_i$ costs nothing
  and strengthens it.
- **Citation-scope slip.** "`\Cref{prop:obs-star-meanfield-coordinate}` **with the added information
  vector** gives the first expression in `eq:obs-star-apex-update`." That proposition is stated and
  proved for the centered star ($r=0$); the $r\ne0$ case is outside its hypotheses. The proof
  effectively redoes the computation, so this is a citation slip rather than a gap, but the clean fix
  is to state the proposition with the information vector from the start.
- **Silent hypothesis, minor.** "converges geometrically from every initial collection of means"
  presupposes that the initial factors possess first moments; the first constituent update requires
  $\mathbb E_{q_b^{(0)}}[b]$ to exist. Also "in parallel or in any order" is asserted; it is true
  because the constituent coordinate optima depend on $q_b$ only and not on each other, which is worth
  one clause.

The scope paragraph at `11:320` — $P_0\succ0$ essential, $B=0\Rightarrow\rho=0$, delayed/noisy/
asynchronous/inexact updates not covered and tagged `OPEN` — is accurate and correctly tagged.

---

## Cross-cutting observations

1. **`SPEC.md` 2.2 compliance is good in the target files.** A grep for the canonical gesture phrases
   ("it follows", "similarly", "one can show", "the general case is analogous", "by a standard
   argument") over `03`, `04`, `05b`, `05c`, `07`, `11` returns essentially nothing; the one "two-line
   computation" (`07:284`) is followed by the two lines. The undischarged steps found above are not of
   the verbal-gesture type — they are *displayed equations asserted without derivation*
   (`eq:pb-covariant-jet-gauge-law`, `eq:obs-posterior-block-kl-chain`) and *undisplayed hypotheses*
   ("the analogous root identities", `hyp:geo-smooth-tier` in ch. 7). Those slip past a phrase-level
   check, which is why they survived wave 1.
2. **The chapter boundary is where hypotheses go missing.** Three findings — `05b` citing
   `thm:elbo-extended-gap` outside (H1)–(H2), `07` re-declaring the geometric state without
   `hyp:geo-smooth-tier`, `05b` using the disintegration KL chain rule that `05_elbo:452` already
   cites correctly — are all cases of a chapter restating a construction and dropping a hypothesis
   the original carried. A mechanical check ("every chapter that re-declares an object must re-cite
   the hypothesis label that types it") would have caught all three.
3. **Two proofs are strictly weaker than a one-line alternative already available in the corpus**:
   `thm:pb-pullback-gauge-invariance` (the frame-free definition makes it immediate) and the attention
   minimizer ($\Fenergy^{\rm att}=\mathrm{KL}(\beta\Vert\beta^\star)-\log Z$). Both repairs shorten
   the text.
