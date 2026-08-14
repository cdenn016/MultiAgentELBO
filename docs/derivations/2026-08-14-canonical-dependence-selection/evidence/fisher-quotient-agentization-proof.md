<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-8112f0083a554a4df3b5de3875174d0b0cbfeee36a7bc2ea20e78c8cf9da6b39","schema_version":"rigorous-theory-search/v1","target_digest":"8112f0083a554a4df3b5de3875174d0b0cbfeee36a7bc2ea20e78c8cf9da6b39"} -->
# Retained Fisher quotient and law-only agentization boundary

## 1. Types and scope

Let \(\Theta\) and \(N\) be finite-dimensional smooth manifolds, let
\(\rho:\Theta\to N\) be a smooth retained-law map, and let \(g\) be a
smooth positive-semidefinite symmetric two-tensor on \(N\). Write

\[
h=\rho^*g,
\qquad
h_\theta(v,w)=g_{\rho(\theta)}(d\rho_\theta v,d\rho_\theta w).
\tag{1}
\]

In the finite categorical application, \(N\) is an open probability-simplex
stratum and \(g\) is its Fisher metric. It is then positive definite. The
semidefinite statement below is kept because it identifies the exact extra
condition needed in a more general retained model. Every statement is about
declared tangent blocks or retained statistical laws. No block is inferred to
be an autonomous agent, and no Fisher tensor is identified with physical
geometry.

## 2. Exact radical and the two different quotients

### Theorem 1 (pointwise radical)

At every \(\theta\in\Theta\),

\[
\operatorname{rad}h_\theta
=(d\rho_\theta)^{-1}
  \bigl(\operatorname{rad}g_{\rho(\theta)}\bigr).
\tag{2}
\]

Consequently,

\[
\operatorname{rad}h_\theta=\ker d\rho_\theta
\quad\Longleftrightarrow\quad
\operatorname{im}d\rho_\theta\cap
\operatorname{rad}g_{\rho(\theta)}=\{0\}.
\tag{3}
\]

In particular, (3) holds whenever \(g\) is positive definite on
\(\operatorname{im}d\rho_\theta\), including the positive finite categorical
Fisher tier.

**Proof.** For a positive-semidefinite symmetric form \(b\),
\(b(u,u)=0\) if and only if \(u\in\operatorname{rad}b\). Indeed, positivity of
\(b(u+tw,u+tw)\) for every real \(t\), together with \(b(u,u)=0\), forces
\(b(u,w)=0\) for every \(w\). Now \(v\in\operatorname{rad}h_\theta\) implies
\(0=h_\theta(v,v)=g(d\rho v,d\rho v)\), so
\(d\rho v\in\operatorname{rad}g\). The converse follows immediately from
(1). This proves (2). Since \(\ker d\rho\) is always contained in the
preimage in (2), equality with the kernel holds exactly when no nonzero
vector in \(\operatorname{im}d\rho\) is Fisher-radical, which is (3).
\(\square\)

### Smooth quotient bundle

Assume (3) on an open set \(U\subseteq\Theta\) and assume \(d\rho\) has
constant rank there. Then

\[
K=\ker d\rho\subset TU,
\qquad
I=\operatorname{im}d\rho\subset\rho^*TN
\tag{4}
\]

are smooth vector subbundles. The fiberwise quotient
\(Q=TU/K\) is a smooth vector bundle, and

\[
\bar h([v],[w])=h(v,w)
\tag{5}
\]

is a well-defined positive-definite bundle metric. The induced map
\([v]\mapsto d\rho(v)\) is an isometric vector-bundle isomorphism
\(Q\cong I\). Constant rank is used only for these smooth subbundle and
quotient-bundle conclusions. If \(g\) is degenerate and (3) fails, constant
rank of \(d\rho\) alone does not make \(\operatorname{rad}h\) a smooth
subbundle; constant rank of the radical preimage is then a separate
hypothesis.

### Global quotient manifold

