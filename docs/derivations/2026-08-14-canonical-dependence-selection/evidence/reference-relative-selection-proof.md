<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-b8102c1f5917a6cbc9a69df8b10c1470d18d5146f56093a253b1a8644465bccb","schema_version":"rigorous-theory-search/v1","target_digest":"b8102c1f5917a6cbc9a69df8b10c1470d18d5146f56093a253b1a8644465bccb"} -->
# Reference-relative finite selection, deterministic completion, and retained VFE descent

## 1. Finite I-projection problem and support convention

Let \(X\) be a nonempty finite set, let \(p\in\Delta(X)\), put \(A=\operatorname{supp}p\), and let \(T:X\to\mathbb R^d\). For a target moment \(m\in\mathbb R^d\), define

\[
\mathcal Q_m=\left\{q\in\Delta(X):\sum_xq(x)T(x)=m\right\},
\qquad
D(q\|p)=\sum_xq(x)\log\frac{q(x)}{p(x)}.\tag{1}
\]

The finite-KL convention is \(0\log(0/p)=0\), while a term with \(q(x)>0=p(x)\) is \(+\infty\). Thus \(D(q\|p)<\infty\) exactly when \(q\ll p\). Write

\[
C_p=\operatorname{conv}T(A).\tag{2}
\]

A *finite minimizer* below means a feasible law whose objective value is finite. This excludes the vacuous statement that every infeasible-support law ties at \(+\infty\).

## 2. Existence and uniqueness as a law

**Theorem 2.1 (finite reference I-projection, claim `SEL-REFERENCE-IPROJECTION`).** A finite minimizer

\[
q_{p,m}=\arg\min_{q\in\mathcal Q_m}D(q\|p)\tag{3}
\]

exists if and only if \(m\in C_p\). Whenever it exists, it is unique as a probability law.

**Proof.** If a finite feasible \(q\) exists, then \(q\ll p\), so

\[
m=\sum_{x\in A}q(x)T(x)\in\operatorname{conv}T(A)=C_p.
\]

Conversely, if \(m\in C_p\), the definition of convex hull supplies a law supported on \(A\) with moment \(m\), so the feasible finite-KL set is nonempty. It is the intersection of the simplex on \(A\) with affine constraints, hence compact. Because \(p(x)>0\) for \(x\in A\), each scalar function \(t\mapsto t\log(t/p(x))\), extended by zero at \(t=0\), is continuous. The objective therefore attains its minimum. It is strictly convex on the simplex on \(A\): \(\sum_xq(x)\log q(x)\) is strictly convex and \(-\sum_xq(x)\log p(x)\) is affine. The feasible set is convex, so two distinct minimizers are impossible. \(\square\)

This uniqueness is relative to the declared reference \(p\), statistic \(T\), target moment \(m\), and finite-KL support convention. It is not an absolute selector from marginal data.

## 3. Minimal face and exact optimizer support

Let \(F_m\) be the unique minimal face of the polytope \(C_p\) containing \(m\); equivalently, \(m\in\operatorname{ri}F_m\). Define

\[
A_m=\{x\in A:T(x)\in F_m\}.\tag{4}
\]

**Lemma 3.1 (face support).** Every finite-KL law in \(\mathcal Q_m\) is supported on \(A_m\), and the optimizer \(q_{p,m}\) has exact support \(A_m\).

**Proof.** Every face of a polytope is exposed. If \(F\) is an exposed face containing \(m\), choose an affine functional \(\ell\) whose maximum \(c\) on \(C_p\) is attained exactly on \(F\). For a feasible \(q\),

\[
c=\ell(m)=\sum_{x\in A}q(x)\ell(T(x))\le c.
\]

Equality of this convex average with the maximum forces \(q(x)=0\) whenever \(T(x)\notin F\). Intersecting over the exposed faces whose intersection is the minimal face gives \(\operatorname{supp}q\subseteq A_m\).

Because \(m\in\operatorname{ri}F_m=\operatorname{ri}\operatorname{conv}T(A_m)\), there exists a feasible law \(q^+\) positive at every point of \(A_m\). One direct construction starts from a relative-interior convex representation and, for each omitted generator \(T(x)\), transfers a sufficiently small positive mass to it while compensating inside a small relative ball around \(m\); finiteness permits all transfers simultaneously. If the minimizer had \(q_{p,m}(x_0)=0\) for some \(x_0\in A_m\), set \(q_t=(1-t)q_{p,m}+tq^+\). The one-sided derivative of \(t\log(t/p(x_0))\) at zero is \(-\infty\), while all positive-coordinate contributions have finite one-sided derivatives. Hence \(D(q_t\|p)<D(q_{p,m}\|p)\) for all sufficiently small \(t>0\), contradicting optimality. Thus every point of \(A_m\) has positive optimizer mass. \(\square\)

