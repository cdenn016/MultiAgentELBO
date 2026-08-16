# Authoring spec — Gauge-Covariant VFE: a single-ELBO theory and its renormalization

**Every agent MUST read this file in full before writing a single line.** It is the only
coordination device. Notation drift between chapters is the failure mode this document exists to
prevent.

## 0. What this document is, and what it is not

A self-contained development of the **general gauge-theoretic variational free energy theory**:
one principal `G`-bundle inducing distinct belief and model associated bundles, one fixed normalized
generative law, one correlated recognition law, **one exact ELBO**, and the renormalization of that
structure under coarse-graining. Belief and model may use different representations, local frame
sections, connections, and coarse maps on that common principal bundle. A common frame or equal
connection is a stronger specialization. Independent principal bundles with product gauge group
`G_b x G_m` are an optional extension, never the ambient theory.

**PIFB2 does not appear.** Not as a source, not as a crosswalk, not as motivation, not in a remark.
The author's earlier five-term consensus functional, the `T1..T6` term labels, the Ouroboros tower,
the historical meta-agent barycenter, and every executable detail are **out of scope**. Historical
`beta_ij`/`gamma_ij` formulas are not imported. The present theory may derive a new categorical
source-label attention `beta_ij` from a fixed normalized interaction-record joint, but it must keep
the generative posterior row, recognition row, receiver occupancy, and joint event law distinct.
The exclusion also does not forbid the holonomy-conditioned projection of transported marginal
laws onto an invariant parent family. That construction must be named as a marginal-law mode and
kept distinct from partition selection, a normalized coarse channel, and exact joint-law recovery.

**The executable does not appear.** No `gauge_agent/`, no `run_experiment.py`, no config toggles, no
runtime crosswalk, no line-number citations to any repository.

Nothing in this document is a report on a prior manuscript. It stands alone.

## 1. Global writing rules (non-negotiable)

- **Flowing academic prose.** Full paragraphs with logical progression. Minimize itemization; if
  content can be a paragraph, make it one. Bullet lists are essentially banned in the body.
- **American English** throughout: color, behavior, normalize, optimize, factorize, center, modeling,
  fiber.
- **No LaTeX spacing macros.** `\;` `\,` `\!` are banned. Use ordinary spacing and `\qquad`/`\quad`.
- **Equation punctuation.** Display equations take a comma or period as the sentence requires.
- **Banned phrases** (Claude-isms): "key insight", "crucially", "critically", "notably",
  "importantly", "it's worth noting", "fundamentally", "leverages", "underscores". No horizontal
  rules (`---`, `--`) in the body.
- **No hedging without payment.** If something is unproved, say exactly what is unproved and under
  what hypotheses the weaker statement holds. Do not write "clearly", "it can be shown", or "for
  suitable conditions" without discharging them.
- **Every load-bearing equation gets a `\label`** using the prefixes in section 4 below.
- **State hypotheses before results.** A proposition with an unstated hypothesis is a defect.

## 2. Epistemic status — the document's central discipline

**This is the requirement the author cares most about.** A reader must be able to tell, at every
point, whether they are reading something established, something conjectured, something gestured at,
or something still owed. Ambiguity here is the worst defect this document can have — worse than a
gap, because a declared gap is honest and an undeclared one is not.

### 2.1 Every non-trivial claim carries a visible status

Use the `\status{...}` macro (defined in `main.tex`) immediately after the statement it governs, and
also name the status in the prose. Seven values, and only these. The middle column below is the
authority: it is reproduced verbatim as the second column of the taxonomy table in
`01_introduction.tex` (`\label{tab:status-taxonomy}`), and the two must be kept word for word
identical.

Each visible tag governs one visibly delimited semantic claim: end that claim with its tag and begin
the next claim in a new prose paragraph. Adjacent status tags and multiple statuses in one prose
paragraph are forbidden. The rows of the explicitly captioned Status taxonomy table are the sole
structural exception.

| Status | What it promises the reader | Obligation on you |
|---|---|---|
| `ESTABLISHED` | Proved here, or a standard result cited to a source that has been checked. | Give the proof or the citation. A citation must be to a real source you have checked. |
| `DEFINITION` | A declared type, construction, or convention. Nothing is being proved and the text says so. | Nothing to prove, but say plainly that nothing is being proved. |
| `HYPOTHESIS` | A restriction the development adopts by choice. What it excludes, and where it is used, are stated. | Say it is a choice, say what it excludes, and say where it is used. |
| `CONJECTURE` | Believed and precisely stated, but not proved. Stated sharply enough to be attacked. | State it precisely enough to be attacked, and give what evidence exists and of what kind. |
| `NUMERICAL` | Supported by computation only, with its measurement, seed, and control reported. Computation is not proof. | Give the measurement, the control, the seed, and say explicitly that computation is not proof. Tag the assertion where it is made, not only in the register. If a seed was not recorded, say that it was not recorded rather than supplying one. |
| `OPEN` | Unsettled. What would settle it, and what obstructs it, are named. | State exactly what would settle it, and what the obstruction is. |
| `NOT-CLAIMED` | A statement the development deliberately declines to make. Declining is not refuting, and the text says which it is doing. | Say that the development declines the statement, say why, and keep it separate from anything shown to be false. |

A claim with no status is a defect. A `CONJECTURE` presented in the grammar of a theorem is a worse
defect. `NOT-CLAIMED` is the tag form of the distinction section 2.5 requires, and it must never be
used for a statement the document refutes.

### 2.2 Hand-waving is a debt, not a style

A hand-wave is any step made by gesture rather than argument: "it follows that", "one can show",
"clearly", "for suitable conditions", "up to technicalities", "in the appropriate limit", "modulo
regularity". **You have exactly two permitted responses,** and silence is not one of them.

Either **discharge it** — supply the proof, compute the constant, name the exact condition, cite a
primary source — or **convert it into a declared gap**: state precisely what holds, under what
hypotheses, what remains unproved, and what would close it, and mark it `OPEN`.

Do not smuggle a gap through by weakening the verb. "The flow presumably converges" is worse than
"whether the flow converges is open, and closing it requires X", because the first hides the debt
inside a sentence that reads like a result.

### 2.3 Numerical evidence is never proof

Where a claim rests on computation, say so in the sentence that makes the claim, not in a footnote.
Report the measurement, the seed, and — this matters — **the control**. A measurement without a null
or a control is not evidence for a structural claim. If a control was not run, say that it was not.

### 2.4 Central open-obligation ledger

The visible inline `\status{...}` tag remains mandatory at the claim it governs. The former
per-chapter registers are replaced by one compact, nonduplicative appendix of unresolved
obligations. It collects conjectures and open problems by topic and says what would close each one.
Established theorems remain at their proofs, while numerical claims and their protocol metadata
remain in the numerical-provenance appendix. The obligation ledger is an audit index, not a second
exposition of the theory, and it must not duplicate every local result.

### 2.5 Distinguish "not claimed" from "false"

Where the development deliberately declines a statement, say that it declines it and why, and keep
that separate from statements shown to be false. Both appear in this document and conflating them
would misrepresent the state of the theory in opposite directions. The tag for the first is
`NOT-CLAIMED`; a refutation is an `ESTABLISHED` negative result and takes that tag instead.

## 3. Notation — fixed, do not deviate

