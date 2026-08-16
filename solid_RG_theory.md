<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87","schema_version":"rigorous-theory-search/v1","target_digest":"15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87"} -->
# Pointwise meta-agent renormalization

For a physicist-facing, standalone LaTeX explanation, see [solid_RG_theory.tex](solid_RG_theory.tex). This Markdown page remains the compact technical and status reference.

This is the repository start page for the strongest certified pointwise result. Fix a finite child block $I$ with parent label $A$ and write

$$
\mathcal U_A:=\bigcap_{i\in I}\mathcal C_i\subseteq\mathcal C,
$$

for its overlap patch. The certificate fixes one base point $r_*\in\mathcal U_A$ and works with a finite network in the single fiber over $r_*$. It does not extend the construction across $\mathcal U_A$ or across the contextual base $\mathcal C$.

The earlier two-channel certificate proved that zero positive-weight transported edge KL is equivalent to one unique common root marginal in each channel. The released full pointwise theorem now supersedes only the resulting marginal-pair boundary. Under its stated standard-Borel, common-channel, evaluator, evidence, and holonomy-branch hypotheses, one normalized recognition-independent channel produces the full parent generative, posterior, and correlated recognition laws, their derived marginals, and the exact conditional-information VFE defect. This is a full pointwise probabilistic datum for a candidate parent. It is not yet a pair of parent local sections, a geometric meta-agent, an autonomous agent, or a dynamical theory.

## Status key

ESTABLISHED means proved in the contained package or in the cited canonical theorem source. CONDITIONAL means exact under hypotheses stated beside the result. DIAGNOSTIC means a finite control or heuristic that is not a theorem. OPEN/TODO names an obligation that the pointwise certificate does not close. The manuscript status of the full datum is ESTABLISHED. Its release metadata records ledger state `EVIDENCE_VERIFIED`, terminal status `COMPLETE_AFFIRMATIVE_WITH_CORRECTIONS`, and target digest `15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87`. The corrections are to the certification apparatus, not the mathematics: two of four domain approvals are stale against canonical sources edited after they approved, the first provenance snapshot is unauditable, and the sixteen-attack rejection count is not evidence. See [POST-RELEASE-CORRECTIONS.md](docs/derivations/2026-08-15-full-pointwise-meta-agent/POST-RELEASE-CORRECTIONS.md).

## 1. Fixed-point data and conventions

At $r_*$ and fixed admitted $(o,X)$, agent $i$ carries normalized marginal laws

$$
q_i^{b;o,X}(r_*)\in\mathcal P(\mathsf Z_i^q),
\qquad
q_i^{m;o,X}(r_*)\in\mathcal P(\mathsf M_i).
$$

on standard-Borel fibers. The original fixed-point certificate locally abbreviates these law-valued quantities by $q_i$ and $m_i$ in Sections 2--8. That historical $m_i$ is a scoped legacy alias only. In the canonical full construction, $m_i\in\mathsf M_i$ is a sampled model presentation, $q_i^{m;o,X}$ is its law, and $s_i^{o,X}$ remains the established section notation where used.

The belief and model channels are separate:

$$
(\beta_{ij},\Omega_{ij}),
\qquad
(\gamma_{ij},\widetilde\Omega_{ij}).
$$

Here $\beta$ and $\gamma$ are conditional rows. Every positive-support edge carries a bimeasurable bijection with the repository convention

$$
\Omega_{ij}:j\longrightarrow i,
\qquad
\widetilde\Omega_{ij}:j\longrightarrow i,
$$

and the reverse edge is its inverse. Paths, inverses, and cancellations form a reciprocal path groupoid. For a path $(v_0,\ldots,v_n)$, the ordered transport is

$$
\Omega_{v_n v_{n-1}}\cdots\Omega_{v_1v_0}.
$$

