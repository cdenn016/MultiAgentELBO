# Multiscale two-channel gauge-network VFE — Part 4
## Literature adjudication, falsification design, claim table, strongest theorem (Q9, Q10)

Continues Parts 1–3.

## 12. Q9 — Bayesian renormalization, network renormalization, and what remains

### 12.1 Bayesian renormalization as a model-space relevance criterion

**Primary source, verified this session.** Berman, Klinger and Stapleton,
"Bayesian Renormalization," arXiv:2305.10491 [hep-th], v1 17 May 2023, v3
9 Oct 2023; published *Machine Learning: Science and Technology* **4**(4) 045011,
doi:10.1088/2632-2153/ad0102. Abstract (verbatim, checked against the arXiv
listing): "In this note we present a fully information theoretic approach to
renormalization inspired by Bayesian statistical inference, which we refer to as
Bayesian Renormalization. The main insight of Bayesian Renormalization is that the
Fisher metric defines a correlation length that plays the role of an emergent RG
scale quantifying the distinguishability between nearby points in the space of
probability distributions."

**What it contributes.** An RG scale that exists where no physical length or
momentum does. Setting $\tau=1/T$ with $T$ the number of observations, the late-$T$
Laplace posterior is $\mathcal N(\mu_T,T^{-1}\mathcal I(\mu_T)^{-1})$, and pushing
through a forward map $G$ gives the diffusion kernel of the induced Fokker–Planck
equation as the pushforward inverse Fisher metric, Eq. (44):
$(K_\tau^{-1})^{ab}=\partial_iG^a\,\partial_jG^b\,\mathcal I^{ij}_\tau$, i.e.
$D_\tau=J_G(\mu_\tau)\,\mathcal I(\mu_\tau)^{-1}J_G(\mu_\tau)^\top$. The operational
scheme, Eq. (55), partitions parameters by Fisher diagonal against a cutoff,
$\Theta^{>}_\Lambda=\{\theta_i:\mathcal I_{ii}>\Lambda\}$, and integrates out the
rest.

**What it does not contribute here, verified against the primary.** The paper does
**not** treat directed graphs, network partitions, or holonomy anywhere. So it
supplies no block selector, no renormalization of non-flat transports, and no
closure statement for a two-channel interaction law.

**Four qualifications that must travel with any use of it.**

* *Stiff/sloppy = relevant/irrelevant is the paper's interpretive claim*, rigorously
  supported only in the CFT case where the Fisher metric coincides with the
  Zamolodchikov metric. It is not a theorem in the general setting.
* *The spectral argument and the diagonal implementation do not match.* §3.1 argues
  in terms of Fisher **eigenvalues**; §4.2 thresholds the **diagonal**
  $\mathcal I_{ii}$. A set of individually sloppy but jointly stiff parameters is
  misclassified, and no bridging argument appears in the visible text.
* *The information-bottleneck link advertised in the abstract is not derived*; it is
  inherited transitively.
* *The authors themselves describe the connections as "largely conceptual"* and
  assume a unique data-generating $\theta_\*$ with a late-$T$ Bernstein–von Mises
  Gaussian posterior. Invertibility of the pushforward Fisher metric is implicit in
  the notation from Eq. (35) onward and is not discussed; singular and near-singular
  metrics go untreated. That is a reader's observation, not an author-stated caveat.

**Orientation, and the typing hazard.** BKS renormalize **model-parameter space**
and keep the **stiff** directions; Wilsonian and Laplacian RG renormalize **sample
space** and keep the **soft** ones. On a single matrix these select opposite
subspaces. Any sentence of the form "coarse-graining keeps the relevant directions"
is ambiguous between them and, read the wrong way, is false. In the present theory
the correct target for a BKS-style criterion is the **model channel**: a parent
model presentation $q^m_A$, once passed through its evaluator into a normalized
generative kernel, has a genuine model-parameter space on which Fisher
distinguishability is well typed. The belief channel is a sample-space object and is
not a legitimate target for the same criterion.

**The bridge is open.** To compare the coarse flow of this theory with the BKS flow
one must put both on one state space, transport the relevant Fisher tensors, declare
a common scale map, and prove a monotone. Similar Gaussian formulas do not prove
opposite flow directions; the relevant derivative is
$\frac{d}{d\tau}[\tau\mathcal I(\mu_\tau)^{-1}]=\mathcal I^{-1}-\tau\mathcal I^{-1}\frac{d\mathcal I}{d\tau}\mathcal I^{-1}$
and no such bridge is asserted anywhere in the live theory.

### 12.2 Network renormalization as a topology/scale mechanism

**Primary source, verified this session.** Gabrielli, Garlaschelli, Patil and
Serrano, "Network Renormalization," arXiv:2412.12988 [physics.soc-ph], v1
17 Dec 2024; published *Nature Reviews Physics* **7**, 203–219 (2025),
doi:10.1038/s42254-025-00817-5. It is a **review**. Its three-step organization is
(i) define coarse variables, (ii) marginalize fine detail, (iii) renormalize
parameters, with the canonical binary rule
$a^{(\ell+1)}_{IJ}=1-\prod_{i\in I}\prod_{j\in J}(1-a^{(\ell)}_{ij})$.

**Do not treat its open problems as solved theorems.** Partially re-verified against
the primary this session: the review does **not** claim that any framework solves
the simultaneous renormalization of topology and of the dynamics running on it; it
states that compatibility of a given coarse-graining with the dynamics "has to be
considered as an additional consistency requirement, whether in terms of any given
realization, or at the level of the statistical ensemble it may derive from." The
remaining §6 open-problem headings — intrinsic versus observational resolution,
coupled renormalization of dynamics and topology, generalized criticality, and
"Parameter (ir)relevance: an information-theoretic perspective" — are recorded here
from the project's vault note rather than re-verified verbatim, because the HTML and
PDF fetches truncated before §6 this session. The vault note additionally records,
from a mechanical check, that the parameter-relevance passage contains **zero
equations** across its ~9.9k characters: it is a stated direction, not a derivation.

