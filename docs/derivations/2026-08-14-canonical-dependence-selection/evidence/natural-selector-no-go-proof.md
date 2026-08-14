<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-b8102c1f5917a6cbc9a69df8b10c1470d18d5146f56093a253b1a8644465bccb","schema_version":"rigorous-theory-search/v1","target_digest":"b8102c1f5917a6cbc9a69df8b10c1470d18d5146f56093a253b1a8644465bccb"} -->
# Local-Markov selector classification and correlated-refinement no-go

## 1. Typed finite categories

For a finite nonempty typed list (X=(X_1,\ldots,X_n)), put

\[
J(X)=\Delta\!\left(\prod_iX_i\right),\qquad
M(X)=\prod_i\Delta(X_i),
\]

and let (m_X:J(X)\to M(X)) extract the singleton marginals. A fixed-arity local morphism (K:X\to Y) is a tuple of finite Markov kernels (K_i:X_i\rightsquigarrow Y_i). Its two actions are

\[
J(K)=\left(\bigotimes_iK_i\right)_\#,
\qquad
M(K)=\prod_i(K_i)_\# .
\tag{1}
\]

The tensor in (1) declares independent channel randomness. Finite summation proves

\[
m_YJ(K)=M(K)m_X.\tag{2}
\]

An arity-changing finite Markov kernel (K:\prod_iX_i\rightsquigarrow\prod_jY_j) is *marginal-compatible* when a map \(\bar K:M(X)\to M(Y)\) satisfies

\[
m_YK_\#=\bar K m_X.\tag{3}
\]

The product coupling \(\otimes_i\mu_i\) makes \(m_X\) surjective, so (3), when it holds, determines \(\bar K\) uniquely. All domains above are nonempty, every pushforward is normalized, and no positivity or continuity hypothesis is used in Sections 2--5.

## 2. Product uniqueness under all coordinatewise finite Markov kernels

**Theorem 2.1 (local-Markov uniqueness).** Suppose a family of law-valued sections \(S_X:M(X)\to J(X)\) satisfies \(m_XS_X=\operatorname{id}\) and is natural under every coordinatewise finite Markov kernel:

\[
J(K)S_X=S_YM(K).\tag{4}
\]

Then, for every finite nonempty typed list and every marginal tuple,

\[
S_X(\mu_1,\ldots,\mu_n)=\bigotimes_i\mu_i.\tag{5}
\]

Conversely, (5) is a section satisfying (4) for precisely this local morphism class.

**Proof.** Let \(\mathbf1_X=(\{*\},\ldots,\{*\})\) have the same arity and typing as \(X\). Both \(J(\mathbf1_X)\) and \(M(\mathbf1_X)\) are singletons, so the section condition forces \(S_{\mathbf1_X}=\delta_{(*,\ldots,*)}\). Given \(\mu=(\mu_i)_i\in M(X)\), define the preparation kernel \(P_i:\{*\}\rightsquigarrow X_i\) by \(P_i(x_i\mid *)=\mu_i(x_i)\). Its independently tensored joint action prepares \(\otimes_i\mu_i\), whereas its marginal action prepares \(\mu\). Naturality (4) therefore gives

\[
S_X(\mu)=J(P)S_{\mathbf1_X}=\bigotimes_i\mu_i.
\]

This proves uniqueness without an entropy, regularity, or positivity assumption. Conversely, independent finite summation gives

\[
J(K)\!\left(\bigotimes_i\mu_i\right)
=\bigotimes_i(K_i)_\#\mu_i
=S_Y(M(K)\mu),
\]

and marginalization of a product returns its factors. \(\square\)

The word *natural* in Theorem 2.1 always means naturality under the coordinatewise finite Markov kernels with independently tensored randomness in (1). The conclusion does not assert that physical independence follows without that declared monoidal structure.

## 3. Maximal product-preserving presentation category

Call a marginal-compatible kernel \(K:X\to Y\) *product-preserving* when, for every \(\mu=(\mu_i)_i\in M(X)\),

