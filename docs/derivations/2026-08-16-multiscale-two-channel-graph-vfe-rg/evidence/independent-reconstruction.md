# Independent reconstruction

Method: re-derive each load-bearing interface from the frozen problem contract, the
claim ledger, and the dependency DAG only, **without** consulting the narrative of the
report, and check that the cited evidence proves the exact recorded statement rather
than a neighboring one. Performed by the same model that authored the derivations; it
is therefore a reconstruction, not independent-model corroboration. Result: PASS with
three recorded discrepancies, all of which were folded back into the claims before
release.

## Interface 1 — normalization of the tower (`construction`)

Reconstructed from the contract alone: a finite family of variables carrying a partial
order, each factor a Markov kernel conditioning only on strictly earlier variables.
Integrating in reverse order removes one normalized kernel at a time. The only step
needing care is measurability of the partial integrals, supplied by the standard fact
that $\int f(y,\cdot)\,K(y,dz)$ is bounded measurable in $y$ for bounded measurable
$f$. Reconstruction agrees with Proposition 1.

Discrepancy found and fixed: the first pass conditioned $P^s_H$ only on
$(Z_{s+1},R_s)$, which would make the dressed boundary marks independent of the graph
weights they dress. The recorded factorization conditions $P^s_H$ on $G_s$ as well.
This is now the version in Part 1 §3.2 and it is the version used in Theorem 2.

## Interface 2 — the chain rule (`decomposition`)

Reconstructed as an iterated application of
$D_{\rm KL}(Q_{1:k}\Vert P_{1:k})=D_{\rm KL}(Q_{1:k-1}\Vert P_{1:k-1})+\mathbb E\,D_{\rm KL}(Q_k\Vert P_k)$
in $[0,+\infty]$. The recorded claim states an identity in $\mathbb R\cup\{+\infty\}$
*for the full VFE including the signed observation term*, which is strictly stronger
than the chain rule alone.

Discrepancy found and fixed: the integrability hypothesis
$\mathbb E_{\mathbb Q}(\log L)^+<\infty$ is genuinely load-bearing and was initially
implicit. It is now stated in the contract's regularity field, in Part 1 §4.3, and in
Theorem A hypothesis (iv). Attack A2 records that its necessity is unproved.

## Interface 3 — partition-blindness (`degeneracy`)

Reconstructed independently of the report's prose: for any generative law whose
observation marginal is $\mathbb P^{\rm flat,O}$, the infimum of
$-\log p+D_{\rm KL}(\mathbb Q\Vert\boldsymbol\Pi)$ over all $\mathbb Q$ is $-\log p$,
attained at the posterior. Hence the minimum depends on the partition only through the
observation marginal. The witness must therefore only preserve that marginal for every
partition, which the copy construction does. Verified that
$\prod_I\delta_{z_{1,I}}=\delta_{z_1}$, so the block-factorization requirement on
$K_\downarrow$ is respected for every partition — this is the step on which the
proposition actually turns, and it holds.

Discrepancy found and fixed: an earlier reading claimed the *cross-scale KL term* is
zero for every partition. That is true at the optimum but not off it; the recorded
statement is now about $\min_{\mathbb Q}\mathcal F$, not about the term.

## Interface 4 — the parent-influence trichotomy (`parent-impossibility`)

Reconstructed from the contract's requirement that the generative law be a normalized
directed composition. Parts (a)–(c) follow from disintegration over the fibers of $C$;
part (d) from Fubini nullity of the graph against a nonatomic reference; part (e) from
the absence of a topological ordering in a 2-cycle. Each part was checked against the
exact recorded statement. Agreement.

## Interface 5 — holonomy obstruction (`holonomy-obstruction`)

Reconstructed: the score is an infimum over a possibly empty set, with the recorded
convention $\inf\varnothing:=+\infty$. Emptiness is exactly
$\mathrm{Fix}(\mathrm{Hol})\cap\mathscr M=\varnothing$. Checked that the witness family
$\{\delta_a:a\ne0\}$ is equivariant under $a\mapsto-a$, which is the hypothesis the
surrounding theory imposes. Agreement.

## Interface 6 — nonequilibrium (`nonequilibrium`)

Reconstructed from LaSalle: $\dot\Psi=-\nabla\Psi^\top M\nabla\Psi\le0$ with $M\succ0$
gives convergence of bounded trajectories to the largest invariant subset of
$\{\nabla\Psi=0\}$. The recorded claim adds that participatory feedback does not evade
this **provided the enlarged system remains such a flow**, which is a hypothesis and is
recorded as one. Agreement, with attack A6's scope limitation attached.

## Interface 7 — the gauge-invariant Laplacian (`intrinsic-scale`)

Reconstructed the two computations independently:
$\sum_j\eta_{ij}=\alpha_i$ gives zero row sums for $\mathrm{diag}(\alpha)-\eta$; and
under $\phi\beta=\phi$, $\sum_j\eta_{ji}=\sum_j\phi_j\beta_{ji}=\phi_i$, so the
symmetrized occupancy equals $\phi$. Both check. The identification
$(\Phi P)_{ij}=\phi_i\beta_{ij}=\eta_{ij}$ with Chung's symmetrization also checks.
Agreement.

## Coverage

Reconstruction covered: `target`, `construction`, `decomposition`, `degeneracy`,
`parent-impossibility`, `holonomy-obstruction`, `nonequilibrium`, `intrinsic-scale`,
`literature`.
