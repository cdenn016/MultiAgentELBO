# Fixed-model map identities and endpoint-feasibility derivation

Date: 2026-08-10

Scientific source revision: `fcb2c49efdca2ad3ee502dc08fbb82fc285e7a05`

Protocol: `2026-08-09-gaussian-fixed-ray-v1a`

## Claim boundary

The theorem proved here is an application-specific statement about the two
frozen six-dimensional coefficient maps, the coefficient basin
`[1/4, 4]^6`, and the preregistered paired raw-angle endpoint. Its
`theorem_status` is `ESTABLISHED` for the exact frozen three-input call, but the
conclusion is conditional on every application premise enumerated below. That
status does not assert that any concrete run satisfied those premises. Its
producer `verification_state` remains `CANDIDATE`, and its `claim_origin` is
`APPLICATION_SPECIFIC` until final exact-revision adjudication. A generic
arithmetic result outside that input scope is not this theorem.

The conclusion is only that the practical-support boundary `-1/50` is
unreachable under this endpoint definition throughout the admitted basin. It
does not refute projective attraction, establish attraction on the full
Gaussian coupling cone, prove an RG fixed point, or support an unrestricted
universality claim. The completed confirmatory experiment therefore remains
`inconclusive` about mathematical attraction.

### Required premises of the conditional application theorem

The paired application conclusion requires all of the following, jointly:

1. complete, uncensored endpoint records for both frozen schemes,
   `adjacent_pairs` and `balanced_alternating`;
2. initial coefficient vectors admitted in the coefficient basin
   `[1/4, 4]^6`;
3. unchanged frozen maps, including runtime-float conformance to the exact
   rational literals below;
4. unchanged endpoint scales `(4, 5, 6, 7, 8)`, raw projective angles, and the
   five-point ordinary-least-squares slope estimator; and
5. the paired least-favorable maximum across the two frozen schemes.

The pure three-input certificate records the exact strings for these conditions
in `required_application_premises` and sets
`conclusion_is_conditional_on_required_premises=true`. It accepts no run-record
or premise-validation flags and sets `actual_run_premises_validated=false`.
Thus its exact frozen call emits the established conditional theorem; it does
not claim that a completed experiment supplied the required evidence. Tasks 4
and 6 own the run-level completeness and conformance evidence. A missing,
censored, or otherwise incomplete run must remain inconclusive there and must
not inherit the conditional theorem as an unconditional application finding.

## Exact source maps

The runtime source constructs the adjacent map with diagonal entries `0.5` and
off-diagonal entries `0.1`. Its independent exact literal is

$$
A_{\mathrm{adj}}
=\frac25 I_6+\frac1{10}\mathbf 1\mathbf 1^\top.
$$

The Perron direction $\mathbf 1$ has eigenvalue
$2/5+6/10=1$. Every vector orthogonal to $\mathbf 1$ has eigenvalue $2/5$.
Consequently,

$$
\chi_{\mathrm{adj}}(\lambda)
=(\lambda-1)(\lambda-2/5)^5
$$

and the descending coefficients are

$$
\left(1,-3,\frac{18}{5},-\frac{56}{25},\frac{96}{125},
-\frac{432}{3125},\frac{32}{3125}\right).
$$

In particular, $2/5$ is a root of multiplicity five: the polynomial and its
first four derivatives vanish there, while the fifth derivative is `-72`.

The independent exact literal for the alternating map is

$$
A_{\mathrm{alt}}=\frac1{10}
\begin{pmatrix}
3&2&2&1&1&1\\
1&3&2&2&1&1\\
1&1&3&2&2&1\\
2&1&1&3&2&1\\
1&2&1&1&3&2\\
2&1&2&1&1&3
\end{pmatrix}.
$$

Exact determinant expansion gives

$$
\begin{aligned}
\chi_{\mathrm{alt}}(\lambda)
={}&\frac1{25000}(\lambda-1)(5\lambda-1)
\,(50\lambda^2-15\lambda+2)(100\lambda^2-30\lambda+3),\\
={}&\lambda^6-\frac95\lambda^5+\frac{27}{25}\lambda^4
-\frac{333}{1000}\lambda^3+\frac{73}{1250}\lambda^2
-\frac{141}{25000}\lambda+\frac3{12500}.
\end{aligned}
$$