**Contributions and their limits, per framework.**

* *Geometric renormalization.* Blocks come from a latent hyperbolic embedding. Not
  applicable here: all scale-0 agents lie at one context point $c_\*$, so there is no
  similarity circle and no angular sector to block by.
* *Laplacian RG.* Supplies a genuine intrinsic scale (§12.3). Its listed
  requirement — the full Laplacian spectrum — is met by any finite realization here.
  Its flow is a semigroup, not a group: fast modes are discarded and not recoverable.
* *Multiscale model (MSM).* The only uniqueness result of the three:
  $p_{ij}=1-e^{-\delta x_ix_jf(d_{ij})}$ is the unique connection probability whose
  functional form survives *every* partition, with fitness $x$ additive, $d$
  renormalizing as a fitness-weighted $f$-mean, and $\delta$ exactly invariant.
  What transfers here is a **cautionary criterion, not a licence**: the closure is
  *parametric*, tied to that independent-edge ensemble, that OR coarse map, and
  that prescribed dyadic update. Additivity of one coarse statistic does not import
  it, and calling the $\eta$-pushforward "MSM-consistent" would overstate the
  connection. Part 2 §8.1 pushes $\eta$ linearly for an internal reason instead:
  $\phi=1$ is the unique $\phi$-norm that is a fixed input-independent Markov
  pushforward, which is what the exact KL chain rule requires. The $\alpha$-stable
  annealed variant makes the flow a two-sided *group* by infinite divisibility,
  which is the only route in this literature to an invertible (fine-graining)
  direction.
* *Weighted geometric renormalization (GRW).* Zheng, García-Pérez, Boguñá and
  Serrano extend GR to weighted networks by the $\phi$-norm
  $\omega'_{IJ}=C\big(\sum_{e}\omega_e^{\phi}\big)^{1/\phi}$ with
  $\phi\equiv\beta/(D(\eta-1)+\alpha)$, the sum rule at $\phi=1$ and sup-GRW as
  $\phi\to\infty$ (*Communications Physics* **7**, 97 (2024), arXiv:2307.00879).
  Two things follow for this program. It **refutes** any claim that
  renormalizability universally means additivity — closure is relative to a
  declared family and protocol. And it isolates why $\phi=1$ is nonetheless forced
  here: it is the only member of the family that is a fixed input-independent
  Markov pushforward, which the KL chain rule needs. Their blocks still come from
  latent geometric order, and the authors name directionality as essential future
  work, so nothing in it covers directed row-stochastic $\beta,\gamma$ channels,
  gauge transports, or partition persistence. Mechanism M5 of Part 3 §10.1 records
  the conjectural transplant and its three caveats.

**What is unsolved for a directed two-channel gauge network.** None of the three
frameworks handles: row-normalized directed conditionals $\beta,\gamma$ as opposed
to symmetric couplings; **two** distinct group representations on the same principal
bundle; non-flat holonomy and the retention of marks; or the simultaneous
renormalization of beliefs, models, topology, and dynamics — which the review itself
names as open. The two-channel, group-valued analogue of the MSM uniqueness theorem
is unformulated, let alone proved.

### 12.3 Better intrinsic scales than $1/\beta$

The problem statement asks for this explicitly. Here is a defensible hierarchy,
with the typing of each object stated.

**Step 1 — a gauge-invariant conductance graph.** $\eta^x_{ij}=\alpha^x_i\beta^x_{ij}$
and $\alpha^x_i$ are gauge-invariant scalars, so

$$
L^x:=\mathrm{diag}(\alpha^x)-\eta^x
$$

is gauge-invariant, has **exactly zero row sums** ($\sum_j\eta^x_{ij}=\alpha^x_i$),
and $-L^x$ is a bona fide rate matrix with jump rates $\eta^x_{ij}$. This already
repairs the standard typing caveat about importing LRG: a precision-like operator
with self terms generates a *killed* diffusion, whereas $L^x$ generates an honest
one. It is directed, hence generally nonsymmetric.

**Step 2 — self-consistent occupancy makes the symmetrization exact.**

**Proposition 11.** Suppose $\beta^x$ is irreducible and choose the receiver
occupancy self-consistently as its Perron vector, $\alpha^x=\phi^x$ with
$\phi^x\beta^x=\phi^x$, $\sum_i\phi^x_i=1$. Let
$\eta^{x,\rm sym}:=\tfrac12(\eta^x+(\eta^x)^\top)$ and
$\alpha^{x,\rm sym}_i:=\sum_j\eta^{x,\rm sym}_{ij}$. Then
$\alpha^{x,\rm sym}=\alpha^x$, and

$$
L^{x,\rm sym}:=\mathrm{diag}(\alpha^{x})-\eta^{x,\rm sym}
$$

is a symmetric positive-semidefinite gauge-invariant weighted graph Laplacian with
kernel spanned by $\mathbf 1$ on each connected component. Moreover, with
$\Phi=\mathrm{diag}(\phi^x)$ and $P=\beta^x$, one has
$\eta^{x,\rm sym}=\tfrac12(\Phi P+P^\top\Phi)$, so $L^{x,\rm sym}$ is exactly the
unnormalized form of Chung's directed Laplacian for $P$.

