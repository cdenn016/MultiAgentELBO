<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2","schema_version":"rigorous-theory-search/v1","target_digest":"ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2"} -->
# Adversarial attacks and resolutions

## Method

A sequential isolated falsifier pass used only the frozen statement,
quantifiers, premises, and proof drafts. It attacked every dependency claim
for normalization, type, symmetry, rank, conditional-VFE, Fisher-sign,
identifiability, and interpretation failures. Agent agreement is not evidence;
each rejected attack below points to a direct derivation or exact
countercontrol.

## A1: one of the 64 atoms becomes negative

**Claims:** positive-normalized-lift, target.

Factoring an atom gives
\(Q=P[1+\kappa\chi P(\bar x)]\). Since
\(0<P(\bar x)<1\) and \(|\kappa|<1\), the bracket is positive. The attack is
rejected on the open strict domain. The boundary \(|\kappa|=1\) is not
claimed.

## A2: a lower-order parity term survives marginalization

**Claims:** all-proper-marginals, right-inverse-immersion, target.

Every proper marginal sums over at least one bit. Pairing its two values
cancels the parity perturbation exactly. This proves all 63 subset identities
and the singleton right inverse. The executable independently enumerates
every assignment in every proper subset.

## A3: the contract confuses singleton sections with two-bit joint sections

**Claims:** all-proper-marginals, lift-dependence-boundaries, target.

This attack was sustained against an early wording and repaired. The final
contract says the retained section data are six singleton Bernoulli marginals
grouped into three agent pairs. The 57-dimensional Frechet-fiber count uses
exactly six affine constraints. Product two-bit marginals are a theorem of the
specific parity family, not the definition of section equivalence.

## A4: within-pair swaps are falsely universalized as typed gauge

**Claims:** symmetry-boundary, target.

This attack was sustained against an early registry phrase and repaired.
Paired complements are the declared equivariance. Pair permutations require
identified agent/channel types. Within-pair coordinate swaps are labeled
accidental toy-formula symmetries because they can exchange belief/model
channel types. No universal gauge claim remains.

## A5: odd flips preserve a fixed nonzero scalar

**Claims:** symmetry-boundary, target.

An odd flip changes \(\chi\) to \(-\chi\), producing
\(Q_{C\theta,-\kappa}\). The scalar claim is false for every atom when
\(\kappa\ne0\) in the off-center executable fixture. The attack is rejected
against the final classification; a pseudoscalar transformation is stated as
an extra repair.

## A6: the VFE witness is mislabeled as a single-agent theta update

**Claims:** fixed-outside-vfe, target.

This attack was sustained against a draft interpretation and repaired. The
theorem is the KL-chain difference for any common outside marginal and its
normalized conditional tangent. The executable changes global \(\kappa\)
from \(1/4\) to \(1/2\), so it is explicitly labeled an
outside-marginal-preserving lift direction. Its differential is along
\(Q_{\rm alt}-Q_{\rm base}\), not per unit \(\kappa\).

## A7: the Fisher correction silently drops signed terms

**Claims:** joint-fisher-decomposition, parity-residual-positive,
weighted-marginal-gate, target.

The general formula retains
\(\mathbb E[ss^{\mathsf T}]-G_{\rm prod}\), both signed cross matrices, and
the residual Gram matrix. Only for the parity family do pairwise independence
and score projection kill the first three defects. The two-bit counterexample
has correction eigenvalues \(-4/9\) and \(4/7\), demonstrating that omission
would be false.

## A8: the residual Gram matrix has a hidden null vector

**Claims:** parity-residual-positive, center-fisher, target.

For nonzero \(\kappa\), a null combination of residuals would make
\(\sum_ia_iu_i(x_i)=0\) on every binary state. Flipping coordinate \(j\)
alone forces \(a_j=0\). Thus all six coefficients vanish. The general
linear-independence proof rejects the attack; exact off-center positive
principal minors provide corroboration only.

## A9: arbitrary marginal weights reproduce the shared joint Fisher

**Claims:** weighted-marginal-gate, center-fisher, target.

The exact defect relative to \(G_w\) includes both the full signed joint
defect and \(\operatorname{diag}((1-w_i)/a_i)\). At the center, equality on
the full tangent requires every \(w_i=1/(1-c^2)\). Unit weights work only at
\(\kappa=0\). Matching a center tensor does not identify the law or extend
off center.

## A10: the hyperedge is derived from pairwise locality

**Claims:** hyperedge-record, lift-dependence-boundaries, target.

The kernel is explicitly declared and engineered. A same-marginal,
strictly-positive cancelling joint kernel removes the \(ab\) term produced by
conditional-independence factorization. This rejects inference from pairwise
record marginals and preserves the boundary that product factorization is
extra structure.

## A11: promoting two amplitudes adds two identifiable directions

**Claims:** lift-dependence-boundaries, right-inverse-immersion, target.

For the explicit redundant promotion \(Q=P+(\kappa\eta)\chi D\), the
interaction derivatives are proportional and the Fisher block has rank at
most one, with rank zero at the origin. The rank-six theorem concerns fixed
\(\kappa\) and the six \(\theta\) coordinates, so there is no contradiction.

## A12: finite information geometry implies physical theory

**Claims:** target and the full dependency closure.

The premises contain no GL(K) bundle, connection, continuum limit,
intervention algebra, agency criterion, operational clock, dimensions, units,
or coarse-graining map. Those conclusions remain outside the certificate.
The attack finds no hidden bridge premise and is rejected as a claim about the
final scoped theorem.

## Packaging gate

The release remains invalid until all target and evidence hashes are frozen,
the RED/GREEN JUnit files are preserved, every dependency ancestor is
evidence verified, and the rigorous-theory release validator exits zero. A
validator pass checks structure and bytes, not mathematical truth.
