# Frozen specification — finite categorical falsification experiment

Source of requirements: `gauge_vfe_rg_status.tex` §9, expanded in
`docs/derivations/2026-08-16-multiscale-two-channel-graph-vfe-rg/REPORT-part4-literature-experiment-verdict.md` §13.
Nothing in this file may be changed once building starts; changes are recorded as
dated amendments at the bottom.

Everything here is finite and categorical. No Gaussian family appears anywhere.
All declared numbers are rationals, so every quantity is a finite sum of rationals
and logarithms of rationals.

---

## 1. The system

### 1.1 Group and the two representations

$G=\mathbb Z_3=\{0,1,2\}$ under addition mod 3, with two *distinct* representations
acting on the same sample space $\mathsf Z^b=\mathsf Z^m=\mathbb Z_3$:

$$
\rho_b(k):z\mapsto z+k \pmod 3,
\qquad
\rho_m(k):z\mapsto z+2k \pmod 3 .
$$

Both are faithful, and they differ as maps for $k\ne0$. This is the minimal
realization of the two-channel structure: one group, two unlike actions.

Pushforward on laws is $(\rho_x(k)_\#p)(z)=p(z-\sigma_x(k))$ with $\sigma_b(k)=k$
and $\sigma_m(k)=2k$.

### 1.2 Presentation spaces (Reading A)

Reading A is in force: the agent's latent state **is** a law, so $D^b_{ij}$ is a
function of the state and may legitimately sit inside a generative factor. Reading
B is not used anywhere, and no generative factor reads a recognition law or a
posterior.

Belief presentations $\mathsf B$ are a finite $\rho_b$-orbit-closed set of laws on
$\mathbb Z_3$. Seed $p^{(0)}=(\tfrac12,\tfrac13,\tfrac16)$, orbit

$$
\mathsf B_{\rm orb}=\Big\{(\tfrac12,\tfrac13,\tfrac16),\;
(\tfrac16,\tfrac12,\tfrac13),\;(\tfrac13,\tfrac16,\tfrac12)\Big\},
\qquad |\mathsf B_{\rm orb}|=3 .
$$

Model presentations $\mathsf M$ are a finite $\rho_m$-orbit-closed set. Seed
$q^{(0)}=(\tfrac23,\tfrac16,\tfrac16)$, orbit

$$
\mathsf M_{\rm orb}=\Big\{(\tfrac23,\tfrac16,\tfrac16),\;
(\tfrac16,\tfrac23,\tfrac16),\;(\tfrac16,\tfrac16,\tfrac23)\Big\} .
$$

Because $2$ is invertible mod 3, $\{\sigma_m(k)\}=\mathbb Z_3$, so $\rho_m$-orbits
and $\rho_b$-orbits coincide as sets; the channels are separated by *which group
element produces which shift*, not by the orbit geometry.

**Two declared admitted parent families**, and the difference between them is a
measurement, not a detail:

* `ADMITTED = "orbit"` — $\mathscr M^x=\mathsf B_{\rm orb}$ (resp. $\mathsf M_{\rm orb}$).
  The uniform law is **excluded**.
* `ADMITTED = "simplex"` — $\mathscr M^x=\Delta(\mathbb Z_3)$, the full simplex.

The stabilizer of a nontrivial cyclic shift acting on $\Delta(\mathbb Z_3)$ is
exactly the uniform law. So under `orbit` the fixed sector is empty on any block
carrying nontrivial holonomy, and Proposition 8 fires with
$\mathfrak D=+\infty$; under `simplex` the fixed sector is the single uniform law
and $\mathfrak D$ is finite. Both are computed and reported.

### 1.3 Evaluator and likelihood

$\mathrm{ev}:\mathsf M\to\mathrm{Kern}(\mathsf Z^b,\mathcal P(\{0,1\}))$ is declared by

$$
\mathrm{ev}(m)(o=1\mid z)=m_z,\qquad \mathrm{ev}(m)(o=0\mid z)=1-m_z .
$$

Every declared $m_z\in\{\tfrac16,\tfrac23\}\subset(0,1)$, so no likelihood entry
vanishes and the observation term is finite. Records are
$\mathsf O=\{0,1\}^6$ and the likelihood attaches **only at scale 0**:

$$
L_\theta(o\mid Z_0,X)=\prod_{i\in V}L_i(o_i\mid b_i,m_i),
\qquad
L_i(o_i\mid b_i,m_i)=\sum_{z\in\mathbb Z_3}b_i(z)\,\mathrm{ev}(m_i)(o_i\mid z).
$$

This per-agent product is what makes the inner $Z_0$ sum factorize; it is a
declared modeling choice and is stated as such.

### 1.4 Graph

$V=\{1,\dots,6\}$, all at the single contextual point $c_\*$. **Convention, fixed
once:** an ordered pair $(i,j)$ means *$i$ is the receiver and $j$ is the source*,
so $\beta_i\in\Delta(V)$ is the receiver-$i$ row over sources, $\alpha_i$ is the
receiver occupancy, and $\Omega_{ij}$ transports $j$'s frame into $i$'s frame,
matching $D_{ij}=\KL(q_i\Vert(\Omega_{ij})_\#q_j)$.

Interaction edges:

$$
E=\{(1,2),(2,3),(3,1)\}\cup\{(4,5),(5,6),(6,4)\}\cup\{(3,4),(6,1)\},
$$

two directed 3-cycles plus two cross edges, together with self-loops $(i,i)$
carrying identity transport so that every row has at least two admitted sources.
The underlying cycle rank is $8-6+1=3$: cycle A, cycle B, and the directed
6-cycle $1\!\leftarrow\!2\!\leftarrow\!3\!\leftarrow\!4\!\leftarrow\!5\!\leftarrow\!6\!\leftarrow\!1$.

### 1.5 Transports, chosen to separate the channels

Group elements $g^x_{ij}\in\mathbb Z_3$ per edge; $\Omega^x_{ij}=\rho_x(g^x_{ij})$.

| edge | $g^b$ | $g^m$ |
|---|---|---|
| (1,2) | 1 | 1 |
| (2,3) | 1 | 1 |
| (3,1) | 0 | 1 |
| (4,5) | 1 | 2 |
| (5,6) | 1 | 2 |
| (6,4) | 1 | 2 |
| (3,4) | 0 | 0 |
| (6,1) | 0 | 0 |
| self  | 0 | 0 |

Resulting loop holonomies as group elements:

| loop | belief | model |
|---|---|---|
| cycle A $\{1,2,3\}$ | $1+1+0=2$ — **nontrivial** | $1+1+1=0$ — trivial |
| cycle B $\{4,5,6\}$ | $1+1+1=0$ — trivial | $2+2+2=0$ — trivial |
| big 6-cycle | $1+1+0+1+1+0=1$ — **nontrivial** | $1+1+0+2+2+0=0$ — trivial |

The model connection is therefore **flat** (every loop holonomy trivial) while the
belief connection is not. Cycle B carries nonzero edge transports with trivial
holonomy, so the test detects holonomy rather than merely detecting whether
transports are the identity. This is the asymmetry §9 predicts should be directly
observable: block $\{4,5,6\}$ admits a stabilized parent in both channels, block
$\{1,2,3\}$ only in the model channel.

Flatness of the model channel implies stabilization but **not** agreement between
agents, so $\mathfrak D^m$ need not vanish; the prediction is only that it *can*,
and the experiment must exhibit a configuration where it does.

### 1.6 Occupancies and rows

Receiver occupancies are declared, skewed, and different per channel:

$$
\alpha^b=(0.30,0.25,0.20,0.12,0.08,0.05),\qquad
\alpha^m=(0.05,0.08,0.12,0.20,0.25,0.30).
$$

Rows $\beta_i,\gamma_i\in\Delta(V)$ are supported on the admitted sources of $i$
(its out-neighbors in the receiver→source convention, plus the self-loop). Edge
event laws are $\eta^b_{ij}=\alpha^b_i\beta_{ij}$ and $\eta^m_{ij}=\alpha^m_i\gamma_{ij}$,
each a probability law on ordered pairs and a family of gauge-invariant scalars.

Optional toggle `PERRON_ALPHA`: replace the declared $\alpha^x$ by the stationary
vector of the row-stochastic attention chain, which is the self-consistent choice
under which additive symmetrization of $\eta^x$ preserves occupancy exactly. Off
by default; on, it feeds the §6.2 Laplacian/effective-resistance diagnostic.

### 1.7 Scales, label pools, and the typing rule

Fixed label pools, never occupied subsets. $\Lambda_0=V$;
$\Lambda_1=\{A_1,A_2,A_3\}$; $\Lambda_2=\{U_1,U_2\}$. Occupancy is the derived
predicate $\alpha^{x,s}_A>0$; unoccupied labels carry coordinates and zero edge
mass. Unoccupied labels decouple, so the implementation may marginalize them
analytically — an exact step, not an approximation.

**Capacity bound (declared, not derived).** $|\mathsf Z_{1,I}|=|\mathsf B|\cdot|\mathsf M|$
independent of $|I|$. Proposition 5 says selection is impossible without it.

**Cost per parent node.** CRP/Ewens prior on set partitions at declared $\vartheta$,

$$
P^0_R(\pi)=\frac{\vartheta^{|\pi|}\prod_{B\in\pi}(|B|-1)!}{\vartheta^{(n)}},
\qquad \vartheta^{(n)}=\vartheta(\vartheta+1)\cdots(\vartheta+n-1),
$$

exactly normalized, exchangeable, projective. Default $\vartheta=1$.

Candidate partitions (all with at most $|\Lambda_1|=3$ blocks, so the pool suffices):

```
R1 = {1,2,3}{4,5,6}        the cycle blocks
R2 = {1,2}{3,4}{5,6}       cross-cutting
R3 = {1,2,3,4,5,6}         one big block
R4 = {1,2,3,4}{5,6}
R5 = {1,4}{2,5}{3,6}       maximally cross-cutting
R6 = {1}{2,3,4,5,6}
```

All-singletons has 6 blocks and exceeds the pool; it is tested on the reduced
instance of §1.10 where it fits, because it is the degeneracy Proposition 5 names.

### 1.8 The generative tower, depth $S=1$

Ordering $Z_1\prec R_0\prec G_0\prec H_0\prec Z_0\prec o$, every factor a
normalized Markov kernel conditioning only on strictly earlier variables, so
Proposition 1 applies and no partition function appears.

* $P_1(dZ_1)$ — product over $\Lambda_1$ of a declared law on $\mathsf B\times\mathsf M$.
* $P^0_R$ — the CRP above, independent of $Z_1$.
* $P^0_G(G_0\mid Z_1,R_0,X)$ — a declared law on a finite set $\mathsf G$ of
  $|\mathsf G|=2$ row/temperature configurations, with Gibbs weights built from
  **parent-level** divergences $D^{(1)}$ only. It may not read $Z_0$, which is
  generated later, and it may not read any recognition law.
* $P^0_H(H_0\mid Z_1,R_0,G_0,X)$ — a two-atom law on
  $\mathsf H=\{\text{computed holonomy},\ \text{identity}\}$ with weights
  $(1-\lambda,\lambda)$. Setting $\lambda=1$ *is* the flatness assumption, and it
  is visible here as a modeling choice rather than hidden in a regularizer.
* $K^0_\downarrow(Z_0\mid Z_1,R_0,G_0,H_0,X)$ — the only site of generative
  downward influence, factorized over agents given the parent:

$$
K^0_\downarrow(z_i\mid z_{1,I},\dots)\;\propto\;
\exp\!\Big(-\kappa_b\KL\big(b_i\big\Vert(\tau^b_{i\leftarrow I})_\#b_{1,I}\big)
-\kappa_m\KL\big(m_i\big\Vert(\tau^m_{i\leftarrow I})_\#m_{1,I}\big)\Big),
$$

normalized over $(b_i,m_i)\in\mathsf B\times\mathsf M$, where $\tau^x_{i\leftarrow I}$
is the spanning-tree transport from the block root to $i$. On a block with
nontrivial holonomy the tree transport is path-dependent, so no parent state makes
all children simultaneously consistent, and the block-formation energy acquires a
strictly positive floor. This is the channel through which holonomy enters the
free energy, and it must not be smoothed away.

### 1.9 The recognition tower

$\mathbb Q_\phi$ is disintegrated along the **same** ordering, factor for factor.
This is a disintegration of a correlated law, not a mean-field assumption.
$\mathbb Q_\phi$ is never reconstructed from coordinate marginals anywhere in the
implementation; any routine that would need to do so is a defect.

### 1.10 Reduced instance, for the independent flat route

`REDUCED`: agents $\{1,2,3\}$ (cycle A alone, retaining nontrivial belief
holonomy and trivial model holonomy), both channels live, $|\mathsf B|=|\mathsf M|=3$,
$\Lambda_1=\{A_1,A_2\}$, candidate partitions including all-singletons. Sizes:
$|Z_0|=9^3=729$, $|Z_1|=9^2=81$, $|\mathsf G|=|\mathsf H|=2$, so the flat joint is
under $10^6$ states and is enumerated **without** exploiting any factorization.
This is what makes route (a) of measurement 1 a genuinely independent computation
rather than a rearrangement of route (b).

---

## 2. The six measurements

Run in order. A failure at any stage invalidates everything downstream, and that
must be reported rather than worked around.

### M1 — VFE accounting

Compute $\mathcal F_{\rm tower}$ two ways.

(a) **Direct**, on `REDUCED`, by flat enumeration of the joint:
$-\log p_\theta(o\mid X)+\KL(\mathbb Q_\phi\Vert\boldsymbol\Pi_{\theta,o,X})$, with
$p_\theta(o\mid X)$ obtained by summing the flat joint over $\mathsf W$ and
$\boldsymbol\Pi$ by normalizing it.

(b) **Decomposition**, the six conditional-KL groups of Theorem 2 at $S=1$:
observation, top prior, $R$, $G$, $H$, and cross-scale.

Also compute the naive sum of local row potentials and report the overcount
$\sum_a(|\partial a|-1)E_{a,o}$, which is exact and pointwise.

*Falsifier.* (a) and (b) differ by more than $10^{-12}$.
*Secondary falsifier.* Any code path reports the naive sum as "the ELBO".

Hypothesis (iv) of Theorem 2, $\mathbb E_{\mathbb Q}(\log L)^+<\infty$, is
satisfied by construction here since $\mathsf W$ is finite and $L$ is bounded away
from 0 and 1; the implementation asserts it rather than assuming it silently.

### M2 — Coarse-edge composition

Build normalized endpoint kernels $K_{10}(A,B\mid i,j)$ and $K_{21}(U,W\mid A,B)$
with **deliberately correlated** endpoint assignments, so $K\ne C\otimes C$.
Push $\eta^{x,c}_{AB}=\sum_{ij}\eta^x_{ij}K(A,B\mid i,j)$, then
$\alpha^c_A=\sum_B\eta^c_{AB}$ and $\beta^c_{AB}=\eta^c_{AB}/\alpha^c_A$ on
$\{\alpha^c_A>0\}$.

Checks: $K_{20}=K_{21}\!\circ\!K_{10}$ as kernels; the event law from $C_{20}$
equals the two-step result; total mass is preserved exactly at every step.
Negative control: assume the product form $K=C\otimes C$ under correlated
assignments and show it fails.

Row-average control: reproduce the declared three-node witness
$\alpha=(0.9,0.1,0)$, $\beta_1=(0,0,1)$, $\beta_2=(1,0,0)$, $\beta_3=(0,0,1)$,
$I=\{1,2\}$, $J=\{3\}$, which gives $\beta^c_{IJ}=0.9$ against
$\beta^{\rm naive}_{IJ}=0.5$, a discrepancy of $0.4$. Then measure the same
discrepancy on the six-agent instance under skewed $\alpha$.

*Falsifier.* Composition fails, which in practice means a product form was assumed
while the intermediate assignments are correlated.

### M3 — Closure residual and generated many-body terms

Möbius inversion on the scale-0 factor graph,

$$
\Phi^c_A(z_A)=\sum_{B\subseteq A}(-1)^{|A|-|B|}H^c_o(z_B,z^\circ_{B^c}),
$$

against a declared ground configuration $z^\circ$. Report the largest generated
three-body coefficient and the residual of projecting onto a pairwise parent
family, measured against the retained flow.

Reference calculation, computed independently as a unit check: the Ising star with
field $h_0$ and couplings $J_1,J_2,J_3$ has leading three-body coefficient
$2\,\mathrm{sech}^2(h_0)\tanh(h_0)J_1J_2J_3$.

*Falsifier.* The residual is not small compared with the retained flow, or the
three-body coefficient is nonzero while the implementation reports a pairwise
coarse theory.

### M4 — Holonomy retention

Per candidate block $I$, per channel $x$, at a chosen root $r_I$:

* the based-loop transport group $\mathfrak h^x_I(r)$ from a cycle basis of the
  induced subgraph;
* the fixed sector
  $\mathscr Q^x_{I,\rm fix}(r)=\{Q\in\mathscr M^x:H_\#Q=Q\ \forall H\in\mathfrak h^x_I(r)\}$,
  computed under **both** admitted families of §1.2;
* the score, with $\inf\varnothing:=+\infty$,

$$
\mathfrak D^x_I=\inf_{Q\in\mathscr Q^x_{I,\rm fix}(r)}\ \sum_{i\in I}w_i\,
\KL\big((\tau^x_{I\leftarrow i})_\#p^x_i\,\big\Vert\,Q\big),
\qquad w_i=\alpha^x_i/\alpha^x_I ;
$$

* the full conditional law of dressed transports
  $\Theta^{IJ,x}_{ij}=\Omega^x_{Ii}\Omega^x_{ij}\Omega^x_{jJ}$, with the endpoint
  factor carried in the numerator over **all** ordered pairs,

$$
\mu^x_{IJ}(g\mid z)=\frac{\sum_{i,j}\eta^x_{ij}K^x(I,J\mid i,j)\,
\mathbf 1[\Theta^{IJ,x}_{ij}=g]}{\sum_{i,j}\eta^x_{ij}K^x(I,J\mid i,j)} ,
$$

its positive-mass atoms, and the barycenter $\overline{\mathsf U}^x_{IJ}$.

Assertions the implementation must make, each an executable check:

* $\mu^x_{IJ}$ sums to exactly 1 under soft memberships. The restricted
  "$i\in I,\ j\in J$" numerator is computed too and shown **not** to normalize,
  reproducing counterexample C27.
* Stabilizer criterion at the measurable tier: $\mu^x_{\rm loop}(\mathrm{Stab}(Q_I))=1$,
  not support containment.
* Flatness $\Rightarrow$ stabilization is checked; flatness $\not\Rightarrow$
  agreement and stabilization $\not\Rightarrow$ flatness are each exhibited by a
  witness in this finite model.
* The barycenter is checked for membership in $\rho_x(G)$ and flagged when it is
  not. Using it as a group element is a falsifier.
* Proposition 9 forward direction only: conditional independence gives the
  convolution. The converse is exhibited false by $G=\mathbb Z_3$, $U$ uniform,
  $V=U$ (counterexample C25).

*Prediction.* $\mathfrak D^b_{\{1,2,3\}}>0$ while $\mathfrak D^m_{\{1,2,3\}}$ can
vanish; both can vanish on $\{4,5,6\}$.
*Theory falsifier.* If $\mathfrak D^b_I>0$ for **every** candidate block, no
zero-distortion belief parent exists anywhere on this cyclic graph — Proposition 8
in action, and the hierarchy mechanism as stated cannot produce an exactly
parallel meta-agent.

### M5 — Partition persistence

Coupled descent on $(R,Z)$ at noise amplitude $\epsilon$: a Metropolis dynamics on
the exact finite free energy, with the partition posterior of Proposition 4,
$Q^\star_R(R)\propto P^0_R(R)e^{-U_0(R)}$, and $U_0$ **derived** as the sum of the
conditional divergences $R$ controls, never hand-written. Note $\tau_R=1$ exactly;
a tempered sector is a different objective and is not mixed into a reported number.

From $K=200$ random initializations measure the co-membership matrix, the modal
partition, per-partition residence time, and the belief relaxation time $t_{\rm rel}$
(time for $\Vert\dot Z\Vert$ to fall by $e^{-1}$). Sweep $\epsilon$ and fit
$\log(\text{exit time})$ against $1/\epsilon$.

*Falsifier.* No partition has residence time exceeding $10\,t_{\rm rel}$, i.e. no
timescale separation and hypothesis (H1) fails.
*Secondary falsifier.* The exit-time fit is not linear in $1/\epsilon$, i.e. the
configuration is not a metastable basin and "persistence" is a misnomer.

### M6 — Downward influence

Intervene on the parent: replace $Z_1$ by $z'$ and recompute the child's optimum
$Q^\star_0\propto K^0_\downarrow(\cdot\mid z')e^{-\mathcal E_0}$. Report

$$
\sup_{z',z''}\big\Vert Q^\star_0(\cdot\mid z')-Q^\star_0(\cdot\mid z'')\big\Vert_{TV}.
$$

**Deterministic-pushforward control.** Replace $K^0_\downarrow$ by the $C$-fiber
disintegration of Proposition 3(a) and verify the same supremum collapses to the
within-fiber variation only.

*Falsifier.* The supremum is zero for the declared $K_\downarrow$, i.e. the
meta-agent exerts no downward influence and is decorative.
*Confirmation of Proposition 3.* The control does collapse, which operationalizes
the impossibility.

### Null control (mandatory)

Rerun the entire pipeline with i.i.d. uniformly random $\Omega^b,\Omega^m$ and
i.i.d. random beliefs, graph skeleton unchanged, over a declared number of seeds.
If blocks form and persist there too, the pipeline is detecting its own blocking
algorithm rather than the system. Every reported block-formation statistic must
carry its null distribution beside it.

---

## 3. Reporting rules

* Every measurement reports its pre-registered falsifier verdict explicitly, and a
  fired falsifier is a result to be reported, not a bug to be worked around.
* Numbers are reported as executed. "Not run" and "failed" are reportable outcomes.
* No measurement is described as verifying the theory. This experiment can refute
  mechanisms; it cannot certify a theorem. Terminal language stays at that level.

---

## Amendments

*(none)*