**Geometry.** Contextual base `\mathcal C` with points `c`. One principal bundle
`\pi:\mathscr P_G\to\mathcal C` with structure group `G` induces the belief and model associated bundles
`\mathcal E_b=\mathscr P_G\times_{\widehat\rho_b}\mathcal B_b` and
`\mathcal E_m=\mathscr P_G\times_{\widehat\rho_m}\mathcal B_m`. Use `\rho_b,\rho_m` for possibly inequivalent
representations of `G` on the two sample fibers and `\widehat\rho_b,\widehat\rho_m` for their
pushforward actions on law fibers. Local principal frames `u_i^b,u_i^m:\mathcal C_i\to\mathscr P_G` are
separate choices. The unique relative principal-frame field is `h_i:\mathcal C_i\to G`, defined by
`u_i^m=u_i^b h_i`; it exists even when the representations have different dimensions, but it does
not define a map between their representation spaces. At the general tier the cross maps are
measurable and fiber preserving. Under the selected smooth-tier hypothesis, the two principal
connections `\omega_b,\omega_m` on the same `\mathscr P_G` induce Ehresmann horizontal
distributions and parallel transports
`\Omega_\gamma` on `\mathcal E_b` and `\widetilde\Omega_\gamma` on `\mathcal E_m` along a
piecewise-smooth base curve `\gamma`. Cross-associated-bundle morphisms cover the identity and have
the fixed directions
`\Phi:\mathcal E_b\to\mathcal E_m` and
`\widetilde\Phi:\mathcal E_m\to\mathcal E_b`; they are not principal-bundle morphisms, gauge
automorphisms, same-channel transports, or assumed inverses. For a smooth nonlinear fiber map,
define the defect by horizontal lifts:
`(\mathcal D\Phi)_e(X)=T_e\Phi(H_e^bX)-H_{\Phi(e)}^mX`, and analogously for
`\widetilde\Phi`. Only for fiberwise-linear vector-bundle morphisms may this be abbreviated as
`D\Phi=\nabla^m\circ\Phi-\Phi\circ\nabla^b`, with the corresponding Hom-bundle left-right law.

Pointwise comparisons between local frames at one base point are written `T^b_{ij},T^m_{ij}` and
take values in the same `G`. The two frame atlases describe one principal-bundle Cech class; their
cocycles are related by the relative field and are not independent topology classes. Independently
declared graph-edge-copy links are written `\Theta^b_e,\Theta^m_e\in G`, with
`\Theta_{\bar e}^x=(\Theta_e^x)^{-1}`, and transform under discrete vertex frame changes `h_i^x`.
Endpoint notation `\Theta_{ij}^x` is permitted only when the edge copy is unique. A smooth local
reframing `g_i^x(c)` induces that vertex gauge only after a vertex context
`c_i\in\mathcal C_i` is chosen, by `h_i^x=g_i^x(c_i)`. Neither a pointwise comparison nor a graph
link is a base parallel transport unless endpoint contexts, edge-labeled curves
`\gamma_e:c_j\to c_i`, and an equality hypothesis are supplied.
On a finite design, the full context-dependent product of passive frame-coordinate changes uses link copies
`\Theta_{a,e}^x` (abbreviated by endpoints when unique) with
`h_{a,i}^x=g_i^x(c_a)`. Constraining one shared link across all design points leaves the stabilizer
for which `h_{a,i}^x\Theta_{ij}^x(h_{a,j}^x)^{-1}` is independent of `a`;
context-independent rechoices are sufficient but need not exhaust that stabilizer. Any larger
transformation law requires a separately declared compensation.
This coordinate product does not replace the single principal structure group. A common-frame
specialization sets `u_i^b=u_i^m`; equal connections and identified graph links are further,
separate assumptions. Use two independent principal bundles only in a labeled product-gauge
extension whose additional physical symmetry or independent topology is actually needed.

**Pullback geometry and histories.** Write `\varpi_x:\mathcal E_x\to\mathcal C` for the
associated-bundle projection, `V\mathcal E_x=\ker T\varpi_x`, and
`\operatorname{ver}^{\omega_x}` for the vertical projection selected by the induced Ehresmann
connection in channel `x\in\{b,m\}`. For a smooth agent section use
`D^{\omega_b}q_i=\operatorname{ver}^{\omega_b}\circ Tq_i` and
`D^{\omega_m}s_i=\operatorname{ver}^{\omega_m}\circ Ts_i`. The vertical Fisher tensors are
`g_b^F,g_m^F`; their section pullbacks are
`h_{i,b}^{\omega_b}=(D^{\omega_b}q_i)^*g_b^F` and
`h_{i,m}^{\omega_m}=(D^{\omega_m}s_i)^*g_m^F`. Call these connection-relative vertical Fisher
semimetrics unless injectivity has been proved. Gauge invariance under passive re-trivialization
does not mean independence from the chosen connection. A combined belief--model tensor requires
declared positive channel weights or a declared joint statistical metric; the common principal
bundle and relative frame supply neither weights nor cross terms.

For a curve `\Gamma:J\to\mathcal E_x`, reserve `\gamma=\varpi_x\circ\Gamma` for its base
projection. The curve is vertical when `\gamma` is constant. It is horizontal only relative to a
chosen `\omega_x`, when
`\dot\Gamma=H^x_{\Gamma}\dot\gamma`, equivalently when its covariant vertical velocity vanishes.
A curve with nonconstant base projection and nonzero covariant vertical velocity is mixed. A base
curve itself needs no connection; its horizontal lift and the horizontal--vertical decomposition
do. A curve in the section configuration space is a different object: its evaluation at every
fixed `c` is vertical. Use `\mathfrak S_i` for a declared regular space of belief--model sections
and `\mathscr H_i` for an oriented, unparameterized inference orbit in it. The adjoint history map
has type `\Sigma_i:\mathscr H_i\times\mathcal C_i\to
\mathcal E_b\times_{\mathcal C}\mathcal E_m` and obeys
`\varpi\circ\Sigma_i(r,c)=c`. The base remains fixed and timeless. Any local parameter used to
calculate a path integral is auxiliary and must disappear from the final arc length.

**Phase 0 pointwise-parent symbols.** For a finite child block \(I\) with parent label \(A\), agent
\(i\in I\) supplies its section pair on \(\mathcal C_i\); the common overlap is
\(\mathcal U_A=\bigcap_{i\in I}\mathcal C_i\), and the present construction fixes
\(r_*\in\mathcal U_A\). Ordinary \(R\) is not an overlap: the intervention comparison retains
\(R\to E\to O\). The action functional is \(\mathscr S\). The associated-bundle projection
remains \(\varpi_x\); it is never receiver occupancy.

At fixed admitted \((o,X)\), use \(q_i^{b;o,X}\) for a belief-law section and
\(q_i^{m;o,X}\) for a model-law section. Established \(q_i^{o,X},s_i^{o,X}\) retain those
dependencies and are not globally renamed. A model sample or presentation is
\(m_i\in\mathsf M_i\), not a law, and its measurable evaluation is
\(\operatorname{ev}_i:m_i\mapsto K^X_{i,m_i}\).
General normalized law and kernel spaces on
standard-Borel domains are primary; smooth statistical manifolds require separate regularity, and
Gaussian families are optional computational realizations only.

Structural \(X\) is fixed outside the random channel, with \(X_A=\chi_A(X)\). The retained random
interface is \(\xi_A\in\boldsymbol\Xi_A\), and
\(\mathsf Z_A=\mathsf B_A\times\mathsf M_A\times\boldsymbol\Xi_A\times\mathsf H_A\) contains random
parent state only. The fine full laws are \(\mathbb P_I(Do,DY\mid X)\), \(\mathbb Q_{I,o,X}\),
and \(\boldsymbol\Pi_{I,o,X}\). The parent full laws are \(\mathbb P_A(Do,Dz\mid X)\),
\(\mathbb Q_{A,o,X}\), and \(\boldsymbol\Pi_{A,o,X}\). Bare global \(P_A,Q_A\) are forbidden;
bare \(P,Q\) are lemma-local dummy probability measures only after a nearby type declaration.

The pointwise coarse object is one normalized recognition-independent Markov kernel
\(C_A:\mathsf Y_I\rightsquigarrow\mathsf Z_A\), not a matrix or deterministic map. A moving
deterministic map is \(c_t\) only after a flow is declared. The parent model evaluation is
\(\operatorname{ev}_A:m_A\mapsto K^{X_A}_{A,m_A}\). At locally fixed \((o,X)\),
\(q_A^b,q_A^m\), \(p_A^b,p_A^m\), and
\(\boldsymbol\Pi_{A,o,X}^b,\boldsymbol\Pi_{A,o,X}^m\) are derived marginals of their typed full
laws or conditionals; historical root \(Q_q,Q_m\) are scoped legacy aliases only.

**Population.** Agents `i\in V=\{1,\dots,N\}`. Design `D=\{c_a\}_{a=1}^M`, design index `a`.
State latent `k_i\in\mathbb R^{K}`, model latent `m_i\in\mathbb R^{d_m}`, observation `o_i`.
Stacked latents `Y`, observations `o`. Structural data `X`.

**Gaussian dimensions.** The belief Gaussian fiber has dimension `K`; the model Gaussian fiber has
dimension `d_m`. Equal dimensions are not assumed. Do not write `d_k` for the belief dimension.

