# Multiscale two-channel gauge-network VFE — Part 1
## Physicist-facing statement, architecture, and the typed construction (Q1, Q2)

Companion parts: Part 2 (Q3–Q5), Part 3 (Q6–Q8), Part 4 (Q9–Q10, claim table,
strongest theorem, obligations, simulation program). Resume ledger: `PROGRESS.md`.

Author model: Claude Opus 5. No cross-model verifier was dispatched (the session
prohibits subagents), so nothing in this document carries a verification state
beyond derivation-in-text. See Part 4 §Scope for what that costs.

## 1. The full VFE, stated for a physicist

There is exactly one free energy. Fix structural data $X$ (the graph skeleton,
the design incidence, the base point $c_\*$), fix an admitted observation record
$o$ with strictly positive finite evidence density, and fix a finite scale depth
$S$. Let $W$ collect **every** random object the multiscale model retains:
belief presentations and model presentations at scales $0,\dots,S$; the directed
weights $\beta,\gamma$; the receiver occupancies $\alpha^b,\alpha^m$; the edge
occupations; the two channels' transports $\Omega^b,\Omega^m$; the membership
(partition) variables; the retained holonomy marks; and any auxiliary latents.

Declare **one** normalized generative kernel $\mathbb P_\theta(do,dW\mid X)$,
fixed before recognition ever runs, and **one** normalized recognition kernel
$\mathbb Q_\phi(dW\mid o,X)$, which is a correlated joint law and not a product
of marginals. Write $\boldsymbol\Pi_{\theta,o,X}$ for the selected posterior
version. Then

$$
\boxed{\;
\mathcal F^{\rm ext}_{\rm tower}[\mathbb Q_\phi;X,o]
= -\log p_\theta(o\mid X)
+ D_{\rm KL}\!\left(\mathbb Q_\phi(\cdot\mid o,X)\,\middle\Vert\,\boldsymbol\Pi_{\theta,o,X}\right)
\;}
$$

as an identity in $\mathbb R\cup\{+\infty\}$, equivalently
$\mathcal F_{\rm tower}=\mathbb E_{\mathbb Q_\phi}\log\frac{q_\phi(W\mid o,X)}{p_\theta(o,W\mid X)}$
on the finite-density domain. This is `eq:full-graph-vfe-global` of
`Theory/07c_full_graph_meta_agent_vfe.tex`, and it is the whole object.

What a physicist should take from this. The evidence term $-\log p_\theta(o\mid X)$
is the true ground-state energy of the record: it is fixed once the generative
model and the observation are fixed, and no amount of variational work moves it.
The divergence term is the only thing descent can lower, and it is a single
relative entropy between two joint laws on a very large product space. Every
familiar-looking piece — a self term, an edge term, a partition term, a
parent–child term, a "connection regularizer" — is legitimate **only** as an
accounting split of that one divergence, obtained by factorizing $\mathbb P$ and
$\mathbb Q$ along a common ordering. A sum of such pieces that was not obtained
that way is a composite descent potential. It may be a perfectly good objective;
it is not an evidence bound, it does not inherit the $\mathcal F\ge-\log p$
floor, and its stationary points carry no Bayesian interpretation.

Two consequences deserve emphasis before any construction.

**The normalizer count.** Because every factor below is a normalized Markov
kernel of finite scope, the tower carries **no partition function at all**: the
only normalizer in the whole theory is the evidence $p_\theta(o\mid X)$. This is
not a stylistic preference. Local normalization of node and edge potentials does
not give a finite global normalizer: with standard Gaussian node potentials on
$\mathbb R^2$ and the everywhere positive finite continuous edge potential
$\psi_{12}(y_1,y_2)=e^{cy_1y_2}$, $c\ge1$, the exchange-precision matrix
$\begin{psmallmatrix}1&-c\\-c&1\end{psmallmatrix}$ has eigenvalue $1-c\le0$ and
$Z_X=+\infty$ (`prop:gen-gibbs-counterexample`). Any same-time reciprocal
cross-scale factor reintroduces exactly this obligation.

**The typing prohibition.** No generative factor may read the recognition law,
its marginals, its parameters, or the posterior it is supposed to determine
(`req:gen-typing-prohibition`). If one does, the "model" becomes a
$\mathbb Q$-indexed family $\mathbb P_{\theta,\mathbb Q}$ and no member is
distinguished; the ELBO identity still holds for each frozen member, but a
divergence decrease certifies improvement only across members lying on one level
set of $e(\mathbb Q)=\log p_{\theta,\mathbb Q}(o\mid X)$
(`prop:gen-no-distinguished-target`).