The exact-support conclusion uses \(A_m\subseteq\operatorname{supp}p\). If one instead calls every point with \(T(x)\in F_m\) part of the face support, including points where \(p(x)=0\), the conclusion is false: finite KL forbids positive optimizer mass there.

## 4. Statistic minimalization and exponential form

Work on \(A_m\). Choose affine coordinates on \(\operatorname{aff}F_m\), producing a statistic \(\widetilde T:A_m\to\mathbb R^r\), \(r=\dim F_m\), whose differences span \(\mathbb R^r\). Let \(\widetilde m\) be the coordinate image of \(m\), and define

\[
\psi(\lambda)=\log\sum_{x\in A_m}p(x)e^{\lambda\cdot\widetilde T(x)},
\qquad
q_\lambda(x)=p(x)e^{\lambda\cdot\widetilde T(x)-\psi(\lambda)}.\tag{5}
\]

Here \(q_\lambda(x)=0\) off \(A_m\). The Hessian of \(\psi\) is the covariance matrix of \(\widetilde T\) under the positive law \(q_\lambda\). If \(v^\mathsf T\nabla^2\psi(\lambda)v=0\), then \(v\cdot\widetilde T\) is constant on \(A_m\); the spanning property forces \(v=0\). Thus \(\nabla^2\psi\) is positive definite.

Consider \(\phi_{\widetilde m}(\lambda)=\psi(\lambda)-\lambda\cdot\widetilde m\). Since \(\widetilde m\) lies in the interior of the full-dimensional polytope \(\operatorname{conv}\widetilde T(A_m)\), compactness of the unit sphere gives a uniform positive gap between every supporting value \(\max_xv\cdot\widetilde T(x)\) and \(v\cdot\widetilde m\). Therefore \(\phi_{\widetilde m}(tv)\to+\infty\) uniformly as \(t\to\infty\). The strictly convex coercive function \(\phi_{\widetilde m}\) has a unique minimizer \(\lambda(\widetilde m)\), and its first-order equation is

\[
\nabla\psi(\lambda)=\mathbb E_{q_\lambda}\widetilde T=\widetilde m.\tag{6}
\]

For any feasible \(q\) supported on \(A_m\),

\[
\begin{aligned}
D(q\|p)-D(q\|q_\lambda)
&=\sum_xq(x)\log\frac{q_\lambda(x)}{p(x)}\\
&=\lambda\cdot\widetilde m-\psi(\lambda),
\end{aligned}\tag{7}
\]

which is independent of \(q\). Taking \(q=q_\lambda\) shows that (7) is exactly \(D(q_\lambda\|p)\); hence \(q_\lambda=q_{p,m}\) by uniqueness.

In the original statistic, the same law may be written

\[
q_{p,m}(x)=p(x)\exp\{\alpha\cdot T(x)-\Psi(\alpha)\},
\qquad x\in A_m.\tag{8}
\]

The multiplier in (8) is unique only modulo

\[
\mathcal N_m=\{v:v\cdot T(x)\text{ is constant on }A_m\}.\tag{9}
\]

Adding \(v\in\mathcal N_m\) changes the normalizer by that same constant and leaves the law unchanged. After the affine minimalization in (5), \(\mathcal N_m=\{0\}\), so \(\lambda\) is unique.

The minimalization hypothesis is load-bearing for multiplier uniqueness. On a bit with redundant statistic \(T(x)=(x,2x)\), every \((\alpha_1,\alpha_2)\) with fixed \(\alpha_1+2\alpha_2\) defines the same law.

## 5. Oriented Pythagorean identity

For every feasible \(q\) with finite KL, Lemma 3.1 and (8) give

\[
\begin{aligned}
&D(q\|p)-D(q\|q_{p,m})-D(q_{p,m}\|p)\\
&\quad=\sum_{x\in A_m}(q(x)-q_{p,m}(x))
\log\frac{q_{p,m}(x)}{p(x)}\\
&\quad=\alpha\cdot\left(\mathbb E_qT-\mathbb E_{q_{p,m}}T\right)
-\Psi(\alpha)\left(\sum_xq(x)-\sum_xq_{p,m}(x)\right)=0.
\end{aligned}\tag{10}
\]