A rooted spanning tree plus every non-tree edge gives a free generating family of based loop words. For nonabelian holonomy, triangle checks suffice only when the based triangle boundary words normally generate the graph fundamental group, for example when attaching the declared triangular 2-cells makes a simply connected filled triangulation. Merely spanning the graph cycle space controls only abelianized holonomy. A chordless square has a based loop and no triangles, so triangle checks alone are not a general flatness test. ESTABLISHED.

For each channel, choose positive normalized receiver weights $\alpha_i^x$ and define the normalized joint directed edge-event laws

$$
\eta_{ij}^q=\alpha_i^q\beta_{ij},
\qquad
\eta_{ij}^m=\alpha_i^m\gamma_{ij}.
$$

Separately choose positive normalized barycenter weights $w_i^x$. Event weights and barycenter weights have different roles.

## 2. What holonomy does, and what it does not do

For the existing fixed-$K$ connection-Laplacian sector with reciprocal invertible links and positive-definite internal edge weights,

$$
\ker L_I\cong\operatorname{Fix}(\operatorname{Hol}_r).
$$

Thus represented trivial holonomy is necessary and sufficient for the full fixed $K$-sector. A smaller holonomy-fixed subspace gives partial structural retention. Semidefinite edge weights require the more general edgewise visibility constraint and do not inherit this full-sector criterion. ESTABLISHED.

Full-frame flatness $H=I$ must not be confused with state stabilization $H_\#Q=Q$. Flatness is not sufficient for belief agreement: laws on a tree can disagree arbitrarily. It is not necessary: nonidentity orthogonal holonomy can stabilize an isotropic Gaussian. ESTABLISHED.

## 3. Exact two-channel zero-distortion theorem

Write $p_i^q=q_i(r_*)$, $p_i^m=m_i(r_*)$, $T_{ij}^q=\Omega_{ij}$, and $T_{ij}^m=\widetilde\Omega_{ij}$. For $x\in\{q,m\}$, define

$$
\mathcal D_x
=\sum_{i,j:\eta_{ij}^x>0}
\eta_{ij}^x
\operatorname{KL}\left(
p_i^x\mathbin\Vert(T_{ij}^x)_\#p_j^x
\right).
$$

On a connected underlying positive-support graph,

$$
\begin{aligned}
\mathcal D_x=0
&\Longleftrightarrow
p_i^x=(T_{ij}^x)_\#p_j^x
\quad\text{on every positive-support edge}\\
&\Longleftrightarrow
\exists! Q_x\in\mathcal P(\mathsf Z_r^x):
(T_{\gamma_i}^x)_\#p_i^x=Q_x\text{ for every }i,
\quad
H_\#Q_x=Q_x\text{ for every }H\in\operatorname{Hol}_r^x.
\end{aligned}
$$

The proof uses positivity of edge weights, the zero criterion for relative entropy, reciprocal transport, and path propagation. Holonomy stabilization makes the reconstructed law independent of the path chosen to reach the root.

Because both channel distortions are nonnegative,

$$
\mathcal D_q+\mathcal D_m=0
\Longleftrightarrow
\mathcal D_q=\mathcal D_m=0.
$$

The result is the typed pair $(Q_q,Q_m)$. A joint parent law requires additional dependence data; marginal agreement cannot supply it. ESTABLISHED.

The complete proof is in [direct-derivation.md](docs/derivations/2026-08-14-pointwise-meta-agent-rg/evidence/direct-derivation.md).

## 4. The unrestricted forward-KL parent

After transporting full laws $P_i$ to one root, choose $w_i>0$ with $\sum_iw_i=1$ and put

$$
M=\sum_iw_iP_i.
$$

For every comparison law $R$, with the extended support convention,

$$
\boxed{
\sum_iw_i\operatorname{KL}(P_i\Vert R)
=\sum_iw_i\operatorname{KL}(P_i\Vert M)
+\operatorname{KL}(M\Vert R).}
$$