*Proof.* $\alpha^{\rm sym}_i=\tfrac12(\sum_j\eta_{ij}+\sum_j\eta_{ji})
=\tfrac12(\phi_i+\sum_j\phi_j\beta_{ji})=\tfrac12(\phi_i+\phi_i)=\phi_i$, using
stationarity in the second sum. Symmetry and zero row sums with nonnegative
off-diagonal weights give the standard PSD weighted-Laplacian conclusion.
$(\Phi P)_{ij}=\phi_i\beta_{ij}=\eta_{ij}$ gives the last identity. Gauge invariance
is inherited from $\eta,\alpha$. $\square$

(Chung, "Laplacians and the Cheeger inequality for directed graphs,"
*Annals of Combinatorics* **9** (2005), 1–19, defines the normalized
$\mathcal L=I-\tfrac12(\Phi^{1/2}P\Phi^{-1/2}+\Phi^{-1/2}P^\top\Phi^{1/2})$;
Proposition 11 records that the unnormalized version is exactly the symmetrized
edge-event law, and that the self-consistent occupancy is what makes the
symmetrization occupancy-preserving.)

**Step 3 — genuine metrics.** On $L^{\rm sym}$ the effective resistance
$R^{\rm eff}(i,j)=(e_i-e_j)^\top (L^{\rm sym})^{\dagger}(e_i-e_j)$ **is a metric**
(Klein and Randić, *J. Math. Chem.* **12** (1993), 81–95), as is the commute time
$\mathrm{vol}\cdot R^{\rm eff}$. Both are gauge-invariant, directed-graph-derived,
and require no embedding. This is the honest replacement for "$1/\beta$ is an
interaction length."

**Step 4 — an intrinsic scale, not a distance.** With $L^{\rm sym}$ symmetric PSD,
$\rho(\tau)=e^{-\tau L^{\rm sym}}/Z(\tau)$ is a legitimate density matrix with real
nonnegative spectrum, so the von Neumann entropy $S(\tau)$ and the entropic
susceptibility $C(\tau)=-dS/d\log\tau$ are well defined. Peaks of $C$ locate
candidate scales $\tau^\*$; a plateau at $C=d_s/2$ marks a scale-invariant window.
Two channels give two independent scale spectra $C^b(\tau),C^m(\tau)$, and their
*disagreement* is itself a diagnostic: a system whose belief and model channels peak
at different $\tau$ has no single hierarchy.

**Step 5 — information geometry, done correctly.** Within one belief fiber the
Fisher–Rao distance is a metric. Across fibers, transport to a common root and
compare there:

