<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87","schema_version":"rigorous-theory-search/v1","target_digest":"15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87"} -->
# Direct derivation of the full common-channel pointwise datum

## 1. Fixed structural data and standard-Borel probability types

Fix a nonempty finite active set (I), one point (r_*\in\mathcal U_A), and one structural datum (X). Define (X_A=\chi_A(X)). Both (X) and (X_A) are fixed conditioning data: neither is randomized, neither belongs to the fine random space, and neither is an output of the coarse channel. This theorem is pointwise in this one (X). It makes no claim that two values (X,X') with (\chi_A(X)=\chi_A(X')) induce the same parent law. Such a cross-(X) claim would require a separately measurable factorization through (X_A).

Let

\[
\mathsf O,\quad \mathsf Y_I,\quad \mathsf B_A,\quad \mathsf M_A,
\quad \boldsymbol\Xi_A,\quad \mathsf H_A
\]

be nonempty standard-Borel spaces with their Borel sigma-algebras. Put

\[
\mathsf Z_A
=\mathsf B_A\times\mathsf M_A\times\boldsymbol\Xi_A\times\mathsf H_A,
\qquad z=(b_A,m_A,\xi_A,h_A).
\]

Finite products of standard-Borel spaces are standard Borel, so every coordinate projection used below is measurable and every probability law on a displayed product admits regular conditional probabilities with respect to its displayed coordinate maps.

Fix a normalized generative law

\[
\mathbb P_I(Do,DY\mid X)\in\mathcal P(\mathsf O\times\mathsf Y_I)
\]

before any recognition law or posterior is chosen. Write (\nu_X=\mathbb P_I^O(\cdot\mid X)) for its observation marginal. Select one measurable regular-conditional kernel

\[
o\longmapsto\boldsymbol\Pi_{I,o,X}\in\mathcal P(\mathsf Y_I)
\]

such that, for measurable (E\subseteq\mathsf O) and (D\subseteq\mathsf Y_I),

\[
\mathbb P_I(E\times D\mid X)
=\int_E\boldsymbol\Pi_{I,o,X}(D)\,\nu_X(do).
\tag{1.1}
\]

The selected kernel is declared on every observation, while (1.1) determines it only (\nu_X)-almost everywhere. An admitted observation (o) is a point at which this selected version, its evidence representative, and every later slice-wise expression are declared to be used. No arbitrary conditional version is silently evaluated on an unspecified null slice.

For the pointwise VFE, additionally fix a sigma-finite observation reference measure (\lambda_X) with (\nu_X\ll\lambda_X), choose one measurable density representative

\[
p_X(o)=\frac{d\nu_X}{d\lambda_X}(o),
\]

and admit only the present (o) with (0<p_X(o)<\infty). The same representative is used at both scales. This extra declaration is what makes a pointwise evidence term meaningful when (\mathsf O) is continuous.

Fix a normalized, possibly correlated recognition law

\[
\mathbb Q_{I,o,X}\in\mathcal P(\mathsf Y_I),
\qquad
\mathbb Q_{I,o,X}\ll\boldsymbol\Pi_{I,o,X}.
\tag{1.2}
\]

If the fine agent coordinates include declared measurable maps (\rho_i^b:\mathsf Y_I\to\mathsf B_i) and (\rho_i^m:\mathsf Y_I\to\mathsf M_i), then the displayed local laws are definitions

\[
q_i^{b;o,X}=(\rho_i^b)_\#\mathbb Q_{I,o,X},
\qquad
q_i^{m;o,X}=(\rho_i^m)_\#\mathbb Q_{I,o,X}.
\tag{1.3}
\]

They are marginals of the correlated full law. Only the forward projection identities are used below; no converse or reconstruction theorem is claimed here.

## 2. The single recognition-independent channel

Fix one Markov kernel

\[
C_A:\mathsf Y_I\rightsquigarrow\mathsf Z_A
\tag{2.1}
\]

such that (Y\mapsto C_A(Y,D)) is measurable for every Borel (D\subseteq\mathsf Z_A) and (C_A(Y,\mathsf Z_A)=1) for every (Y). The kernel is fixed by the structural construction before recognition and posterior laws are supplied. It does not read (\mathbb Q_{I,o,X}), (\boldsymbol\Pi_{I,o,X}), a recognition parameter, or the realized observation. It acts only on (Y); the observation coordinate and the fixed data (X,X_A) stay outside it. Separate generative, posterior, and recognition channels are not covered by the theorem.

