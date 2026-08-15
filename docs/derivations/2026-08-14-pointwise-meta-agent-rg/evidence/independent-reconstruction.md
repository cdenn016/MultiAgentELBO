<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-48389cdfa67c229a7a179881667aa14591ad8c4b126a506781a189e1b82d2d06","schema_version":"rigorous-theory-search/v1","target_digest":"48389cdfa67c229a7a179881667aa14591ad8c4b126a506781a189e1b82d2d06"} -->
# Independent reconstruction

## Method and independence boundary

This is a sequential reconstruction pass from the frozen contract, atomic claim statements, and dependency directions. It was performed without treating the root guide or the direct derivation's prose order as a premise. Because the task forbids subagent dispatch, it is role-separated reasoning by the same implementer, not evidence of independent-agent agreement. Mathematical closure rests on the reconstructed derivations, not on the number of passes.

## Reconstruction of the typed graph claims

The convention (T_{ij}:j\to i) fixes the only composition order compatible with function application. A rooted spanning tree supplies one path from the root to every vertex. Appending each non-tree edge produces a fundamental cycle. Reduction of an arbitrary closed walk by canceling inverse tree edges expresses it as a product of those fundamental cycles and inverses. For nonabelian holonomy, based triangle loop words may replace that free basis only when they normally generate the graph fundamental group, as when attaching the declared triangle 2-cells gives a simply connected filled triangulation. Cycle-space spanning alone sees only the abelianization. A chordless square with no diagonals has no triangles but has a nontrivial fundamental loop.

For the positive-definite connection-Laplacian sector, zero energy is equivalent edge by edge to (z_i=T_{ij}z_j). Root evaluation is injective because tree transport determines every vertex. It lands in the holonomy-fixed space because a parallel section returns its root value after a loop. Conversely, a holonomy-fixed root vector extends along the tree, and each non-tree constraint follows from its fundamental-cycle holonomy. Thus (ker L\cong\operatorname{Fix}(\operatorname{Hol})), and full dimension (K) is equivalent to identity represented holonomy. This argument says nothing about probability-law agreement.

## Reconstruction of zero distortion

Finite positive weighted sums of nonnegative extended numbers vanish exactly when every summand vanishes. Relative entropy vanishes exactly for equal measures. An equality on one orientation of a reciprocal support edge can be inverted, so directed row asymmetry does not break propagation on the connected underlying graph. Tree propagation sends every law to one root law. Loop closure stabilizes that law. Conversely, a common root law fixed by every loop makes competing path presentations equal, and applying this to the path obtained by adjoining one edge recovers the edge equality. The root law is unique because the root's identity path fixes it. The two-channel statement is the product of two independent applications and supplies no joint lift.

## Reconstruction of the full-law barycenter

For (M=\sum_iw_iP_i) with (w_i>0), (P_i\ll M) and (dP_i/dM\leq1/w_i). Hence every source-to-mixture KL is finite. If (M\not\ll R), at least one source also fails absolute continuity and both sides of the proposed identity are infinite. If (M\ll R), the derivative factorization (dP_i/dR=(dP_i/dM)(dM/dR)) is exact. When the mixture-to-(R) KL is finite, domination makes all logarithmic terms integrable and weighted summation gives the decomposition. When it is infinite, KL convexity makes the source aggregate infinite as well. The residual (operatorname{KL}(M\Vert R)) proves uniqueness.