$$
d^{x}_{FR}(i,j):=d_{FR}\big((T^x_{\gamma_i})_\#q^x_i,\ (T^x_{\gamma_j})_\#q^x_j\big).
$$

Because each $T^x_\gamma$ is a bimeasurable bijection of the sample space and the
admitted family is equivariant, the induced map on the statistical manifold is an
isometry for Fisher–Rao (invariance of relative entropy under a common bimeasurable
bijection gives invariance of the induced metric). Hence $d^x_{FR}$ is symmetric and
satisfies the triangle inequality — a genuine pseudometric, and a metric on the
quotient by "equal transported law." Its two caveats are exactly the geometry of the
problem: **path independence requires holonomy stabilization** of the compared laws,
and a change of root conjugates every transport, which preserves the distance
(isometry) but relabels the fiber.

**Step 6 — relevance, not distance.** BKS Fisher shells order **model-channel
parameter directions** by distinguishability. This is not a graph distance and must
not be mixed with Steps 3–4; see the typing hazard in §12.1.

**What must be discarded.** $1/\beta_{ij}$ is directed, row-relative, competitive
(raising one entry lowers the others by normalization), divergent as $\beta\to0$,
and has no triangle inequality. The Gibbs-optimal surprisal
$\ell^b_{ij}=\mathbb E_{\mathbb Q}D^b_{ij}+\tau^b_i\log Z^b_i$ inherits all of these.
Raw $D_{\rm KL}$ is worse still: it is asymmetric with unbounded asymmetry (a point
mass against a fair bit gives $\log2$ forward and $+\infty$ reverse), and thresholding
it does not even yield a partition, since KL-threshold adjacency is not transitive
(Bernoulli $1/10\to1/2\to9/10$ at threshold $0.6$).

## 13. Q10 — a minimal finite categorical falsification experiment

The design is fully finite and categorical: no Gaussian family appears, every
quantity is a finite sum of rationals and logarithms of rationals, and every test is
exact to machine precision using rational arithmetic plus high-precision logs. This
is deliberate — a Gaussian implementation cannot falsify the hierarchy mechanism
because its closure properties are special.

### 13.1 The system

* **Agents.** $N=6$, all at one context point $c_\*$. No length, lattice, or tree.
* **Group.** $G=\mathbb Z_3$, with **two distinct representations**: $\rho_b(k)$ acts
  on $\mathsf Z^b=\mathbb Z_3$ by cyclic shift $z\mapsto z+k$; $\rho_m(k)$ acts on
  $\mathsf Z^m=\mathbb Z_3$ by $z\mapsto z+2k$. Same group, unlike actions, which is
  the minimal realization of the two-channel structure.
* **States (Reading A).** $\mathsf B_i$ is a declared finite set of laws on
  $\mathbb Z_3$, closed under $\rho_b$-pushforward (a union of $\mathbb Z_3$-orbits;
  ten orbits suffice). $\mathsf M_i$ is a finite set of laws on $\mathbb Z_3$ closed
  under $\rho_m$, with a declared evaluator
  $\mathrm{ev}:\mathsf M_i\to\mathrm{Kern}(\mathsf Z^b,\mathcal P(\{0,1\}))$.
  Reference measures are counting measures throughout, so no measure-theoretic
  overhead survives.
* **Graph.** Two directed 3-cycles $1\!\to\!2\!\to\!3\!\to\!1$ and
  $4\!\to\!5\!\to\!6\!\to\!4$, plus cross edges $3\!\to\!4$ and $6\!\to\!1$. The
  skeleton is cyclic by construction.
* **Transports, chosen to separate the channels.** On cycle A take belief shifts
  $(1,1,0)$, giving belief holonomy $2\ne0$ — **nontrivial**; take model shifts
  $(1,1,1)$, giving model holonomy $0$ — **trivial**. On cycle B take both trivial.
  So block $\{4,5,6\}$ admits a stabilized parent in both channels, while
  $\{1,2,3\}$ admits one only in the model channel. That asymmetry is a *prediction*,
  and it is what measurement 4 tests.
* **Records.** $\mathsf O=\{0,1\}^6$; the likelihood attaches only at scale 0.
* **Partition variable inside the model**, with a CRP prior at declared $\vartheta$
  and a declared **capacity bound**: $|\mathsf Z_{1,I}|$ fixed at 3 regardless of
  $|I|$. Proposition 5 of Part 2 says this bound is not optional.

### 13.2 The six measurements, each with a pre-registered falsifier

Run in this order; a failure at any stage invalidates everything downstream.

**(1) VFE accounting.** Compute $\mathcal F_{\rm tower}$ two ways: (a) directly, by
brute-force enumeration of $-\log p_\theta(o\mid X)+D_{\rm KL}(\mathbb Q_\phi\Vert\boldsymbol\Pi)$;
(b) as the sum of the seven conditional-KL groups of Theorem 2. Also compute the
naive sum of local row potentials and report the overcount
$\sum_a(|\partial a|-1)E_{a,o}$.
*Falsifier:* (a) and (b) differ by more than $10^{-12}$. *Secondary falsifier:* an
implementation reports the naive sum as "the ELBO."

**(2) Coarse-edge composition.** Build $C_{10}$ and $C_{21}$, and check that the
event law obtained via $C_{20}=C_{21}C_{10}$ equals the two-step result; likewise for
the endpoint kernels $K_{20}$ versus $K_{21}\circ K_{10}$. Separately compute the
naive uniform row average and report its discrepancy from the event-law pushforward
(Part 2 §8.2 predicts $\ge0.4$ under skewed $\alpha$).
*Falsifier:* composition fails, which in practice means the product form
$K=C\otimes C$ was assumed while the intermediate assignments are correlated.

**(3) Closure residual.** Push the exact law, project onto the declared parent
family, and report
$\Vert(I-\widehat R_{s+1})\widehat T^{\mathcal G}_s(g)\Vert/\Delta s$ against the
retained flow $\Vert\beta^{\rm ret}_s\Vert$. Also detect generated hyperedges by
Möbius inversion, $\Phi^c_A(z_A)=\sum_{B\subseteq A}(-1)^{|A|-|B|}H^c_o(z_B,z^\circ_{B^c})$,
and report the largest three-body coefficient.
*Falsifier:* the residual is not small compared to the retained flow, or the
three-body Möbius coefficient is nonzero while the implementation reports a pairwise
coarse theory. (The Ising-star calculation guarantees the latter is generically
nonzero.)

**(4) Holonomy retention.** For each candidate block and channel, compute
$\mathscr Q^x_{I,\rm fix}(r)$, the score $\mathfrak D^x_I$, and the full conditional
law $\mu^x_{IJ}$ of dressed transports together with $\mathrm{supp}\,\mu^x_{IJ}$ and
the barycenter $\overline{\mathsf U}^x_{IJ}$.
*Prediction:* $\mathfrak D^b_{\{1,2,3\}}>0$ (belief holonomy nontrivial) while
$\mathfrak D^m_{\{1,2,3\}}$ can vanish; both can vanish on $\{4,5,6\}$.
*Falsifier (implementation):* the code reports a holonomy-blind parent while
$\mathrm{supp}\,\mu^x_{\rm loop}\not\subseteq\mathrm{Stab}(Q_I)$.
*Falsifier (theory):* if $\mathfrak D^b_I>0$ for **every** candidate block, then no
zero-distortion belief parent exists anywhere on this cyclic graph, and the
hierarchy mechanism as stated cannot produce an exactly parallel meta-agent —
Proposition 8 in action.
*Falsifier (barycenter):* $\overline{\mathsf U}^x_{IJ}\notin\rho_x(G)$ while the
implementation uses it as a group element.

**(5) Partition persistence.** Run the coupled descent from $K=200$ random
initializations. Measure the co-membership matrix, the modal partition, the
residence time of each partition, and the belief relaxation time $t_{\rm rel}$
(time for $\Vert\dot Z\Vert$ to fall by $e^{-1}$). Sweep the noise amplitude
$\epsilon$ and fit $\log(\text{exit time})$ against $1/\epsilon$.
*Falsifier:* no partition has residence time exceeding $10\,t_{\rm rel}$, i.e. there
is no timescale separation and hypothesis (H1) fails. *Secondary falsifier:* the
exit-time fit is not linear in $1/\epsilon$, i.e. the configuration is not a
metastable basin and "persistence" is a misnomer.

**(6) Downward influence.** Intervene: replace $Z_{s+1}$ by $z'$ and recompute the
child's optimal $Q^\star_s\propto K^s_\downarrow(\cdot\mid z')e^{-\mathcal E_s}$.
Report $\sup_{z'}\Vert Q^\star_s(\cdot\mid z')-Q^\star_s(\cdot\mid z'')\Vert_{TV}$.
Run the **deterministic-pushforward control**: replace $K^s_\downarrow$ by the
$C$-fiber disintegration of Proposition 3(a) and verify that the same supremum
collapses to the within-fiber variation only.
*Falsifier:* the supremum is zero for the declared $K_\downarrow$, i.e. the
"meta-agent" exerts no downward influence and is decorative. *Confirmation of
Proposition 3:* the control does collapse, operationalizing the impossibility.