The bundle \(TU/K\) is not automatically the tangent bundle of a global
quotient manifold. Such an interpretation requires a smooth Hausdorff
manifold \(\bar U\) and a surjective submersion
\(q:U\to\bar U\) whose connected fibers are exactly the null leaves and for
which \(\ker dq=K\). Equivalently, the null foliation must be simple and its
leaf space regular; involutivity is necessary but does not ensure Hausdorffness
or a manifold leaf space.

For the specific tensor in (1), basicness is automatic once
\(K=\ker d\rho\) and such a \(q\) exists. Because \(d\rho\) vanishes on
\(K\), \(\rho\) is constant on each connected \(q\)-fiber. Surjective-
submersion descent gives a unique smooth map
\(\bar\rho:\bar U\to N\) with \(\rho=\bar\rho\circ q\). Therefore

\[
h=\rho^*g=q^*(\bar\rho^*g).
\]

Thus \(h\) is already horizontal and leafwise invariant:
\(\iota_Zh=0\) and \(\mathcal L_Zh=0\) for every
\(Z\in\Gamma(K)\). Basicness remains an extra hypothesis for an arbitrary
tensor on \(U\) whose radical happens to be \(K\), and for declared block
projectors or image subbundles. It is not an additional hypothesis for this
pullback \(h\). The simple/Hausdorff quotient requirement remains genuinely
extra.

A scope-matched failure is the punctured plane
\(U=\mathbb R^2\setminus\{0\}\), with
\(\rho(x,y)=y\), \(g=dy^2\), and hence \(h=dy^2\) and
\(K=\operatorname{span}\{\partial_x\}\). For \(y\ne0\), a null leaf is
the entire horizontal line. At \(y=0\), the puncture splits the fiber into
the two leaves \(x<0\) and \(x>0\). The connected-leaf space is a line
with doubled origin and is non-Hausdorff. Here \(h\) is manifestly the
pullback of \(dy^2\) and is basic, yet no smooth Hausdorff leaf-space
quotient realizes \(TU/K\) globally. This isolates the topology obstruction
without falsely attributing it to basicness.

## 3. Familywise presentation isometry

Let \((N_A,g_A)\) and \((N_B,g_B)\) be retained statistical manifolds. Let
\(\rho_A:\Theta_A\to N_A\) and \(\rho_B:\Theta_B\to N_B\) be smooth, and
suppose there are maps

\[
F:\Theta_A\to\Theta_B,
\qquad
J:N_A\to N_B,
\qquad
\rho_B\circ F=J\circ\rho_A.
\tag{6}
\]

Assume first that \(F\) is a diffeomorphism and \(J\) is a Fisher isometric
immersion on the retained family:

\[
g_B(dJ\,u,dJ\,v)=g_A(u,v)
\quad\text{for every retained point and tangent pair.}
\tag{7}
\]

Differentiating (6) gives

\[
d\rho_B\,dF=dJ\,d\rho_A.
\tag{8}
\]

At each \(\theta\in\Theta_A\), injectivity of \(dJ\) and invertibility of
\(dF_\theta\) imply

\[
dF_\theta(K_{A,\theta})=K_{B,F(\theta)}.
\]

No constant-rank hypothesis is needed for the pointwise quotient-vector-space
isometry

\[
\bar F_\theta:
T_\theta\Theta_A/K_{A,\theta}
\longrightarrow
T_{F(\theta)}\Theta_B/K_{B,F(\theta)},
\qquad [v]\longmapsto[dF_\theta(v)].
\tag{9}
\]

Indeed,

\[
h_B(dFv,dFw)=g_B(dJd\rho_Av,dJd\rho_Aw)
=g_A(d\rho_Av,d\rho_Aw)=h_A(v,w).
\tag{10}
\]

On open strata where both retained maps have constant rank, the quotient
spaces assemble into smooth bundles and the maps (9) assemble into a smooth
bundle isomorphism \(Q_A\to Q_B\) covering \(F\). Without constant rank,
(9) remains a pointwise statement only.