For bounded measurable (f:\mathsf Z_A\to\mathbb R), write

\[
(C_Af)(Y)=\int_{\mathsf Z_A}f(z)C_A(Y,dz).
\]

Kernel measurability makes (C_Af) measurable, and normalization gives (C_A1=1).

## 3. Parent generation, posterior, and recognition

Define the parent generative joint by the observation-preserving pushforward

\[
\mathbb P_A(do,dz\mid X)
=\int_{\mathsf Y_I}C_A(Y,dz)\mathbb P_I(do,dY\mid X).
\tag{3.1}
\]

Equivalently, for bounded measurable (\varphi:\mathsf O\to\mathbb R) and (f:\mathsf Z_A\to\mathbb R),

\[
\int\varphi(o)f(z)\mathbb P_A(do,dz\mid X)
=\int\varphi(o)(C_Af)(Y)\mathbb P_I(do,dY\mid X).
\tag{3.2}
\]

Taking (\varphi=f=1) proves normalization. Kernel integration and monotone-class extension prove countable additivity and measurability. Taking (f=1) shows

\[
\mathbb P_A^O(Do\mid X)=\nu_X(Do),
\tag{3.3}
\]

so the observation law and the selected density representative (p_X(o)) are unchanged.

Define, as observation-indexed kernels and not merely as isolated slices,

\[
\boldsymbol\Pi_{A,o,X}=\boldsymbol\Pi_{I,o,X}C_A,
\qquad
\mathbb Q_{A,o,X}=\mathbb Q_{I,o,X}C_A.
\tag{3.4}
\]

The first formula is a parent posterior version. Indeed, (1.1), (3.2), and Tonelli give for bounded measurable (\varphi,f)

\[
\begin{aligned}
\int\varphi(o)f(z)\mathbb P_A(do,dz\mid X)
&=\int\varphi(o)\left[\int(C_Af)(Y)\boldsymbol\Pi_{I,o,X}(dY)\right]\nu_X(do)\\
&=\int\varphi(o)\left[\int f(z)\boldsymbol\Pi_{A,o,X}(dz)\right]\nu_X(do).
\end{aligned}
\tag{3.5}
\]

Indicators followed by a monotone-class argument yield the regular-conditional identity for every measurable observation and parent event. The map (o\mapsto\boldsymbol\Pi_{A,o,X}(D)) is measurable by composition of kernels. Thus (3.4) selects a globally measurable parent version, including declared exceptional-point values inherited from the fine selected version, before the theorem specializes to the admitted (o).

The same channel preserves absolute continuity. If (\boldsymbol\Pi_{A,o,X}(D)=0), then (C_A(Y,D)=0) for (\boldsymbol\Pi_{I,o,X})-almost every (Y). Equation (1.2) gives the same statement (\mathbb Q_{I,o,X})-almost surely, hence (\mathbb Q_{A,o,X}(D)=0). Therefore

\[
\mathbb Q_{A,o,X}\ll\boldsymbol\Pi_{A,o,X}.
\tag{3.6}
\]

Equations (3.1) and (3.4), with (3.5), are the full static pointwise parent probabilistic datum. No independence between its coordinates is asserted.

## 4. Model evaluation and the compatibility seam

Let (\mathsf W_A=\mathsf B_A\times\mathsf O\times\mathsf H_A). At fixed (X_A), a parent evaluation family means a normalized jointly measurable kernel family

\[
(m_A,\xi_A,E)\longmapsto
K^{X_A}_{A,m_A}(\xi_A;E),
\qquad E\in\mathcal B(\mathsf W_A),
\tag{4.1}
\]

where ((m_A,\xi_A)\mapsto K^{X_A}_{A,m_A}(\xi_A;E)) is measurable for every (E) and (K^{X_A}_{A,m_A}(\xi_A;\mathsf W_A)=1) for every ((m_A,\xi_A)). The notation

\[
\operatorname{ev}_A:\mathsf M_A\longrightarrow
\operatorname{Kern}(\boldsymbol\Xi_A,\mathsf W_A),
\qquad m_A\longmapsto K^{X_A}_{A,m_A},
\tag{4.2}
\]

abbreviates (4.1); no sigma-algebra on an abstract kernel space is being inferred.

There are exactly two valid construction tiers.