For a finite holonomy group, uniform orbit averaging is invariant and path independent. For an invariant candidate (R), common-pushforward KL invariance identifies (\operatorname{KL}(P_i\Vert R)) with the average of (\operatorname{KL}(h_\#P_i\Vert R)) over the orbit. The mixture identity splits that orbit average into an (R)-independent orbit-dispersion constant plus (\operatorname{KL}(\overline P_i\Vert R)). A second mixture decomposition therefore makes the mixture of the (\overline P_i) the unique invariant minimizer. A compact continuous version needs the declared measurable domination and finite-integral conditions. The absence of normalized Haar probability blocks this argument for general noncompact groups.

## Reconstruction of approximate control

Use the convention (\operatorname{TV}(P,Q)=\frac12\lVert P-Q\rVert_1). Fix a rooted spanning tree and orient each tree edge in a positive-support direction. Each selected tree-edge KL is bounded by total distortion divided by the minimum selected tree-edge weight. Pinsker converts that bound to total variation. Transport all laws to the root along their unique tree paths; bimeasurable pushforward preserves total variation, and the total-variation triangle inequality telescopes along the unique tree path between two vertices. The spanning-tree diameter bounds that path length. Convexity then bounds distance to the transported root mixture. This proof never applies a triangle inequality to KL.

## Reconstruction of scalar and marked coarse data

A conditional row lacks receiver mass. Multiplication by a normalized receiver law gives a normalized joint edge-event law. Any normalized endpoint kernel pushes that joint law to another normalized joint law, and disintegration recovers the receiver law and conditional row on positive receiver mass. The product (C(A\mid i)C(B\mid j)) is one endpoint kernel only under declared conditional independence; a general correlated kernel (K(A,B\mid i,j)) is the typed replacement.

A hard partition is a deterministic Markov kernel. A normalized soft membership remains a Markov kernel even with several nonzero entries. A replicated incidence with column sum above one is not normalized and increases total mass. Kernel composition proves exact nesting. Scalar pushforward needs no parent root. For marked closure, support of K on C(A|i)>0 and C(B|j)>0 makes every selected endpoint a declared incidence. For each channel and parent, decomposing V_A={i:C(A|i)>0} into connected components of the induced positive-support transport graph assigns every incidence to one component; choosing one rooted tree per component therefore defines every dressed mark without asserting transport across disconnected components. The component endpoint kernel is normalized, and summing its component pair masses recovers the scalar A,B event mass. Pushing the component-indexed joint event-plus-mark law retains its conditional distribution and each component's internal based holonomy. An operator mean is only a moment; opposite quarter-turns average to zero and disprove group closure of that moment. Hyperedge, shared-factor, and path-memory closure requires the separate Theory/07b joint-factor, full-path-law/transport, and linear-dynamic hypotheses and is not reconstructed as a target ancestor.

## Reconstruction of VFE closure

Attaching the same normalized channel to posterior and recognition measures preserves the fine KL on the lifted joint space. Standard-Borel disintegration of that lifted pair, followed by the relative-entropy chain rule, splits the fine KL into coarse KL plus a conditional KL integral. The evidence is unchanged because the channel does not touch the observation. Adding the common (-\log p(o)) term gives the VFE identity. A finite nonnegative conditional integral vanishes exactly when the conditional laws agree almost surely. Marginal equality alone lacks those conditionals and cannot imply the result.

## Reconstruction of hierarchy and dynamics

Ordinary Markov-kernel composition proves nested hard and normalized soft memberships. Replicated covers fail the normalization premise and therefore do not enter that theorem. For dynamics, differentiating (z(t)=C_t(y(t))) gives (dot z=\partial_tC_t+DC_t\dot y); substituting the fine vector field yields the exact moving-map semiconjugacy condition. The frozen constant-metric Gaussian estimate follows by conjugating (R\dot z=-Lz) to (dot y=-R^{-1/2}LR^{-1/2}y) and applying the spectral theorem. None of this types (t) as base position, RG depth, or physical time.

## Reconstruction of the shortcut refutations

The Bernoulli triple gives two below-threshold KL edges and one above-threshold endpoint. The parity and anti-parity laws give equal singleton marginals with disjoint joint support. The two-node Gaussian tree and the isotropic law under nonidentity orthogonal holonomy separate flatness from law agreement. Scaling a two-node Laplacian changes its gap without reading state. A point mass versus a fair law gives finite forward and infinite reverse KL. Equally weighted children (\mathcal N(\pm a,1)) projected to their moment-matching Gaussian leave the exact signed quartic boundary residual (2\lambda a^4); cubing a standard Gaussian is an additional family-closure control. A two-parent replicated incidence doubles one child's mass. Each witness satisfies the scope recorded in the counterexample register.

## Result

Every dependency of `TARGET-POINTWISE-RG` reconstructs from the frozen premises with the recorded side conditions. The result is `PASS`. The reconstruction supports `COMPLETE_AFFIRMATIVE` for the fixed pointwise conjunction only; all named cross-base, partition-selection, agency, physical-time, continuum, adaptive-dynamics, and noncompact-holonomy extensions remain outside the certificate.