There is a useful redundant-presentation variant. Suppose \(F\) is instead
a surjective submersion, \(J\) remains an isometric immersion, and (6)
holds. At every \(\theta\), (8) maps \(K_{A,\theta}\) onto
\(K_{B,F(\theta)}\). To prove surjectivity, lift
\(w\in K_{B,F(\theta)}\) to \(v\) with \(dF_\theta v=w\); then
\(dJd\rho_Av=0\), so injectivity of \(dJ\) gives
\(v\in K_{A,\theta}\). Hence the induced map (9) is again a pointwise linear isometry.
On constant-rank strata, the correct global statement is the smooth
fiberwise isometry

\[
Q_A\cong F^*Q_B
\quad\text{over }\Theta_A,
\qquad
[v]_\theta\longmapsto
\bigl(\theta,[dF_\theta v]_{F(\theta)}\bigr).
\]

It is not a claim that the induced map from the total space of \(Q_A\) into
the total space of \(Q_B\) is injective: distinct points of one
\(F\)-fiber remain distinct base points in \(F^*Q_B\).

The rank qualifications are load-bearing. For
\(\Theta_A=\Theta_B=N_A=N_B=\mathbb R\), take
\(F(t)=t^2\), \(J=\operatorname{id}\),
\(\rho_A(t)=t^2\), and \(\rho_B(s)=s\). The diagram (6) commutes, but
\(F\) is not a submersion at zero. At \(t=0\),
\(T_0\Theta_A/K_{A,0}=0\), whereas
\(T_0\Theta_B/K_{B,0}\cong\mathbb R\); away from zero, both quotients are
one-dimensional. Thus a commuting diagram alone supplies neither a pointwise
isomorphism at the rank drop nor a smooth quotient-bundle isomorphism across
it.

A generic Markov pushforward does not meet these hypotheses. Data processing
gives Fisher contraction, not an isometry, and a lossy channel can create new
kernel directions. Equality for one tangent at one parameter is only local
score sufficiency. It supplies neither the familywise commuting diagram (6)
nor equality (7) on all retained tangents, and therefore cannot establish
kernel transport or a smooth quotient-bundle isometry. Likewise, equality of
two law values at one point does not identify their derivatives or Fisher
tensors; the complete retained family is the relevant object.

## 4. Declared blocks: exact linear theorem

Fix a point and abbreviate

\[
E=T_\theta\Theta=\bigoplus_{a=1}^m B_a,
\qquad L=d\rho_\theta:E\to W,
\qquad K=\ker L,
\tag{11}
\]

where the \(B_a\) are **declared** subspaces. Let
\(\pi:E\to E/K\) and \(\bar B_a=\pi(B_a)\). Then the following are
equivalent:

1. \(E/K=\bigoplus_a\bar B_a\);
2. \(\operatorname{im}L=\bigoplus_aL(B_a)\);
3. \(K=\bigoplus_a(K\cap B_a)\);
4. every quotient tangent has a unique linear decomposition
   \([v]=\sum_a[b_a]\) with \([b_a]\in\bar B_a\).

**Proof.** The induced map \(\widetilde L:E/K\to\operatorname{im}L\) is a
linear isomorphism and maps \(\bar B_a\) onto \(L(B_a)\), proving the
equivalence of 1, 2, and 4. If 2 holds and
\(k=\sum_ab_a\in K\), then \(\sum_aL(b_a)=0\); directness forces
\(L(b_a)=0\) for every \(a\), so
\(k\in\bigoplus_a(K\cap B_a)\). Conversely, if 3 holds and
\(\sum_aL(b_a)=0\), then \(\sum_ab_a\in K\). Its unique decomposition in
the ambient direct sum, together with 3, forces every
\(b_a\in K\cap B_a\), so the image sum is direct. \(\square\)