**Null control (mandatory).** Rerun the whole pipeline with i.i.d. uniformly random
$\Omega^b,\Omega^m$ and i.i.d. random beliefs, with the graph skeleton unchanged. If
blocks "form" and persist there too, the pipeline is detecting the blocking
algorithm rather than the system.

### 13.3 Why this falsifies before any Gaussian implementation

Every failure mode above is generic and none is Gaussian-specific: nontrivial
holonomy on a cycle, non-group-valued barycenters, generated three-body terms,
correlated endpoint assignments, and partition degeneracy all occur in the smallest
finite categorical model. A Gaussian implementation would additionally have to
contend with the fact that Gaussian projection does not preserve nonlinear boundary
actions — equally weighted children $\mathcal N(\pm a,1)$ with $H(x)=\lambda x^4$
leave a signed residual $2\lambda a^4$ — so a Gaussian run cannot separate a real
failure of the mechanism from a failure of the Gaussian ansatz.

## 14. Claim table

Statuses: **E** established (proved here or in the live theory, with the proof
present); **C** conditional (holds under stated hypotheses not verified for the
present system); **J** conjecture; **N** numerical/diagnostic only; **O** open.

| # | Claim | Status | Where |
|---|---|---|---|
| 1 | $\mathcal F^{\rm ext}_{\rm tower}=-\log p_\theta(o\mid X)+D_{\rm KL}(\mathbb Q_\phi\Vert\boldsymbol\Pi)$ in $\mathbb R\cup\{+\infty\}$ | **E** | P1 §1 |
| 2 | The depth-$S$ tower is normalized with no partition function, **provided every scale is indexed by its fixed label pool**; indexing by random occupied sets is ill-typed | **E** | P1 Prop. 1, §3.1 |
| 3 | Exact seven-group conditional-KL decomposition under a common ordering | **E** | P1 Thm. 2 |
| 4 | Observation term is the only term that can be $-\infty$; $\mathbb E_{\mathbb Q}(\log L)^+<\infty$ suffices | **E** | P1 §4.3 |
| 5 | $\mathcal P(\mathsf Z)$ standard Borel for standard Borel $\mathsf Z$, so "state is a law" is well typed | **E** | P1 §1.1 (Kechris 17.23) |
| 6 | $\Phi^b_i,\Phi^m_i$ are exact VFE sectors **only** under Reading A + label exclusivity + constant-row recognition + $D\mapsto\mathbb E_{\mathbb Q}D$ + $\tau=1$ | **E** | P1 §1.2 |
| 7 | Under Reading B, $\Phi$ violates the typing prohibition and is a composite potential | **E** | P1 §1.1–1.2 |
| 8 | $\beta^{Q\star}_i\ne\mathbb E_{Q_Y}\beta^P_i(Y)$ in general | **E** | P1 §1.2 |
| 9 | Summing singleton local potentials overcounts by $\sum_a(|\partial a|-1)E_a$ | **E** | P1 §4.4 |
| 10 | Marginals do not determine the correlated recognition joint | **E** | P1 §4.1 |
| 11 | Local normalization does not give a finite $Z_X$ | **E** | P1 §1 |
| 12 | Deterministic pushforward forces $P_1=C_\#\nu$ and $K_\downarrow$ = fiber disintegration | **E** | P2 Prop. 3(a) |
| 13 | Such a parent contributes zero conditional randomness | **E** | P2 Prop. 3(b) |
| 14 | Free parent prior + deterministic pushforward is generically inconsistent | **E** | P2 Prop. 3(c) |
| 15 | Deterministic constraint + Gibbs density against nonatomic reference gives $Z_\psi=0$ | **E** | P2 Prop. 3(d) |
| 16 | Both arrows as generative factors form a directed 2-cycle with no normalization | **E** | P2 Prop. 3(e) |
| 17 | Exactly three normalized repairs (recognition demotion / delay / undirected Gibbs) | **E** | P2 §6.4 |
| 18 | Partition update is the Gibbs posterior $Q^\star_R\propto P_R e^{-U_s}$ | **E** | P2 Prop. 4 |
| 19 | $\tau_R\ne1$ is an ELBO sector only for the rescaled energy $E/\tau_R$ | **E** | P2 §7.2 |
| 20 | **Without a capacity bound the tower VFE is exactly constant across partitions** | **E** | P2 Prop. 5 |
| 21 | Hence $Q^\star_R=P^s_R$: hierarchy selection lives entirely in declared restrictions | **E** | P2 Cor. 6 |
| 22 | Capacity bound and node-count cost are **sufficient** design mechanisms, one per degeneracy; joint necessity is **open** | **E** / **O** | P2 §7.3 |
| 23 | Event-law pushforward + disintegration is normalized, gauge-invariant, composes | **E** | P2 §8.1, §8.5 |
| 24 | Row averaging $\ne$ event-law pushforward (explicit $0.4$ discrepancy) | **E** | P2 §8.2 |
| 25 | Zero-occupancy parent rows are not invariants of the coarse law | **E** | P2 §8.3 |
| 26 | Replicated covers are not Markov kernels and double mass | **E** | P2 §8.3 |
| 27 | $C^b\ne C^m$ needs a declared correspondence; common refinement may not coarsen | **E** | P2 Prop. 7 |
| 28 | Product endpoint form is not preserved under nested composition without independence | **E** | P2 §8.5 |
| 29 | On the zero-distortion sector, $H_\#Q=Q$ is necessary and sufficient | **E** | P3 §9.2(A) |
| 30 | Flatness $\Rightarrow$ stabilization; flatness $\not\Rightarrow$ agreement; stabilization $\not\Rightarrow$ flatness | **E** | P3 §9.2(B) |
| 31 | **Empty $\mathrm{Fix}(\mathrm{Hol})\cap\mathscr M$ makes a zero-distortion parent nonexistent** | **E** | P3 Prop. 8 |
| 32 | Exact coarse connection datum is the conditional law $\mu^x_{IJ}$, not a mean; its numerator must carry the endpoint factor $K^x(I,J\mid i,j)$ or it is unnormalized under soft membership | **E** | P3 §9.4 |
| 33 | Barycenter of $\mu$ need not lie in $\rho_x(G)$; first moment may not exist | **E** | P3 §9.4 |
| 34 | Conditional independence of consecutive marks is **sufficient** for coarse transports to convolve; the converse is **false** (Z_3 witness C25) | **E** | P3 Prop. 9 |
| 35 | Coarse holonomy blindness $\iff \mu_{\rm loop}(\mathrm{Stab}(Q_I))=1$ (measure-one; the support form needs a declared topology) | **E** | P3 §9.4 |
| 36 | Uniform low transported KL produces **no** block ($\beta^\star=\pi$) | **E** | P3 §10.2 |
| 37 | Large $\eta$ ranks hubs, not blocks | **E** | P3 §10.3 |
| 38 | KL-threshold adjacency is not transitive, so it induces no partition | **E** | P3 §10.2 |
| 39 | Child update: parent kernel acts as the child's prior | **E** | P3 §11.1 |
| 40 | Parent update: $Q^\star_{s+1}\propto P_{s+1}e^{-\mathcal V_{s+1}}$ where $\mathcal V_{s+1}$ collects **all four** parent-dependent conditional divergences ($R,G,H$, downward kernel), not the downward term alone | **E** | P3 §11.1 |
| 41 | Per-scale natural gradient $=$ tower natural gradient **iff** cross-scale Fisher orthogonality | **E** | P3 §11.2 |
| 42 | $\Delta^{\rm ng}=0$ needs both $c$-measurability of $\Delta$ and horizontal conformality | **E** | P3 §11.3 |
| 43 | Strong lumpability is the every-initial-law condition; weak is strictly weaker | **E** | P3 §11.3 |
| 44 | Fisher equality at a point is not experiment recovery | **E** | P3 §11.3 |
| 45 | **One scalar + symmetric mobility ⇒ LaSalle convergence; participatory feedback alone changes nothing** | **E** | P3 Prop. 10 |
| 46 | NESS requires driven controls, a non-gradient (antisymmetric) sector, delay, or non-gradient drift with noise | **E** | P3 §11.6 |
| 47 | $L^x=\mathrm{diag}(\alpha^x)-\eta^x$ is gauge-invariant with exactly zero row sums | **E** | P4 §12.3 |
| 48 | **Perron occupancy $\Rightarrow$ symmetrization preserves occupancy and equals Chung's Laplacian** | **E** | P4 Prop. 11 |
| 49 | Effective resistance/commute time on $L^{\rm sym}$ are genuine gauge-invariant metrics | **E** | P4 §12.3 (Klein–Randić) |
| 50 | Transported Fisher–Rao is a pseudometric; path independence needs stabilization | **E** | P4 §12.3 |
| 51 | $1/\beta$, $\ell_{ij}$, and $D_{\rm KL}$ are not metrics | **E** | P4 §12.3 |
| 52 | BKS does not treat directed graphs, partitions, or holonomy (primary-checked) | **E** | P4 §12.1 |
| 53 | BKS stiff↔relevant is interpretive; §3.1 spectral vs §4.2 diagonal mismatch | **E** | P4 §12.1 (vault-recorded, primary-consistent) |
| 54 | The network-RG review names coupled topology+dynamics renormalization as **open** | **E** | P4 §12.2 (partially re-verified) |
| 55 | Review §6 heading list as quoted | **N** | P4 §12.2 — vault-recorded, **not** re-verified verbatim this session |
| 56 | Mean-field coherence instability $2Jc\rho_0>a$ with quartic correction | **C** | P3 §10.1 (declared composite potential, mean field) |
| 57 | Grand-canonical occupation law and conjugacy $-\partial\Phi_E/\partial\mu=\rho^\star$ | **E** (as algebra) / **C** (as physics) | P3 §10.1 |
| 58 | Descent on a generic cyclic graph produces persistent scale-1 blocks | **O** | P3 §10.5 |
| 59 | ... and then scale-2 blocks | **O** | P3 §10.5 |
| 60 | Existence of a rescaling/identification kernel $I_b$ making $K_b=C_bI_b$ a semigroup | **O** | P2 §8.6 |
| 61 | A beta function, blocking ratio, or relevant/irrelevant classification for this network | **O** | P2 §8.6 |
| 62 | Two-channel group-valued analogue of the MSM uniqueness theorem | **O** | P4 §12.2 |
| 63 | Bayesian-RG bridge (common state space, transported Fisher, monotone) | **O** | P4 §12.1 |
| 64 | Semiconjugacy of the recomputed coarse natural gradient | **O** | P3 §11.3 |
| 65 | Thermodynamic/infinite-volume limit; continuum reference measure | **O** | P1 §4.3 |
| 66 | Physical-time identification of $t$ or $\tau_F$ | **O** | P3 §11.5 |
| 67 | Canonical, relabeling-natural, gauge-compatible nondegenerate partition selector | **O** | P2 §7.3 |
| 68 | Autonomous agency; participatory nonequilibrium as a distinguishable model | **O** | P3 §11.6 |
| 69 | Two-channel spectra $C^b,C^m$ peaking at a common $\tau^\*$ on real systems | **J** | P4 §12.3 |
| 70 | Consecutive coarse-edge marks are conditionally independent (needed for convolution) | **J** | P3 Prop. 9 |
| 71 | Renormalizability universally means additivity of the defining parameter | **REFUTED** | P4 §12.2 — the $\phi$-GRW family closes at every $\phi$; closure is protocol-relative |
| 72 | $\phi=1$ is the unique $\phi$-norm that is a fixed input-independent Markov pushforward, hence the only one compatible with the exact KL chain rule | **E** | P2 §8.1 |
| 73 | A $\sup$ or $\phi$-norm rule on the effective-resistance scale proposes usable blocks here (mechanism M5) | **J** | P3 §10.1 — protocol only; no self-similarity, hidden-degree recursion, or angular-sector result transfers |
| 74 | Mechanism M5 lies outside the exact $\eta$ pushforward and discards directionality via the symmetrized Laplacian | **E** | P3 §10.1 |
| 75 | A directed $\phi$-family preserving both semigroup composition and Markov pushforward | **O** | P3 §10.1; named as future work by Zheng et al. |

