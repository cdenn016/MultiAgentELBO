<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-a0d61fb082b9632a9aac685fced7bf4a82f1a9f115a72b9583a6ed96f636c952","schema_version":"rigorous-theory-search/v1","target_digest":"a0d61fb082b9632a9aac685fced7bf4a82f1a9f115a72b9583a6ed96f636c952"} -->
# Direct derivation

## 1. Frozen pointwise types

Fix one base point (r_*). Let (V) be a finite nonempty set. The belief channel (x=q) has standard-Borel sample fibers (mathsf Z_i^q) and normalized laws (p_i^q=q_i(r_*)). The model channel (x=m) has standard-Borel fibers (mathsf Z_i^m) and normalized laws (p_i^m=m_i(r_*)). Older repository prose may write (s_i) for (m_i); this is an alias, not a third channel.

For each channel, let (a_{ij}^q=\beta_{ij}) and (a_{ij}^m=\gamma_{ij}) be conditional rows. Let (\alpha_i^x>0), (\sum_i\alpha_i^x=1), and define the joint directed edge-event weights

\[
\eta_{ij}^x=\alpha_i^x a_{ij}^x,
\qquad
\sum_{i,j}\eta_{ij}^x=1.
\]

The positive-support graph has an undirected edge ({i,j}) whenever (eta_{ij}^x+eta_{ji}^x>0). It is assumed connected for the one-root theorem. Every support edge carries a bimeasurable bijection

\[
T_{ij}^x:\mathsf Z_j^x\longrightarrow\mathsf Z_i^x,
\qquad
T_{ji}^x=(T_{ij}^x)^{-1}.
\]

The repository convention is (T_{ij}:j\to i). Thus a path (gamma=(v_0,v_1,\ldots,v_n)) from (v_0) to (v_n) has ordered transport

\[
T_\gamma^x
=T_{v_n v_{n-1}}^x\circ\cdots\circ T_{v_1v_0}^x,
\]

and a based cycle (c=(v_0,v_1,\ldots,v_{n-1},v_0)) has holonomy

\[
H_c^x
=T_{v_0v_{n-1}}^x\circ\cdots\circ T_{v_1v_0}^x.
\]

The formal paths, inverses, and cancellation relations form a reciprocal path groupoid. A rooted spanning tree and its non-tree edges give fundamental cycles; their holonomies generate all based graph-loop holonomies. Triangles generate all graph cycles only when triangle boundaries span the cycle space, as in a declared triangulation. A bare graph can contain a chordless cycle of length four or more, so checking all available triangles is not a flatness test in general.

For each channel, choose positive normalized barycenter weights (w_i^x>0), (sum_iw_i^x=1). These vertex weights are independent of the joint edge-event weights (eta_{ij}^x).

## 2. Frame flatness and law stabilization

For a fixed (K)-dimensional represented sector with positive-definite internal edge weights, the connection-Laplacian energy is

\[
z^TL_xz
=\sum_{e=(i,j)}(z_i-T_{ij}^xz_j)^TW_e^x(z_i-T_{ij}^xz_j).
\]

The spanning-tree argument gives

\[
\ker L_x\cong\operatorname{Fix}(\operatorname{Hol}_r^x).
\]

Consequently, the full fixed (K)-sector exists if and only if every represented holonomy is the identity. This statement uses reciprocal invertible links and positive-definite weights. With semidefinite weights, the exact condition is edgewise visibility, (W_e^{1/2}(z_i-T_{ij}z_j)=0), and nonidentity transport may survive in weight-null directions.

