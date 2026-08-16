# Adversarial attack portfolio

Author model: Claude Opus 5. **No cross-model verifier was dispatched** (the session
prohibits subagents), so these attacks are self-adversarial. Under the project's
cross-model rule this is why no claim in this run reaches `EVIDENCE_VERIFIED`.

## A1 — against `construction` (the normalized finite-depth joint)

*Attack.* The tower joint is claimed normalized without a partition function, but it
contains a membership variable $R_s$ whose *support* (the occupied vertex set
$V_{s+1}$) is itself random. A random index set breaks the fixed-measurable-space
requirement and with it the reverse-order Tonelli argument, because the later
factors $P^s_G$, $K^s_\downarrow$ would be kernels into a space that depends on the
value of an earlier variable. Concretely: pool $\{A,B\}$, a random partition that
sometimes occupies only $\{A\}$, and the target space of $P_S$ changes with a
variable sampled downstream of it.

*Response.* **SUSTAINED** on external review (PR #17, finding H1). The original
response asserted that fixed finite label pools fix every later codomain. That is
the correct repair, but the body of Part 1 nonetheless indexed $Z_s$, $G_s$, and
the rows by the **random occupied sets** $V_s$ — the pools appeared in the prose and
were never used as the index. The repair was described and not implemented, so
marking this `REJECTED` was itself an error, and a more damaging one than missing
the attack, because it converted an open question into a false clearance.

Repaired: Part 1 §3.1, the architecture diagram, and
`construction-or-strongest-theorem.md` now index every scale-$s$ object by the fixed
pool $\Lambda_s$, with occupancy the derived predicate $\alpha^{x,s}_A>0$ and the
measurable disjoint union recorded as the equivalent alternative. The review's
second point — that differing $C^b,C^m$ leave no common occupied index for a shared
parent state — is handled by routing through Proposition 7's declared
correspondence, which Part 2 §8.4 already established and §3.1 had ignored.
*Falsifies this repair:* a factor in Part 1 §3.2 whose codomain still depends on a
realized value rather than on the pool.

*Disposition:* SUSTAINED, repaired.

## A2 — against `decomposition` (the seven-group conditional-KL identity)

*Attack.* The identity sums seven groups of terms, one of which
($-\mathbb E\log L$) can be negative and one of which ($D_{\rm KL}(Q_S\Vert P_S)$)
can be $+\infty$. A sum containing both is at risk of $\infty-\infty$, so the
"identity in $\mathbb R\cup\{+\infty\}$" is not justified as stated.

*Response.* Partially sustained, and the report already carries the fix as a stated
hypothesis rather than burying it. The six nonnegative groups sum unambiguously in
$[0,+\infty]$. The observation group is the only signed one, and Part 1 §4.3 imposes
$\mathbb E_{\mathbb Q}(\log L_\theta(o\mid Z_0,X))^{+}<\infty$, which bounds its
*negative* excursion and makes the total well defined in $\mathbb R\cup\{+\infty\}$.
What remains genuinely open is that this is a sufficient condition presented without
a matching necessity proof; the report says "essentially sharp," which is a hedge and
is recorded as such. *Falsifies:* a model with
$\mathbb E(\log L)^+=\infty$ and finite total VFE, which would show the condition is
not necessary; or one satisfying the condition with an ill-defined sum, which would
show it is not sufficient.

*Disposition:* PARTIALLY_SUSTAINED. Smallest unresolved obligation: prove or refute
necessity of the integrability condition.

## A3 — against `degeneracy` (Proposition 5, partition-blindness)

*Attack.* Proposition 5 chooses $\mathsf Z_{1,I}=\mathsf Y_{0,I}$ and
$K^0_I=\delta$, which is a *degenerate* hierarchy — the parent is a literal copy of
its children. Real modelers never do that, so the proposition attacks a straw model
and does not show that a sensible tower is partition-blind.

*Response.* Rejected. The proposition is a **necessity** result, not a description of
practice: it establishes that partition selection cannot come from the variational
principle alone, because there exists an admissible tower in which the objective is
exactly constant across partitions. That is precisely what is needed to show a
capacity restriction is *required*, and it is the proof of the manuscript's own
unproved assertion that "no canonical selector follows from the global VFE alone."
The copy construction is admissible under the stated hypotheses (block-factorized
$K_\downarrow$, normalized kernels, unrestricted parent space), so it is a legitimate
witness. *Falsifies:* showing the copy construction violates a hypothesis actually
imposed in Part 1 §3.2 — e.g. if $\mathsf Z_{s+1}$ were required a priori to be
strictly smaller than $\mathsf Y_s$, in which case the capacity bound is already
assumed and the proposition's conclusion is what one wanted anyway.

*Disposition:* REJECTED.

## A4 — against `parent-impossibility` (Proposition 3)

*Attack.* Part (d) claims a Gibbs presentation fails because the graph of $C$ is
$(\mu\otimes\lambda)$-null. But nobody imposes an *exact* deterministic constraint in
a Gibbs model; they use a soft penalty. So (d) refutes something no one asserts, and
the trichotomy in §6.4 is not exhaustive because "soft constraint" is a fourth option.

*Response.* Partially sustained on presentation, rejected on substance. The report
already states that the soft version "is a different model with a different (and
still unproved) $Z_\psi$," so a soft penalty is not a fourth option but an instance of
mechanism (iii) — an undirected Gibbs factor, carrying its own normalizer obligation
(and the Gaussian $e^{cy_1y_2}$ witness shows that obligation is not automatic).
Part (d) is aimed at the specific combination the problem statement asks about, namely
an *instantaneous deterministic pushforward* imposed together with a reciprocal
factor. *Falsifies:* a soft-constrained reciprocal model with a proved finite $Z_\psi$
that also reproduces an exact deterministic pushforward in a limit while keeping
$Z_\psi$ finite along the way.

