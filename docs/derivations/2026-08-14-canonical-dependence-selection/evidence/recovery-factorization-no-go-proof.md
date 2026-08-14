<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-8112f0083a554a4df3b5de3875174d0b0cbfeee36a7bc2ea20e78c8cf9da6b39","schema_version":"rigorous-theory-search/v1","target_digest":"8112f0083a554a4df3b5de3875174d0b0cbfeee36a7bc2ea20e78c8cf9da6b39"} -->
# Three independently typed recovery-factorization no-go theorems

## 1. Scope and factorization predicates

This artifact dispositions three distinct predicates from the frozen contract. They are not consequences of one another.

1. `RECOVERY-FULL-VFE-NOGO` concerns a scalar extended-real functional of two full joint laws and evidence.
2. `RECOVERY-FULL-FISHER-NOGO` concerns a covariant tensor assigned to an entire positive \(C^1\) statistical family on a common parameter base.
3. `RECOVERY-TYPED-INTERVENTION-NOGO` concerns objects and isomorphisms in a typed causal/intervention category.

In each case the proposed factorization would pass through singleton marginalization \(m_X\). Each proof supplies two compatible enrichments with the same proposed input but different required outputs. The selector nonexistence proof is not a premise.

## 2. Full-joint VFE does not factor through marginal laws

Let \(X_1=X_2=\{0,1\}\), let \(u=(1/2,1/2)\), and order the four joint atoms as \(00,01,10,11\). Define

\[
P=Q_0=(1/4,1/4,1/4,1/4),
\qquad
Q_{1/2}=(3/8,1/8,1/8,3/8).\tag{1}
\]

Both recognition laws and the positive posterior \(P\) have marginal datum \((u,u)\). For any fixed evidence \(z>0\),

\[
-\log z+D_{\rm KL}(Q_0\|P)=-\log z,\tag{2}
\]

whereas

\[
\begin{aligned}
-\log z+D_{\rm KL}(Q_{1/2}\|P)
&=-\log z
+2\frac38\log\frac{3/8}{1/4}
+2\frac18\log\frac{1/8}{1/4}\\
&=-\log z+\frac34\log\frac32+\frac14\log\frac12
>-\log z .
\end{aligned}\tag{3}
\]

The strict inequality is the finite KL zero criterion: \(P\) is positive and \(Q_{1/2}\ne P\), so \(D_{\rm KL}(Q_{1/2}\|P)>0\). It is not inferred from a floating-point evaluation.

**Theorem 2.1 (claim `RECOVERY-FULL-VFE-NOGO`).** There is no function

\[
V_X:M(X)\times M(X)\times(0,\infty)\longrightarrow(-\infty,\infty]
\]

such that

\[
V_X(m_XQ,m_XP,z)=-\log z+D_{\rm KL}(Q\|P)\tag{4}
\]

for every compatible recognition law \(Q\), positive posterior \(P\), and \(z>0\).

**Proof.** The triples \((Q_0,P,z)\) and \((Q_{1/2},P,z)\) give the same input \(((u,u),(u,u),z)\) to \(V_X\). Equations (2)--(3) require unequal outputs. A function cannot satisfy both requirements. \(\square\)

**Conditional replacement.** Once the full laws \((Q,P)\) and evidence convention are supplied, (4)'s right side is well-defined. If a retained joint posterior \(\pi_R\) and evidence \(z\) are supplied, the collapsed retained functional \(-\log z+D_{\rm KL}(q_R\|\pi_R)\) factors through those retained *joint* data. Under a declared auxiliary posterior reference, conditional minimization of the full VFE returns that collapsed value. None of these statements makes the full-joint VFE a function of singleton marginals alone.

The witness depends only on the frozen VFE signature, finite KL with its support convention, and the explicitly normalized laws (1). It has no dependency on the August 13 or August 14 packages.

## 3. Full-joint Fisher does not factor through a marginal family

Let \(\Omega=\{0,1\}^6\), \(\Theta=(0,1)^6\),

\[
P_\theta(x)=\prod_{i=1}^6\theta_i^{x_i}(1-\theta_i)^{1-x_i},
\quad
D(\theta)=\prod_{i=1}^6\theta_i(1-\theta_i),
\quad
\chi(x)=(-1)^{\sum_i x_i},
\]

and, for fixed \(|\kappa|<1\),

\[
Q^{(\kappa)}_\theta(x)=P_\theta(x)+\kappa\chi(x)D(\theta).\tag{5}
\]

Write \(\bar x=(1-x_1,\ldots,1-x_6)\). Atomwise,

\[
P_\theta(x)P_\theta(\bar x)
=\prod_i\theta_i(1-\theta_i)=D(\theta),
\]

so

\[
Q^{(\kappa)}_\theta(x)
=P_\theta(x)\left[1+\kappa\chi(x)P_\theta(\bar x)\right]>0. \tag{5a}
\]

Indeed, \(0<P_\theta(\bar x)<1\) and \(|\kappa|<1\), so the bracket is
strictly larger than \(1-|\kappa|P_\theta(\bar x)>0\).
For any proper coordinate subset \(A\), its complement is nonempty and the
parity correction cancels:

