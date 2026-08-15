<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-48389cdfa67c229a7a179881667aa14591ad8c4b126a506781a189e1b82d2d06","schema_version":"rigorous-theory-search/v1","target_digest":"48389cdfa67c229a7a179881667aa14591ad8c4b126a506781a189e1b82d2d06"} -->
# Adversarial attacks and responses

## ATTACK-1: triangle checks may miss curvature

Attack: A proof that checks only triangle products can declare a chordless four-cycle flat.

Disposition: `REJECTED`. The certified type claim uses a rooted spanning tree and every non-tree fundamental cycle. For nonabelian holonomy it permits triangle reduction only when the based triangle loop words normally generate the graph fundamental group, for example when the filled triangular complex is simply connected. Cycle-space spanning alone is sufficient only for abelian holonomy.

## ATTACK-2: full-frame flatness may have been substituted for law agreement

Attack: The connection-Laplacian kernel theorem concerns vectors, not probability laws, and cannot prove consensus.

Disposition: `REJECTED`. The package uses that theorem only for the structural full-(K) sector. Zero law distortion is proved separately from KL positivity. CE-3 and CE-4 refute both directions of the attempted substitution.

## ATTACK-3: directed attention support may block path propagation

Attack: A reverse conditional row can be zero, so an equality might be unavailable in the needed path orientation.

Disposition: `REJECTED`. Every support edge carries an invertible reciprocal transport. Equality of measures on the one positive orientation can be pushed through the inverse, which supplies the reverse equality without a positive reverse row. Connectedness is imposed on the underlying positive-support graph.

## ATTACK-4: the KL decomposition may hide undefined extended arithmetic

Attack: Splitting (log(dP_i/dR)) can create an infinity-minus-infinity expression.

Disposition: `REJECTED`. The proof separates (M\not\ll R), infinite (operatorname{KL}(M\Vert R)), and finite (operatorname{KL}(M\Vert R)). Radon-Nikodym algebra is used only in the finite case after both logarithmic parts are shown integrable. The infinite cases are closed by support and convexity without subtraction.

## ATTACK-5: orbit averaging may be invalid for continuous or noncompact holonomy

Attack: A formal group average need not exist or commute with KL.

Disposition: `REJECTED`. Finite holonomy uses normalized counting measure. Compact continuous holonomy is explicitly conditional on a measurable action, common domination, finite KL, and Fubini conditions. The general noncompact case remains open.

## ATTACK-6: approximate agreement may use a nonexistent KL triangle inequality

Attack: Edge KL bounds cannot be summed along paths as KL distances.

Disposition: `REJECTED`. The proof fixes a rooted spanning tree, applies Pinsker on its selected positive orientations, transports laws along the unique root paths, and telescopes total variation along the unique tree path between vertices. The guide expressly forbids a KL triangle claim and records the minimum selected tree-edge weight and tree-diameter hypotheses.

## ATTACK-7: soft endpoint assignment may hide independence

Attack: The formula (C(A\mid i)C(B\mid j)) assumes conditionally independent endpoint assignments and can erase shared assignment noise.

Disposition: `REJECTED`. The package names that product as the conditional-independence specialization. Its general scalar formula uses a normalized correlated endpoint kernel (K(A,B\mid i,j)), pushes the joint edge-event law, and only then disintegrates. The marked tier additionally requires that correlated kernel to be supported on the declared membership incidences.

## ATTACK-8: averaging transport matrices may leave the group

Attack: A coarse link defined by an arithmetic matrix mean can be singular and lose mark-feature correlation.

Disposition: `REJECTED`. After refining every induced parent support into rooted connected components, the certified state retains component-indexed conditional laws of dressed marks or raw marked edges. The zero mean of opposite quarter-turns and the correlated mark-feature witness attack the unclaimed averaged-link truncation.

## ATTACK-9: coarse VFE equality may be manufactured by a recognition-dependent map

Attack: Choosing the coarse channel after seeing (Q) can force equality and ceases to compare one fixed generative construction.

Disposition: `REJECTED`. Recognition independence is a frozen premise. The exact theorem retains the conditional-KL defect and asserts equality only when the conditional laws agree almost surely.

## ATTACK-10: overlapping parents may duplicate mass and factors

Attack: Calling a replicated cover "soft" can make one shared child fully belong to several parents and double-count its factors.

Disposition: `REJECTED`. Soft membership is normalized columnwise. Literal replication is separately typed, preserves multiplicity, and is not certified as a probability channel. CE-8 exhibits the exact mass defect.

## ATTACK-11: a moving coarse map may invalidate semiconjugacy

Attack: The familiar condition (D C[X]=\bar X\circ C) omits movement of the partition or coarse map.

Disposition: `REJECTED`. The certified equation contains (partial_tC_t). The frozen-map formula is identified as a specialization, and dynamically selected memberships remain open.

## ATTACK-12: finite computation may have been treated as proof

Attack: The recomputation script checks only selected finite values and decimal logarithms.

Disposition: `REJECTED`. No mathematical claim depends on the script. The ledger labels it `SYMBOLIC_CHECK`; exact rational/integer checks and decimal corroboration are separated. Direct derivations close the theorems.

## ATTACK-13: a hard or soft parent support may be disconnected

Attack: One root and one within-parent transport are undefined when the vertices with positive membership in a parent occupy several disconnected components.

Disposition: `REJECTED`. Scalar event-law pushforward uses no parent root and remains exact for every normalized endpoint kernel. The marked tier requires endpoint assignments supported on declared membership incidences, refines each channel-specific parent support into connected components, and roots every component separately. Each incidence determines its component; component-indexed marked masses sum to the scalar parent-pair mass, and no transport between disconnected components is asserted.

## Attack coverage result

The attacks jointly cover `TARGET-POINTWISE-RG` and every dependency claim: graph typing and holonomy, zero distortion, full-law barycenter, approximate TV control, event-law renormalization, retained marks, VFE closure, hierarchy/dynamic semiconjugacy, and the counterexample register. No sustained attack remains inside the frozen conjunction. Each rejected extension remains either explicitly conditional or open rather than being silently absorbed into the theorem.
