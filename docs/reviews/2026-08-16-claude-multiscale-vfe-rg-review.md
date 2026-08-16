# Review of the Claude multiscale two-channel graph-VFE package

**Reviewed revision:** `8ec8f4ab273cf2883030ab97241dbcc51ffc0eeb`
**Package:** `docs/derivations/2026-08-16-multiscale-two-channel-graph-vfe-rg/`
**Authoring model:** Claude Opus 5
**Reviewing system:** Codex/GPT-5 with independent probability/VFE and gauge/RG specialist checks
**Disposition:** **WITHHOLD pending four High and six Medium corrections.**

## Executive assessment

The Git round-trip repair is correct. At the reviewed revision, local `main`, `origin/main`, and the remote `main` ref all resolve to the same commit. In a clean detached checkout, the package generator exits successfully, the installed rigorous-theory release validator passes in normal and optimized Python modes, regeneration leaves no tracked diff, and `git diff --check` is clean. Commit `af7cc18` therefore fixes the earlier line-ending-dependent digest failure.

That mechanical result does not validate the mathematics. The package itself remains `INCONCLUSIVE`, which is the correct terminal status. Several useful constructions survive review, but four promoted claims fail in their advertised generality: the random occupied-node typing of the tower, the parent-coordinate Gibbs update, the dressed-transport law for soft memberships, and the claimed converse from convolution to conditional independence.

The package should be repaired rather than discarded. Its strongest surviving structure is the normalized-kernel formulation of a collective multiscale VFE, the distinction between law-valued latent beliefs and recognition marginals, the pushforward of directed edge-event measures followed by disintegration, and retention of a full non-flat holonomy law rather than a mean transport.

## High-severity findings

### H1. Random occupied sets make the multiscale joint ill-typed

`REPORT-part1-vfe-and-construction.md` declares fixed label pools but then indexes `Z_s` and `G_s` by occupied sets `V_s^b,V_s^m` determined by random membership variables. The displayed generative order samples `P_S(dZ_S,dG_S)` before the lower membership variables that determine those occupied sets. The two channels may also induce different parent partitions, so there need not be a common `V_s` on which the shared parent state is typed.

This is not a cosmetic notation issue. If a parent pool is `{A,B}` and a random partition sometimes occupies only `{A}` and sometimes occupies `{A,B}`, then the target space of `P_S` changes with a variable sampled later in the kernel order.

The bounded repair is to put every scale on a fixed finite label-pool product and carry explicit occupancy masks, or to declare a measurable disjoint-union state space and type every kernel on it. If belief and model partitions differ, the construction must also declare a common parent correspondence, a joint refinement, or separate parent states with an explicit coupling.

### H2. The parent-coordinate Gibbs update omits live descendant terms

The full tower VFE contains membership, graph, holonomy, and downward-kernel conditional divergences that may all depend on `Z_{s+1}`. The claimed coordinate update in `REPORT-part3-holonomy-blocks-dynamics.md` retains only a downward mismatch profile and an undeclared parent prior. It is therefore not the coordinate minimizer of the displayed full functional.

A two-state counterexample suffices. Let the parent prior be uniform, make the downward mismatch zero, and let a descendant membership term have probability one at parent state zero but one half at parent state one. The true coordinate optimum is proportional to `(1,1/2)`, hence `(2/3,1/3)`, while the stated update remains uniform.

The update must include every descendant expected log-ratio that depends on the parent coordinate, or be explicitly restricted to a factorization in which the omitted conditional laws are parent-independent.

### H3. The dressed-transport law omits the soft endpoint kernel

Part 2 correctly defines the coarse edge-event mass by pushing the microscopic event law through `K^x(A,B|i,j)`. Part 3 then defines the conditional law of dressed transports by summing only `eta^x_{ij}` over `i in I,j in J` and dividing by the coarse mass that does include `K`. For soft memberships this is not normalized.

The exact numerator must sum over all microscopic endpoints and include the same endpoint factor:

$$
\sum_{i,j}\eta^x_{ij}K^x(I,J\mid i,j)\,\delta_{\Theta^{IJ,x}_{ij}}.
$$

Equivalently, the present formula can be retained only under hard deterministic endpoint assignments, where the omitted indicator is identically one on the displayed index set.

### H4. Convolution equality does not imply conditional independence

Proposition 9 proves the forward implication: conditional independence of consecutive marks makes the product law the convolution of the marginal mark laws. The ledger, theorem table, and generator strengthen this to an `if and only if`. That converse is false because group multiplication is not an injective map from joint laws to product laws.

For a finite counterexample, take the additive group `Z_3`, let `U` be uniform, and set `V=U`. The pair `(U,V)` is dependent, but `U+V=2U` is uniform, exactly the convolution of the two uniform marginals. Convolution equality therefore cannot test independence.

The claim should state only that conditional independence is sufficient. If independence matters operationally, test factorization of the full joint mark law or conditional mutual information; otherwise retain the joint law and push it through group multiplication.

## Medium-severity findings

### M1. The main VFE theorem omits its integrability premise

Theorem 2 displays the extended-real VFE decomposition without placing the required observation integrability assumption in its hypotheses. Positive finite evidence and absolute continuity alone do not exclude an observation contribution of negative infinity combined with a relative-entropy contribution of positive infinity. The condition already appears elsewhere in the package and in Theorem A; it should be promoted into Theorem 2 itself.

### M2. Capacity control and a node-count penalty are sufficient remedies, not jointly proved necessary ones

The unrestricted copy-parent witness establishes that the partition can become uninformative. It does not prove that every viable restricted model must contain both a capacity restriction and a separate node-count cost. The package should describe these as sufficient design mechanisms unless it supplies a necessity theorem over a specified model class.

