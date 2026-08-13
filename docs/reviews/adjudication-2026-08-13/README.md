# Adjudication of the interim referee review, 2026-08-13

Verbatim agent returns from workflow `wf_0b4620e2-7dc`, which adjudicated every finding of
`docs/reviews/2026-08-12-pifb2-elbo-program-interim-theory-review.md`.

**Read the consolidated response first:** `docs/reviews/2026-08-13-response-to-interim-theory-review.md`.
These files are the evidence behind it.

## Method

The review was written against `caa4a15`. The repository had since advanced to `4dee0db`, which added
worklog §4b and the 16 recovered panel returns — material the reviewer could not see. Each finding was
therefore adjudicated on two axes: **is it correct**, and **is it now superseded**.

Six adjudicators (one per finding cluster), each required to recompute every mathematical and
numerical claim rather than accept it, each then attacked by an independent adversarial verifier whose
brief was to attack *the adjudication*, not the review. Where a verifier overturned or narrowed an
adjudication, the verifier's verdict governs.

## Outcome

**All six adjudications survived verification** (`holds: true` in every case). Twelve separable
findings: 10 upheld outright, 2 narrowed, **none moot**. Not one is wrong on its substance.

| File pair | Finding | Final verdict | Severity |
|---|---|---|---|
| `F1-likelihood-bridge-*` | Theorem proves a repaired scalar, not equality to literal PIFB2 | UPHELD | **High** |
| `F2-lagged-vs-contemporaneous-*` | Base-neighbour proposition conflates lagged with contemporaneous | UPHELD | **High** |
| `F4-kl-expansion-scaling-*` | Local KL expansion ≠ global continuum estimate | UPHELD, NARROWED | Medium |
| `F5-u1-witness-*` | U(1) witness detects flat monodromy, not curvature or topology | UPHELD | Medium |
| `F6-gl-no-go-*` | Full-GL invariant-form no-go worded too strongly | UPHELD | Medium |
| `F3-7-8-and-minors-*` | Contraction schema; SPEC conflict; provenance; 4 minor | UPHELD / PARTLY | Medium |

## What independent recomputation confirmed

Every load-bearing number in the review reproduces: the Jensen gap `log2 − ½log3 = 0.1438410362`
(sympy-exact); the `arccos(cos Θ)` statistic identity to `4.4e-16` and the `Θ=π/2` / `3π/2` record-law
gauge-equivalence to `1.06e-16`; the `(tr X)(tr Y)` counterexample (Ad-invariant to `2.8e-14`,
signature `(1,0,3)`/`(1,0,8)`, radical `sl(K,R)`); oriented-vs-symmetric stencil rates `O(h)` vs
`O(h²)` in both flat and covariant settings; and the `d=1 → 0`, `d=2 → finite`, `d=3 → divergent`
scaling of the unweighted bond sum.

## Two blind hits worth recording

1. **Finding 6(c)** predicted — without access to the T-CURV panel — that Fisher dressing would give
   *a nonnegative invariant state-dependent sector that is stabilizer-degenerate and noncoercive along
   noncompact gauge orbits*. That is three-for-three the T-CURV outcome.
2. **Finding 2**'s lagged/contemporaneous dichotomy was restated independently and blind by the T-GRAD
   panel agent, then converted into a proven inequivalence by T-SIMUL (§4.5).

## Two defects the adjudication found *inside* §4b

Neither referee saw these; both were introduced on 2026-08-13 in the hand-written §4b:

- **§4.7 over-unified `d=2` with the Amari–Chentsov drop-out** — contradicted by its own source
  (`panelB-V-BRIDGE-derivation.md:17`) and refuted by a `d=2` Poisson-fibre run where `T_skew > 0`
  everywhere. Retracted in place.
- **§4.3's peer-sector negative is a balanced-stencil artifact.** Biased rows — exactly the ones PIFB2
  deploys — retain up to 90% of the sector at `O(h²)`. Scope-restricted in place.

## Caveat on reading these files

Verifier corrections govern over the adjudications they attack. In particular `F6-gl-no-go-verification`
corrects the adjudication's source forensics: `rm-04` overstates in **three** places (`:43-46`,
`:295-299`, `:879`), not one, so `rm-04`'s finding K1 must not be cited as the authoritative wording.
`rm-04` itself is left unedited — it is an archived verbatim return.
