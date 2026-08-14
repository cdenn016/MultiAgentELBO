<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-b8102c1f5917a6cbc9a69df8b10c1470d18d5146f56093a253b1a8644465bccb","schema_version":"rigorous-theory-search/v1","target_digest":"b8102c1f5917a6cbc9a69df8b10c1470d18d5146f56093a253b1a8644465bccb"} -->
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

The contained certified source
`../../2026-08-14-collective-joint-lift-fisher/evidence/collective-lift-fisher-proof.md`, Sections 1--3 and 7, proves positivity, normalization, equality of all proper marginals, and the center formula used below. For completeness, the load-bearing center calculation is reconstructed here.

Summing the parity term over any omitted bit cancels it, so every singleton marginal of (5) is \(\operatorname{Ber}(\theta_i)\), independently of \(\kappa\). At \(\theta_i=1/2\), put \(c=\kappa/64\) and let \(s_i(x_i)=2\) for \(x_i=1\), \(-2\) for \(x_i=0\). Since \(\partial_iD=0\) at the center,

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

For \(b\ne1/2\), \(\operatorname{do}(E=0)\) and \(\operatorname{do}(E=1)\) give different output laws. The direct presentation has only a singleton auxiliary coordinate and therefore no pair of typed binary \(E\)-interventions corresponding to (13). The null-extended presentation additionally has a typed binary \(N\)-node absent from both other presentations. Node type and admitted intervention targets are invariants of the declared type-preserving intervention isomorphism. Thus the three enriched structures are pairwise nonisomorphic even though their retained observational law agrees.

**Theorem 4.1 (claim `RECOVERY-TYPED-INTERVENTION-NOGO`).** The forgetful map from these compatible typed causal/intervention presentations to their marginal observational datum has a fiber containing nonisomorphic objects. Consequently, no marginal-to-enrichment reconstruction can be a section of that forgetful map up to type-preserving intervention isomorphism for every compatible enrichment.

**Proof.** If such a reconstruction existed, every two objects over the same marginal datum would be isomorphic to the reconstructed object and hence to each other. Equations (10)--(13) give objects over one datum that are not type-preservingly intervention-isomorphic. Contradiction. \(\square\)

**Conditional replacement.** Typed interventions descend after they are included in the retained datum and the equivalence requires intertwining every admitted intervention kernel. Alternatively, one may choose a conventional enrichment or postulate an intervention/agency structure. Equality of observational laws alone supplies neither choice.

The retained-law equality and nonisomorphism depend exactly on the August 13 BSC construction cited above. They do not depend on the parity family or on either scalar/tensor no-go.

## 5. Independent claim and dependency edges

| Claim | Witness type | Exact dependencies | Conditional replacement |
| --- | --- | --- | --- |
| `RECOVERY-FULL-VFE-NOGO` | two positive full-joint VFE inputs with equal displayed marginals and unequal KL | laws (1); finite KL strictness; frozen signature of \(V_X\) | supply full laws, or retain a complete joint posterior/evidence and collapse or conditionally minimize |
| `RECOVERY-FULL-FISHER-NOGO` | two positive \(C^1\) full-joint families with the same marginal-family map and unequal tensors | parity family (5); cancellation of proper marginals; center calculation (6)--(9); certified August 14 source | supply a parameterized full-joint lift, or compute Fisher only at the declared retained-joint scope |
| `RECOVERY-TYPED-INTERVENTION-NOGO` | nonisomorphic enriched objects in one observational fiber | BSC presentations (10)--(12); intervention law (13); certified August 13 source; declared type-preserving isomorphism | retain the intervention algebra/kernels, or declare an enrichment convention/postulate |

No edge between these three claims is needed or valid: scalar VFE, statistical-family Fisher, and typed intervention structure have different codomains and different equality notions. Each proof remains valid if the other two sections are erased.

## 6. Scope

The results show only nonfactorization through the frozen singleton marginal data. They do not say that joint VFE, joint Fisher, or interventions are undefinable; each becomes well-defined once its missing typed input is supplied. They also do not identify nodes with autonomous agents, recover a continuum ontology, or turn an information tensor into physical geometry.