### 1.1 The typing fork in $D^b_{ij}$, and why it decides everything

The problem statement gives

$$
D^b_{ij}=D_{\rm KL}\!\left(q^b_i\,\middle\Vert\,(\Omega^b_{ij})_\#q^b_j\right),
\qquad
D^m_{ij}=D_{\rm KL}\!\left(q^m_i\,\middle\Vert\,(\Omega^m_{ij})_\#q^m_j\right),
$$

without saying what kind of object $q^b_i$ is. There are two readings and they
give different theories. This is the single most load-bearing distinction in the
whole problem, and it is where most confusions about "is the row free energy part
of the ELBO" originate.

**Reading A (state-level; ELBO-legitimate).** The agent's latent random variable
*is* a law: $y_i$ has a component $q^b_i\in\mathsf B_i\subseteq\mathcal P(\mathsf Z^b)$,
a point of the associated-bundle fiber $(\mathcal E_b)_{c_i}$. This is explicitly
permitted by `hyp:local-interaction-kernels`: "its state may contain a belief-law
point in $(\mathcal E_b)_{c_i}$." The typing is sound: for standard Borel
$\mathsf Z^b$, realize it as Polish; then $\mathcal P(\mathsf Z^b)$ with the weak
topology is Polish (Kechris, *Classical Descriptive Set Theory*, Thm. 17.23) and
its Borel structure does not depend on the compatible Polish topology, so
$\mathcal P(\mathsf Z^b)$ is standard Borel and may be used as an agent state
space. Under Reading A, $D^b_{ij}$ is a measurable **function of the sample**
$y=(q^b_1,\dots,q^b_N,\dots)$, so it may legitimately appear inside a generative
likelihood factor. It reads no recognition law.

**Reading B (recognition-marginal; composite).** $q^b_i$ *is* the belief marginal
of $\mathbb Q_\phi$, i.e. $q^b_i=(\mathrm{pr}^b_i)_\#\mathbb Q_\phi$
(`def:prob-recognition-marginals`). Then $D^b_{ij}$ is a **functional of the
recognition law**. Inserting it into a generative factor violates the typing
prohibition. Whatever is assembled from it is a composite free-energy potential.

Reading B is what the grand-canonical note uses
(`Theory/grand_canonical_meta_agent_formation.tex`, Eq. `eq:canonical-agent-vfe`
and `eq:transported-divergence`), and that document is correspondingly careful:
it calls $\mathcal G$ a *proposed addition* whose identification with physical
thermodynamics is open, never an evidence bound. Reading A is what
`prop:obs-attention-elbo` uses, and there the row free energy really is an exact
ELBO sector — but with a modification the problem statement omits, derived next.

### 1.2 What the row free energy actually is under Reading A

Under Reading A the row free energies are recovered as follows, and the
derivation fixes their status precisely. Augment the fixed generative baseline by
a latent **source label** $J_i$ for each receiving agent, drawn from a fixed
reference row $\pi_i$ independently of the state,
$P_0^{\rm aug}(dy,dj)=P_0^Y(dy)\prod_i\pi_i(dj_i)$, and let the interaction
record density carry the source-dependent energy
$\ell_i(o_i\mid y,J_i=j)=c_i(o_i,y)\exp[-D_{ij}(y)/\tau_i]$ with $c_i$
independent of $j$, subject to the label-exclusivity hypothesis that the full
augmented likelihood factors as
$L^{\rm aug}_o(y,j)=L^Y_o(y)\prod_i c_i(o_i,y)e^{-D_{ij_i}(y)/\tau_i}$ with no
other factor reading any $J_i$. Then (`prop:obs-attention-elbo`):

* the **generative posterior row at a fixed state** is
  $\beta^P_{ij}(y)=\pi_{ij}e^{-D_{ij}(y)/\tau_i}\big/\sum_k\pi_{ik}e^{-D_{ik}(y)/\tau_i}$;
* if the recognition law is additionally restricted so that every label row is
  independent of $y$ and of the other labels, the exact categorical contribution
  of row $i$ to the collective VFE is
  $-\mathbb E_{Q_Y}\log c_i(o_i,Y)+\mathcal F^{\rm att}_i(\beta^Q_i)$ with
  $\mathcal F^{\rm att}_i(\beta_i)=D_{\rm KL}(\beta_i\Vert\pi_i)+\tau_i^{-1}\sum_j\beta_{ij}\mathbb E_{Q_Y}D_{ij}$,
  whose unique interior minimizer is
  $\beta^{Q\star}_{ij}=\pi_{ij}e^{-\mathbb E_{Q_Y}D_{ij}/\tau_i}\big/\sum_k\pi_{ik}e^{-\mathbb E_{Q_Y}D_{ik}/\tau_i}$.

So the object $\Phi^b_i=\sum_j\beta_{ij}D^b_{ij}+\tau^b_i D_{\rm KL}(\beta_i\Vert\pi^b_i)$
is exactly $\tau_i\mathcal F^{\rm att}_i$ **with $D_{ij}$ replaced by
$\mathbb E_{Q_Y}D_{ij}$**, and it is an exact sector of one collective VFE under
Reading A plus label exclusivity plus the constant-row recognition restriction.
Three qualifications follow immediately and none is optional.

1. **The energy is an expectation, not a value.** Writing $\Phi_i$ with the bare
   $D_{ij}$ is correct only if $D_{ij}$ is deterministic under $\mathbb Q$ — that
   is, only in the degenerate case where the recognition law puts a point mass on
   the belief-law coordinates. Otherwise the correct energy is
   $\mathbb E_{\mathbb Q}D_{ij}$, and using $D_{ij}(\mathbb E_{\mathbb Q}Y)$ or
   $D_{ij}$ evaluated at the recognition marginal is a different (Reading B)
   object.
2. **The two softmaxes are different.** In general
   $\beta^{Q\star}_i\ne\mathbb E_{Q_Y}[\beta^P_i(Y)]$; they agree pointwise
   exactly when all differences $D_{ij}(Y)-D_{ik}(Y)$ are $Q_Y$-a.s. constant.
   "Average the posterior softmax over the recognition law" is a shortcut failure.
3. **Correlated rows retain a total-correlation term.** Merely requiring each row
   marginal to be independent of $y$ does not license the row functional. For an
   arbitrary $Q(dy,dj)=Q_Y(dy)Q_{J\mid Y}(dj\mid y)$ the exact label contribution
   is
   $-\sum_i\mathbb E_{Q_Y}\log c_i+\mathbb E_{Q_Y}\mathrm{TC}(Q_{J\mid Y})
   +\sum_i\mathbb E_{Q_Y}[D_{\rm KL}(Q_{J_i\mid Y}\Vert\pi_i)+\tau_i^{-1}\mathbb E_{Q_{J_i\mid Y}}D_{iJ_i}(Y)]$,
   and the nonnegative conditional total correlation does not vanish under the
   marginal condition alone.

And one further qualification about $\tau_i$. The row functional
$\sum_j\beta_{ij}\mathbb E_QD_{ij}+\tau_iD_{\rm KL}(\beta_i\Vert\pi_i)$ equals
$\tau_i\mathcal F^{\rm att}_i$. It has the same minimizer, but for $\tau_i\ne1$
it is not an independently weighted sector of one standard global ELBO: it is an
exact ELBO sector for the *rescaled* generative energy $D_{ij}/\tau_i$, and its
numerical value differs from the corresponding ELBO sector by the factor
$\tau_i$. Reporting $\Phi_i$ in "energy units" and adding it to a VFE in nats is
therefore an accounting error unless the entire objective is scaled or a
different generalized free energy is declared.

**Verdict on the problem statement's $\Phi^b_i,\Phi^m_i$.** They are exact VFE
sectors under Reading A, label exclusivity, constant-row recognition,
$\tau=1$ (or a declared global rescaling), and with $D\mapsto\mathbb E_{\mathbb Q}D$.
Under Reading B they are composite potentials. The problem statement's own
instruction — "otherwise call it a composite free-energy potential, not an
ELBO" — is therefore satisfied only by Reading A, and the rest of this report
carries both readings explicitly wherever they diverge.

## 2. The architecture

```
                                         X  (structural data: skeleton, incidence, c_*)
                                         |  fixed, outside every channel
                                         v
   scale S   [ Z_S , G_S ]  <----------- P_S(dZ_S,dG_S | X)          top prior
                 |   ^
      K_down^{S-1}   |  Q_{S-1}(.|Z_S,R,G)         (recognition disintegration,
                 v   |                              same ordering, correlated)
   scale s+1 [ Z_{s+1}, G_{s+1} ]
                 |                              R_s^b : V_s ~~> Lambda^b_{s+1}
        P_R^s ---+---> [ R_s^b , R_s^m ]        R_s^m : V_s ~~> Lambda^m_{s+1}
                 |                              (two channels may block differently)
        P_G^s ---+---> [ G_s = (beta^s, gamma^s, alpha^{b,s}, alpha^{m,s},
                 |                 a^s, Omega^{b,s}, Omega^{m,s}) ]
        P_H^s ---+---> [ H_s = based holonomy reps + dressed boundary marks ]
                 |
        K_down^s |     the ONLY generative locus of downward influence
                 v
   scale s   [ Z_s ]  =  ( q^b_i , q^m_i , xi_i )_{i in V_s}
                 |
                ...
                 v
   scale 0   [ Z_0 ]  ---- L_theta(do | Z_0, X) ----> o     (likelihood attaches
                                                             ONLY at scale 0)

   Coarse-graining direction (measures, not arrows of causation):
       eta^{x,s}_{ij} = alpha^{x,s}_i * (beta or gamma)^s_{ij}          [scale s]
                 |  push through normalized endpoint kernel K^x(A,B|i,j)
                 v
       eta^{x,s+1}_{AB} = sum_{i,j} eta^{x,s}_{ij} K^x(A,B|i,j)
       alpha^{x,s+1}_A  = sum_B eta^{x,s+1}_{AB}
       beta^{s+1}_{AB}  = eta^{x,s+1}_{AB} / alpha^{x,s+1}_A     on {alpha^{x,s+1}_A > 0}
                                                     ^-- disintegration, not row averaging
```

Two orientations run in this picture and they must not be confused. The
**generative** arrow runs top-down: $Z_{s+1}\Rightarrow Z_s\Rightarrow o$. The
**coarse-graining** arrow runs bottom-up and acts on *measures*: it pushes the
fine law through a normalized recognition-independent channel. The bottom-up map
is not a second generative arrow at the same time slice. Inserting it as one
creates a directed 2-cycle, which the ordered-kernel construction cannot
normalize; see Part 2 §Q3.

## 3. Q1 — the most general tractable normalized finite-depth joint

### 3.1 Types

Fix a finite scale set $L=\{0,1,\dots,S\}$. All spaces below are nonempty and
standard Borel, and all reference measures are $\sigma$-finite.

* **Base.** $\mathcal C$ is the context space; **every scale-0 agent sits at one
  point $c_\*\in\mathcal C$**. No length, lattice, translation symmetry, momentum
  space, or tree is assumed. $X\in\mathsf X$ carries the finite directed skeleton
  (cycles permitted), the design incidence, and the geometric data. $X$ and each
  $X_A=\chi_A(X)$ stay outside every random channel.
* **Label pools.** At each scale $s\ge1$ fix a **finite label pool**
  $\Lambda^b_s$, $\Lambda^m_s$ for the two channels. The occupied vertex sets
  $V^b_s,V^m_s$ are then determined by the membership variables rather than fixed
  in advance; this is how a variable number of blocks enters a fixed measurable
  space. $V^b_0=V^m_0=V$, the finite agent set.
* **Agent states.** For $i\in V_s$,
  $\mathsf Y_{i,s}=\mathsf B_{i,s}\times\mathsf M_{i,s}\times\Xi_{i,s}$, with
  $\mathsf B_{i,s}\subseteq\mathcal P(\mathsf Z^b_{i,s})$ the belief-presentation
  space, $\mathsf M_{i,s}$ the model-presentation space equipped with an
  evaluation map $\mathrm{ev}_{i,s}:m\mapsto K_m$ into normalized generative
  kernels, and $\Xi_{i,s}$ auxiliary. $Z_s=(Z_{i,s})_{i\in V_s}$.
  Under Reading A the belief coordinate is genuinely law-valued and
  $\mathcal P(\mathsf Z^b)$ is standard Borel as recorded in §1.1; a model
  presentation is a presentation, not a law, until $\mathrm{ev}$ is declared.
* **Graph data.** $G_s=(\alpha^{b,s},\alpha^{m,s},\beta^s,\gamma^s,a^s,\Omega^{b,s},\Omega^{m,s})$
  with $\alpha^{x,s}\in\Delta(V_s)$ the external receiver occupancies,
  $\beta^s_i,\gamma^s_i\in\Delta(V_s)$ the normalized directed source rows,
  $a^s\in\{0,1\}^{V_s\times V_s}$ the edge occupations, and
  $\Omega^{b,s}_{ij},\Omega^{m,s}_{ij}$ the two channels' transports, valued in a
  standard Borel $G$-space. **The transports are not assumed flat and loop
  holonomy is not penalized toward the identity.**
* **Memberships.** $R^b_s$ and $R^m_s$ are normalized membership kernels
  $C^x_s(A\mid i)\ge0$, $\sum_{A\in\Lambda^x_{s+1}}C^x_s(A\mid i)=1$, together
  with normalized **endpoint kernels** $K^x_s(A,B\mid i,j)$ supported on declared
  incidences. Hard partitions are the deterministic case; soft overlapping
  memberships are permitted; a literal replicated cover
  ($\sum_A R(A\mid i)>1$) is *excluded* because it is not a Markov kernel and
  duplicates mass.
* **Holonomy marks.** $H_s$ records, per parent component, the based holonomy
  representation $H^x_I:\pi_1(\Gamma_I,r_I)\to G$, the component root $r_I$, and
  the dressed boundary generators $V^x_e=\tau^x_{I\leftarrow i}\Theta^x_e(\tau^x_{J\leftarrow j})^{-1}$,
  as one simultaneous root-gauge orbit.
* **Observation.** $o\in\mathsf O$ with $\sigma$-finite $\nu^O$; the likelihood
  $L_\theta(do\mid Z_0,X)$ attaches only at scale 0.

### 3.2 The joint

$$
\begin{aligned}
\mathbb P_\theta(do,dW\mid X)
={}& L_\theta(do\mid Z_0,X)\;P_S(dZ_S,dG_S\mid X)\\
&\times\prod_{s=0}^{S-1}
  P^s_{R}\big(dR^b_s,dR^m_s\,\big\vert\,Z_{s+1},G_{s+1},X\big)\\
&\times\prod_{s=0}^{S-1}
  P^s_{G}\big(dG_s\,\big\vert\,Z_{s+1},R_s,X\big)\;
  P^s_{H}\big(dH_s\,\big\vert\,Z_{s+1},R_s,G_s,X\big)\\
&\times\prod_{s=0}^{S-1}
  K^s_{\downarrow}\big(dZ_s\,\big\vert\,Z_{s+1},R_s,G_s,H_s,X\big).
\end{aligned}
$$

Every factor is a normalized measurable Markov kernel and the product denotes
ordered kernel composition, not multiplication of measures. Four design choices
are doing work.

* The membership factor comes **before** the graph factor at the same scale, so
  the scale-$s$ weights and transports may be generated conditionally on which
  block each fine node belongs to. Reversing the order is legal but gives a
  different model.
* The two channels' memberships are generated **jointly** by one $P^s_R$, which
  permits $R^b_s\ne R^m_s$ (Part 2 §Q5) while keeping their dependence inside the
  model rather than smuggled in later.
* $H_s$ is a *generated* variable, so a parent may be given a prior preference for
  low holonomy without that preference being confused with a theorem. Setting
  $P^s_H$ to a point mass at the identity is the flatness assumption, and it is
  visible as a modeling choice rather than hidden in a regularizer.
* $K^s_\downarrow$ is the **only** location of generative downward influence.

### 3.3 Normalization without a partition function

**Proposition 1 (tower normalization).** Under the typing of §3.1, for every
admissible $(\theta,X)$ the displayed $\mathbb P_\theta(\cdot\mid X)$ is a
probability measure on $\mathsf O\times\mathsf W$, and no global normalizing
constant appears.

*Proof.* The variables carry a finite partial order
$Z_S,G_S\prec R_{S-1}\prec G_{S-1}\prec H_{S-1}\prec Z_{S-1}\prec\cdots\prec Z_0\prec o$,
and every displayed factor conditions only on strictly earlier variables. Integrate
in the reverse of that order against bounded measurable test functions. Each
integral is of a normalized kernel over its own target variable, with all
descendant factors already removed, so each contributes exactly one; the last
integral is against the normalized $P_S$. Measurability at each stage is
preserved because integrating a bounded measurable function against a probability
kernel yields a bounded measurable function of the remaining variables. This is
the finite kernel construction for directed graphical models and reproduces
`cons:gen-finite-directed-law` and `prop:gen-exact-normalization` at tower depth.
$\square$

This is the precise sense in which the construction is "tractable." It is also
where the contrast with a same-time reciprocal factor bites: a Gibbs factor
$\psi(Z_s,Z_{s+1})$ has no such argument and requires a separate proof that
$0<Z_X<\infty$.

## 4. Q2 — the exact VFE and its conditional-KL decomposition

### 4.1 Recognition side

Disintegrate the recognition law along the **same** ordering:

$$
\begin{aligned}
\mathbb Q_\phi(dW\mid o,X)
={}& Q_S(dZ_S,dG_S\mid o,X)\\
&\times\prod_{s=0}^{S-1} Q^s_R(dR_s\mid Z_{s+1},G_{s+1},o,X)\\
&\times\prod_{s=0}^{S-1} Q^s_G(dG_s\mid Z_{s+1},R_s,o,X)\,
   Q^s_H(dH_s\mid Z_{s+1},R_s,G_s,o,X)\\
&\times\prod_{s=0}^{S-1} Q_s(dZ_s\mid Z_{s+1},R_s,G_s,H_s,o,X).
\end{aligned}
$$

This is a *disintegration of a correlated law*, not a mean-field assumption. Any
bottom-up recognition network is free to parameterize the same joint; the written
ordering is bookkeeping. What is **not** permitted is to reconstruct
$\mathbb Q_\phi$ from its coordinate marginals: with at least two nondegenerate
real coordinates, distinct joints share all coordinate marginals
(`prop:prob-marginals-do-not-determine-joint`, witness
$\mathcal N(0,I_2)$ against $\mathcal N(0,\begin{psmallmatrix}1&r\\r&1\end{psmallmatrix})$).

### 4.2 The decomposition

**Theorem 2 (exact hierarchical decomposition).** Assume the factorizations of
§3.2 and §4.1, $p_\theta(o\mid X)\in(0,\infty)$, and
$\mathbb Q_\phi\ll\boldsymbol\Pi_{\theta,o,X}$. Then, as an identity in
$\mathbb R\cup\{+\infty\}$,

$$
\begin{aligned}
\mathcal F_{\rm tower}
={}& \underbrace{-\,\mathbb E_{\mathbb Q_\phi}\log L_\theta(o\mid Z_0,X)}_{\text{observation}}
 \;+\;\underbrace{D_{\rm KL}(Q_S\Vert P_S)}_{\text{top prior}}\\
&+\sum_{s=0}^{S-1}\mathbb E_{\mathbb Q_\phi}\,
  D_{\rm KL}\!\left(Q^s_R(\cdot\mid Z_{s+1},G_{s+1},o,X)\,\Vert\,P^s_R(\cdot\mid Z_{s+1},G_{s+1},X)\right)\\
&+\sum_{s=0}^{S-1}\mathbb E_{\mathbb Q_\phi}\,
  D_{\rm KL}\!\left(Q^s_G(\cdot\mid Z_{s+1},R_s,o,X)\,\Vert\,P^s_G(\cdot\mid Z_{s+1},R_s,X)\right)\\
&+\sum_{s=0}^{S-1}\mathbb E_{\mathbb Q_\phi}\,
  D_{\rm KL}\!\left(Q^s_H(\cdot\mid Z_{s+1},R_s,G_s,o,X)\,\Vert\,P^s_H(\cdot\mid Z_{s+1},R_s,G_s,X)\right)\\
&+\sum_{s=0}^{S-1}\mathbb E_{\mathbb Q_\phi}\,
  D_{\rm KL}\!\left(Q_s(\cdot\mid Z_{s+1},R_s,G_s,H_s,o,X)\,\Vert\,K^s_\downarrow(\cdot\mid Z_{s+1},R_s,G_s,H_s,X)\right),
\end{aligned}
$$

each conditional divergence being averaged over its displayed conditioning
variables under $\mathbb Q_\phi$.

*Proof.* Substitute both factorizations into the Radon–Nikodym ratio and apply
the conditional relative-entropy chain rule at the measure level, one factor at a
time in the declared order. Each step is the standard disintegration identity
$D_{\rm KL}(Q_{1:k}\Vert P_{1:k})=D_{\rm KL}(Q_{1:k-1}\Vert P_{1:k-1})+\mathbb E_{Q_{1:k-1}}D_{\rm KL}(Q_k(\cdot\mid\cdot)\Vert P_k(\cdot\mid\cdot))$,
valid in $[0,+\infty]$ without a finiteness hypothesis. Adding the finite real
$-\log p_\theta(o\mid X)$ to the resulting nonnegative extended real gives the
stated identity. $\square$

### 4.3 Every normalizer, base measure, absolute-continuity condition, and boundary

The problem statement asks for these explicitly. They are:

**Normalizers.** Exactly one: $p_\theta(o\mid X)=\int p_\theta(o,W\mid X)\,\mu_W(dW)$,
the evidence. Proposition 1 shows no other normalizer exists in the directed
tower. If a same-time reciprocal Gibbs factor is added (Part 2 §Q3, mechanism
(iii)), a second normalizer $Z_X$ appears and its finiteness is a
**model-existence condition**, not an algebraic detail. If the row free energies
are used, a third family appears: the row partition functions
$Z^{b,s}_i=\sum_k\pi^{b,s}_{ik}e^{-\mathbb E_{\mathbb Q}D^{b,s}_{ik}/\tau^b_i}$,
finite automatically for a finite source set with finite energies, and the
reduced row value is $-\tau_i\log Z_i$.

**Base measures.** $\nu^O$ on $\mathsf O$; on each $\mathsf B_{i,s}$ a declared
$\sigma$-finite reference on $\mathcal P(\mathsf Z^b_{i,s})$ (this is a real
obligation, not a formality: a canonical reference on a space of laws is not
given for free — a Dirichlet-type or a discrete-support reference must be
declared); $\sigma$-finite references on $\mathsf M_{i,s}$ and $\Xi_{i,s}$;
**counting measure** on all finite/discrete factors ($R_s$, $a^s$, source labels,
label pools) — which is why a finite categorical realization has no measure-theoretic
overhead at all, and why the falsification experiment of Part 4 is built that way;
a declared reference on the transport space (Haar measure if $G$ is locally
compact, counting measure if $G$ is finite). The tower reference is the product
$\mu_W=\bigotimes(\text{all of the above})$, $\sigma$-finite because it is a
finite product of $\sigma$-finite factors. **This finiteness of the product is
exactly what fails in a continuum limit** (`open:prob-continuum-theory`): an
infinite product of non-probability $\sigma$-finite factors is not $\sigma$-finite,
so a continuum theory cannot obtain its reference this way and every claim here
is a finite-design claim.

**Absolute continuity.** (i) $\mathbb Q_\phi\ll\boldsymbol\Pi_{\theta,o,X}$ is
needed for a finite divergence; without it $\mathcal F_{\rm tower}=+\infty$ and
the identity still holds. (ii) For the **density** form
$\mathbb E_{\mathbb Q}\log(q_\phi/p_\theta)$ one additionally needs both laws
dominated by $\mu_W$ with jointly measurable versions
(`thm:prob-kernel-rn-measurable-version`); one family-level dominating measure per
kernel, not a pointwise choice per state, since pointwise Radon–Nikodym versions
need not assemble into a measurable likelihood
(this is the open pointwise-domination item in the claim ledger). (iii) Each
conditional term requires the corresponding conditional absolute continuity
$Q^s_\bullet(\cdot\mid\cdot)\ll P^s_\bullet(\cdot\mid\cdot)$ for
$\mathbb Q_\phi$-a.e. conditioning value; failure at a positive-measure set of
conditioning values makes that term $+\infty$ and, by nonnegativity, makes
$\mathcal F_{\rm tower}=+\infty$.

**Finite versus extended-real boundary.** The clean statements are:

* $D_{\rm KL}(\mathbb Q_\phi\Vert\boldsymbol\Pi)\in[0,+\infty]$ always; the sum of
  the last four groups of terms in Theorem 2 is a sum of nonnegative extended
  reals and is therefore unambiguous with no rearrangement risk.
* The **observation term is the only one that can be $-\infty$**. Since
  $L_\theta(\cdot\mid Z_0,X)$ is a density, $-\log L\in(-\infty,+\infty]$ pointwise,
  but $\mathbb E_{\mathbb Q}(-\log L)$ can be $-\infty$ if $L$ is unbounded above.
  The sufficient and essentially sharp condition is
  $$\mathbb E_{\mathbb Q_\phi}\big(\log L_\theta(o\mid Z_0,X)\big)^{+}<\infty,$$
  automatic when the record is a probability mass function ($L\le1$), or more
  generally when $L$ is $\mathbb Q$-essentially bounded. Under it the displayed
  sum is well defined in $\mathbb R\cup\{+\infty\}$.
* A **finite $\mathcal F_{\rm tower}$ may be negative**: it is the sum of the
  finite real $-\log p_\theta(o\mid X)$ (of either sign) and a nonnegative
  divergence.
* **Never subtract.** The extended-real version of the decomposition must be
  performed at the measure level. Writing
  $\mathcal F_{\rm fine}-\mathcal F_{\rm coarse}=\Delta$ requires **finite fine
  KL**; a bare $+\infty=+\infty$ supplies neither a zero-defect criterion nor a
  recovery consequence, and there is an explicit witness: on $\{a,b,c\}\to\{u,v\}$
  with $a\mapsto u$, $b,c\mapsto v$, $P=\tfrac12\delta_a+\tfrac12\delta_b$,
  $Q=\tfrac12\delta_b+\tfrac12\delta_c$, both fine and coarse divergences are
  $+\infty$ yet no single reverse kernel recovers both
  (`cor:cg-dpi-infinite-equality-warning`).

### 4.4 The two accounting errors the decomposition is designed to prevent

**Double counting a shared factor.** The conditional VFE of a block $B$ contains
*every* interaction factor incident to $B$. Summing singleton local objectives
therefore overcounts: with nonempty factor scopes,

$$
H_{\{i\},o}(y_i;y_{-i})=\sum_{a:\,i\in\partial a}E_{a,o}(y_{\partial a}),
\qquad
\sum_{i\in V}H_{\{i\},o}(y_i;y_{-i})=\sum_{a\in\mathcal A}|\partial a|\,E_{a,o}(y_{\partial a}),
$$

an exact extended-real pointwise identity (`eq:obs-singleton-incident-counting`).
The overcount is $\sum_a(|\partial a|-1)E_{a,o}$ and it is not small. The correct
single-count additive ledger, for a product baseline $P_0=\bigotimes_i\rho_i$ and
an arbitrary correlated $\mathbb Q$, is

$$
\mathcal F^{\rm ext}_o(Q)=\mathrm{TC}(Q)+\sum_i D_{\rm KL}(Q_i\Vert\rho_i)+\mathbb E_Q\Big[\sum_{a\in\mathcal A}E_{a,o}\Big],
\qquad \mathrm{TC}(Q)=D_{\rm KL}\Big(Q\,\Big\Vert\,\bigotimes_iQ_i\Big),
$$

in which each interaction appears exactly once and mean field is the special case
$\mathrm{TC}=0$ rather than a premise. What *is* true about the local objectives
is the exact-potential identity: for $Q=Q_{B^c}r_B$ and $Q'=Q_{B^c}r'_B$ sharing
an outside marginal with $Q_{B^c}\ll\Pi_{o,B^c}$ and both fine KLs finite,
$\mathcal F^{\rm ext}_o(Q')-\mathcal F^{\rm ext}_o(Q)=\mathbb E_{Q_{B^c}}[\mathcal F^{\rm ext}_{B,o}(r'_B;Y_{B^c})-\mathcal F^{\rm ext}_{B,o}(r_B;Y_{B^c})]$.
Local exact updates are coordinate updates of the collective VFE; local objective
*values* do not add.

**Reconstructing a correlated law from marginals.** Every parent belief and model
"law" named in the theory is a coordinate pushforward of a full parent law, and
the pair does not determine the joint. This blocks, in particular, the tempting
move of defining a meta-agent by its transported belief marginal alone: identical
transported marginals do not imply the common-recovery condition
$P_\theta CR=P_\theta$, and equal fair marginals can coexist with an infinite
full-joint KL (parity/anti-parity witness).

## 5. Immediate corollaries worth recording

**Coarse-graining is a loss, not an improvement.** For one normalized
recognition-independent channel $C$ applied to *both* the recognition law and the
posterior, with the observation coordinate untouched,

$$
\mathcal F_P(Q_o)=\mathcal F_{P^c}(Q^c_o)+\int_{\mathsf Z}
D_{\rm KL}\big(\widehat Q_o(dy\mid z)\Vert\widehat\Pi_o(dy\mid z)\big)\,Q^c_o(dz),
$$

an additive identity in $[0,+\infty]$ with the integral $\ge0$
(`thm:rg-exact-coarse-vfe`). The coarse ELBO rises only because a conditional
inference gap was discarded; the evidence is unchanged. This is the correct
statement of "RG lowers the free energy" in this theory, and it must not be read
as model improvement or as EM evidence ascent.

**$1/\beta_{ij}$ is not a metric.** At the Gibbs optimum the source-relative
surprisal is $\ell^b_{ij}=-\tau^b_i\log(\beta^{\star}_{ij}/\pi^b_{ij})=\mathbb E_{\mathbb Q}D^b_{ij}+\tau^b_i\log Z^b_i$:
the transported mismatch plus a row-dependent constant. It is directed, depends on
every competing source through row normalization, diverges as $\beta\to0$, and
inherits no triangle inequality (KL has none). Part 3 §Q9 constructs replacements
that are metrics.