Therefore $M$ is the unique unrestricted full-law forward-KL barycenter. The proof is exact Radon-Nikodym algebra: every $P_i$ is dominated by $M$, support failure makes both sides infinite, the remaining infinite case closes by KL convexity, and logarithmic factorization is used only in the finite integrable case. ESTABLISHED.

Trivial holonomy makes the transported sources immediately path independent. Finite holonomy permits canonical uniform orbit averaging: for invariant $R$, the original objective equals an $R$-independent orbit-dispersion constant plus the orbit-averaged objective. Compact continuous holonomy permits the analogous Haar construction only with a measurable action, explicit common domination, finite-KL or integrability conditions, and justified Fubini interchange. A general noncompact invariant-barycenter theorem remains OPEN/TODO.

The proved Gaussian moment-matching and compact-Haar Gaussian specializations remain available in [Theory/09_coarsegraining.tex](Theory/09_coarsegraining.tex). A nonlinear boundary action can leave the Gaussian family, so those formulas do not replace the unrestricted law theorem.

## 5. Approximate agreement is a total-variation statement

We use the convention $\operatorname{TV}(P,Q)=\frac12\lVert P-Q\rVert_1$.

Suppose $\mathcal D_x\leq\varepsilon_x<\infty$. Fix one rooted spanning tree $\mathsf T_x$ of the connected undirected positive-support graph and orient each tree edge in a direction whose directed event weight is positive. Define

$$
\eta_{\min}^x
=\min_{(i,j)\in E(\mathsf T_x)}\eta_{ij}^x>0,
\qquad
d_x=\operatorname{diam}(\mathsf T_x),
\qquad
\delta_x=\sqrt{\frac{\varepsilon_x}{2\eta_{\min}^x}}.
$$

Pinsker gives the selected tree-edge bound

$$
\operatorname{TV}\left(
p_i^x,(T_{ij}^x)_\#p_j^x
\right)
\leq\delta_x.
$$

Transport every law to the root along its unique tree path, writing the result as $P_i^x$. Pushforward invariance and the total-variation triangle inequality along the unique tree path between $u$ and $v$ give

$$
\operatorname{TV}(P_u^x,P_v^x)
\leq d_x\delta_x.
$$

For the root-frame mixture $M_x=\sum_jw_j^xP_j^x$, convexity gives

$$
\operatorname{TV}(P_i^x,M_x)
\leq\sum_jw_j^x\operatorname{TV}(P_i^x,P_j^x)
\leq d_x\delta_x.
$$

The belief and model bounds use their own selected tree weights and diameters. A different tree gives a different valid constant. No KL triangle inequality is used or claimed. ESTABLISHED.

## 6. Exact scalar and marked network coarse-graining

Coarse-grain the normalized joint event law, never a conditional row alone. Let $C(A\mid i)$ be a normalized membership kernel. If receiver and source assignments are conditionally independent given the fine edge, declare that hypothesis and use

$$
K_\otimes(A,B\mid i,j)=C(A\mid i)C(B\mid j).
$$

Otherwise provide a normalized correlated endpoint kernel $K(A,B\mid i,j)$. This scalar event-law formula needs no parent root. Then

$$
\eta^c_{AB}
=\sum_{i,j}\eta_{ij}K(A,B\mid i,j),
\qquad
\alpha_A^c=\sum_B\eta^c_{AB},
\qquad
a^c_{AB}=\frac{\eta^c_{AB}}{\alpha_A^c},
$$

on positive receiver mass. Apply this formula separately to $(\eta^q,\beta)$ and $(\eta^m,\gamma)$. Pushing the joint law and then disintegrating is normalized and composes exactly under typed nested kernels. ESTABLISHED.

Scalar event-law closure above needs only a normalized endpoint kernel and no parent root. For retained marks, strengthen the endpoint datum in each channel $x$ to a kernel $K^x$ supported on the declared membership incidences:

$$
K^x(A,B\mid i,j)>0
\Longrightarrow
C(A\mid i)>0\text{ and }C(B\mid j)>0.
$$