Thus the exact orientation is

\[
D(q\|p)=D(q\|q_{p,m})+D(q_{p,m}\|p).\tag{11}
\]

If a feasible \(q\) assigns mass outside \(\operatorname{supp}p\), then both \(D(q\|p)\) and \(D(q\|q_{p,m})\) are \(+\infty\), while the last term is finite, so (11) remains a valid extended-real identity \(+\infty=+\infty+\text{finite}\). The algebra in (10) is asserted only for finite-KL \(q\); it never subtracts infinities.

## 6. Relative-interior analytic strata and boundary controls

Fix a face \(F\) of \(C_p\) and let \(m\in\operatorname{ri}F\). Then \(A_m=A_F\) is locally fixed. In minimal affine coordinates, \(\psi\) is real analytic and its Hessian is positive definite. The analytic inverse-function theorem applied to \(\nabla\psi\) makes \(\lambda(m)\), and hence every atom of \(q_{p,m}\), real analytic on \(\operatorname{ri}F\) in its affine coordinates. This is the precise analytic-stratum claim; no smoothness across a face change is asserted.

Two controls show why the qualifications cannot be dropped.

* If \(X=\{0,1\}\), \(p=\delta_0\), and \(T(x)=x\), then \(C_p=\{0\}\). The target \(m=1\) is feasible only by \(q=\delta_1\), for which \(D(q\|p)=+\infty\); no finite minimizer exists.
* If \(p=(1/2,1/2)\) and \(T(x)=x\), then \(q_{p,m}=(1-m,m)\) for \(0\le m\le1\), but the fixed-support natural parameter \(\lambda(m)=\log[m/(1-m)]\) diverges at both boundary faces and the optimizer support jumps. Thus one cannot extend the interior exponential chart, its finite multiplier, or its fixed-support statistical stratum smoothly through the boundary merely because the mass-vector limit exists.

## 7. Transported-reference equivariance and reference dependence

