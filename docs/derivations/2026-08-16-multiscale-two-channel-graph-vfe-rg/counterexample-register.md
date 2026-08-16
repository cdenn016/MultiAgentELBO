<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-7d2c4a48da6b18e0d1dd177ba0e42e6ab6b625410e5cbefa9c9031dcfb9dd985","schema_version":"rigorous-theory-search/v1","target_digest":"7d2c4a48da6b18e0d1dd177ba0e42e6ab6b625410e5cbefa9c9031dcfb9dd985"} -->
# Counterexample register

Each entry is an exact construction, not a numerical observation. Entries marked
[live] are established results of the project's own theory reused here with citation;
entries marked [new] are constructed in this run.

## C1 [new] Partition-blindness of the tower VFE — Proposition 5, Part 2 §7.3

Refutes: "descent of one multiscale VFE ranks partitions."
Construction: depth $S=1$; for every candidate partition $R$ take
$\mathsf Z_{1,I}:=\mathsf Y_{0,I}$, $K^0_I(dz_{0,I}\mid z_{1,I}):=\delta_{z_{1,I}}$,
$P_1:=\mathbb P^{\rm flat,Z_0}$. Then $\prod_I\delta_{z_{1,I}}=\delta_{z_1}$, so the
block factorization is respected, and the $(o,Z_0)$-marginal is $\mathbb P^{\rm flat}$
for every $R$. Hence $\min_{\mathbb Q}\mathcal F^{(R)}_{\rm tower}=-\log p^{\rm flat}(o\mid X)$
independently of $R$: all-singleton and all-in-one-block tie with every intermediate
partition. Consequence: $Q^\star_R=P^s_R$, the posterior over partitions equals the
prior, and hierarchy selection is carried entirely by declared capacity restrictions.

## C2 [new] Uniform low transported KL produces no block — Part 3 §10.2

Refutes: "low $D_{ij}$ signals block membership."
Construction: if $\mathbb E_{\mathbb Q}D_{ij}=D$ for every admitted source $j$, then
$\beta^\star_{ij}=\pi_{ij}e^{-D/\tau_i}/\sum_k\pi_{ik}e^{-D/\tau_i}=\pi_{ij}$, exactly
the reference row, for every value of $D$ including $D\to0$. The row responds to
contrast $D_{ij}-D_{ik}$, never to level; a uniform shift $D\mapsto D+c$ moves the
reduced row free energy $-\tau_i\log Z_i$ by the global constant $c$ with zero
distinguishing gradient.

## C3 [new] Large $\eta$ ranks hubs, not blocks — Part 3 §10.3

Refutes: "large edge-event mass signals structure."
Construction: $\alpha_1=0.9$ with $\beta_1$ uniform over $n=4$ sources gives
$\eta_{1j}=0.225$ for each $j$; $\alpha_2=0.05$ with $\beta_{2,3}=1$ gives
$\eta_{23}=0.05$. Ranking by $\eta$ prefers the four maximally uninformative hub edges
over the single perfectly concentrated edge.

## C4 [new] Row averaging is not event-law pushforward — Part 2 §8.2

Refutes: "coarse attention = average the rows over the block."
Construction: $V=\{1,2,3\}$, $\alpha=(0.9,0.1,0)$, $\beta_1=(0,0,1)$,
$\beta_2=(1,0,0)$, $\beta_3=(0,0,1)$; blocks $I=\{1,2\}$, $J=\{3\}$. Event-law
pushforward gives $\beta^c_{II}=0.1$, $\beta^c_{IJ}=0.9$; uniform row averaging gives
$0.5,0.5$. Discrepancy $0.4$, drivable to $1$ by skewing $\alpha$.

## C5 [new] Distinct channel partitions admit no common parent — Part 2 §8.4

Refutes: "optimize the belief and model partitions separately and combine."
Construction: $V=\{1,2,3,4\}$; $C^b$ blocks $\{1,2\},\{3,4\}$; $C^m$ blocks
$\{1,3\},\{2,4\}$. The common refinement is the four singletons, so it achieves no
coarsening; a common partition does not exist; only a declared correspondence kernel
$J:\Lambda^b\rightsquigarrow\Lambda^m$ produces a two-channel parent, at the price of
an extra coarse channel with its own divergence term.

## C6 [new] Holonomy can make a coherent parent nonexistent — Proposition 8, Part 3 §9.2

Refutes: "a cyclic graph is a tree plus extra edges."
Construction: $\mathsf Z^x_r=\mathbb R$, $G=\mathbb Z_2$ acting by $a\mapsto-a$,
admitted equivariant family $\mathscr M=\{\delta_a:a\ne0\}$. Then
$H_\#\delta_a=\delta_{-a}\ne\delta_a$ for every admitted $a$, so
$\mathscr Q_{I,\rm fix}=\varnothing$ and $\mathfrak D^x_I=+\infty$. No zero-distortion
parent exists for that block at any belief configuration.

## C7 [new] Deterministic pushforward plus reciprocal Gibbs factor is unnormalizable — Proposition 3(d), Part 2 §6.4