For each parent $A$, set $V_A=\{i:C(A\mid i)>0\}$ and let $\mathcal C_A^x=\pi_0(G_x[V_A])$ be the connected components of the induced channel-$x$ positive-support transport graph. Each incidence $(A,i)$ determines a unique component $c_A^x(i)\in\mathcal C_A^x$. Use component meta-labels $\widehat A=(A,c)$, choose one root and one rooted spanning tree in every component, and let $\tau_{(A,c)\leftarrow i}^x$ be the ordered transport from $i$ to that component root.

With component indicators understood to be zero outside their incidence domains, the component event masses are

$$
\widehat\eta^x_{(A,c),(B,d)}
=\sum_{i,j}\eta_{ij}^xK^x(A,B\mid i,j)
\mathbf1_{\{c=c_A^x(i)\}}
\mathbf1_{\{d=c_B^x(j)\}},
\qquad
\eta_{AB}^{x,c}
=\sum_{c\in\mathcal C_A^x}\sum_{d\in\mathcal C_B^x}
\widehat\eta^x_{(A,c),(B,d)}.
$$

On an assigned component pair, dress the fine boundary transport by

$$
\widehat V_{ij;(A,c),(B,d)}^x
=\tau_{(A,c)\leftarrow i}^xT_{ij}^x
(\tau_{(B,d)\leftarrow j}^x)^{-1}.
$$

Pushing the joint event-plus-mark law gives a conditional mark law on every positive component event mass. A matrix mean need not lie in the group: opposite quarter-turn rotations average to the zero matrix. Exact certified closure therefore retains each component's internal based holonomy and the component-indexed conditional laws of root-relative boundary marks. Summing component masses recovers the scalar $A,B$ event mass, but collapsing disconnected component roots or mark fibers to one parent root requires another declared coarse channel. ESTABLISHED.

OPEN outside this certificate: induced hyperedge or shared-factor closure requires the separate Theory/07b complete joint-density/factorization hypotheses (or retention of an arbitrary correlated baseline as one global factor with law-level pushforward). Full path-law closure requires a declared joint law on a finite ordered path interval, the normalized pointwise coarse channel, and the required spatial and, for a separately declared dynamical model, parameter-direction transports. An exact linear memory-kernel recurrence additionally requires vector spaces and linear maps T, C, and P with CP=I and a declared fine recursion. None of those data is frozen here, so those richer closures are not target ancestors.

The canonical network source is [Theory/07b_agent_network_rg.tex](Theory/07b_agent_network_rg.tex).

## 7. Hard partitions, soft memberships, and replicated covers

A hard partition is the deterministic kernel $C(A\mid i)=\mathbf1_{A=h(i)}$. A normalized soft membership satisfies $C(A\mid i)\geq0$ and $\sum_AC(A\mid i)=1$; one child may have several nonzero memberships without duplicating mass. For marked closure, every incidence $(A,i)$ is assigned to its channel-specific connected component inside $V_A$; a soft parent is not assumed connected and receives no single root. Shared children can require a correlated endpoint kernel supported on the declared incidences. Any shared-factor claim requires a separately declared joint-factor model.

A literal replicated cover instead uses incidences $R(A\mid i)\in\{0,1\}$ with several ones allowed. Its column sum can exceed one, so it is not a Markov kernel and retains multiplicity. Treating it as normalized doubles child mass and incident event contributions in the simplest two-parent example. Literal full membership in several parents is not certified here. ESTABLISHED boundary.

Nested normalized memberships compose by

$$
C_{20}(B\mid i)
=\sum_A C_{21}(B\mid A)C_{10}(A\mid i).
$$

Nested endpoint assignments require composition of the full endpoint kernels; a product remains a product only while its independence hypotheses remain valid. ESTABLISHED.

## 8. Exact VFE closure requires one common channel