**Probability.** Generative kernel `P_\theta(do,dY\mid X)`, density `p_\theta`. Recognition kernel
`Q_X(dY\mid o)`, density `q_X`. Evidence `\log p_\theta(o\mid X)`. ELBO `\mathcal L(Q_X;X)`.
Free energy `\mathcal F=-\mathcal L`. Relative entropy `\KL(\cdot\Vert\cdot)`.

**Interaction records and attention.** A factor `a` owns one normalized record kernel
`K_a(y_{\partial a},do_a)`. At a regular record its fixed negative log density is `E_{a,o}`.
Coordinate-local VFEs include every incident factor, while the global joint owns each record once.
For directed attention, `\pi_{ij}` is the generative source prior, `\beta^P_{ij}` the generative
posterior row, `\beta^Q_{ij}` the recognition row, and `\alpha_i^x` the external normalized receiver
occupancy in channel `x`. The marked event laws are `\eta_{ij}^q=\alpha_i^q\beta_{ij}` and
`\eta_{ij}^m=\alpha_i^m\gamma_{ij}`. Exact coarse attention pushes
`\eta`, not `\beta` alone.

**Gaussian information form.** Natural parameters `(h,J)`, moments `\mu=J^{-1}h`, `C=J^{-1}`.
Log normalizer `A(h,J)` — **note the clash**: use `\mathsf A(h,J)` for the log normalizer so it does
not collide with the self terms `A_i`.

**Interaction family.** Precision `\Lambda`, self terms `A_i\succeq0` (`K\times K`), edge weights
`W_{ij}=W_{ji}\succeq0` (`K\times K`), with
`\Lambda_{ii}=A_i+\sum_{j\neq i}W_{ij}` and `\Lambda_{ij}=-W_{ij}` for `i\neq j`.
Laplacian part `L`. Trivialized coordinates `z_i=U_i^{-1}\mu_i`.

**Coarse-graining.** Partition into clusters `I,J`. Aggregation matrix `S` (`0/1`, `\hat S\otimes I_K`).
Coarse precision `\Lambda_{\mathrm c}=S^\top\Lambda S`. Cluster size `n_I`, block size `b`.
Orthonormal bases: `B` spans `\operatorname{range}(S)`, `B_\perp` its complement.

**General scale diagram.** Choose one target category `\mathscr K`: deterministic maps, normalized
Markov kernels, topological vector spaces with continuous linear maps for an operator state, or an
explicitly declared product category for a mixed state. The analytic operator tier uses Banach
spaces and bounded linear maps. A state functor assigns `\mathfrak X_\ell`, which records the level base, the common
principal bundle, both associated bundles and their induced connections, the cross-bundle morphisms and
their defects, and any declared law or operator components. Every coarse arrow
`C_{\ell k}:\mathfrak X_\ell\to\mathfrak X_k` is a morphism in `\mathscr K`; one symbol is never
simultaneously treated as a map, a kernel, and an operator. Abstract arrows compose as
`C_{kr}\circ C_{\ell k}=C_{\ell r}`. Separately, right-acting kernels use
`K_{\ell r}:=K_{\ell k}K_{kr}` so that
`(\mu K_{\ell k})K_{kr}=\mu K_{\ell r}`. A reference-space expression using
`I_\ell^{-1}` requires declared isomorphisms
`I_\ell:\mathfrak X_\ell\xrightarrow{\sim}\mathfrak X_\star`. Reference-measure transformations
remain explicit, so a density Jacobian cannot be hidden inside a coupling rescaling. Only such
identifications produce endomorphisms with ordinary fixed points. A scale-independent endomorphism
is autonomous; a scale-dependent sequence is a cocycle, with periodic points, invariant sections,
or monodromy fixed points as separately typed notions.

**MVG operator component.** In the multivariate-Gaussian realization, with rescaling
`\zeta_\ell>0`, the precision component of the scale diagram is
`\Lambda^{(\ell+1)}=\zeta_\ell^{-1}S_\ell^\top\Lambda^{(\ell)}S_\ell`.
This equation is not the definition of the general RG transformation. Fixed-ray data for this
component are the additive node parameter `x_i`, coupling matrix `M\succeq0`, and self matrix `A`.
For a regular pencil `(L,\Lambda)`, write its finite generalized roots as `{d_a}`; there are exactly
`NK` roots, written `d_1,\dots,d_{NK}`, only when `\Lambda` is invertible. At the singular fixed
operator ray there is no unconditional full list; quotient, mass, and pinning are distinct repairs.

## 4. Label prefixes

`eq:geo-*`, `eq:prob-*`, `eq:gen-*`, `eq:elbo-*`, `eq:exp-*`, `eq:gauss-*`, `eq:restrict-*`, `eq:ig-*`,
`eq:cg-*`, `eq:rg-*`, `eq:obs-*`, `eq:pb-*`, `eq:hist-*`. Chapters `ch:*`, sections `sec:*`, appendix `app:*`.
Use semantic labels `def:*`, `thm:*`, `prop:*`, `lem:*`, `cor:*`, `conj:*`, `open:*`, and
`claim:*` for numbered statements; use `tab:*` and `fig:*` for tables and figures. The text must
refer to labeled objects with `\cref` or `\Cref`, never by a hard-coded chapter or result number.
Revision-order tokens such as `R15` are forbidden.

## 5. Results this document MUST contain, stated correctly

These are established. Reproduce them faithfully; do not weaken or overstate.

**The typing prohibition.** A generative kernel is fixed once `(\theta,X)` is fixed and may not take
a recognition law, a recognition parameter, or **a posterior** as an input. This is a definitional
requirement of the fixed-joint construction and is load-bearing for several later results.

**The exact ELBO.** Under absolute continuity `Q_X\ll P_\theta(\cdot\mid o,X)` and log-integrability,
`\log p_\theta(o\mid X)=\mathcal L(Q_X;X)+\KL(Q_X\Vert P_\theta(\cdot\mid o,X))`, with equality iff
the recognition law equals the posterior as measures. Absolute continuity is a **hypothesis**, and it
is what later forbids degenerate (subspace-supported) recognition laws.

**Interaction family is a declared subfamily.** The Laplacian-plus-self-terms form does NOT follow
from a general linear-Gaussian directed model: an unrestricted state transition contributes an
off-diagonal block that need be neither symmetric nor sign-correct. Give the counterexample
(`\Lambda_i=\begin{psmallmatrix}2&1\\1&3\end{psmallmatrix}`, transition `\begin{psmallmatrix}0&1\\-1&0\end{psmallmatrix}`
gives `\begin{psmallmatrix}1&-2\\3&-1\end{psmallmatrix}`, not symmetric). State the form as a
hypothesis with the condition that makes it hold.

**Graph flatness is a hypothesis.** Coboundary graph links
`\Theta_{ij}=U_iU_j^{-1}` give a clean gauge-covariant sufficient domain because trivialization
turns residuals into plain differences. Pointwise frame comparisons use `T_{ij}`. This graph
condition is distinct from triviality of a principal bundle, zero curvature of a chosen connection,
and trivial connection holonomy on a specified family of base loops.
Under Regime II an internal edge contributes
`(I-\Theta_{ij})^\top W_{ij}(I-\Theta_{ij})` to the coarse self term. This vanishes exactly when
`W_ij^(1/2)(I-\Theta_ij)=0`; only positive-definite or otherwise faithful weights force
`\Theta_ij=I`. A Regime-II coarse operator can therefore leave the family, but need not when its
nonidentity transport lies entirely in weight-null directions. Cut blocks must separately satisfy
symmetry, sign, and diagonal-representability conditions.

**Aggregation closure (Proposition).** `(\Lambda_{\mathrm c})_{IJ}=-\sum_{i\in I,j\in J}W_{ij}` and
`(\Lambda_{\mathrm c})_{II}=\sum_{i\in I}A_i+\sum_{i\in I,j\notin I}W_{ij}`. Internal edges are
annihilated. **Cite, do not claim**: this is the Galerkin coarse operator of aggregation-based
algebraic multigrid, and the block/matrix-weighted case is that method's systems setting.