**Induced tier.** Let (\mu_A^{M\Xi}(dm_A,d\xi_A\mid X)) be the ((M_A,\Xi_A)) marginal of (\mathbb P_A(\cdot\mid X)). Standard-Borel disintegration supplies a selected normalized measurable kernel

\[
G_A^X(m_A,\xi_A;db_A,do,dh_A)
\]

such that, for Borel (D\subseteq\mathsf M_A\times\boldsymbol\Xi_A) and (E\subseteq\mathsf W_A),

\[
\mathbb P_A\bigl((M_A,\Xi_A)\in D,(B_A,O,H_A)\in E\mid X\bigr)
=\int_DG_A^X(m_A,\xi_A;E)\mu_A^{M\Xi}(dm_A,d\xi_A\mid X).
\tag{4.3}
\]

Choosing (K^{X_A}_{A,m_A}(\xi_A;\cdot)=G_A^X(m_A,\xi_A;\cdot)) proves existence of an induced normalized jointly measurable evaluation family at this fixed (X). This existence is a conclusion of disintegration, not an evaluation-family hypothesis. It is recognition independent because it is selected from the fixed pushed generative law, not from (\mathbb Q) or (\boldsymbol\Pi). The notation (X_A) does not prove cross-(X) factorization: if several fine structural values are later compared, equality of their induced kernels whenever (\chi_A(X)=\chi_A(X')), together with measurability in (X_A), is an additional premise.

**Predeclared tier.** If (4.1) is fixed before (\mathbb P_A), standard-Borel disintegration does not force it to equal (G_A^X). One must assume the explicit compatibility

\[
G_A^X(m_A,\xi_A;\cdot)
=K^{X_A}_{A,m_A}(\xi_A;\cdot)
\quad\text{for }\mu_A^{M\Xi}(\cdot\mid X)\text{-almost every }(m_A,\xi_A).
\tag{4.4}
\]

Under either the induced choice or hypothesis (4.4), (4.3) becomes the precise version of

\[
\mathbb P_A(db_A,do,dh_A\mid \xi_A,m_A,X)
=K^{X_A}_{A,m_A}(\xi_A;db_A,do,dh_A)
\quad\mu_A^{M\Xi}\text{-almost surely}.
\tag{4.5}
\]

This is a consequence of the selected disintegration plus the declared seam, not of a model marginal. The conditional is unique only almost surely; values on a (\mu_A^{M\Xi})-null set are version choices. Evaluation need not be injective. The default object retains the presentation (m_A). Quotienting by equality of evaluated kernels does not automatically yield a standard-Borel, Hausdorff, or smooth quotient; each such property needs its own theorem.

## 5. Derived marginals and their exact scope

First distinguish the parent joint, its latent prior, and its posterior. Define

\[
\mathbb P_A^Z(D\mid X)=\mathbb P_A(\mathsf O\times D\mid X),
\tag{5.1}
\]

which integrates out the observation and is not (\boldsymbol\Pi_{A,o,X}). With coordinate projections (\operatorname{pr}_b,\operatorname{pr}_m), define

\[
\begin{aligned}
q_A^b&=(\operatorname{pr}_b)_\#\mathbb Q_{A,o,X},
&q_A^m&=(\operatorname{pr}_m)_\#\mathbb Q_{A,o,X},\\
p_A^b&=(\operatorname{pr}_b)_\#\mathbb P_A^Z(\cdot\mid X),
&p_A^m&=(\operatorname{pr}_m)_\#\mathbb P_A^Z(\cdot\mid X),\\
\boldsymbol\Pi_{A,o,X}^b&=(\operatorname{pr}_b)_\#\boldsymbol\Pi_{A,o,X},
&\boldsymbol\Pi_{A,o,X}^m&=(\operatorname{pr}_m)_\#\boldsymbol\Pi_{A,o,X}.
\end{aligned}
\tag{5.2}
\]

For every bounded measurable (u) on (\mathsf B_A), for example,

\[
\int u(b_A)q_A^b(db_A)
=\int u(\operatorname{pr}_b z)\mathbb Q_{A,o,X}(dz)
=\int C_A(u\circ\operatorname{pr}_b)(Y)\mathbb Q_{I,o,X}(dY),
\tag{5.3}
\]

and the other five projection identities follow identically. Thus all displayed parent marginals are derived from typed full laws. No converse or reconstruction theorem from these marginal identities is claimed here; the corresponding Task-4 claims remain (\texttt{CANDIDATE}).

## 6. Extended KL disintegration and finite VFE closure

At the admitted ((o,X)), form the two joint channel lifts

\[
\widehat{\mathbb Q}_{I,o,X}(dY,dz)
=\mathbb Q_{I,o,X}(dY)C_A(Y,dz),
\qquad
\widehat{\boldsymbol\Pi}_{I,o,X}(dY,dz)
=\boldsymbol\Pi_{I,o,X}(dY)C_A(Y,dz).
\tag{6.1}
\]

Their (z)-marginals are (\mathbb Q_{A,o,X}) and (\boldsymbol\Pi_{A,o,X}). By (1.2), the first lift is absolutely continuous with respect to the second. If (r=d\mathbb Q_{I,o,X}/d\boldsymbol\Pi_{I,o,X}), bounded test functions show

\[
\frac{d\widehat{\mathbb Q}_{I,o,X}}
{d\widehat{\boldsymbol\Pi}_{I,o,X}}(Y,z)=r(Y)
\quad\widehat{\boldsymbol\Pi}_{I,o,X}\text{-almost surely}.
\tag{6.2}
\]

Consequently, in the extended nonnegative reals,

\[
\operatorname{KL}(\widehat{\mathbb Q}_{I,o,X}
\Vert\widehat{\boldsymbol\Pi}_{I,o,X})
=\operatorname{KL}(\mathbb Q_{I,o,X}
\Vert\boldsymbol\Pi_{I,o,X}).
\tag{6.3}
\]

Standard-Borel disintegration gives selected conditional kernels

\[
\widehat{\mathbb Q}_{I,o,X}(dY\mid z),
\qquad
\widehat{\boldsymbol\Pi}_{I,o,X}(dY\mid z).
\]

The relative-entropy chain rule, obtained by factorizing the Radon--Nikodym derivative into its (z)-marginal density and conditional density and applying monotone truncation to the nonnegative relative-entropy integrands, gives the additive identity

\[
\begin{aligned}
\operatorname{KL}(\mathbb Q_{I,o,X}\Vert\boldsymbol\Pi_{I,o,X})
&=\operatorname{KL}(\mathbb Q_{A,o,X}\Vert\boldsymbol\Pi_{A,o,X})
+\Delta_A(o,X),\\
\Delta_A(o,X)
&=\int_{\mathsf Z_A}
\operatorname{KL}\!\left(
\widehat{\mathbb Q}_{I,o,X}(dY\mid z)
\middle\Vert
\widehat{\boldsymbol\Pi}_{I,o,X}(dY\mid z)
\right)\mathbb Q_{A,o,X}(dz)\geq0.
\end{aligned}
\tag{6.4}
\]

Equation (6.4) is an equality in ([0,+\infty]). It is not formed by subtracting an infinite coarse divergence from an infinite fine divergence.

Using the one finite evidence representative already declared, define

\[
\begin{aligned}
\mathcal F_I(o,X;\mathbb Q_{I,o,X})
&=-\log p_X(o)+
\operatorname{KL}(\mathbb Q_{I,o,X}\Vert\boldsymbol\Pi_{I,o,X}),\\
\mathcal F_A(o,X;\mathbb Q_{A,o,X})
&=-\log p_X(o)+
\operatorname{KL}(\mathbb Q_{A,o,X}\Vert\boldsymbol\Pi_{A,o,X}).
\end{aligned}
\tag{6.5}
\]

Because (-\log p_X(o)) is a fixed finite real number, (6.4) yields the extended additive identity

\[
\mathcal F_I(o,X;\mathbb Q_{I,o,X})
=\mathcal F_A(o,X;\mathbb Q_{A,o,X})+\Delta_A(o,X).
\tag{6.6}
\]

If the fine KL is finite, both terms on the right of (6.4) are finite. Only on this finite tier may one take the ordinary real-valued difference

\[
\mathcal F_I-\mathcal F_A=\Delta_A\geq0.
\tag{6.7}
\]

The equality condition is exact. A nonnegative measurable function has zero integral exactly when it is zero almost surely, and KL vanishes exactly at equality of probability measures. Hence

\[
\Delta_A(o,X)=0
\quad\Longleftrightarrow\quad
\widehat{\mathbb Q}_{I,o,X}(dY\mid z)
=\widehat{\boldsymbol\Pi}_{I,o,X}(dY\mid z)
\quad\mathbb Q_{A,o,X}\text{-almost surely}.
\tag{6.8}
\]

When the fine KL is finite, (6.8) is also equivalent to ordinary real-valued VFE equality.

There is a pairwise common-recovery formulation, but only under explicit hypotheses. Let

\[
R_{\Pi,o,X}(z,dY)
=\widehat{\boldsymbol\Pi}_{I,o,X}(dY\mid z)
\tag{6.9}
\]

be a normalized selected posterior reverse kernel. Disintegration always gives

\[
\boldsymbol\Pi_{A,o,X}R_{\Pi,o,X}=\boldsymbol\Pi_{I,o,X}.
\tag{6.10}
\]

If (6.8) holds, disintegration of the recognition lift also gives

\[
\mathbb Q_{A,o,X}R_{\Pi,o,X}=\mathbb Q_{I,o,X}.
\tag{6.11}
\]

Conversely, assume the fine KL is finite and there exists one normalized kernel (R:\mathsf Z_A\rightsquigarrow\mathsf Y_I) satisfying both recovery identities. Data processing through (C_A) and then through (R) forces equality of the finite fine and coarse KL values; (6.4) then gives (\Delta_A=0). Thus, on the finite tier,

\[
\Delta_A=0
\quad\Longleftrightarrow\quad
\text{one common normalized recovery kernel recovers both declared laws}.
\tag{6.12}
\]

This is pair-specific recovery. A single recovery kernel for an entire model family requires simultaneous recovery hypotheses for every family member. Equality (+\infty=+\infty) supplies neither (6.8) nor (6.12).

## 7. Full-law holonomy alternatives

The Task-3 proof starts from full-law covariance data rather than from marginal stabilization such as (h_\#q_A^x=q_A^x). No converse or reconstruction theorem from marginal identities is claimed here. The forward construction is cleanest for a typed holonomy groupoid.

Let an arrow (g:(o,X)\to(o',X')) have bimeasurable actions

\[
T_O^g:\mathsf O\to\mathsf O',\qquad
T_I^g:\mathsf Y_I\to\mathsf Y_I',\qquad
T_A^g:\mathsf Z_A\to\mathsf Z_A'
\]

with source and target spaces understood from the arrow. Assume composition and inverses agree with the groupoid laws. For covariance of the pushed datum, assume

\[
(T_O^g\times T_I^g)_\#\mathbb P_I(\cdot\mid X)
=\mathbb P_I'(\cdot\mid X'),
\tag{7.1}
\]

the selected posterior versions are jointly compatible,

\[
(T_I^g)_\#\boldsymbol\Pi_{I,o,X}
=\boldsymbol\Pi'_{I,o',X'},
\tag{7.2}
\]

the recognition laws are covariant,

\[
(T_I^g)_\#\mathbb Q_{I,o,X}
=\mathbb Q'_{I,o',X'},
\tag{7.3}
\]

and the channel intertwines the actions,

\[
C_A'(T_I^gY,D)=C_A(Y,(T_A^g)^{-1}D).
\tag{7.4}
\]

Equation (7.2) is an explicit version hypothesis; almost-sure uniqueness of regular conditionals does not choose covariant null-slice values automatically.

Substitution into the defining integrals proves

\[
(T_O^g\times T_A^g)_\#\mathbb P_A(\cdot\mid X)
=\mathbb P_A'(\cdot\mid X'),
\quad
(T_A^g)_\#\boldsymbol\Pi_{A,o,X}
=\boldsymbol\Pi'_{A,o',X'},
\quad
(T_A^g)_\#\mathbb Q_{A,o,X}
=\mathbb Q'_{A,o',X'}.
\tag{7.5}
\]

For example, the posterior identity follows for bounded (f) from

\[
\int f(z')(T_A^g)_\#(\boldsymbol\Pi_{I,o,X}C_A)(dz')
=\int C_A'(f)(T_I^gY)\boldsymbol\Pi_{I,o,X}(dY)
=\int C_A'(f)(Y')\boldsymbol\Pi'_{I,o',X'}(dY').
\]

