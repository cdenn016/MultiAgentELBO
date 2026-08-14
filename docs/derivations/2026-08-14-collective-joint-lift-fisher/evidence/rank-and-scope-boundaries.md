<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2","schema_version":"rigorous-theory-search/v1","target_digest":"ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2"} -->
# Rank, identifiability, and scope boundaries

## Lift selection and identifiability

The six singleton Bernoulli sections determine \(\theta\), but every
\(Q_{\theta,\kappa}\) has those same sections. They do not determine
\(\kappa\). The parity family is one direction in the 57-dimensional
fixed-singleton Frechet fiber, so even selecting this one-dimensional ansatz
is extra model structure.

If the interaction amplitude is redundantly promoted to two parameters by

\[
Q_{\theta,\kappa,\eta}
=P_\theta+(\kappa\eta)\chi D,
\]

only \(\lambda=\kappa\eta\) is identifiable. The two interaction derivatives
are proportional:

\[
\partial_\kappa Q=\eta\chi D,\qquad
\partial_\eta Q=\kappa\chi D.
\]

Their Fisher block has rank at most one, and the tangent
\(\kappa\partial_\kappa-\eta\partial_\eta\) is radical whenever
\((\kappa,\eta)\ne(0,0)\). At the origin both derivatives vanish and the
interaction block has rank zero. A quotient by this redundancy requires the
same constant-rank, integrability, regular-leaf-space, and basicness checks
stated in the main proof; global identifiability does not follow from a local
rank count.

This generic redundant-amplitude example is not a pairwise-record auxiliary.
No extra record-noise parameterization is included in the theorem.

## Lift-dependent joint objects

Changing \(\kappa\) while holding all six singleton sections fixed changes the
full joint law. Therefore full-joint VFE and full-joint Fisher remain
lift-dependent. The declared hyperedge likelihood provides one selection
mechanism, but the selection comes from the likelihood, not the sections.
The cancelling-kernel control in vfe-hyperedge-proof.md shows that even fixed
pairwise record marginals do not select a unique joint record kernel.

For VFE covariance under a finite relabeling, both recognition and its fixed
generative target must be pushed forward. A coordinate-fixed target that is
not invariant can break the equality. Thus the finite paired-complement
calculation is not an unconditional gauge-covariance theorem.

## Excluded conclusions

The release proves none of the following:

- a canonical lift or a canonical joint record factorization;
- preservation or recovery of an intervention algebra;
- autonomous agency or an ontological identification of agents with nodes;
- a GL(K) gauge theory, principal or associated bundle construction, or
  connection;
- a continuum limit or probability law on a section space;
- physical geometry, causal signature, operational time, clock, mass, energy,
  or dimensional units;
- an exact or projected renormalization transformation, scale closure, beta
  function, fixed point, or universality class.

Obtaining any such conclusion requires a new frozen contract with the missing
typed structures and operational bridges. The finite categorical Fisher
matrix is an information-geometric tensor on the declared statistical family,
not physical spacetime.