**Kron reduction is a different operation and is not closed in general.** Unrestricted
matrix-weighted Kron reduction can leave the interaction family; the manuscript gives an exact
rational three-agent counterexample. The broader fixed congruence-diagonal cone
`\mathcal C_H={H D H^\top:D\succeq0\text{ diagonal}}`, including its self terms, is closed because a
fixed congruence reduces elimination channelwise to scalar loopy-Laplacian elimination. Under the
stated closed-convex-cone, SPD-order-unit, independent-coefficient, and positive-scaling
hypotheses, this cone is also maximal. Classification beyond those hypotheses---including
correlated or nonconvex sets, variable congruence charts, and nonflat links---remains open. Never
describe unrestricted matrix-weighted Kron closure as an open conjecture.

**Closure does not select the family.** The continuum `\Lambda_{ij}=-\lambda W_{ij}`,
`\lambda\in[-1,1]`, is PSD and closed under every partition; `\lambda=-1` is the signless Laplacian,
outside the family. Congruence is linear and preserves the PSD cone, so closure is near-vacuous.
Every aggregation matrix factors into pair merges, so "closed under every partition" reduces to
"closed under one pair merge". **What selects the form is translation invariance** — equivalently
purely additive coarse self terms, equivalently no memory of collapsed internal edges, equivalently
consensus as a null direction of the interaction part.

**Contrast with network renormalization, not template.** The uniqueness theorem for edge-independent
random graphs has force because its coarse-graining rule is *nonlinear* in the connection
probability, so additivity of the node parameter must be forced out of a functional equation. Here
the rule is linear and the Gaussian energy is additive from the start, so the same demand yields
nothing. What the functional equation gives here is an **invariant bi-additive family**:
`w(x,y)=xyM` and `\alpha(x)=xA` under a **measurability hypothesis** (without which the Cauchy
equation admits pathological solutions). This is closure under additive push-forward, not by itself
a fixed point. A fixed ray is typed only after a hierarchical identification makes the changing
parameter spaces into one space and the pushed-forward size vector is a positive eigenvector.

**Identification is not a recognition restriction.** A recognition law assigning each cluster one
common value is supported on `\operatorname{range}(S)`, violating absolute continuity, so its cost is
`+\infty`; the regularized cost diverges as `\tfrac m2\log(1/\varepsilon)` with `m=NK-n_{\mathrm c}K`.
Identification is a **generative** construction. The admissible finite operation restricts the
recognition **mean**, with exact cost
`\tfrac12 m_\perp^\top(B_\perp^\top\Lambda^{-1}B_\perp)^{-1}m_\perp` — the **marginal** precision
(Schur complement) of the identified directions, not the restriction `B_\perp^\top\Lambda B_\perp`.
The two agree only when the identified and retained subspaces are `\Lambda`-orthogonal.

**The analyzed costs do not supply a nondegenerate scale.** The mean-tie cost is nonnegative and
vanishes at the finest partition, so minimizing it across partitions selects the finest endpoint
(with possible ties). The determinant gap decreases under merging, so the coarsest endpoint is a
generally nonunique minimizer rather than a nondegenerate selector. The volume term has
partition-dependent scale behavior, and mixing the pieces requires a coefficient
not supplied by the bound. This does **not** prove that no intrinsic selection functional exists;
that general question remains OPEN and needs either a nonmonotone functional with a nondegenerate
optimizer or an impossibility theorem.

**Frame sector.** The coarse frame cancels: constituent laws depend on `(U_I,\mu_I,\Sigma_I)` only
through `(m,S)`, so the frame occupies a `K^2`-dimensional orbit. With a **faithful** `\rho_b` the
level set is exactly one gauge orbit (pure gauge); without faithfulness only unidentifiability
survives. Independent obstruction: no left-equivariant permutation-symmetric map
`\mathrm{GL}^+(K)^n\to\mathrm{GL}^+(K)` exists for `K\geq2`, `n\geq2` (order-`n` rotation argument;
no continuity needed).

**Gauge invariance of the generalized spectrum.** `\Lambda` and `L` transform by the *same*
congruence, so the generalized eigenvalues of `(L,\Lambda)` are frame-independent (measured stable to
4.2e-12 under independent `\mathrm{GL}(K)` frames). Absolute eigenvalue criteria are frame-dependent
and inadmissible; any invariant must be stated in generalized-eigenvalue form.

**Sylvester collapse.** `M` is defined only up to congruence `M\mapsto h^\top Mh`. By Sylvester's law
of inertia, congruence orbits of a PSD matrix are determined by **rank alone**, so the internal
universality label is an integer `0\leq r\leq K` with exactly one class in the nondegenerate case.
No continuous internal moduli survive in that one Gaussian coupling matrix. This does **not** prove
that all remaining variety is one spectral exponent: existence, convergence, invariance, and
completeness of any exponent are separate open obligations, and a general belief family has no
reason to share the Sylvester collapse.

**Rescaling is required and is a declaration.** Aggregation composes as a precision-increasing
semigroup; without a declared `\zeta_\ell` there is no flow and the question of a fixed point does not
arise. The document declares one and says so.

**Bi-additive closure and the finite gate.** `W_{ij}=x_ix_jM`, `A_i=x_iA` with `x` additive is closed
under additive push-forward: `W_{IJ}=x_Ix_JM`, `A_I=x_IA`. It is not invariant in one fixed parameter
space until a hierarchical identification is declared. On the identified homogeneous complete-graph
endomorphism, dense rescaling fixes the common coupling ray and contracts the self term.
**Attraction on an infinite hierarchy is open.** A finite blocking sequence terminates and cannot
establish asymptotic convergence.
Numerical gate (report as numerical evidence, not proof): the homogeneous endomorphism
`A'=bA`, `W'=b^2W` has spectrum `\{b^2\}` with multiplicity `K(K+1)/2` and `\{b\}` likewise, so the
contraction ratio against the largest eigenvalue **outside the dominant eigenspace** is `1/b`
(`=0.5` at `b=2`); self terms are irrelevant; within the coupling sector the map is a scalar so `M`
is not selected, corroborating the Sylvester collapse. Finite heterogeneous blocking moves the
reported diagnostics toward the bi-additive form in both a matrix-separability and a spatial-rank-one measure, controlled against
freshly drawn systems at matched size (flowed/null reaching 0.148 spatially and 0.014 in the matrix
sector); the raw spatial measure rises at small `N` for finite-size reasons and that is why the null
control is necessary. These finite measurements neither supply an infinite orbit nor prove
convergence. The `\lambda=-1` control is distinguished (its self sector grows rather than decays).

**Universality remains a program.** Rank is an established discrete label for the Gaussian coupling
matrix under full congruence. A spectral exponent is only a candidate continuous label after a
positive reference form, a thermodynamic family, and convergence of the normalized counting
function have been declared and proved. No result shows that rank plus one exponent is complete,
that an orbit converges, that a component has a unique limit, or that the result is
blocking-scheme-independent. The component theorem gives independent operator orbits, not a shared
reached law. The proposed **running** of effective couplings is therefore conditional on a declared
flow and still lacks a quantitative prediction. The claim labeled
`claim:physical-law-identification`---identifying a repaired fixed object with a physical law or
empirical regularity---remains **OPEN/INCONCLUSIVE**; it is not closed by a definition, numerical
trend, or interpretive preference.

## 5b. Non-trivial topology, and the coarse-graining criterion (added 2026-07-28)

The manuscript treats the flat and non-flat regimes **both**, and does not assume the flat one away.
Every such statement is channel-typed. A belief-sector comparison or graph link does not determine
its model-sector counterpart, and neither determines a cross-bundle morphism.

**Four independent notions.** The transition functions of the principal bundle form a nonabelian
Cech cocycle. Belief- and model-frame atlases on the same `P` produce cohomologous cocycles, not
two independent topology classes. The class being a coboundary is equivalent to principal-bundle
triviality over the covered region and to the existence of a global principal section. Independently declared graph
links `\Theta` are graph-flat on a subgraph exactly when every graph-loop product is the identity,
equivalently when those links are a graph coboundary there. A chosen principal connection is flat
when its curvature vanishes. Its holonomy is trivial only on the specified loops for which parallel
transport is the identity; a flat connection can retain nontrivial monodromy on a noncontractible
base. None of these implications may be substituted for another without the curve-assignment and
transport-identification hypotheses. Singletons and trees are automatically graph-trivializing,
but say nothing by themselves about bundle topology or connection curvature.