\[
\sum_{x_{A^c}}\chi(x)D(\theta)
=D(\theta)(-1)^{\sum_{i\in A}x_i}
  \prod_{j\notin A}\sum_{x_j=0}^1(-1)^{x_j}
=0. \tag{5b}
\]

Thus every proper marginal is the corresponding product marginal. Taking
\(A=\varnothing\) also proves normalization. These calculations make
positivity, normalization, and familywise singleton-marginal equality local
to this proof. The contained certified source
`../../2026-08-14-collective-joint-lift-fisher/evidence/collective-lift-fisher-proof.md`,
Sections 1--3 and 7, is a corroborating cross-reference rather than a missing
premise.

At \(\theta_i=1/2\), put \(c=\kappa/64\) and let \(s_i(x_i)=2\) for \(x_i=1\), \(-2\) for \(x_i=0\). Since \(\partial_iD=0\) at the center,

\[
Q^{(\kappa)}_\theta(x)=\frac{1+c\chi(x)}{64},
\qquad
\partial_iQ^{(\kappa)}_\theta(x)=\frac{s_i(x_i)}{64}.\tag{6}
\]

The categorical pullback Fisher tensor is therefore

\[
G^{(\kappa)}_{ij}
=\sum_x\frac{\partial_iQ^{(\kappa)}(x)\partial_jQ^{(\kappa)}(x)}
{Q^{(\kappa)}(x)}
=\frac1{64}\sum_x\frac{s_i(x_i)s_j(x_j)}{1+c\chi(x)}.\tag{7}
\]

For \(i\ne j\), the four unused bits give equal cancellation in each parity class, so (7) is zero. For \(i=j\), \(s_i^2=4\) and each parity class has 32 states, giving

\[
G^{(\kappa)}=\frac4{1-(\kappa/64)^2}I_6.\tag{8}
\]

Thus the two positive \(C^1\) families \(Q^{(0)}\) and \(Q^{(1/2)}\) have the same singleton-marginal map \(\theta\mapsto(\operatorname{Ber}(\theta_i))_i\), but at the common center

\[
G^{(0)}=4I_6,
\qquad
G^{(1/2)}=\frac{65536}{16383}I_6\ne4I_6.\tag{9}
\]

**Theorem 3.1 (claim `RECOVERY-FULL-FISHER-NOGO`).** Pulled-back full-joint Fisher information on positive \(C^1\) families does not factor through the complete singleton-marginal family map.

**Proof.** A factorization would assign the same tensor to any two families with the same marginal map on the same base. The families in (5) with \(\kappa=0\) and \(\kappa=1/2\) meet those hypotheses, while (9) gives unequal tensors. \(\square\)

**Conditional replacement.** The Fisher tensor of the supplied retained *joint* family factors through that parameterized family. The full-joint tensor is also defined after a positive \(C^1\) full-joint lift is declared. Equality at one law value is insufficient: the derivatives of the family are part of the Fisher datum. A marginal-only reconstruction would therefore need an additional parameterized lift rule, not merely a selected law at one parameter.

Strict positivity and familywise marginal equality are load-bearing. At a boundary atom the categorical score can be singular, so (7) need not be a finite tensor. Conversely, two families that agree only at one parameter can have different marginal derivatives; for example, a constant fair Bernoulli family and \(\operatorname{Ber}(1/2+t)\) agree at \(t=0\) but have Fisher values zero and four there. Neither control weakens the witness, which is positive and agrees as a marginal map on all of \(\Theta\).

## 4. Typed intervention structure does not factor through observational marginals

Let \(R=O=E=N=\{0,1\}\), let \(E_D=\{*\}\), and define

\[
B_t(x)=t^x(1-t)^{1-x},\qquad
\delta(a,b)=a+b-2ab,
\]

on \(\Theta=(0,1)^3\). Consider the direct, latent, and null-extended presentations

\[
P^D_\theta(r,*,o)=\frac12B_{\delta(a,b)}(o\oplus r),\tag{10}
\]

\[
P^{L0}_\theta(r,e,o)=\frac12B_a(e\oplus r)B_b(o\oplus e),\tag{11}
\]

\[
P^{L+}_\theta(r,e,n,o)=\frac12B_a(e\oplus r)B_b(o\oplus e)B_\eta(n).\tag{12}
\]

The contained certified source
`../../2026-08-13-finite-presentation-descent-joint-fisher/evidence/bsc-presentation-proof.md`, equations (1) and (7), proves the observational and interventional statements reconstructed next. Summing over \(n\) contributes one. Summing over \(e\), the mismatch probability between \(R\) and \(O\) is

\[
a(1-b)+(1-a)b=\delta(a,b),
\]

so all three retained \((R,O)\) laws are the same, and hence all their singleton marginal data are the same. Under the typed intervention that replaces the selected \(E\)-kernel while leaving the downstream kernel fixed,

\[
P^{L0}_\theta(O=o\mid\operatorname{do}(E=e))
=P^{L+}_\theta(O=o\mid\operatorname{do}(E=e))
=B_b(o\oplus e).\tag{13}
\]

