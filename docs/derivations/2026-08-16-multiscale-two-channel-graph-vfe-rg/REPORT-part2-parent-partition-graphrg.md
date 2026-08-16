# Multiscale two-channel gauge-network VFE — Part 2
## Parent influence, partition variables, and graph renormalization (Q3, Q4, Q5)

Continues Part 1. Notation and typing as declared there.

## 6. Q3 — three mechanisms for parent influence, and one impossibility

### 6.1 Mechanism (i): top-down generative kernel with bottom-up recognition

The parent enters the generative law only through
$K^s_\downarrow(dZ_s\mid Z_{s+1},R_s,G_s,H_s,X)$, which for a block-factorized
form reads $\prod_{I}K^s_I(dZ^s_I\mid Z_{I,s+1},R_s,G_s,X)$. The parent belief
and model presentations are then arguments of the children's conditional
generative prior. The corresponding exact VFE term is the last group in
Theorem 2,
$\mathcal F^s_{\rm cross}=\mathbb E_{\mathbb Q_\phi}D_{\rm KL}(Q_s\Vert K^s_\downarrow)$.

This mechanism is static, exactly normalized, and needs no partition function.
Its content is the following asymmetry, which is easy to state wrongly.

**The generative arrow is one-way; the optimization is two-way.** Varying the
recognition law with respect to a parent coordinate changes the parent update;
varying it with respect to a child coordinate changes the child update. Both
gradients pass through the *same* term $\mathcal F^s_{\rm cross}$. So a
meta-agent influences its sub-agents without any generative factor reading a
posterior. Part 3 §Q8 derives the two coordinate updates explicitly and shows
that the child's conditional-KL profile acts as the parent's likelihood while the
parent's kernel acts as the child's prior.

Cost: this is not "downward causation in time." It is a statement about the
stationary conditions of one scalar functional.

### 6.2 Mechanism (ii): delayed parent-to-child feedback

Let the inferred parent at descent parameter $t$ modify the child kernel at
$t+\Delta$: $K^{s}_{\downarrow,\,t+\Delta}(\cdot\mid\cdot)=\mathcal K[\,\widehat Z_{s+1}(t)\,]$.
This is a *nonautonomous family of models*, one per time slice, and it is a
dynamical extension rather than a static ELBO identity. Two consequences.

* At each frozen slice the ELBO identity holds for that slice's own joint. Across
  slices, the family $\{\mathbb P_{\theta,\mathbb Q}\}$ selects no member as "the
  model." An increase in a bound certifies improvement relative to one fixed
  reference value exactly when the compared members lie on one level set of
  $e(\mathbb Q)=\log p_{\theta,\mathbb Q}(o\mid X)$
  (`prop:gen-no-distinguished-target`). The stronger claims fail: nonconstant
  dependence of $\mathbb P$ on $\mathbb Q$ does *not* imply that $e$ varies. A
  finite witness: one binary latent, $Q_\beta=\mathrm{Ber}(\beta)$,
  $g(\beta)=\beta/2+1/4$, $P_{\theta,Q_\beta}(o,y)=\tfrac12\mathrm{Ber}(g(\beta))(y)$
  — the joint varies injectively with $\beta$ while $e(Q_\beta)=\log(1/2)$ for
  every $\beta$ (`prop:gen-moving-target-witness`).
* The delay breaks the same-slice cycle, which is exactly why it works. It buys a
  genuine dynamical system at the price of losing the single-scalar Lyapunov
  structure; see Part 3 §Q8 for what that buys and costs.

### 6.3 Mechanism (iii): normalized undirected reciprocal Gibbs factor

Replace both arrows by one symmetric compatibility factor
$\psi_s(Z_s,Z_{s+1})\ge0$ and define
$p^{\rm Gibbs}_\theta(o,W\mid X)=Z_X^{-1}\Psi_X(o,W)$ with
$Z_X=\int\Psi_X\,d\mu_W$. This is the only one of the three that supports genuine
**same-time reciprocal** influence.

Its price is a model-existence condition, not a formality:
$0<Z_X<\infty$ must be **proved**. Normalized node potentials plus an everywhere
positive, finite, continuous edge potential do not suffice
(`prop:gen-gibbs-counterexample`). On a finite categorical state space $Z_X<\infty$
is automatic, which is one more reason the falsification design of Part 4 is
finite and categorical.