**The coarse-graining criterion, derived and not posited.** For a connected cluster with
positive-definite represented internal edge weights, the exact coarse fixed-section fiber is
`F_I=Fix(Hol_I)`, and its retained rank is `f_I=dim F_I`. Trivial represented holonomy is therefore
necessary and sufficient for full fixed-dimension coarsening (`f_I=K`), while
`0<f_I<K` gives exact partial fixed-section coarsening and `f_I=0` leaves no retained cluster
degree. The proof must identify the kernel of the connection Laplacian with the holonomy-fixed
space by spanning-tree transport. Principal holonomy may nevertheless be nontrivial when the
selected representation is not faithful. With merely positive-semidefinite weights, the exact
edgewise constraint is `W_e^(1/2)(z_i-Theta_e z_j)=0`; nonidentity transport and loop holonomy may
survive in weight-null directions. Those effective-support cases require their own typed quotient
or constraint fiber. Three things about this criterion must be stated wherever it is used.

It is an **admissibility** criterion, not a **cost** criterion. It compares no bounds across latent
inventories, needs no complexity coefficient, and needs no externally declared scale. The
manuscript's analysis of the available costs remains separate: those costs select trivial endpoints
or require an external coefficient, while the existence of some other intrinsic selector is open.

It **does not select a partition**. Singletons are admissible. What is well posed is the family of
maximal trivializing clusters, and choosing among admissible partitions remains subject to the cost
obstruction.

It is **not a consensus-of-beliefs condition**. Two agreements are independent and must never be
conflated: *frame agreement* is trivial internal holonomy, meaning a common trivialization exists,
and is the criterion; *belief agreement* is coincidence of the means, which is the null direction of
the interaction Laplacian and the degenerate mode the renormalization chapter penalizes. Agents may
hold sharply different beliefs while their frames trivialize, and identical beliefs under nontrivial
holonomy. Prefer the phrase "common trivialization" and avoid "consensus" for the criterion.

**What is closed, and what remains open, in the non-flat case.** Positive-definite internal weights
give the exact fixed-section fiber above. Positive-semidefinite weights give the exact edgewise
constraint space, but its canonical effective-support quotient is not classified. When an invariant
quotient is available it may be used; without one, rectangular cellular-sheaf endpoint maps reproduce
the Galerkin energy exactly and remain closed under nested blocking. If one insists on the original
fixed-`K` link family, every cut block must still satisfy the symmetry, sign, and
diagonal-representability conditions. Canonical minimal compression, compression to one invertible
transporter and one SPD weight, compatibility with normalized laws, and RG rescaling remain open.

**The tension to record rather than resolve.** The declared full-`K` coarse-graining domain uses
trivial represented internal holonomy, and under positive-definite weights that condition is
necessary and sufficient for `f_I=K`. Nontrivial holonomy may still permit exact partial
fixed-section or rectangular-sheaf coarsening. By contrast, the flat unanchored parallel-edge fold
singularity is *relieved* by visible nontrivial holonomy, since
`dim ker J = dim ker(H - I)`. Holonomy confined to weight-null directions is a separate
effective-support case. The full-rank coarse sector and the unanchored fold therefore pull in
opposite directions only after the represented support and edge copies are specified.

## 5c. The interpretive chapter

The interpretive chapter states interpretation and proves nothing. **No interpretive claim may carry
`ESTABLISHED`.** Declared readings are `DEFINITION`; interpretive commitments the mathematics
actually uses are `HYPOTHESIS`; readings with unsettled consequences are `OPEN`. Where a position is
merely *available* rather than supported, say so and say what would support it. Graph-link holonomy
on the finite interaction complex, smooth base-connection holonomy, and principal-bundle topology
are different objects; no interpretive paragraph may infer one from another. The possibility that a
specified base connection has an operational population-level trace is a conjectural extension, not
a result. The participatory reading and the noumenal reading pull against each other and the
formalism does not adjudicate; set out what each buys and costs.

## 5d. The general theory, and the Gaussian as an example (added 2026-07-29)

**The multivariate Gaussian is a worked realization, not the ambient theory.** The hierarchy below
is mandatory. A statement may move down it only by naming the additional hypotheses it consumes.

### 5d.1 Ambient fibers and the selected smooth tier

At the most general tier, a state-recognition belief fiber is a declared collection of normalized
probability laws on a declared measurable state space. A model-belief fiber is likewise a declared
collection of normalized probability laws on its declared model-parameter or latent-model space.
Distinct from both is a generative-kernel fiber: a declared collection of Markov kernels between
specified source and target measurable spaces. Do not identify either law fiber with a kernel
fiber, and do not infer a manifold, common dominating measure, affine chart, natural parameter,
convex cone, boundary, or Fisher metric merely because the elements are beliefs or models.

The two law fibers are carried by the separate associated bundles
`\mathcal E_b=\mathscr P_G\times_{\widehat\rho_b}\mathcal B_b` and
`\mathcal E_m=\mathscr P_G\times_{\widehat\rho_m}\mathcal B_m`. The representations of the common group `G`
may be inequivalent and may act on different-dimensional fibers. The cross maps `\Phi` and
`\widetilde\Phi` are declared morphisms of these associated bundles over
`\operatorname{id}_{\mathcal C}`. Their existence is additional structure: the relative principal
frame `h_i` does not supply them, and inequivalent linear representations admit a nonzero linear
cross map only when an appropriate intertwiner exists. Neither map forces equal ranks, inverse
maps, or parallelness. A shared-frame model imposes `u_i^b=u_i^m`; it does not follow merely from
using one `\mathscr P_G`. Compatibility with either of the two connections remains a separate condition.

The selected differential tier is a finite-dimensional smooth **parametrized-measure model**. State
its parameter manifold and require differentiability in quadratic mean, square-integrable score
fields, the integrability needed by each tensor or derivative, and nondegeneracy of the Fisher form
before calling that form a Riemannian metric. A degenerate Fisher tensor is still a tensor but not a
Riemannian metric. These are hypotheses on the selected model; they are not inherited by arbitrary
law or kernel fibers. Statements for changing supports or null sets must be formulated at this
parametrized-measure level rather than smuggled through one fixed density chart.

### 5d.2 Tractable subclasses

A dominated finite-dimensional canonical exponential family is a further subclass, with declared
reference measure `nu`, statistic `T`, natural parameter `theta`, log partition `A(theta)`, and
natural domain `N={theta:A(theta)<infinity}`. Regularity and minimality are separate hypotheses.
Only in this subclass do the affine natural chart, Bregman formulas, and Hessian representation of
Fisher information follow.

A graph-exponential representation is a further declaration: node and pair statistics, a
graph-indexed affine energy, and a diagonal-affinity condition. A closed operator cone is yet another
separately declared structure on that finite parameter space. Neither the graph representation nor
the cone is universal, and the cone need not be the closure of the natural domain.

The multivariate Gaussian is the quadratic realization of this chain. Its information parameter is
`(h,J)` with `J` positive definite on the probability layer. The interaction family is a declared
operator subcone of the Gaussian quadratic parameters, not a consequence of all Gaussian models.

### 5d.3 Boundary statement and repairs

The proposed scale-free ray with vanishing self terms is a boundary operator in the **Gaussian
interaction representation**: its precision is singular, so it has no full-space Gaussian
normalizer, no Gaussian Fisher metric there, no recognition law to which the exact ELBO applies, and
an irregular endogenous pencil. These are one Gaussian natural-domain fact seen through four
functionals. Do not promote this to a theorem that every general belief fiber has a natural-domain
boundary, or that every flow on beliefs has the same failure.

Do **not** silently substitute a pseudoinverse or pseudodeterminant. Pinning, quotienting, and
retaining a mass sector each change or enlarge the object and must be declared. Their algebraic
definitions do not complete the cross-scale probability theory: compatible quotient measures and
bounds, pin dependence, and mass scaling remain open where the manuscript says they do.

### 5d.4 Coarse maps and conditional closure

For arbitrary laws, coarse-graining may be represented by a declared Markov kernel and its
pushforward. For the graph-exponential operator subclass, the operation used in this manuscript is
different: the sample-variable identification maps a coarse configuration into the fine sample
space, and aggregation **precomposes the unnormalized energy** with that map. Affinity in the
parameter and diagonal affinity of the pair statistic then induce a linear parameter map. A coarse
reference measure, integrability of the pulled-back energy, and its finite normalizer are three
separate obligations; none follows from the algebraic parameter calculation.