Refutes: "impose $Z=C(Y)$ and a same-time symmetric factor."
Construction: with $\lambda$ nonatomic on $\mathsf Z$ and
$\mathbb P=Z_\psi^{-1}\psi\,(\mu\otimes\lambda)$, concentration on
$\Gamma_C=\{(y,C(y))\}$ forces $\psi=0$ off $\Gamma_C$; by Fubini each slice
$\{C(y)\}$ is $\lambda$-null, so $\Gamma_C$ is $(\mu\otimes\lambda)$-null and
$Z_\psi=0$.

## C8 [new] Deterministic pushforward plus generative downward kernel has no directed normalization — Proposition 3(e)

Refutes: "the parent is both a function of its children and a generative cause."
Argument: two generative arrows between the same variables at one slice form a
directed 2-cycle; the ordered-kernel composition has no topological ordering and the
reverse-order Tonelli argument of Proposition 1 does not run.

## C9 [live] KL-threshold clustering is not transitive

Bernoulli chain $1/10\to1/2\to9/10$ at threshold $0.6$ nats: first–second and
second–third are linked, first–third is not. KL-threshold adjacency induces no
partition.

## C10 [live] Zero marginal KL does not control the full VFE

Equal fair marginals with disjoint parity and anti-parity joint supports have
identical singleton marginals and infinite full-joint KL.

## C11 [live] Trivial holonomy does not imply belief agreement

Two-node tree, $\Omega=I$, Gaussian means $\pm ae_1$, unit covariance: transported
divergence $2a^2>0$.

## C12 [live] Belief agreement does not imply trivial holonomy

$H=\mathrm{diag}(1,-1,-1)\ne I$ stabilizes an isotropic Gaussian.

## C13 [live] A spectral gap is not an intrinsic agreement scale

Two-node connection Laplacian has gap $2c$, independent of the laws and arbitrary
under rescaling of $c$.

## C14 [live] One-way KL does not control the reverse

Point mass against a fair bit: $\log2$ forward, $+\infty$ reverse.

## C15 [live] Gaussian projection does not preserve nonlinear boundary actions

Equally weighted children $\mathcal N(\pm a,1)$ with $H(x)=\lambda x^4$ leave signed
residual $2\lambda a^4$.

## C16 [live] Replicated covers double mass

One child fully replicated into two parents gives total mass $2$; a replicated cover
is not a Markov kernel.

## C17 [live] Local normalization does not give a finite partition function

On $\mathbb R^2$ with standard normal node potentials and $\psi_{12}=e^{cy_1y_2}$,
$c\ge1$, the exchange precision has eigenvalue $1-c\le0$ and $Z_X=+\infty$.

## C18 [live] Pairwise closure is false

Eliminating the center of an Ising star gives $2\cosh(h_0+\sum_rJ_rs_r)$, whose
negative log has cubic coefficient
$2\,\mathrm{sech}^2(h_0)\tanh(h_0)J_1J_2J_3+O(J^5)$, nonzero for all small nonzero
$J_r$ with $h_0\ne0$.

## C19 [live] An averaged group element need not be a group element

Rotations by $+\pi/2$ and $-\pi/2$ average to the zero matrix.

## C20 [live] Mean marks and mean features do not determine the mean message

Equal-probability pairs $(I,v)$ and $(-I,-v)$ have zero separate means and mean
product $v$.

## C21 [live] Weak lumpability is strictly weaker than strong

Three states with $c(1)=c(2)=a$, $c(3)=\beta$; $1\mapsto3$, $2\mapsto\{1,2\}$
uniformly, $3\mapsto\{1,3\}$ uniformly. Strong lumpability fails, yet started at
$\delta_3$ the coarse process is Markov.

## C22 [live] Infinite KL equality carries no recovery conclusion

$\{a,b,c\}\to\{u,v\}$ with $a\mapsto u$, $b,c\mapsto v$;
$P=\tfrac12\delta_a+\tfrac12\delta_b$, $Q=\tfrac12\delta_b+\tfrac12\delta_c$. Both
divergences are $+\infty$ and no single reverse kernel recovers both.

## C23 [live] Fisher equality at a point is not experiment recovery

Independent Bernoulli coordinates with $\Pr_\theta(A=1)=\tfrac12+\tfrac\theta4$,
$\Pr_\theta(B=1)=\tfrac12+\tfrac{\theta^2}4$, discarding $B$: Fisher informations agree
at $\theta=0$ and are nonzero, yet $\Pr_\theta(B=1\mid A)$ depends on $\theta$.

## C24 [live] A moving generative target need not move the evidence

One binary latent, $Q_\beta=\mathrm{Ber}(\beta)$, $g(\beta)=\beta/2+1/4$,
$P_{\theta,Q_\beta}(o,y)=\tfrac12\mathrm{Ber}(g(\beta))(y)$: the joint varies
injectively in $\beta$ while $e(Q_\beta)=\log(1/2)$ for every $\beta$.