The production implementation computes these coefficients with exact
`Fraction` arithmetic using Faddeev-LeVerrier. It accepts only canonical
tuple-of-tuples of `Fraction` entries. It does not convert runtime floats into
Fractions. A separate conformance function instead compares the runtime
floating encodings with the exact literals and reports a maximum absolute
residual. For the frozen source the residuals are `0.0` for `adjacent_pairs`
and `5.551115123125783e-17` for `balanced_alternating`; the latter comes from
the runtime expression `0.1 * 3`, not from a different exact map.

## Basin-wide endpoint-feasibility theorem

Let an admissible coefficient vector be

$$
c_0=m\mathbf 1+d,\qquad
m=\frac16\mathbf 1^\top c_0,\qquad d\perp\mathbf 1,
$$

with every coordinate of $c_0$ in $[a,b]=[1/4,4]$. Let $\theta_k$ be the
raw projective angle between $A_{\mathrm{adj}}^k c_0$ and $\mathbf 1$.
The preregistered adjacent endpoint is the ordinary-least-squares slope of
$(\theta_4,\ldots,\theta_8)$ against scales $(4,\ldots,8)$, and the paired
job endpoint is the maximum of the adjacent and alternating slopes.

### 1. Exact angle recurrence

The radial part is preserved and the transverse part is multiplied by `2/5`:

$$
A_{\mathrm{adj}}^k c_0
=m\mathbf 1+\left(\frac25\right)^k d.
$$

The two terms are orthogonal and $\lVert m\mathbf 1\rVert_2=\sqrt6\,m$,
so

$$
\tan\theta_k
=\left(\frac25\right)^k
\frac{\lVert d\rVert_2}{\sqrt6\,m}.
$$

### 2. Bhatia-Davis coefficient-of-variation bound

For the uniform empirical law on the six coordinates, Bhatia-Davis gives

$$
\frac{\lVert d\rVert_2^2}{6}\le (b-m)(m-a).
$$

This step is also immediate here without an external theorem: average the
pointwise inequality $(x_i-a)(b-x_i)\ge0$, expand it, and subtract the empirical
variance identity $\operatorname{Var}(x)=\mathbb E[x^2]-m^2$.

Dividing by $m^2$ and using the exact identity

$$
\frac{(b-a)^2}{4ab}-\frac{(b-m)(m-a)}{m^2}
=\frac{((a+b)m-2ab)^2}{4abm^2}\ge0
$$

yields

$$
\frac{\lVert d\rVert_2}{\sqrt6\,m}
\le\frac{b-a}{2\sqrt{ab}}.
$$

At $a=1/4$ and $b=4$, this is the exact bound `15/8`. Therefore

$$
\tan\theta_4\le
\left(\frac25\right)^4\frac{15}{8}=\frac6{125},
\qquad
\theta_4\le\arctan\left(\frac6{125}\right).
$$

### 3. Five-point OLS inequality

The centered five-point OLS weights are

$$
\frac1{10}(-2,-1,0,1,2),
$$

so the adjacent raw-angle slope is

$$
s_{\mathrm{adj}}
=\frac{-2\theta_4-\theta_5+\theta_7+2\theta_8}{10}.
$$

The angle sequence is nonnegative and decreasing. Dropping the nonnegative
terms and using $\theta_5\le\theta_4$ gives

$$
s_{\mathrm{adj}}\ge-\frac3{10}\theta_4
\ge-\frac3{10}\arctan\left(\frac6{125}\right)
=-0.01438895606312301\ldots.
$$

Because $\arctan x<x$ for $x>0$,

$$
s_{\mathrm{adj}}> -\frac3{10}\frac6{125}
=-\frac9{625}.
$$

Relative to the frozen threshold, the exact rational margin is