Invariance of a pair statistic under a declared site action supplies a conditional selection
principle. Translation invariance is the Gaussian difference-statistic instance. Internal-edge
annihilation follows from constant diagonal restriction; translation invariance implies that
condition but is not equivalent to it without an additional off-diagonal hypothesis.

For a channel-typed law fiber with bimeasurable represented transports, transport each marginal to
one root and minimize weighted forward KL over a declared holonomy-fixed parent-law family. The
resulting infimum is independent of paths, root, and frame. When the infimum is attained, it is zero
exactly for a holonomy-stabilized parallel marginal-law section. An empty fixed family gives
infinite distortion; without attainment, zero infimum proves only approximability. This theorem is
a marginal-law statement. It neither selects a partition nor supplies a normalized coarse channel,
and exact joint recovery still requires a parameter-independent coarse Markov kernel with a common
recovery kernel.

### 5d.5 What remains realization-specific

The determinant gap, the Schur-complement mean-tie cost, explicit Gaussian Fisher charts, matrix
pencils, Loewner-order arguments, the Sylvester classification, the reciprocal-pair determinant,
and the exact Kron counterexample and common-eigenbasis theorem are **Gaussian quadratic results**.
Where a general analog is plausible but unproved, mark it `OPEN` and state its extra category,
integrability, closure, and attainment obligations. General statement first, realization second;
never use Gaussian notation as if it proved a theorem about all belief or model fibers.

## 5e. Covariant pullbacks and timeless inference histories (added 2026-08-01)

**The base is fixed and timeless.** A curve in `\mathcal C` orders contexts; it is not an agent
history. Belief/model updating at one `c` is a vertical curve in the product of the two statistical
fibers. Evolution of the full agent over `\mathcal C_i` is an oriented curve in a declared section
space, whose pointwise evaluation velocities are vertical. A curve over changing base points is
horizontal only relative to a chosen connection; a general such curve is mixed. Tensors pull back
through sections, while base curves push forward through them. A statistical-fiber curve descends
to the base only when it lies in the section image, with local and global injectivity hypotheses
stated separately.

**The covariant pullback is connection-relative.** On the selected smooth tier, require the
represented group action to preserve each vertical Fisher and Amari--Chentsov tensor. Then
`(D^{\omega_x}\sigma)^*g_x^F` and the analogous cubic tensor are global and gauge invariant.
Ordinary derivatives of local representatives are forbidden as global pullbacks. Under a change
of connection `\omega_x' = \omega_x+a`, display the exact linear and quadratic correction terms;
there is no connection-independent metric derived from the principal bundle alone.

**Semimetric, quotient, and foliation are distinct.** With positive-definite vertical Fisher
metric, the radical of the pullback is exactly `\ker D^{\omega_x}\sigma`. It is a Riemannian
metric only when this map is injective. At constant rank the quotient vector bundle by the radical
inherits a metric, but it is not automatically the tangent bundle of a quotient manifold.
Frobenius involutivity, a simple regular foliation, and basicness of the tensor are separate
hypotheses. Include a rank-jump witness and a constant-rank nonintegrable contact witness.

**VFE selects an orbit only after a metric or mobility is declared.** Descent of `\mathcal F`
alone supplies neither a path nor a speed. On a regular metric or quotient-metric configuration
space, the positive ray of `-\operatorname{grad}\mathcal F` defines the oriented unparameterized
natural-gradient orbit. Positive scalar mobility changes only parameterization; anisotropic
mobility can change the orbit. A semidefinite metric may not be inverted before a justified
quotient or separately declared regularization.

**An exact multi-agent VFE requires a joint-law lift.** A pair of displayed marginal belief--model
sections does not determine a correlated recognition law. Declare a smooth extraction map from an
admissible conditional- or full-law manifold to the agent configuration and a smooth right-inverse
`\iota_i`; require the lifted law to reproduce the displayed configuration. With the outside
marginal fixed, the differentiable block objective is the outside-averaged conditional VFE, under
the support, finiteness, integrability, and differentiation-under-expectation hypotheses of the
local--global potential theorem. Its differential then equals the differential of the collective
VFE restriction. The exact recognition Fisher metric is the pullback of the conditional/full-law
Fisher metric along `\iota_i`, or its justified quotient. A weighted sum of marginal Fisher metrics
is exact only after a separate block-orthogonality or fixed-dependence result.

**Governing finite-lift correction (2026-08-14).** The general lift obligation above remains open,
but it now has one exact nonproduct witness. For three paired binary agents, the declared family
p_kappa = p_0 + kappa chi D, with fixed |kappa| < 1, is a strictly positive normalized smooth right
inverse of the six one-bit marginal map and an immersion. Every proper marginal remains the
corresponding product marginal. For each fixed marginal tuple, this is one parity line in the
57-dimensional Frechet fiber, not a construction of arbitrary paired-joint laws. It is equivariant
under simultaneous complement of both typed channels of an agent and typed agent permutations.
An odd independent channel complement changes kappa's sign, so it requires a pseudoscalar kappa; no
within-pair belief--model swap, GL(K) action, Lie connection, intervention map, or canonical agency
follows.

For any regular joint score, use the exact residual
G_J - G_w = K - C + sum_i (1-w_i)G_i, where K = E[RR^T] and the ordered signed cross tensor is
C = sum_{i ne j} E[L_iL_j^T]. Equality on a declared tangent subspace means that this bilinear
residual restricts to zero there. In the parity witness, pairwise independence gives C = 0 and K is
positive definite for nonzero kappa. At the symmetric point c = kappa/64,
G_J = 4I_6/(1-c^2); equality with a weighted marginal metric on the full tangent requires every
w_i = 1/(1-c^2), and unit weights agree only at kappa = 0. Do not generalize this ordering: the
older two-bit lift has a signed, indefinite joint-minus-product Fisher difference. The symmetric
posterior is realized by the supplied hyperedge record K_hyp(1|x) = (1+c chi(x))/2; it is engineered
generative data, not a consequence of pairwise locality or conditional independence. The
arbitrary-family, coarse-preservation, continuum, physicalization, time, units,
and renormalization obligations remain open.

**Governing canonical-dependence-selection correction (2026-08-14).** The selection question is now
split by quantifier. For finite typed lists, naturality under
fixed-arity coordinatewise finite Markov kernels whose channel randomness is independently tensored
uniquely forces the product section; preparation arrows already determine it. This is not a theorem
about arbitrary kernels in `FinStoch`. If that local class is enlarged to a wide
marginal-compatible category, a natural section exists if and only if every added morphism preserves
product laws, and the section is then uniquely the product section. Thus the product-preserving
marginal-compatible kernels form the maximal such wide category.

The frozen selector contract separately declares the two arity-increasing split kernels
`R_rho(y,z|x) = 1[y=x]((1+rho)/2 if z=x, else (1-rho)/2)` at `rho=1/3` and
`rho=1/2`. On a fair source bit both descend to the same fair/fair marginal datum, but their
pushforward atom multisets are respectively `{1/3,1/3,1/6,1/6}` and
`{3/8,3/8,1/8,1/8}`. A single-valued target section natural under both declared splits would have
to return both unequal laws, even modulo sample relabeling. The declaration of both splits and the
single-valuedness requirement are load-bearing. Hence an absolute selector with those quantifiers is
**REFUTED**, rather than open. Under the declared full naturality and canonicity requirements, one
must either restrict the admitted morphism class or add declared relational, constraint, or reference
data to select nonproduct dependence.

One bounded relative replacement is exact in the finite setting. Given a declared reference law
`p`, statistic `T`, and target moment `m`, a finite-KL minimizer of `D(q||p)` subject to
`E_q T=m` exists exactly when
`m in conv T(supp p)` and is then unique as a law, with support
`{x in supp p : T(x) in F_m}`, where `F_m` is the minimal face of `conv T(supp p)` containing `m`.
Its equivariance requires coherent transport of the reference and the
complete constraint diagram. For a deterministic coarse map `f:X->Y` and `r << f_#p`, the unique
conditional-KL completion is `L_f^p(r)(x)=r(f(x))p(x)/(f_#p)(f(x))` on positive reference fibers and
zero otherwise. Such completions compose strictly along nested deterministic coarse maps when each
stage uses the pushed reference. Descent of the retained optimizer and optimum VFE additionally
requires the declared complete retained-law/conditioning equivalence and one common feasible retained
problem; envelope differentials need the stronger positive `C^1`, fixed-support-stratum, and unique
`C^1`-optimizer hypotheses.