For smooth declared subbundles \(B_a\subset T\Theta\), this theorem is a
smooth bundle decomposition on a stratum when \(d\rho\) and every restriction
\(d\rho|_{B_a}\) have locally constant rank and the equivalent conditions
hold fiberwise. These rank hypotheses ensure that the intersections and image
spaces assemble as smooth subbundles rather than merely pointwise spaces.

### Energy additivity is stronger

Suppose (3) holds so that the quotient metric \(\bar h\) is positive definite.
For \([v]=\sum_a\bar v_a\),

\[
\bar h([v],[v])
=\sum_a\bar h(\bar v_a,\bar v_a)
+2\sum_{a<b}\bar h(\bar v_a,\bar v_b).
\tag{12}
\]

Therefore the unique linear block decomposition gives a unique additive
Fisher-energy attribution
\(\bar h([v],[v])=\sum_a\bar h(\bar v_a,\bar v_a)\) if and only if

\[
\bar h(\bar B_a,\bar B_b)=0
\quad(a\ne b).
\tag{13}
\]

Directness alone does not dispose of the cross terms. Assigning those terms to
one node or splitting them by convention would be extra attribution data.

### Basicness and presentation naturality

Assume \(\rho:\Theta\to N\) is a surjective submersion. The canonical map
\(T\Theta/K\cong\rho^*TN\) turns the quotient blocks into subspaces
\(d\rho(B_a)_\theta\subset T_{\rho(\theta)}N\). A block decomposition
descends to \(N\) exactly when there are smooth subbundles
\(C_a\subset TN\) such that

\[
d\rho(B_a)_\theta=(C_a)_{\rho(\theta)}
\quad\text{for every }\theta.
\tag{14}
\]

This is the basicness or projectability requirement. Put
\(D_a=B_a+K\). On a local quotient by the connected \(K\)-leaves,
projectability of the quotient distribution is exactly the bracket condition

\[
[\Gamma(K),\Gamma(D_a)]\subseteq\Gamma(D_a).
\]

This distribution condition must not be confused with projectability of one
vector field: an individual field \(X\) is projectable precisely when

\[
[Z,X]\in\Gamma(K)
\quad\text{for every }Z\in\Gamma(K).
\]

The bracket tests are local and propagate data only along connected leaves.
If a retained-law fiber is disconnected and the intended base identifies all
of its components, equality of the projected block subspaces across those
components is an additional global invariance condition.
Smoothness and pointwise orthogonality do not imply (14) or the distribution bracket condition.

Across two presentations satisfying (6), a descended node attribution is
natural only if the quotient isometry (9) also carries block classes by a
declared type-preserving permutation \(\sigma\):

\[
\bar F(\bar B_a^A)=\bar B_{\sigma(a)}^B.
\tag{15}
\]

The retained Fisher metric supplies neither the original \(B_a\) nor the
typing/permutation \(\sigma\). Equations (14)--(15) are additional structure,
not consequences of the quotient metric.

## 5. Rotating-block counterexample

Let \(\Theta=\mathbb R^3\) with coordinates \((x,y,z)\), let
\(N=\mathbb R^2\), and set \(\rho(x,y,z)=(x,y)\). Give \(N\) the Euclidean
metric, so

\[
h=dx^2+dy^2,
\qquad K=\operatorname{span}\{\partial_z\}.
\]

Define smooth declared blocks

\[
\begin{aligned}
e_1(z)&=\cos z\,\partial_x+\sin z\,\partial_y,\\
e_2(z)&=-\sin z\,\partial_x+\cos z\,\partial_y,\\
B_1&=\operatorname{span}\{e_1(z),\partial_z\},
\qquad B_2=\operatorname{span}\{e_2(z)\}.
\end{aligned}
\tag{16}
\]

