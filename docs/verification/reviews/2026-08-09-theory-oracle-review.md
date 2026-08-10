# Session 2 exact-theory oracle derivation and review

**Review basis.** This is an independent mathematical review of the Session 2
implementation at commit `2480e969fda0aa3f73d8820611ecbfb572d9d9e6`. The
reviewed implementation is `src/multiagent_elbo/finite/theory_oracles.py` and
`src/multiagent_elbo/finite/theory_oracle_experiment.py`; the principal literal
checks are in `tests/test_theory_oracles.py` and
`tests/test_theory_oracle_experiment.py`. The governing mathematical sources are
the frozen `Theory/05_elbo.tex`, `Theory/05c_pullback_geometry.tex`,
`Theory/07b_agent_network_rg.tex`, `Theory/09_coarsegraining.tex`, and
`Theory/SPEC.md`. No statement below promotes a finite fixture to a continuum,
universality, fixed-point, learned-agent, or physical-time claim.

**Verdict.** The exact finite identities encoded by Session 2 are mathematically
correct under the premises named below. The rational implementation realizes
the displayed finite sums and matrix products without floating-point
roundoff. Its comparison with the NumPy production path is useful reproduced
evidence about that implementation, but numerical agreement is not a proof of
the identities. The two-scale application file supplies a checked literal
Jacobian and commuting square only. Its broader application premises and its
recognition extraction-after-lift right inverse remain unverified.

## 1. Finite evidence and ELBO identity

Let a finite evidence submeasure be $M=(M_i)_{i\in X}$, with
$M_i\geq 0$ and

\[
z=\sum_i M_i>0, \qquad p_i=\frac{M_i}{z}.
\]

Thus $p$ is the normalized posterior slice. Let $q$ be a probability
law. On the finite branch $q\ll p$, every index with $q_i>0$ also has
$p_i>0$, and therefore $M_i>0$. The classical finite ELBO is

\[
\mathcal L(q)=\sum_{i:q_i>0}q_i\log\frac{M_i}{q_i}.
\]

Substituting $M_i=zp_i$, using $\sum_iq_i=1$, and collecting only finite
terms gives

\[
\begin{aligned}
\mathcal L(q)
&=\sum_{i:q_i>0}q_i
  \left(\log z+\log p_i-\log q_i\right)\\
&=\log z-\sum_{i:q_i>0}q_i\log\frac{q_i}{p_i}\\
&=\log z-D_{\mathrm{KL}}(q\Vert p).
\end{aligned}
\]

Equivalently, on this finite branch,

\[
\log z-\mathcal L(q)-D_{\mathrm{KL}}(q\Vert p)=0.
\]

This is exactly the algebra encoded by `exact_evidence_elbo`. Rational log
arguments are prime-factorized into a canonical formal sum, so cancellation
to the empty formal-log sum is an exact statement rather than a small
floating residual. For the frozen fixture, $z=1/2$, and the test literal is

\[
\log z=-\log 2,\qquad
\mathcal L=\log 3-3\log 2=\log(3/8),\qquad
D_{\mathrm{KL}}=2\log 2-\log 3.
\]

The support-violating branch must be stated separately. If some $i$ has
$q_i>0=p_i$, then $D_{\mathrm{KL}}(q\Vert p)=+\infty$ and the canonical
extended ELBO is $-\infty$. The well-defined assertion is the extended gap

\[
\log z-\mathcal L^{\mathrm{ext}}(q)
=D_{\mathrm{KL}}(q\Vert p),
\]

not an unconditional rearrangement
$\log z=\mathcal L^{\mathrm{ext}}+D_{\mathrm{KL}}$, whose right-hand side
would be the undefined sum $-\infty+\infty$. The oracle preserves this
boundary by returning the extended values, the offending support indices,
and no residual. This matches the extended-real qualification in
`Theory/05_elbo.tex`.

**Falsifier.** On the finite branch, any nonempty canonical residual falsifies
the encoding. On the singular branch, returning a finite KL, a finite ELBO, or
forming an (-\infty+\infty) residual falsifies the claimed boundary handling.

## 2. Fixed-channel score and Fisher defect

Let $p_\theta(x)>0$ on its active finite support, let
$s_a(x)=\partial_a\log p_\theta(x)$ be a centered score, and let
$K(y\mid x)$ be a normalized source-row Markov kernel independent of
$\theta$. Define

