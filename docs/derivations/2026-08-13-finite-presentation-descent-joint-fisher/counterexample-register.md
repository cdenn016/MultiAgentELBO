<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2","schema_version":"rigorous-theory-search/v1","target_digest":"c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2"} -->
# Counterexample register

## C1: observationally null auxiliary split changes full VFE

Take singleton retained and record spaces. The collapsed VFE is zero. Insert a
binary auxiliary node whose posterior is uniform and choose auxiliary
recognition \(\delta_0\). The retained law and conditioning algebra are
unchanged, while the full VFE gains \(\log 2\). This refutes unqualified
descent of arbitrary full-latent VFE. Posterior completion or merging the node
restores zero.

Status: exact derivation, sustained as a boundary; it does not attack the
support-qualified theorem.

## C2: singular retained recognition makes equality vacuous

Let the retained posterior be \(\delta_0\) and recognition be \(\delta_1\).
Both collapsed and full VFE are infinite. Changing the auxiliary posterior
version on the posterior-null retained state can change the displayed
conditional term without changing the joint law. This refutes an unconditional
"equality iff posterior completion" statement and justifies the theorem's
absolute-continuity qualifier.

Status: exact finite boundary control.

## C3: one-point law equality does not imply Fisher equality

Near zero, the Bernoulli families
\(p_A(1;\theta)=1/2+\theta\) and
\(p_B(1;\theta)=1/2+2\theta\) agree at \(\theta=0\), but their Fisher values
there are 4 and 16. This refutes Fisher descent from equality at only one
parameter. The theorem requires parameterwise family equality.

Status: exact derivative calculation.

## C4: identical paired marginals support different joint geometry

At \(a=b=1/2\), the product and correlated lifts are
\((8,8,8,8)/32\) and \((9,7,7,9)/32\). They have identical binary marginals,
but their VFE values and Fisher matrices differ. No outcome permutation maps
the uniform law to the nonuniform law. This refutes any claim that paired
marginals alone canonically fix the full joint family.

Status: exact construction and symbolic corroboration.

## C5: observational equivalence does not preserve interventions

The direct binary channel with crossover \(\delta=a+b-2ab\) and the latent
chain \(R\to E\to O\) have the same retained law. For \(b\ne1/2\), however,
\(\operatorname{do}(E=0)\) and \(\operatorname{do}(E=1)\) generate distinct
record laws, while the direct presentation has no matching two-valued
auxiliary intervention. This refutes recovery of every presentation's typed
intervention structure from the observational quotient alone.

Status: exact quotient-level obstruction. It does not prove that no enriched
equivalence or independent canonicalization axiom can exist.

## C6: null-node insertion changes full Fisher rank

Adding an independent Bernoulli null node with parameter \(\eta\) preserves
the retained joint law but adds the positive full-Fisher component
\(1/[\eta(1-\eta)]\). This refutes presentation descent of the full-joint
Fisher tensor and of latent node count.

Status: exact finite score calculation.