If (T_A^g) decomposes into measurable maps on (B,M,\Xi,H), model evaluation is covariant only when the additional kernel identity

\[
(T_B^g\times T_O^g\times T_H^g)_\#
K^{X_A}_{A,m}(\xi;\cdot)
=K^{X_A'}_{A,T_M^gm}(T_\Xi^g\xi;\cdot)
\tag{7.6}
\]

holds on the compatibility domain. Equations (4.4) and (7.6) then make the transformed generative conditional compatible with the transformed evaluator.

Equation (7.5) is covariance between source and target slices. Same-slice invariance follows only for isotropy arrows that fix the declared (X) and admitted (o), preserve the selected versions, and identify the source and target spaces. Full-frame triviality is one sufficient way to make these actions identities, but it is not necessary: a nontrivial action may stabilize the full law. Forward projection gives marginal invariance whenever full-law invariance holds. No converse or reconstruction theorem from separate marginal invariance is claimed here; the Task-4 marginal-versus-joint claim remains (\texttt{CANDIDATE}).

The alternative is exact retention rather than blindness. Declare (\mathsf H_A) to include measurable component roots, the raw root-framed based-holonomy representation, and dressed boundary marks, and require (C_A) to output those records jointly with ((B_A,M_A,\Xi_A)). Then (3.1) and (3.4) retain their joint distributions and every correlation with the other parent coordinates by definition of full-law pushforward. No quotient by conjugacy, averaged group element, path erasure, or holonomy-blind invariance is asserted. This retained presentation is the default safe alternative when (7.1)--(7.6) have not been established.

A concrete parent declaration chooses its semantics: either it invokes the holonomy-blind covariance theorem under (7.1)--(7.6), or it retains the raw records and declines a blindness claim. Neither branch selects the membership (A).

## 8. Dynamics is a typed open boundary

The datum above is static. In a separate differentiable special case, let (y(t)) solve (\dot y=V_t(y)), let (c_t) be a differentiable deterministic moving map, and let (\overline V_t) be a proposed coarse vector field. The ordinary chain rule gives

\[
\delta_t
=\partial_tc_t+Dc_tV_t-\overline V_t\circ c_t.
\tag{8.1}
\]

Exact trajectory semiconjugacy is equivalent to (\delta_t=0) on the declared state class. An approximate result needs a norm, a state class, a parameter interval, and a bound on (\delta_t) together with a stability argument that propagates it. The term (\partial_tc_t) cannot be dropped for adaptive memberships or a changing map.

For a Markov evolution, define the observable lift of the kernel (C_A) by

\[
(Uf)(Y)=\int f(z)C_A(Y,dz).
\]

If (T_t) and (\overline T_t) are fine and parent Markov semigroups, exact lumpability is the separately proved intertwining

\[
T_tU=U\overline T_t.
\tag{8.2}
\]

On a common invariant generator domain, (8.2) implies (LU=U\overline L). Conversely, a generator identity yields (8.2) only with a declared invariant domain or core, hypotheses that (L) and (\overline L) generate the stated semigroups, and the required uniqueness or closure theorem for lifting the generator identity to the semigroups. A bare generator identity is insufficient. Nothing in the static pushforward proves (8.1) or (8.2).

Autonomy, dynamically selected membership, Wheelerian coarse-to-fine feedback, sustained nonequilibrium behavior, and a physical-time interpretation of (t) remain OPEN. Closing any one requires, respectively, a well-posed parent evolution, a measurable or smooth selection law, a typed joint bidirectional composition without VFE double counting, a normed state class and nontrivial interval with a persistence theorem, or an operational clock bridge.

## 9. Strongest Task-3 theorem and exact limitations

Under Sections 1--3, one common normalized recognition-independent channel constructs normalized (\mathbb P_A), (\boldsymbol\Pi_{A,o,X}), and (\mathbb Q_{A,o,X}); the second is a selected posterior version and the third is absolutely continuous with respect to it. Section 4 gives model evaluation only through the induced tier or the explicit predeclared compatibility hypothesis. Section 5 derives, rather than posits, all belief and model marginals. Section 6 proves the exact extended KL chain and the finite-tier VFE equality, zero-defect, and pairwise-recovery criteria. Section 7 proves full-law covariance under the complete joint hypotheses and supplies raw holonomy retention as the alternative. Section 8 types dynamics without claiming it.

The result is primary on general normalized laws and kernels over standard-Borel spaces. It supplies no statistical manifold, DQM structure, Fisher metric, Gaussian closure, injective evaluator, regular presentation quotient, canonical membership, full geometric section over (\mathcal U_A), autonomous agent, nonequilibrium theorem, ontic intervention, unique DAG or microscopic physics, or cross-(X) factorization.