Pointwise, \(T\Theta=B_1\oplus B_2\),
\(K=(K\cap B_1)\oplus(K\cap B_2)\), and the two quotient images are
one-dimensional and Fisher-orthogonal. Nevertheless, over the same retained
point \((x,y)\), the first image is the \(x\)-axis at \(z=0\) and the
\(y\)-axis at \(z=\pi/2\). Hence no subbundle \(C_1\subset TN\) can satisfy
(14). The local bracket obstruction is explicit:

\[
[\partial_z,e_1]=e_2\notin\Gamma(B_1+K),
\qquad
[\partial_z,e_2]=-e_1\notin\Gamma(B_2+K).
\]

The pointwise split and its block energies do not descend. This directly
separates smooth directness and orthogonality from fiberwise projectability.

## 6. Seven-outcome law/Fisher-only agentization no-go

Let \(q_*=(1/7,\ldots,1/7)\) on seven unlabeled outcomes. Its simplex tangent
and Fisher form are

\[
V=\left\{u\in\mathbb R^7:\sum_i u_i=0\right\},
\qquad g_{q_*}(u,v)=7\sum_i u_iv_i.
\tag{17}
\]

Assume, for contradiction, a rule depending only on the law and its Fisher
geometry assigns an unordered direct-sum decomposition

\[
V=B_1\oplus B_2\oplus B_3,
\qquad \dim B_a=2,
\tag{18}
\]

and is natural under every relabeling of the seven outcomes. The uniform law
and (17) are fixed by \(S_7\), so relabeling must permute the three distinct
blocks. This defines a homomorphism \(\varphi:S_7\to S_3\).

The restriction \(\varphi|_{A_7}\) is trivial. Here is a contained group
argument. The alternating group is generated by 3-cycles, and, using two
additional symbols \(d,e\), every 3-cycle has the commutator form

\[
[(bc)(de),(ab)(de)]=(abc).
\tag{19}
\]

Thus \(A_7=[A_7,A_7]\) is perfect. The image of a perfect group is perfect,
whereas the only perfect subgroup of \(S_3\) is the trivial subgroup: its
other subgroups are cyclic, or \(S_3\) itself whose commutator subgroup is
\(A_3\). Therefore \(\varphi(A_7)=1\), and each \(B_a\) is invariant under
\(A_7\).

It remains to show that the real six-dimensional representation (17) is
irreducible under \(A_7\). The action of \(A_7\) on ordered pairs of distinct
outcomes is transitive: after mapping one ordered pair to another, the parity
can be corrected by swapping two of the five unused outcomes. Hence any
endomorphism of \(\mathbb R^7\) commuting with \(A_7\) has one common
diagonal entry and one common off-diagonal entry, so it is
\(\alpha I+\beta\mathbf1\mathbf1^{\mathsf T}\).

To transfer this commutant calculation to \(V\), let
\(T\in\operatorname{End}_{A_7}(V)\). Use the invariant orthogonal
decomposition \(\mathbb R^7=\mathbb R\mathbf1\oplus V\) and extend \(T\)
by zero on \(\mathbb R\mathbf1\):

\[
\widetilde T(c\mathbf1+v)=T(v).
\]

The extension commutes with \(A_7\), so
\(\widetilde T=\alpha I+\beta\mathbf1\mathbf1^{\mathsf T}\). Its
vanishing on \(\mathbf1\) gives \(\alpha+7\beta=0\), while restriction to
\(V\) gives \(T=\alpha I_V\). Thus the commutant of \(V\) is scalar. If
\(V\) had a nonzero proper invariant subspace, its orthogonal complement
would also be invariant and the orthogonal projection onto it would be a
nonscalar \(A_7\)-equivariant endomorphism of \(V\), a contradiction. Thus
\(V\) is irreducible, while every \(B_a\) in (18) is nonzero and proper. The
assumed natural decomposition cannot exist.

The conclusion is exactly scoped: an unlabeled seven-outcome law and its
Fisher metric cannot naturally manufacture three two-dimensional node blocks.
A declared outcome typing, a subgroup that preserves a partition, a selected
factorization, or other symmetry-breaking structure can supply blocks, but
then the blocks come from that added structure. This is not a no-go theorem
for typed agents, and it does not identify any declared block with autonomous
agency.

