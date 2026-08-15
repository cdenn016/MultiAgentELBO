<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-48389cdfa67c229a7a179881667aa14591ad8c4b126a506781a189e1b82d2d06","schema_version":"rigorous-theory-search/v1","target_digest":"48389cdfa67c229a7a179881667aa14591ad8c4b126a506781a189e1b82d2d06"} -->
# Construction or strongest theorem

## Strongest certified pointwise meta-agent theorem

Fix one base point (r_*). Let the active finite vertex set be nonempty. For each channel (x in {q,m}), let the vertex sample fibers be standard Borel, let (p_i^x) be normalized laws, let the positive-support graph be connected, and let every support edge carry a reciprocal bimeasurable bijection (T_{ij}^x:Z_j^x to Z_i^x) with (T_{ji}^x=(T_{ij}^x)^{-1}). Let (eta_{ij}^x) be the normalized joint directed edge-event weights induced by positive receiver weights and normalized conditional rows, and let (w_i^x>0) be normalized barycenter weights. Use the repository order (T_{ij}:j to i).

Under the additional side conditions stated below, the following conjunction is established.

1. The reciprocal arrows form a path groupoid. A rooted spanning tree and its non-tree fundamental cycles generate all based loop constraints. For nonabelian holonomy, triangle products suffice only when the based triangle loop words normally generate the graph fundamental group, as when attaching the declared triangular 2-cells gives a simply connected filled triangulation. Cycle-space spanning alone suffices only for abelian holonomy.
2. In the positive-definite represented connection-Laplacian sector, root evaluation gives (ker L_x isomorphic to Fix(Hol_r^x)); the full K-sector is present exactly when every represented holonomy is the identity. This is a frame statement, not a law-agreement theorem.
3. For each channel, zero weighted edge distortion is equivalent to transported equality on every positive-support edge and equivalent to one unique common root law fixed by the full channel holonomy group. The paired conclusion constructs (Q_q,Q_m), not a joint belief-model law.
4. For arbitrary probability laws (P_i), positive normalized weights (w_i), mixture (M=sum_i w_i P_i), and any comparison law (R),

\[
\sum_i w_i\operatorname{KL}(P_i\Vert R)
=
\sum_i w_i\operatorname{KL}(P_i\Vert M)
+\operatorname{KL}(M\Vert R).
\]

in the extended nonnegative reals. Hence (M) is the unique unrestricted forward-KL minimizer. Trivial holonomy gives immediate path independence; finite holonomy admits normalized orbit averaging; compact continuous holonomy requires the recorded measurable-domination and finite-integral hypotheses; no general noncompact theorem is asserted.
5. Use the convention (\operatorname{TV}(P,Q)=\frac12\lVert P-Q\rVert_1). If (\mathcal D_x\leq\varepsilon_x<\infty), fix one rooted spanning tree (\mathsf T_x), orient every tree edge in a direction of positive event weight, and put

\[
\eta_{\min}^x=\min_{(i,j)\in E(\mathsf T_x)}\eta_{ij}^x,
\qquad
d_x=\operatorname{diam}(\mathsf T_x),
\qquad
\delta_x=\sqrt{\frac{\varepsilon_x}{2\eta_{\min}^x}}.
\]

After transporting all laws along their unique tree paths to the root, every pair satisfies (TV(P_i^x,P_j^x)\leq d_x\delta_x), and every transported law is within (d_x\delta_x) of their weighted root mixture.
6. Scalar attention renormalizes exactly by pushing the normalized joint edge-event law through any declared normalized endpoint kernel and then disintegrating; it requires no parent root. A product kernel encodes a declared conditional-independence specialization, while correlated endpoint assignments require their full normalized kernel.
7. Marked closure is the explicit incidence-supported component-rooted tier. For each channel and parent A, refine V_A={i:C(A|i)>0} into connected components of the induced positive-support transport graph and root each component separately. The component-indexed marked event masses sum to the scalar A,B event mass, while the exact state retains each component's conditional law of dressed boundary transports and internal based holonomy. An arithmetic mean of group matrices is not generally a group element and is not an exact coarse link.

The Theory/07b hyperedge/shared-factor, full path-law, and exact memory closures are conditional imports only under their separate joint-density/factorization, full-path-law/transport, and linear T, C, P with CP=I hypotheses. Those data are absent here, so those richer claims remain OPEN outside target ancestry.
8. Applying one fixed recognition-independent common coarse Markov channel to posterior and recognition laws gives

\[
\mathcal F_o(Q_o)
=\mathcal F_o^c(Q_oC)
+\int\operatorname{KL}\left(
Q_o(\cdot\mid z)\Vert\Pi_o(\cdot\mid z)
\right)(Q_oC)(dz).
\]

When the fine KL is finite, the residual vanishes exactly at conditional-law equality almost surely. Low marginal KL does not imply this condition.
9. Normalized hard and soft memberships compose as typed Markov kernels. Literal replicated covers remain nonnormalized and retain multiplicity. If a differentiable fine flow and a C1 moving coarse map are declared, exact semiconjugacy is equivalent to