$$
-\frac9{625}-\left(-\frac1{50}\right)=\frac7{1250}>0.
$$

### 4. Paired maximum implication

Assume the application premises above. In particular, both frozen schemes have
complete, uncensored endpoints for every admitted in-basin initial coefficient;
the frozen maps and the scales 4 through 8/raw-angle OLS endpoint are unchanged;
and the recorded paired endpoint is the least-favorable maximum. Then, for
every such job,

$$
s_{\mathrm{paired}}
=\max(s_{\mathrm{adj}},s_{\mathrm{alt}})
\ge s_{\mathrm{adj}}> -\frac1{50}.
$$

Thus no individual complete paired endpoint in the basin can meet the support
boundary. Because completeness supplies both endpoints for every admitted job,
every bootstrap resample median of values that all exceed the threshold also
exceeds it, and so does every percentile endpoint of those resampled medians.
The preregistered practical-support rule is therefore structurally unreachable
throughout the frozen basin under the enumerated premises. A missing, censored,
or incomplete record breaks this implication instead of inheriting it.

## Fail-closed control

For the synthetic wider interval `[1/16,16]`, the same Bhatia-Davis route gives

$$
\mathrm{CV}\le\frac{255}{32},\qquad
\tan\theta_4\le\frac{51}{250},\qquad
-\frac3{10}\tan\theta_4=-\frac{153}{2500}.
$$

Its rational margin above `-1/50` is `-103/2500`, so this sufficient bound no
longer excludes the threshold. The implementation returns `not_certified` and
does not report the boundary as reachable or unreachable. This control
falsifies an over-eager certificate branch; it is not evidence that a vector in
the wider basin actually reaches the boundary. In fixed dimension, additional
inequalities can be tighter than this interval-only Bhatia-Davis bound.

The implementation exposes the interval calculation separately as
`arithmetic_certificate_status`. Even when generic arithmetic excludes a
synthetic threshold, application promotion is withheld unless the exact basin,
threshold, and frozen numerical inputs match this derivation. Wider, synthetic,
or arithmetically `not_certified` three-input calls therefore remain `OPEN` and
mathematically `INCONCLUSIVE`. The required run premises remain explicit
conditions of the exact theorem rather than extra inputs to this pure function.

When $ab$ has no rational square root, the standard-library exact encoding used
here cannot represent the Bhatia-Davis coefficient as a `Fraction`. The function
fails closed with `not_certified`; it never creates an exact claim by applying
`Fraction.limit_denominator` or otherwise snapping a float.

## Evidence and self-check

Two ignored developer-oracle outputs accompany this derivation:

- `.verification/task-2-sympy-oracle.txt` uses SymPy 1.14.0 to recompute both
  characteristic polynomials, factorizations, spectra, and certificate values.
- `.verification/task-2-hand-fraction-oracle.txt` imports no production
  diagnostic module and recomputes both degree-six polynomials by a direct
  720-term Leibniz determinant over `Fraction` polynomial entries. It also
  checks the fivefold adjacent root and both certificate margins.

Both independent paths reproduce every coefficient and exact bound above. SymPy
is a developer oracle only and is not imported by production code or tests.

## Explicit non-implications

This result depends on complete uncensored endpoints for both frozen schemes,
admitted in-basin initial coefficients, unchanged frozen source maps, the
scalar coefficient-ray construction, the exact basin, raw projective angle,
scales 4 through 8, five-point OLS, and the paired least-favorable maximum. A
missing or censored record, or a changed map, endpoint, scale window, basin, or
pairing rule, prevents an unconditional run-level application conclusion even
though the exact three-input theorem remains conditionally established. The
result does not establish any of the following:

- attraction for `balanced_alternating` or for an arbitrary fixed map;
- attraction on the unrestricted space of positive-definite matrix couplings;
- a Gaussian-family attraction theorem beyond the scalarized ray realization;
- an RG semigroup, beta function, continuum limit, or universality class; or
- a causal explanation of the observed finite trajectory slopes.

Those obligations remain outside this certificate and retain their existing
`INCONCLUSIVE` or `OPEN` status.