Fix an observation $o$, posterior $\Pi_o$, recognition law $Q_o$, and one normalized recognition-independent Markov channel $C$ applied to both. It leaves the observation and evidence unchanged. With $Q_o^c=Q_oC$ and $\Pi_o^c=\Pi_oC$, standard-Borel disintegration gives

$$
\operatorname{KL}(Q_o\Vert\Pi_o)
=\operatorname{KL}(Q_o^c\Vert\Pi_o^c)
+\int\operatorname{KL}\left(
Q_o(\cdot\mid z)\Vert\Pi_o(\cdot\mid z)
\right)Q_o^c(dz).
$$

Therefore

$$
\mathcal F_o(Q_o)
=\mathcal F_o^c(Q_o^c)+\Delta_C(Q_o,\Pi_o),
\qquad
\Delta_C\geq0.
$$

For finite fine KL, $\Delta_C=0$ exactly when the discarded conditional recognition and posterior laws agree $Q_o^c$-almost surely. Otherwise the residual is explicit. Low marginal KL does not control this defect; equal singleton marginals can coexist with an infinite full-joint KL. ESTABLISHED.

The canonical sources are [Theory/06_general_coarsegraining.tex](Theory/06_general_coarsegraining.tex) and [Theory/07b_agent_network_rg.tex](Theory/07b_agent_network_rg.tex).

## 9. Inference flow is optional and typed after the fact

Only after declaring a fine flow $\dot y=X_t(y)$ may $t$ be called an inference-flow parameter. For a $C^1$ moving coarse map $c_t$ and $z(t)=c_t(y(t))$,

$$
\dot z
=\partial_t c_t(y)+D c_t(y)X_t(y).
$$

Exact dynamic semiconjugacy to $\dot z=\overline X_t(z)$ is the equation

$$
\partial_t c_t+D c_tX_t
=\overline X_t\circ c_t.
$$

The $\partial_t c_t$ term disappears only for a frozen coarse map. The parameter $t$ is not a base coordinate, physical time, or RG depth. ESTABLISHED.

For frozen memberships and the constant-metric Gaussian or feature flow

$$
R\dot z=-Lz,
\qquad
R\succ0,
\quad
L\succeq0,
$$

the existing spectral theorem gives exponential convergence to the $R$-orthogonal projection onto $\ker L$. This is a CONDITIONAL stability corollary, not a proof for adaptive $\beta$ or $\gamma$, nonlinear full-law VFE dynamics, dynamically selected memberships, or an autonomous meta-agent flow. Those extensions remain OPEN/TODO.

## 10. Eight shortcut failures

The contained register proves the following exact failures:

| Shortcut | Counterexample |
|---|---|
| KL-threshold clusters are transitive | Bernoulli $1/10\to1/2\to9/10$ at threshold $0.6$ |
| Zero marginal KL controls full VFE | Equal fair marginals with disjoint parity and anti-parity joint supports |
| Trivial holonomy implies belief agreement | Two-node tree with Gaussian means $\pm ae_1$ and KL $2a^2$ |
| Belief agreement implies trivial holonomy | Nonidentity $\operatorname{diag}(1,-1,-1)$ stabilizing an isotropic Gaussian |
| A spectral gap is an intrinsic agreement scale | Two-node gap $2c$, independent of laws and arbitrary under $c$-rescaling |
| One-way KL controls reverse KL | Point mass versus fair bit: $\log2$ forward and $+\infty$ reverse |
| Gaussian projection preserves nonlinear boundary actions exactly | Equally weighted children $\mathcal N(\pm a,1)$ and $H(x)=\lambda x^4$ leave signed residual $2\lambda a^4$ |
| Overlapping full parents preserve mass | One child fully replicated into two parents has total mass $2$ |

See [counterexample-proofs.md](docs/derivations/2026-08-14-pointwise-meta-agent-rg/evidence/counterexample-proofs.md). The deterministic recomputation is DIAGNOSTIC corroboration only.

## 11. Certified boundary and repository map