For a smooth retained-law map `rho:Theta->N` and positive-semidefinite target tensor `g`,
`rad(rho^*g)=d rho^{-1}(rad g)`, and this equals `ker d rho` exactly when
`im d rho` meets `rad g` trivially. Constant rank then gives a positive-definite quotient vector
bundle, not automatically a global quotient manifold; the latter still needs a simple Hausdorff
null-leaf quotient. Under that transversality equality and a regular connected-leaf quotient, the
specific pullback `rho^*g` is basic because `rho` factors through that quotient. This does not make
arbitrary tensors, declared block projectors, or the `05c` connection-relative covariant jet
automatically basic. Declared block directness also requires blockwise kernel splitting, energy
additivity requires Fisher orthogonality, and block descent requires projectable/basic image data.

The recovery statements remain independently typed. Full-joint VFE and full-joint Fisher tensors do
not factor through singleton marginal data. The governing finite typed-intervention correction is
bound to target digest
`efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874`.
Its raw groupoid `FinTIP_(R,O)^iso` contains finite normalized typed DAG presentations and all
partial hard assignments. Their total right-override monoid `A_P` is reduced by the two-sided
congruence that equates contexts exactly when every left/right contextual retained response agrees.
This gives the well-typed functors
`Red : FinTIP_(R,O)^iso -> FinRIE_(R,O)^iso` and
`Ubar_pass : FinRIE_(R,O)^iso -> FinObs_(R,O)^iso`.

The operational-extension certificate is bound to target digest
`af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1`.
For any fixed protocol monoid `A` and response `Phi`, contextual equivalence is the largest
two-sided congruence contained in `ker(Phi)`. Every response-compatible quotient
`q:A->B` with `Phi=psi q` has one unique surjective unital factor
`B->Syn(Phi)` over `A`. Thus `Syn(Phi)` is terminal from finer to coarser quotients and
contextually fully abstract relative to the fixed operational data. If `A` is finite, it has
minimum protocol-class cardinality, and equality of cardinalities gives the unique isomorphism
over `A`. The cardinality statement is finite-only and does not minimize or canonically recover a
raw latent state space, DAG, kernel family, parameterization, or computational realization.

If `A` is a compact metrizable topological monoid, multiplication is jointly continuous, `Phi`
is continuous into a metrizable Hausdorff response space, and `D` is a countable dense context
set, the signature `S_D(a)=(Phi(uav))_(u,v in D)` realizes the contextual quotient as a compact
metrizable image. Its multiplication and response are continuous. The same terminal factor is
continuous for compact-Hausdorff response-compatible triples whose `q` and `psi` are continuous
and whose `q` is a quotient map. Compactness and the quotient-map hypotheses are load-bearing.

Inside the declared BSC subcategory,
`L(1/4,1/3)` and `L(1/3,1/4)` have one raw structural signature and the same complete passive
retained law `(7/24,5/24,5/24,7/24)`, in lexicographic retained-coordinate order
`(R,O)=(0,0),(0,1),(1,0),(1,1)`, but their fifteen-class reduced experiments are
nonisomorphic. The first model's `do(E=0)` response `(1/3,1/6,1/3,1/6)` is absent from the
complete second-model response image under all four admitted typed boundary flips. This full
response-image obstruction is load-bearing; unequal mediator total variation is diagnostic only.
An independent isolated null node collapses under the same two-sided quotient and is a control, not
the negative certificate. The frozen universal target is therefore `COMPLETE_NEGATIVE`.

Accordingly, `Ubar_pass` is not essentially injective and no universal reconstruction satisfies
`R Ubar_pass ~= id_FinRIE` on that subcategory. A conventional representative-selecting section
`Ubar_pass R ~= id_FinObs` remains allowed.

The same BSC pair with equal passive retained law is nonisomorphic on the marked normalized soft mediator face.
For `0<epsilon<1/2`, its exact total-variation diameters are
`(1-2epsilon)/3` and `(1-2epsilon)/2`; every
`epsilon<s_-<s_+<1-epsilon` gives the strict-interior separation
`|1-2b|(s_+-s_-)`. The theorem retains the mediator target, keeps `R` as input/parameter and
`O` as output/observation, and uses one protocol-independent response intertwiner. It does not
admit target erasure, boundary exchange, or time reversal.

For the released fifteen-class hard monoids, independently randomized selectors form the affine
convolution monoids `Delta(S)`. The complete contextual vectors have an exact minor
`det M(b,delta)=(2b-1)^6(2delta-1)^3/32`, nonzero for both models at
`delta=5/12`. Randomized contextual equivalence is therefore equality, and an admitted affine
unital convolution-monoid isomorphism would preserve simplex vertices and restrict to the
already-refuted hard isomorphism. This proof is not the old unmatched-response proof:
convexification makes that hard response a `5/6,1/6` mixture in the other model. Correlated or
shared-noise selectors require a joint selector object and are not covered.

For a finite DAG of standard-Borel node spaces, declared standard-Borel palettes and normalized
pointwise kernels with jointly measurable evaluations give a Borel retained response by finite
topological-order recursion. The construction supplies an algebraic quotient but does not by itself
establish a standard-Borel or smooth quotient; that requires an exhibited smooth classifier or
stronger topology. On the stronger compact-Polish, compact-palette, isolated-bottom, jointly Feller
tier, the finite-coordinate right-override monoid and weak retained response are continuous, so the
compact quotient theorem applies. Finite-coordinate does not mean finite cardinality.

A smooth compact-Feller witness is supplied by circle heat kernels. For `0<s<t`, the ordered
chains `m(dR)H_s(R,dE)H_t(E,dO)` and `m(dR)H_t(R,dE)H_s(E,dO)` have the same passive retained law
`m(dR)H_(s+t)(R,dO)`. With mediator palette `P(T)` and constant-parent preparations, `H_s`
strictly Blackwell-dominates `H_t`, and
`{nu H_t}` is a proper subset of `{nu H_s}`; the positive smooth witness is
`nu_rho=H_rho(x_0,dot)` for `0<rho<t-s`. The comparison preserves the marked mediator, circle
heat geometry, ordered boundary, compatible protocol map, and one global response map.

These results supersede the earlier blanket `INCONCLUSIVE` or open wording only in their frozen
hard, marked-soft, independently randomized, declared standard-Borel, compact-Feller, and circle
categories. Target-erasing soft morphisms, correlated/adaptive selectors, identification of
null-version point interventions from almost-sure passive observational conditionals, noncompact quotients, arbitrary latent dilation, minimal
raw realization, autonomous agency, base-manifold continuum/gauge/RG extension, fixed-observation
ELBO or VFE equality, and every physical or ontological identification remain **OPEN**.

**Governing full pointwise probabilistic-datum correction (2026-08-15).** The released package is
bound to target digest
`15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87`. Its manuscript theorem is
**ESTABLISHED**; its package ledger records `target` as `EVIDENCE_VERIFIED`, and `release.json`
records `COMPLETE_AFFIRMATIVE_WITH_CORRECTIONS` (the mathematical content is unchanged; two of four
domain approvals are stale, one provenance stage is unauditable, and the adversarial rejection count
is not evidence — see
`docs/derivations/2026-08-15-full-pointwise-meta-agent/POST-RELEASE-CORRECTIONS.md`).
Fix a nonempty finite child block `I`, a parent label `A`, one
`r_* in U_A = intersection_{i in I} C_i`, fixed structural `X`, and `X_A=chi_A(X)` outside the
random channel. One normalized recognition-independent
`C_A:Y_I rightsquigarrow Z_A`, with the observation space `O` unchanged, pushes the fixed fine
generative joint, selected posterior-version family, and correlated recognition law to the
normalized parent triple `mathbb P_A`, `boldsymbol Pi_A`, and `mathbb Q_A`. The selected parent
posterior identity holds at the observation-kernel level, not by applying an almost-sure equality at
an arbitrary exceptional observation.

