# Session 1 Multi-Agent Network Review

Date: 2026-08-09

Review type: same-session adversarial source, derivation, artifact, and negative-control review. This record is durable but is not represented as the independent cross-session review required during serial integration.

## Verdict

No unresolved critical, high, or medium implementation defect remains in the
Session-1 allowlist after the provenance-framing repair. The lane is ready for
independent cross-session review and serial integration, conditional on current
mechanical evidence at its final commit.

## Derivation checks

### Common-channel evidence

Every fine-to-coarse row is an exact `Fraction` probability vector. Therefore

$$
\sum_z (mK)(z)=\sum_y m(y)\sum_z K(y,z)=\sum_y m(y)
$$

holds exactly for the scenario evidence submeasure. The experiment records the
exact rational difference, not a floating all-close comparison. This matches
the fixed-evidence theorem's normalized, recognition-independent channel
premise.

### Joint VFE gap

The direct finite functional is computed from the unnormalized evidence masses
as

$$
\sum_y q(y)\log\frac{q(y)}{m_o(y)}.
$$

It is independently compared with
$\mathrm{KL}(q\Vert\pi_o)-\log Z_o$, where
$\pi_o=m_o/Z_o$. No marginal entropy or sum of agent-local objectives replaces
the joint recognition law.

### Local-to-collective difference

For each declared block, the before and after recognition laws are exact
four-site product laws and their outside marginals are compared as `Fraction`
vectors before any subtraction. The local conditional KL change and the full
joint KL change are then evaluated through separate loops. The aligned `B01`
literal oracle is `0.4496337464793081` on both sides. The deliberately wrong
overlapping-local-objective sum has gap `0.18747552763150188`, so the test suite
would catch additive-local substitution.

### Complete interactions

The implementation computes every Boolean-lattice conditional expectation and
Mobius component with exact rational arithmetic, broadcasts every subset
component onto the full 16-state order, and reconstructs by an independent full
sum. The higher-order parity record has pure `(0,1,2)` component values
`(-1,-1,1,1,1,1,-1,-1,...)` in log2 units and exact pairwise omitted sup norm
one. This pins the required failure of automatic pairwise closure.

### One-arrow effective action

The scenario submeasure and correlated baseline are pushed through the single
frozen channel. The coarse effective likelihood is their exact rational ratio;
only the final `-log` action display is floating point. No second scale arrow or
composition claim is introduced in Session 1.

## Artifact and runtime review

Validation of the experiment discriminator, figure boundary, fixture digest,
frozen application ID, exact literals, and normalized channel finishes before
RNG construction and `RunStore.create`. Publication uses the existing atomic
run-store contract. Metrics, claims, arrays, and optional diagnostics finalize
before the result is returned.

The first provenance implementation recomputed Git state through a safe
read-only command but used a lane-local byte concatenation while retaining the
shared `dirty_tree_format` label. A red test independently reconstructed the
declared length-framed digest and failed. The implementation now uses the exact
length framing of the shared runtime contract, and the test passes.

The frozen shared validator already rejected self-consistent alternative
application IDs; a regression test now pins that behavior. No shared contract
file was changed.

## Claim/evidence/falsifier table

| Claim | `theorem_status` | `verification_state` | `claim_origin` | Evidence | Falsification condition |
|---|---|---|---|---|---|
| Normalized common pushforward preserves evidence | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Exact rational pushforward and residual zero | A validated row-stochastic channel produces a nonzero exact mass difference |
| Joint VFE equals posterior KL minus log evidence | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Independent direct and posterior forms on the explicit joint | Finite supported inputs produce a residual beyond the declared tolerance |
| Fixed-outside block differences equal collective differences | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `PROJECT_NOVEL` | Two blocks, exact outside marginals, independent KL paths | Equal outside marginals and finite KL yield disagreement beyond tolerance |
| Complete product-reference Hoeffding reconstruction | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Fraction Mobius decomposition and exact reconstruction | A valid finite action/reference has nonzero exact reconstruction residual |
| Frozen product lift is a right inverse on the tested coordinates | `HYPOTHESIS` | `EVIDENCE_VERIFIED` | `APPLICATION_SPECIFIC` | Exact extraction-after-lift residual zero | A declared in-domain coordinate is not recovered exactly |
| Higher-order scenario is not pairwise closed | `HYPOTHESIS` | `EVIDENCE_VERIFIED` | `APPLICATION_SPECIFIC` | Literal triple component and exact omitted sup norm one | Complete decomposition gives no component above order two |
| Parameter-dependent channel remains outside the fixed-channel theorem | `HYPOTHESIS` | `INCONCLUSIVE` | `APPLICATION_SPECIFIC` | Pinned negative-control classification | A separate theorem admits the supplied parameter dependence with all required hypotheses |

## Ownership and scope audit

The expected changed paths are exactly the two Session-1 production files, the
Session-1 launcher, two Session-1 test files, this review, and the Session-1
results record. No package export, shared registry, shared launcher, figure,
README, hypotheses, dependency, lockfile, `.gitignore`, or `Theory/**` path is
owned or modified by this lane.

## Open integration obligations

- Independent mathematical review should reconstruct at least the aligned VFE
  oracle and the higher-order triple component without importing Session-1
  helpers.
- Independent code review should rerun the sanitized subprocess launcher,
  deterministic artifact comparison, validation-before-RNG probes, coverage,
  and full suite at the final commit.
- Shared exports, figure rendering, launcher registry, README, and consolidated
  hypotheses/results belong only to the serial integration owner.
- Physical time, learned dynamics, universality, continuum limits, and
  fixed-point claims remain outside this lane.
