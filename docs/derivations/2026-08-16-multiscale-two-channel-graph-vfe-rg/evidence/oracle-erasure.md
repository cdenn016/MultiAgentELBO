# Oracle erasure

The affirmative search prior recorded in the contract is the requester's framing that
a multiscale hierarchy of meta-agents can be made to emerge from descent of one
multiscale VFE. Erasure removes that framing from the logical context, scans the
premises, assumptions, and load-bearing proof steps for direct **or paraphrased**
dependence on it, and recomputes the target's dependency closure. Result: PASS.

The paraphrase scan is performed here by hand. The structural validator matches only
the literal `SEARCH_PRIOR_AFFIRMATIVE` token and cannot detect a leak carried in
mathematical content, so a clean validator run is evidence that no label was pasted
and is never evidence that the prior went unused.

## Scan of premises and assumptions

* **Contract premises.** All are typing statements (standard Borel spaces,
  $\sigma$-finite references, normalized kernels, finite depth, one context point,
  possibly cyclic skeleton, non-flat transports). None asserts that a hierarchy exists,
  persists, or is selected. No leak.
* **Modeling postulates.** Reading A (belief coordinate is law-valued); the capacity
  bound; label exclusivity; constant-row recognition; endpoint independence. The
  capacity bound is the one to watch, because a strong enough capacity bound could
  smuggle in the conclusion. It does not: the bound is invoked only *negatively*, as
  the thing whose **absence** makes the objective constant (Proposition 5). No step
  assumes a bound and then concludes that a hierarchy emerges. No leak.
* **Regularity.** The integrability hypothesis $\mathbb E(\log L)^+<\infty$ concerns
  finiteness of the observation term and is independent of hierarchy formation.
  No leak.

## Scan of load-bearing steps

* Proposition 1 uses only reverse-order Tonelli on a fixed product space. Erasing the
  prior changes nothing.
* Theorem 2 uses only the conditional chain rule. Erasing the prior changes nothing.
* Proposition 3 is a negative result about combining two arrows; erasing an
  affirmative hierarchy prior cannot weaken it.
* Proposition 4 is the standard Gibbs variational lemma on a dominated space.
* **Proposition 5 is the critical case.** Under erasure the question becomes neutral:
  "does the tower VFE rank partitions?" The construction that answers it — take the
  parent space to be a copy of the child space and $K_\downarrow=\delta$ — is *anti*
  to the prior, since it exhibits a tower in which no hierarchy is preferred. A leaked
  affirmative prior would have pushed toward the opposite conclusion, so the result
  survives erasure a fortiori.
* Propositions 8, 9, 10, 11 are, respectively, an obstruction, a conditional
  composition law, a negative dynamical result, and an algebraic identity. None uses
  the prior.

## Recomputed closure

With the prior erased, the dependency closure of `target` is
`{construction, decomposition, degeneracy, parent-impossibility,
holonomy-obstruction, nonequilibrium, intrinsic-scale, literature}`. Every node in
that closure retains the same support it had before erasure. No node loses support, so
no downgrade is triggered by erasure itself.

## What erasure does *not* show

Passing shows only that the prior was unnecessary. It does not prove any theorem, and
it does not repair the fact that no cross-model verifier examined these derivations.
The terminal status remains INCONCLUSIVE for that separate reason: the affirmative
half of the target (that some declared capacity bound makes descent select a
persistent hierarchy) is neither proved nor refuted here.

## Coverage

Erasure covered: `target`, `construction`, `decomposition`, `degeneracy`,
`parent-impossibility`, `holonomy-obstruction`, `nonequilibrium`, `intrinsic-scale`,
`literature`.