## 15. The strongest defensible theorem

**Theorem A (exact finite-depth two-channel multiscale VFE with partition,
connection, and mark variables inside the model).**
Assume: (i) the typing of Part 1 §3.1, with every space nonempty standard Borel,
every reference $\sigma$-finite, and belief coordinates valued in $\mathcal P(\cdot)$
(Reading A); (ii) the ordered generative factorization of Part 1 §3.2 with every
factor a normalized measurable Markov kernel, the likelihood attached only at scale
$0$, and $p_\theta(o\mid X)\in(0,\infty)$; (iii) a recognition law disintegrated
along the same ordering with $\mathbb Q_\phi\ll\boldsymbol\Pi_{\theta,o,X}$; (iv)
$\mathbb E_{\mathbb Q_\phi}(\log L_\theta(o\mid Z_0,X))^{+}<\infty$. Then:

1. $\mathbb P_\theta(\cdot\mid X)$ is a probability measure and the tower carries no
   normalizer other than the evidence.
2. $\mathcal F^{\rm ext}_{\rm tower}=-\log p_\theta(o\mid X)+D_{\rm KL}(\mathbb Q_\phi\Vert\boldsymbol\Pi_{\theta,o,X})$
   holds in $\mathbb R\cup\{+\infty\}$ and equals the seven-group sum of Theorem 2,
   with the observation term the only one that can be negative.