### 6.4 Why (i) with a deterministic pushforward and an independent same-time parent cannot both be imposed

This is the impossibility the problem statement asks about. State it as five
separate facts, because they fail for five different reasons.

**Proposition 3.** Let $\mathsf Y,\mathsf Z$ be standard Borel, $C:\mathsf Y\to\mathsf Z$
Borel, and consider a joint $\mathbb P$ on $\mathsf Y\times\mathsf Z$ with
marginals $\nu=\mathbb P^Y$, $P_1=\mathbb P^Z$.

**(a) A deterministic parent is a statistic, and its prior is not free.**
If $\mathbb P(\{Z=C(Y)\})=1$ then $\mathbb P(dy,dz)=\nu(dy)\delta_{C(y)}(dz)$,
hence $P_1=C_\#\nu$ necessarily. Writing the same measure in the top-down order
gives $\mathbb P(dy,dz)=P_1(dz)\,\nu_z(dy)$ where $\nu_z$ is the disintegration of
$\nu$ over $C$, concentrated on $C^{-1}(z)$ for $P_1$-a.e. $z$. So a top-down
kernel $K_\downarrow$ compatible with the deterministic constraint exists, but it
is *forced* to be that fiber disintegration, and $P_1$ is *forced* to be $C_\#\nu$.

**(b) Such a parent supplies no conditional randomness.** Under (a),
$\sigma(Z)\subseteq\sigma(Y)$ modulo $\mathbb P$-null sets,
$\mathbb E[g(Z)\mid Y]=g(C(Y))$ a.s. for every bounded measurable $g$, and (in the
discrete case) $H(Z\mid Y)=0$, $I(Y;Z)=H(Z)$. The parent adds nothing that is not
already a function of the children. "Downward influence" is then vacuous: varying
$z$ off $\mathrm{ran}(C)$ is a null operation, and varying it inside
$\mathrm{ran}(C)$ is the same as varying a function of the children.

**(c) Demanding a freely declared parent prior overdetermines the model.** If
$P_1$ is a declared model parameter rather than something read off the children,
consistency with (a) requires the functional constraint $C_\#\nu=P_1$ on the child
marginal. That is one equation, not a free choice, and it generically fails. In
particular one cannot simultaneously (1) declare $P_1$, (2) declare a top-down
$K_\downarrow$ with support strictly larger than the fibers of $C$, and (3) impose
$Z=C(Y)$ a.s.

**(d) A hard deterministic constraint kills a Gibbs density against a nonatomic
reference.** Suppose additionally that $\mathbb P$ is to be written as
$Z_\psi^{-1}\psi(y,z)\,(\mu\otimes\lambda)(dy,dz)$ with $\lambda$ nonatomic on
$\mathsf Z$. Concentration on the graph $\Gamma_C=\{(y,C(y))\}$ forces $\psi=0$
off $\Gamma_C$ up to null sets; but by Fubini each slice $\{C(y)\}$ is
$\lambda$-null, so $\Gamma_C$ is $(\mu\otimes\lambda)$-null and
$Z_\psi=\int\psi\,d(\mu\otimes\lambda)=0$. The Gibbs model is not normalizable.
Hence a same-time reciprocal factor cannot be combined with an exact
deterministic pushforward against a nonatomic reference; it can only be combined
with a *soft* constraint $\psi=e^{-\lambda\,d(z,C(y))^2}$, which is a different
model with a different (and still unproved) $Z_\psi$.

**(e) The structural reason: a directed 2-cycle at one time slice.** Imposing
both $Y\to Z$ (deterministic map, as a generative factor) and $Z\to Y$ (kernel
$K_\downarrow$, as a generative factor) puts two directed generative arrows
between the same two variables at the same slice. The ordered-kernel composition
of §3.3 is defined only along a topological ordering; with a 2-cycle there is
none, and no normalized directed joint is produced. This is not a technicality
about proofs — it is the reason Proposition 1's normalization argument evaporates.

**The trichotomy.** There are exactly three normalized repairs, and they are
mechanisms (i)–(iii):