Full-frame flatness (H=I) is different from state-specific stabilization (H_\#Q=Q). Flatness is neither sufficient nor necessary for belief agreement. It is not sufficient because arbitrary laws on a tree can disagree by an arbitrarily large KL divergence. It is not necessary because a nonidentity rotation or reflection can stabilize an isotropic law. The counterexample evidence gives both witnesses.

## 3. Channelwise zero-distortion theorem

Define the extended channel distortion

\[
\mathcal D_x
=\sum_{i,j:\eta_{ij}^x>0}
\eta_{ij}^x
\operatorname{KL}\left(
p_i^x\mathbin\Vert(T_{ij}^x)_\#p_j^x
\right).
\]

All summands are nonnegative extended real numbers and every displayed coefficient is strictly positive. The following three conditions are equivalent.

1. (mathcal D_x=0).
2. On every positive-support directed edge, (p_i^x=(T_{ij}^x)_\#p_j^x).
3. For a root (r), there is one law (Q_x\in\mathcal P(\mathsf Z_r^x)) such that, for some and hence every path (gamma_i:i\to r),

\[
(T_{\gamma_i}^x)_\#p_i^x=Q_x
\quad\text{for all }i,
\qquad
(H^x)_\#Q_x=Q_x
\quad\text{for all }H^x\in\operatorname{Hol}_r^x.
\]

The law (Q_x) is unique for the given vertex laws.

To prove (1\Leftrightarrow2), use positivity of the coefficients and the exact zero criterion for relative entropy: (operatorname{KL}(P\Vert Q)=0) if and only if (P=Q). If a support edge is positive only in the reverse orientation, the inverse bijection turns its equality into the needed equality in the other orientation.

Assume condition 2. Transporting edge equalities along a path shows that every (p_i^x) transported to the root equals (p_r^x). Transporting (p_r^x) around any loop also returns (p_r^x), so (Q_x=p_r^x) is holonomy stabilized. This proves 3 and uniqueness.

Assume condition 3. For a support edge (j\to i), concatenate that edge with a chosen path from (i) to the root. This is another path from (j) to the root. Two such paths differ by a rooted loop, and holonomy stabilization makes their pushforwards of (p_j^x) equal. Applying the inverse root transport gives (p_i^x=(T_{ij}^x)_\#p_j^x), proving 2.

Apply the theorem separately to (x=q) with ((\beta,\Omega)) and (x=m) with ((\gamma,\widetilde\Omega)). Since both distortions are nonnegative,

\[
\mathcal D_q+\mathcal D_m=0
\quad\Longleftrightarrow\quad
\mathcal D_q=\mathcal D_m=0.
\]

The result produces the typed pair ((Q_q,Q_m)) of marginal parent laws. It does not construct a joint belief-model law, a correlated recognition law, a generative kernel, or an exact VFE agent.

## 4. Unrestricted forward-KL mixture theorem

Let (P_1,\ldots,P_n) and (R) be probability laws on one measurable space, let (w_i>0), (sum_iw_i=1), and put

\[
M=\sum_iw_iP_i.
\]

Then, in ([0,+\infty]),

\[
\boxed{
\sum_iw_i\operatorname{KL}(P_i\Vert R)
=\sum_iw_i\operatorname{KL}(P_i\Vert M)
+\operatorname{KL}(M\Vert R).}
\]

First, (P_i\ll M) and (dP_i/dM\leq1/w_i), so every (operatorname{KL}(P_i\Vert M)) is finite and bounded above by (log(1/w_i)). If (M\not\ll R), some (P_i\not\ll R); both sides are (+infty).

Suppose (M\ll R). Set (f_i=dP_i/dM) and (g=dM/dR), so (dP_i/dR=f_ig). If (operatorname{KL}(M\Vert R)=+\infty), convexity of relative entropy under finite mixing gives

\[
\operatorname{KL}(M\Vert R)
\leq\sum_iw_i\operatorname{KL}(P_i\Vert R),
\]

so both sides of the boxed identity are (+infty). If (operatorname{KL}(M\Vert R)<\infty), then (log g) is integrable under every (P_i\leq w_i^{-1}M): its positive part is controlled by finite (operatorname{KL}(M\Vert R)), while its negative part is integrable because (u(-\log u)\leq e^{-1}) for (0<u\leq1). Also, (log f_i) is (P_i)-integrable because (0\leq f_i\leq1/w_i) and (u|\log u|) is bounded near zero. Therefore exact Radon-Nikodym algebra is legitimate:

\[
\begin{aligned}
\sum_iw_i\operatorname{KL}(P_i\Vert R)
&=\sum_iw_i\int\log(f_ig)\,dP_i\\
&=\sum_iw_i\int\log f_i\,dP_i
+\int\log g\,d\left(\sum_iw_iP_i\right)\\
&=\sum_iw_i\operatorname{KL}(P_i\Vert M)
+\operatorname{KL}(M\Vert R).
\end{aligned}
\]

The first term on the right is always finite. Hence the aggregate forward-KL objective has unique minimizer (R=M), because the remaining term is nonnegative and vanishes exactly at (R=M).

For transported pointwise laws (P_i=(T_{\gamma_i})_\#p_i), trivial holonomy gives immediate path independence. If the represented holonomy group (mathcal H) is finite, define

\[
\overline P_i
=\frac1{|\mathcal H|}\sum_{h\in\mathcal H}h_\#P_i,
\qquad
M_{\mathcal H}=\sum_iw_i\overline P_i.
\]

The orbit average is invariant and independent of the path presentation. For every (\mathcal H)-invariant candidate (R), common-pushforward invariance gives (\operatorname{KL}(P_i\Vert R)=|\mathcal H|^{-1}\sum_h\operatorname{KL}(h_\#P_i\Vert R)). Applying the mixture identity to this orbit family gives (\operatorname{KL}(P_i\Vert R)=c_i+\operatorname{KL}(\overline P_i\Vert R)), where (c_i=|\mathcal H|^{-1}\sum_h\operatorname{KL}(h_\#P_i\Vert\overline P_i)) is finite and independent of (R). Thus the constrained objective differs from the orbit-averaged objective only by (\sum_iw_ic_i); a second application of the boxed identity makes (M_{\mathcal H}) its unique invariant minimizer.

For a compact continuous holonomy closure, the analogous Haar average is conditional on a jointly measurable action, a common dominating measure for the orbit family and candidate, and finite-KL or domination hypotheses sufficient for Fubini and the KL averaging step. Without those hypotheses, formal Haar averaging is not a certified KL minimization argument. A general noncompact holonomy group has no normalized Haar probability and can have an empty invariant parent family; the unrestricted noncompact case remains open.

The full-Gaussian moment-matching formula and the compact-Haar Gaussian specialization have already been proved in `Theory/09_coarsegraining.tex`. They are specializations of the law-level statement, not evidence that arbitrary nonlinear law fibers are Gaussian closed.

## 5. Approximate total-variation theorem

Fix a channel and suppose (\mathcal D_x\leq\varepsilon_x<\infty). Fix a rooted spanning tree (\mathsf T_x) of the connected undirected positive-support graph, orienting each tree edge in a direction whose directed event weight is positive. Let

\[
\eta_{\min}^x
=\min\{\eta_{ij}^x:(i,j)\in E(\mathsf T_x)\}>0,
\qquad
d_x=\operatorname{diam}(\mathsf T_x).
\]

Every selected tree-edge term is at most (\varepsilon_x/\eta_{\min}^x). Pinsker's inequality therefore gives

\[
\operatorname{TV}\left(
p_i^x,(T_{ij}^x)_\#p_j^x
\right)
\leq
\delta_x
:=\sqrt{\frac{\varepsilon_x}{2\eta_{\min}^x}}.
\]

Transport every law to the root along its unique tree path, writing the result as (P_i^x). For adjacent tree vertices, total-variation invariance under the common residual pushforward gives the selected edge bound in the root frame. Along the unique tree path between (u) and (v), the triangle inequality yields

\[
\operatorname{TV}\left(
P_u^x,P_v^x
\right)
\leq\operatorname{dist}_{\mathsf T_x}(u,v)\delta_x
\leq d_x\delta_x.
\]

Form the root-frame mixture (M_x=\sum_jw_j^xP_j^x). Convexity of total variation gives

\[
\operatorname{TV}(P_i^x,M_x)
\leq\sum_jw_j^x\operatorname{TV}(P_i^x,P_j^x)
\leq d_x\delta_x.
\]

The belief and model bounds apply separately with their own positive minimum selected tree-edge weights and tree diameters. A different spanning tree gives a different valid constant. The proof uses the total-variation triangle inequality. KL has no triangle inequality, and no KL path-sum bound is claimed.

## 6. Exact scalar network renormalization

For either channel, the conditional row (a_{ij}) is not a joint law. The normalized receiver law is required:

\[
\eta_{ij}=\alpha_i a_{ij}.
\]

Let (C(A\mid i)\geq0) be a normalized membership kernel, (sum_A C(A\mid i)=1). If endpoint memberships are conditionally independent given the fine edge event, declare that hypothesis and use

\[
K_\otimes(A,B\mid i,j)=C(A\mid i)C(B\mid j).
\]

More generally, use any explicitly declared normalized correlated endpoint kernel (K(A,B\mid i,j)). Push the joint event law first:

\[
\eta^c_{AB}
=\sum_{i,j}\eta_{ij}K(A,B\mid i,j),
\qquad
\sum_{A,B}\eta^c_{AB}=1.
\]

Then disintegrate it:

\[
\alpha_A^c=\sum_B\eta^c_{AB},
\qquad
a^c_{AB}=\frac{\eta^c_{AB}}{\alpha_A^c}
\quad\text{on }\{\alpha_A^c>0\}.
\]

A row on a zero-mass receiver is an immaterial conditional version. The formula applies to ((\alpha^q,\beta,\eta^q)) and ((\alpha^m,\gamma,\eta^m)) separately. Writing (C(A\mid i)C(B\mid j)) without declaring conditional independence would discard possible correlated endpoint assignments; the correct datum in that case is (K(A,B\mid i,j)).

For a hard partition (h:V\to\mathcal A), (C(A\mid i)=\mathbf1_{A=h(i)}). A normalized soft membership permits several nonzero values for one child while preserving unit mass. A literal replicated cover instead has incidence (R(A\mid i)\in\{0,1\}) with (sum_AR(A\mid i)>1) allowed. It is not a Markov kernel and retains multiplicity; treating it as (C) double-counts mass and shared factors.

Nested normalized memberships compose as typed Markov kernels:

\[
C_{20}(B\mid i)
=\sum_A C_{21}(B\mid A)C_{10}(A\mid i).
\]

The same statement for endpoint events requires composition of the declared joint endpoint kernels. Product endpoint kernels compose as products only while their conditional-independence hypotheses remain true. Shared children generally induce correlated parents or shared effective factors.

## 7. Boundary marks and exact retained state

Choose rooted trees inside coarse blocks. For a fine boundary edge (j\to i) from source block (B) to receiver block (A), define the channel-typed dressed mark

\[
V_{ij}^x
=\tau_{A\leftarrow i}^xT_{ij}^x
(\tau_{B\leftarrow j}^x)^{-1}.
\]

The exact coarse marked measure is

\[
\Xi_{AB}^x(D)
=\sum_{i,j}\eta_{ij}^xK(A,B\mid i,j)
\mathbf1_{\{V_{ij}^x\in D\}},
\]

and, on (eta_{AB}^{x,c}>0), its conditional mark law is

\[
\kappa_{AB}^x(D)
=\frac{\Xi_{AB}^x(D)}{\eta_{AB}^{x,c}}.
\]

Conditional expectations of a linear representation (R_x(V)) may be derived under Bochner integrability, but the result need not lie in (R_x(G)). For example, the arithmetic mean of the two planar rotations by (\pi/2) and (-\pi/2) is the zero matrix. It is neither invertible nor a group element. Separate means of marks and features also fail to determine the mean product when they are correlated.

Exact coarse state therefore retains the internal based holonomy representation, the boundary-mark conditional law or raw marked edges, all induced hyperedges and shared factors, and path memory or an exact memory kernel. Any removal needs a theorem matched to the declared scope; a scalar average or memoryless pairwise ansatz is a truncation otherwise.

## 8. Exact VFE closure and its residual

Fix a regular observation (o), posterior (Pi_o), and recognition law (Q_o). Let (C:\mathsf Y\rightsquigarrow\mathsf Z) be one normalized standard-Borel Markov channel that is fixed independently of (Q_o), does not alter the observation coordinate, and is applied to both laws. Define (Q_o^c=Q_oC) and (Pi_o^c=\Pi_oC). The lifted joints (Q_o(dy)C(y,dz)) and (Pi_o(dy)C(y,dz)) have regular conditional laws (Q_o(dy\mid z)) and (Pi_o(dy\mid z)). The relative-entropy chain rule gives, with the extended support convention,

\[
\operatorname{KL}(Q_o\Vert\Pi_o)
=\operatorname{KL}(Q_o^c\Vert\Pi_o^c)
+\int\operatorname{KL}\left(
Q_o(\cdot\mid z)\Vert\Pi_o(\cdot\mid z)
\right)Q_o^c(dz).
\]

Using the same evidence representative at both scales, define

\[
\mathcal F_o(Q)=-\log p(o)+\operatorname{KL}(Q\Vert\Pi_o).
\]

Then

\[
\mathcal F_o(Q_o)
=\mathcal F_o^c(Q_o^c)
+\Delta_C(Q_o,\Pi_o),
\]

where the displayed conditional-KL integral is the nonnegative exact defect (Delta_C). When the fine KL is finite, (Delta_C=0) exactly when

\[
Q_o(\cdot\mid z)=\Pi_o(\cdot\mid z)
\quad Q_o^c\text{-almost surely}.
\]

Thus zero defect gives exact coarse/fine VFE equality, while nonzero defect is retained explicitly. A fitted coarse model, different posterior and recognition channels, a channel that reads (Q_o), or a simultaneous change of evidence lies outside this theorem. Low singleton-marginal KL does not imply a small or finite conditional defect.

## 9. Declared inference flow and moving-map semiconjugacy

An inference-flow parameter exists only after a flow is declared. Let (y(t)) solve a fine vector field (dot y=X_t(y)), let (C_t) be a (C^1) moving coarse map, and put (z(t)=C_t(y(t))). The ordinary chain rule gives the exact identity

\[
\dot z(t)
=\partial_tC_t(y(t))
+D C_t(y(t))X_t(y(t)).
\]

The moving map semiconjugates the fine flow to (dot z=\overline X_t(z)) exactly when

\[
\partial_tC_t+D C_tX_t
=\overline X_t\circ C_t
\]

on the declared domain. Omitting (partial_tC_t) is valid only for a frozen coarse map. The parameter (t) here is not a coordinate on the contextual base, physical time, or RG depth.

As a conditional frozen Gaussian/feature corollary, let (R\succ0) and (L\succeq0) be constant and let (R\dot z=-Lz). With (Pi_0^R) the (R)-orthogonal projector onto (ker L) and (lambda_+>0) the least positive eigenvalue of (R^{-1/2}LR^{-1/2}),

\[
\|z(t)-\Pi_0^Rz(0)\|_R
\leq e^{-\lambda_+t}
\|z(0)-\Pi_0^Rz(0)\|_R.
\]

This is the proved frozen constant-metric stability result. It becomes a meta-agent flow statement only after the displayed semiconjugacy condition is verified. Adaptive (\beta) or (\gamma), nonlinear full-law VFE dynamics, dynamically selected memberships, rank-changing metrics, and autonomous coarse dynamics remain open.

## 10. Exact scope boundary

The results above are established at the fixed point (r_*) under their stated hypotheses. The extension across (R), patch gluing, active-set changes, a canonical partition selector, literal multiple-parent membership, autonomous agency, physical time, continuum limits, a noncompact invariant barycenter theorem, and an intrinsic threshold remain open. Numerical or symbolic recomputation can test the contained finite witnesses but is not proof of any universal mathematical claim.