ESTABLISHED: fixed-point types; fundamental-cycle holonomy bookkeeping; two-channel zero distortion; unrestricted full-law mixture identity and uniqueness; finite-holonomy orbit averaging; rooted-tree total-variation control; normalized joint-event pushforward and disintegration; incidence-supported component-indexed retained mark laws; the full pointwise parent generative/posterior/recognition triple; induced or explicitly compatible parent evaluation; derived recognition, prior, and posterior marginals; the extended common-channel KL/VFE chain and its finite zero-defect and pairwise recovery corollaries; normalized nested composition; moving-map chain rule; and the released counterexamples.

CONDITIONAL: holonomy blindness under typed actions, full fine-law covariance, compatible selected posterior versions, $C_A$ equivariance, evaluator covariance, and fixed-$(o,X)$ isotropy for same-slice invariance; compact continuous holonomy averaging under explicit domination and finite-KL assumptions; the frozen constant-metric Gaussian or feature stability corollary; the richer Theory/07b hypergraph, path-law, and memory closures under their separately stated joint-factor, full-path-law/transport, and linear-dynamic hypotheses; and any exact removal of the certified marks or holonomy under a theorem stated for that removal.

DIAGNOSTIC: raw connection spectral gaps, KL thresholds, and finite symbolic or numerical checks. They can test a proposed construction but do not select a partition or prove a theorem.

OPEN/TODO: **the renormalization group itself** — see below; family-wide common recovery absent simultaneous hypotheses; the frozen comparison category; extension across $\mathcal U_A$; parent local sections and patch gluing; active-set changes; canonical channel, membership, and partition selection; literal replicated-parent semantics; a geometric meta-agent; autonomous agency; nonequilibrium persistence; physical time; continuum limits; unique latent DAG or microscopic physics; ontology; an intrinsic threshold; general noncompact holonomy averaging; adaptive attention dynamics; nonlinear full-law VFE semiconjugacy; and dynamically selected memberships.

**The obligation named in this file's own title is OPEN.** This page is titled for a renormalization
*group*, and nothing on it establishes one. There is no rescaling or identification map, no beta
function, no blocking ratio, no relevant/irrelevant operator classification, and no universality
statement; the only fixed point named anywhere above is the base point $r_*$, which is a chosen
location and not a fixed point of a flow. The certified channel $C_A:\mathsf Y_I\rightsquigarrow\mathsf Z_A$
has no declared inverse-direction map, so it admits no iterate and no flow. What *is* established is a
composed-scale composition law for coarse channels at three levels (§ above,
$C_{20}(B\mid i)=\sum_A C_{21}(B\mid A)\,C_{10}(A\mid i)$) together with the exact pointwise
coarse-graining identities — that is a consistent family of coarse-grainings, which is a prerequisite
for an RG semigroup, not an RG semigroup. Closing this requires at minimum a scale parameter with a
composition law in that parameter, a flow on a space of couplings or laws, and a fixed-point analysis.
Recorded by the 2026-08-16 remediation of finding M3 in
`docs/reviews/2026-08-15-deep-review/REPORT.md`.

| Location | Role |
|---|---|
| [solid_RG_theory.md](solid_RG_theory.md) | Compact technical start page and status reference |
| [solid_RG_theory.tex](solid_RG_theory.tex) | Standalone physicist-facing exposition with intuition, a worked example, and explicit proof boundaries |
| [Theory](Theory/) | Canonical theorem source, especially chapters 06, 07b, and 09 plus SPEC.md |
| [Dated worklog](docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md) | Chronological investigation; later corrections supersede earlier exploratory language |
| [Full-datum certification package](docs/derivations/2026-08-15-full-pointwise-meta-agent/) | Current hash-bound proof, reconstruction, adversarial, counterexample, reviews, and release metadata |
| [Marginal-pair certification package](docs/derivations/2026-08-14-pointwise-meta-agent-rg/) | Historical two-channel marginal theorem and normalized network closure |

