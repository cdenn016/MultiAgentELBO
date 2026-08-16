# Multiscale two-channel gauge-network VFE — Part 3
## Non-flat connections, block formation, and cross-scale dynamics (Q6, Q7, Q8)

Continues Parts 1–2.

## 9. Q6 — treating non-flat connection data exactly

### 9.1 The objects

For an oriented cycle $C=e_1\cdots e_r$ in channel $x\in\{b,m\}$ put
$H^x_C=\Omega^x_{e_r}\cdots\Omega^x_{e_1}$, and for a connected block $I$ with a
chosen root $r_I$ let $H^x_I:\pi_1(\Gamma_I,r_I)\to G$ be the based holonomy
representation. Under a passive section rechoice $a^x_i$ these transform by
conjugation at the root, $H^{x\prime}_I(\gamma)=(a^x_{r_I})^{-1}H^x_I(\gamma)a^x_{r_I}$,
and the tree transports by
$\tau^{x\prime}_{I\leftarrow i}=(a^x_{r_I})^{-1}\tau^x_{I\leftarrow i}a^x_i$.
Nonidentity $H^x_C$ is allowed and is **not** penalized toward the identity
anywhere below.

### 9.2 When is $H_\#Q=Q$ necessary, and when sufficient?

Write $\mathfrak h^x_I(r)=\{T^x_\lambda:\lambda\ \text{a loop at}\ r\}$ for the
based-loop transport group and
$\mathscr Q^x_{I,\rm fix}(r)=\{Q\in\mathscr M^x_r:H_\#Q=Q\ \forall H\in\mathfrak h^x_I(r)\}$
for the stabilized sector inside the admitted parent family. The answer splits by
regime.

**(A) On the zero-distortion sector, stabilization is necessary and sufficient.**
With $\mathcal D_x=\sum_{i,j:\eta^x_{ij}>0}\eta^x_{ij}D_{\rm KL}(p^x_i\Vert(T^x_{ij})_\#p^x_j)$
on a connected positive-support graph with reciprocal transports,

$$
\mathcal D_x=0
\iff p^x_i=(T^x_{ij})_\#p^x_j\ \text{on every positive-support edge}
\iff \exists!\,Q_x:\ (T^x_{\gamma_i})_\#p^x_i=Q_x\ \forall i,\ \ H_\#Q_x=Q_x\ \forall H\in\mathrm{Hol}^x_r .
$$

So an exactly parallel parent exists precisely when a stabilized law exists and the
transported marginals all equal it. Both channels must vanish independently:
$\mathcal D_b+\mathcal D_m=0\iff\mathcal D_b=\mathcal D_m=0$.

**(B) Off that sector, stabilization is neither necessary nor sufficient for
anything one wants.** Two exact witnesses, both already established in the
project's counterexample register:

* *Flatness does not give agreement.* On a two-node tree with $\Omega=I$ and
  Gaussian beliefs with means $\pm a e_1$ and unit covariance, the transported
  divergence is $2a^2>0$. Trivial holonomy, arbitrary disagreement.
* *Agreement does not require flatness.* $H=\mathrm{diag}(1,-1,-1)\ne I$ stabilizes
  an isotropic Gaussian. Nonidentity holonomy, exact agreement.

Consequently **full-frame flatness $H=I$ and state stabilization $H_\#Q=Q$ are
different conditions and neither implies the other.** For the fixed-$K$
connection-Laplacian sector with reciprocal invertible links and positive-definite
internal edge weights one has $\ker L_I\cong\mathrm{Fix}(\mathrm{Hol}_r)$, so
represented trivial holonomy is necessary and sufficient *for that full sector*;
semidefinite edge weights fall outside and need the edgewise visibility condition.

**(C) A holonomy-blind *joint* parent needs far more than stabilized marginals.**
The marginal statement above concerns transported marginal laws. Blindness at the
level of the full parent triple $(\mathbb P_A,\boldsymbol\Pi_A,\mathbb Q_A)$
requires the whole package: bimeasurable typed groupoid actions on the fine random
space, on $\mathsf Z_A$, on $\mathsf O$, and on $X$; covariance of the fine
generative and recognition laws; a posterior-version family compatible with those
actions; channel equivariance $C_A(g\cdot Y,g\cdot D)=C_A(Y,D)$; and evaluator
covariance. Same-slice invariance at fixed $(o,X)$ follows only for isotropy
arrows fixing $(o,X)$. And the scope caveat matters: what that argument proves is
*covariance of the full parent laws under a declared groupoid*, by substitution of
an equivariant channel — no connection form, horizontal distribution, lift, loop,
or curvature enters. It is not a statement that a holonomy was computed or
quotiented away.

**(D) A holonomy-induced obstruction to block formation.** This is worth stating
separately because it is a mechanism, not a caveat.

**Proposition 8.** If the based holonomy group $\mathrm{Hol}^x_r$ acts on
$\mathcal P(\mathsf Z^x_r)$ with **no fixed point inside the admitted parent
family** $\mathscr M^x_r$, then $\mathscr Q^x_{I,\rm fix}(r)=\varnothing$ and the
holonomy-conditioned forward-KL score is $\mathfrak D^x_I=+\infty$ (by the
convention $\inf\varnothing:=+\infty$). No zero-distortion parent exists for that
block, and the block-formation energy has a strictly positive floor set by the
holonomy alone.

*Witness.* Let $\mathsf Z^x_r=\mathbb R$, $G=\mathbb Z_2$ acting by $a\mapsto-a$
on the sample space, and let the admitted family be the Dirac masses
$\mathscr M=\{\delta_a:a\ne0\}$. Then $H_\#\delta_a=\delta_{-a}\ne\delta_a$ for
every admitted $a$, so $\mathscr Q_{\rm fix}=\varnothing$ and $\mathfrak D=+\infty$.
The same happens for a Gaussian family with fixed nonzero mean magnitude under a
reflection holonomy. $\square$

The physical reading: on a cyclic graph, nontrivial holonomy can make a coherent
meta-agent **impossible** rather than merely expensive. Cycles are not a neutral
complication of the tree case. Whether $\mathrm{Fix}(\mathrm{Hol})\cap\mathscr M$
is empty is a checkable property of the pair (holonomy group, admitted family) and
belongs in any block-formation criterion.

### 9.3 What the parent must retain when stabilization fails

The exact datum is the simultaneous root-framed equivariant state

$$
\big(\bar z^x_I,\ H^x_I,\ \{V^x_e\}\big),
\qquad
V^x_e=\tau^x_{I\leftarrow i}\,\Theta^x_e\,(\tau^x_{J\leftarrow j})^{-1},
$$

taken as one simultaneous root-gauge orbit. Four separate warnings attach.

* **Do not quotient each holonomy separately.** Quotienting $H^x_I$ by conjugacy
  independently of the root features and boundary legs loses its orientation
  relative to them. Only the *simultaneous* orbit is a legitimate quotient.
* **Noncompact $G$ blocks the naive quotient.** A conjugacy quotient of a
  noncompact group need not be standard Borel, so the measure tier retains the raw
  root-framed $G$-space unless a proper-action or standard-Borel quotient theorem is
  supplied.
* **Disconnected blocks have no single root.** A soft parent is not assumed
  connected. Index every incidence $(A,i)$ by its channel-specific connected
  component $c^x_A(i)$ inside $V_A=\{i:C(A\mid i)>0\}$, use component meta-labels
  $\widehat A=(A,c)$, and root each component separately. Summing component masses
  recovers the scalar $(A,B)$ event mass, but collapsing disconnected component
  roots or mark fibers to one parent root is a further declared coarse channel with
  its own conditional KL.
* **Different trees, different presentations.** Nested trees with the compatibility
  of Part 2 §8.5 give strict composition; arbitrary tree choices give a
  root-gauge-equivariant isomorphism of presentations, related by Nielsen
  transformations.

### 9.4 The distribution of dressed microscopic transports

The problem statement asks specifically for the distribution of
$\Theta^{IJ,x}_{ij}=\Omega^x_{Ii}\Omega^x_{ij}\Omega^x_{jJ}$, not a mean. This is
the right demand, and the reasons are sharp.

**Define the exact object.** Condition on the coarse edge event $(I,J)$ and push
the joint edge-event-and-mark law:

$$
\boxed{\;
\mu^x_{IJ}(dg\mid z)\;:=\;\frac{1}{\eta^{x,c}_{IJ}(z)}\,
\mathbb E_{B_o}\!\Big[\sum_{i\in I,\,j\in J}\eta^x_{ij}(Y)\,\delta_{\Theta^{IJ,x}_{ij}}(dg)\ \Big|\ Z=z\Big]
\;}
$$

on $\{\eta^{x,c}_{IJ}>0\}$, a normalized probability measure on $G$ (or on the
represented group $R_x(G)$), defined as a Markov kernel $z\mapsto\mu^x_{IJ}(\cdot\mid z)$.
This is the exact coarse connection datum. It is normalized by construction and
requires no integrability hypothesis.

**Why a mean is not a substitute.** Three independent failures.

1. *The mean is not a group element.* The average of rotations by $+\pi/2$ and
   $-\pi/2$ is the zero matrix, which is not in $\mathrm{SO}(2)$ and not
   invertible. So "the coarse edge transport," as a single group element, does not
   exist for a generic $\mu^x_{IJ}$. The set of measures whose barycenter lies in
   $R_x(G)$ is not generic and is not preserved under blocking.
2. *The first moment need not exist.* The Hom operator
   $\mathsf T^x_{IJ}(z)=\mathbb E_{B_o}[\sum\eta_{ij}R_x(V^x_{ij})\mid Z=z]$ is
   defined only under the conditional Bochner-integrability condition
   $\mathbb E_{B_o}[\sum\eta_{ij}\Vert R_x(V^x_{ij})\Vert\mid Z]<\infty$ a.e. For
   noncompact $\rho_x$ this can fail.
3. *A mean transport plus a mean feature does not give the mean message.* If marks
   and source features are correlated, means do not determine $\mathbb E[Uz]$:
   equal-probability pairs $(I,v)$ and $(-I,-v)$ have zero mean mark and zero mean
   feature but mean product $v$. Exact closure therefore retains the marked
   operator–feature kernel, with the Hom moment as a derived quantity, not as the
   state.

**Composition of coarse transports as measures.** The natural question at the next
scale is how $\mu$ composes. Here is the exact statement and its obstruction.

**Proposition 9 (convolution under conditional independence, correlation defect
otherwise).** Fix coarse nodes $I,J,K$ and condition on the coarse state $z$. Let
$\Theta^{IJ}$ and $\Theta^{JK}$ be the dressed transports sampled from consecutive
coarse edge events. If, given $z$ and given the pair of coarse edge events, the two
dressed marks are conditionally independent, then the law of the composite
$\Theta^{IK}=\Theta^{IJ}\Theta^{JK}$ is the ordered convolution
$\mu^x_{IJ}\ast\mu^x_{JK}$ on $G$. Without that hypothesis the composite law is the
pushforward of the *joint* mark law under group multiplication, and it differs from
the convolution by exactly the dependence between the two marks.

*Proof.* Group multiplication $m:G\times G\to G$ is measurable; the law of
$m(\Theta^{IJ},\Theta^{JK})$ is $m_\#$ of their joint law, which factorizes as the
product measure precisely under conditional independence, and $m_\#(\mu\otimes\nu)$
is by definition the convolution. $\square$

The dependence is not a pathology to be assumed away: consecutive coarse edges
share the intermediate block's internal tree transports $\tau^x_{J\leftarrow\cdot}$,
which appear in $\Theta^{IJ}$ (as a right factor) and in $\Theta^{JK}$ (as a left
factor). Those factors **cancel** in the product when the same intermediate node is
used, and do not cancel otherwise. So conditional independence is exactly the
statement that the intermediate node index is independent across the two hops — a
Markov property on the coarse walk, and a genuine hypothesis.

**Coarse holonomy blindness, stated on the distribution.** With $\mu$ in hand, the
right coarse-scale criterion is not "the mean transport stabilizes $Q_I$" but

$$
\mathrm{supp}\,\mu^x_{\rm loop}(\cdot\mid z)\subseteq\mathrm{Stab}(Q_I)
:=\{g:\ (R_x(g))_\#Q_I=Q_I\}\qquad\text{for }\ z\ \text{-a.e.},
$$

where $\mu^x_{\rm loop}$ is the ordered-convolution law of a coarse loop.
$\mathrm{Stab}(Q_I)$ is a closed subgroup, so this is a checkable support
condition. Penalizing the *variance* of $\mu$ toward zero, or penalizing its mean
toward the identity, is an extra modeling preference and is not a consequence of
gauge covariance.

**When may a mean plus a residual be used?** Only as a declared truncation. Write
$\overline{\mathsf U}^x_{IJ}=\mathsf T^x_{IJ}/\eta^{x,c}_{IJ}$ for the normalized
first moment and define the residual as the omitted part of the conditional law,
$\mathrm{res}^x_{IJ}:=\mu^x_{IJ}-\delta_{\overline{\mathsf U}^x_{IJ}}$ as a signed
measure, or in operator form the conditional covariance of $R_x(\Theta)$. Report
its norm alongside any flow; this is the connection-sector instance of the
truncation residual $\delta\beta_\ell$ of Part 3 §11.4.

## 10. Q7 — can descent spontaneously produce persistent scale-1 and scale-2 blocks?

**Verdict first.** No current result proves it, and two of the obvious routes are
provably insufficient. What can be said is: (a) a *conditional* mean-field
instability exists for a declared composite potential; (b) any block so produced is
a local minimum of a Lyapunov functional, so "persistence" is a metastability
statement, not a descent statement; and (c) on a cyclic graph holonomy can make the
target object nonexistent (Proposition 8). Scale-2 blocks require in addition a
closure hypothesis that is unproved.

### 10.1 Four competing block-formation mechanisms

**M1 — Annealed attention (canonical Gibbs feedback).** Beliefs and rows coevolve:
$\beta^\star_{ij}\propto\pi_{ij}e^{-\mathbb E_{\mathbb Q}D_{ij}/\tau_i}$ while
$D_{ij}$ falls as beliefs align. Low disagreement raises attention; raised
attention strengthens alignment. Order parameter: a coherence scalar $m$ with
$D(m)=D_0-cm^2$, $c>0$. This is the mechanism implicit in the row free energy.

**M2 — Grand-canonical occupation (lattice gas).** Introduce a binary edge
occupation $a_{ij}$ with mean $\rho_{ij}$, an edge energy
$\epsilon_{ij}=J_qD^q_{ij}+J_mD^m_{ij}+B_{ij}-G_{ij}$, a chemical potential
$\mu_{ij}$, and an edge temperature $\tau_E$. The minimizer is
$\rho^\star_{ij}=\mathrm{sigmoid}[\mathrm{logit}(\pi^E_{ij})+(\mu_{ij}-\epsilon_{ij})/\tau_E]$
with grand potential
$\Phi_E=-\tau_E\sum\log[1-\pi^E+\pi^Ee^{(\mu-\epsilon)/\tau_E}]$ and exact
conjugacy $-\partial\Phi_E/\partial\mu_{ij}=\rho^\star_{ij}$. A parallel
construction on membership indicators $n_{iA}$ gives
$\rho^\star_{iA}=\mathrm{sigmoid}[\mathrm{logit}(\pi_{iA})+(\mu_A-\epsilon_{iA})/\tau_A]$
with expected parent size conjugate to $\mu_A$.

The mean-field reduction gives a calculable instability. With
$\mathcal G_{\rm mf}(m,\rho)=\tfrac a2m^2+\tfrac b4m^4+\rho J(D_0-cm^2)-\mu\rho
+\tau_E[\rho\log\rho+(1-\rho)\log(1-\rho)]$, eliminating $\rho$ and writing
$\rho_0=\mathrm{sigmoid}((\mu-JD_0)/\tau_E)$, the quadratic coefficient is
$(a-2Jc\rho_0)/2$, so the incoherent state loses local stability exactly when

$$
\boxed{\,2Jc\rho_0>a\,}
$$

and the quartic coefficient acquires the correction
$-J^2c^2\rho_0(1-\rho_0)/(2\tau_E)$: positive final quartic gives a continuous
transition, negative gives a discontinuous one with hysteresis. The occupation
susceptibility $\partial\rho_0/\partial\mu=\rho_0(1-\rho_0)/\tau_E$ peaks at half
occupation and is a direct experimental diagnostic.

Status of M2: this is a **conditional reduction of a proposed composite
functional**, not a theorem about the network and not an ELBO. It requires
declared $J,c,a,\mu,\tau_E,B,G$; the VFE supplies none of them.

**M3 — Spectral/diffusion blocking (Laplacian RG import).** Blocks are
diffusion-equivalence cells at the scale $\tau^\*$ where the entropic
susceptibility $C(\tau)=-dS/d\log\tau$ of $\rho(\tau)=e^{-\tau L}/Z(\tau)$ peaks.
The obstruction here is gauge: represented heat-kernel blocks transform as
$K_{ij}\mapsto g_i^{-1}K_{ij}g_j$ and are **not** invariant scalar node affinities.
Part 4 §12.3 gives the repair — run the construction on the edge-event law, which
is gauge-invariant by construction, and use a directed Laplacian built from it.

**M4 — Aggregation-invariance (MSM route): do not select blocks at all.** Choose
the model family whose functional form is invariant under *every* partition, so no
block selection is needed. The uniqueness result behind this
(Garuccio–Lalli–Garlaschelli) is for edge-independent Bernoulli graphs with an
additive scalar fitness, $p_{ij}=1-e^{-\delta x_ix_jf(d_{ij})}$. Its transferable
content here is the criterion, not the formula: **renormalizability is additivity
of the defining parameter.** $\eta$ is additive; $\beta$ is not. The two-channel,
matrix/group-valued analogue of the uniqueness theorem is open.

### 10.2 Why low transported KL alone is insufficient

**Counterexample N1a (uniform mismatch produces no block).** The row is
normalized. If $\mathbb E_{\mathbb Q}D_{ij}=D$ for every admitted source $j$, then

$$
\beta^\star_{ij}=\frac{\pi_{ij}e^{-D/\tau_i}}{\sum_k\pi_{ik}e^{-D/\tau_i}}=\pi_{ij},
$$

independently of $D$. Driving every transported divergence to zero therefore leaves
every row exactly at its reference and produces no structure at all. What the row
responds to is **contrast** $D_{ij}-D_{ik}$, not level. Any criterion of the form
"cluster the agents whose transported KL is small" is measuring the wrong quantity.

A second, sharper version: the row-optimal free energy is
$\mathcal F^{\rm row}_{i,\rm red}=-\tau_i\log Z_i$, which under a uniform shift
$D\mapsto D+c$ changes by exactly $c$ for every $i$ — a global constant with zero
gradient in any direction that could distinguish blocks.

**And KL thresholds do not even define clusters.** Thresholding
$D_{\rm KL}$ at $0.6$ nats on the Bernoulli chain $1/10\to1/2\to9/10$ links the
first two and the last two but not the first and last: KL-threshold adjacency is
not transitive, so it does not induce a partition.

### 10.3 Why large $\eta$ alone is insufficient

**Counterexample N1b ($\eta$ ranks hubs, not blocks).** Since
$\eta_{ij}=\alpha_i\beta_{ij}$, a high-occupancy receiver with a completely flat row
outranks a low-occupancy receiver with a deterministic row. Take
$\alpha_1=0.9$ with $\beta_1$ uniform over $n=4$ sources, and $\alpha_2=0.05$ with
$\beta_{2,3}=1$. Then $\eta_{1j}=0.225$ for each $j$ while $\eta_{23}=0.05$. Ranking
edges by $\eta$ selects the four *uninformative* edges of the hub over the one
*perfectly concentrated* edge. Edge-event mass measures how often an interaction is
sampled, not how structured it is.

The correct structural quantity separating these is the row's departure from its
reference, $D_{\rm KL}(\beta_i\Vert\pi_i)$, weighted by occupancy — that is,
$\alpha_iD_{\rm KL}(\beta_i\Vert\pi_i)$, the *mutual-information-like* part of the
edge-event law rather than its mass. Neither $\eta$ alone nor $D$ alone is it.

### 10.4 Hypotheses a persistence theorem would need

State them separately because they fail independently.

**(H1) Timescale separation.** Write the coupled descent as
$\dot Z=\gamma_Z F_Z(Z,R)$, $\dot R=\gamma_R F_R(Z,R)$ with
$\varepsilon=\gamma_R/\gamma_Z\to0$. A slow manifold exists if the frozen-$R$ fast
subsystem has, for each $R$ in a compact set, a hyperbolic attracting equilibrium
$Z^\star(R)$ depending smoothly on $R$ (Tikhonov/Fenichel). Nothing in the theory
supplies this: `05b` and the grand-canonical note both update beliefs, rows,
frames, and occupations under *one* functional with independently declared
mobilities, and the existing investigation of the tower found no timescale
separation.

**(H2) Spectral gap.** Uniform hyperbolicity: the frozen-$R$ Jacobian
$\partial_ZF_Z$ satisfies $\mathrm{Re}\,\lambda\le-\kappa<0$ uniformly in $R$. Note
that a *graph* spectral gap is not this: a two-node connection Laplacian has gap
$2c$, independent of the beliefs and arbitrary under rescaling of $c$, so a raw
spectral gap is not an intrinsic agreement scale.

**(H3) Metastability.** With stochastic drive of strength $\epsilon$, the expected
exit time from the basin of a block configuration scales as
$\exp(\Delta\mathcal F/\epsilon)$ (Freidlin–Wentzell / Kramers), where
$\Delta\mathcal F$ is the barrier in the *same* functional being descended.
Persistence over a horizon $T$ therefore requires $\Delta\mathcal F\gg\epsilon\log T$.
This is what "persistent" has to mean; a deterministic gradient flow reaching a
local minimum is not persistence, it is termination.

**(H4) Closure.** For scale-2 blocks one needs the parent family to be invariant
under the induced map: $T_\ell(\mathrm{Ran}\,R_\ell)\subseteq\mathrm{Ran}\,R_{\ell+1}$,
which is exactly the criterion under which the retained beta is exact and the
residual $\delta\beta_\ell$ vanishes. Boundedness and idempotence of the retained
projections do not imply it. And exact closure *generates hyperedges*: eliminating
the center of an Ising star produces $2\cosh(h_0+\sum_rJ_rs_r)$, whose negative log
has cubic coefficient $2\,\mathrm{sech}^2(h_0)\tanh(h_0)J_1J_2J_3+O(J^5)$, nonzero
for all small nonzero $J_r$ with $h_0\ne0$. Pairwise closure is false.

**(H5) Capacity.** Proposition 5 of Part 2: without a declared capacity bound on
$(\mathsf Z_{s+1},K_\downarrow,P_{s+1})$ the tower VFE is exactly constant across
partitions. No dynamics on a constant landscape selects anything.

**(H6) Holonomy admissibility.** Proposition 8: on a cyclic graph one needs
$\mathrm{Fix}(\mathrm{Hol}^x_r)\cap\mathscr M^x_r\ne\varnothing$ for the block, or
the retention alternative must be adopted and the parent must carry the marks.

### 10.5 What can honestly be claimed

Under (H1)–(H6) **and** a declared composite potential of M2 type with
$2Jc\rho_0>a$, the incoherent state is linearly unstable and a coherent block
appears in mean field. That is a CONDITIONAL statement about a proposed functional
under a mean-field reduction, resting on six hypotheses none of which is proved for
the actual coupled system on a generic cyclic graph. Iterating to scale 2
additionally needs (H4) at scale 1, which is where the hyperedge generation above
bites: the scale-1 theory is not pairwise, so the scale-1 "network" on which one
would repeat the argument is not the object the argument assumed.

The honest status of "descent spontaneously produces persistent nested blocks" is
therefore **OPEN**, and this matches the manuscript's own next-theorem statement.

## 11. Q8 — cross-scale natural gradient, semiconjugacy, and time

### 11.1 The coupled stationarity conditions, derived

Two exact coordinate updates fall directly out of Theorem 2 and are the precise
content of "bidirectional coupling under a one-way generative arrow."

**Child update.** Freeze everything except the child conditional
$Q_s(\cdot\mid z_{s+1},R,G,H)$. The terms involving it are its own cross-scale
divergence and whatever it feeds below (the observation likelihood at $s=0$, or the
next cross-scale term at $s>0$). Collecting the latter into
$\mathcal E_s(z_s)$ gives

$$
Q^\star_s(dz_s\mid z_{s+1},\cdot)\ \propto\ K^s_\downarrow(dz_s\mid z_{s+1},\cdot)\,e^{-\mathcal E_s(z_s)} ,
$$

so **the parent kernel acts as the child's prior**.

**Parent update.** Freeze the child *kernel* $Q_s(\cdot\mid z_{s+1},\cdot)$ and
vary $Q_{s+1}$. The only $z_{s+1}$-dependent contribution of the cross-scale term
is the conditional divergence profile

$$
\mathcal V_{s+1}(z_{s+1}):=D_{\rm KL}\big(Q_s(\cdot\mid z_{s+1},\cdot)\,\Vert\,K^s_\downarrow(\cdot\mid z_{s+1},\cdot)\big),
$$

so the parent's coordinate objective is
$\mathbb E_{Q_{s+1}}[\mathcal V_{s+1}]+D_{\rm KL}(Q_{s+1}\Vert P_{s+1})+\text{const}$,
with minimizer

$$
\boxed{\;Q^\star_{s+1}(dz_{s+1})\ \propto\ P_{s+1}(dz_{s+1})\,e^{-\mathcal V_{s+1}(z_{s+1})}\;}
$$

whenever the normalizer is in $(0,\infty)$. **The child's conditional-KL profile
acts as the parent's likelihood.** This is the exact static sense in which a
meta-agent both constrains and is constrained by its sub-agents, with no generative
factor reading a posterior.

### 11.2 Natural gradient on the tower

Let $\phi$ parameterize $\mathbb Q_\phi$ and let $\mathcal G(\phi)$ be the Fisher
metric of the *joint* recognition family. The natural-gradient flow

$$
\dot\phi=-\Gamma\,\mathcal G(\phi)^{-1}\nabla_\phi\mathcal F_{\rm tower},
\qquad
\frac{d}{dt}\mathcal F_{\rm tower}=-\big\Vert\nabla_\phi\mathcal F_{\rm tower}\big\Vert^2_{\Gamma\mathcal G^{-1}}\le0,
$$

is a descent flow for any positive $\Gamma$. The per-scale decomposition

$$
\dot\phi_s=-\gamma_s\,\mathcal G_s(\phi_s)^{-1}\nabla_{\phi_s}\mathcal F_{\rm tower}
$$

is **the same dynamics only when $\mathcal G$ is block diagonal across scales**,
i.e. when
$\mathcal G_{s,s'}=\mathbb E_{\mathbb Q_\phi}[\partial_{\phi_s}\log q_\phi\,\partial_{\phi_{s'}}\log q_\phi]=0$
for $s\ne s'$. Since $\mathbb Q_\phi$ is deliberately *correlated* across scales
(that is the point of §4.1), cross-scale Fisher orthogonality is a substantive
hypothesis and is generically false. With a nondiagonal metric the global natural
gradient mixes scales and independent per-scale inversions are a different flow.
Hard support boundaries (the simplices carrying $\beta,\gamma$, the finite label
pools carrying $R$) additionally require a projected flow, line search, damping, or
an acceptance test. On the open simplex the row block of the natural gradient is
the replicator equation
$\dot\beta_{ij}=-\gamma_i\beta_{ij}(c_{ij}-\sum_k\beta_{ik}c_{ik})$ with
$c_{ij}=\log(\beta_{ij}/\pi_{ij})+\mathbb E_{\mathbb Q}D_{ij}/\tau_i$, whose partial
dissipation is $-\gamma_i\mathrm{Var}_{\beta_i}(c_{ij})\le0$; if the state law
evolves simultaneously its chain-rule term must be added.

### 11.3 The semiconjugacy and lumpability defects

Three different defects, often conflated.

**(a) Deterministic moving-map defect.** For a fine field $V_t$, a $C^1$ moving
coarse map $c_t$, and a candidate coarse field $\overline V_t$,

$$
\delta_t=\partial_tc_t+Dc_t\,V_t-\overline V_t\circ c_t .
$$

The $\partial_tc_t$ term vanishes only for a frozen coarse map, so an *adaptive*
partition is automatically outside exact semiconjugacy unless its motion is
compensated.

**(b) Markov lumpability defect.** For a Borel surjection $c$ and a Markov kernel
$T$, a coarse kernel $T^c$ with $c_\#(\mu T)=(c_\#\mu)T^c$ for **every** $\mu$
exists iff strong lumpability holds, $T(y,c^{-1}B)=T(y',c^{-1}B)$ whenever
$c(y)=c(y')$; $T^c$ is then unique, and a Borel right inverse gives the formula
$T^c(z,B)=T(\varsigma(z),c^{-1}B)$. A natural scalar defect is

$$
\mathrm{lump}(T,c)=\sup_{B\in\mathscr Z}\ \operatorname*{osc}_{\{y:\,c(y)=z\}} T(y,c^{-1}B),
$$

vanishing exactly under strong lumpability. Strong lumpability is the
*every-initial-law* condition and is not necessary for one law: a three-state chain
with $c(1)=c(2)=a$, $c(3)=\beta$, $1\mapsto3$, $2\mapsto\{1,2\}$ uniformly,
$3\mapsto\{1,3\}$ uniformly violates it, yet started at $\delta_3$ the chain never
leaves $\{1,3\}$, on which $c$ is injective, and the coarse process is Markov.
Weak lumpability at a selected initial law is strictly weaker and is the only thing
available when strong lumpability fails.

**(c) Natural-gradient semiconjugacy defect.** This is the one specific to the
present theory and it factorizes into two independent conditions:

$$
\Delta^{\rm ng}:=Dc\big(\mathcal G_{\rm fine}^{-1}\nabla\mathcal F_{\rm fine}\big)
-\big(\mathcal G_{\rm coarse}^{-1}\nabla\mathcal F_{\rm coarse}\big)\circ c .
$$

$\Delta^{\rm ng}=0$ requires **both**

* an *objective* condition: $\mathcal F_{\rm fine}-\mathcal F_{\rm coarse}\circ c$
  must be $c$-measurable, which by the coarse-VFE chain rule of Part 1 §5 says
  precisely that the discarded conditional-information defect $\Delta$ is a function
  of the coarse variable alone; and
* a *metric* condition: horizontal conformality,
  $Dc\,\mathcal G_{\rm fine}^{-1}\,Dc^\top=\lambda\,\mathcal G_{\rm coarse}^{-1}$
  for a positive scalar $\lambda$.

Neither implies the other, and the Fisher-contraction theorem gives only the
*inequality* $I_{\mathsf Y}\preceq I_{\mathsf X}$ with defect
$\mathbb E\,\mathrm{Cov}(\ell\mid Y)$, not conformality. That the manuscript's own
independently recomputed coarse natural-gradient flow satisfies semiconjugacy is
explicitly unproved.

Finally, Fisher equality at one parameter is *local score sufficiency*, not
recovery: with independent Bernoulli coordinates
$\Pr_\theta(A=1)=\tfrac12+\tfrac\theta4$, $\Pr_\theta(B=1)=\tfrac12+\tfrac{\theta^2}4$
and $K$ discarding $B$, the fine and coarse Fisher informations agree at
$\theta=0$ and are nonzero, yet $\Pr_\theta(B=1\mid A)$ depends on $\theta$ so no
parameter-independent reverse kernel recovers the experiment.

### 11.4 Truncation residual, for completeness

Where a retained coupling sector $R_\ell$ is used, the omitted flow is exactly
$\delta\beta_\ell(g)=(I-\widehat R_{\ell+1})\widehat T^{\mathcal G}_\ell(g)/\Delta s_\ell$,
and it vanishes on the whole retained sector iff
$T^{\mathcal G}_\ell(\mathrm{Ran}\,R_\ell)\subseteq\mathrm{Ran}\,R_{\ell+1}$. A beta
functional is also a joint statement about the action *and* the declared reference
trajectory: under a reference change $\rho'=e^{-\Delta}\rho$, $H'=H-\Delta$, the
beta obeys the inhomogeneous law
$\mathfrak B^H_b[H';\rho']=\mathfrak B^H_b[H;\rho]-\mathfrak B^H_b[\Delta;\rho]$,
which is not a linear reparameterization and vanishes only when the increment is
itself a fixed action.

### 11.5 Optimization time versus physical time

The parameter $t$ in $\dot\phi$ is a declared descent parameter. It is not a
coordinate on $\mathcal C$, not RG depth, and not physical time. Passing from a
solution curve to its oriented orbit and measuring that orbit by Fisher length are
separate constructions: a common positive scalar mobility changes only the
parameterization, whereas unequal block rates $\gamma_i$ generally change the orbit.

The resulting Fisher duration $\tau_F(\lambda)=\tau_0+\int_{\lambda_0}^\lambda v_F$
is nondecreasing and invariant under regular orientation-preserving
reparameterization; it is strictly increasing exactly when there is positive
accumulated length on every nontrivial subinterval, and it is a *regular arc-length
coordinate* only if the curve is $C^1$ with $v_F>0$ everywhere. For a curve
confined to one fixed statistical fiber the speed is connection-independent; for a
section-induced curve over a moving base point it is **connection-relative**,
$v_F^\omega=\sqrt{I(\mathrm{ver}^\omega\dot\eta,\mathrm{ver}^\omega\dot\eta)}$, and
no canonical connection is selected anywhere in this theory. A shared scalar clock
across agents additionally needs a closed clock one-form with zero periods on the
region. A physical-time claim would need a named target clock, a calibration map
and uncertainty model, causal and compositional consistency, and discriminating
evidence against alternative parameterizations. None is available.

### 11.6 What is required for sustained nonequilibrium and Wheelerian feedback

Here is the sharpest statement available, and it is a negative one.

**Proposition 10 (a single scalar with symmetric mobility cannot sustain
nonequilibrium).** Let the enlarged variable set $u$ — beliefs, models, rows,
occupations, frames, memberships, *and* any participatory control fields — evolve
as $\dot u=-M(u)\nabla_u\Psi(u)$ with $M(u)$ symmetric positive definite and
$\Psi\in C^1$ a single scalar. Then $\dot\Psi=-\nabla\Psi^\top M\nabla\Psi\le0$,
and by LaSalle's invariance principle every bounded trajectory converges to the
largest invariant subset of $\{\nabla\Psi=0\}$. Adding a participatory feedback of
the form $\mu_{ij}=\mu^{(0)}_{ij}+\lambda M_A(\mathbb Q_A,\boldsymbol\Pi_A)$ does
**not** change this conclusion as long as the enlarged system remains a gradient
flow of one such $\Psi$.

Consequently multistability, hysteresis, and arbitrarily long transients are all
compatible with the flow and none of them is sustained nonequilibrium. To get an
NESS one must break the hypotheses, and there are exactly four ways:

1. **Time-dependent controls.** With driven reservoirs the balance becomes
   $d\mathcal G/dt=-\mathcal D-\sum_{ij}\rho_{ij}\dot\mu_{ij}+(\partial\mathcal G/\partial\tau_E)\dot\tau_E+\text{boundary work}$,
   $\mathcal D\ge0$. Work must be accounted, not asserted.
2. **Nonreciprocity / an antisymmetric sector.** Write the drift as
   $F=-M\nabla\Psi+A$ with $A$ not of gradient form. A nonzero $A$ with nonzero
   circulation produces stationary probability currents. Operationally,
   nonreciprocity here means $\partial F_i/\partial u_j\ne\partial F_j/\partial u_i$
   after symmetrization by $M$ — for the two-channel network the natural source is
   $\Omega_{ij}\ne\Omega_{ji}^{-1}$ together with $\beta_{ij}\ne\beta_{ji}$, i.e.
   genuinely directed influence that is *not* derived from a symmetric energy.
3. **Delay.** $\dot u(t)=F(u(t),u(t-\Delta))$ admits no Lyapunov functional in
   general and supports Hopf bifurcation to sustained oscillation. This is
   mechanism (ii) of §6.2.
4. **Stochastic drive with a non-gradient drift.** For
   $\dot u=F(u)+\sqrt{2\epsilon}\,\xi$, the stationary state has zero probability
   current iff detailed balance holds, which for symmetric constant $M$ means $F$ is
   a gradient. So noise alone on a gradient flow gives an equilibrium Gibbs state,
   not an NESS.

**Wheelerian feedback specifically.** A participatory claim becomes mathematically
substantive only when it (i) declares which parent variables modify which fine
kernels, (ii) accounts for the corresponding work or flux, and (iii) identifies an
observable distinguishing the participatory model from an ordinary hierarchical
latent-variable model. By Proposition 10, a feedback loop that is itself derivable
from the same scalar fails (iii) automatically: it is observationally an ordinary
hierarchical model with a reparameterized potential. The loop must be
**non-integrable** — no scalar $\Psi$ with $F=-M\nabla\Psi$ — and that is the
precise technical content of "participatory."
