# 2026-08-18 deep audit: the rescaling laboratory (amendments 3–7)

Scope: the 2026-08-17/18 rescaling-laboratory work frozen at `9743962` — `cocycle_flow.py`,
`closure_residual.py`, `coupling_readback.py`, `contraction_backend.py`, `rescaling.py`,
`nested_tower.py`, `cuda_backend.py`, `tools/cuda_worker.py`, and their tests. Five parallel
domain investigators (gauge theory, variational, numerical, implementation, transformer-ML),
50+ live probe scripts, all published numbers re-executed. Author model: Fable 5.
Verification: inline live reproduction of every claimed number and every claimed defect
(the machine crashed before a separate cross-model verifier pass could be dispatched; each
finding below was confirmed by executed code, not judgment). Remediation: all nine findings
fixed on 2026-08-18 in the commit that adds this report.

## Positive confirmations (all published numbers reproduced)

- C1 gauge covariance: exhaustive 3^6 = 729 gauge-shift sweep, C1 on regenerated instances at
  every declared tau, and 144 random tower instances — zero failures.
- C2 Wilson-rank conservation: 144 random tower instances, zero failures; self-loop case correct.
- C3 live reproduction: deviation 0.2035 with lossless intermediate (omitted sup 0.0), staged
  route independent of coarse edge ordering.
- IPF M-projection: pair marginals matched to 4e-17; stationarity confirmed; tightening the
  1e-13 stopping rule to 1e-16 costs one sweep and moves couplings by <= 2e-15.
- mpmath 120-digit reference: float64 Moebius agrees to < 2e-16 at all scales.
- M-bundle (0.156/0.441/0.564), M-capacity as then defined (0.144/0.406), regen fixed point
  (0.579 at tau = 1, 110 iterations), sustained-over-injected 1.246 (seed-step denominator,
  confirmed consistent), RC6 (0.165–0.265): all reproduced.
- Regenerated rows and injected-energy orientation: brute-force match to 1e-16; injection is
  added to `step.variational`, and the three-body truncation content (~4 nats) is correctly
  discarded by the pairwise read-back.
- Block kernel normalization: f64 2.2e-16 (declared 1e-12), f32 1.2e-7 (declared 1e-6).
- 52 tests passing, 1 CUDA-skipped; `test_remediation_evidence` failures are pre-existing
  environment issues (CUDA_VISIBLE_DEVICES), out of scope.

## Findings

### F1 (MEDIUM) — controller misses the worker's subscript-pool check
- Location: `src/multiagent_elbo/cuda_backend.py`, `_validate_blocked_contraction_job`.
- Evidence: live-confirmed validation asymmetry — the controller accepts a 27-site/27-block
  job that the worker then rejects with `ProtocolError` (`tools/cuda_worker.py` checks
  `sites + blocks > len(CONTRACTION_LETTERS)`; the controller mirror omitted it).
- Fix: the controller now enforces the same 52-letter pool check and fails before artifacts.
- Falsifies: a controller-accepted job the worker refuses on the subscript pool.

### F2 (LOW) — inner-2 towers constructible but unusable
- Location: `src/multiagent_elbo/finite/nested_tower.py`, `_check_sizes`.
- Evidence: `_check_sizes` allowed `inner = 2` while `homogeneous_cycle_instance` refuses
  length < 3 and `coarse_connection` refuses the reciprocal arcs an inner 2-cycle creates,
  so the failure surfaced downstream instead of at construction.
- Fix: `_check_sizes` now requires `inner >= 3`; the reciprocal-arc refusal keeps its own
  test via a hand-built graph.
- Falsifies: a constructible tower every declared consumer refuses.

### F3 (LOW-MEDIUM) — unreachable sectors floored into garbage
- Location: `src/multiagent_elbo/finite/cocycle_flow.py`, `capacity_pair_retention`.
- Evidence: at `sector_count >= 6` on width-2 blocks only five charges are reachable; the
  zero-mass sectors hit the `floor * 1e-300` guard and produced retention 2179.
- Fix: `sector_count` must be a positive integer and every sector must be reachable by the
  block charge; unreachable sectors now raise instead of flooring.
- Falsifies: any `sector_count` whose retention is dominated by the zero-mass floor.