3. The $R_s$-coordinate minimizer is $Q^\star_R\propto P^s_Re^{-U_s}$ with $U_s$ the
   derived sum of graph, mark, and cross-scale conditional divergences; the
   $Z_{s+1}$-coordinate minimizer at frozen child kernel is
   $Q^\star_{s+1}\propto P_{s+1}e^{-\mathcal V_{s+1}}$ with
   $\mathcal V_{s+1}(z)=D_{\rm KL}(Q_s(\cdot\mid z)\Vert K^s_\downarrow(\cdot\mid z))$.
4. Pushing the joint directed edge-event laws $\eta^b,\eta^m$ through normalized
   incidence-supported endpoint kernels and disintegrating gives normalized,
   gauge-invariant coarse occupancies and rows that compose exactly under nested
   normalized memberships, on positive parent occupancy.
5. The scale-to-scale VFE loss under one common recognition-independent channel is
   the nonnegative conditional-information defect $\Delta$, additive in
   $[0,+\infty]$, with $\Delta=0$ exactly when the discarded conditional recognition
   and posterior laws agree almost surely; ordinary subtraction requires finite fine
   KL.
6. Non-flat holonomy is retained exactly as the simultaneous root-framed orbit
   $(\bar z^x_I,H^x_I,\{V^x_e\})$ together with the conditional law $\mu^x_{IJ}$ of
   dressed transports, and no flatness is imposed.

**And, in the same breath, what Theorem A does not give.** It supplies no partition
selector — indeed by Proposition 5 the objective is *exactly* partition-blind absent
a declared capacity bound; no block-persistence theorem; no rescaling/identification
kernel, hence no RG semigroup, no beta function, no blocking ratio, and no
relevant/irrelevant classification; no cross-scale dynamical closure; no sustained
nonequilibrium (Proposition 10 forbids it within one scalar with symmetric
mobility); no continuum or thermodynamic limit; no physical time; no autonomous
agency; and no unique latent DAG, unique hierarchy, or unique microscopic physics.

## 16. Unresolved proof obligations, ordered

1. **Capacity axiom.** State and defend the declared restriction on
   $(\mathsf Z_{s+1},K^s_\downarrow,P_{s+1})$ that makes the partition posterior
   differ from its prior. Without it Corollary 6 makes every hierarchy claim vacuous.
   This is now the *first* obligation, not a refinement.
2. **Nondegenerate, relabeling-natural, gauge-compatible partition selector**
   satisfying $S(P\cdot X)=PS(X)Q^\top$, reducing gauge-carrying inputs to invariant
   assignment scores, and compatible with the holonomy admissibility of
   Proposition 8.
3. **The rescaling kernel $I_b$.** Construct a rescaling/identification kernel
   returning coarse states to a common measurable space with
   $K_{b_1b_2}=K_{b_1}K_{b_2}$. Until then this is a consistent family of
   coarse-grainings, not an RG.
4. **Persistence theorem.** Prove or refute (H1)–(H6) for the actual coupled flow on
   a generic cyclic graph, with a metastability statement (exit time versus noise),
   not merely a local-minimum statement.
5. **Cross-scale closure.** Either prove
   $T_\ell(\mathrm{Ran}\,R_\ell)\subseteq\mathrm{Ran}\,R_{\ell+1}$ or carry
   $\delta\beta_\ell$ with a two-sided norm bound; account for the hyperedges that
   exact closure generates.
