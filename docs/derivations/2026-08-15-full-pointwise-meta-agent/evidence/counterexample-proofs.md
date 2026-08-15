<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87","schema_version":"rigorous-theory-search/v1","target_digest":"15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87"} -->
# Finite non-Gaussian witness and counterexample proofs

All spaces in this artifact are finite and categorical. No Gaussian family or approximation is used. The structural datum (X) is fixed and remains outside every random channel. The displayed arguments are the direct mathematical evidence; `finite_nongaussian_witness.py` only corroborates their finite arithmetic.

## 1. Exact lossy common-channel witness

Let

\[
\mathsf M=\mathsf B=\mathsf E=\{0,1\},\qquad
\mathsf O=\{1\},\qquad
\boldsymbol\Xi_A=\{\ast\},\qquad
\mathsf H_A=\{\ast\}.
\]

Put (\mathbb P(M=m\mid X)=1/2). For (m\in\{0,1\}), declare the normalized evaluated kernel on (\mathsf B\times\mathsf O\times\mathsf H_A) by

\[
K_m(B=1,O=1,H_A=\ast)=\frac14+\frac m2,
\qquad
K_m(B=0,O=1,H_A=\ast)=\frac34-\frac m2.
\tag{1.1}
\]

Each row has nonnegative entries summing to one. Add an independent fair fine bit (E), so

\[
\mathbb P_I(O=1,M=m,B=b,E=e\mid X)
=\frac12 K_m(b)\frac12.
\tag{1.2}
\]

The sole observation has (p_X(1)=1). Hence the selected fine posterior is

\[
\boldsymbol\Pi_{I,1,X}(m,b,e)=\frac14K_m(b),
\tag{1.3}
\]

and its ((M,B)) marginal, in the order ((0,0),(0,1),(1,0),(1,1)), is

\[
\boldsymbol\Pi_{I,1,X}^{MB}
=\left(\frac38,\frac18,\frac18,\frac38\right).
\tag{1.4}
\]

Define the correlated recognition law by preserving (1.4) and setting (E=B):

\[
\mathbb Q_{I,1,X}(m,b,e)
=\frac12K_m(b)\mathbf 1_{\{e=b\}}.
\tag{1.5}
\]

Thus its positive atoms are

\[
\mathbb Q_{I,1,X}(0,0,0)=\frac38,
\quad
\mathbb Q_{I,1,X}(0,1,1)=\frac18,
\quad
\mathbb Q_{I,1,X}(1,0,0)=\frac18,
\quad
\mathbb Q_{I,1,X}(1,1,1)=\frac38.
\tag{1.6}
\]

All atoms of the fine posterior are positive, so (\mathbb Q_{I,1,X}\ll\boldsymbol\Pi_{I,1,X}). Let the deterministic, recognition-independent common channel be

\[
C_A(m,b,e)=z=(b,m,\ast,\ast).
\tag{1.7}
\]

It acts only on random fine variables and retains ((B,M)); fixed structural (X) is not emitted. Equations (1.4)--(1.7) give

\[
\mathbb Q_{A,1,X}(m,b)
=\boldsymbol\Pi_{A,1,X}(m,b)
=\frac12K_m(b).
\tag{1.8}
\]

The parent recognition model marginal (q_A^m) is fair because (\sum_bK_m(b)=1), and the parent recognition belief marginal is fair because

\[
q_A^b(B=1)
=\frac12\left(\frac14+\frac34\right)=\frac12.
\]

Thus (q_A^m=q_A^b=\operatorname{Bernoulli}(1/2)). Separately, the parent generative latent marginal (\mathbb P_A^Z(\cdot\mid X)) has the same ((M,B)) table in this singleton-observation example, so the derived prior marginals (p_A^m,p_A^b) are also fair; this numerical equality does not identify prior and recognition types in general.

Conditioning the pushed generative joint on (M=m) and the singleton interface yields exactly

\[
\mathbb P_A(dB,do,dh\mid M=m,\Xi_A=\ast,X)
=K_m(dB,do,dh),
\tag{1.9}
\]

so the predeclared evaluator (\operatorname{ev}_A(m)=K_m) is compatible on both positive-mass model points under the generative (M)-marginal (\mathbb P_A^M(m\mid X)=1/2).

On every recognition atom (e=b), the likelihood ratio in the fine KL is exactly

\[
\frac{\mathbb Q_{I,1,X}(m,b,b)}
{\boldsymbol\Pi_{I,1,X}(m,b,b)}=2.
\]

Consequently,

\[
\operatorname{KL}(\mathbb Q_{I,1,X}\Vert\boldsymbol\Pi_{I,1,X})
=\sum_{m,b}\mathbb Q_{I,1,X}(m,b,b)\log2=\log2.
\tag{1.10}
\]

The reverse divergence is (+\infty), because (\boldsymbol\Pi_{I,1,X}) gives positive mass to every atom with (e\ne b), where (\mathbb Q_{I,1,X}) gives zero. It is not interchangeable with (1.10).

Equation (1.8) gives

\[
\operatorname{KL}(\mathbb Q_{A,1,X}\Vert\boldsymbol\Pi_{A,1,X})=0.
\tag{1.11}
\]