\[
w(x,y)=p_\theta(x)K(y\mid x),\qquad
r(y)=\sum_xw(x,y).
\]

For $r(y)>0$, differentiation through the fixed channel gives the coarse
score

\[
\bar s_a(y)
=\partial_a\log r(y)
=\frac{\sum_xw(x,y)s_a(x)}{r(y)}
=\mathbb E[s_a(X)\mid Y=y].
\]

No conditional is formed at $r(y)=0$; such targets make zero contribution.
The fine and coarse Fisher matrices are

\[
(I_X)_{ab}=\sum_xp(x)s_a(x)s_b(x),\qquad
(I_Y)_{ab}=\sum_yr(y)\bar s_a(y)\bar s_b(y).
\]

Since $\sum_yK(y\mid x)=1$, the fine matrix can also be written as
$\sum_{x,y}w(x,y)s(x)s(x)^\top$. Expanding the joint-weighted conditional
covariance gives

\[
\begin{aligned}
&\sum_{x,y}w(x,y)
  (s(x)-\bar s(y))(s(x)-\bar s(y))^\top\\
&\quad=I_X
-\sum_y r(y)\bar s(y)\bar s(y)^\top
-\sum_y r(y)\bar s(y)\bar s(y)^\top
+\sum_y r(y)\bar s(y)\bar s(y)^\top\\
&\quad=I_X-I_Y\succeq0.
\end{aligned}
\]

The second and third terms use
$\sum_xw(x,y)s(x)=r(y)\bar s(y)$. In the one-parameter literal packet,
$p=(1/3,2/3)$, $s=(2,-1)$, and

\[
K=\begin{pmatrix}1&0\\1/4&3/4\end{pmatrix}.
\]

This yields $r=(1/2,1/2)$, $\bar s=(1,-1)$, $I_X=2$, $I_Y=1$, and
conditional covariance $1$, so the defect closes exactly. An unweighted
average would instead give the wrong first conditional score $1/2$.

The theorem consumes more than finite arithmetic: the channel must be
parameter independent, the selected statistical family must admit the score
(DQM is sufficient in the frozen theory), the score must be square
integrable and centered, and the output family must be closed under the
channel. If $K=K_\theta$, differentiating $r_\theta$ adds a channel-score
term; the displayed conditional-score formula no longer follows. The exact
fixture checks the finite algebra after these analytic premises are declared;
it does not prove DQM or family closure.

**Falsifier.** A mismatch between $I_X-I_Y$ and the displayed joint-weighted
conditional covariance falsifies the finite encoding. Acceptance of a
transposed or nonnormalized source-row channel, or promotion of the result to
a parameter-dependent channel, falsifies its typing.

## 3. Marked-event pushforward and associativity

Let $p(y)$ be a state law and let $\eta(i,j\mid y)$ be a normalized joint
receiver-source event law conditional on state. Let $A(z\mid y)$,
$B(I\mid i)$, and $C(J\mid j)$ be source-row Markov kernels. The object
that must be pushed is the joint marked law

\[
\mu(y,i,j)=p(y)\eta(i,j\mid y),
\]

not $\eta$ alone and not a source-given-receiver row $\beta$ alone. Its pushforward is

\[
\mu'(z,I,J)=\sum_{y,i,j}p(y)\eta(i,j\mid y)
A(z\mid y)B(I\mid i)C(J\mid j).
\]

The coarse state mass is $p'(z)=\sum_{I,J}\mu'(z,I,J)$. Only where
$p'(z)>0$ is the conditional event law
$\eta'(I,J\mid z)=\mu'(z,I,J)/p'(z)$ formed. Receiver occupancy and the
source-given-receiver row are subsequent disintegrations of this same joint.
This ordering retains the receiver weights needed to combine independently
normalized rows.

For two stages, write $A_1,A_2$ for the state kernels and analogously for
the two mark axes. Direct pushforward uses

\[
(A_1A_2)(z\mid y)=\sum_uA_1(u\mid y)A_2(z\mid u),
\]

with the corresponding products $B_1B_2$ and $C_1C_2$. Expanding the
direct joint gives a finite sum over $y,i,j,u,r,s$. Staged pushforward first
forms