6. **Semiconjugacy.** Prove or refute $\Delta^{\rm ng}=0$ for the recomputed coarse
   natural gradient, separating the $c$-measurability condition from horizontal
   conformality.
7. **Mark composition.** Prove or refute conditional independence of consecutive
   dressed marks (Proposition 9) for the declared blocking, or supply the joint law
   and its correlation defect.
8. **Two-channel MSM uniqueness.** Formulate and attempt: is the additive edge-event
   family the unique two-channel gauge-covariant family form-invariant under all
   normalized membership kernels?
9. **Bayesian-RG bridge.** Common state space, transported Fisher tensors, declared
   scale map, proved monotone; and a resolution of the spectral-versus-diagonal gap
   before importing the shell criterion.
10. **Nonequilibrium mechanism.** Declare which of driven controls, antisymmetric
    sector, delay, or non-gradient stochastic drift is intended, and supply the
    corresponding flux or work accounting plus an observable distinguishing it from a
    hierarchical latent-variable model.
11. **Continuum/thermodynamic limit.** The concrete obstruction is the reference
    measure: a finite product of $\sigma$-finite factors is $\sigma$-finite, an
    infinite product of non-probability factors is not. Any continuum theory must
    declare a measure on the section space directly.
12. **Cross-model verification.** Nothing here has been checked by an independent
    model. Every derivation in Parts 1–4 is single-author.

## 17. Staged simulation program

Each stage has an exit gate; do not proceed past a failed gate.

**Stage 0 — exact arithmetic harness.** Finite categorical system of §13.1 in
rational arithmetic (`fractions.Fraction`) with high-precision logs. Enumerate
$\mathsf O$, $\mathsf B$, $\mathsf M$ exhaustively. *Gate:* measurement (1) agrees to
$10^{-12}$ and the overcount $\sum_a(|\partial a|-1)E_a$ is reported explicitly.

**Stage 1 — event-law coarse-graining.** Implement the $\eta$-push and
disintegration for both channels, hard and soft memberships, with the zero-occupancy
convention and the replicated-cover guard. *Gate:* measurement (2), including a
reported nonzero discrepancy against naive row averaging and an explicit failure when
endpoint independence is violated.

**Stage 2 — connection data as a distribution.** Implement $\mu^x_{IJ}$ as an
explicit finite measure on $\mathbb Z_3$; compute $\mathrm{supp}$, barycenter, and the
convolution test of Proposition 9. *Gate:* measurement (4)'s barycenter and support
falsifiers both run and the two channels' holonomies are reported separately.

**Stage 3 — partitions inside the model.** Add $R_s$ with a CRP prior and the
declared capacity bound; implement the Gibbs update of Proposition 4. *Gate:* run the
**degeneracy control** first — remove the capacity bound and verify that
$\min\mathcal F$ is constant across partitions to $10^{-12}$ (Proposition 5). If that
control does not reproduce, the implementation does not match the theory.

**Stage 4 — coupled descent and persistence.** Natural-gradient flow with the full
(non-block-diagonal) Fisher metric, projected on the simplices; noise sweep and
exit-time fit. *Gate:* measurement (5), with the null control of §13.2 run in
parallel.

**Stage 5 — intrinsic scales and cross-scale dynamics.** Build $L^{x,\rm sym}$ under
Perron occupancy (Proposition 11), compute $C^b(\tau)$, $C^m(\tau)$, effective
resistances, and transported Fisher–Rao distances; compare the blocks each proposes
against the inferred $Q^\star_R$. Then measure the closure residual and
$\Delta^{\rm ng}$ directly. *Gate:* measurements (3) and (6). Only after this gate is
it meaningful to ask whether a rescaling kernel $I_b$ can be constructed.

**Stage 6 (only if Stage 5 passes) — nonequilibrium.** Add exactly one mechanism from
§11.6, measure entropy production or circulation directly, and compare against the
gradient-flow control that Proposition 10 predicts must relax.

## 18. Scope and limitations

* **Theorems** here are Propositions 1, 3, 4, 5, 7, 8, 9, 10, 11, Corollary 6, and
  Theorem 2/A, each proved in text from stated hypotheses. Proofs of results imported
  from the live theory are cited by label, not reproduced.
* **Constructions** are the typed joint of Part 1 §3.2, the coarse connection
  distribution $\mu^x_{IJ}$, and the gauge-invariant Laplacian family of Part 4 §12.3.
* **Modeling postulates**, declared as such: Reading A of the belief coordinate; the
  capacity bound; label exclusivity; constant-row recognition; endpoint independence.
* **Operational identifications** are absent. No object here is identified with a
  physical clock, energy, reservoir, particle number, or spacetime.
* **Physical interpretation** is limited to the thermodynamic *mathematics* of Gibbs
  ensembles in the sense of Jaynes. Multiplying a VFE in nats by $k_{\rm B}T$ requires
  a separate operational bridge that is not supplied.
* **Analogy** is used only where labeled: the lattice-gas reading of edge occupation,
  the Wilsonian reading of the diffusion cutoff.
* **Numerical observations**: none were executed in this session. Every number in
  §13 is a design target, not a result. Row 55 of the claim table is the one item
  carried on vault provenance rather than a primary check performed here.
* **Verification**: no cross-model verifier was dispatched, because the session
  prohibits subagents. Under the project's own cross-model rule an Opus-authored
  derivation must be checked by a different model before any durable verification
  state is assigned. Accordingly **no claim above carries `EVIDENCE_VERIFIED`**; the
  terminal status of this run is INCONCLUSIVE in the technical sense of the
  rigorous-theory-search protocol, meaning: strongest verified result stated, minimal
  unresolved obligation set named, closure evidence still needed.