Conditionally on each retained ((m,b)), recognition has (E=b) surely while the posterior has (E\sim\operatorname{Bernoulli}(1/2)). Every forward conditional KL is therefore (\log2); averaging against the normalized parent recognition law gives

\[
\Delta_A(1,X)=\log2.
\tag{1.12}
\]

Because the unchanged evidence term is (-\log p_X(1)=0), equations (1.10)--(1.12) also give the exact VFE identity (\mathcal F_I=\mathcal F_A+\Delta_A).

## 2. CE-1: paired fair marginals do not determine a joint law

On (\{0,1\}^2), define the correlated and anticorrelated laws

\[
R(0,0)=R(1,1)=\frac12,
\qquad
S(0,1)=S(1,0)=\frac12,
\]

with every unlisted atom assigned zero. Both coordinate marginals of both laws are (\operatorname{Bernoulli}(1/2)), but (R\ne S). Their supports are disjoint. In each KL direction, a source atom of mass (1/2) has zero target mass, so

\[
\operatorname{KL}(R\Vert S)=\operatorname{KL}(S\Vert R)=+\infty.
\]

This finite witness proves `NEG-MARGINAL-DETERMINATION`: even both complete coordinate marginals do not reconstruct the full dependence law.

## 3. CE-2: split channels can increase zero fine KL to infinite coarse KL

Let the fine state be (U\in\{0,1\}) and set (Q=\Pi=\operatorname{Bernoulli}(1/2)), so (\operatorname{KL}(Q\Vert\Pi)=0). Push recognition through the identity channel (C_Q(u)=u), but push the posterior/generative law through the constant-zero channel (C_\Pi(u)=0). Then

\[
QC_Q=\operatorname{Bernoulli}(1/2),
\qquad
\Pi C_\Pi=\delta_0.
\]

The first coarse law gives mass (1/2) to (1), where the second gives zero, and therefore

\[
\operatorname{KL}(QC_Q\Vert\Pi C_\Pi)=+\infty.
\]

The reverse coarse KL is only (\log2); it is not the VFE orientation. With singleton evidence, the forward fine VFE is zero and the split-channel forward coarse VFE is infinite. This proves `NEG-SPLIT-CHANNEL-VFE`. It does not attack the common-channel theorem because (C_Q\ne C_\Pi); it proves that the common-channel hypothesis cannot be omitted.

## 4. CE-3: a normalized model marginal does not force evaluator compatibility

Reuse the parent generative law from Section 1, whose generative model marginal (\mathbb P_A^M(\cdot\mid X)) assigns mass (1/2) to each (m). Keep the same normalized family (K_0,K_1), but predeclare the swapped evaluator

\[
\operatorname{ev}'_A(m)=K_{1-m}.
\]

For both (m=0) and (m=1),

\[
K_m(B=1)=\frac14+\frac m2
\ne
\frac14+\frac{1-m}{2}=K_{1-m}(B=1).
\]

Thus (\operatorname{ev}'_A) disagrees with the actual conditional generative kernel at every model point, and each such point has positive generative parent mass (1/2). The generative model marginal remains normalized and fair. This proves `NEG-MODEL-MARGINAL-EVALUATION`; the missing repair is precisely the almost-sure compatibility hypothesis from Task 3. The recognition marginal (q_A^m) is not used to establish this mismatch seam.

## 5. CE-4: holonomy boundary witnesses

### 5.1 Trivial holonomy does not imply agreement

Take a two-node tree with identity transport on its sole edge. A tree has no nontrivial based loops, so its holonomy group is trivial. Assign (P=\operatorname{Bernoulli}(1/4)) at one node and (Q=\operatorname{Bernoulli}(3/4)) at the other. Identity transport leaves both laws unchanged, and they remain unequal because their masses at (1) differ. More sharply,

\[
\operatorname{KL}(P\Vert Q)
=\operatorname{KL}(Q\Vert P)
=\frac12\log3>0.
\]

This proves `NEG-TRIVIAL-HOLONOMY-AGREEMENT` without a Gaussian example.

### 5.2 Nontrivial holonomy can stabilize a law

Let the nonidentity bit flip be (g(u)=1-u). For the fair law (F=\operatorname{Bernoulli}(1/2)), one has (g_\#F=F). Hence triviality is not necessary for state-specific stabilization.

### 5.3 Invariant marginals do not imply invariant dependence

Let (R) be the correlated law and (S) the anticorrelated law from Section 2. Act on the joint space by

\[
T(b,m)=(1-b,m).
\]

The (B) marginal is fair and therefore invariant under the bit flip; the (M) marginal is fair and unchanged by the identity action. Nevertheless (T_\#R=S\ne R). Thus both coordinate marginals are invariant under their declared actions while the correlated full law is not. This proves `NEG-MARGINAL-HOLONOMY-JOINT`.

## 6. Exactness and scope

The normalization, marginal, support, conditional, and likelihood-ratio calculations above use only finite sums of rational numbers. The primary logarithmic results are the symbolic values (0), (\log2), (\tfrac12\log3), and (+\infty). Decimal values in the contained JSON are readability-only corroboration. These witnesses prove exactly the five existential negative claims recorded in the package ledger. They do not change the mixed target state, constitute Task-5 adversarial reconstruction, or release the package.