Let \(\varphi:X\to X'\) be a bijection. Suppose the entire constraint diagram is transported:

\[
p'=\varphi_\#p,
\qquad
T'(\varphi x)=LT(x)+b,
\qquad
m'=Lm+b,
\tag{12}
\]

where \(L\) is injective on \(\operatorname{aff}C_p\). Pushforward by \(\varphi\) bijects the feasible sets, preserves supports, and reindexes the finite KL sum:

\[
D(\varphi_\#q\|\varphi_\#p)=D(q\|p).\tag{13}
\]

Uniqueness relative to the transported reference and constraints therefore gives

\[
q_{p',m'}=\varphi_\#q_{p,m}.\tag{14}
\]

Equation (14) is the reference-relative equivariance claim. It requires coherent transport of the reference and constraint diagram. For a counterexample, let \(X=\{a,b,c\}\), \(T(a)=T(b)=0\), \(T(c)=1\), and target \(m=1/2\). The constraint fixes \(q(c)=1/2\), while minimization splits the remaining mass as

\[
q(a):q(b)=p(a):p(b).
\]

Swapping \(a,b\) while holding a nonsymmetric reference \(p(a)\ne p(b)\) fixed does not commute with selection. The reference must be pushed forward as in (12).

For singleton-indicator constraints on a finite product space and a positive reference, (8) becomes

\[
\log q_{p,m}(x)=\log p(x)+\sum_i\alpha_i(x_i)-\Psi.\tag{15}
\]

Every higher-order log-linear contrast annihilates constants and sums of one-coordinate functions, so (15) has exactly the higher-order interaction contrasts of \(\log p\). They are inherited from the declared reference, not derived from the target marginals. A product reference remains product after the unary tilt and therefore yields the product law with the target marginals. If a correlated reference already has the target marginals, it is itself feasible and has KL zero, so uniqueness relative to that reference selects it unchanged.

## 8. Deterministic posterior completion

Let \(f:X\to Y\) be a deterministic map of nonempty finite sets, let \(p\in\Delta(X)\), write \(p_Y=f_\#p\), and let \(r\in\Delta(Y)\) satisfy \(r\ll p_Y\). Define

\[
L_f^p(r)(x)=
\begin{cases}
r(f(x))\,p(x)/p_Y(f(x)),&p_Y(f(x))>0,\\
0,&p_Y(f(x))=0.
\end{cases}\tag{16}
\]

On a zero-reference fiber \(p_Y(y)=0\), every \(p(x)\) in the fiber is zero and absolute continuity forces \(r(y)=0\); the second line is therefore normalized and removes every \(0/0\) ambiguity. Summing (16) on each fiber gives \(f_\#L_f^p(r)=r\), and summing over \(y\) gives total mass one.

For any \(q\) with \(f_\#q=r\) and finite \(D(q\|p)\), disintegrate on each \(r\)-positive fiber:

\[
D(q\|p)=D(r\|p_Y)
+\sum_{y:r(y)>0}r(y)
D\!\left(q(\cdot\mid y)\middle\|p(\cdot\mid y)\right).
\tag{17}
\]

The lift (16) has conditional law \(p(\cdot\mid y)\), so it attains the lower bound \(D(r\|p_Y)\). Equality in every finite conditional KL forces the same conditional on each \(r\)-positive fiber; zero-target fibers carry no mass. Hence (16) is the unique minimizing *law* relative to \((f,p,r)\), even though irrelevant kernel versions on zero-target fibers are not unique.

This proves claim `SEL-DETERMINISTIC-COMPLETION`. Absolute continuity is necessary: with \(p=\delta_0\), \(f\) the identity on a bit, and \(r=\delta_1\), every lift has infinite KL and (16) would otherwise contain an unsupported target fiber.

## 9. Strict nested composition with pushed references

Let \(X\xrightarrow{f}Y\xrightarrow{g}Z\) be deterministic, put \(p_Y=f_\#p\), \(p_Z=g_\#p_Y\), and let \(s\ll p_Z\). Then

\[
L_f^p\!\left(L_g^{p_Y}(s)\right)=L_{g\circ f}^p(s).\tag{18}
\]

For every \(x\) with \(p(x)>0\), both pushed-reference denominators are positive and cancellation gives

\[
L_f^p(L_g^{p_Y}s)(x)
=\frac{s(gf(x))p_Y(f(x))}{p_Z(gf(x))}
\frac{p(x)}{p_Y(f(x))}
=\frac{s(gf(x))p(x)}{p_Z(gf(x))}.
\]

If \(p(x)=0\), both sides of (18) are zero under convention (16). This proves strict equality of laws, not merely equality up to versions.

Using the pushed reference at each stage is load-bearing. Let \(X=\{a,b,c,d\}\), let \(f\) have fibers \(\{a,b\}\), \(\{c,d\}\), let \(g\) collapse \(Y\) to one point, and take \(p=(1/2,1/4,1/8,1/8)\). Direct completion is \(p\). If the \(Z\)-to-\(Y\) stage instead uses the arbitrary reference \(h=(1/2,1/2)\ne f_\#p=(3/4,1/4)\), the staged lift is \((1/3,1/6,1/4,1/4)\ne p\). Likewise, determinism cannot be silently replaced by an arbitrary channel: the channel that outputs a fair bit independently of its input has only the fair output law in its image and has no right inverse on all target laws.

## 10. Retained VFE optimization and August 13 presentation descent

Fix a finite retained state \(R\), observation \(o\), and a presentation \(a\) with positive evidence \(z^a=P^a_O(o)>0\) and retained posterior \(\pi^a=P^a(R\mid o)\). Its retained objective is

\[
\mathcal F^a_{\rm ret}(q)=-\log z^a+D(q\|\pi^a).\tag{19}
\]

**Theorem 10.1 (retained descent, claim `SEL-PRESENTATION-DESCENT`).** Under the August 13 equivalence of the complete retained joint law and completed retained conditioning algebra, equivalent presentations have equal \(z^a\) and \(\pi^a\) on every positive-evidence retained slice. If they use the same declared moment constraints \((T,m)\), Theorem 2.1 applied with reference \(\pi^a\) gives the same unique retained optimizer as a law and the same optimum of (19). In the unconstrained case the optimizer is \(q^*=\pi^a\) and the optimum is \(-\log z^a\).

For each presentation with deterministic forgetting map \(f_a:(R,E_a)\to R\), the full posterior supplies a presentation-specific reference \(p^a=P^a(R,E_a\mid o)\). Equation (16) gives the full recognition completion

\[
Q^{a,*}=L_{f_a}^{p^a}(q^*).
\tag{20}
\]

The conditional KL identity (17) shows that (20) uniquely minimizes the full VFE among recognition laws with retained marginal \(q^*\), and the optimized value equals the retained value. Thus the retained optimizer and optimized value descend under the August 13 equivalence, relative to the common retained constraints and positive slice. The full auxiliary law (20) does not descend: its sample space, conditional posterior, node inventory, and intervention typing can differ between equivalent presentations. This is exactly the boundary proved in the contained August 13 artifacts
`../../2026-08-13-finite-presentation-descent-joint-fisher/evidence/vfe-descent-proof.md` and
`../../2026-08-13-finite-presentation-descent-joint-fisher/evidence/bsc-presentation-proof.md`.

Equality of singleton marginals alone is not the August 13 equivalence and does not imply (19) agrees. Positive evidence is also load-bearing: at \(z=0\), the posterior slice is undefined and \(-\log z=+\infty\).

## 11. Qualified parameterized envelope differential

Let \(U\subset\mathbb R^k\) be open. On a neighborhood \(U_0\subset U\), assume:

1. \(z_\theta>0\) and the reference/posterior law \(\pi_\theta\) is positive, both \(C^1\) in \(\theta\);
2. the feasible set is one common, locally fixed affine slice \(\mathcal Q\) of one fixed support stratum;
3. \(\mathcal F(\theta,q)=-\log z_\theta+D(q\|\pi_\theta)\) has a unique optimizer \(q^*_\theta\in\mathcal Q\) that is \(C^1\) on \(U_0\); and
4. differentiation is taken with respect to this declared retained parameter, with finite sums permitting termwise differentiation.

For a tangent \(v\in T_\theta U_0\), the chain rule gives

\[
dV_\theta[v]
=\partial_\theta\mathcal F(\theta,q^*_\theta)[v]
+d_q\mathcal F(\theta,q^*_\theta)[dq^*_\theta v].\tag{21}
\]

Because \(dq^*_\theta v\) lies in the tangent of the locally fixed feasible affine slice and the optimizer is stationary on that slice, the second term is zero. Therefore

\[
dV_\theta[v]
=-d\log z_\theta[v]
-\sum_rq^*_\theta(r)\,d\log\pi_\theta(r)[v].\tag{22}
\]

If two August 13-equivalent presentation families have the same retained joint law and completed conditioning algebra *parameterwise* on \(U_0\), and the same fixed feasible slice, then \(z_\theta,\pi_\theta,q^*_\theta,V_\theta\), and (22) agree. Under exactly these familywise, support-stratum, feasible-set, positivity, and \(C^1\) hypotheses, the retained optimizer, value, and envelope differential descend. Presentation-specific auxiliary completions still do not.

The hypotheses cannot be inferred from pointwise equality. A constant fair Bernoulli posterior and \(\operatorname{Ber}(1/2+t)\) agree at \(t=0\) but not as families. A moving feasible singleton \(q_\theta=(1-\theta,\theta)\) with fixed uniform \(\pi\) has \(\partial_\theta\mathcal F(\theta,q)=0\) at fixed \(q\), while the optimized value \(D(q_\theta\|\pi)\) generally has nonzero derivative; this shows why the feasible set must be locally fixed. Finally, restricting a Bernoulli recognition law to the nonconvex set \(\{\delta_0,\delta_1\}\) yields a switch and two minimizers at a fair posterior, with optimum \(-\log\max\{\pi_\theta(0),\pi_\theta(1)\}\) nondifferentiable at the switch. This shows why a unique \(C^1\) optimizer on a fixed stratum is required for (22).

## 12. Dependency map and scope

| Claim | Exact dependencies | Result |
| --- | --- | --- |
| `SEL-REFERENCE-IPROJECTION` | finite counting measure; support convention (1); \(m\in C_p\); strict convexity; minimal-face support; statistic minimalization | existence iff, unique law relative to \((p,T,m)\), exact support, exponential form, (11), analytic on each fixed relative-interior face stratum, transported-reference equivariance |
| `SEL-DETERMINISTIC-COMPLETION` | deterministic \(f\); \(r\ll f_\#p\); zero-reference convention; conditional KL identity | unique law (16) and strict pushed-reference composition (18) |
| `SEL-PRESENTATION-DESCENT` | August 13 retained-joint/conditioning equivalence; positive evidence; common retained constraints; for (22), positive \(C^1\) family, locally fixed feasible support stratum, and unique \(C^1\) optimizer | retained optimizer/value descend; envelope differential descends only under the stated familywise hypotheses; full auxiliary completion does not |

These positive theorems are logically independent of the absolute selector refutation. Their uniqueness statements are always relative to an explicit reference, morphism, constraint, support stratum, or equivalence class in the same paragraph. They provide no autonomous-agency, continuum, intervention-recovery, or physical-geometry conclusion.