## 7. Promoted parity direction: full rank versus retained rank

On \(\Omega=\{0,1\}^6\), define on
\((0,1)^6\times(-1,1)\)

\[
Q_{\theta,\kappa}(x)
=P_\theta(x)+\kappa\chi(x)D(\theta),
\quad
P_\theta(x)=\prod_i\theta_i^{x_i}(1-\theta_i)^{1-x_i},
\quad
D(\theta)=\prod_i\theta_i(1-\theta_i).
\tag{20}
\]

For the bitwise complement \(\bar x\),

\[
P_\theta(x)P_\theta(\bar x)=D(\theta),
\qquad
Q_{\theta,\kappa}(x)
=P_\theta(x)\left[1+\kappa\chi(x)P_\theta(\bar x)\right]>0. \tag{21}
\]

The strict inequality follows from \(0<P_\theta(\bar x)<1\) and
\(|\kappa|<1\). If \(A\) is any proper coordinate subset, then
\(A^c\ne\varnothing\) and

\[
\sum_{x_{A^c}}\chi(x)D(\theta)
=D(\theta)(-1)^{\sum_{i\in A}x_i}
 \prod_{j\notin A}\sum_{x_j=0}^1(-1)^{x_j}
=0. \tag{22}
\]

Therefore every proper marginal of \(Q_{\theta,\kappa}\) is the
corresponding product marginal; \(A=\varnothing\) also gives normalization.
These local identities establish the positivity and cancellation facts used
below without importing them from another package. Let a tangent
\((a_1,\ldots,a_6,b)\) have zero derivative under the full-joint map in
(20). Marginalizing that zero derivative to singleton \(i\) gives the
derivative of \(\operatorname{Bernoulli}(\theta_i)\), namely
\((-a_i,a_i)\). Therefore every \(a_i=0\). The full derivative then reduces
to

\[
b\,\partial_\kappa Q_{\theta,\kappa}(x)
=b\,\chi(x)D(\theta).
\tag{23}
\]

Because \(D(\theta)>0\) on the open cube, (23) vanishes at every atom only
when \(b=0\). Thus the promoted full-joint map is an immersion of rank seven
everywhere on its domain. Its pullback of the positive categorical Fisher
metric is positive definite.

By contrast, the singleton retained-law map is

\[
m(\theta,\kappa)=\theta,
\qquad dm=(I_6\;0),
\tag{24}
\]

so it has rank six and
\(\ker dm=\operatorname{span}\{\partial_\kappa\}\). The exact witness checks
the corresponding \(64\times7\) and \(6\times7\) derivative matrices at
\(\theta_i=1/2,\kappa=1/2\), but the preceding marginal argument proves the
rank statement on the whole positive domain. Therefore \(\kappa\) is an
identifiable full-joint interaction direction and simultaneously a null
direction for singleton retention. Whether it is retained or quotiented is a
choice of retained-law map; neither rank count turns it into an agent.

## 8. Dependency and interpretation boundary

The radical theorem reconstructs and sharpens the local quotient interface in
`Theory/05c_pullback_geometry.tex`. Presentation isometry consumes the
August 13 requirement of parameterwise retained-family equivalence, not merely
one-point law equality. The parity rank proof uses the normalized positive
family and proper-marginal identity established locally in Section 7; the
August 14 collective-lift package is a corroborating cross-reference. The
executable fraction checks corroborate finite ranks but do not
replace the derivations above.

The strongest justified interpretation is an identifiable retained Fisher
quotient with optional, declared, basic, natural, and, when energy additivity
is claimed, orthogonal block structure. Fisher geometry alone supplies none of
the node typing, symmetry breaking, intervention structure, autonomous-agency
criterion, continuum limit, physical metric, or dimensional-unit bridge.