1. Keep $K_\downarrow$ generative and demote $C$ to a **recognition or coarse
   channel** (bottom-up, acting on measures). Then $C$ is not a generative factor
   and there is no cycle. This is the theory's actual choice.
2. Break the cycle **in time** (mechanism (ii)). Reciprocity becomes sequential.
3. Replace both arrows by **one** undirected factor with a proved finite
   normalizer (mechanism (iii)). Reciprocity becomes simultaneous but the price is
   $Z_X$.

Nothing else is available. In particular, "the parent is a deterministic function
of its children *and* an independent cause of them" is not a fourth option; by
(a)–(b) it degenerates, by (c) it is generically inconsistent as a declared model,
by (d) it destroys any Gibbs presentation, and by (e) it has no directed
normalization at all.

## 7. Q4 — partition variables inside the probabilistic model

### 7.1 Where they live

$R_s=(R^b_s,R^m_s)$ is generated by $P^s_R(\cdot\mid Z_{s+1},G_{s+1},X)$ in the
joint of §3.2 and inferred by $Q^s_R$ in the recognition disintegration of §4.1.
Concretely, take the categorical case $R^x_s\in(\Lambda^x_{s+1})^{V_s}$ (a
function assigning each fine node to a label), or the independent-Bernoulli case
$n_{iA}\in\{0,1\}$ for overlapping parents. Both are **finite** state spaces at
each scale, so any Gibbs prior on them normalizes automatically:
$P^s_R(R)=\Pi_R(R)e^{-E_{\rm block}(R)}/\sum_{R'}\Pi_R(R')e^{-E_{\rm block}(R')}$
with the sum finite and positive whenever $E_{\rm block}>-\infty$. This is the
one place in the theory where a Gibbs factor is safe without a separate proof.

### 7.2 The variational update, derived

Collect the terms of $\mathcal F_{\rm tower}$ in which $R_s$ appears. From
Theorem 2 these are the $R$-term itself and, through their conditioning, the $G$,
$H$, and cross-scale terms. Define, at frozen values of all other coordinates,

$$
U_s(R):=D_{\rm KL}\big(Q^s_G(\cdot\mid Z_{s+1},R)\Vert P^s_G(\cdot\mid Z_{s+1},R)\big)
+\mathbb E_{Q^s_G}\Big[
D_{\rm KL}\big(Q^s_H\Vert P^s_H\big)
+\mathbb E_{Q^s_H} D_{\rm KL}\big(Q_s\Vert K^s_\downarrow\big)\Big].
$$

Then the $R_s$-dependent part of the tower VFE at frozen everything else is

$$
\mathcal F[Q^s_R]=\mathbb E_{Q^s_R}\big[U_s(R)\big]+D_{\rm KL}\big(Q^s_R\Vert P^s_R\big).
$$

**Proposition 4 (partition update).** If
$\mathcal Z_R:=\sum_{R}P^s_R(R)\,e^{-U_s(R)}\in(0,\infty)$ then $\mathcal F[Q^s_R]$
has the unique minimizer

$$
\boxed{\;Q^{s\star}_R(R)=\frac{P^s_R(R)\,e^{-U_s(R)}}{\mathcal Z_R}\;}
\qquad\text{with minimum value}\qquad -\log\mathcal Z_R .
$$

*Proof.* $\mathcal F[Q]=D_{\rm KL}(Q\Vert P^{\star})-\log\mathcal Z_R$ where
$P^\star(R)\propto P^s_R(R)e^{-U_s(R)}$, by direct expansion; relative entropy is
nonnegative and vanishes only at $Q=P^\star$. For a finite label pool the
normalizer is a finite sum of nonnegative terms, positive as soon as $U_s<+\infty$
somewhere on the support of $P^s_R$. $\square$

Three things follow that the problem statement's `eq:full-graph-partition-free-energy`
does not make visible.

* **The temperature is not free.** The exact ELBO coordinate update has
  $\tau_R=1$. Writing $\mathbb E_{Q_R}[E_{\rm block}]+\tau_R D_{\rm KL}(Q_R\Vert\Pi_R)$
  with $\tau_R\ne1$ is $\tau_R$ times the ELBO sector for the *rescaled* energy
  $E_{\rm block}/\tau_R$. Same argmin, different value, and it is an exact ELBO
  sector only for the correspondingly tempered generative law. If a tower VFE is
  reported as a number, mixing $\tau_R\ne1$ sectors into it is an accounting error.
* **The block energy is not free either.** $U_s$ is *derived*: it is exactly the
  sum of conditional divergences that the choice of $R$ controls. Any hand-written
  "internal mismatch versus boundary retention versus evaluator closure" trade-off
  is a *proposal for* $U_s$, and it is only an ELBO sector if it equals the
  displayed $U_s$ for a declared $P^s_G,P^s_H,K^s_\downarrow$.
* **The prior is label-natural if it is exchangeable.** The Ewens/CRP prior on set
  partitions,
  $P^s_R(\pi)=\vartheta^{|\pi|}\prod_{B\in\pi}(|B|-1)!\big/\vartheta^{(n)}$ with
  $\vartheta^{(n)}=\vartheta(\vartheta+1)\cdots(\vartheta+n-1)$, is exactly
  normalized, exchangeable, and projective in $n$. Exchangeability gives it the
  relabeling naturality $S(P\cdot X)=PS(X)Q^\top$ demanded of any admissible
  partition selector (`eq:cg-partition-naturality`).

### 7.3 The degeneracy problem, and why priors alone cannot fix it

Now the substantive point. **The tower VFE by itself ranks no partition.**

**Proposition 5 (partition degeneracy without a capacity restriction).**
Fix $S=1$ and a flat model $\mathbb P^{\rm flat}(do,dZ_0\mid X)$ with evidence
$p^{\rm flat}(o\mid X)\in(0,\infty)$. Suppose the parent space and the downward
kernel family are unrestricted, in the sense that for each candidate partition
$R$ one is permitted to take $\mathsf Z_{1,I}:=\mathsf Y_{0,I}=\prod_{i\in I}\mathsf Y_{0,i}$,
$K^0_I(dz_{0,I}\mid z_{1,I}):=\delta_{z_{1,I}}(dz_{0,I})$, and
$P_1:=\mathbb P^{\rm flat,Z_0}$. Then for every partition $R$ — including
all-singleton and all-in-one-block —

$$
\min_{\mathbb Q_\phi}\mathcal F^{(R)}_{\rm tower}=-\log p^{\rm flat}(o\mid X),
$$

a value independent of $R$. In particular the cross-scale divergence
$\mathbb E\,D_{\rm KL}(Q_0\Vert K^0_\downarrow)$ is zero at the optimum for every
$R$, and the VFE induces no preference among partitions whatsoever.

*Proof.* The stated data give
$\mathbb P^{(R)}(do,dz_0,dz_1\mid X)=P_1(dz_1)\,\delta_{z_1}(dz_0)\,L_\theta(do\mid z_0,X)$,
whose $(o,Z_0)$-marginal is $\mathbb P^{\rm flat}$ for every $R$; note
$\prod_I\delta_{z_{1,I}}=\delta_{z_1}$, so the block factorization
`eq:full-graph-downward-kernel` is respected by every partition. Hence
$p^{(R)}_\theta(o\mid X)=p^{\rm flat}(o\mid X)$ for every $R$. The minimum of
$\mathcal F=-\log p+D_{\rm KL}(\mathbb Q\Vert\boldsymbol\Pi)$ over all $\mathbb Q$
is $-\log p$, attained at $\mathbb Q=\boldsymbol\Pi$. $\square$

**Corollary 6 (selection is entirely in the declared restrictions).** Under the
hypotheses of Proposition 5, $R\mapsto\min_{\mathbb Q}\mathcal F^{(R)}_{\rm tower}$
is constant, so the minimizing $Q^{\star}_R$ of Proposition 4 reduces to
$Q^{\star}_R=P^s_R$: the inferred partition is the prior, and the data contribute
nothing. Any nondegenerate hierarchy claim therefore rests on a **declared
capacity restriction**, not on the variational principle.

This is the proof of the assertion in `07c` that "no canonical selector follows
from the global VFE alone," and it sharpens it: the failure is not that the VFE is
weakly informative about partitions, but that under an unrestricted parent it is
*exactly* uninformative.

**What actually prevents each degeneracy.** With Proposition 5 in hand the
requirements can be named precisely.

*Against all-in-one-block.* One needs the parent to be genuinely unable to
represent the children's joint law. That requires a **capacity bound**: a fixed
parent space $\mathsf Z_{s+1,I}$ whose "size" (cardinality for finite spaces,
dimension for smooth ones, or a declared parametric family for $K^s_\downarrow$)
does not grow with $|I|$. Then a large block pays a strictly positive
$\mathbb E\,D_{\rm KL}(Q_s\Vert K^s_\downarrow)$ that increases with $|I|$. This
is a **modeling hypothesis and must be declared**; it does not follow from the
gauge geometry or from the ELBO.

*Against all-singleton.* One needs a strictly positive **cost per parent node**.
Two clean ways to put it inside the model: (α) let $P^s_R$ charge for block count
(a CRP with small $\vartheta$, or an explicit $\kappa^{|\pi|}$ factor); (β) let
the top prior $P_S$ and the graph prior $P^s_G$ carry a per-node term, so that the
divergences $D_{\rm KL}(Q_S\Vert P_S)$ and $\mathbb E D_{\rm KL}(Q^s_G\Vert P^s_G)$
grow with $|V_{s+1}|$. Route (β) is preferable because it keeps the cost in the
same currency as the rest of the tower.

*Why no exchangeable prior alone suffices.* Any $P^s_R$ that is strictly positive
at both extremes merely reweights them; with $\vartheta=1$ the CRP gives
$P(\text{all singletons})=1/n!$ and $P(\text{one block})=1/n$, so it prefers the
coarse degeneracy rather than excluding either. Since by Corollary 6 the data
contribute nothing without a capacity bound, the posterior over partitions is
*exactly* the prior, and a prior cannot by itself make a nondegenerate partition
the unique minimizer unless it is constructed to be maximized there — which is
assuming the answer. **Both a capacity restriction and a node-count cost are
necessary; neither alone is sufficient.**

## 8. Q5 — graph RG by pushing $(\eta^b,\eta^m)$ and disintegrating parent rows

### 8.1 The rule

Rows are conditional laws and cannot be coarse-grained on their own. The
coarse-grainable object is the **joint directed edge-event law**

$$
\eta^{b}_{ij}=\alpha^b_i\beta_{ij},\qquad
\eta^{m}_{ij}=\alpha^m_i\gamma_{ij},\qquad
\sum_{i,j}\eta^x_{ij}=1,
$$

which is a probability law on ordered pairs and, by construction, a family of
**gauge-invariant scalars**. Declare a normalized endpoint kernel
$K^x(A,B\mid i,j)$ per channel, supported on the declared membership incidences
($K^x(A,B\mid i,j)>0\Rightarrow C^x(A\mid i)>0$ and $C^x(B\mid j)>0$). Then

$$
\boxed{\;
\eta^{x,c}_{AB}=\sum_{i,j}\eta^x_{ij}\,K^x(A,B\mid i,j),
\qquad
\alpha^{x,c}_A=\sum_B\eta^{x,c}_{AB},
\qquad
\beta^{c}_{AB}=\frac{\eta^{x,c}_{AB}}{\alpha^{x,c}_A}\ \ \text{on }\{\alpha^{x,c}_A>0\}. \;}
$$

Push the joint, then disintegrate. This is normalized, needs no parent root, and
is the direct-sum specialization when $K^x=C^x\otimes C^x$ and the memberships are
hard: $\eta^{c}_{IJ}=\sum_{i\in I}\sum_{j\in J}\eta_{ij}$.

**Why $\eta$ and not $\beta$.** The renormalizability criterion that the network-RG
literature isolates is that the *defining parameter must be additive under
aggregation* — this is the content of the Garuccio–Lalli–Garlaschelli failure
taxonomy (arXiv:2009.11024, §II.6), which is why the configuration model, the
degree-corrected SBM, and preferential attachment are not renormalizable. Here
$\eta$ is additive under blocking and $\beta$ is not. The theory's choice to push
the event law is therefore exactly the MSM-consistent choice, arrived at
independently.

### 8.2 Counterexample: row averaging is not event-law pushforward

Take $V=\{1,2,3\}$, $\alpha=(0.9,\,0.1,\,0)$, and the rows
$\beta_1=(0,0,1)$, $\beta_2=(1,0,0)$, $\beta_3=(0,0,1)$. Block $I=\{1,2\}$,
$J=\{3\}$. Then $\eta_{13}=0.9$, $\eta_{21}=0.1$, all other $\eta_{ij}=0$, so

$$
\eta^c_{II}=0.1,\quad \eta^c_{IJ}=0.9,\quad \alpha^c_I=1,\qquad
\beta^c_{II}=0.1,\quad \beta^c_{IJ}=0.9 .
$$

Uniform row averaging over the block gives instead
$\bar\beta_I=\tfrac12(0,0,1)+\tfrac12(1,0,0)=(0.5,0,0.5)$, hence
$\beta^{\rm naive}_{II}=0.5$, $\beta^{\rm naive}_{IJ}=0.5$. The discrepancy is
$0.4$ in each entry and can be driven to $1$ by skewing $\alpha$. Averaging rows
with any weights other than the receiver-occupancy weights $\alpha_i/\alpha_I$ is
wrong, and after conditioning on the observation record even those are wrong: the
correct receiver weights become the **evidence-weighted**
$\alpha'_i(y)=a_{i\mid I}c_i(o_i,y)Z_i(y)\big/W_I(y)$
(`eq:rg-attention-evidence-weights`), with $\alpha'_i=a_{i\mid I}$ exactly when
$c_i(o_i,y)Z_i(y)$ is constant on the conditional support in $I$.

### 8.3 Directed graphs, cycles, zero weights

*Directedness.* Nothing in the rule uses symmetry: $\eta^x$ is a law on **ordered**
pairs and $K^x(A,B\mid i,j)$ need not be symmetric in $(A,B)$ or in $(i,j)$. No
reversibility, no undirected substrate, and no acyclicity of the interaction
skeleton is used. Cycles in the skeleton are irrelevant to this step; they matter
only for the marks (Part 3 §Q6).

*Zero weights.* Three distinct situations must be separated.
(1) $\eta^x_{ij}=0$ on a fine edge: that edge contributes nothing and its
transport mark is never sampled, so its holonomy is not retained; but the edge may
still exist in the skeleton and may acquire mass later under descent.
(2) $\alpha^{x,c}_A=0$: the parent row $\beta^c_{A\cdot}$ is an arbitrary version
of a conditional on a null event. Any two constructions agree $\eta^{x,c}$-almost
surely and may disagree pointwise, so **no pointwise statement about a
zero-occupancy parent row is an invariant of the coarse law**. Removing such a
parent from the effective support is legitimate; assigning it a "default uniform
row" is a fabrication that will silently propagate at the next scale.
(3) $\alpha^{x,c}_A=0$ does **not** mean the parent node is absent: a node may
carry belief and model coordinates with zero receiver occupancy. Node existence
and edge-event mass are different data and are generated by different factors
($P^s_R$ and $P^s_G$ respectively).

*Overlaps.* Soft normalized memberships $C^x(A\mid i)\ge0$, $\sum_AC^x(A\mid i)=1$
preserve total mass and permit a child to belong partially to several parents. A
literal **replicated cover** with $R(A\mid i)\in\{0,1\}$ and several ones is *not*
a Markov kernel: its column sums exceed one, and in the simplest two-parent
example one fully replicated child gives total mass $2$. Treating a replicated
cover as normalized doubles child mass and every incident event contribution. This
is the exact boundary between "overlapping soft memberships" (certified) and
"full membership in several parents" (not certified).

*Endpoint independence.* The product form $K^x=C^x\otimes C^x$ encodes the
hypothesis that the receiver and source assignments are conditionally independent
given the fine edge. This must be **declared**, not assumed. It fails, for
instance, when $i=j$ (a self-loop cannot land in two different parents) and when a
shared child is assigned by a coupled rule. Otherwise supply a correlated
$K^x(A,B\mid i,j)$.

### 8.4 Distinct belief and model partitions

Apply the rule separately with $K^b$ and $K^m$. If $C^b\ne C^m$ then in general
$V^b_{s+1}\ne V^m_{s+1}$ and there is **no single parent node set**.

**Proposition 7 (two-channel parent requires a declared correspondence).** A
scale-$(s+1)$ agent is, by the typing of §3.1, a triple
$(q^b_A,q^m_A,\xi_A)$ together with an evaluator
$\mathrm{ev}_A:\mathsf M_A\to\mathrm{Kern}(\boldsymbol\Xi_A,\mathsf B_A\times\mathsf O\times\mathsf H_A)$.
The evaluator's domain and codomain must be indexed by the *same* label. Hence if
$C^b\ne C^m$, a two-channel parent exists only under one of:
(1) $C^b=C^m$ (common partition);
(2) a declared normalized correspondence kernel
$J:\Lambda^b_{s+1}\rightsquigarrow\Lambda^m_{s+1}$, in which case the parent's
model presentation is $\int J(A^m\mid A^b)\,q^m_{A^m}$ and the evaluator is
defined on the mixture — this is a further coarse channel whose conditional KL
appears in $\mathcal F_{\rm tower}$;
(3) working on the **common refinement** $\Lambda^b_{s+1}\times\Lambda^m_{s+1}$,
which is always available but generally produces many low-occupancy parents.

*Counterexample (N4).* $V=\{1,2,3,4\}$; $C^b$ blocks as $\{1,2\},\{3,4\}$; $C^m$
blocks as $\{1,3\},\{2,4\}$. The common refinement is the four singletons, so
options (1) and (3) both collapse the intended coarse-graining: (1) is
unavailable and (3) achieves no coarsening at all. Only option (2), a declared
correspondence, produces a genuine two-channel parent, and it is not free — it is
extra model structure carrying its own divergence term. The lesson is that
independently optimized belief and model partitions do not compose into a
hierarchy; the coupling must be inside $P^s_R$ from the start, which is why §3.2
generates $(R^b_s,R^m_s)$ from one joint factor.

### 8.5 Nested composition

Memberships compose as normalized kernels,
$C_{20}(B\mid i)=\sum_AC_{21}(B\mid A)C_{10}(A\mid i)$, and endpoint kernels
compose as
$K_{20}(B,B'\mid i,j)=\sum_{A,A'}K_{21}(B,B'\mid A,A')\,K_{10}(A,A'\mid i,j)$.
Two warnings.

* **Product form is not preserved by composition unless independence holds at every
  stage.** $K_{21}=C_{21}\otimes C_{21}$ and $K_{10}=C_{10}\otimes C_{10}$ give
  $K_{20}=C_{20}\otimes C_{20}$ only when the intermediate assignments $(A,A')$ are
  conditionally independent given $(i,j)$. Coarse-graining a graph that has already
  been coarse-grained typically correlates them.
* **Marked closure needs nested trees.** With retained holonomy the coarse state is
  root-framed, so composition of the dressed transports requires the inter-root
  compatibility $\tau^{x,02}_{A\leftarrow i}=\sigma^{x,12}_{A\leftarrow I}\tau^{x,01}_{I\leftarrow i}$
  and the weight compatibility $w^{02}_{Ai}=w^{12}_{AI}w^{01}_{Ii}$
  (`eq:rg-linear-nested-compatibility`). Nested forests alone do not imply either
  equality. Without them the two-step and one-step constructions differ by a
  Nielsen-transformation ambiguity in the holonomy presentation.

### 8.6 What this is and is not

Pushing $\eta$ and disintegrating gives a **consistent family of coarse-grainings**
with an exact composition law. It does **not** give a renormalization *group*. The
project's own status page states this without hedging: there is no rescaling or
identification map $I_b$, no beta function, no blocking ratio, no
relevant/irrelevant operator classification, and the only "fixed point" named is
the base point $c_\*$, which is a chosen location and not a fixed point of a flow
(`solid_RG_theory.md` §11). A genuine RG step requires the pair $(C_b,I_b)$ with
$K_b=C_bI_b$ satisfying $K_{b_1b_2}=K_{b_1}K_{b_2}$ after canonical
identifications (`eq:rg-kernel-semigroup`); the closure theorem
`thm:rg-complete-effective-theory` *assumes* such rescaling kernels among its
hypotheses. Constructing $I_b$ for a directed two-channel gauge network is open.