### M3. Flatness and law stabilization are not logically independent in both directions

The package correctly notes that a nonidentity holonomy can stabilize a law, so stabilization does not imply flatness. The reverse implication does hold: identity holonomy stabilizes every law. The correct statement is that flatness implies stabilization but not agreement between different agents, while stabilization does not imply flatness.

### M4. The support-based holonomy criterion lacks its topological hypotheses

The construction initially assumes only standard-Borel spaces and measurable actions. The notation `supp(mu)` and the assertion that the stabilizer is a closed subgroup require a declared topology and suitable continuity. At the measurable tier, the exact statement is `mu(Stab(Q))=1`. A support inclusion is available only after adding the necessary topological assumptions.

### M5. Pushing the event law is not by itself an MSM closure theorem

The event-law pushforward is normalized and composes as ordinary measure transport. Calling it “exactly MSM-consistent” overstates the connection to multiscale network renormalization. The Garuccio-Lalli-Garlaschelli theorem closes a specific independent-edge family under an OR coarse map with additive hidden fitness and a prescribed dyadic update. Additivity of one coarse statistic alone does not establish that parametric closure.

### M6. “Strongest verified result” contradicts the release state

The final report uses that heading while every mathematical claim remains `INCONCLUSIVE` under the package's own cross-model rule. “Strongest author-derived result” is accurate; “verified” is not.

## What survives the review

The package's Reading A/Reading B distinction is useful: a law-valued belief coordinate may be part of a generative latent state, whereas a recognition marginal cannot be inserted into the generative model without changing the objective. The row free-energy correspondence is exact under its declared exclusivity and constant-row assumptions, and correlated rows correctly retain a total-correlation correction.

The right graph-level primitive for exact probabilistic coarse-graining is the joint directed edge-event law `eta`, not a row-normalized attention matrix in isolation. Pushing `eta` through one normalized endpoint kernel and then disintegrating gives a normalized coarse event law and coarse rows. This conclusion survives, but its justification is linear Markov pushforward, not a universal principle that every renormalizable edge statistic must be additive.

The treatment of non-flat connections also survives in its main direction: a coarse parent should retain a distribution or joint marked law of dressed transports unless stronger closure assumptions justify a reduced statistic. Holonomy stabilization is an admissibility condition for a holonomy-blind parent, not a partition-selection mechanism.

## Correction prompted by weighted geometric renormalization

Zheng, Garcia-Perez, Boguna, and Serrano define a family of weighted aggregation protocols

$$
\omega'_{IJ}=C\left(\sum_{e\in E(I,J)}\omega_e^{\phi}\right)^{1/\phi},
$$

with the sum rule at `phi=1` and the supremum rule as `phi` tends to infinity. This refutes the package's broad motivation that renormalizability universally means additivity of the defining parameter. Closure is relative to a declared model family and aggregation protocol.

There is nevertheless a sharper in-program reason for the linear rule. If `eta` is a probability law on ordered microscopic edges and `K` is a fixed Markov endpoint kernel, then

$$
\sum_{A,B}\sum_{i,j}\eta_{ij}K(A,B\mid i,j)
=\sum_{i,j}\eta_{ij}\sum_{A,B}K(A,B\mid i,j)=1.
$$

Within the proposed `phi`-norm family, `phi=1` is the unique member that is a fixed linear pushforward of the input measure. A nonlinear aggregation followed by a global normalization constant can still define a normalized coarse object, but it is not the pushforward through one input-independent Markov kernel. The package's exact KL chain rule relies on that fixed-channel structure. This is the defensible reason to push `eta` linearly.

The geometric paper also suggests a research mechanism, not a transferred theorem. Effective resistance or commute time from the package's symmetrized directed Laplacian can supply a graph-derived scale for proposing blocks without an ambient spatial embedding. It does not reproduce the paper's consecutive angular sectors, hidden-degree renormalization, or empirical self-similarity. A max-weight or `sup` aggregation can therefore be investigated as an additional block-formation protocol, but it must be labeled conjectural, will generally not preserve the exact Markov-pushforward VFE identity, and currently discards directionality when built from the symmetrized graph.

## Literature scope

Garuccio, Lalli, and Garlaschelli provide geometry-free multiscale closure for arbitrary prescribed hierarchies, not a mechanism that learns the hierarchy from VFE descent. Their theorem concerns a specific independent-edge ensemble with additive hidden variables. Zheng and coauthors provide a semigroup of weighted geometric transformations and empirical self-similarity under maximum-weight aggregation, but their blocks come from latent geometric order and their theory does not cover directed row-stochastic belief/model channels, gauge transports, or partition persistence.

These papers should be used as external closure templates: the first for exact family closure under prescribed blocks, the second for protocol-relative weighted aggregation and semigroup composition. Neither closes the program's central problem of selecting persistent nested blocks in a coupled directed `beta/gamma` network under VFE descent.

## Required repair order

The minimal repair is to correct H1-H4 in the derivation, generator, ledger, theorem summary, and claim table; narrow M1-M6; regenerate every bound digest; and rerun the clean-checkout validator. Only after that should the optional `sup`-aggregation mechanism be added. It should be placed beside the existing block-proposal mechanisms and explicitly separated from the exact `eta` pushforward used in the VFE decomposition.

## Sources

- Elena Garuccio, Margherita Lalli, and Diego Garlaschelli, “Multiscale network renormalization: scale-invariance without geometry,” *Physical Review Research* 5, 043101 (2023), arXiv:2009.11024.
- Muhua Zheng, Guillermo Garcia-Perez, Marian Boguna, and M. Angeles Serrano, “Geometric renormalization of weighted networks,” *Communications Physics* 7, 97 (2024), DOI: 10.1038/s42005-024-01589-7.
