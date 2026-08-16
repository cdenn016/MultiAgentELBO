<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-7d2c4a48da6b18e0d1dd177ba0e42e6ab6b625410e5cbefa9c9031dcfb9dd985","schema_version":"rigorous-theory-search/v1","target_digest":"7d2c4a48da6b18e0d1dd177ba0e42e6ab6b625410e5cbefa9c9031dcfb9dd985"} -->
# Rigorous theory search report

## Frozen contract

Target: for a finite directed two-channel gauge network of agents at one shared
context point $c_\*$, with generally non-flat belief and model transports and a
possibly cyclic skeleton, (1) construct a normalized finite-depth generative joint
containing belief and model presentations, directed edge-event data
$(\alpha^b,\alpha^m,\beta,\gamma)$, transports $\Omega^b,\Omega^m$, stochastic
partitions, retained holonomy marks, and parent variables; (2) derive the exact
variational free energy and its conditional-KL decomposition with every normalizer,
base measure, absolute-continuity condition, and finite-versus-extended-real boundary
identified; and (3) decide whether descent of that VFE alone selects a nondegenerate
partition and produces persistent nested blocks.

Quantifier class MIXED: existential in conjuncts (1) and (2), universal in (3). The
declared negative certificate kind is COUNTEREXAMPLE, matched to conjunct (3). The
affirmative search prior — the requester's framing that a hierarchy of meta-agents can
be made to emerge from descent of one multiscale VFE — is recorded only in
`target.search_priors` and appears in no premise, assumption, evidence record, claim,
dependency edge, or certificate. Literature policy: primary sources only for
load-bearing statements about arXiv:2305.10491 and arXiv:2412.12988, with any
vault-recorded statement labeled as such at the point of use.

## Terminal status

INCONCLUSIVE.

The construction and decomposition conjuncts are discharged by derivation. The
selection conjunct is refuted in the unrestricted case by a scope-matched
counterexample, but the corresponding positive question — whether some declared
capacity restriction makes descent select a persistent hierarchy — is neither proved
nor refuted. The compound target is therefore not closed in either direction. A second
and independent reason for this status: no cross-model verifier examined any
derivation, because the session prohibits subagents, and the project's cross-model
rule forbids assigning a verification state to work checked only by its own author
model.

## Certificate

No terminal certificate is issued. The target claim `target` is recorded INCONCLUSIVE
with evidence links to the four derivation parts and to the counterexample register.
Its ancestors `construction`, `decomposition`, `degeneracy`, `parent-impossibility`,
`holonomy-obstruction`, `nonequilibrium`, `intrinsic-scale`, and `literature` carry
their own evidence links of kind DERIVATION, COUNTEREXAMPLE, or PRIMARY_SOURCE. All
are recorded INCONCLUSIVE, not EVIDENCE_VERIFIED, for the cross-model reason above.
The assumptions on which every claim rests are: standard-Borel typing with
$\sigma$-finite references; the belief coordinate typed as law-valued rather than as a
recognition marginal; normalized kernels throughout with the likelihood at scale 0
only; $p_\theta(o\mid X)\in(0,\infty)$; $\mathbb Q_\phi\ll\boldsymbol\Pi$; and
$\mathbb E_{\mathbb Q}(\log L)^+<\infty$.

## Strongest verified result

Nothing in this section is verified. Under this package's own cross-model rule
every claim remains INCONCLUSIVE, so what follows is the strongest
**author-derived** result. The heading above is fixed verbatim by the
`rigorous-theory-search` output contract, which requires exactly nine headings and
forbids others, so it cannot be renamed to "author-derived" without failing the
structural validator; this paragraph carries the correction instead.

Theorem A of `construction-or-strongest-theorem.md`: under the stated typing and
integrability hypotheses the depth-$S$ two-channel tower is normalized with no
partition function beyond the evidence; the exact VFE equals
$-\log p_\theta(o\mid X)+D_{\rm KL}(\mathbb Q_\phi\Vert\boldsymbol\Pi_{\theta,o,X})$ in
$\mathbb R\cup\{+\infty\}$ and decomposes into the observation term plus conditional
divergences over the top prior, the two channels' memberships, the graph data, the
holonomy marks, and the parent-child kernels; the partition and parent coordinate
minimizers are the Gibbs posteriors $Q^\star_R\propto P_Re^{-U_s}$ and
$Q^\star_{s+1}\propto P_{s+1}e^{-\mathcal V_{s+1}}$; pushing the joint directed
edge-event laws and disintegrating gives normalized, gauge-invariant coarse rows that
compose under nested memberships; and non-flat holonomy is retained exactly as a
root-framed orbit together with the conditional law of dressed transports.

Paired with it, the strongest negative result is Proposition 5: with an unrestricted
parent space and downward-kernel family the tower VFE is exactly constant across
partitions, so the posterior over partitions equals the prior and hierarchy selection
is carried entirely by declared capacity restrictions plus a node-count cost. This is
the proof of an assertion the live manuscript states without one.