\[
K_\#\!\left(\bigotimes_i\mu_i\right)
=\bigotimes_j\left[m_YK_\#\!\left(\bigotimes_i\mu_i\right)\right]_j
=\bigotimes_j(\bar K\mu)_j .
\tag{6}
\]

**Theorem 3.1 (maximal-category iff).** Let \(\mathcal C\) be a wide category on the finite typed lists whose morphisms are marginal-compatible kernels and which contains every fixed-arity local kernel. The category \(\mathcal C\) admits a section family natural under every morphism of \(\mathcal C\) if and only if every morphism of \(\mathcal C\) is product-preserving in the sense of (6). When such a natural family exists for this morphism class, it is unique and is the product family (5). Consequently, the collection of all product-preserving marginal-compatible kernels is the maximal wide category containing the local kernels on which a natural marginal section exists.

**Proof.** If a \(\mathcal C\)-natural section exists, its restriction to local kernels is the product family by Theorem 2.1. For any \(K\in\mathcal C(X,Y)\) and any \(\mu\in M(X)\), naturality and marginal compatibility give

\[
K_\#\!\left(\bigotimes_i\mu_i\right)
=K_\#S_X(\mu)
=S_Y(\bar K\mu)
=\bigotimes_j(\bar K\mu)_j,
\]

which is (6). Conversely, if every \(K\in\mathcal C\) satisfies (6), then the product section obeys

\[
K_\#S_X(\mu)=K_\#\!\left(\bigotimes_i\mu_i\right)
=\bigotimes_j(\bar K\mu)_j=S_Y(\bar K\mu),
\]

so it is \(\mathcal C\)-natural. Uniqueness again follows from the local preparation kernels. Identity kernels preserve products. If \(K\) and \(L\) preserve products, then \(LK\) does too, because \(K\) sends each product input to the product with marginals \(\bar K\mu\), and \(L\) sends that product to the product with marginals \(\bar L\bar K\mu\). Thus all such kernels form a category. The preceding necessity shows that adding any non-product-preserving marginal-compatible kernel destroys existence, which proves maximality. \(\square\)

The maximality statement is relative to the frozen finite typed objects, marginalization functor, and independently tensored local subcategory. It does not classify categories with a different marginal functor, correlated channel randomness supplied as input, or set-valued selectors.

## 4. A marginal-compatible correlated split

Let the source be one fair bit \(U=\{0,1\}\) and the target be two bits \(Y=Z=\{0,1\}\). For \(|\rho|<1\), define

\[
R_\rho(y,z\mid x)
=\mathbf1[y=x]\begin{cases}
(1+\rho)/2,&z=x,\\
(1-\rho)/2,&z\ne x.
\end{cases}\tag{7}
\]

Each row of (7) is normalized and nonnegative. For a source law \(\mu\), the \(Y\)-marginal is \(\mu\), while the \(Z\)-marginal is the output of a binary symmetric channel of crossover \((1-\rho)/2\) applied to \(\mu\). Hence \(R_\rho\) is marginal-compatible; its \(\bar R_\rho\) is exactly this pair of one-bit marginal maps.

For the fair source \(u=(1/2,1/2)\), direct pushforward gives the strictly positive output law

\[
Q_\rho(y,z)=\frac{1+\rho(-1)^{y\oplus z}}4.\tag{8}
\]

Indeed, (8) has two atoms \((1+\rho)/4\), two atoms \((1-\rho)/4\), total mass one, and both singleton marginals equal to \(u\). The kernel (7) itself has structural zeros from \(\mathbf1[y=x]\); only its output law (8) is asserted to be strictly positive.

## 5. Relabeling-robust correlated-refinement nonexistence

**Theorem 5.1 (claim `SEL-CORRELATED-REFINEMENT-NOGO`).** The section axiom together with naturality under the two admitted split refinements \(R_{1/3}\) and \(R_{1/2}\), without any local-kernel naturality assumption, contradicts a single-valued law assignment at the fair/fair marginal datum.

**Proof.** On the one-coordinate source, the section condition forces \(S_U(u)=u\). Both split marginal maps send \(u\) to \((u,u)\). Naturality under each split would therefore require

\[
S_{(Y,Z)}(u,u)=R_{1/3\,\#}u=Q_{1/3},
\qquad
S_{(Y,Z)}(u,u)=R_{1/2\,\#}u=Q_{1/2}.\tag{9}
\]

But their atom multisets are

\[
\{1/3,1/3,1/6,1/6\},\qquad
\{3/8,3/8,1/8,1/8\},\tag{10}
\]

so the laws are unequal. A relabeling of the four sample outcomes only permutes an atom multiset. Coordinate bit flips can replace \(\rho\) by \(-\rho\), but the multiset depends on \(|\rho|\); the unequal magnitudes \(1/3\) and \(1/2\) therefore remain distinct under every sample relabeling. Equation (9) is impossible for one law-valued section. \(\square\)

Together with Theorem 2.1, any single \(R_\rho\) with \(\rho\ne0\) also contradicts a section natural under all local kernels: those kernels force \(S(u,u)=Q_0=u\otimes u\), whereas split naturality forces \(S(u,u)=Q_\rho\ne Q_0\).

Theorem 5.1 refutes the frozen existential selector target by a scope-matched nonexistence proof: the target demands one family satisfying both universal morphism requirements, and the finite subdiagram (9) makes that conjunction inconsistent. It does not use any positive replacement theorem as a premise.

## 6. Faithful quasi-inverse nonexistence

**Theorem 6.1 (claim `SEL-FAITHFUL-QUASI-INVERSE-NOGO`).** For any typed list with at least two nontrivial coordinates, no marginal section \(S_X\) can also satisfy \(S_Xm_X=\operatorname{id}_{J(X)}\) on every admitted joint law.

**Proof.** On two bits, \(m(Q_0)=m(Q_{1/2})=(u,u)\), while (8) gives \(Q_0\ne Q_{1/2}\). Thus \(m\) is not injective. If both \(mS=\operatorname{id}\) and \(Sm=\operatorname{id}\) held on all joints, then equal marginals would imply

\[
Q_0=S(mQ_0)=S(mQ_{1/2})=Q_{1/2},
\]

a contradiction. The same binary fiber embeds in any list with two nontrivial coordinates by fixing all other coordinates at point masses. \(\square\)

A conditional replacement is exact: a section may select one representative per marginal fiber after extra structure is declared, but it cannot recover every member of that fiber. The product rule is the unique representative compatible with the local morphism class of Theorem 2.1; the reference-relative rule proved separately selects a representative relative to its declared reference.

## 7. Hypothesis controls and dependency map

The preparation arrows are load-bearing. If the admitted local class is reduced to typed bijections, many equivariant selectors can coexist; for example, on two unlabeled bits the family \(Q_\rho\) with a fixed nonzero \(|\rho|\) is equivariant under simultaneous relabelings but is not the product rule. Thus Theorem 2.1 does not survive deletion of the preparation kernels.

Marginal compatibility is also load-bearing for a morphism to act on \(M\). The deterministic XOR map \((x_1,x_2)\mapsto x_1\oplus x_2\) sends \(Q_0\) to a fair bit and \(Q_1\) to a deterministic bit although those sources have the same singleton marginals, so no \(\bar K\) satisfying (3) exists for XOR on the marginal-only category.

Single-valuedness is load-bearing in Theorem 5.1. The full fiber-valued assignment \(\mu\mapsto\{Q:mQ=\mu\}\) contains both outputs, but it is not a law-valued section of the frozen signature and supplies no selected VFE, Fisher family, or typed intervention structure.

The direct dependency record for this artifact is:

| Claim | Exact dependencies | Disposition here |
| --- | --- | --- |
| `SEL-PRODUCT-UNIQUENESS` | finite normalization; independently tensored local kernels; preparation arrows; section equation | proved by Theorem 2.1 |
| `SEL-MAXIMAL-PRODUCT-CATEGORY` | `SEL-PRODUCT-UNIQUENESS`; marginal compatibility (3); product-preservation definition (6) | proved by Theorem 3.1 |
| `SEL-CORRELATED-REFINEMENT-NOGO` | normalized split (7); fair-source pushforward (8); single-valued section naturality | proved by Theorem 5.1 |
| `SEL-FAITHFUL-QUASI-INVERSE-NOGO` | noninjective binary marginal fiber \(Q_0,Q_{1/2}\) | proved by Theorem 6.1 |

These are direct finite derivations under the frozen contract. Exact executable checks may corroborate (8)--(10), but no numerical assertion is used to prove a theorem here.