The parent model coordinate has a generative interpretation only through a jointly measurable
normalized evaluator. Standard-Borel disintegration supplies an induced evaluator; a predeclared
evaluator requires separate almost-sure compatibility with the selected parent conditional. Belief,
model, prior, and posterior marginals are forward coordinate projections of their typed full laws and
do not reconstruct those laws. The common-channel KL chain is additive in `[0,+infinity]`. Adding
the same finite real `-log p_X(o)` to both KL terms gives an extended-real VFE identity; a finite
VFE may be negative. Without a finiteness premise, `Delta_A=0` exactly when the discarded
conditional recognition and posterior laws agree `mathbb Q_A`-almost surely. Finite fine KL is
required for ordinary subtraction `F_I-F_A=Delta_A` and for the stated two-way pairwise
common-recovery equivalence; family-wide recovery requires simultaneous hypotheses for every member.

Holonomy blindness is conditional on typed fine and parent actions, full fine-law covariance,
compatible selected posterior versions, `C_A` equivariance, and evaluator covariance. Same-slice
invariance at fixed `(o,X)` follows only for isotropy arrows fixing that slice and its selected
versions. The alternative retains raw root-framed holonomy and boundary marks and makes no blindness
claim; neither branch selects membership. Canonical channel or partition selection, family-wide
recovery, the comparison category, gluing over `U_A`, parent local sections, a geometric meta-agent,
autonomy, agency, nonequilibrium persistence, continuum limits, physical time, a unique DAG or
microscopic physics, and ontology remain **OPEN**.

Finally, when `kappa` is promoted in the six-bit parity family, the full-joint map has rank seven
everywhere, whereas singleton retention has rank six with kernel exactly
`span{partial_kappa}`. This identifies `kappa` only as a full-joint interaction direction lost by
singleton retention; rank does not type or agentize it. Arbitrary-family and coarse-preserving lifts,
physical geometry, physical time, dimensional units, and renormalization remain **OPEN**.

**Emergent duration is Fisher length on an already selected orbit.** The oriented inference orbit
inherits the Fisher line element, and integration from a chosen origin defines an agent-relative
information clock invariant under orientation-preserving reparameterization. Fisher supplies
duration and the VFE natural-gradient ray supplies orientation. The clock can stall on null or
critical segments and need not extend to a global scalar on configuration space. A global
orthogonal unit-speed clock requires exactness of the normalized VFE one-form, including vanishing
periods. Do not identify this construction with physical time. A continuum section-space clock
also requires a declared base measure, channel weights, and gauge-quotient rule; without them only
pointwise or finite-design clocks are defined.

In an infinite-dimensional section space, free, proper, and isometric gauge action alone does not
guarantee the quotient-speed formula. Require a smooth principal quotient, closed split
orbit-tangent subbundles, and smooth orthogonal complements, equivalently a declared
Riemannian-submersion or mechanical-connection structure. The familiar free/proper/isometric
sufficiency applies directly only in the finite-dimensional regular case.

**Operational and meta-agent geometry is a Markov statement.** A parameter-independent normalized
record channel replaces a score by its conditional expectation and contracts Fisher information
by the exact conditional-covariance defect. The result applies to the coarse image of the same
fine orbit. It does not compare independently recomputed fine and meta natural-gradient orbits
without an oriented semiconjugacy. A parameter-dependent channel, a fitted coarse approximation,
a Galerkin restriction, and a generative-versus-recognition parameter mismatch lie outside the
contraction theorem.

**Cross-scale first jets require descent and connection compatibility.** A fine section determines
only a section of a pulled-back coarse bundle until it is constant on fibers of the base coarse
map. If fine and coarse sections are related and the bundle morphism preserves horizontal lifts,
their covariant first jets commute. Otherwise retain the explicit vertical connection-mismatch
term. Under a genuine Markov fiber map, the pulled-back coarse Fisher tensor is bounded by the
fine tensor and the information-loss defects add under composition. This scale index is RG depth,
not physical time.

## 6. Obstructions chapter — state these as results, not apologies

**The flat unanchored reciprocal fold is inadmissible; cyclic Gaussian models are not.** Represent
the two-node fold by two distinct parallel edge copies traversed in opposite directions. Each copy
separately obeys the inverse-orientation rule; the two copies need not be inverses. If their
parallel-edge loop is flat, the assembled precision is singular for every SPD link covariance,
with kernel the transport-consistent configurations. If the fold is not part of a fixed generative
joint, there is no evidence for the exact ELBO to bound. Proper SPD anchors restore definiteness,
and a globally normalized cyclic Gaussian Markov random field is legitimate; its partition
function is part of the model and generally depends on the declared transports. Never generalize
the scoped no-go to all cycles or all reciprocal models.

**Bayesian posterior flow is a separate construction.** It neither repairs nor violates the fold
theorem by itself. Composing a posterior flow with this model requires an explicit transition
between normalized models and a common comparison target; without one, differences of ELBOs mix
evidence and tightness. A large-information covariance expansion supplies no conclusion at the
zero-information endpoint. **What survives inside the present model is a declared top prior on a
truncated tower**, or an apex latent with a proper prior — a tree whose exact mean-field coordinate
is precision addition and whose declared prior supplies exactly the coercivity the fold lacks.

**The participatory content survives in the inference, not as a cycle in the model.** At a
variational fixed point each agent's effective prior is constituted by the population's beliefs,
mediated by a latent inside the joint rather than by a kernel reading a posterior.

## 7. Literature — what to use and how

**Draw on the research wiki at `C:\Users\chris and christine\Desktop\Research`.** Read `index.md`,
follow relevant `[[wikilinks]]`, and use `sources/papers/` and `sources/refs/` notes. The notes on
Bayesian renormalization and network renormalization were corrected on 2026-07-28 and are reliable as
of that date; read them rather than re-deriving. The bibliography is
`C:\Users\chris and christine\Desktop\Research\manuscripts\references.bib` — **check whether a key
already exists before adding one**, and never invent a DOI, page range, or quotation.

**Bayesian renormalization** (Berman, Klinger & Stapleton 2023; the Berman–Klinger inverse-flow
companion; the neural-network-field-theory follow-up; and the dynamical-Bayes prequel
arXiv:2204.12939) supplies the Fisher-as-scale idea and the stiff/sloppy vocabulary. Use it for
those. **Do not** attribute to it: a spectral cutoff (its implemented criterion is diagonal), a
statement about singular or near-singular Fisher metrics (its construction implicitly requires
invertibility and it never says so), or a concession that its scheme is merely analogical — its
Discussion in fact claims a one-to-one adaptation of momentum-shell renormalization, so any
disagreement is ours and must be voiced as ours.

**Network renormalization** (the Gabrielli et al. review; Garuccio–Lalli–Garlaschelli for the
multiscale model; Villegas et al. for the Laplacian renormalization group) supplies the contrast of
section 5 and the diffusion-scale construction. Note that the Laplacian construction's specific heat
peaks on structureless graphs as well, so peak existence is not evidence of an intrinsic scale; if
you use it, use the spectral gap and say so.

**Prior art that must be cited rather than claimed**: aggregation and smoothed-aggregation algebraic
multigrid for the coarse operator; matrix-weighted consensus for the matrix-weighted Laplacian as an
object; Sylvester's law of inertia; Birkhoff/Hilbert projective metric contraction for the flow
argument. **What remains genuinely open** and may be claimed as such is the classification beyond
the qualified congruence-diagonal theorem and closure for nonflat connection Laplacians.

## 8. Mechanics

Preamble is in `main.tex`; do not add `\usepackage` lines to chapter files. Chapters are `\input`
and must contain **no preamble and no `\begin{document}`**. Start each with `\chapter{...}` and a
`\label{ch:...}`.

Available: `amsmath`, `mathtools` (so `\begin{psmallmatrix}` works), `bm`, `mathrsfs`, `cleveref`,
`natbib`, `tikz`, `longtable`, and the `sciencetable` environment from `scientific_report.sty`.
The typed-notation appendix uses `longtable`; `sciencetable` is for short tables that fit on a page.

Macros already defined in `main.tex`: `\KL`, `\E`, `\R`, `\given`, `\Tr`, `\Sym`, `\PSD`, `\GL`.
Use them.

Write only your assigned file. Do not edit `main.tex`, `SPEC.md`, or another agent's chapter.