Supporting exact results: the deterministic-pushforward trichotomy (a deterministic
parent is a statistic whose prior is not free; a free prior overdetermines the model; a
hard constraint annihilates a Gibbs normalizer against a nonatomic reference; two
generative arrows form a directed 2-cycle with no normalization); the
holonomy obstruction $\mathrm{Fix}(\mathrm{Hol})\cap\mathscr M=\varnothing\Rightarrow\mathfrak D=+\infty$;
the convolution law for coarse dressed transports under conditional independence of
consecutive marks; the LaSalle bar on sustained nonequilibrium within one scalar with
symmetric mobility; and the gauge-invariant directed Laplacian
$L^x=\mathrm{diag}(\alpha^x)-\eta^x$ whose Perron-occupancy symmetrization is exactly
Chung's directed Laplacian and supports effective-resistance and commute-time metrics.

## Dependency closure

`target` depends on `construction`, `decomposition`, `degeneracy`,
`parent-impossibility`, `holonomy-obstruction`, `nonequilibrium`, `intrinsic-scale`,
and `literature`. `decomposition` depends on `construction`. `degeneracy` depends on
`decomposition`. The graph is acyclic and every node in the closure is covered by the
attack portfolio, the independent reconstruction, and the oracle erasure.

## Independent reconstruction

Performed and recorded in `evidence/independent-reconstruction.md`, result PASS,
covering all nine claims. Seven load-bearing interfaces were re-derived from the frozen
contract, the ledger, and the DAG without the report's narrative: tower normalization,
the conditional chain rule, partition-blindness, the parent-influence trichotomy, the
holonomy obstruction, the LaSalle argument, and the Perron-occupancy Laplacian
identity. Three discrepancies were found and folded back before release: the
conditioning of the holonomy-mark factor on $G_s$, the promotion of the observation
integrability condition from implicit to explicit, and the restriction of the
degeneracy statement from the cross-scale term to $\min_{\mathbb Q}\mathcal F$. The
reconstruction was performed by the authoring model and is therefore a reconstruction,
not independent-model corroboration.

## Oracle erasure

Performed and recorded in `evidence/oracle-erasure.md`, result PASS, covering all nine
claims. The affirmative prior was removed from the logical context and the premises,
modeling postulates, regularity hypotheses, and load-bearing proof steps were scanned
by hand for paraphrased dependence. The only assumption capable of carrying the prior's
content is the capacity bound, and it is invoked exclusively in the negative direction:
Proposition 5 turns on its *absence*, and the witness construction is anti-correlated
with the prior, so that result survives erasure a fortiori. The recomputed closure of
`target` loses no support. Passing shows only that the prior was unnecessary; the
structural validator's prior-leak check matches the literal token alone and cannot
detect a paraphrase, so this hand scan is the operative record.

## Unresolved obligations

State and defend a capacity restriction on $(\mathsf Z_{s+1},K^s_\downarrow,P_{s+1})$
that makes the partition posterior differ from its prior. Construct a nondegenerate,
relabeling-natural, gauge-compatible partition selector consistent with the holonomy
admissibility condition. Construct the rescaling and identification kernel $I_b$ with
$K_{b_1b_2}=K_{b_1}K_{b_2}$, without which this is a consistent family of
coarse-grainings and not a renormalization group. Prove or refute the six persistence
hypotheses (timescale separation, spectral gap, metastability, closure, capacity,
holonomy admissibility) for the actual coupled flow on a generic cyclic graph. Prove or
refute exact-image invariance of the retained sector, and account for the hyperedges
that exact closure generates. Prove or refute vanishing of the natural-gradient
semiconjugacy defect, separating $c$-measurability of the discarded defect from
horizontal conformality. Prove or refute conditional independence of consecutive
dressed marks. Formulate and attempt the two-channel group-valued analogue of the
multiscale-model uniqueness theorem. Build the Bayesian-RG bridge on a common state
space with a proved monotone, after resolving the spectral-versus-diagonal gap in the
shell criterion. Declare and account for one nonequilibrium mechanism together with an
observable distinguishing it from a hierarchical latent-variable model. Supply a
continuum reference measure directly on a section space, since a finite product of
$\sigma$-finite factors does not extend. Prove or refute necessity of the observation
integrability condition. Re-fetch section 6 of arXiv:2412.12988 and confirm or correct
the one vault-recorded row of the claim table. Obtain cross-model verification of every
derivation in this run.

## Scope and limitations

Theorems: Propositions 1, 3, 4, 5, 7, 8, 9, 10, 11, Corollary 6, and Theorem 2/A, each
proved in text from stated hypotheses; results imported from the live manuscript are
cited by label rather than reproduced. Constructions: the typed joint, the conditional
law of dressed transports, and the gauge-invariant Laplacian family. Modeling
postulates, declared as such: the law-valued belief coordinate, the capacity bound,
label exclusivity, constant-row recognition, and endpoint independence. Operational
identifications: none. Physical interpretation: limited to the mathematics of Gibbs
ensembles in the sense of Jaynes; no object here is identified with a physical clock,
energy, reservoir, particle number, or spacetime, and converting a free energy in nats
to energy units requires a bridge that is not supplied. Analogy, used only where
labeled: the lattice-gas reading of edge occupation and the Wilsonian reading of a
diffusion cutoff. Numerical observations: none were executed; every quantity in the
falsification design is a target, not a result, and the single vault-provenance item is
marked in the claim table. Verification: single author model, no cross-model check,
hence no claim carries EVIDENCE_VERIFIED and the structural validator's clean run
establishes artifact well-formedness only, never mathematical truth.