For \(b\ne1/2\), \(\operatorname{do}(E=0)\) and \(\operatorname{do}(E=1)\) give different output laws. The direct presentation has only a singleton auxiliary coordinate and therefore no pair of typed binary \(E\)-interventions corresponding to (13). The null-extended presentation additionally has a typed binary \(N\)-node absent from both other presentations. Conditional on a category that admits these presentations and makes node type and intervention targets invariants of type-preserving isomorphism, the three enriched structures are pairwise nonisomorphic even though their retained observational law agrees.

**Unconditional disposition (claim
`RECOVERY-TYPED-INTERVENTION-NOGO`).** The frozen predicate quantifies
inside a declared typed causal/intervention category, but this run does not
supply a complete definition of that category or an internal proof that
(10)--(12) are admitted pairwise nonisomorphic objects in it. Observational
law equality alone cannot discharge those obligations. The unconditional
predicate is therefore **INCONCLUSIVE** in this package; neither the displayed
presentations nor the abstract argument below are promoted into an
unconditional no-go.

**Theorem 4.1 (claim
`RECOVERY-TYPED-INTERVENTION-CONDITIONAL-NOGO`).** Let \(U:\mathcal E\to\mathcal B\) be the declared forgetful functor from enriched typed intervention presentations to marginal observational data. Conditional on the August 13 direct, latent, and null-extended witnesses being objects of \(\mathcal E\) that have one common \(U\)-image and are nonisomorphic under the declared type-preserving intervention isomorphisms, no reconstruction \(R:\mathcal B\to\mathcal E\) can recover every compatible enrichment by a two-sided law

\[
R\,U(E)\cong E\qquad\text{for every compatible }E\in\mathcal E.\tag{14}
\]

**Proof.** If (14) held and \(U(E_1)=U(E_2)=b\), then \(E_1\cong R(b)\cong E_2\). The conditional August 13 witnesses supply nonisomorphic \(E_1,E_2\) over one \(b\), a contradiction. This refutes universal fiber uniqueness and faithful two-sided recovery. It does not refute a mere right-inverse section satisfying \(U R\cong\operatorname{id}_{\mathcal B}\), which may choose one conventional representative from each fiber without recovering the other representatives. \(\square\)

**Conditional replacement.** A mere section \(R\) may choose one conventional enrichment per marginal datum. Faithful recovery requires the stronger two-sided condition (14), which is impossible under the conditional nonisomorphic-fiber witness. Typed interventions can instead descend after the retained datum includes them and the equivalence intertwines every admitted intervention kernel. The full typed causal category, autonomy predicate, and causal/agency interpretation remain open formalization obligations; equality of observational laws alone supplies none of them.

The retained-law equality is proved by the displayed finite sums. The conditional nonisomorphism premise additionally requires the ambient category, object admission, and type-preserving invariants stated above. Neither part depends on the parity family or on either scalar/tensor no-go.

## 5. Independent claim and dependency edges

| Claim | Witness type | Exact dependencies | Conditional replacement |
| --- | --- | --- | --- |
| `RECOVERY-FULL-VFE-NOGO` | two positive full-joint VFE inputs with equal displayed marginals and unequal KL | laws (1); finite KL strictness; frozen signature of \(V_X\) | supply full laws, or retain a complete joint posterior/evidence and collapse or conditionally minimize |
| `RECOVERY-FULL-FISHER-NOGO` | two positive \(C^1\) full-joint families with the same marginal-family map and unequal tensors | parity family (5); cancellation of proper marginals; center calculation (6)--(9); August 14 source as corroboration only | supply a parameterized full-joint lift, or compute Fisher only at the declared retained-joint scope |
| `RECOVERY-TYPED-INTERVENTION-NOGO` | frozen unconditional typed-category predicate | complete ambient category, witness admission, and internal nonisomorphism proof are absent | **INCONCLUSIVE**; formalize those inputs before assigning a closed mathematical disposition |
| `RECOVERY-TYPED-INTERVENTION-CONDITIONAL-NOGO` | nonisomorphic enriched objects in one observational fiber, conditional on the stated category hypotheses | BSC presentations (10)--(12); intervention law (13); abstract forgetful-fiber contradiction | no universal two-sided recovery under those hypotheses; a mere right-inverse may choose one representative |

No edge between the VFE, Fisher, and intervention claims is needed or valid:
they have different codomains and equality notions. The conditional
intervention theorem records the strongest proved implication; it is not a
dependency that closes the unconditional intervention predicate.

## 6. Scope

The closed results show only nonfactorization through the frozen singleton
marginal data at their stated scopes. They do not say that joint VFE, joint
Fisher, or interventions are undefinable. The unconditional intervention
predicate remains inconclusive; only the explicitly conditional implication
is proved, and it does not forbid a conventional right-inverse section.
Formal definitions of autonomous agency, the full causal category, and its
intervention isomorphisms remain open. The results also do not recover a
continuum ontology or turn an information tensor into physical geometry.