The current package terminal status is COMPLETE_AFFIRMATIVE_WITH_CORRECTIONS for the exact frozen full-datum conjunction, and its `target` ledger entry is EVIDENCE_VERIFIED. Those package labels report release evidence; the canonical manuscript theorem is ESTABLISHED. No status crosses an OPEN/TODO boundary above; the machine-readable certificate is `docs/derivations/2026-08-15-full-pointwise-meta-agent/release.json`. Two certification obligations are open and are recorded in `docs/derivations/2026-08-15-full-pointwise-meta-agent/POST-RELEASE-CORRECTIONS.md`: re-running the two stale domain reviews against the released bytes, and repairing or replacing the unauditable first provenance snapshot. Neither affects the mathematics.

## 12. Ordered TODO roadmap beyond the pointwise certificate

This roadmap records the completed static phases and the next theory program. The full-datum release closes only Phases 1--2; each later phase remains OPEN/TODO and depends on closure of the preceding phase.

### Phase 0: collision-free notation standard -- COMPLETE

Before another theorem is stated, publish a notation dictionary and migration table, then scan the governing sources for collisions. The standard must enforce all of the following.

- The base is $\mathcal C$; agent supports are $\mathcal C_i$; and a finite child block $I$ with parent label $A$ has overlap patch $\mathcal U_A=\bigcap_{i\in I}\mathcal C_i$. Bare $R$ is never an overlap region. In the intervention chapters, $R$ remains the typed retained input or parameter, $E$ the intervened mediator, and $O$ the retained output or observation.
- $\mathscr P_G\to\mathcal C$ denotes a principal bundle when that object is needed. Full generative and recognition laws use $\mathbb P$ and $\mathbb Q$, and the posterior uses $\boldsymbol\Pi$. Bare $P$ and $Q$ may occur only as explicitly local dummy measures or inside a frozen historical theorem whose types are stated nearby.
- $\varpi$ remains reserved for the established projection notation; it is not reused for receiver occupancy. The normalized receiver occupancy in channel $x$ remains $\alpha_i^x$, and $\eta_{ij}^q=\alpha_i^q\beta_{ij}$ and $\eta_{ij}^m=\alpha_i^m\gamma_{ij}$ remain the joint directed edge-event laws. These $\alpha_i^x$ are external occupancy or sampling weights, not learned attention logits, attention rows, or an instruction to add a new transformer parameter. Any unrelated manuscript use of $\alpha$ must carry a distinguishing qualifier or superscript.
- The new full-law construction uses $q_i^b$ for a local belief law and $q_i^m$ for a law over generative models. The symbol $m_i$ remains a model sample or presentation wherever it is so typed; it is not a general alias for $q_i^m$. Only explicitly law-valued $m_i$ occurrences in the frozen pointwise RG certificate may receive the local migration alias $q_i^m$. Preserve the distinct dependency notation $s_i^{o,X}$ and $q_i^{o,X}$; bare legacy $s_i$ is not globally renamed. A model point $m\in\mathsf M_i$ denotes a model presentation only after declaring an evaluation map $\operatorname{ev}_i:m\mapsto K_m$ into normalized generative kernels.
- $C_A$ denotes the normalized coarse Markov channel used in the pointwise law construction. A moving deterministic coarse map in a dynamical closure problem is written $c_t$, not $C_t$.
- General measurable or smooth statistical model spaces are the theory default. Multivariate Gaussian families are optional finite computational realizations, never the definition of the model fiber or of a meta-agent.

The exit gate is closed by the authoritative registry, migration record, scanner self-test, and stored collision report in the full-datum package.

### Phase 1: full pointwise probabilistic datum at one fixed point -- ESTABLISHED

At $r_*$, the released theorem types the fine full recognition law $\mathbb Q_{I,o,X}$, full generative law $\mathbb P_I$, and selected posterior $\boldsymbol\Pi_{I,o,X}$. One normalized recognition-independent coarse channel $C_A$ leaves the observation coordinate unchanged, while the structural datum $X_A=\chi_A(X)$ remains outside $C_A$. The candidate parent objects are