\[
\mu_1(u,r,s)=\sum_{y,i,j}\mu(y,i,j)
A_1(u\mid y)B_1(r\mid i)C_1(s\mid j),
\]

and then sums

\[
\sum_{u,r,s}\mu_1(u,r,s)
A_2(z\mid u)B_2(I\mid r)C_2(J\mid s).
\]

Substitution of the first display into the second and reassociation of finite
sums produces the direct expression term for term. If a staged conditional
$\eta_1$ is used, its state mass multiplies it before the second push, so
$p_1(u)\eta_1(r,s\mid u)=\mu_1(u,r,s)$. This is the finite tower-property
argument and explains why zero-mass states have no conditional version.

The asymmetric literal produces the same eight direct and staged joint
entries, including $p'=(101/315,214/315)$. Reversing kernel composition
changes the state mass to $(121/252,131/252)$, so orientation is
observationally discriminating. A separate literal shows that omitting the
source state mass changes the joint. Another shows that equal averaging of
$\beta$ rows gives $(1/2,1/2)$ where the pushed joint requires $(1/4,3/4)$.

**Falsifier.** Any direct/staged joint mismatch under normalized kernels
falsifies associativity. Agreement obtained only after dropping $p(y)$,
averaging conditional rows without receiver occupancy, reversing source-row
composition, or inventing a conditional on zero mass does not test the stated
theorem.

## 4. Hoeffding/Möbius reconstruction and retained residual

Let $X=\prod_{a\in V}X_a$ be finite and let the declared reference be the
normalized product law $\nu=\bigotimes_{a\in V}\nu_a$. For $A\subseteq V$, define the
conditional projection, lifted back to the full tensor shape,

\[
(C_Af)(x_A)=\sum_{x_{A^c}}f(x_A,x_{A^c})
\prod_{a\notin A}\nu_a(x_a).
\]

The Möbius component is

\[
P_Af=\sum_{B\subseteq A}(-1)^{|A|-|B|}C_Bf.
\]

Summing over all subsets and collecting the coefficient of $C_Bf$ yields

\[
\sum_{A\subseteq V}P_Af
=\sum_{B\subseteq V}C_Bf
  \sum_{A:B\subseteq A\subseteq V}(-1)^{|A|-|B|}.
\]

The inner sum is $(1-1)^{|V|-|B|}$, hence it vanishes unless $B=V$.
Since $C_V=I$, the full reconstruction is exactly $f$. The empty
component $P_\varnothing f=C_\varnothing f$ is required for reconstruction
of the function itself; omitting it reconstructs only the equivalence class
modulo constants.

For a retained interaction order $k$, define

\[
f_{\leq k}=\sum_{|A|\leq k}P_Af,\qquad
R_{>k}=f-f_{\leq k}=\sum_{|A|>k}P_Af.
\]

The oracle records both the zero full-reconstruction residual and the
generally nonzero retained residual. For the uniform three-spin literal

\[
f=(-1,1,1,-1,1,-1,-1,1),
\]

every projection associated with a proper subset is zero. Therefore the
only nonzero component is $P_{\{0,1,2\}}f=f$. Retaining through order two
gives $f_{\leq2}=0$ and $R_{>2}=f\neq0$. This is a direct witness that a
pairwise-only truncation loses a genuine higher-order interaction. The
nonuniform-reference test separately confirms that the implementation uses
the declared factor weights rather than silently substituting uniform
weights.

Product structure is load bearing for the coordinatewise conditional
projections and their commuting-projector interpretation. The implementation
requires one normalized factor law per tensor axis. It does not establish
that an arbitrary target law admits an equivalent product reference; the
frozen theory contains explicit cases where no such reference exists.

**Falsifier.** A nonzero full residual, omission of the empty component,
failure under a normalized nonuniform product reference, or disappearance of
the three-way residual after an order-two truncation falsifies the encoding.

## 5. Three separately typed Gaussian operations

These operations have different domains and meanings. Equality of their
output dimensions does not identify them.

### 5.1 Inverse congruence and the transformed prolongator