*Disposition:* PARTIALLY_SUSTAINED. Smallest unresolved obligation: state the soft
reciprocal model explicitly and prove or refute finiteness of its normalizer.

## A5 — against `holonomy-obstruction` (Proposition 8)

*Attack.* The witness uses the admitted family $\{\delta_a:a\ne0\}$, which excludes
$\delta_0$ by hand. Any reasonable admitted family is closed and contains the fixed
point, so the "obstruction" is an artifact of an artificial family.

*Response.* Rejected. Equivariance of the admitted family
($(T_\gamma)_\#\mathscr M_i=\mathscr M_j$) is the hypothesis actually used elsewhere
in the theory, and $\{\delta_a:a\ne0\}$ satisfies it under $a\mapsto-a$. Nothing in
the theory requires the family to contain its own fixed points; requiring that is
exactly the extra hypothesis Proposition 8 identifies as necessary. The physically
serious version is not the Dirac example but the general statement
$\mathrm{Fix}(\mathrm{Hol}^x_r)\cap\mathscr M^x_r=\varnothing\Rightarrow\mathfrak D^x_I=+\infty$,
which is a support condition on the admitted family and is checkable case by case.
*Falsifies:* a theorem showing every equivariant admitted family used in this program
is closed and contains a $\mathrm{Hol}$-fixed point.

*Disposition:* REJECTED.

## A6 — against `nonequilibrium` (Proposition 10)

*Attack.* Proposition 10 assumes $M(u)$ symmetric positive definite and $\Psi\in C^1$
globally. Real implementations use state-dependent, sometimes indefinite,
preconditioners and nonsmooth projections onto simplices, so the LaSalle conclusion
does not apply and the claim "participatory feedback changes nothing" is overstated.

*Response.* Partially sustained. The proposition is conditional and is labeled as
such; its content is that the *stated* hypotheses are exactly what must be broken, and
it enumerates the four ways to break them. A nonsmooth projection or an indefinite
preconditioner is a legitimate fifth route and is not listed. However, a projected
gradient flow onto a convex set still decreases the objective, so simplex projection
alone does not produce nonequilibrium; an indefinite $M$ does, but it is then not a
metric and the flow is no longer a natural gradient. *Falsifies:* exhibiting a
projected natural-gradient flow on the simplices with symmetric positive-definite $M$
and one $C^1$ scalar that has a nonconstant $\omega$-limit set.

*Disposition:* PARTIALLY_SUSTAINED. Smallest unresolved obligation: extend or refute
Proposition 10 for projected flows on the simplex boundary and for indefinite
preconditioners.

## A7 — against `literature` (the BKS and network-RG adjudication)

*Attack.* The report relies on the project's Obsidian vault notes for several
statements about the primary papers, including the §6 open-problem headings of the
network-RG review. A vault note is a secondary source and citing it as if it were the
primary is exactly the failure mode the problem statement warned against.

*Response.* Sustained in part, and disclosed at the point of use. Verified against the
primary in this session: both papers' titles, author lists, version dates, journal
references, and abstracts; BKS Eq. (44) and Eq. (55); and the fact that BKS treats no
directed graph, network partition, or holonomy. **Not** re-verified in this session:
the exact §6 heading list of arXiv:2412.12988, because both the HTML and PDF fetches
truncated before §6. That item is marked **N** (row 55 of the claim table) and is
explicitly labeled vault-recorded. Partial primary confirmation was obtained that the
review does not claim any framework solves coupled topology-and-dynamics
renormalization. *Falsifies:* a successful fetch showing the §6 headings differ from
the recorded list.

*Disposition:* PARTIALLY_SUSTAINED. Smallest unresolved obligation: re-fetch §6 of
arXiv:2412.12988 and confirm or correct row 55.

## A8 — against `target` (the run's compound target as a whole)

*Attack.* The target is a conjunction — construct, derive, and decide selection — and
the run closes only the first two conjuncts while the third is answered negatively
only under a hypothesis (unrestricted parent). So the release should not claim to
have addressed the target at all.

*Response.* Partially sustained, and this is why the terminal status is INCONCLUSIVE
rather than complete. Conjunct 1 (construction) and conjunct 2 (decomposition) are
discharged by derivation. Conjunct 3 is answered in the *negative for the unrestricted
case* by Proposition 5, which is a scope-matched counterexample to "descent alone
selects a nondegenerate partition"; but the positive question — whether some declared
capacity bound makes descent select persistently — remains open, so the compound
target is not closed in either direction. Each conjunct receives a disposition in
Part 4 §14–§16 rather than being absorbed into a single verdict.

*Disposition:* PARTIALLY_SUSTAINED. Smallest unresolved obligation: obligations 1, 2,
and 4 of Part 4 §16.

## A9 — against `decomposition` and `holonomy-obstruction` (external review PR #17)

*Attack.* Six further defects, raised externally rather than by this package's own
adversarial pass. H2: the parent Gibbs update omits the membership, graph, and
holonomy conditional divergences that also condition on $Z_{s+1}$. H3: the
dressed-transport law omits the soft endpoint factor $K^x(I,J\mid i,j)$ and is
therefore unnormalized outside hard partitions. H4: the convolution statement was
promoted to an `iff` whose converse is false. M1: Theorem 2 omits its integrability
premise. M3: flatness was said not to imply stabilization, though the identity
stabilizes every law. M4: a support inclusion and a closed stabilizer were asserted
at a tier with no declared topology.

*Response.* All six sustained and repaired, with three new witnesses added to the
counterexample register. $\mathcal V_{s+1}$ now sums the four parent-dependent
conditional divergences, and C26 shows the truncated form moves the argmin rather
than merely the value. The $\mu^x_{IJ}$ numerator now carries the endpoint factor,
with C27 exhibiting total mass $2$ or $0$ under a split child; the restricted form
survives only for hard assignment. Proposition 9 keeps the forward implication
only, with C25 ($\mathbb Z_3$, $U$ uniform, $V=U$) refuting the converse. Theorem 2
lists integrability as hypothesis (iv) and states that it is not implied by
positive finite evidence plus absolute continuity. Section 9.2(B) now states the
chain rather than a mutual independence. The blindness criterion reads
$\mu^x_{
m loop}(\mathrm{Stab}(Q_I))=1$, with the support form deferred to a
declared topological tier.
*Falsifies this repair:* any of the six restated claims failing on its own terms —
for instance a parent-dependent factor still missing from $\mathcal V_{s+1}$, or a
soft-membership configuration on which the corrected $\mu^x_{IJ}$ is still not a
probability measure.

*Disposition:* SUSTAINED, repaired.
