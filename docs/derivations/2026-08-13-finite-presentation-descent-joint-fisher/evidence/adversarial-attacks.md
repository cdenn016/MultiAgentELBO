<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2","schema_version":"rigorous-theory-search/v1","target_digest":"c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2"} -->
# Adversarial attacks and resolutions

## Method

An isolated falsifier read the frozen contract and ledger, sought satisfying
finite counterexamples to every universal dependency, recomputed every
existential witness, and checked packaging separately from mathematics. The
draft run had one packaging failure and two wording/type defects. The
packaging failure is resolved only when the final evidence hashes and terminal
records validate; the two mathematical presentation defects were repaired
before release.

## Attack A1: singular recognition defeats an unqualified iff

**Claims:** `conditional-kl-completion`, `target`.

**Attack.** Let the retained posterior be \(\delta_0\) and recognition be
\(\delta_1\). Both full and collapsed VFE equal \(+\infty\) for every auxiliary
kernel, so raw equality cannot imply posterior completion.

**Disposition:** REJECTED against the final claim. The contract and proof
restrict the iff and unique-minimizer statements to
\(Q_R\ll P_R(\cdot\mid o)\) with finite conditional terms. The example is
retained as the sharp boundary control.

## Attack A2: an observationally null split changes full VFE

**Claims:** `full-latent-nondescend`, `conditional-kl-completion`, `target`.

**Attack.** Insert a posterior-uniform binary auxiliary into singleton retained
and record spaces and choose auxiliary recognition \(\delta_0\). The full VFE
gains \(\log2\) while the retained law is unchanged.

**Disposition:** REJECTED as an attack on the final theorem. It proves the
theorem's non-descent clause and shows why posterior completion or conditional
minimization is necessary.

## Attack A3: equality at one parameter does not fix Fisher information

**Claims:** `retained-fisher-descent`, `target`.

**Attack.** The Bernoulli families
\(p_A(1;\theta)=1/2+\theta\) and
\(p_B(1;\theta)=1/2+2\theta\) agree at zero but have Fisher values 4 and 16.

**Disposition:** REJECTED against the final claim. Parameterwise equality under
one fixed sample identification is explicit and load-bearing.

## Attack A4: pullback was under-typed

**Claims:** `retained-fisher-descent`, `target`.

**Attack.** A bare map \(z:\mathcal S\to\Theta\) does not define a tensor
pullback without differentiable manifold typing.

**Disposition:** REJECTED after repair. The final proof states a common
\(C^1\) map between the declared smooth manifolds. The underlying retained
Fisher equality was unaffected.

## Attack A5: XOR dilation formulas or quantifiers fail

**Claims:** `binary-dilation-boundary`, `collapsed-vfe-descent`,
`retained-fisher-descent`, `target`.

**Attack.** Recompute normalization, XOR convolution, retained Fisher, and all
full Fisher tensors over the open parameter cube.

**Disposition:** REJECTED. Exact reconstruction gives

\[
\delta=a+b-2ab,
\quad I_{\rm ret}=\frac{vv^\mathsf T}{\delta(1-\delta)},
\quad v=(1-2b,1-2a,0)^\mathsf T,
\]

and the displayed diagonal full tensors. Their ranks are at most one, two, and
three respectively, so they are pairwise distinct for every admitted
parameter. The draft word "generally" was replaced by the exact quantified
statement.

## Attack A6: smooth lifts leave the simplex or fail to preserve marginals

**Claims:** `smooth-right-inverse-lifts`,
`paired-marginal-noncanonicity`, `target`.

**Attack.** Search the open square for a negative component, failed
normalization, wrong marginal, nonsmooth point, or equality of the two lifts.

**Disposition:** REJECTED. The only subtracted cells factor as

\[
(1-a)b[1-\kappa a(1-b)]>0,
\qquad
a(1-b)[1-\kappa(1-a)b]>0
\]

for \(\kappa=0,1/2\). The maps are polynomial, normalized right inverses and
are distinct throughout the open square.

## Attack A7: lift-dependent VFE or Fisher calculations are wrong

**Claims:** `vfe-lift-dependence`, `fisher-lift-dependence`,
`paired-marginal-noncanonicity`, `target`.

**Attack.** Recompute both KL gaps, all categorical derivatives, every Fisher
entry, and the difference eigenvalues at \(a=b=1/2\).

**Disposition:** REJECTED. The independent values are

\[
D_{\rm KL}(\iota_0\|\iota_{1/2})
=\tfrac12\log(64/63)>0,
\]

\[
g_0=4I_2,
\qquad
g_{1/2}=\frac1{63}
\begin{pmatrix}256&-32\\-32&256\end{pmatrix},
\]

with difference eigenvalues \(-4/9\) and \(4/7\).

## Attack A8: the proof assumes its desired ontology

**Claims:** all dependency-closure claims and `target`.

**Attack.** Erase the affirmative search prior and scan for a premise that
asserts agent-only ontology, physical geometry, or the desired descent.

**Disposition:** REJECTED. The reconstruction uses only retained-law equality,
finite disintegration and KL, parameterwise categorical calculus, and explicit
lift formulas. Autonomous agency, physicalization, and canonical agentization
remain explicitly outside the certificate.

## Packaging attack

The first adversarial snapshot correctly rejected release because evidence
hashes were placeholders and the reconstruction/oracle/release records were
empty. This was a provenance failure rather than a mathematical
counterexample. A final release is valid only if all artifact hashes match and
the rigorous-run validator exits successfully after every artifact is frozen.