Let $A\in\mathbb Q^{n\times n}$, let $G_f\in\mathrm{GL}_n(\mathbb Q)$,
and let $S\in\mathbb Q^{n\times m}$. If old and new fine coordinates obey
$x_{\rm old}=G_f^{-1}x_{\rm new}$, the quadratic matrix in the new frame is

\[
A'=G_f^{-T}AG_f^{-1}.
\]

With an independent coarse frame $G_c\in\mathrm{GL}_m(\mathbb Q)$, the
same prolongation map is represented by

\[
S'=G_fSG_c^{-1}.
\]

Consequently

\[
S'^TA'S'
=G_c^{-T}S^TAG_c^{-1}.
\]

This proves the commuting congruence square. Holding the numerical matrix
$S$ fixed is valid only under the intertwining condition
$G_fS=SG_c$, which the implementation checks when requested.

For the exact packet, $A=\operatorname{diag}(2,3,4,5)$, the declared
prolongator ties coordinates $(0,2)$ and $(1,3)$,
$G_f=\operatorname{diag}(2,1,1,3)$, and
$G_c=\operatorname{diag}(5,2)$. The calculations give

\[
S^TAS=\operatorname{diag}(6,8),\qquad
S'^TA'S'=\operatorname{diag}(6/25,2)
=G_c^{-T}(S^TAS)G_c^{-1}.
\]

Invertibility of both frames is necessary for these inverse congruences. If
$A$ is symmetric positive definite, inverse congruence preserves that
property; the rational routine itself correctly implements the more general
algebraic operation and does not pretend to prove SPD from unchecked input.

### 5.2 Galerkin restriction

The Galerkin operator is

\[
A_G=S^TAS.
\]

It is the exact restriction of the quadratic energy to the identified
subspace $x=Sz$, because $x^TAx=z^TA_Gz$. Symmetry or definiteness is not
needed for this algebraic equality. For a Gaussian precision interpretation,
$A$ should be symmetric positive definite; $A_G$ is then positive
definite when $S$ has full column rank. In the packet above,
$A_G=\operatorname{diag}(6,8)$.

### 5.3 Schur complement

Partition a symmetric precision by retained coordinates $R$ and eliminated
coordinates $E$:

\[
A=\begin{pmatrix}A_{RR}&A_{RE}\\A_{ER}&A_{EE}\end{pmatrix}.
\]

When $A_{EE}$ is invertible, the algebraic Schur complement is

\[
\operatorname{Sc}_E(A)
=A_{RR}-A_{RE}A_{EE}^{-1}A_{ER}.
\]

If $A\succ0$, then $A_{EE}\succ0$, and completing the square in the
eliminated variables shows that this is the precision induced by Gaussian
marginalization (up to the usual information-vector update when a nonzero
linear term is present). This SPD hypothesis supplies the probabilistic
meaning; mere invertibility supplies only the algebraic formula.

For

\[
A=\begin{pmatrix}4&1&0\\1&3&1\\0&1&2\end{pmatrix},
\quad R=(0,2),\quad E=(1),
\]

the exact result is

\[
\operatorname{Sc}_E(A)
=\begin{pmatrix}4&0\\0&2\end{pmatrix}
-\frac13\begin{pmatrix}1\\1\end{pmatrix}
\begin{pmatrix}1&1\end{pmatrix}
=\begin{pmatrix}11/3&-1/3\\-1/3&5/3\end{pmatrix}.
\]

For the displayed aggregation prolongator, Galerkin restriction instead
gives

\[
S^TAS=\begin{pmatrix}9&1\\1&2\end{pmatrix}.
\]

Their inequality is expected: hard identification and marginal integration
are different maps. The code enforces a full, disjoint, unique, in-range
retained/eliminated partition and exact invertibility of the eliminated
block. It does not collapse the two constructions.

**Falsifier.** Failure of the congruence square, acceptance of a singular
frame, disagreement with $S^TAS$, disagreement with the Schur formula, or
identification of Galerkin restriction with marginalization falsifies the
corresponding encoding. A Gaussian-law claim from a nonsymmetric or non-SPD
input would exceed what the exact algebra establishes.

## 6. Frozen two-scale Jacobian and commuting square

The application fixture declares the block-average coordinate map

\[
C=\begin{pmatrix}
1/2&1/2&0&0\\
0&0&1/2&1/2
\end{pmatrix}.
\]