### F4 (LOW) — zero marginal raises OverflowError
- Location: `src/multiagent_elbo/finite/closure_residual.py`, `_action_and_flow_from_marginal`.
- Evidence: an exact-zero marginal entry gave `-log(0) = inf` and `Fraction(inf)` raised
  `OverflowError` with no indication of the cause.
- Fix: nonpositive or nonfinite marginals now raise `ValueError` naming the exact-zero entry.
- Falsifies: a zero-mass coarse state reaching the action read-back.

### F5 (LOW) — Moebius dedup broken for reverse pairs
- Location: `src/multiagent_elbo/finite/coupling_readback.py`, `mobius_couplings`.
- Evidence: `admitted_pairs = ((0, 1), (1, 0))` survived the pre-sort `set()` and produced two
  identical (0, 1) tables, doubling the pair term (confirmed error 1.6).
- Fix: pairs are normalized to sorted order before deduplication.
- Falsifies: a doubled pair table from reverse-pair admittance.

### F6 (LOW) — coarse connection silently accepts disconnected blocks
- Location: `src/multiagent_elbo/finite/rescaling.py`, `coarse_connection`.
- Evidence: a block whose induced graph is disconnected has no single root frame, yet
  `coarse_connection` succeeded and left downstream checks to fail loudly.
- Fix: each block's induced graph must be weakly connected; disconnection now raises.
- Falsifies: a coarse connection built from a block without a root frame.

### F7 (LOW) — in-process 12-letter subscript ceiling
- Location: `src/multiagent_elbo/finite/closure_residual.py` `_blocked_action` and
  `cocycle_flow.py` `capacity_pair_retention`.
- Evidence: the hardcoded `"abcdefghijkl"` pool raised bare `IndexError` for L = 10 at
  ratio 2 (15 labels needed); the worker already carries 52 letters.
- Fix: both sites use the 52-letter pool and refuse beyond it with the worker's message.
  All declared instances (L <= 9) were unaffected.
- Falsifies: an in-process contraction failing where the worker route succeeds.

### F8 (MEDIUM) — the capacity sector charge was gauge-dependent
- Location: `src/multiagent_elbo/finite/cocycle_flow.py`, `capacity_pair_retention` /
  `_belief_orbit_coordinates`.
- Evidence: the amendment-6 charge referenced orbit coordinates to the first family member,
  so it shifted under a sample-shift gauge; the root-framed charge (coordinates carried to
  the block root by the spanning-tree transport) is exactly invariant under root-fixed
  shifts — measured deviation 1.9e-16 against 4.3e-2 for the family-referenced charge on
  the declared 4-cycle probe.
- Fix: the charge is root-framed, `s(x_B) = sum_a (k_a + t_a) mod 3`, declared as amendment 8.
  Re-measurement on the declared 6-cycle instances reverses the published null: R_cap 0.209
  vs 0.156 at k = 1 and 0.568 vs 0.441 at k = 3 (constant-sector control still exact, old
  values 0.144/0.406 reproduced under the retired charge before the change). STATUS section
  16, ROADMAP, Theory/07b, and both root manuscripts updated.
- Falsifies: unequal coarse pair sup between a plain and a root-gauged instance.

### F9 (LOW-MEDIUM) — worker interpreter numpy nondeterminism
- Location: `src/multiagent_elbo/finite/contraction_backend.py` (declared worker interpreter).
- Evidence: the 9.3e-8 discrepancy in the 8-cycle reduced step was numpy 2.0.0 (Anaconda
  worker) within-session nondeterminism (repeatability gap 1.27e-8), not a protocol bug;
  re-run on py314/numpy 2.4.4 with a fresh work directory agrees to 2.67e-15.
- Fix: documented as the module's reproducibility boundary — bit-level claims about
  worker-routed steps must pin the worker's numpy version, not only the interpreter path.
- Falsifies: a reproducibility claim about a worker-routed step that survives a numpy pin.

## Non-findings worth recording

- The sustained-over-injected ratio 1.246 uses the seed-step injection as denominator
  (0.5791 / 0.4648); the fixed-point injection (0.5021) gives 1.153. STATUS declares the
  seed-step convention; no discrepancy.
- `_blocked_action`'s einsum route, the moment-matching diagnostic, and the regenerated-row
  orientation all brute-force match to <= 1e-15.