$$
\mathbb Q_{A,o,X}=\mathbb Q_{I,o,X}C_A,
\qquad
\mathbb P_A=(\operatorname{id}_{\mathsf O}\times C_A)_\#\mathbb P_I,
\qquad
\boldsymbol\Pi_{A,o,X}=\boldsymbol\Pi_{I,o,X}C_A.
$$

The theorem proves normalization, the selected parent posterior identity, absolute continuity, induced or explicitly compatible parent evaluation, and the coordinate-projection identities for $q_A^b$, $q_A^m$, the prior marginals, and the posterior marginals. These projections do not reconstruct a joint law. This phase is closed for the static pointwise datum and does not construct a geometric meta-agent.

### Phase 2: static pointwise VFE and holonomy alternatives -- ESTABLISHED

The common-channel KL chain is additive in $[0,+\infty]$ with defect $\Delta_A(o,X)$. Adding the same finite real $-\log p_X(o)$ to both KL terms gives an extended-real VFE identity; a finite VFE may be negative. Without a finiteness premise, $\Delta_A=0$ exactly when the discarded conditional recognition and posterior laws agree $\mathbb Q_{A,o,X}$-almost surely. Finite fine KL is required for ordinary subtraction $\mathcal F_I-\mathcal F_A=\Delta_A$ and for the stated two-way pairwise common-recovery equivalence; family-wide recovery still needs simultaneous hypotheses. A bare equality $+\infty=+\infty$ supplies neither the zero-defect criterion nor a recovery consequence. The holonomy-blind branch is conditional on the typed action, channel, evaluator, fine-law, and selected-version hypotheses stated above. The alternative retains raw root-framed holonomy and boundary marks and makes no blindness claim. Neither branch selects membership. Dynamics is not part of this static closure.

### Phase 3: comparison theorem -- OPEN/TODO

Only after Phase 2, formalize how conclusions change when the comparison category permits or forbids target erasure, boundary exchange, time reversal, protocol-dependent relabeling, or latent dilation. Prove monotonicity under enlargement of the admitted morphism category and separate observational equivalence from equality of VFE, posterior, factorization, or meta-agent structure. Interventions are analyst-declared probes of a mechanism in this theorem; their use does not add ontic actions, plans, or controls to the underlying dynamics.

### Phase 4: extend from $r_*$ across $\mathcal U_A$ -- OPEN/TODO

Promote the pointwise objects to local sections over $\mathcal U_A$ and prove the required gluing, cocycle, measurability or smoothness, and path-consistency statements. Treat changing active sets, soft or multiple memberships, stabilizer and rank jumps, and failure of one global parent section explicitly. A single child may participate in multiple normalized coarse channels, but a literal replicated cover has different mass semantics and remains separately typed. The exit gate is a patchwise construction; no continuum or spacetime interpretation follows automatically.

### Phase 5: participatory and cross-scale nonequilibrium -- OPEN

Begin with declared fine dynamics $\dot y=V_t(y)$, a possibly moving deterministic coarse map $c_t$, and the coarse vector field $\overline V_t$. The semiconjugacy defect is

$$
\delta_t=\partial_t c_t+D c_tV_t-\overline V_t\circ c_t.
$$

Determine whether one coupled multiscale action can derive reciprocal fine-to-coarse and coarse-to-fine influence without double counting. Frozen dissipative gradient flow may relax toward equilibrium; sustained nonequilibrium would require a proved mechanism such as adaptive coarse maps, open boundary flux, stochastic driving, an antisymmetric sector, or Wheelerian participatory feedback. Distinguish universal variational evolution from the stronger claim of emergent agency. This phase remains OPEN until a typed coupled action, conservation or flux accounting, and an exact or controlled approximate dynamical closure theorem are supplied.