\[
\partial_t C_t+D C_t X_t=\overline X_t\circ C_t.
\]

The frozen constant-metric Gaussian or feature flow is only a conditional spectral corollary.
10. The eight excluded shortcut claims have explicit exact counterexamples, including the nonlinear Gaussian-boundary residual (2\lambda a^4).

## Proof architecture

The groupoid statement is a finite spanning-tree reduction. Every closed walk reduces, after canceling inverse tree steps, to a product of fundamental cycles and inverses. The positive-definite connection energy is a sum of squared edge residuals, so its kernel is exactly the parallel-section space. Root evaluation is injective, its image is holonomy fixed, and a fixed root vector extends back along the tree.

For zero distortion, every summand is a nonnegative extended KL multiplied by a strictly positive event weight. The sum vanishes exactly when each supported KL vanishes, hence when each transported pair of laws is equal. Reciprocal inversion supplies the equality in either path orientation. Tree propagation produces the root law, loops stabilize it, and adjoining one edge to a root path proves the converse. The identity path proves uniqueness.

For the full-law barycenter, each (P_i) is dominated by (M) with density at most (1/w_i), so every source-to-mixture KL is finite. If (M) is not dominated by (R), support failure makes both sides infinite. If (KL(M||R)) is infinite, mixture convexity makes the aggregate source-to-(R) term infinite. In the remaining finite case, Radon-Nikodym factorization through (M), together with domination-based integrability, gives the displayed identity without subtracting infinities. Nonnegativity and the KL zero criterion give uniqueness.

For the approximate result, each selected tree-edge KL is at most (\varepsilon_x/\eta_{\min}^x). Pinsker gives the edge TV bound (\delta_x). Transport invariance gives the same bound between adjacent root-frame laws, and the TV triangle inequality telescopes along the unique tree path between any pair. Convexity of TV gives the mixture bound. No triangle inequality is applied to KL.

Normalized event pushforward and disintegration prove scalar closure for arbitrary normalized endpoint kernels. For marked closure, incidence support assigns every selected endpoint to a unique induced parent component; rooting every component separately makes the dressed mark well typed, component pushforward preserves mass, and summing component endpoint pairs recovers each scalar parent-pair event mass. The zero matrix obtained by averaging the two opposite quarter-turn rotations proves that a matrix moment need not remain in the group. No hypergraph or path-memory theorem is inferred from that pushforward. Standard-Borel relative-entropy disintegration after one common channel proves the VFE defect. The tower property proves normalized hierarchy composition, and the ordinary chain rule proves the moving-map identity.

The contained counterexample derivations prove all eight existential refutations. For the nonlinear Gaussian case, equally weighted child laws (N(-a,1)) and (N(a,1)) have moment-matching Gaussian parent (N(0,1+a^2)). With (H(x)=\lambda x^4), the parent expectation minus the child average is the signed residual

\[
\lambda\left(3(1+a^2)^2-(a^4+6a^2+3)\right)=2\lambda a^4.
\]

## Dependency and evidence closure

The target depends on TYPE-GROUPOIDS, ZERO-DISTORTION, FULL-LAW-BARYCENTER, TV-STABILITY, EVENT-LAW-RENORMALIZATION, RETAINED-MARKS, VFE-CHAIN-RULE, HIERARCHY-SEMICONJUGACY, and COUNTEREXAMPLES. Every dependency is EVIDENCE_VERIFIED.

The direct mathematical evidence is evidence/direct-derivation.md (SHA-256 7860e7cfd631352fd1f4d6dc4de72bd06383b2c02d7fd8d09cce0e8c5230e790) and evidence/counterexample-proofs.md (SHA-256 a18f11f19bda4935462acf1b3974de59fb44efd341880aa03c082d05003ef883). The deterministic script and output are separately classified as symbolic corroboration and do not close mathematical claims.

## Quantifier-sensitive certificate

The certificate is universal over every frozen in-scope network and comparison law described by the target quantifiers; retained marks additionally quantify over incidence-supported endpoint assignments and rooted connected-component refinements, while existential witnesses occur only for the eight shortcut refutations. Compact continuous holonomy is conditional on the explicit measurable-domination and finite-integral hypotheses. The frozen spectral statement is conditional on constant positive-definite metric data. No cross-base or autonomous dynamic conclusion is quantified into the theorem.

## Open boundary

Extension over the contextual base R, patch gluing, active-set changes, a canonical partition selector, literal full multiple-parent membership as a probability channel, autonomous agency, physical time, continuum limits, an intrinsic threshold, general noncompact invariant averaging, adaptive attention dynamics, nonlinear full-law semiconjugacy, and dynamically selected memberships remain open or outside scope. These do not weaken the complete affirmative certificate for the frozen conjunction.
