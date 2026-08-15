<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-a0d61fb082b9632a9aac685fced7bf4a82f1a9f115a72b9583a6ed96f636c952","schema_version":"rigorous-theory-search/v1","target_digest":"a0d61fb082b9632a9aac685fced7bf4a82f1a9f115a72b9583a6ed96f636c952"} -->
# Pointwise meta-agent renormalization

This is the repository start page for the strongest certified pointwise result. It fixes one base point $r_*$ in an overlap region and works with a finite network there. It does not extend the construction across the contextual base $R$.

The result is exact but deliberately bounded. In each of the belief and model channels, zero positive-weight transported edge KL is equivalent to one unique common root marginal stabilized by that channel's holonomy. The two channel results combine into a pair of marginal parent laws. They do not by themselves produce a joint belief-model law, an exact recognition law, or a VFE agent.

## Status key

ESTABLISHED means proved in the contained package or in the cited canonical theorem source. CONDITIONAL means exact under hypotheses stated beside the result. DIAGNOSTIC means a finite control or heuristic that is not a theorem. OPEN/TODO names an obligation that the pointwise certificate does not close.

## 1. Fixed-point data and conventions

At $r_*$, agent $i$ carries normalized marginal laws

$$
q_i(r_*)\in\mathcal P(\mathsf Z_i^q),
\qquad
m_i(r_*)\in\mathcal P(\mathsf Z_i^m)
$$

on standard-Borel fibers. Legacy text may write $s_i$ for the model law $m_i$; this guide uses $m_i$ consistently.

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

A rooted spanning tree plus every non-tree edge gives a fundamental cycle basis. Checking triangles is sufficient only after declaring a triangulation whose triangle boundaries span the graph cycle space. A chordless square has a cycle and no triangles, so triangle checks alone are not a general flatness test. ESTABLISHED.

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
\operatorname{KL}\!\left(
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
\exists!\,Q_x\in\mathcal P(\mathsf Z_r^x):
(T_{\gamma_i}^x)_\#p_i^x=Q_x\ \forall i,
\quad
H_\#Q_x=Q_x\ \forall H\in\operatorname{Hol}_r^x .
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
\operatorname{TV}\!\left(
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

Otherwise provide a normalized correlated endpoint kernel $K(A,B\mid i,j)$. Then

$$
\eta^c_{AB}
=\sum_{i,j}\eta_{ij}K(A,B\mid i,j),
\qquad
\alpha_A^c=\sum_B\eta^c_{AB},
\qquad
a^c_{AB}=\frac{\eta^c_{AB}}{\alpha_A^c}
$$

on positive receiver mass. Apply this formula separately to $(\eta^q,\beta)$ and $(\eta^m,\gamma)$. Pushing the joint law and then disintegrating is normalized and composes exactly under typed nested kernels. ESTABLISHED.

For a boundary edge $j\to i$ from parent $B$ to parent $A$, retain the dressed channel mark

$$
V_{ij}^x
=\tau_{A\leftarrow i}^xT_{ij}^x
(\tau_{B\leftarrow j}^x)^{-1}
$$

as a conditional distribution under the pushed joint event law. A matrix mean need not lie in the group: opposite quarter-turn rotations average to the zero matrix. Exact closure therefore retains internal based holonomy, root-relative boundary marks, induced hyperedges and shared factors, and path memory or an exact memory kernel. A one-link, pairwise, memoryless replacement is a truncation unless a scope-matched removal theorem is supplied. ESTABLISHED.

The canonical network source is [Theory/07b_agent_network_rg.tex](Theory/07b_agent_network_rg.tex).

## 7. Hard partitions, soft memberships, and replicated covers

A hard partition is the deterministic kernel $C(A\mid i)=\mathbf1_{A=h(i)}$. A normalized soft membership satisfies $C(A\mid i)\geq0$ and $\sum_AC(A\mid i)=1$; one child may have several nonzero memberships without duplicating mass. Shared children can still induce correlations or shared effective factors.

A literal replicated cover instead uses incidences $R(A\mid i)\in\{0,1\}$ with several ones allowed. Its column sum can exceed one, so it is not a Markov kernel and retains multiplicity. Treating it as normalized doubles child mass and shared factors in the simplest two-parent example. Literal full membership in several parents is not certified here. ESTABLISHED boundary.

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
+\int\operatorname{KL}\!\left(
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

Only after declaring a fine flow $\dot y=X_t(y)$ may $t$ be called an inference-flow parameter. For a $C^1$ moving coarse map $C_t$ and $z(t)=C_t(y(t))$,

$$
\dot z
=\partial_tC_t(y)+DC_t(y)X_t(y).
$$

Exact dynamic semiconjugacy to $\dot z=\overline X_t(z)$ is the equation

$$
\partial_tC_t+DC_tX_t
=\overline X_t\circ C_t.
$$

The $\partial_tC_t$ term disappears only for a frozen coarse map. The parameter $t$ is not a base coordinate, physical time, or RG depth. ESTABLISHED.

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
| Gaussian projection preserves nonlinear boundary actions exactly | Equal children $\mathcal N(\pm a,1)$ and $H(x)=\lambda x^4$ leave residual $2\lambda a^4$ |
| Overlapping full parents preserve mass | One child fully replicated into two parents has total mass $2$ |

See [counterexample-proofs.md](docs/derivations/2026-08-14-pointwise-meta-agent-rg/evidence/counterexample-proofs.md). The deterministic recomputation is DIAGNOSTIC corroboration only.

## 11. Certified boundary and repository map

ESTABLISHED: fixed-point types; fundamental-cycle holonomy bookkeeping; two-channel zero distortion; unrestricted full-law mixture identity and uniqueness; finite-holonomy orbit averaging; rooted-tree total-variation control; normalized joint-event pushforward and disintegration; retained mark laws; common-channel VFE chain rule; normalized nested composition; moving-map chain rule; and the eight counterexamples.

CONDITIONAL: compact continuous holonomy averaging under explicit domination and finite-KL assumptions; the frozen constant-metric Gaussian or feature stability corollary; and any exact removal of marks, hyperedges, shared factors, or memory under a theorem stated for that removal.

DIAGNOSTIC: raw connection spectral gaps, KL thresholds, and finite symbolic or numerical checks. They can test a proposed construction but do not select a partition or prove a theorem.

OPEN/TODO: extension across $R$; patch gluing; active-set changes; canonical partition selection; literal replicated-parent semantics; autonomous agency; physical time; continuum limits; an intrinsic threshold; general noncompact holonomy averaging; adaptive attention dynamics; nonlinear full-law VFE semiconjugacy; and dynamically selected memberships.

| Location | Role |
|---|---|
| [solid_RG_theory.md](solid_RG_theory.md) | Start page and sole human-facing pointwise guide |
| [Theory](Theory/) | Canonical theorem source, especially chapters 06, 07b, and 09 plus SPEC.md |
| [Dated worklog](docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md) | Chronological investigation; later corrections supersede earlier exploratory language |
| [Certification package](docs/derivations/2026-08-14-pointwise-meta-agent-rg/) | Hash-bound proof, reconstruction, adversarial, counterexample, and validator evidence |

The package terminal status is COMPLETE_AFFIRMATIVE for the exact frozen pointwise conjunction. That status does not cross any OPEN/TODO boundary above; the machine-readable certificate is release.json.