Because this map is linear, its Jacobian is the same constant matrix $C$.
The frozen application comparisons are $I_f=I_4$ and $I_c=I_2$, so

\[
I_cC=C=CI_f.
\]

This application square is exact but structurally simple. The separate
lane-private nonidentity control guards against a hard-coded identity result:

\[
I_f=\operatorname{diag}(2,2,3,3),\qquad
I_c=\operatorname{diag}(2,3)
\]

gives

\[
I_cC=CI_f=
\begin{pmatrix}1&1&0&0\\0&0&3/2&3/2\end{pmatrix},
\]

whereas changing the second coarse comparison factor to $4$ makes the two
paths unequal. The loader also checks the canonical fixture digest, the
source-row channel shape and normalization, rational literal canonicality,
probability normalization, evidence/posterior consistency, and invertibility
of the two declared comparison maps.

Those checks do **not** establish the full application theorem. In particular,
the fixture's typed equation “extraction after lift equals the identity on the
open unit cube” remains `NOT_CHECKED`. The application conclusion remains
`theorem_status=HYPOTHESIS`, `verification_state=CANDIDATE`, and
`claim_origin=APPLICATION_SPECIFIC`. No exact commuting square can substitute
for the right-inverse proof, local-to-collective VFE premises, absolute
continuity obligations, or any later scientific-lane conclusion.

**Falsifier.** A digest mismatch, a noninvertible declared comparison, or
$I_cC\neq CI_f$ falsifies this literal application check. Passing this check
does not falsify or verify any of the still-open application-family premises.

## 7. Evidence boundary and closure assessment

The `Fraction` path establishes the encoded finite algebra once its inputs
meet the declared premises. The exact numerator/denominator artifacts make
that path reproducible, and the experiment adapter reconstructs each oracle
metric layout from those exact components before comparing it with the
separate floating production path. Mutation controls detect reversed channel
orientation, omitted state mass, wrong conditional weights, missing
higher-order interactions, malformed Schur partitions, and a noncommuting
comparison square. These are strong anti-tautology controls for the finite
implementation.

The following claims remain outside that closure:

- DQM transfer, smooth family closure, and parameter independence are analytic
  premises of the Fisher theorem, not consequences of rational enumeration.
- Existence of an application-appropriate product reference is a premise of
  the Hoeffding coordinates; it is not automatic for arbitrary pushed laws.
- SPD and invertibility must be supplied where a rational matrix calculation
  is interpreted as a proper Gaussian precision or marginalization.
- The application recognition right inverse and the remaining application
  premises are open at this revision.
- Finite exactness does not prove continuum limits, RG fixed points,
  universality, learned-agent behavior, or physical interpretations.

Accordingly, the finite evidence/ELBO, conditional Fisher-defect,
marked-event associativity, full Hoeffding reconstruction, inverse-congruence,
Galerkin, and Schur identities are supported here by derivation. The
application-family conclusion is not closed. Floating-point residuals may
corroborate correct implementation of these formulas, but no residual,
however small, changes a mathematical claim from numerical evidence into a
proof.

## Source and implementation map

| Subject | Frozen mathematical source | Exact implementation | Literal and negative controls |
|---|---|---|---|
| Evidence/ELBO | `Theory/05_elbo.tex`, extended gap and classical identity | `theory_oracles.py:484` | `test_theory_oracles.py:59,97` |
| Fisher defect | `Theory/05c_pullback_geometry.tex`, Fisher-defect section | `theory_oracles.py:556` | `test_theory_oracles.py:119,148` |
| Marked events | `Theory/07b_agent_network_rg.tex`, exact meta-attention | `theory_oracles.py:828` | `test_theory_oracles.py:167,209,235,342` |
| Hoeffding/Möbius | `Theory/07b_agent_network_rg.tex`, coordinate projectors | `theory_oracles.py:981` | `test_theory_oracles.py:364,390` |
| Gaussian operations | `Theory/09_coarsegraining.tex`, hard aggregation and Kron reduction | `theory_oracles.py:1107,1144,1178` | `test_theory_oracles.py:472,534,566` |
| Two-scale square | `Theory/SPEC.md` and `tests/fixtures/two_scale_application_v1.json` | `theory_oracles.py:1045,1404` | `test_theory_oracles.py:602,626,680` |
